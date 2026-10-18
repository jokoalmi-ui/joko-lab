#!/bin/bash
# Captura 14 frames del page turn (?t=ms determinista, SIN --disable-gpu)
# Animacion: delay 500ms + dur 2000ms = fin en 2500ms
set -e
cd /home/jokoalmi/joko-lab/tfm/slides
CHROME=$(which google-chrome)
OUT=paso-pagina-frames
mkdir -p "$OUT"

MOMENTS="500 650 800 950 1100 1250 1400 1550 1700 1850 2000 2150 2300 2500"

i=0
for ms in $MOMENTS; do
  i=$((i+1))
  F=$(printf "%s/frame_%02d.png" "$OUT" "$i")
  timeout 50 "$CHROME" --headless --virtual-time-budget=6000 \
    --screenshot="$F" --window-size=1824,2310 --hide-scrollbars \
    "file:///home/jokoalmi/joko-lab/tfm/slides/paso-pagina.html?t=$ms" 2>/dev/null
  echo "t=$ms ms -> $(ls -la $F 2>/dev/null | awk '{print $5}') bytes"
done
