#!/usr/bin/env bash
# archivar_baks.sh — archiva copias .bak en vez de borrarlas (reversible).
#
# Uso:
#   archivar_baks.sh                 -> DRY-RUN del nivel 1 (scripts)
#   archivar_baks.sh --scripts       -> DRY-RUN nivel 1
#   archivar_baks.sh --fichas        -> DRY-RUN nivel 2 (infografías)
#   archivar_baks.sh --scripts --apply
#   archivar_baks.sh --fichas  --apply
#
# Nivel 1: ~/.hermes/scripts/*.bak-*  -> ~/.hermes/_archive/<FECHA>/scripts/
# Nivel 2: joko-lab/research/infografias/**/*.bak* -> .../infografias/_archive-<FECHA>/
# Nunca borra: mueve con `mv -n` y preserva la ruta relativa. Reversible.
set -uo pipefail

FECHA="${FECHA:-$(date +%Y%m%d)}"
LEVEL="scripts"; APPLY=0
for a in "$@"; do
  case "$a" in
    --scripts) LEVEL="scripts" ;;
    --fichas)  LEVEL="fichas" ;;
    --apply)   APPLY=1 ;;
    *) echo "argumento no reconocido: $a"; exit 2 ;;
  esac
done

SIN_ORIGEN=(
  "perfume-del-dia-20261003/salaria_figura.bak-20261003.png"
  "perfume-del-dia-20261012/aquafortis_figura_RAMP.bak-20261012.png"
)

if [ "$LEVEL" = "scripts" ]; then
  SRC="$HOME/.hermes/scripts"; DEST="$HOME/.hermes/_archive/$FECHA/scripts"; RELBASE="$HOME/.hermes/scripts/"
  mapfile -t FILES < <(find "$SRC" -maxdepth 1 -type f -name '*.bak-*' | sort)
else
  SRC="$HOME/joko-lab/research/infografias"; DEST="$SRC/_archive-$FECHA"; RELBASE="$SRC/"
  mapfile -t FILES < <(find "$SRC" -type f -name '*.bak*' -not -path "*/_archive*" | sort)
fi

n=0; bytes=0; skipped=0
for f in "${FILES[@]}"; do
  rel="${f#$RELBASE}"
  orig="${f%%.bak*}"
  if [ ! -e "$orig" ]; then
    ok=0; for s in "${SIN_ORIGEN[@]}"; do [ "$rel" = "$s" ] && ok=1; done
    if [ "$ok" -eq 0 ]; then echo "SKIP (sin original, no declarado): $rel"; skipped=$((skipped+1)); continue; fi
  fi
  sz=$(stat -c %s "$f"); bytes=$((bytes+sz)); n=$((n+1))
  printf '%9.1f KB  %s\n' "$(awk -v s="$sz" 'BEGIN{printf "%.1f", s/1024}')" "$rel"
  if [ "$APPLY" -eq 1 ]; then
    mkdir -p "$DEST/$(dirname "$rel")"
    mv -n "$f" "$DEST/$rel" || { echo "ERROR moviendo $rel"; exit 1; }
  fi
done

printf '\nNIVEL=%s  TOTAL: %d ficheros, %.1f MB\n' "$LEVEL" "$n" "$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1048576}')"
[ "$skipped" -gt 0 ] && echo "SKIPPED: $skipped (quedan donde están)"
if [ "$APPLY" -eq 1 ]; then
  echo "ARCHIVADO en: $DEST"
  echo "Reversible: mv -n \"$DEST\"/**/* a su origen preservando ruta."
else
  echo "DRY-RUN: no se ha movido nada. Añade --apply para archivar."
fi
