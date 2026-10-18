#!/usr/bin/env bash
# llm-router.sh — Router local/cloud por TIPO DE TAREA (09-ago-2026; gpt-oss 19-ago-2026)
#
# Decide qué motor usa una tarea SIN tocar config.yaml (el modelo principal
# de Hermes sigue siendo deepseek cloud; este router es solo para tareas
# batch/delegadas).
#
# Uso:
#   llm-router.sh batch "prompt"          → ejecuta con gpt-oss-20b local (LM Studio)
#   llm-router.sh batch-json "prompt"     → igual pero pide JSON estricto
#   llm-router.sh auto "prompt"           → PREESTIMA el modelo por tipo de tarea
#                                            (pipeline_seleccion_modelo.py + tabla YAML)
#                                            y ejecuta con el ganador (auto-carga/swap)
#   llm-router.sh check                   → muestra qué motor tocaría cada tipo
#
# Reglas (validado 19-ago-2026, batería de producción 5x5 vs R1-14B):
#   - batch / resumen / clasificacion / extraccion → LOCAL (gpt-oss-20b, VALIDADO
#     96% razonamiento duro, 0 cortes, 3-15x más rápido que R1)
#   - vision → LOCAL (GLM 4.6V)
#   - interactivo / razonamiento complejo → CLOUD (deepseek, ya configurado)
#
# Salida: stdout = respuesta del motor. Código: 0 OK, 2 motor local no disponible.

set -euo pipefail

# PATH autogestionado (13-oct-2026, RULE-021): el planificador (systemd, gateway)
# NO hereda el PATH del shell interactivo, asi que 'lms' no se encontraba y su
# error real se descartaba (>/dev/null 2>&1). Garantizamos aqui la ruta del binario.
LMS_BIN_DIR="${LMS_BIN_DIR:-$HOME/.lmstudio/bin}"
case ":$PATH:" in
    *":$LMS_BIN_DIR:"*) ;;
    *) PATH="$PATH:$LMS_BIN_DIR" ;;
esac
export PATH

LM_API="http://localhost:1234/api/v0/chat/completions"
LM_MODEL="${LM_MODEL:-openai/gpt-oss-20b}"
# Modelo por defecto si el indicado no esta cargado (fallback razonable)
LM_MODEL_FALLBACK="glm-4.6v-flash"
TIMEOUT_S=300

# Espejo local (11-oct-2026): cada consulta local anota sus tokens en
# 04-operations/metrics/ahorro_local_ledger.jsonl para poder calcular
# "USD evitados" con la tabla de tarifas de coste_ahorro.py. Es aditivo y
# defensivo: si el registrador falla, el router sigue (|| true).
LEDGER_LOCAL="${LEDGER_LOCAL:-$HOME/joko-lab/tools/ledger_local.py}"
LEDGER_LOG="${LEDGER_LOG:-$HOME/joko-lab/04-operations/metrics/ahorro_local.log}"

# ── Detectar si un modelo esta cargado en LM Studio ──
# Verifica el CAMPO state:loaded (el ID aparece tambien en modelos no cargados)
_model_cargado() {
    local buscado="$1"
    curl -s -m 5 "http://localhost:1234/api/v0/models" 2>/dev/null \
        | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    for m in d.get('data', []):
        if m.get('id') == '$buscado' and m.get('state') == 'loaded':
            sys.exit(0)
    sys.exit(1)
except Exception:
    sys.exit(1)
"
}

# ── Arrancar el servidor BAJO DEMANDA (13-oct-2026) ──
# Motivacion: con el PC recien encendido y sin abrir la app, :1234 esta caido y
# el router se plantaba => el trabajo caia a cloud (coste) o fallaba.
# Diseno: UN arranque headless ('lms server start', no necesita GUI ni auth de
# Xwayland), con lock (varios jobs a las 12:01 no deben pelearse) y con el exito
# acreditado en el PUERTO, no en el rc: un rc=0 con :1234 caido seria un falso ok
# (RULE-021). La salida real de 'lms' NUNCA se silencia.
# Escape (comportamiento antiguo): LMSTUDIO_ASEGURAR_OFF=1
_asegurar_servidor() {
    if [ "${LMSTUDIO_ASEGURAR_OFF:-0}" = "1" ]; then
        echo "ERROR: :1234 caido y el arranque bajo demanda esta desactivado (LMSTUDIO_ASEGURAR_OFF=1)" >&2
        return 2
    fi
    # RULE-021: el planificador no hereda el PATH; si el binario no esta, se DICE.
    if ! command -v lms >/dev/null 2>&1; then
        echo "ERROR: binario 'lms' no encontrado en PATH=$PATH" >&2
        return 2
    fi
    local lock="/tmp/lmstudio-asegurar.lock"
    exec 9>"$lock"
    if flock -n 9; then
        echo "  :1234 caido — arrancando el servidor bajo demanda ('lms server start')..." >&2
        local sal
        # OJO (13-oct-2026, medido): 'lms server start' lanza la app DESPRENDIDA y
        # el hijo heredaba los fds sin CLOEXEC => la app se quedaba con ESTE lock
        # para siempre y todo arranque posterior moria esperando 60s a un "otro
        # proceso" que ya no existia. El arranque va en un subshell con el fd 9
        # cerrado; el padre conserva el suyo (el lock sigue vivo hasta el final).
        sal=$( ( exec 9>&-; timeout 90 lms server start ) 2>&1 ) || true
        printf '  salida real de lms server start: %s\n' "${sal:-<sin salida>}" >&2
    else
        echo "  :1234 caido — otro proceso ya lo esta arrancando; espero sin duplicar" >&2
    fi
    local i
    for i in $(seq 1 30); do
        if curl -s -m 2 "http://localhost:1234/api/v0/models" >/dev/null 2>&1; then
            echo "  servidor local ARRIBA (comprobado en el puerto, intento $i, tras $((i*2))s)" >&2
            exec 9>&-
            return 0
        fi
        sleep 2
    done
    exec 9>&-
    echo "ERROR: :1234 sigue sin responder 60s despues del arranque bajo demanda" >&2
    return 2
}

# ── Cargar un modelo bajo demanda (si LM Studio esta activo) ──
# Devuelve 0 si el modelo queda cargado, 2 si no se pudo.
# Si la carga falla por VRAM (otro modelo ocupa), hace SWAP automatico:
# descarga el modelo cargado actual y carga el pedido.
_cargar_si_falta() {
    local model="$1"
    if _model_cargado "$model"; then
        return 0
    fi
    # LM Studio activo? Si NO responde, se arranca BAJO DEMANDA (13-oct-2026).
    # Antes: el router se plantaba (return 2) y el trabajo caia a cloud sin intentarlo.
    if ! curl -s -m 3 "http://localhost:1234/api/v0/models" >/dev/null 2>&1; then
        _asegurar_servidor || return 2
    fi
    # RULE-021: si el binario no esta, se DICE. No se asume VRAM ni se silencia.
    if ! command -v lms >/dev/null 2>&1; then
        echo "ERROR: binario 'lms' no encontrado en PATH=$PATH" >&2
        echo "       (el planificador no hereda el PATH del shell interactivo; RULE-021)" >&2
        return 2
    fi
    echo "Cargando modelo $model (bajo demanda)..." >&2
    local err_carga
    if err_carga=$(timeout 180 lms load "$model" 2>&1); then
        sleep 2
        if _model_cargado "$model"; then
            echo "Modelo $model cargado ✅" >&2
            return 0
        fi
    fi
    # Fallo de carga -> se imprime el error REAL de lms (sin asumir el motivo) y se intenta SWAP
    echo "  Carga directa fallo — salida real de 'lms':" >&2
    printf '    %s\n' "${err_carga:-<sin salida>}" >&2
    echo "  Intentando swap (descargar el modelo cargado y reintentar)..." >&2
    local actual
    actual=$(curl -s -m 5 "http://localhost:1234/api/v0/models" 2>/dev/null \
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
")
    if [ -n "$actual" ]; then
        echo "  Descargando $actual (swap)..." >&2
        timeout 60 lms unload "$actual" >/dev/null 2>&1 || true
        sleep 2
    fi
    # Reintentar carga tras liberar VRAM (capturando su error real, RULE-021)
    local err_carga2
    if err_carga2=$(timeout 180 lms load "$model" 2>&1); then
        sleep 2
        if _model_cargado "$model"; then
            echo "Modelo $model cargado tras swap ✅" >&2
            return 0
        fi
    fi
    echo "  Segunda carga fallo — salida real de 'lms':" >&2
    printf '    %s\n' "${err_carga2:-<sin salida>}" >&2
    echo "ERROR: no se pudo cargar $model — ver el error real de 'lms' arriba (no asumir VRAM)" >&2
    return 2
}

# ── Ejecutar prompt en el modelo local ──
_llm_local() {
    local prompt="$1"
    local model="$LM_MODEL"
    local sysmsg="${2:-Eres el asistente del lab. Responde SIEMPRE en español. NO mezcles otros idiomas ni caracteres no latinos. NO razones en voz alta, da la respuesta directa.}"
    # TOKEN BUDGETING (13-ago-2026, patrón del vídeo "7 Ways to Speed Up AI Agents"):
    # presupuesto distinto según la tarea (simple vs profunda). Configurable por env.
    local max_tokens="${MAX_TOKENS:-800}"

    # Si R1 no esta cargado, cargarlo bajo demanda (ya no falla ni usa fallback)
    if ! _cargar_si_falta "$model"; then
        # Fallback: intentar GLM (VLM, sirve para texto) si esta cargado o se puede cargar
        if _cargar_si_falta "$LM_MODEL_FALLBACK"; then
            model="$LM_MODEL_FALLBACK"
        else
            return 2
        fi
    fi

    # Payload JSON (sin jq: construir con python3)
    local payload
    payload=$(python3 - "$model" "$sysmsg" "$prompt" "$max_tokens" <<'PYEOF'
import json, sys
model, sysmsg, prompt, max_tokens = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
print(json.dumps({
    "model": model,
    "messages": [
        {"role": "system", "content": sysmsg},
        {"role": "user", "content": prompt}
    ],
    "max_tokens": max_tokens,
    "temperature": 0.3,
    "stream": False
}))
PYEOF
)

    local resp t0
    t0=$(date +%s.%N)
    resp=$(curl -s -m "$TIMEOUT_S" -X POST "$LM_API" \
        -H "Content-Type: application/json" \
        -d "$payload")

    # -- Espejo local: anotar los tokens de esta consulta (no altera la salida) --
    if [ -f "$LEDGER_LOCAL" ]; then
        local lat
        # LC_NUMERIC=C: awk debe dar 2.13 y no 2,13 (argparse rechaza la coma decimal)
        lat=$(LC_NUMERIC=C awk -v a="$t0" -v b="$(date +%s.%N)" 'BEGIN{printf "%.2f", b-a}')
        printf '%s' "$resp" | python3 "$LEDGER_LOCAL" --desde-stdin --motor lmstudio \
            --fuente "llm-router.sh:${ROUTER_MODO:-?}" --latencia "$lat" \
            >/dev/null 2>>"$LEDGER_LOG" || true
    fi

    # Extraer content (y reasoning si content vacio)
    python3 - "$resp" <<'PYEOF'
import json, sys
try:
    d = json.loads(sys.argv[1])
    msg = d["choices"][0]["message"]
    content = msg.get("content", "").strip()
    if content:
        print(content)
    else:
        reasoning = msg.get("reasoning_content", "").strip()
        print(reasoning[:2000] if reasoning else "(respuesta vacia)")
except Exception as e:
    print(f"ERROR parseando respuesta local: {e}", file=sys.stderr)
    print(sys.argv[1][:500], file=sys.stderr)
    sys.exit(1)
PYEOF
}

# ── Router principal ──
case "${1:-}" in
    batch)
        # Tarea batch: resumen, clasificacion, extraccion → LOCAL
        # Token budgeting: decisiones simples no merecen presupuesto de investigacion (patrón 7 Ways)
        # MAX_TOKENS externo se respeta si viene definido (ej: informe diario necesita 1200
        # porque gpt-oss/R1 razonan antes de responder — con presupuesto corto se queda en el pensamiento)
        # 600 desde 22-ago-2026: batería real mostró informes de hasta ~280 tokens de salida
        # (T1 content 1127 chars) + razonamiento encubierto de gpt-oss; 400 era justo y cortaba.
        ROUTER_MODO=batch MAX_TOKENS="${MAX_TOKENS:-600}" _llm_local "${2:?Uso: llm-router.sh batch <prompt>}"
        ;;
    batch-json)
        # Batch con salida JSON estricta — presupuesto corto (JSON real ~30 tokens, batería 22-ago)
        # Respetar MAX_TOKENS externo (antes fijo 300 sin override; JSON largo se cortaba sin remedio)
        ROUTER_MODO=batch-json MAX_TOKENS="${MAX_TOKENS:-300}" _llm_local "${2:?Uso: llm-router.sh batch-json <prompt>}" \
            "Eres el asistente del lab. Devuelve SOLO JSON valido, sin markdown, sin explicaciones."
        ;;
    vision)
        # Vision → GLM (VLM) — presupuesto moderado (razonamiento + descripción)
        ROUTER_MODO=vision LM_MODEL="glm-4.6v-flash" MAX_TOKENS=600 _llm_local "${2:?Uso: llm-router.sh vision <prompt>}"
        ;;
    auto)
        # PREESTIMACIÓN AUTOMÁTICA (06-sep-2026): el pipeline clasifica la tarea
        # contra modelos_por_tarea.yaml y devuelve el modelo ganador ANTES de cargar.
        # Si el modelo no está cargado, _llm_local lo carga bajo demanda (con swap).
        est=$(python3 /home/jokoalmi/joko-lab/tools/pipeline_seleccion_modelo.py --check "${2:?Uso: llm-router.sh auto <prompt>}" --json 2>/dev/null) || {
            echo "ERROR: pipeline_seleccion_modelo.py no respondió (¿PYTHONPATH/venv?)" >&2
            exit 2
        }
        # Parsear JSON: tipo, modelo, local (true/false), fuera_de_lmstudio, herramienta
        tipo=$(printf '%s' "$est" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tipo','?'))")
        modelo=$(printf '%s' "$est" | python3 -c "import json,sys; print(json.load(sys.stdin).get('modelo','?'))")
        local_flag=$(printf '%s' "$est" | python3 -c "import json,sys; print(json.load(sys.stdin).get('local',False))")
        fuera=$(printf '%s' "$est" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('herramienta') or '') if d.get('fuera_de_lmstudio') else print('')")
        echo "auto: tipo=$tipo → modelo=$modelo (local=$local_flag)" >&2
        if [ -n "$fuera" ]; then
            # Tarea declarada fuera de LM Studio (generacion_imagen, transcripcion...)
            echo "ERROR: tipo '$tipo' NO es tarea de LM Studio → herramienta: $fuera." >&2
            exit 4
        fi
        if [ "$local_flag" != "True" ]; then
            # Clasificado como cloud/interactivo: este router es solo local.
            echo "ERROR: tipo '$tipo' clasificado como CLOUD → usa el motor cloud configurado, no llm-router." >&2
            exit 3
        fi
        ROUTER_MODO=auto LM_MODEL="$modelo" _llm_local "${2}"
        ;;
    check)
        # Diagnostico: que motor tocaria cada tipo
        echo "=== ROUTER LOCAL/CLOUD (check) ==="
        echo "Modelo principal Hermes (config): deepseek / deepseek-v4-flash (cloud)"
        if _model_cargado "$LM_MODEL"; then
            echo "Motor local batch: $LM_MODEL (cargado) ✅"
        elif _model_cargado "$LM_MODEL_FALLBACK"; then
            echo "Motor local batch: $LM_MODEL_FALLBACK (cargado, gpt-oss no) ⚠️"
        else
            echo "Motor local batch: NINGUNO cargado → se cargara bajo demanda al usar (lms load)"
        fi
        echo ""
        echo "  batch / resumen / clasificacion → LOCAL (auto-carga si falta)"
        echo "  vision → GLM local (auto-carga si falta)"
        echo "  auto <prompt> → preestima modelo por tipo de tarea (tabla YAML) y ejecuta"
        echo "  interactivo / razonamiento complejo → CLOUD (deepseek)"
        ;;
    *)
        echo "Uso: llm-router.sh {batch|batch-json|vision|auto|check} [prompt]" >&2
        exit 1
        ;;
esac
