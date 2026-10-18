#!/usr/bin/env bash
# Render ficha Founderz: HTML -> PNG (preview + verificación visual) y HTML -> PDF (entrega)
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
RENDER="/home/jokoalmi/joko-lab/tools/render_html.sh"   # helper unico HTML->PNG/PDF del lab

echo "== PNG =="
bash "$RENDER" "$DIR/ficha-actividad.html" "$DIR/ficha-actividad.png" 1180 3200

echo "== PDF =="
bash "$RENDER" --pdf "$DIR/ficha-actividad.html" "$DIR/ficha-actividad.pdf"

echo "== recorte del PNG =="
python3 "$DIR/recorta.py" "$DIR/ficha-actividad.png" || echo "recorte omitido"

echo "== resultado =="
ls -la "$DIR"
pdfinfo "$DIR/ficha-actividad.pdf" 2>/dev/null | sed -n '1,20p'
