#!/usr/bin/env bash
# Diagnóstico rápido de Hermes Agent
# Uso: ./hermes-diag.sh
set -uo pipefail

HERMES_HOME="${HOME}/.hermes"
OK="  \xE2\x9C\x94"
WARN="  \xE2\x9A\xA0"
ERR="  \xE2\x9C\x96"

echo "=== Diagnostico Hermes Agent ==="
echo ""

# 1. Config
echo "-- Configuracion --"
if [[ -f "${HERMES_HOME}/config.yaml" ]]; then
    echo -e "${OK} config.yaml existe ($(wc -l < "${HERMES_HOME}/config.yaml") lineas)"
    DEFAULT_MODEL=$(grep -A1 'default:' "${HERMES_HOME}/config.yaml" | tail -1 | sed 's/.*name: //')
    echo "  Modelo por defecto: ${DEFAULT_MODEL:-?}"
else
    echo -e "${ERR} No existe config.yaml"
fi

# 2. state.db
echo ""
echo "-- Base de datos --"
if [[ -f "${HERMES_HOME}/state.db" ]]; then
    SIZE=$(du -h "${HERMES_HOME}/state.db" | cut -f1)
    echo -e "${OK} state.db ($SIZE)"
    SESIONES=$(sqlite3 "${HERMES_HOME}/state.db" "SELECT COUNT(*) FROM sessions;" 2>/dev/null || echo "0")
    MENSAJES=$(sqlite3 "${HERMES_HOME}/state.db" "SELECT COUNT(*) FROM messages;" 2>/dev/null || echo "0")
    echo "  Sesiones: ${SESIONES} | Mensajes: ${MENSAJES}"
else
    echo -e "${WARN} No existe state.db (primera ejecucion?)"
fi

# 3. Logs
echo ""
echo "-- Logs --"
for log in agent.log errors.log update.log; do
    if [[ -f "${HERMES_HOME}/logs/${log}" ]]; then
        LINES=$(wc -l < "${HERMES_HOME}/logs/${log}")
        echo -e "${OK} ${log} (${LINES} lineas)"
    else
        echo -e "${WARN} ${log} no existe"
    fi
done

# 4. Variables de entorno
echo ""
echo "-- Variables de entorno --"
if [[ -f "${HERMES_HOME}/.env" ]]; then
    ACTIVAS=$(grep -v '^#' "${HERMES_HOME}/.env" | grep -v '^$' | grep -v '^\s*$' | wc -l)
    echo -e "${OK} ${ACTIVAS} variables activas en .env"
    if grep -q "DEEPSEEK_API_KEY" "${HERMES_HOME}/.env"; then
        echo -e "${OK} DEEPSEEK_API_KEY presente"
    else
        echo -e "${WARN} DEEPSEEK_API_KEY ausente"
    fi
else
    echo -e "${ERR} No existe .env"
fi

# 5. Skills
echo ""
echo "-- Skills --"
SKILLS_DIR="${HERMES_HOME}/skills"
if [[ -d "${SKILLS_DIR}" ]]; then
    TOTAL=$(ls -d "${SKILLS_DIR}"/*/ 2>/dev/null | wc -l)
    CON_SKILL=$(find "${SKILLS_DIR}" -maxdepth 2 -name 'SKILL.md' -not -path '*/references/*' 2>/dev/null | wc -l)
    echo -e "${OK} ${TOTAL} skills instaladas, ${CON_SKILL} con SKILL.md"
else
    echo -e "${ERR} No existe directorio skills/"
fi

# 6. Permisos
echo ""
echo "-- Permisos --"
if [[ -O "${HERMES_HOME}" ]]; then
    echo -e "${OK} ~/.hermes/ pertenece a $(whoami)"
else
    echo -e "${ERR} ~/.hermes/ no pertenece al usuario actual"
fi

# 7. Espacio en disco
echo ""
echo "-- Espacio en disco --"
du -sh "${HERMES_HOME}" 2>/dev/null | sed 's/^/  /'

echo ""
echo "=== Fin del diagnostico ==="
echo "Ejecuta 'hermes doctor' para un chequeo mas profundo."
