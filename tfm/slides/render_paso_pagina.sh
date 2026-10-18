#!/bin/bash
# Captura los frames del paso de pagina (page turn) y monta GIF + MP4
# Animacion: delay 0.3s + duracion 1.4s = fin en 1.7s
set -e
cd /home/jokoalmi/joko-lab/tfm/slides

CHROME=$(which google-chrome 2>/dev/null || which chromium 2>/dev/null || which chromium-browser 2>/dev/null)
[ -z "$CHROME" ] && { echo "ERROR: no Chrome"; exit 1; }

OUT=paso-pagina-frames
mkdir -p "$OUT"

# 8 momentos: antes, durante (4), despues, estabilizado
MOMENTS="0 400 700 1000 1300 1600 1900 2200"

i=0
for ms in $MOMENTS; do
  i=$((i+1))
  F=$(printf "%s/frame_%02d.png" "$OUT" "$i")
  "$CHROME" --headless --disable-gpu --virtual-time-budget="$ms" \
    --screenshot="$F" \
    --window-size=1824,2310 --hide-scrollbars \
    "file:///home/jokoalmi/joko-lab/tfm/slides/paso-pagina.html" 2>/dev/null
  echo "frame $i a ${ms}ms -> $F"
done

echo "--- montando con ffmpeg ---"
ffmpeg -y -framerate 5 -i "$OUT/frame_%02d.png" \
  -vf "scale=912:-1:flags=lanczos" -loop 0 paso-pagina.gif 2>/dev/null
ffmpeg -y -framerate 5 -i "$OUT/frame_%02d.png" \
  -vf "scale=912:-1:flags=lanczos" -c:v libx264 -pix_fmt yuv420p -crf 20 paso-pagina.mp4 2>/dev/null

ls -la paso-pagina.gif paso-pagina.mp4
