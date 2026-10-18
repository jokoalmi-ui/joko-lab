#!/bin/bash
# Renderiza una slide montada sobre la hoja cuaderno base (1824x2310)
# Uso: bash render_montaje.sh [archivo.html] [salida.png]
set -e
cd /home/jokoalmi/joko-lab/tfm/slides

HTML="${1:-prueba-montaje.html}"
PNG="${2:-prueba-montaje.png}"

CHROME=$(which google-chrome 2>/dev/null || which chromium 2>/dev/null || which chromium-browser 2>/dev/null)
if [ -z "$CHROME" ]; then
  echo "ERROR: no se encontro Chrome/Chromium"
  exit 1
fi

echo "BINARIO: $CHROME"
"$CHROME" --headless --disable-gpu --virtual-time-budget=15000 \
  --screenshot="/home/jokoalmi/joko-lab/tfm/slides/$PNG" \
  --window-size=1824,2310 --hide-scrollbars \
  "file:///home/jokoalmi/joko-lab/tfm/slides/$HTML" 2>/dev/null

ls -la "/home/jokoalmi/joko-lab/tfm/slides/$PNG"
