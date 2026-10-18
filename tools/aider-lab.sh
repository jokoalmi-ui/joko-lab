#!/usr/bin/env bash
# aider-lab.sh — Wrapper de Aider para el lab (worker #2, 14-ago-2026)
#
# Usa Aider 0.86.2 en su venv propio (~/.venv/aider) SIN tocar el venv RAG.
# Sigue el patrón del router local/cloud del lab:
#   - Por defecto: LM Studio local (R1-14B o el modelo que esté cargado)
#   - Con --cloud: DeepSeek (si se quiere el modelo principal)
#
# USO:
#   bash aider-lab.sh [opciones de aider]   → modelo local (LM Studio :1234)
#   bash aider-lab.sh --cloud ...           → modelo cloud DeepSeek
#
# NOTA: requiere LM Studio activo en :1234 (lmstudio-headless.sh tras reinicio).

VENV=/home/jokoalmi/.venv/aider/bin/aider
LM_BASE="http://localhost:1234/v1"   # endpoint OpenAI-compatible de LM Studio

if [ "${1:-}" = "--cloud" ]; then
    shift
    # Cloud: DeepSeek (misma API que usa Hermes). La key vive en el entorno
    # del gateway (config.yaml, protegida) — se pasa por env si está definida.
    if [ -z "${DEEPSEEK_API_KEY:-}" ]; then
        echo "ERROR: --cloud requiere DEEPSEEK_API_KEY en el entorno" >&2
        echo "  (la key vive en config.yaml del gateway — no se expone por Telegram)" >&2
        exit 1
    fi
    exec "$VENV" --model deepseek/deepseek-v4-flash \
        --api-key deepseek="$DEEPSEEK_API_KEY" "$@"
else
    # Local: LM Studio (OpenAI-compatible en :1234)
    exec "$VENV" --openai-api-base "$LM_BASE" \
        --model openai/deepseek-r1-distill-qwen-14b "$@"
fi
