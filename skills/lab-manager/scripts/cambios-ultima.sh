#!/usr/bin/env bash
# cambios-ultima.sh — Compara el estado actual con la última auditoría
# Uso: bash skills/lab-manager/scripts/cambios-ultima.sh
# Solo lectura. No modifica ningún archivo.

set -euo pipefail

LAB_DIR="/home/jokoalmi/hermes-lab"
SNAPSHOT_FILE="$LAB_DIR/skills/lab-manager/data/ultima-auditoria.json"

echo "===== CAMBIOS DESDE LA ÚLTIMA AUDITORÍA ====="
echo "Fecha actual: $(date '+%Y-%m-%d %H:%M')"
echo ""

if [ ! -f "$SNAPSHOT_FILE" ]; then
    echo "No hay snapshot previo."
    echo "Ejecuta primero: bash skills/lab-manager/scripts/diagnosticar.sh"
    echo ""
    echo "====="
    exit 0
fi

echo "Snapshot previo encontrado."
PREV_DATE=$(grep -m1 '"fecha"' "$SNAPSHOT_FILE" 2>/dev/null | sed 's/.*"fecha": "\(.*\)",*/\1/')
echo "Fecha del snapshot: ${PREV_DATE:-desconocida}"
echo ""

# --- Estado actual ---
echo "--- ESTADO ACTUAL ---"
# Skills
SKILLS_DIR="$LAB_DIR/skills"
AHORA_POBLADAS=0
AHORA_VACIAS=0
for skill_dir in "$SKILLS_DIR"/*/; do
    sk_file="$skill_dir/SKILL.md"
    if [ -f "$sk_file" ] && [ "$(wc -l < "$sk_file")" -ge 3 ]; then
        AHORA_POBLADAS=$((AHORA_POBLADAS + 1))
    else
        AHORA_VACIAS=$((AHORA_VACIAS + 1))
    fi
done

# Documentación
DOCS_DIR="$LAB_DIR/docs"
AHORA_DOCS_OK=$(find "$DOCS_DIR" -maxdepth 1 -name "*.md" -size +1k 2>/dev/null | wc -l)
AHORA_DOCS_VACIOS=$(find "$DOCS_DIR" -maxdepth 1 -name "*.md" -size -1k 2>/dev/null | wc -l)
AHORA_DECISIONES=$(find "$DOCS_DIR/decisiones" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l)

# IA
AHORA_OLLAMA=$(curl -s --max-time 3 http://localhost:11434/api/tags >/dev/null 2>&1 && echo "true" || echo "false")
AHORA_LM=$(curl -s --max-time 3 http://localhost:1234/api/v0/models >/dev/null 2>&1 && echo "true" || echo "false")

# --- Extraer valores del snapshot previo ---
ANTES_POBLADAS=$(grep -m1 '"pobladas"' "$SNAPSHOT_FILE" 2>/dev/null | sed 's/.*"pobladas": \([0-9]*\).*/\1/')
ANTES_VACIAS=$(grep -m1 '"vacias"' "$SNAPSHOT_FILE" 2>/dev/null | sed 's/.*"vacias": \([0-9]*\).*/\1/')
ANTES_DOCS_OK=$(grep -m1 '"docs_ok"' "$SNAPSHOT_FILE" 2>/dev/null | sed 's/.*"docs_ok": \([0-9]*\).*/\1/')
ANTES_DOCS_VACIOS=$(grep -m1 '"docs_vacios"' "$SNAPSHOT_FILE" 2>/dev/null | sed 's/.*"docs_vacios": \([0-9]*\).*/\1/')
ANTES_DECISIONES=$(grep -m1 '"decisiones"' "$SNAPSHOT_FILE" | tail -1 | sed 's/.*"decisiones": \([0-9]*\).*/\1/')
ANTES_OLLAMA=$(grep -m1 '"ollama"' "$SNAPSHOT_FILE" 2>/dev/null | sed 's/.*"ollama": \(true\|false\).*/\1/')
ANTES_LM=$(grep -m1 '"lm_studio"' "$SNAPSHOT_FILE" 2>/dev/null | sed 's/.*"lm_studio": \(true\|false\).*/\1/')

echo "--- CAMBIOS DETECTADOS ---"

# Skills
if [ -n "$ANTES_POBLADAS" ]; then
    DIFF_POBLADAS=$((AHORA_POBLADAS - ANTES_POBLADAS))
    DIFF_VACIAS=$((AHORA_VACIAS - ANTES_VACIAS))
    if [ "$DIFF_POBLADAS" -gt 0 ]; then
        echo "  ⬆ Skills pobladas: +$DIFF_POBLADAS (de $ANTES_POBLADAS a $AHORA_POBLADAS)"
    elif [ "$DIFF_POBLADAS" -lt 0 ]; then
        echo "  ⬇ Skills pobladas: $DIFF_POBLADAS (de $ANTES_POBLADAS a $AHORA_POBLADAS)"
    else
        echo "  — Skills pobladas: sin cambios ($AHORA_POBLADAS)"
    fi
fi

# Documentación
if [ -n "$ANTES_DOCS_OK" ]; then
    DIFF_DOCS_OK=$((AHORA_DOCS_OK - ANTES_DOCS_OK))
    if [ "$DIFF_DOCS_OK" -gt 0 ]; then
        echo "  ⬆ Documentos completos: +$DIFF_DOCS_OK (de $ANTES_DOCS_OK a $AHORA_DOCS_OK)"
    elif [ "$DIFF_DOCS_OK" -lt 0 ]; then
        echo "  ⬇ Documentos completos: $DIFF_DOCS_OK (de $ANTES_DOCS_OK a $AHORA_DOCS_OK)"
    else
        echo "  — Documentos completos: sin cambios ($AHORA_DOCS_OK)"
    fi
fi

if [ -n "$ANTES_DECISIONES" ]; then
    DIFF_DEC=$((AHORA_DECISIONES - ANTES_DECISIONES))
    if [ "$DIFF_DEC" -gt 0 ]; then
        echo "  ⬆ Decisiones registradas: +$DIFF_DEC (de $ANTES_DECISIONES a $AHORA_DECISIONES)"
    elif [ "$DIFF_DEC" -lt 0 ]; then
        echo "  ⬇ Decisiones registradas: $DIFF_DEC (de $ANTES_DECISIONES a $AHORA_DECISIONES)"
    else
        echo "  — Decisiones: sin cambios ($AHORA_DECISIONES)"
    fi
fi

# IA
if [ -n "$ANTES_OLLAMA" ] && [ "$ANTES_OLLAMA" != "$AHORA_OLLAMA" ]; then
    echo "  ⚠ Ollama: cambió de estado ($ANTES_OLLAMA → $AHORA_OLLAMA)"
else
    echo "  — Ollama: sin cambios"
fi

if [ -n "$ANTES_LM" ] && [ "$ANTES_LM" != "$AHORA_LM" ]; then
    echo "  ⚠ LM Studio: cambió de estado ($ANTES_LM → $AHORA_LM)"
else
    echo "  — LM Studio: sin cambios"
fi

echo ""
echo "===== DIF COMPLETADO ====="
