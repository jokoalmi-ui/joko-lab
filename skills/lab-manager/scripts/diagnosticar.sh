#!/usr/bin/env bash
# diagnosticar.sh — Snapshot de estado del laboratorio
# Uso: bash skills/lab-manager/scripts/diagnosticar.sh
# Salida: stdout + guarda snapshot en skills/lab-manager/data/ultima-auditoria.json
#
# Solo lectura. No modifica ningún archivo fuera de data/.

set -uo pipefail

LAB_DIR="/home/jokoalmi/hermes-lab"
SNAPSHOT_FILE="$LAB_DIR/skills/lab-manager/data/ultima-auditoria.json"

echo "===== DIAGNÓSTICO DE JOKO LAB ====="
echo "Fecha: $(date '+%Y-%m-%d %H:%M')"
echo ""

# --- Skills ---
echo "--- SKILLS ---"
SKILLS_DIR="$LAB_DIR/skills"
TOTAL=0
POBLADAS=0
VACIAS=0
for skill_dir in "$SKILLS_DIR"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    TOTAL=$((TOTAL + 1))
    sk_file="$skill_dir/SKILL.md"
    if [ -f "$sk_file" ] && [ "$(wc -l < "$sk_file")" -ge 3 ]; then
        nombre=$(grep -m1 "^## " "$sk_file" 2>/dev/null | sed 's/^## *//' || echo "$skill_name")
        etapa=$(grep -im1 "etapa" "$sk_file" 2>/dev/null | sed 's/.*etapa *\([0-9]\).*/\1/' || grep -im1 "stage" "$sk_file" 2>/dev/null | sed 's/.*stage *\([0-9]\).*/\1/' || echo "?")
        echo "  $skill_name — $nombre (etapa $etapa)"
        POBLADAS=$((POBLADAS + 1))
    else
        echo "  $skill_name — VACIA"
        VACIAS=$((VACIAS + 1))
    fi
done
echo "  Total: $TOTAL | Pobladas: $POBLADAS | Vacias: $VACIAS"
echo ""

# --- Scripts por skill ---
echo "--- SCRIPTS ---"
SCRIPT_COUNT=0
for skill_dir in "$SKILLS_DIR"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    scripts=()
    # scripts/ subdirectorio
    if [ -d "$skill_dir/scripts" ]; then
        while IFS= read -r -d '' script; do
            scripts+=("$(basename "$script")")
        done < <(find "$skill_dir/scripts" -maxdepth 1 -type f -name "*.sh" -print0 2>/dev/null)
    fi
    # scripts en raiz de skill
    while IFS= read -r -d '' script; do
        base=$(basename "$script")
        if [[ ! " ${scripts[*]} " =~ " $base " ]]; then
            scripts+=("$base")
        fi
    done < <(find "$skill_dir" -maxdepth 1 -type f -name "*.sh" -print0 2>/dev/null)

    if [ ${#scripts[@]} -gt 0 ]; then
        echo "  $skill_name: ${scripts[*]}"
        SCRIPT_COUNT=$((SCRIPT_COUNT + ${#scripts[@]}))
    fi
done
echo "  Total scripts: $SCRIPT_COUNT"
echo ""

# --- Servicios Docker ---
echo "--- SERVICIOS DOCKER ---"
COMPOSE_FILE="$LAB_DIR/../automation-stack/docker-compose.yml"
if [ -f "$COMPOSE_FILE" ]; then
    DOCKER_OUTPUT=$(docker compose -f "$COMPOSE_FILE" ps 2>/dev/null) || true
    if echo "$DOCKER_OUTPUT" | grep -q "Up"; then
        echo "$DOCKER_OUTPUT" | while IFS= read -r line; do
            if echo "$line" | grep -q "Up"; then
                srv=$(echo "$line" | awk '{print $1}')
                echo "  $srv — UP"
            fi
        done
    else
        echo "  (no se pudo obtener estado Docker o compose no accesible)"
    fi
else
    echo "  (compose no encontrado en $COMPOSE_FILE)"
fi
echo ""

# --- IA disponible ---
echo "--- IA DISPONIBLE ---"

# Ollama
OLLAMA_OK=false
if curl -s --max-time 3 http://localhost:11434/api/tags >/dev/null 2>&1; then
    OLLAMA_OK=true
    OLLAMA_MODELS=$(curl -s --max-time 3 http://localhost:11434/api/tags 2>/dev/null | jq -r '.models[]?.name' 2>/dev/null | tr '\n' ', ' | sed 's/, $//')
    echo "  Ollama — modelos: ${OLLAMA_MODELS:-sin modelos cargados}"
else
    echo "  Ollama — no responde"
fi

# LM Studio
LM_OK=false
if curl -s --max-time 3 http://localhost:1234/api/v0/models >/dev/null 2>&1; then
    LM_OK=true
    LM_MODELS=$(curl -s --max-time 3 http://localhost:1234/api/v0/models 2>/dev/null | jq -r '.data[]?.id' 2>/dev/null | tr '\n' ', ' | sed 's/, $//')
    echo "  LM Studio — modelos: ${LM_MODELS:-sin respuesta}"
else
    echo "  LM Studio — API no responde"
fi

# DeepSeek
echo "  DeepSeek — activo (proveedor principal de Hermes)"
echo ""

# --- Documentación ---
echo "--- DOCUMENTACION ---"
DOCS_DIR="$LAB_DIR/docs"
for doc in "$DOCS_DIR"/*.md; do
    [ -f "$doc" ] || continue
    doc_name=$(basename "$doc")
    lines=$(wc -l < "$doc")
    if [ "$lines" -lt 3 ]; then
        echo "  $doc_name — VACIO ($lines lineas)"
    else
        fecha=$(grep -m1 -i "ultima actualizacion\|fecha:\|fecha de la ultima" "$doc" 2>/dev/null | sed 's/.*: *//')
        echo "  $doc_name — $lines lineas${fecha:+ (ultima: $fecha)}"
    fi
done
echo ""

# --- Decisiones ---
echo "--- DECISIONES DE ARQUITECTURA ---"
DEC_COUNT=$(find "$DOCS_DIR/decisiones" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l)
ACTIVAS=0
for dec_file in "$DOCS_DIR/decisiones"/*.md; do
    [ -f "$dec_file" ] || continue
    if grep -qi "Activa\|Pendiente" "$dec_file" 2>/dev/null; then
        ACTIVAS=$((ACTIVAS + 1))
    fi
done
echo "  Total: $DEC_COUNT | Activas/pendientes: $ACTIVAS"
echo ""

# --- Auditoria previa ---
echo "--- AUDITORIA PREVIA ---"
if [ -f "$SNAPSHOT_FILE" ]; then
    PREV_DATE=$(grep -m1 '"fecha"' "$SNAPSHOT_FILE" 2>/dev/null | sed 's/.*"fecha": "\(.*\)",*/\1/')
    echo "  Snapshot disponible — $PREV_DATE"
else
    echo "  — No hay snapshot previo (primera ejecucion)"
fi

echo ""
echo "===== DIAGNOSTICO COMPLETADO ====="
echo ""

# --- Guardar snapshot ---
echo "Guardando snapshot en $SNAPSHOT_FILE..."

cat > "$SNAPSHOT_FILE" << SNAPEOF
{
  "fecha": "$(date '+%Y-%m-%d %H:%M')",
  "skills": {"total": $TOTAL, "pobladas": $POBLADAS, "vacias": $VACIAS},
  "scripts": $SCRIPT_COUNT,
  "documentacion": {
    "docs_ok": $(find "$DOCS_DIR" -maxdepth 1 -name "*.md" -size +1k 2>/dev/null | wc -l),
    "docs_vacios": $(find "$DOCS_DIR" -maxdepth 1 -name "*.md" -size -1k 2>/dev/null | wc -l),
    "decisiones": $DEC_COUNT,
    "decisiones_activas": $ACTIVAS
  },
  "ia": {
    "ollama": $OLLAMA_OK,
    "lm_studio": $LM_OK
  }
}
SNAPEOF

echo "Snapshot guardado."
