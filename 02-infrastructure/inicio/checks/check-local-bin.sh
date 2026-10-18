#!/bin/bash
# check-local-bin.sh — Verifica binarios criticos en ~/.local/bin
# Retorna: 0 = OK, 1 = WARNING, 2 = ERROR

LOCAL_BIN="$HOME/.local/bin"

if [ ! -d "$LOCAL_BIN" ]; then
    echo "WARNING: $LOCAL_BIN no existe"
    exit 1
fi

# Binarios que deberian estar (ampliable)
EXPECTED=("hermes" "lms" "uvx")
FOUND=0
MISSING=0

for bin in "${EXPECTED[@]}"; do
    if [ -f "$LOCAL_BIN/$bin" ] || [ -L "$LOCAL_BIN/$bin" ]; then
        FOUND=$((FOUND + 1))
    else
        MISSING=$((MISSING + 1))
    fi
done

TOTAL_EXPECTED=${#EXPECTED[@]}
echo "OK: $FOUND/$TOTAL_EXPECTED binarios encontrados"
exit 0
