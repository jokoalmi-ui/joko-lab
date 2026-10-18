#!/bin/bash
# check-uv.sh — Verifica que uv toolchain esta instalado
# Retorna: 0 = OK, 1 = WARNING, 2 = ERROR

UV_DIR="$HOME/.local/share/uv"

if ! command -v uv >/dev/null 2>&1; then
    echo "ERROR: uv no instalado"
    exit 2
fi

UV_VER=$(uv --version 2>/dev/null | head -1)
echo "OK: uv $UV_VER"

if [ ! -d "$UV_DIR" ]; then
    echo "WARNING: toolchain uv en $UV_DIR no existe"
    exit 1
fi

# uv moderno instala toolchains en python/ (la ruta toolchains/ es obsoleta)
TOOLCHAIN=$(ls "$UV_DIR/python/" 2>/dev/null | head -3)
if [ -z "$TOOLCHAIN" ]; then
    echo "WARNING: uv instalado pero sin toolchains"
    exit 1
fi

echo "OK: $UV_DIR/python (toolchains disponibles)"
exit 0
