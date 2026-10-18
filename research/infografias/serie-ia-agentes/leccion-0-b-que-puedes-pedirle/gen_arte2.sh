#!/usr/bin/env bash
# Reintento de las 2 escenas rechazadas (s2 cubos en rejilla full-bleed, s5 lamina de 5 llaves).
set -u
ART="/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes/leccion-0-b-que-puedes-pedirle/arte"
GEN="/home/jokoalmi/joko-lab/tools/gen_lab.py"
ESTILO="tiny object centered, plain warm cream paper background filling almost the entire image, lots of empty space, thin black ink outlines, one small vivid orange accent, clean, no text"
NEG="text, letters, words, numbers, typography, watermark, signature, poster, label, catalog sheet, grid, repeating pattern, full bleed, cluttered, blurry, low quality, distorted, photo, realistic, dark background, orange background"

echo "=== s2 reintento ==="
python3 "$GEN" "four small wooden cubes arranged in a single row with wide gaps between them, $ESTILO" "$ART/s2-cuatro-cubos.png" --size 768 --seed 5 --steps 26 --neg "$NEG" || echo "FALLO s2"
echo "=== s5 reintento ==="
python3 "$GEN" "three old metal keys lying loose in a row, the same design, different sizes, $ESTILO" "$ART/s5-tres-llaves.png" --size 768 --seed 17 --steps 26 --neg "$NEG" || echo "FALLO s5"
echo "=== fin reintento ==="
ls -la "$ART"
