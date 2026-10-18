#!/usr/bin/env bash
# Arte de la Leccion 2 (serie IA y agentes) — SDXL via gen_lab.py, 768px.
# Estilo de la serie: objeto pequeno centrado, fondo crema dominante, sin texto.
set -u
ART="/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes/leccion-2-el-modelo-conectado-al-mundo/arte"
GEN="/home/jokoalmi/joko-lab/tools/gen_lab.py"
mkdir -p "$ART"
ESTILO="tiny object centered, plain warm cream paper background filling almost the entire image, lots of empty space, thin black ink outlines, one small vivid orange accent, clean, no text, no words, no letters"

gen() {  # $1 fichero  $2 seed  $3 objeto
  echo "=== $1 (seed $2) ==="
  python3 "$GEN" "$3, $ESTILO" "$ART/$1" --size 768 --seed "$2" --steps 24 || echo "FALLO $1"
}

gen s1-puente.png 42 "a small wooden footbridge with rope railings"
gen s2-libro-llave.png 7 "an open blank book with a small brass key lying on it"
gen s5-calculadora-recibos.png 21 "a small solar calculator next to a stack of paper receipts"
gen s7-candado.png 11 "an open small padlock with its key on the side"
echo "=== fin ==="
ls -la "$ART"
