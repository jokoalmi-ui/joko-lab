#!/bin/bash
# Verificación visual v2 de la ficha F1 — con redimensionado a ≤1024px (regla GLM del lab)
# El script glm_vision.py original manda la imagen a tamaño completo (1080x1350) y GLM
# degrada (content vacío / "no" a todo). Fix validado en skill infografia-html:
# redimensionar con PIL LANCZOS a ≤1024px ANTES de llamar a GLM.
# Uso: bash verificar_f1_v2.sh
set -u
GLM=/home/jokoalmi/.hermes/skills/creative/infografia-html/scripts/glm_vision.py
DIR=/home/jokoalmi/joko-lab/research/linkedin-lab/salidas/2026-09-01-ia-ml-dl-que-es-cada-uno
TMP=/tmp/f1_verify
mkdir -p "$TMP"

CHECK="Verifica esta slide de carrusel LinkedIn (1080x1350, mostrada reducida). Checklist: 1) fondo crema claro correcto 2) titulo visible y sin cortes 3) logo JL y marca Joko Lab visibles arriba 4) grafico central o listas visibles y sin solapamientos 5) sin texto cortado ni desbordado 6) pie de slide visible. Responde SOLO si/no por punto, sin razonar."

echo "=== Tamaños originales (descartar render vacío) ==="
ls -la "$DIR"/slide-*.png

for i in 01 02 03 04 05 06; do
  SRC="$DIR/slide-$i.png"
  DST="$TMP/slide-$i.png"
  python3 - "$SRC" "$DST" <<'EOF'
import sys
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
w, h = im.size
if w > 1024 or h > 1024:
    scale = 1024 / max(w, h)
    im = im.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
im.save(dst)
print(f"redimensionada: {w}x{h} -> {im.size[0]}x{im.size[1]}")
EOF
  echo "===== slide-$i ====="
  python3 "$GLM" "$DST" "$CHECK"
  echo ""
done
