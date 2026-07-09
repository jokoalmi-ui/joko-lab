#!/usr/bin/env bash
# governor-check.sh — Comprobaciones de integridad del conocimiento de Joko Lab
# Versión: 0.1.0
# Uso: bash governor-check.sh [--opcion|--all]

set -euo pipefail

HERMES_LAB="$HOME/hermes-lab"
OUTDIR="/tmp/knowledge-governor"
mkdir -p "$OUTDIR"

show_help() {
    cat <<EOF
knowledge-governor — Comprobaciones de integridad del conocimiento

Uso: bash governor-check.sh [OPCIÓN]

Opciones:
  --all                 Ejecutar todas las comprobaciones
  --duplicados          Buscar archivos duplicados en docs/ y certification/
  --rotos               Buscar enlaces rotos a archivos inexistentes
  --decisiones-pendientes  Decisiones con Estado no vigente y >30 días
  --skills-huerfanas    Skills no referenciadas desde otros documentos
  --changelogs          Archivos modificados sin changelog actualizado
  --certificaciones     Casos C-XXX con referencias a docs inexistentes
  --help                Mostrar esta ayuda

Salida: Terminal + informe en $OUTDIR/
EOF
}

# --- COMPROBACIONES ---------------------------------------------------------

check_duplicados() {
    echo "--- [duplicados] Buscando archivos con contenido idéntico..."
    local total=0
    local informe="$OUTDIR/duplicados.txt"
    : > "$informe"

    while IFS= read -r -d '' f1; do
        while IFS= read -r -d '' f2; do
            if [[ "$f1" < "$f2" ]] && cmp -s "$f1" "$f2"; then
                echo "DUPLICADO: $f1 <-> $f2" | tee -a "$informe"
                total=$((total + 1))
            fi
        done < <(find "$HERMES_LAB/docs" "$HERMES_LAB/certification" -type f -print0)
    done < <(find "$HERMES_LAB/docs" "$HERMES_LAB/certification" -type f -print0)

    if [[ "$total" -eq 0 ]]; then
        echo "  OK: 0 duplicados detectados."
    else
        echo "  TOTAL: $total par(es) duplicado(s). Severidad: MEDIA"
    fi
}

check_rotos() {
    echo "--- [rotos] Buscando referencias a archivos inexistentes..."
    local informe="$OUTDIR/rotos.txt"
    : > "$informe"
    local total=0

    while IFS= read -r -d '' archivo; do
        while IFS=: read -r num linea; do
            # Extraer rutas relativas y limpiar caracteres markdown
            while read -r posible; do
                # Saltar si es solo un directorio (termina en /)
                [[ "$posible" == */ ]] && continue
                ruta="$HERMES_LAB/$posible"
                if [[ ! -f "$ruta" ]] && [[ ! -d "$ruta" ]]; then
                    echo "ROTO: $archivo línea $num → $posible" >> "$informe"
                    echo "  ROTO: $archivo línea $num → $posible"
                    total=$((total + 1))
                fi
            done < <(echo "$linea" | grep -oP '(docs/|certification/|skills/|HERMES\.md)\w[\w./-]*' || true)
        done < <(grep -n -oP '(docs/|certification/|skills/|HERMES\.md)\w[\w./-]*' "$archivo" || true)
    done < <(find "$HERMES_LAB/docs" "$HERMES_LAB/certification" "$HERMES_LAB/skills" "$HERMES_LAB" -maxdepth 1 -name "HERMES.md" -type f -print0)

    if [[ "$total" -eq 0 ]]; then
        echo "  OK: 0 enlaces rotos."
    else
        echo "  TOTAL: $total enlace(s) roto(s). Severidad: ALTA"
    fi
}

check_decisiones_pendientes() {
    echo "--- [decisiones-pendientes] Buscando decisiones no vigentes..."
    local informe="$OUTDIR/decisiones-pendientes.txt"
    : > "$informe"
    local total=0
    local hoy
    hoy=$(date +%s)

    for d in "$HERMES_LAB/docs/decisiones/"*.md; do
        [[ -f "$d" ]] || continue
        filename=$(basename "$d")
        # Extraer fecha del nombre del archivo AAAA-MM-DD
        fecha_str="${filename:0:10}"
        if [[ "$fecha_str" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
            f_epoch=$(date -d "$fecha_str" +%s 2>/dev/null || echo "")
            if [[ -n "$f_epoch" ]]; then
                dias=$(( (hoy - f_epoch) / 86400 ))
                # Buscar estado distinto de "Vigente"
                estado=$(grep -i 'Estado:' "$d" | head -1 | grep -oP '(Vigente|Pendiente|Descartada|Reemplazada)' || echo "Vigente")
                if [[ "$estado" != "Vigente" ]] && [[ "$dias" -gt 30 ]]; then
                    echo "PENDIENTE: $filename — Estado: $estado, $dias días" | tee -a "$informe"
                    total=$((total + 1))
                fi
            fi
        fi
    done

    if [[ "$total" -eq 0 ]]; then
        echo "  OK: 0 decisiones pendientes olvidadas."
    else
        echo "  TOTAL: $total decisión(es) pendiente(s). Severidad: ALTA"
    fi
}

check_skills_huerfanas() {
    echo "--- [skills-huérfanas] Buscando skills no referenciadas..."
    local informe="$OUTDIR/skills-huerfanas.txt"
    : > "$informe"
    local total=0

    for skill_dir in "$HERMES_LAB/skills/"*/; do
        skill_name=$(basename "$skill_dir")
        [[ "$skill_name" == "knowledge-governor" ]] && continue  # no se referencia a sí misma
        # Buscar referencias en docs/, certification/, HERMES.md, otras skills
        if ! grep -rq "$skill_name" "$HERMES_LAB/docs" "$HERMES_LAB/certification" "$HERMES_LAB/HERMES.md" "$HERMES_LAB/skills" 2>/dev/null; then
            echo "HUÉRFANA: $skill_name" | tee -a "$informe"
            total=$((total + 1))
        fi
    done

    if [[ "$total" -eq 0 ]]; then
        echo "  OK: 0 skills huérfanas."
    else
        echo "  TOTAL: $total skill(s) huérfana(s). Severidad: BAJA"
        echo "  (puede ser normal si están en creación)"
    fi
}

check_changelogs() {
    echo "--- [changelogs] Buscando archivos modificados sin changelog..."
    local informe="$OUTDIR/changelogs-pendientes.txt"
    : > "$informe"
    local total=0
    local hace_7_dias
    hace_7_dias=$(date -d '7 days ago' +%s)

    # Directorios que por convención no tienen CHANGELOG propio
    local exclude_dirs=(
        "$HERMES_LAB/docs"
        "$HERMES_LAB/certification"
        "$HERMES_LAB/scripts"
        "$HERMES_LAB/.git"
    )
    local find_exclude=""
    for d in "${exclude_dirs[@]}"; do
        find_exclude+=" -path $d -prune -o"
    done

    while IFS= read -r -d '' archivo; do
        # Saltar CHANGELOGs ellos mismos
        [[ "$archivo" == */CHANGELOG.md ]] && continue
        # Saltar directorios no documentales
        [[ "$archivo" == */scripts/* ]] && continue
        [[ "$archivo" == */logs/* ]] && continue
        [[ "$archivo" == */data/* ]] && continue
        [[ "$archivo" == */.git/* ]] && continue

        mtime=$(stat -c %Y "$archivo" 2>/dev/null || echo "")
        [[ -z "$mtime" ]] && continue
        if [[ "$mtime" -gt "$hace_7_dias" ]]; then
            dir=$(dirname "$archivo")
            changelog="$dir/CHANGELOG.md"
            if [[ ! -f "$changelog" ]]; then
                echo "SIN CHANGELOG: $archivo" | tee -a "$informe"
                total=$((total + 1))
            else
                today=$(date +%Y-%m-%d)
                if ! grep -q "$today" "$changelog"; then
                    echo "CHANGELOG NO ACTUALIZADO: $archivo → $changelog" | tee -a "$informe"
                    total=$((total + 1))
                fi
            fi
        fi
    done < <(eval find "$HERMES_LAB" "$find_exclude" -type f -print0)

    if [[ "$total" -eq 0 ]]; then
        echo "  OK: 0 archivos modificados sin changelog."
    else
        echo "  TOTAL: $total archivo(s) sin changelog actualizado. Severidad: MEDIA"
    fi
}

check_certificaciones() {
    echo "--- [certificaciones] Verificando referencias en casos C-XXX..."
    local informe="$OUTDIR/certificaciones-obsoletas.txt"
    : > "$informe"
    local total=0

    for caso in "$HERMES_LAB/certification/tests"/*/C-*.md; do
        [[ -f "$caso" ]] || continue
        caso_nombre=$(basename "$caso")
        while IFS=: read -r num linea; do
            while read -r posible; do
                [[ "$posible" == */ ]] && continue
                ruta="$HERMES_LAB/$posible"
                if [[ ! -f "$ruta" ]]; then
                    echo "CERT-ROTO: $caso_nombre línea $num → $posible" | tee -a "$informe"
                    total=$((total + 1))
                fi
            done < <(echo "$linea" | grep -oP '(docs/|skills/|certification/)\w[\w./-]*' || true)
        done < <(grep -n -oP '(docs/|skills/|certification/)\w[\w./-]*' "$caso" || true)
    done

    if [[ "$total" -eq 0 ]]; then
        echo "  OK: 0 certificaciones con referencias rotas."
    else
        echo "  TOTAL: $total referencia(s) rota(s) en certificaciones. Severidad: ALTA"
    fi
}

# --- MAIN -------------------------------------------------------------------

if [[ $# -eq 0 ]]; then
    show_help
    exit 0
fi

fecha=$(date '+%Y-%m-%d %H:%M')
echo "knowledge-governor — $fecha"
echo "Laboratorio: $HERMES_LAB"
echo "Informes: $OUTDIR/"
echo ""

case "$1" in
    --all)
        check_duplicados
        echo ""
        check_rotos
        echo ""
        check_decisiones_pendientes
        echo ""
        check_skills_huerfanas
        echo ""
        check_changelogs
        echo ""
        check_certificaciones
        echo ""
        echo "--- Resumen ---"
        echo "Informes disponibles en: $OUTDIR/"
        ;;
    --duplicados) check_duplicados ;;
    --rotos) check_rotos ;;
    --decisiones-pendientes) check_decisiones_pendientes ;;
    --skills-huerfanas) check_skills_huerfanas ;;
    --changelogs) check_changelogs ;;
    --certificaciones) check_certificaciones ;;
    --help|*) show_help ;;
esac
