#!/usr/bin/env bash
# docker-admin: Instala los cron jobs de mantenimiento del stack Docker
# Uso: bash scripts/install-cron.sh
set -uo pipefail

SCRIPTS_DIR="/home/jokoalmi/hermes-lab/skills/docker-admin/scripts"
CRON_LOG_DIR="/home/jokoalmi/hermes-lab/skills/docker-admin/logs"
CRONTAB_HEADER="# === docker-admin cron jobs (instalados el $(date '+%Y-%m-%d %H:%M')) ==="

mkdir -p "$CRON_LOG_DIR"

# Respaldar crontab actual si existe
crontab -l 2>/dev/null > /tmp/crontab.bak || true

# Eliminar bloque docker-admin previo si existe (para reinstalación limpia)
sed -i '/# === docker-admin cron jobs/,/# === fin docker-admin ===/d' /tmp/crontab.bak 2>/dev/null

# Escribir nuevo bloque
cat >> /tmp/crontab.bak << EOF
$CRONTAB_HEADER

# Healthcheck stack cada hora (minuto 5)
5 * * * * cd "$SCRIPTS_DIR" && bash healthcheck.sh --cron >> "$CRON_LOG_DIR/healthcheck.log" 2>&1 || notify-send "docker-admin" "Healthcheck falló: algún servicio no responde"

# Healthcheck específico n8n cada 30 minutos
*/30 * * * * bash /home/jokoalmi/hermes-lab/skills/n8n-admin/healthcheck-n8n.sh >> "$CRON_LOG_DIR/healthcheck-n8n.log" 2>&1 || notify-send "n8n-admin" "Healthcheck n8n falló"

# Backup diario de n8n a las 3:00
0 3 * * * cd "$SCRIPTS_DIR" && bash backup-volumen.sh n8n >> "$CRON_LOG_DIR/backup-n8n.log" 2>&1

# Backup diario de ollama a las 3:30
30 3 * * * cd "$SCRIPTS_DIR" && bash backup-volumen.sh ollama >> "$CRON_LOG_DIR/backup-ollama.log" 2>&1

# === fin docker-admin ===
EOF

crontab /tmp/crontab.bak
echo "✔  Cron jobs instalados."
echo ""
echo "Jobs activos:"
crontab -l | grep -A1 "docker-admin"
echo ""
echo "Logs: $CRON_LOG_DIR/"
echo "  - healthcheck.log"
echo "  - backup-n8n.log"
echo "  - backup-ollama.log"
echo ""
echo "Horarios:"
echo "  - Healthcheck: cada hora (minuto 5)"
echo "  - Backup n8n:   diario a las 3:00"
echo "  - Backup ollama: diario a las 3:30"
