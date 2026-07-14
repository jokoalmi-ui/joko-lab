#!/usr/bin/env bash
# provider-detect.sh — Detecta qué proveedor online usar según la hora
# Lee de /tmp/current-provider.txt (escrito por router-cron.sh)
# Si no existe el archivo, calcula por hora
#
# Uso: source provider-detect.sh → $ONLINE_PROVIDER, $ONLINE_MODEL, $ONLINE_BASE_URL

PROVIDER_FILE="/tmp/current-provider.txt"

if [ -f "$PROVIDER_FILE" ]; then
    # Leer del archivo de estado (escrito por router-cron.sh)
    ONLINE_PROVIDER=$(head -1 "$PROVIDER_FILE" 2>/dev/null)
else
    # Fallback: calcular por hora
    HORA=$(date +%H | sed 's/^0//')
    if [ "$HORA" -ge 3 ] && [ "$HORA" -lt 12 ]; then
        ONLINE_PROVIDER="gemini"
    else
        ONLINE_PROVIDER="deepseek"
    fi
fi

# Asignar modelo y URL según proveedor
case "$ONLINE_PROVIDER" in
    gemini)
        ONLINE_MODEL="gemini-3.1-flash-lite"
        ONLINE_BASE_URL="https://generativelanguage.googleapis.com/v1beta"
        ;;
    deepseek)
        ONLINE_MODEL="deepseek-v4-flash"
        ONLINE_BASE_URL="https://api.deepseek.com/v1"
        ;;
    *)
        ONLINE_PROVIDER="deepseek"
        ONLINE_MODEL="deepseek-v4-flash"
        ONLINE_BASE_URL="https://api.deepseek.com/v1"
        ;;
esac

export ONLINE_PROVIDER ONLINE_MODEL ONLINE_BASE_URL
