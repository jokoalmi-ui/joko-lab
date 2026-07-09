#!/usr/bin/env bash
# deuda-tecnica.sh — Calcula la deuda técnica de Joko Lab
# Uso: bash skills/lab-manager/scripts/deuda-tecnica.sh
# Solo lectura. No modifica ningún archivo.
#
# La deuda se calcula usando la escala de madurez de skills (0-7, ver HERMES.md §5):
# - nivel 0-1: alta deuda (vacía o solo SKILL.md)
# - nivel 2-3: deuda media (documentada pero sin scripts)
# - nivel 4-5: deuda baja (instrumentada o auditada)
# - nivel 6-7: sin deuda significativa

set -euo pipefail

LAB_DIR="/home/jokoalmi/hermes-lab"

echo "===== DEUDA TÉCNICA — JOKO LAB ====="
echo "Fecha: $(date '+%Y-%m-%d %H:%M')"
echo ""

DEUDA_TOTAL=0
MAX_DEUDA=0
ITEMS=()

# --- 1. Deuda por nivel de madurez de skills ---
echo "--- 1. MADUREZ DE SKILLS (niveles 0-7) ---"
SKILL_DEUDA=0
SKILL_MAX=0
for skill_dir in "$LAB_DIR/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    sk_file="$skill_dir/SKILL.md"
    nivel=0

    # Nivel 1: existe SKILL.md con contenido
    if [ -f "$sk_file" ] && [ "$(wc -l < "$sk_file")" -ge 3 ]; then
        nivel=1
    fi

    # Nivel 2: tiene README.md
    if [ -f "$skill_dir/README.md" ] && [ "$(wc -l < "$skill_dir/README.md")" -ge 3 ]; then
        nivel=2
    fi

    # Nivel 3: tiene COMMANDS.md
    if [ -f "$skill_dir/COMMANDS.md" ] && [ "$(wc -l < "$skill_dir/COMMANDS.md")" -ge 5 ]; then
        nivel=3
    fi

    # Nivel 4: tiene scripts/
    if [ -d "$skill_dir/scripts" ] && [ "$(find "$skill_dir/scripts" -name '*.sh' 2>/dev/null | wc -l)" -ge 1 ]; then
        nivel=4
    fi

    # Nivel 5: tiene CHANGELOG.md y ha pasado auditoría (marcado en SKILL.md o CHANGELOG)
    if [ -f "$skill_dir/CHANGELOG.md" ] && [ "$(wc -l < "$skill_dir/CHANGELOG.md")" -ge 5 ]; then
        # Solo si también tiene scripts (nivel 4)
        if [ "$nivel" -ge 4 ]; then
            nivel=5
        fi
    fi

    # Nivel 6: tiene tests
    tests=$(find "$skill_dir" -maxdepth 2 \( -name '*test*' -o -name '*spec*' \) 2>/dev/null | head -1)
    if [ -n "$tests" ] && [ "$nivel" -ge 5 ]; then
        nivel=6
    fi

    # Calcular deuda: max nivel 7, deuda = (7 - nivel) * 1.5 redondeado
    deuda_skill=$(( (7 - nivel) * 3 / 2 ))
    [ "$deuda_skill" -lt 0 ] && deuda_skill=0
    echo "  $skill_name — nivel $nivel (deuda: +$deuda_skill)"
    SKILL_DEUDA=$((SKILL_DEUDA + deuda_skill))
    SKILL_MAX=$((SKILL_MAX + 10))  # 7 * ~1.5, redondeado a 10 por skill
done
echo "  Deuda por madurez: $SKILL_DEUDA / $SKILL_MAX"
DEUDA_TOTAL=$((DEUDA_TOTAL + SKILL_DEUDA))
MAX_DEUDA=$((MAX_DEUDA + SKILL_MAX))
echo ""

# --- 2. Documentación incompleta ---
echo "--- 2. DOCUMENTACIÓN ---"
DOCS_INCOMPLETOS=0
# docs vacíos o con < 5 líneas
for doc in "$LAB_DIR/docs"/*.md; do
    doc_name=$(basename "$doc")
    lines=$(wc -l < "$doc")
    if [ "$lines" -lt 5 ]; then
        echo "  ✗ $doc_name — solo $lines líneas"
        DOCS_INCOMPLETOS=$((DOCS_INCOMPLETOS + 1))
    fi
done
# HERMES.md secciones vacías
hermes_total=$(grep -c "^## " "$LAB_DIR/HERMES.md" 2>/dev/null || true)
hermes_total=${hermes_total:-0}
# Contar secciones que contengan "(pendiente)"
hermes_vacias=$(grep -c "pendiente" "$LAB_DIR/HERMES.md" 2>/dev/null || true)
hermes_vacias=${hermes_vacias:-0}
if [ "$hermes_vacias" -gt 0 ]; then
    echo "  ✗ HERMES.md — $hermes_vacias/$hermes_total secciones vacías"
    DOCS_INCOMPLETOS=$((DOCS_INCOMPLETOS + hermes_vacias))
fi
echo "  Documentos incompletos: $DOCS_INCOMPLETOS (penalización: +$((DOCS_INCOMPLETOS * 2)))"
DEUDA_TOTAL=$((DEUDA_TOTAL + DOCS_INCOMPLETOS * 2))
MAX_DEUDA=$((MAX_DEUDA + 14))
echo ""

# --- 3. Skills en nivel 0-1 (vacías) ---
echo "--- 3. SKILLS SIN DOCUMENTACIÓN BÁSICA ---"
SIN_BASICA=0
for skill_dir in "$LAB_DIR/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    sk_file="$skill_dir/SKILL.md"
    if [ ! -f "$sk_file" ] || [ "$(wc -l < "$sk_file")" -lt 3 ]; then
        echo "  ✗ $skill_name — sin SKILL.md"
        SIN_BASICA=$((SIN_BASICA + 1))
    fi
done
echo "  Skills sin SKILL.md: $SIN_BASICA (penalización: +$((SIN_BASICA * 2)))"
DEUDA_TOTAL=$((DEUDA_TOTAL + SIN_BASICA * 2))
MAX_DEUDA=$((MAX_DEUDA + 6))
echo ""

# --- 4. Git ---
echo "--- 4. INFRAESTRUCTURA ---"
GIT_DEUDA=0
if ! command -v git &>/dev/null; then
    echo "  ✗ Git no instalado (+4)"
    GIT_DEUDA=4
elif [ ! -d "$LAB_DIR/.git" ]; then
    echo "  ✗ Repositorio Git no inicializado (+2)"
    GIT_DEUDA=2
else
    echo "  ✔ Git instalado y repositorio inicializado"
fi
DEUDA_TOTAL=$((DEUDA_TOTAL + GIT_DEUDA))
MAX_DEUDA=$((MAX_DEUDA + 4))
echo ""

# --- 5. Incoherencias entre docs ---
echo "--- 5. INCOHERENCIAS ENTRE DOCUMENTOS ---"
INCOHERENCIAS=0

# docs/estado-real.md — contar decisiones en disco vs mencionadas
DECISIONES_DISCO=$(find "$LAB_DIR/docs/decisiones" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l)
# docs/arquitectura.md
if grep -q "7 archivos" "$LAB_DIR/docs/arquitectura.md" 2>/dev/null; then
    echo "  ✗ docs/arquitectura.md: dice '7 archivos' en decisiones ($DECISIONES_DISCO reales)"
    INCOHERENCIAS=$((INCOHERENCIAS + 1))
fi

echo "  Incoherencias detectadas: $INCOHERENCIAS (penalización: +$((INCOHERENCIAS * 3)))"
DEUDA_TOTAL=$((DEUDA_TOTAL + INCOHERENCIAS * 3))
MAX_DEUDA=$((MAX_DEUDA + 9))
echo ""

# --- Resumen ---
echo "==========================================="
echo "RESUMEN DE DEUDA TÉCNICA"
echo "==========================================="
if [ "$MAX_DEUDA" -gt 0 ]; then
    PORCENTAJE=$((100 - DEUDA_TOTAL * 100 / MAX_DEUDA))
else
    PORCENTAJE=100
fi

echo "  Deuda acumulada: $DEUDA_TOTAL / $MAX_DEUDA puntos"
echo "  Salud del laboratorio: $PORCENTAJE%"

if [ "$PORCENTAJE" -ge 80 ]; then
    echo "  Estado: ✔ BAJA — el laboratorio está en buena forma"
elif [ "$PORCENTAJE" -ge 50 ]; then
    echo "  Estado: ⚠ MEDIA — hay áreas que requieren atención"
else
    echo "  Estado: ✗ ALTA — se recomienda priorizar reducción de deuda"
fi
echo ""

# Prioridades
echo "ACCIONES RECOMENDADAS:"
if [ "$SIN_BASICA" -gt 0 ]; then echo "  - Poblar $SIN_BASICA skills vacías (nivel 0→1, prioridad alta)"; fi
if [ "$DOCS_INCOMPLETOS" -gt 0 ]; then echo "  - Completar $DOCS_INCOMPLETOS documentos"; fi
SKILLS_NIVEL_BAJO=$(for skill_dir in "$LAB_DIR/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    sk_file="$skill_dir/SKILL.md"
    [ -f "$sk_file" ] && [ "$(wc -l < "$sk_file")" -ge 3 ] || continue
    # Comprobar si tiene nivel < 4 (sin scripts)
    if [ ! -d "$skill_dir/scripts" ] || [ "$(find "$skill_dir/scripts" -name '*.sh' 2>/dev/null | wc -l)" -eq 0 ]; then
        echo "  - $skill_name: necesita scripts para subir a nivel 4"
    fi
done)
if [ -n "$SKILLS_NIVEL_BAJO" ]; then echo "$SKILLS_NIVEL_BAJO"; fi
if [ "$GIT_DEUDA" -gt 2 ]; then echo "  - Instalar Git"; fi
if [ "$GIT_DEUDA" -gt 0 ] && [ "$GIT_DEUDA" -le 2 ]; then echo "  - Inicializar repositorio Git"; fi
if [ "$INCOHERENCIAS" -gt 0 ]; then echo "  - Corregir $INCOHERENCIAS incoherencias entre documentos"; fi
echo ""

echo "===== ====="
