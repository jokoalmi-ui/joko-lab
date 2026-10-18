#!/bin/bash
# Renderiza la plantilla base cuaderno a PNG
# Uso: bash render_plantilla_cuaderno.sh
set -e
cd /home/jokoalmi/joko-lab/tfm/slides

CHROME=$(which google-chrome 2>/dev/null || which chromium 2>/dev/null || which chromium-browser 2>/dev/null)
if [ -z "$CHROME" ]; then
  echo "ERROR: no se encontro Chrome/Chromium"
  exit 1
fi

echo "BINARIO: $CHROME"
"$CHROME" --headless --disable-gpu --virtual-time-budget=10000 \
  --screenshot=/home/jokoalmi/joko-lab/tfm/slides/prueba-cuaderno-base.png \
  --window-size=1000,1260 --hide-scrollbars \
  "file:///home/jokoalmi/joko-lab/tfm/slides/plantilla-cuaderno-base.html" 2>/dev/null

ls -la /home/jokoalmi/joko-lab/tfm/slides/prueba-cuaderno-base.png
