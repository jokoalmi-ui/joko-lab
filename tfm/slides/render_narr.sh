#!/bin/bash
# Renderiza los 11 slides narr-*.html sobre hoja-cuaderno-base.png (1824x2310)
# Uso: bash render_narr.sh
# NOTA: lista explícita de archivos (no glob) para evitar que el antiguo
# narr-09-resultados.html (renumerado a narr-11) capture el slot 09.
set -u
cd /home/jokoalmi/joko-lab/tfm/slides

CHROME=$(which google-chrome 2>/dev/null || which chromium 2>/dev/null || which chromium-browser 2>/dev/null)
if [ -z "$CHROME" ]; then
  echo "ERROR: no se encontro Chrome/Chromium"
  exit 1
fi
echo "BINARIO: $CHROME"

FILES="
narr-01-portada.html
narr-02-problema.html
narr-03-circuito.html
narr-04-modelos.html
narr-05-conocimiento.html
narr-06-memoria.html
narr-07-enrutador.html
narr-08-productos.html
narr-09-tecnologias.html
narr-10-etica.html
narr-11-resultados.html
"

for HTML in $FILES; do
  if [ ! -f "$HTML" ]; then
    echo "SKIP: no existe $HTML"
    continue
  fi
  OUT="${HTML%.html}.png"
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
ls -la narr-*.png
