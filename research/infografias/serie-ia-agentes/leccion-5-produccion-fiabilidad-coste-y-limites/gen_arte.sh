#!/usr/bin/env bash
# Arte de la Leccion 5 (serie IA y agentes) — SDXL via gen_lab.py, 768px.
# Estilo de la serie: objeto pequeno centrado, fondo crema dominante, sin texto.
# Tras generar, normalizar_crema.py remapea el fondo a #F5EFE6 y deja los PNG
# "-crema" que son los que usa build_slides.py (asi no se ve costura con el
# fondo de las slides).
set -u
ART="/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes/leccion-5-produccion-fiabilidad-coste-y-limites/arte"
GEN="/home/jokoalmi/joko-lab/tools/gen_lab.py"
NORM="/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes/leccion-5-produccion-fiabilidad-coste-y-limites/normalizar_crema.py"
mkdir -p "$ART"
ESTILO="tiny object centered, plain warm cream paper background filling almost the entire image, lots of empty space, thin black ink outlines, one small vivid orange accent, clean, no text, no words, no letters"

gen() {  # $1 fichero  $2 seed  $3 objeto
  echo "=== $1 (seed $2) ==="
  python3 "$GEN" "$3, $ESTILO" "$ART/$1" --size 768 --seed "$2" --steps 24 || echo "FALLO $1"
}

gen s1-balanza.png 21 "a small tin toy weighing scale with a round dial standing on a blank sheet of paper"
gen s2-fichero-pruebas.png 53 "a small stack of blank white index cards held by a metal clip on a table"
gen s5-iman-trampa.png 72 "a small tin toy horseshoe magnet lying on a blank sheet of paper next to two tiny paper clips"
gen s7-candado-limite.png 96 "a small tin toy padlock with a short chain lying on a blank sheet of paper"

echo "=== normalizando fondo a crema (genera los -crema) ==="
python3 "$NORM" "$ART"
echo "=== fin ==="
ls -la "$ART"
