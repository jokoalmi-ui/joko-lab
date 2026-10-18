#!/bin/bash
# check-path.sh — Verifica rutas criticas en PATH
# Retorna: 0 = OK, 1 = WARNING, 2 = ERROR

ERRORS=0
WARNINGS=0

check_in_path() {
    local dir="$1"
    local label="$2"
    local is_critical="${3:-no}"

    if echo "$PATH" | tr ':' '\n' | grep -qx "$dir"; then
        if [ -d "$dir" ]; then
            echo "OK: $label ($dir)"
        else
            echo "WARNING: $label en PATH pero el directorio no existe ($dir)"
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        if [ "$is_critical" = "critico" ]; then
            echo "ERROR: $label NO esta en PATH ($dir)"
            ERRORS=$((ERRORS + 1))
        else
            echo "WARNING: $label NO esta en PATH ($dir)"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
}

check_in_path "$HOME/.local/bin" "~/.local/bin" "critico"
check_in_path "$HOME/.cargo/bin" "~/.cargo/bin" "critico"
check_in_path "/usr/local/bin" "/usr/local/bin" "critico"
check_in_path "/usr/bin" "/usr/bin" "critico"

if [ "$ERRORS" -gt 0 ]; then
    exit 2
fi
if [ "$WARNINGS" -gt 0 ]; then
    exit 1
fi
exit 0
