#!/bin/sh
set -eu
mkdir -p assets/video/stereo-skis
if [ -z "${STEREO_PREVIEW_URL:-}" ]; then
  echo "Stereo Skis preview source unavailable; keeping fallback poster"
  exit 0
fi
curl --fail --silent --show-error --location --max-time 180 "$STEREO_PREVIEW_URL" --output /tmp/stereo-source.mp4
mkdir -p /tmp/norden-ffmpeg
cd /tmp/norden-ffmpeg
npm pack @ffmpeg-installer/linux-x64 --silent >/dev/null
tar -xf ffmpeg-installer-linux-x64-*.tgz
cd "$OLDPWD"
 /tmp/norden-ffmpeg/package/ffmpeg -hide_banner -loglevel error -y -i /tmp/stereo-source.mp4 -vf "scale=1280:-2" -c:v libx264 -preset veryfast -crf 27 -pix_fmt yuv420p -c:a aac -b:a 112k -movflags +faststart assets/video/stereo-skis/full.mp4
 /tmp/norden-ffmpeg/package/ffmpeg -hide_banner -loglevel error -y -ss 9 -i /tmp/stereo-source.mp4 -frames:v 1 -vf scale=1280:-2 -q:v 4 assets/video/stereo-skis/poster.jpg
 test -s assets/video/stereo-skis/full.mp4
