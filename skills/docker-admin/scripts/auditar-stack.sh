#!/usr/bin/env bash
# docker-admin: Ejecuta auditoría completa del stack + Hermes
# Uso: bash scripts/auditar-stack.sh
# Integra: healthcheck.sh (docker-admin) + hermes-diag.sh (hermes-expert)
set -uo pipefail

HERMES_LAB="/home/jokoalmi/hermes-lab"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "╔══════════════════════════════════════════╗"
echo "║  Auditoría completa del stack            ║"
echo "║  $TIMESTAMP              ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 1. Healthcheck Docker
echo "── 1. Healthcheck Docker ──"
if bash "$HERMES_LAB/skills/docker-admin/scripts/healthcheck.sh" --cron; then
    echo "  ✔  Docker OK"
else
    echo "  ✘  Docker: algún servicio falló"
fi
echo ""

# 2. Healthcheck específico n8n
echo "── 2. Healthcheck n8n ──"
if bash "$HERMES_LAB/skills/n8n-admin/healthcheck-n8n.sh" --quiet 2>/dev/null; then
    echo "  ✔  n8n OK (5/5 tests)"
else
    echo "  ✘  n8n: healthcheck falló"
fi
echo ""

# 3. Auditoría Hermes
echo "── 3. Auditoría Hermes ──"
if [ -f "$HERMES_LAB/skills/hermes-expert/hermes-diag.sh" ]; then
    bash "$HERMES_LAB/skills/hermes-expert/hermes-diag.sh" 2>&1 | head -30
    echo "  ... (ver ~/hermes-lab/skills/hermes-expert/ para completo)"
else
    echo "  hermes-diag.sh no encontrado (skill hermes-expert no completada)"
fi
echo ""

# 3. Espacio en disco
echo "── 3. Espacio en disco ──"
df -h / /mnt/ssd_ia_datos 2>/dev/null | head -2
echo ""

# 4. Últimos backups
echo "── 4. Últimos backups ──"
LS_OUTPUT=$(ls -1t /mnt/ssd_ia_datos/backups/ 2>/dev/null | head -5)
if [ -n "$LS_OUTPUT" ]; then
    echo "$LS_OUTPUT"
else
    echo "  No hay backups"
fi
echo ""

# 5. GPU
echo "── 5. GPU ──"
if command -v nvidia-smi &>/dev/null; then
    nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits 2>/dev/null
else
    echo "  nvidia-smi no disponible"
fi
echo ""

echo "── Auditoría completada ──"
