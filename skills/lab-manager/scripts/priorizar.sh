#!/usr/bin/env bash
# priorizar.sh — Propone orden de reconstrucción y prioridades del laboratorio
# Uso: bash skills/lab-manager/scripts/priorizar.sh [--desde-cero]
#   --desde-cero: simula que el laboratorio empieza vacío y propone orden de reconstrucción
# Solo lectura. No modifica ningún archivo.

set -euo pipefail

LAB_DIR="/home/jokoalmi/hermes-lab"
DESDE_CERO="${1:-}"

echo "===== PRIORIZACIÓN — JOKO LAB ====="
echo "Fecha: $(date '+%Y-%m-%d %H:%M')"
echo ""

if [ "$DESDE_CERO" = "--desde-cero" ]; then
    echo "Modo: ¿Si empezara desde cero, qué reconstruirías primero?"
    echo ""
    echo "--- ORDEN DE RECONSTRUCCIÓN ---"
    echo "1. Infraestructura base"
    echo "   • Docker + Docker Compose → servicios base"
    echo "   • n8n → motor de automatización (zona protegida)"
    echo "   • Ollama → IA local"
    echo ""
    echo "2. Automatización y conectividad"
    echo "   • ai-router → enrutamiento inteligente de modelos"
    echo "   • Backups automáticos → seguridad de datos"
    echo "   • Healthchecks → detección temprana de fallos"
    echo ""
    echo "3. Skills de Hermes"
    echo "   • docker-admin → gestión del stack"
    echo "   • n8n-admin → gestión de workflows"
    echo "   • lab-manager (Director Técnico) → monitoreo y deuda"
    echo "   • hermes-expert → diagnóstico y configuración"
    echo ""
    echo "4. Skills de dominio específico"
    echo "   • betterbird → gestión de correo"
    echo "   • perfumes → (pendiente de definir)"
    echo "   • evolution → (pendiente de definir)"
    echo ""
    echo "Razón del orden: dependencias técnicas."
    echo "Sin Docker no hay servicios. Sin servicios no hay skills que los gestionen."
    echo "Sin skills base no tiene sentido poblar skills de dominio."
    echo ""
    echo "--- QUÉ SE RECONSTRUIRÍA IGUAL ---"
    echo "  ✔ docker-admin — madura, completa, documentada"
    echo "  ✔ ai-router — funcional, árbol de decisión claro"
    echo "  ✔ n8n-admin — operativa, healthchecks activos"
    echo ""
    echo "--- QUÉ SE REPENSARÍA ---"
    echo "  ⚠ hermes-expert — tiene 3 scripts pero su propósito es amplio"
    echo "  ⚠ lab-manager — se convertiría en Director Técnico desde el inicio"
    echo ""
    echo "--- QUÉ NO SE RECONSTRUIRÍA IGUAL ---"
    echo "  ✗ betterbird, perfumes, evolution — se definiría primero su propósito exacto"
    echo "  ✗ docs/hermes-notes.md — contenido antiguo, no se migraría"
    echo "  ✗ docs/joko-lab-principles.md — se redactaría desde cero con los 5 principios actuales"
    echo ""
else
    echo "Modo: Prioridades actuales del laboratorio"
    echo ""

    # Leer skills vacías
    VACIAS=()
    for skill_dir in "$LAB_DIR/skills"/*/; do
        sk_file="$skill_dir/SKILL.md"
        if [ ! -f "$sk_file" ] || [ "$(wc -l < "$sk_file")" -lt 3 ]; then
            VACIAS+=("$(basename "$skill_dir")")
        fi
    done

    echo "--- PRIORIDAD ALTA (urgencia técnica) ---"
    echo ""
    echo "1. Skills vacías (${#VACIAS[@]} encontradas)"

    # Ordenar por valor práctico
    for s in "${VACIAS[@]}"; do
        case "$s" in
            betterbird)
                echo "   → betterbird — valor alto (gestión de correo, uso diario)"
                ;;
            evolution)
                echo "   → evolution — valor medio (pendiente de definir)"
                ;;
            perfumes)
                echo "   → perfumes — valor bajo (pendiente de definir)"
                ;;
            *)
                echo "   → $s — pendiente de evaluar"
                ;;
        esac
    done
    echo ""

    echo "2. Documentación incompleta"
    echo "   → docs/joko-lab-principles.md — vacío"
    echo "   → HERMES.md — 6/8 secciones vacías"
    echo ""

    echo "--- PRIORIDAD MEDIA (esta semana) ---"
    echo ""
    echo "3. Lab-manager a etapa 2"
    echo "   → Crear scripts de diagnóstico (diagnosticar.sh, deuda-tecnica.sh)"
    echo ""
    echo "4. Git"
    echo "   → Inicializar repositorio para trazabilidad"
    echo ""

    echo "--- PRIORIDAD BAJA (próximas semanas) ---"
    echo ""
    echo "5. Tests para skills existentes"
    echo "6. n8n-admin etapa 4"
    echo "7. ai-router etapa 4"
    echo "8. Revisar docs/hermes-notes.md"
    echo ""

    # Dependencias
    echo "--- DEPENDENCIAS A CONSIDERAR ---"
    echo "  Ninguna skill vacía depende de otra."
    echo "  ai-router y n8n-admin pueden evolucionar independientemente."
    echo "  lab-manager necesita skills pobladas para monitorizarlas."
    echo "  Git no afecta a ninguna skill pero da trazabilidad."
fi

echo ""
echo "===== ====="
