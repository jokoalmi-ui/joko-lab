#!/usr/bin/env bash
# generar_recibo.sh — Congela y aprueba el árbol de cambios en staging.
#
# Ejecutar SOLO después de haber revisado el diff correspondiente.
# No revisa nada por sí mismo: certifica que "estos bytes exactos,
# revisados por X, quedan aprobados para commit".
#
# Uso:
#   ./generar_recibo.sh "nombre-de-quien-aprueba" ["nota opcional"]
#
# Ejemplos:
#   ./generar_recibo.sh joseba
#   ./generar_recibo.sh hermes "revisado tras auditoría de riesgo 2, sin hallazgos"

set -euo pipefail

if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "[joko-rdd] ERROR: no estás dentro de un repositorio git." >&2
  exit 1
fi

APROBADO_POR="${1:-}"
if [ -z "$APROBADO_POR" ]; then
  echo "[joko-rdd] ERROR: falta indicar quién aprueba." >&2
  echo "  Uso: ./generar_recibo.sh <nombre> [nota]" >&2
  exit 1
fi
NOTA="${2:-}"

TREE_SHA=$(git write-tree)
GIT_DIR=$(git rev-parse --git-dir)
RECIBO_FILE="${GIT_DIR}/joko-recibo.json"

# El recibo se escribe con python3 (el mismo interprete que usa el gate para
# validarlo). Antes se volcaba con un heredoc y la nota interpolada sin escapar:
# en cuanto la nota llevaba un salto de linea, unas comillas dobles o una barra
# invertida el JSON quedaba invalido, el gate lo leia como corrupto y BLOQUEABA
# el commit. Se escribe en un temporal y se sustituye con mv para que el gate
# nunca lea un recibo a medias.
TMP_RECIBO="${RECIBO_FILE}.tmp$$"
python3 - "$TMP_RECIBO" "$TREE_SHA" "$(date -Iseconds)" "$APROBADO_POR" "$NOTA" <<'PY'
import json, sys

destino, tree_sha, ts, aprobado_por, nota = sys.argv[1:6]
with open(destino, "w", encoding="utf-8") as fh:
    json.dump(
        {
            "tree_sha": tree_sha,
            "timestamp": ts,
            "aprobado_por": aprobado_por,
            "nota": nota,
        },
        fh,
        ensure_ascii=False,
        indent=2,
    )
    fh.write("\n")
PY
mv -f "$TMP_RECIBO" "$RECIBO_FILE"

echo "[joko-rdd] Recibo generado."
echo "  tree_sha:     ${TREE_SHA}"
echo "  aprobado_por: ${APROBADO_POR}"
echo "  guardado en:  ${RECIBO_FILE}"
echo ""
echo "  Cualquier cambio posterior en el staging invalidará este recibo."
