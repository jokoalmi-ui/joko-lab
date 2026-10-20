#!/bin/bash
# check-local-bin.sh — Verifica binarios criticos del lab
# Retorna: 0 = OK, 1 = WARNING (falta algun binario), 2 = ERROR (no existe ~/.local/bin)
#
# 2026-10-20: antes exigia que el binario estuviera en ~/.local/bin y salia
# siempre con exit 0 ("OK: 2/3"), asi que un binario ausente se veia verde.
# Ahora basta con que se resuelva en el PATH y el codigo de salida es real.

LOCAL_BIN="$HOME/.local/bin"

if [ ! -d "$LOCAL_BIN" ]; then
    echo "ERROR: $LOCAL_BIN no existe"
    exit 2
fi

# Binarios que deberian estar disponibles (ampliable)
EXPECTED=("hermes" "lms" "uvx")
LOCAL=0
EN_PATH=0
MISSING=()

for bin in "${EXPECTED[@]}"; do
    if [ -f "$LOCAL_BIN/$bin" ] || [ -L "$LOCAL_BIN/$bin" ]; then
        LOCAL=$((LOCAL + 1))
    elif command -v "$bin" >/dev/null 2>&1; then
        EN_PATH=$((EN_PATH + 1))
    else
        MISSING+=("$bin")
    fi
done

TOTAL=${#EXPECTED[@]}
DISPONIBLES=$((LOCAL + EN_PATH))

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "WARNING: faltan ${#MISSING[@]}/$TOTAL (${MISSING[*]}) | $LOCAL en ~/.local/bin, $EN_PATH en PATH"
    exit 1
fi

echo "OK: $DISPONIBLES/$TOTAL disponibles ($LOCAL en ~/.local/bin, $EN_PATH en PATH)"
exit 0
