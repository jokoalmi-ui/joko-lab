#!/usr/bin/env bash
# Wrapper de mapa_conocimiento.py — Mapa temático visual del conocimiento del RAG.
# Uso:
#   tools/mapa_conocimiento.sh                    # HTML en /tmp/mapa_conocimiento.html
#   tools/mapa_conocimiento.sh --out ruta.html    # salida personalizada
#   tools/mapa_conocimiento.sh --k 12             # número de clusters
exec ~/.venv/hermes-rag/bin/python3 "$(dirname "$0")/mapa_conocimiento.py" "$@"
