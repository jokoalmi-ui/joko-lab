#!/bin/bash
# Renderiza la portada del TFM a PNG con Chrome headless
# Uso: bash render_portada.sh
set -e
cd /home/jokoalmi/joko-lab/tfm/slides

CHROME=$(which google-chrome 2>/dev/null || which chromium 2>/dev/null || which chromium-browser 2>/dev/null)
if [ -z "$CHROME" ]; then
  echo "ERROR: no se encontro Chrome/Chromium"
  exit 1
fi

echo "BINARIO: $CHROME"
"$CHROME" --headless --disable-gpu --virtual-time-budget=10000 \
  --screenshot=/home/jokoalmi/joko-lab/tfm/slides/01-portada-lab.png \
  --window-size=1200,900 --hide-scrollbars \
  "file:///home/jokoalmi/joko-lab/tfm/slides/01-portada-lab.html" 2>/dev/null

ls -la /home/jokoalmi/joko-lab/tfm/slides/01-portada-lab.png
