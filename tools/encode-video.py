#!/usr/bin/env python3
"""Create web assets from an original. Requires ffmpeg and ffprobe on PATH."""
import argparse
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('input', type=Path)
p.add_argument('slug', help='For example stereo-skis. Existing assets are never overwritten.')
p.add_argument('--webm', action='store_true', help='Keep VP9/Opus only if at least 25 percent smaller than MP4.')
a = p.parse_args()
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', a.slug):
    p.error('Use a lowercase slug with letters, numbers and single hyphens.')
if not a.input.is_file():
    p.error('Original file does not exist.')
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(a.input)]))
v = next(s for s in probe['streams'] if s['codec_type'] == 'video')
w, h = v['width'], v['height']
rotation = next((s.get('rotation', 0) for s in v.get('side_data_list', []) if 'rotation' in s), int(v.get('tags', {}).get('rotate', 0)))
if abs(int(rotation)) % 180 == 90:
    w, h = h, w
portrait = h > w
maxw, maxh = (1080, 1920) if portrait else (1920, 1080)
scale = f"scale=w='min({maxw},iw)':h='min({maxh},ih)':force_original_aspect_ratio=decrease:force_divisible_by=2,setsar=1"
duration = float(probe['format']['duration'])
if duration <= 0:
    p.error('Original duration is invalid.')
out = Path(__file__).resolve().parents[1] / 'assets' / 'video' / a.slug
out.mkdir(parents=True, exist_ok=False)

def run(args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', *args], check=True)

base = ['-i', str(a.input), '-map', '0:v:0', '-map', '0:a:0?', '-map_metadata', '-1', '-vf', scale]
run(base + ['-c:v', 'libx264', '-crf', '24', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', str(out/'full.mp4')])
start = min(2.0, duration / 4)
length = min(5.0, duration - start)
pw, ph = (404, 720) if portrait else (1280, 720)
preview_scale = f"scale=w='min({pw},iw)':h='min({ph},ih)':force_original_aspect_ratio=decrease:force_divisible_by=2,setsar=1"
run(['-ss', str(start), '-i', str(a.input), '-t', str(length), '-map', '0:v:0', '-map_metadata', '-1', '-vf', preview_scale, '-an', '-c:v', 'libx264', '-crf', '28', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out/'preview.mp4')])
run(['-ss', str(start), '-i', str(a.input), '-frames:v', '1', '-vf', preview_scale, '-map_metadata', '-1', '-c:v', 'libwebp', '-quality', '85', str(out/'poster.webp')])
if a.webm:
    run(base + ['-c:v', 'libvpx-vp9', '-crf', '34', '-b:v', '0', '-row-mt', '1', '-pix_fmt', 'yuv420p', '-c:a', 'libopus', '-b:a', '96k', str(out/'full.webm')])
    if (out/'full.webm').stat().st_size > (out/'full.mp4').stat().st_size * .75:
        (out/'full.webm').unlink()
        print('WebM omitted: saving was less than 25 percent.')
for f in sorted(out.iterdir()):
    print(f'{f.name}: {f.stat().st_size / 1_000_000:.2f} MB')
if (out/'full.mp4').stat().st_size > 25_000_000 or (out/'preview.mp4').stat().st_size > 2_000_000:
    print('REVIEW REQUIRED: size target exceeded. Adjust encode settings before committing.')
print('Watch every export, choose a suitable poster, and confirm the description and publication date before adding the project to the website.')
