#!/usr/bin/env bash
# cleanup.sh — Limpieza de logs y temporales del laboratorio
# Uso: ./cleanup.sh [--dry-run] [--older-than N] [--all]
set +e

DRY_RUN=false
OLDER_THAN=30
CLEAN_ALL=false
ROOT="/home/jokoalmi/hermes-lab"
TOTAL=0

mostrar_ayuda() {
    cat <<EOF
Uso: $0 [OPCIONES]

Limpia logs y archivos temporales del laboratorio.

Opciones:
  --dry-run           Mostrar qué se borraría sin borrar nada
  --older-than N      Borrar archivos con más de N días (default: 30)
  --all               Limpiar también logs de docker-admin y n8n-admin
  --help              Mostrar esta ayuda

Sin opciones, limpia solo logs/ de hermes-lab (más de 30 días).
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --older-than) OLDER_THAN="$2"; shift 2 ;;
        --all) CLEAN_ALL=true; shift ;;
        --help) mostrar_ayuda ;;
        *) echo "Opción desconocida: $1"; exit 1 ;;
    esac
done

limpiar() {
    local dir="$1"
    local pattern="$2"
    local label="$3"
    local count=0

    if [[ ! -d "$dir" ]]; then
        return
    fi

    while IFS= read -r -d '' f; do
        if $DRY_RUN; then
            echo "  [DRY-RUN] $f ($(du -h "$f" | cut -f1))"
        else
            rm -f "$f"
            echo "  ✗ $f eliminado"
        fi
        count=$((count + 1))
    done < <(find "$dir" -name "$pattern" -type f -mtime "+$OLDER_THAN" -print0 2>/dev/null)

    TOTAL=$((TOTAL + count))
    [[ $count -gt 0 ]] && echo "  → $label: $count archivo(s)"
}

echo "═══════════════════════════════════════"
echo "  Cleanup — Joko Lab"
echo "  $(date '+%Y-%m-%d %H:%M')"
$DRY_RUN && echo "  Modo: DRY-RUN (no se borra nada)"
echo "  Antigüedad: > $OLDER_THAN días"
echo "═══════════════════════════════════════"

# Siempre: logs del laboratorio
echo -e "\n■ Logs del laboratorio ($ROOT/logs/)"
limpiar "$ROOT/logs" "*.log" "logs de hermes-lab"

# Opcional: docker-admin
if $CLEAN_ALL; then
    echo -e "\n■ Logs de docker-admin ($ROOT/skills/docker-admin/logs/)"
    limpiar "$ROOT/skills/docker-admin/logs" "*.log" "logs de docker-admin"
fi

# Opcional: n8n-admin (solo el log de healthcheck, no exports)
if $CLEAN_ALL; then
    echo -e "\n■ Logs de n8n-admin ($ROOT/skills/n8n-admin/logs/)"
    limpiar "$ROOT/skills/n8n-admin/logs" "*.log" "logs de n8n-admin"
fi

# Resumen
echo
echo "═══════════════════════════════════════"
if $DRY_RUN; then
    echo "  DRY-RUN: $TOTAL archivo(s) se borrarían"
    echo "  Ejecuta sin --dry-run para borrarlos"
else
    echo "  $TOTAL archivo(s) eliminados"
fi
echo "═══════════════════════════════════════"
