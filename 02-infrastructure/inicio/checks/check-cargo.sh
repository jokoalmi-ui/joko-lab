#!/bin/bash
# check-cargo.sh — Verifica que cargo y rust estan instalados
# Retorna: 0 = OK, 1 = WARNING, 2 = ERROR

if ! command -v cargo >/dev/null 2>&1; then
    echo "WARNING: cargo no instalado"
    exit 1
fi

CARGO_VER=$(cargo --version 2>/dev/null | head -1)
echo "OK: $CARGO_VER"
exit 0
