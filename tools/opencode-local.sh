#!/usr/bin/env bash
# opencode-local.sh — Lanza OpenCode con modelo LOCAL (Ollama) preparando la VRAM.
#
# Patron heredado del lab (validado):
#   - swap automatico LM Studio: llm-router.sh (11-ago) / llm_as_judge.py --swap (22-ago)
#   - restauracion del estado original al final (_restaurar_estado, 21-ago)
#
# Problema que resuelve: opencode con el provider ollama-local falla lento/silencioso
# si la VRAM esta ocupada por LM Studio (p.ej. GLM 4.6V): Ollama no coordina VRAM
# con LM Studio. Este wrapper libera la VRAM antes y restaura despues.
#
# Uso:
#   opencode-local.sh 'prompt' [args de opencode...]
#   OPENCODE_MODEL=ollama-local/deepseek-r1-distill-qwen-14b (default)
#   --force   ademas mata un llama-server de la GUI de LM Studio si ocupa VRAM
#             (NO restaurable automaticamente: la GUI queda sin modelo cargado)
#
# Salida: stdout/stderr de opencode. Codigo: el de opencode.

set -euo pipefail

export PATH="$HOME/.npm-global/bin:$PATH"

LM_API="http://localhost:1234/api/v0/models"
OPENCODE_MODEL="${OPENCODE_MODEL:-ollama-local/deepseek-r1-distill-qwen-14b}"
OLLAMA_MODEL="${OLLAMA_MODEL:-deepseek-r1-distill-qwen-14b}"
FORCE_GUI=0

# ── Parseo de flags ──
ARGS=()
for a in "$@"; do
    if [ "$a" = "--force" ]; then
        FORCE_GUI=1
    else
        ARGS+=("$a")
    fi
done
if [ "${#ARGS[@]}" -lt 1 ]; then
    echo "Uso: opencode-local.sh 'prompt' [--force]" >&2
    exit 2
fi

# ── Modelo cargado via lms (:1234) ──
_lms_cargado() {
    curl -s -m 5 "$LM_API" 2>/dev/null \
        | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    for m in d.get('data', []):
        if m.get('state') == 'loaded':
            print(m.get('id', ''))
            break
except Exception:
    pass
"
}

# ── llama-server de la GUI de LM Studio (fuera de lms) ──
_gui_llama_pid() {
    ps -eo pid=,cmd= 2>/dev/null \
        | grep "llama-server" \
        | grep -v "grep" \
        | grep -v "ollama" \
        | awk '{print $1; exit}'
}

ESTADO_LMS=""      # modelo lms cargado antes (para restaurar)
GUI_MATADO=0

# 1. Guardar estado original
ESTADO_LMS="$(_lms_cargado)"
echo "[opencode-local] Estado LM Studio (:1234): '${ESTADO_LMS:-ninguno}'" >&2

# 2. Gestionar ocupantes de VRAM
# 2a. llama-server de la GUI (no restaurable)
GUI_PID="$(_gui_llama_pid)"
if [ -n "$GUI_PID" ]; then
    if [ "$FORCE_GUI" -eq 1 ]; then
        echo "[opencode-local] Liberando VRAM: matando llama-server de la GUI (PID $GUI_PID)..." >&2
        kill "$GUI_PID" 2>/dev/null || true
        sleep 3
        GUI_MATADO=1
    else
        echo "[opencode-local] AVISO: la GUI de LM Studio tiene un llama-server activo (PID $GUI_PID)" >&2
        echo "[opencode-local] que no es restaurable via lms. Usa --force para matarlo y liberar VRAM." >&2
        exit 3
    fi
fi

# 2b. Modelo cargado via lms (:1234) — restaurable
if [ -n "$ESTADO_LMS" ]; then
    echo "[opencode-local] Descargando $ESTADO_LMS (lms unload) para liberar VRAM..." >&2
    timeout 60 lms unload "$ESTADO_LMS" >/dev/null 2>&1 || true
    sleep 2
fi

# 3. Ollama: si el modelo local ya esta cargado (p.ej. en CPU), descargarlo para
#    que la peticion de opencode lo recargue fresco — con VRAM libre, en GPU.
#    (API REST: el CLI ollama puede no estar en PATH de shells no interactivos)
if curl -s -m 3 http://localhost:11434/api/ps >/dev/null 2>&1; then
    if curl -s -m 3 http://localhost:11434/api/ps 2>/dev/null \
        | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    sys.exit(0 if any('$OLLAMA_MODEL' in m.get('name','') for m in d.get('models',[])) else 1)
except Exception:
    sys.exit(1)
"; then
        echo "[opencode-local] Ollama: descargando $OLLAMA_MODEL (recarga fresca en GPU)..." >&2
        curl -s -m 60 http://localhost:11434/api/generate \
            -d "{\"model\": \"$OLLAMA_MODEL\", \"keep_alive\": 0}" >/dev/null 2>&1 || true
        sleep 2
    fi
fi

# 4. Ejecutar opencode con el modelo local
echo "[opencode-local] Lanzando opencode con $OPENCODE_MODEL ..." >&2
set +e
opencode run "${ARGS[@]}" --model "$OPENCODE_MODEL"
RC=$?
set -e

# 5. Restaurar estado original (trap-like, tras opencode)
if [ -n "$ESTADO_LMS" ]; then
    echo "[opencode-local] Restaurando $ESTADO_LMS en LM Studio..." >&2
    timeout 180 lms load "$ESTADO_LMS" >/dev/null 2>&1 || \
        echo "[opencode-local] AVISO: no se pudo restaurar $ESTADO_LMS (cargalo manualmente)" >&2
fi
if [ "$GUI_MATADO" -eq 1 ]; then
    echo "[opencode-local] Nota: se mato el llama-server de la GUI de LM Studio." >&2
    echo "[opencode-local] Recargalo desde la GUI cuando necesites ese modelo (p.ej. GLM para vision)." >&2
fi

exit "$RC"
