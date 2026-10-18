#!/usr/bin/env bash
# create-mcp-lab.sh — Crea un servidor MCP y lo registra en Hermes (Joko Lab)
#
# Automatiza el procedimiento validado en la skill mcp-lab (17/20-ago-2026,
# 3 MCPs reales: animation-server, lab-db, lancedb):
#   1. Venv dedicado (o --venv para reutilizar uno de dominio, patrón lancedb)
#   2. pip install fastmcp + mcp [+ deps extra]
#   3. Registro: hermes mcp add <nombre> --command <venv>/bin/python3 --args <server.py>
#   4. Verificación: hermes mcp list + hermes mcp test <nombre>
#
# USO:
#   bash create-mcp-lab.sh [--venv RUTA] [--force] <nombre> <ruta/server.py> [deps...]
#
#   --venv RUTA   reutilizar un venv existente (patrón lancedb: ahorra
#                 re-descargar torch/transformers, ~2GB). Por defecto crea
#                 un venv dedicado junto al server (patrón manim).
#   --force       sobrescribir el registro si el MCP ya existe en Hermes.
#   --dry-run     valida todo (venv, instalación, chequeos) pero NO registra
#                 en Hermes: muestra el comando hermes mcp add sin ejecutarlo.
#   deps...       paquetes extra a instalar (fastmcp y mcp van siempre).
#
# Ejemplos reales:
#   # Patrón manim (venv dedicado junto al server):
#   bash create-mcp-lab.sh animation-server ~/manim-mcp/server/animation_mcp.py \
#       "fastmcp==1.0" "manim>=0.19.0"
#   # Patrón lancedb (reutilizar venv de dominio con deps pesadas):
#   bash create-mcp-lab.sh --venv ~/.venv/hermes-rag lancedb \
#       ~/joko-lab/mcp/lancedb_server.py
#
# Reglas del lab aplicadas:
#   - Venv dedicado por servidor; --venv SOLO para venv de dominio con deps
#     pesadas (NUNCA el venv de Hermes ni el del sistema).
#   - No edita config.yaml a mano: siempre a través de hermes mcp add.
#   - Verificación de capa 1 (protocolo) con hermes mcp test. La capa 2
#     (uso real desde una sesión) se verifica aparte: /new o /reload-mcp.
#   - Si el server necesita un binario fuera de PATH (p.ej. manim), el
#     server.py debe leer la ruta desde env var (patrón MANIM_EXECUTABLE).

set -euo pipefail

NOMBRE=""
SERVER=""
VENV=""
FORCE=0
DRY_RUN=0
DEPS=()

while [ $# -gt 0 ]; do
    case "$1" in
        --venv)
            VENV="$2"; shift 2 ;;
        --force)
            FORCE=1; shift ;;
        --dry-run)
            DRY_RUN=1; shift ;;
        -h|--help)
            sed -n '2,32p' "$0"; exit 0 ;;
        *)
            if [ -z "$NOMBRE" ]; then
                NOMBRE="$1"
            elif [ -z "$SERVER" ]; then
                SERVER="$1"
            else
                DEPS+=("$1")
            fi
            shift ;;
    esac
done

if [ -z "$NOMBRE" ] || [ -z "$SERVER" ]; then
    echo "Uso: bash create-mcp-lab.sh [--venv RUTA] [--force] [--dry-run] <nombre> <ruta/server.py> [deps...]" >&2
    echo "  --venv RUTA   reutilizar venv existente (patrón lancedb); por defecto crea venv junto al server" >&2
    echo "  --force       sobrescribir registro si el MCP ya existe" >&2
    echo "  --dry-run     valida todo pero NO registra en Hermes (solo muestra el comando)" >&2
    echo "  deps...       paquetes extra (fastmcp y mcp se instalan siempre)" >&2
    exit 1
fi

if [ ! -f "$SERVER" ]; then
    echo "ERROR: no existe el server: $SERVER" >&2
    exit 1
fi

# No pisar un registro existente sin --force (regla del lab: confirmar antes)
if hermes mcp list 2>/dev/null | grep -qw "$NOMBRE"; then
    if [ "$FORCE" -eq 0 ]; then
        echo "ERROR: el MCP '$NOMBRE' ya está registrado en Hermes." >&2
        echo "  Si quieres actualizar su registro, repite con --force." >&2
        exit 1
    fi
    echo "→ '$NOMBRE' ya existía: se sobrescribirá el registro."
fi

# Venv: --venv explícito, o dedicado junto al server (patrón manim)
if [ -z "$VENV" ]; then
    DIR_SERVER="$(cd "$(dirname "$SERVER")" && pwd)"
    VENV="$DIR_SERVER/venv"
fi

if [ ! -x "$VENV/bin/python3" ]; then
    echo "→ Creando venv: $VENV"
    python3 -m venv "$VENV"
else
    echo "→ Venv OK: $VENV"
fi

echo "→ Instalando dependencias (fastmcp + mcp${DEPS:+ + extras}) ..."
if [ ${#DEPS[@]} -eq 0 ]; then
    "$VENV/bin/pip" install fastmcp mcp
else
    "$VENV/bin/pip" install fastmcp mcp "${DEPS[@]}"
fi

echo "→ Registrando en Hermes: hermes mcp add $NOMBRE ..."
if [ "$DRY_RUN" -eq 1 ]; then
    echo "  [DRY-RUN] no se ejecuta. Comando que se lanzaría:"
    echo "  echo 'Y' | hermes mcp add $NOMBRE --command $VENV/bin/python3 --args $SERVER"
    echo "  Verificación posterior: hermes mcp list && hermes mcp test $NOMBRE"
    exit 0
fi
# El prompt interactivo "Enable all N tools? [Y/n/select]" se responde con Y
echo "Y" | hermes mcp add "$NOMBRE" \
    --command "$VENV/bin/python3" \
    --args "$SERVER"

echo "→ Verificación:"
hermes mcp list
hermes mcp test "$NOMBRE"

echo "✅ MCP '$NOMBRE' creado y registrado."
echo "   Las tools se cargan en la PRÓXIMA sesión de Hermes (o /reload-mcp en la actual)."
