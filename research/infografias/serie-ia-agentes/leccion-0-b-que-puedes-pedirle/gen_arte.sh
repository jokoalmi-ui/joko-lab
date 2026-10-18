#!/usr/bin/env bash
# Arte de la Leccion 0-B (serie IA y agentes) — SDXL via gen_lab.py, 768px.
# Estilo de la serie: objeto pequeno centrado, fondo crema dominante, sin texto.
set -u
ART="/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes/leccion-0-b-que-puedes-pedirle/arte"
GEN="/home/jokoalmi/joko-lab/tools/gen_lab.py"
mkdir -p "$ART"
ESTILO="tiny object centered, plain warm cream paper background filling almost the entire image, lots of empty space, thin black ink outlines, one small vivid orange accent, clean, no text"

gen() {  # $1 fichero  $2 seed  $3 objeto
  echo "=== $1 (seed $2) ==="
  python3 "$GEN" "$3, $ESTILO" "$ART/$1" --size 768 --seed "$2" --steps 24 || echo "FALLO $1"
}

gen s1-caja-herramientas.png 42 "a small open toolbox with a wrench and a screwdriver inside"
gen s2-cuatro-cubos.png 7 "four identical small wooden cubes in a row"
gen s5-tres-llaves.png 21 "three keys of the same shape but different sizes in a row"
gen s6-reloj-arena.png 33 "a small hourglass next to a tiny brass balance scale"
gen s7-cuaderno.png 11 "a small closed notebook with a pen lying on top"
echo "=== fin ==="
ls -la "$ART"
