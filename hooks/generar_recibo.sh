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

cat > "$RECIBO_FILE" <<EOF
{
  "tree_sha": "${TREE_SHA}",
  "timestamp": "$(date -Iseconds)",
  "aprobado_por": "${APROBADO_POR}",
  "nota": "${NOTA}"
}
EOF

echo "[joko-rdd] Recibo generado."
echo "  tree_sha:     ${TREE_SHA}"
echo "  aprobado_por: ${APROBADO_POR}"
echo "  guardado en:  ${RECIBO_FILE}"
echo ""
echo "  Cualquier cambio posterior en el staging invalidará este recibo."
