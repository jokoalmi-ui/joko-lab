#!/usr/bin/env bash
# Detector de cambios en config.yaml de Hermes
# Compara el archivo actual con una copia de referencia
# Instalar como cron: corre cada hora y avisa si hay cambios

set -uo pipefail

HERMES_HOME="${HOME}/.hermes"
CONFIG="${HERMES_HOME}/config.yaml"
SNAPSHOT="${HERMES_HOME}/config.snapshot"

if [[ ! -f "${CONFIG}" ]]; then
    echo "ERROR: No existe config.yaml"
    exit 1
fi

HASH_ACTUAL=$(md5sum "${CONFIG}" | cut -d' ' -f1)

if [[ ! -f "${SNAPSHOT}" ]]; then
    # Primera ejecucion: guardar referencia
    echo "${HASH_ACTUAL}" > "${SNAPSHOT}"
    echo "Snapshot de config.yaml creado por primera vez."
    exit 0
fi

HASH_REF=$(cat "${SNAPSHOT}")

if [[ "${HASH_ACTUAL}" != "${HASH_REF}" ]]; then
    echo "ALERTA: config.yaml ha cambiado desde el ultimo snapshot!"
    echo ""
    echo "Hash anterior: ${HASH_REF}"
    echo "Hash actual:   ${HASH_ACTUAL}"
    echo ""
    echo "Para ver diferencias:"
    echo "  diff -u ${CONFIG} <(cat ${CONFIG})"
    echo ""
    echo "Para actualizar el snapshot (si el cambio es intencionado):"
    echo "  md5sum ${CONFIG} | cut -d' ' -f1 > ${SNAPSHOT}"
else
    echo "OK: config.yaml no ha cambiado."
fi
