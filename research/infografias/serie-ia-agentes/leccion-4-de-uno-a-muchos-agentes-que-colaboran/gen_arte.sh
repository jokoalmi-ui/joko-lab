#!/usr/bin/env bash
# Arte de la Leccion 4 (serie IA y agentes) — SDXL via gen_lab.py, 768px.
# Estilo de la serie: objeto pequeno centrado, fondo crema dominante, sin texto.
set -u
ART="/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes/leccion-4-de-uno-a-muchos-agentes-que-colaboran/arte"
GEN="/home/jokoalmi/joko-lab/tools/gen_lab.py"
mkdir -p "$ART"
ESTILO="tiny object centered, plain warm cream paper background filling almost the entire image, lots of empty space, thin black ink outlines, one small vivid orange accent, clean, no text, no words, no letters"

gen() {  # $1 fichero  $2 seed  $3 objeto
  echo "=== $1 (seed $2) ==="
  python3 "$GEN" "$3, $ESTILO" "$ART/$1" --size 768 --seed "$2" --steps 24 || echo "FALLO $1"
}

gen s1-tres-robots.png 41 "a small row of three identical tin toy robots standing in a line"
gen s2-fichas-rol.png 17 "three small blank round cardboard badges on a small table next to a closed notebook"
gen s5-lupa-revisora.png 64 "a small tin toy magnifying glass lying on a blank sheet of paper"
gen s7-fabrica-juguete.png 88 "a small tin toy factory building with a chimney"
echo "=== fin ==="
ls -la "$ART"
