#!/usr/bin/env bash
# commit-con-recibo.sh - commit con recibo de joko-git-recibos, fail-closed, generico.
#
#   bash commit-con-recibo.sh --fichero <ruta> --mensaje "<msg>" [opciones]
#
# Opciones:
#   --fichero <ruta>     fichero a commitear (repetible; staging SOLO de esos ficheros)
#   --mensaje "<texto>"  mensaje del commit
#   --nota "<texto>"     nota que se pasa al recibo (por defecto: mensaje)
#   --aprueba <quien>    quien aprueba (por defecto: $APRUEBA o "joseba")
#   --repo <ruta>        repositorio (por defecto: /home/jokoalmi/joko-lab)
#   --push               ademas empuja a origin y verifica en el bare
#   --apply              ejecuta de verdad (SIN --apply es dry-run: no commitea)
#
# Fail-closed, en este orden y abortando en el primer fallo:
#   1. el fichero esta modificado (git status --porcelain no vacio)
#   2. `git add` SOLO de los ficheros pedidos y staging == exactamente esos ficheros
#   3. blob del indice == blob del disco (git ls-files -s vs git hash-object)
#   4. recibo generado con hooks/generar_recibo.sh DESPUES de tener el staging listo
#   5. tree_sha del recibo == HEAD^{tree} tras el commit
#   6. con --push: `origin/rama..HEAD` vacio y comprobacion dentro del remoto
#
# Se niega a correr si hay ficheros ajenos en staging (los arrastraria al commit).
set -euo pipefail

REPO="/home/jokoalmi/joko-lab"
FICHEROS=()
MENSAJE=""
NOTA=""
APRUEBA="${APRUEBA:-joseba}"
APLICAR=0
PUSH=0

while [ $# -gt 0 ]; do
  case "$1" in
    --fichero)   FICHEROS+=("$2"); shift 2 ;;
    --mensaje)   MENSAJE="$2"; shift 2 ;;
    --nota)      NOTA="$2"; shift 2 ;;
    --aprueba)   APRUEBA="$2"; shift 2 ;;
    --repo)      REPO="$2"; shift 2 ;;
    --push)      PUSH=1; shift ;;
    --apply)     APLICAR=1; shift ;;
    -h|--help)   sed -n '2,25p' "$0"; exit 0 ;;
    *) echo "opcion desconocida: $1" >&2; exit 2 ;;
  esac
done

[ "${#FICHEROS[@]}" -gt 0 ] || { echo "ABORTA: falta --fichero" >&2; exit 2; }
[ -n "$MENSAJE" ]          || { echo "ABORTA: falta --mensaje" >&2; exit 2; }
[ -n "$NOTA" ] || NOTA="$MENSAJE"

cd "$REPO"
echo "== 0. estado del repo =="
echo "rama=$(git rev-parse --abbrev-ref HEAD)  HEAD=$(git rev-parse --short HEAD)"
echo "-- staging previo (debe estar vacio) --"
git diff --cached --name-only

# staging ajeno => abortar (git add -A arrastraria trabajo de otras tareas)
if [ -n "$(git diff --cached --name-only)" ]; then
  echo "ABORTA: ya hay ficheros en staging; commit sea o vacielos antes" >&2; exit 1
fi

for f in "${FICHEROS[@]}"; do
  if [ ! -f "$f" ]; then echo "ABORTA: no existe $f" >&2; exit 1; fi
  if [ -z "$(git status --porcelain -- "$f")" ]; then
    echo "ABORTA: $f no esta modificado respecto a HEAD (nada que commitear)" >&2; exit 1
  fi
done

echo "== 1. staging explicito =="
git add -- "${FICHEROS[@]}"
echo "-- ficheros en staging --"; git diff --cached --name-only
N_STAGED=$(git diff --cached --name-only | wc -l)
if [ "$N_STAGED" -ne "${#FICHEROS[@]}" ]; then
  echo "ABORTA: $N_STAGED ficheros en staging, se esperaban ${#FICHEROS[@]}" >&2; exit 1
fi
echo "-- diff staged --"; git diff --cached --stat

echo "== 2. blob del indice == blob del disco =="
for f in "${FICHEROS[@]}"; do
  IDX=$(git ls-files -s -- "$f" | awk '{print $2}')
  DISK=$(git hash-object -- "$f")
  if [ -z "$IDX" ] || [ "$IDX" != "$DISK" ]; then
    echo "ABORTA: blob indice ($IDX) != blob disco ($DISK) en $f" >&2; exit 1
  fi
  echo "   $f  $IDX"
done

if [ "$APLICAR" -eq 0 ]; then
  echo "== [dry-run] =="
  echo "   tree que se certificaria: $(git write-tree)"
  echo "   NO se commitea ni se empuja"
  git reset -q HEAD -- "${FICHEROS[@]}"     # deja el staging como estaba
  echo "FIN (dry-run)"
  exit 0
fi

echo "== 3. recibo =="
TREE=$(hooks/generar_recibo.sh "$APRUEBA" "$NOTA" | awk '/tree_sha:/ {print $2}')
[ -n "$TREE" ] || { echo "ABORTA: no se pudo leer el tree_sha del recibo" >&2; exit 1; }

echo "== 4. commit =="
git commit -q -m "$MENSAJE"
HEAD_TREE=$(git rev-parse HEAD^{tree})
if [ "$TREE" != "$HEAD_TREE" ]; then
  echo "ABORTA: recibo $TREE != HEAD^{tree} $HEAD_TREE" >&2; exit 1
fi
echo "   RECIBO_OK: $APRUEBA | tree $TREE | commit $(git rev-parse --short HEAD)"

if [ "$PUSH" -eq 1 ]; then
  echo "== 5. push a origin =="
  RAMA=$(git rev-parse --abbrev-ref HEAD)
  git push origin "$RAMA"
  echo "-- sin pushear (debe estar vacio) --"; git log --oneline "origin/$RAMA..HEAD"
  BARE=$(git remote get-url origin)
  echo "-- comprobacion dentro del remoto ($BARE) --"
  if [ -d "$BARE" ]; then
    git --git-dir="$BARE" log --oneline -1
  else
    echo "   (origin no es una ruta local; verificar en el remoto a mano)"
  fi
fi
echo "FIN"
