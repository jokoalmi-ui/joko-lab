#!/usr/bin/env bash
# smoke-test.sh — Tests de humo del stack Joko Lab
# Verifica que cada servicio responde antes de confiar en él.
# Uso: ./smoke-test.sh [--quiet] [--service n8n|ollama|...]
set +e

PASS=0
FAIL=0
SERVICES=()

mostrar_ayuda() {
    cat <<EOF
Uso: $0 [OPCIONES]

Opciones:
  --quiet          Solo mostrar resultados, sin detalle por servicio
  --service NOMBRE Testear solo un servicio (n8n, ollama, stirling, pdf-cleaner, lm-studio, hermes)
  --help           Mostrar esta ayuda

Sin opciones, testea todos los servicios.
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --quiet) QUIET=1; shift ;;
        --service) SERVICES+=("$2"); shift 2 ;;
        --help) mostrar_ayuda ;;
        *) echo "Opción desconocida: $1"; exit 1 ;;
    esac
done

if [[ -z "${QUIET:-}" ]]; then
    ROJO='\033[0;31m'
    VERDE='\033[0;32m'
    AMARILLO='\033[1;33m'
    NC='\033[0m'
else
    ROJO=''
    VERDE=''
    AMARILLO=''
    NC=''
fi

test_service() {
    local name="$1"
    local cmd="$2"
    local label="${3:-$name}"
    
    if eval "$cmd" &>/dev/null; then
        PASS=$((PASS + 1))
        if [[ -z "${QUIET:-}" ]]; then
            echo -e "  ${VERDE}✓${NC} $label"
        fi
        return 0
    else
        FAIL=$((FAIL + 1))
        echo -e "  ${ROJO}✗${NC} $label"
        return 1
    fi
}

echo "═══════════════════════════════════"
echo "  Smoke tests — Joko Lab"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "═══════════════════════════════════"

# === n8n ===
if [[ ${#SERVICES[@]} -eq 0 ]] || [[ " ${SERVICES[*]} " =~ " n8n " ]]; then
    echo -e "\n${AMARILLO}■ n8n${NC}"
    test_service "n8n" \
        "curl -sf http://127.0.0.1:5678/healthz" \
        "HTTP 127.0.0.1:5678/healthz"
    test_service "n8n-webhook" \
        "curl -sf http://127.0.0.1:5678/webhook-test/health 2>/dev/null || curl -sf http://127.0.0.1:5678/webhook/health 2>/dev/null || test \$? -eq 7" \
        "Webhook (opcional)"
fi

# === Ollama ===
if [[ ${#SERVICES[@]} -eq 0 ]] || [[ " ${SERVICES[*]} " =~ " ollama " ]]; then
    echo -e "\n${AMARILLO}■ Ollama${NC}"
    test_service "ollama" \
        "curl -sf http://localhost:11434/api/tags | python3 -c 'import sys,json; d=json.load(sys.stdin); assert len(d.get(\"models\",[]))>0'" \
        "API /api/tags (modelos cargados)"
fi

# === Stirling-PDF ===
if [[ ${#SERVICES[@]} -eq 0 ]] || [[ " ${SERVICES[*]} " =~ " stirling " ]]; then
    echo -e "\n${AMARILLO}■ Stirling-PDF${NC}"
    test_service "stirling" \
        "curl -sf http://localhost:8081 | grep -qi 'stirling'" \
        "HTTP localhost:8081"
fi

# === pdf-cleaner ===
if [[ ${#SERVICES[@]} -eq 0 ]] || [[ " ${SERVICES[*]} " =~ " pdf-cleaner " ]]; then
    echo -e "\n${AMARILLO}■ pdf-cleaner${NC}"
    test_service "pdf-cleaner" \
        "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/health 2>/dev/null || curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/ 2>/dev/null | grep -qv '000'" \
        "HTTP localhost:8000 (respuesta detectada)"
fi

# === LM Studio ===
if [[ ${#SERVICES[@]} -eq 0 ]] || [[ " ${SERVICES[*]} " =~ " lm-studio " ]]; then
    echo -e "\n${AMARILLO}■ LM Studio${NC}"
    test_service "lm-studio" \
        "curl -sf http://localhost:1234/api/v0/models &>/dev/null" \
        "API localhost:1234 (modelos)"
fi

# === Hermes ===
if [[ ${#SERVICES[@]} -eq 0 ]] || [[ " ${SERVICES[*]} " =~ " hermes " ]]; then
    echo -e "\n${AMARILLO}■ Hermes Agent${NC}"
    test_service "hermes" \
        "command -v hermes &>/dev/null && hermes --version &>/dev/null" \
        "Comando hermes disponible"
fi

# === GPU ===
if [[ ${#SERVICES[@]} -eq 0 ]] || [[ " ${SERVICES[*]} " =~ " gpu " ]]; then
    echo -e "\n${AMARILLO}■ GPU${NC}"
    test_service "nvidia-smi" \
        "nvidia-smi &>/dev/null" \
        "nvidia-smi detectado"
fi

# === Resumen ===
echo
echo "═══════════════════════════════════"
TOTAL=$((PASS + FAIL))
echo -e "  ${VERDE}PASS:${NC} $PASS    ${ROJO}FAIL:${NC} $FAIL    Total: $TOTAL"
if [[ $FAIL -eq 0 ]]; then
    echo -e "  ${VERDE}Todo correcto.${NC}"
else
    echo -e "  ${ROJO}$FAIL servicio(s) con problemas.${NC}"
fi
echo "═══════════════════════════════════"

exit $FAIL
