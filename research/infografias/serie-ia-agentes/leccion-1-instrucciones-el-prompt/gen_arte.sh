#!/usr/bin/env bash
# Arte de la Leccion 1 (serie IA y agentes) — SDXL via gen_lab.py, 768px.
# Estilo de la serie: objeto pequeno centrado, fondo crema dominante, sin texto.
set -u
ART="/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes/leccion-1-instrucciones-el-prompt/arte"
GEN="/home/jokoalmi/joko-lab/tools/gen_lab.py"
mkdir -p "$ART"
ESTILO="tiny object centered, plain warm cream paper background filling almost the entire image, lots of empty space, thin black ink outlines, one small vivid orange accent, clean, no text, no words, no letters"

gen() {  # $1 fichero  $2 seed  $3 objeto
  echo "=== $1 (seed $2) ==="
  python3 "$GEN" "$3, $ESTILO" "$ART/$1" --size 768 --seed "$2" --steps 24 || echo "FALLO $1"
}

gen s1-cartel-flecha.png 42 "a small wooden signpost with one arrow, blank sign board"
gen s2-tres-piezas.png 7 "three small wooden blocks fitting together like a puzzle"
gen s3-embudo.png 33 "a small tin funnel standing upright"
gen s5-dos-formas.png 21 "a crumpled sheet of paper next to a flat blank index card"
gen s7-cuaderno.png 11 "a small closed notebook with a pen lying on top"
echo "=== fin ==="
ls -la "$ART"
