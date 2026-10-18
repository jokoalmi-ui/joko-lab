#!/usr/bin/env bash
# Arte de la Leccion 3 (serie IA y agentes) — SDXL via gen_lab.py, 768px.
# Estilo de la serie: objeto pequeno centrado, fondo crema dominante, sin texto.
set -u
ART="/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes/leccion-3-el-agente-el-bucle/arte"
GEN="/home/jokoalmi/joko-lab/tools/gen_lab.py"
mkdir -p "$ART"
ESTILO="tiny object centered, plain warm cream paper background filling almost the entire image, lots of empty space, thin black ink outlines, one small vivid orange accent, clean, no text, no words, no letters"

gen() {  # $1 fichero  $2 seed  $3 objeto
  echo "=== $1 (seed $2) ==="
  python3 "$GEN" "$3, $ESTILO" "$ART/$1" --size 768 --seed "$2" --steps 24 || echo "FALLO $1"
}

gen s1-noria.png 5 "a small ferris wheel of a fairground ride"
gen s2-caja-herramientas.png 29 "a small open metal toolbox with a few hand tools beside a small closed notebook"
gen s5-etiquetas-precio.png 13 "three small blank paper price tags on strings next to a small notebook"
gen s7-llave-etiqueta.png 77 "a small brass key with a plain paper tag tied to it"
echo "=== fin ==="
ls -la "$ART"
