#!/bin/bash
# Renderiza los 8 slides gui-*.html sobre hoja-cuaderno-base.png (1824x2310)
# Uso: bash render_gui.sh
set -u
cd /home/jokoalmi/joko-lab/tfm/slides

CHROME=$(which google-chrome 2>/dev/null || which chromium 2>/dev/null || which chromium-browser 2>/dev/null)
if [ -z "$CHROME" ]; then
  echo "ERROR: no se encontro Chrome/Chromium"
  exit 1
fi
echo "BINARIO: $CHROME"

for i in 01 02 03 04 05 06 07 08; do
  HTML="gui-${i}-"*.html
  PNG="gui-${i}-"*.png
  # Expandir glob (si hay varios, tomar el primero)
  HTML=$(ls gui-${i}-*.html 2>/dev/null | head -1)
  if [ -z "$HTML" ]; then
    echo "SKIP: no hay html gui-${i}-"
    continue
  fi
  BASE="${HTML%.html}"
  OUT="${BASE}.png"
  echo "== Render $HTML -> $OUT"
  timeout 120 "$CHROME" --headless --disable-gpu --virtual-time-budget=15000 \
    --screenshot="/home/jokoalmi/joko-lab/tfm/slides/$OUT" \
    --window-size=1824,2310 --hide-scrollbars \
    "file:///home/jokoalmi/joko-lab/tfm/slides/$HTML" 2>/dev/null
  if [ -f "$OUT" ]; then
    ls -la "$OUT"
  else
    echo "FALLO: no se genero $OUT"
  fi
done

echo "=== RESUMEN ==="
ls -la gui-*.png
