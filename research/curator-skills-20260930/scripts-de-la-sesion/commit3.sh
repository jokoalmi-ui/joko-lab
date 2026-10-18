#!/usr/bin/env bash
# commit3.sh - dos commits con recibo (RULE-018 rectificada | addendum de OBS-154) + push a origin.
#
#   bash commit3.sh            # DRY-RUN: no commitea ni empuja
#   bash commit3.sh --apply    # commitea los dos y empuja a origin
#
# Fail-closed: staging SOLO del fichero de cada commit, blob del indice == blob del disco,
# recibo generado con hooks/generar_recibo.sh y tree_sha del recibo == HEAD^{tree}.
set -euo pipefail

REPO=/home/jokoalmi/joko-lab
RULE=01-knowledge/objects/RULE-018.yaml
OBS=01-knowledge/observations/OBS-154-curador-edita-skills-sin-ok-2026-09-30.md
MSG_A="regla: RULE-018 - el corte efectivo del curador es la PROPIEDAD de la skill (created_by), no 'pause'; dos cifras rectificadas con instrumento (30-sep-2026)"
MSG_B="obs: OBS-154 addendum - el conteo del curador subio a 55 tras cerrar el OBS y el pase corre POR TURNO dentro de la sesion del agente"
APRUEBA="${APRUEBA:-joseba}"
APLICAR=0
[ "${1:-}" = "--apply" ] && APLICAR=1

cd "$REPO"
echo "== 0. estado =="
git status --porcelain | head -20
echo "HEAD=$(git rev-parse --short HEAD)  rama=$(git rev-parse --abbrev-ref HEAD)"

verificar_staging() {   # $1 = ruta
  local idx disk
  idx=$(git ls-files -s -- "$1" | awk '{print $2}')
  disk=$(git hash-object -- "$1")
  if [ -z "$idx" ] || [ "$idx" != "$disk" ]; then
    echo "ABORTA: blob del indice ($idx) != blob del disco ($disk) en $1" >&2; exit 1
  fi
  echo "  blob indice == blob disco: $idx"
}

commit_uno() {          # $1 = ruta, $2 = mensaje, $3 = nota del recibo
  echo "== staging de $1 =="
  git add -- "$1"
  verificar_staging "$1"
  echo "-- diff staged --"
  git diff --cached --stat -- "$1"
  echo "-- ficheros staged (debe ser 1) --"
  git diff --cached --name-only
  local n; n=$(git diff --cached --name-only | wc -l)
  [ "$n" -eq 1 ] || { echo "ABORTA: hay $n ficheros en staging, se esperaba 1" >&2; exit 1; }
  if [ "$APLICAR" -eq 0 ]; then
    echo "  [dry-run] tree que se certificaria: $(git write-tree)"
    echo "  [dry-run] NO se commitea"
    git reset -q HEAD -- "$1"   # deja el staging como estaba
    return 0
  fi
  echo "== recibo =="
  local tree; tree=$(hooks/generar_recibo.sh "$APRUEBA" "$3" | awk '/tree_sha:/ {print $2}')
  [ -n "$tree" ] || { echo "ABORTA: no se pudo leer el tree_sha del recibo" >&2; exit 1; }
  echo "== commit =="
  git commit -q -m "$2"
  local head_tree; head_tree=$(git rev-parse HEAD^{tree})
  [ "$tree" = "$head_tree" ] || { echo "ABORTA: recibo $tree != HEAD^{tree} $head_tree" >&2; exit 1; }
  echo "  RECIBO_OK: $APRUEBA | tree $tree | $(git rev-parse --short HEAD)"
}

echo "== 1. commit A: $RULE =="
commit_uno "$RULE" "$MSG_A" "rectificacion RULE-018 (created_by) verificada contra disco y contra el literal del curador"
echo "== 2. commit B: $OBS =="
commit_uno "$OBS" "$MSG_B" "addendum aditivo de OBS-154 (backup .bak-obs154-addendum-drift-20260930)"

echo "== 3. push a origin =="
if [ "$APLICAR" -eq 0 ]; then
  echo "  [dry-run] git push origin master (pendientes: $(git log --oneline origin/master..HEAD | wc -l))"
else
  git push origin master
  echo "== 4. verificacion =="
  echo "-- sin pushear (debe estar vacio) --"; git log --oneline origin/master..HEAD
  echo "-- ultimos 3 --"; git log --oneline -3
  echo "-- los dos ficheros (debe estar vacio) --"; git status --porcelain -- "$RULE" "$OBS"
fi
echo "FIN"
