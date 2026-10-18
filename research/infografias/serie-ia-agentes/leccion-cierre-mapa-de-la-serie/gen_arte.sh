#!/usr/bin/env bash
# Arte de la PIEZA DE CIERRE (serie IA y agentes) — SDXL via gen_lab.py, 768px.
# Estilo de la serie: objeto pequeno centrado, fondo crema dominante, sin texto.
# Tras generar, normalizar_crema.py remapea el fondo a #F5EFE6 y deja los PNG
# "-crema" que son los que usa build_slides.py.
# Reanudable: si un PNG ya existe y no esta vacio, se salta. Lock para no
# lanzar dos corridas a la vez (ComfyUI comparte VRAM con el VLM: nunca a la vez).
set -u
PIEZA="/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes/leccion-cierre-mapa-de-la-serie"
ART="$PIEZA/arte"
GEN="/home/jokoalmi/joko-lab/tools/gen_lab.py"
NORM="$PIEZA/normalizar_crema.py"
LOCK="/tmp/cierre_arte.lock"
mkdir -p "$ART"

exec 9>"$LOCK"
flock -n 9 || { echo "LOCK OCUPADO: ya hay una corrida de arte en marcha ($LOCK)"; exit 3; }

ESTILO="tiny object centered, plain warm cream paper background filling almost the entire image, lots of empty space, thin black ink outlines, one small vivid orange accent, clean, no text, no words, no letters"

gen() {  # $1 fichero  $2 seed  $3 objeto
  if [ -s "$ART/$1" ]; then echo "=== $1 ya existe ($(stat -c%s "$ART/$1") B): se salta ==="; return 0; fi
  echo "=== $1 (seed $2) ==="
  python3 "$GEN" "$3, $ESTILO" "$ART/$1" --size 768 --seed "$2" --steps 24 || echo "FALLO $1"
}

gen s1-escalera.png 202 "a small tin toy staircase with six steps standing on a blank sheet of paper"
gen s5-torre-capas.png 214 "a small tin toy stack of nested round boxes standing on a blank sheet of paper"
gen s7-llave.png 226 "a small tin toy key with a short orange ribbon lying on a blank sheet of paper"

echo "=== normalizando fondo a crema (genera los -crema) ==="
python3 "$NORM" "$ART"
echo "=== fin ==="
ls -la "$ART"
