#!/usr/bin/env python3
"""Convert a locally synced /NC Dropbox directory into gallery WebP assets.

Usage:
  python3 -m pip install Pillow
  python3 tools/import-gallery.py --source "/path/to/Dropbox/NC" --dry-run
  python3 tools/import-gallery.py --source "/path/to/Dropbox/NC" --write

This program never modifies the Dropbox originals. It only writes WebP files
listed in assets/media.json. Source names and output names remain deterministic.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "media.json"


def locate(source: Path, original: str) -> Path | None:
    relative = Path(original)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Unsafe source path: {original}")
    candidates = [source / relative]
    if relative.parts and relative.parts[0].casefold() == "bilder":
        candidates.insert(0, source / "Intersport" / relative)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def target_path(value: str) -> Path:
    if not value.startswith("/assets/img/") or ".." in Path(value).parts:
        raise ValueError(f"Unsafe output: {value}")
    return ROOT / value.lstrip("/")


def convert(source: Path, dest: Path, size: tuple[int, int], quality: int) -> None:
    # Work in RGB, respect camera orientation and crop to the editorial frame.
    with Image.open(source) as img:
        image = ImageOps.exif_transpose(img).convert("RGB")
        image = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        temp = dest.with_suffix(".tmp.webp")
        try:
            image.save(temp, format="WEBP", quality=quality, method=6)
            temp.replace(dest)
        finally:
            temp.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Synced Dropbox /NC directory")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--force", action="store_true", help="Overwrite already exported images")
    args = parser.parse_args()
    source = args.source.expanduser().resolve()
    if not source.is_dir():
        parser.error(f"Source folder not found: {source}")
    items = json.loads(MANIFEST.read_text(encoding="utf-8"))
    missing, failures = [], []
    written = skipped = 0
    for idx, item in enumerate(items, 1):
        original = item.get("original")
        if not isinstance(original, str):
            failures.append(f"Gallery entry {idx}: missing original path")
            continue
        try:
            raw = locate(source, original)
            if raw is None:
                missing.append(original)
                continue
            targets = [
                (target_path(item["src"]), (int(item["width"]), int(item["height"])), 82),
                (target_path(item["small"]), (int(item["smallWidth"]), int(item["smallHeight"])), 78),
            ]
            for dest, size, quality in targets:
                if size[0] <= 0 or size[1] <= 0:
                    raise ValueError(f"Invalid dimensions: {size}")
                if dest.exists() and not args.force:
                    skipped += 1
                    continue
                if args.dry_run:
                    print(f"PLAN {raw} -> {dest.relative_to(ROOT)} ({size[0]}x{size[1]})")
                else:
                    convert(raw, dest, size, quality)
                    written += 1
        except (OSError, KeyError, ValueError, UnidentifiedImageError) as exc:
            failures.append(f"{original}: {exc}")
    print(f"Gallery entries: {len(items)} | Written: {written} | Already present: {skipped} | Missing originals: {len(missing)} | Errors: {len(failures)}")
    for name in sorted(set(missing)):
        print("MISSING SOURCE:", name)
    for error in failures:
        print("ERROR:", error)
    return 1 if missing or failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
