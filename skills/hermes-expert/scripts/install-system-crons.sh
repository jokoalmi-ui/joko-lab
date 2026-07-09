#!/usr/bin/env bash
# Instalador de crons del sistema para Hermes
# Ejecutar: bash ~/hermes-lab/skills/hermes-expert/scripts/install-system-crons.sh

set -euo pipefail

SCRIPTS_DIR="/home/jokoalmi/hermes-lab/skills/hermes-expert/scripts"
DETECT_SCRIPT="${SCRIPTS_DIR}/detect-config-changes.sh"
DIAG_SCRIPT="${SCRIPTS_DIR}/hermes-diag-system.sh"

# Copiar scripts a ~/ si no están ya
cp /home/jokoalmi/hermes-lab/skills/hermes-expert/hermes-diag.sh "${DIAG_SCRIPT}" 2>/dev/null || true
chmod +x "${DIAG_SCRIPT}"

# Crear crontab
cat << 'EOF' > /tmp/hermes-crontab
# Crons del sistema para Hermes Agent
# Auditoria diaria: se ejecuta a las 08:00
0 8 * * * /home/jokoalmi/hermes-lab/skills/hermes-expert/scripts/hermes-diag-system.sh | logger -t hermes-diag

# Deteccion de cambios en config.yaml: cada hora
0 * * * * /home/jokoalmi/hermes-lab/skills/hermes-expert/scripts/detect-config-changes.sh | logger -t hermes-config-watch
EOF

echo "Se ha generado /tmp/hermes-crontab"
echo ""
echo "Para instalarlo, ejecuta:"
echo "  crontab /tmp/hermes-crontab"
echo ""
echo "Para verificar:"
echo "  crontab -l"
