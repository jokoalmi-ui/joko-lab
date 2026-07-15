#!/bin/bash
# apply-decision.sh
# Aplica la decisión del Runtime a Hermes Agent.
# Consume Runtime.resolve() via runtime/api.py.
#
# Ya no llama al DE directamente. El DE es puro (solo decide).
# El Runtime (runtime/api.py) gestiona logs y archivos de estado.
#
# Responsabilidades de este script:
# 1. Llamar a Runtime.resolve() (vía runtime/api.py --json)
# 2. Aplicar el resultado mediante hermes config set
# 3. Informar del resultado

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="/mnt/ssd_ia_datos/lab-state/logs/apply-decision.log"
RUNTIME_API="$PROJECT_ROOT/runtime/api.py"
SECRETS_DIR="/mnt/ssd_ia_datos/lab-state/secrets"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $*" >> "$LOG_FILE"
}

# Obtener decisión del Runtime
DECISION=$(python3 "$RUNTIME_API" --json 2>/dev/null)

if [ -z "$DECISION" ]; then
    log "ERROR: No se pudo obtener decisión del Runtime"
    exit 1
fi

PROVIDER=$(echo "$DECISION" | python3 -c "import json,sys; print(json.load(sys.stdin)['provider'])")
MODEL=$(echo "$DECISION" | python3 -c "import json,sys; print(json.load(sys.stdin)['model'])")
REASON=$(echo "$DECISION" | python3 -c "import json,sys; print(json.load(sys.stdin)['reason'])")

log "Decisión: $PROVIDER / $MODEL — $REASON"

# ─── Validación pre-aplicación contra API real ────────────────────────
# Patrón: state-manager.py read_secret() + check_cloud() con argument arrays.
# Los proveedores cloud (deepseek, gemini) REQUIEREN key siempre.
# La ausencia del archivo .key en SECRETS_DIR es bloqueante.
log "VALIDACIÓN: $PROVIDER/$MODEL — verificando disponibilidad real..."

_validar_modelo_deepseek() {
    local model="$1"
    local key="$2"
    local timeout=10
    local url="https://api.deepseek.com/models"

    local tmpfile
    tmpfile=$(mktemp)

    local curl_args=(-s --max-time "$timeout")
    [ -n "$key" ] && curl_args+=(-H "Authorization: Bearer $key")

    local http_code
    http_code=$(curl "${curl_args[@]}" -w "%{http_code}" "$url" -o "$tmpfile" 2>/dev/null)

    if [ "$http_code" = "000" ]; then
        log "   deepseek: HTTP 000 (conexión rechazada o timeout)"
        rm -f "$tmpfile"
        return 1
    fi

    if [ "$http_code" = "401" ]; then
        log "   deepseek: HTTP 401 (key rechazada) — key de ${#key} chars"
        rm -f "$tmpfile"
        return 1
    fi

    if [ "$http_code" != "200" ]; then
        log "   deepseek: HTTP $http_code (inesperado) — se permite el paso"
        rm -f "$tmpfile"
        return 0
    fi

    local body
    body=$(cat "$tmpfile" 2>/dev/null)
    rm -f "$tmpfile"

    # Validar que el modelo concreto existe en la lista
    if echo "$body" | python3 -c "
import json, sys
data = json.load(sys.stdin)
models = [m['id'] for m in data.get('data', [])]
sys.exit(0 if '$model' in models else 1)
" 2>/dev/null; then
        log "   deepseek: modelo '$model' confirmado en lista de modelos"
        return 0
    else
        log "   deepseek: modelo '$model' NO encontrado en lista de modelos"
        return 1
    fi
}

_validar_modelo_gemini() {
    local model="$1"
    local key="$2"
    local timeout=10
    local url="https://generativelanguage.googleapis.com/v1beta/models/$model"
    [ -n "$key" ] && url="$url?key=$key"

    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$timeout" "$url" 2>/dev/null)

    if [ "$http_code" = "000" ]; then
        log "   gemini: HTTP 000 (conexión rechazada o timeout)"
        return 1
    fi

    if [ "$http_code" = "401" ] || [ "$http_code" = "403" ]; then
        log "   gemini: HTTP $http_code (key rechazada) — key de ${#key} chars"
        return 1
    fi

    if [ "$http_code" = "404" ]; then
        log "   gemini: modelo '$model' no existe (HTTP 404)"
        return 1
    fi

    if [ "$http_code" = "200" ]; then
        log "   gemini: modelo '$model' confirmado (HTTP 200)"
        return 0
    fi

    log "   gemini: HTTP $http_code (inesperado) — se permite el paso"
    return 0
}

_validar_local() {
    local url="$1"
    local name="$2"
    local timeout=5

    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$timeout" "$url" 2>/dev/null)

    if [ "$http_code" = "000" ]; then
        log "   $name: HTTP 000 (proceso no responde)"
        return 1
    fi

    log "   $name: responde (HTTP $http_code)"
    return 0
}

validacion_ok=true

case "$PROVIDER" in
    deepseek)
        # deepseek SIEMPRE requiere key
        if [ ! -f "$SECRETS_DIR/deepseek.key" ]; then
            log "❌ VALIDACIÓN FALLÓ: deepseek requiere key pero no existe $SECRETS_DIR/deepseek.key"
            log "   Ejecutar: echo 'sk-tu-key-aqui' > $SECRETS_DIR/deepseek.key"
            validacion_ok=false
        else
            ds_key=$(cat "$SECRETS_DIR/deepseek.key" | tr -d '[:space:]')
            if [ -z "$ds_key" ]; then
                log "❌ VALIDACIÓN FALLÓ: $SECRETS_DIR/deepseek.key está vacío"
                validacion_ok=false
            else
                _validar_modelo_deepseek "$MODEL" "$ds_key" || validacion_ok=false
            fi
        fi
        ;;
    gemini)
        # gemini SIEMPRE requiere key
        if [ ! -f "$SECRETS_DIR/gemini.key" ]; then
            log "❌ VALIDACIÓN FALLÓ: gemini requiere key pero no existe $SECRETS_DIR/gemini.key"
            log "   Ejecutar: echo 'AIza-tu-key-aqui' > $SECRETS_DIR/gemini.key"
            validacion_ok=false
        else
            gm_key=$(cat "$SECRETS_DIR/gemini.key" | tr -d '[:space:]')
            if [ -z "$gm_key" ]; then
                log "❌ VALIDACIÓN FALLÓ: $SECRETS_DIR/gemini.key está vacío"
                validacion_ok=false
            else
                _validar_modelo_gemini "$MODEL" "$gm_key" || validacion_ok=false
            fi
        fi
        ;;
    ollama)
        _validar_local "http://localhost:11434/api/tags" "ollama" || validacion_ok=false
        ;;
    lmstudio)
        _validar_local "http://localhost:1234/api/v0/models" "lmstudio" || validacion_ok=false
        ;;
    none)
        log "   VALIDACIÓN: proveedor 'none' — salteando validación"
        ;;
    *)
        log "   VALIDACIÓN: proveedor '$PROVIDER' desconocido — se permite el paso"
        ;;
esac

if [ "$validacion_ok" != true ]; then
    log "❌ VALIDACIÓN FALLÓ: $PROVIDER/$MODEL no disponible o no válido"
    log "   config.yaml NO modificado — se mantiene proveedor anterior"
    exit 1
fi

log "✅ VALIDACIÓN OK: $PROVIDER/$MODEL"

# Estado actual antes del cambio
OLD_PROVIDER=$(hermes config show 2>/dev/null | grep "provider:" | head -1 | awk '{print $2}')
OLD_MODEL=$(hermes config show 2>/dev/null | grep "default:" | head -1 | awk '{print $2}')

if [ "$OLD_PROVIDER" = "$PROVIDER" ] && [ "$OLD_MODEL" = "$MODEL" ]; then
    log "Sin cambios: ya está en $PROVIDER/$MODEL"
    exit 0
fi

# Aplicar nuevo proveedor, modelo y base_url
log "Cambiando: $OLD_PROVIDER/$OLD_MODEL → $PROVIDER/$MODEL"

# Mapa de base_url por proveedor (evita base_url cruzado)
case "$PROVIDER" in
    deepseek)  BASE_URL="https://api.deepseek.com/v1" ;;
    gemini)    BASE_URL="https://generativelanguage.googleapis.com/v1beta" ;;
    ollama)    BASE_URL="http://localhost:11434/v1" ;;
    lmstudio)  BASE_URL="http://localhost:1234/v1" ;;
    *)         BASE_URL="" ;;
esac

hermes config set model.provider "$PROVIDER" 2>/dev/null
hermes config set model.default "$MODEL" 2>/dev/null
[ -n "$BASE_URL" ] && hermes config set model.base_url "$BASE_URL" 2>/dev/null

# Verificar
NEW_PROVIDER=$(grep -A4 "^model:" ~/.hermes/config.yaml 2>/dev/null | grep "provider:" | awk '{print $2}')
NEW_MODEL=$(grep -A4 "^model:" ~/.hermes/config.yaml 2>/dev/null | grep "default:" | awk '{print $2}')
NEW_BASE=$(grep -A4 "^model:" ~/.hermes/config.yaml 2>/dev/null | grep "base_url:" | awk '{print $2}')

if [ "$NEW_PROVIDER" = "$PROVIDER" ] && [ "$NEW_MODEL" = "$MODEL" ]; then
    if [ -z "$BASE_URL" ] || [ "$NEW_BASE" = "$BASE_URL" ]; then
        log "✅ Cambio aplicado correctamente: $PROVIDER/$MODEL (base_url: $BASE_URL)"
    else
        log "⚠️  Proveedor/modelo OK, pero base_url no coincide: esperado $BASE_URL, obtenido $NEW_BASE"
    fi
else
    log "❌ Fallo al aplicar: esperado $PROVIDER/$MODEL, obtenido $NEW_PROVIDER/$NEW_MODEL"
fi
