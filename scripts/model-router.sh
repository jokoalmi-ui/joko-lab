#!/usr/bin/env bash
# model-router.sh — Router horario para Hermes Agent
# Cambia el modelo activo según la hora para evitar sobrecoste de DeepSeek
#
# Franja cara DeepSeek (facturación ×2): 03:00 - 12:00 España → Gemini 3.1 Flash Lite
# Resto del día → DeepSeek (configuración por defecto)
#
# Instalación: Añadir al final de ~/.bashrc:
#   source /home/jokoalmi/hermes-lab/scripts/model-router.sh
#
# El script NO modifica config.yaml. Solo exporta HERMES_MODEL
# que Hermes respeta como override sobre model.default.

HORA=$(date +%H)
HORA=${HORA#0}  # quitar cero inicial para evitar problemas en bash

if [ "$HORA" -ge 3 ] && [ "$HORA" -lt 12 ]; then
    # Franja cara — usamos Gemini
    export HERMES_MODEL="gemini-3.1-flash-lite"
else
    # Franja normal — DeepSeek (no hace falta exportar, es el default)
    unset HERMES_MODEL
fi
