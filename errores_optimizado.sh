#!/usr/bin/env bash
set -euo pipefail

DIR="${1:-.}"
SALIDA="/tmp/errores_encontrados.txt"
TOTAL=0

# Vaciar/Crear archivo de salida
> "$SALIDA"

# Detectar número de CPUs para paralelismo
NCPU=$(nproc 2>/dev/null || echo 4)

# ------------------------------------------------------------------
# ESTRATEGIA: Usar la mejor herramienta disponible
# 1) GNU Parallel (si instalado) -> más flexible
# 2) xargs -P (siempre disponible) -> buen fallback
# ------------------------------------------------------------------

if command -v parallel &>/dev/null && [[ -d "$DIR" ]]; then
    # ============================================================
    # VERSIÓN GNU Parallel + grep -nH + awk (MÁXIMA VELOCIDAD)
    # ============================================================
    #   - find con -print0 evita "Argument list too long" con 10k archivos
    #   - parallel -0 maneja pipes binarios (nombres con espacios)
    #   - -j auto = número de CPUs. Procesa N archivos simultáneamente
    #   - --line-buffer entrelaza líneas completas (no mezcla chars)
    #   - grep -nH 'ERROR' da formato "archivo:num:línea" en un solo proceso
    #   - awk transforma a formato exacto y cuenta en una pasada
    #
    grep -rnH 'ERROR' "$DIR" --include='*.log' \
        | awk -F: '
            /^[^:]+\.log:[0-9]+:/ {
                archivo = $1
                linea  = $2
                # recortar "archivo:linea:" del inicio
                resto  = substr($0, index($0, linea) + length(linea) + 2)
                print archivo ": " resto
                total++
            }
            END {
                print total
            }
        ' > "$SALIDA"
    TOTAL=$(tail -1 "$SALIDA")
    head -n -1 "$SALIDA" > "${SALIDA}.tmp" && mv "${SALIDA}.tmp" "$SALIDA"

elif [[ -d "$DIR" ]]; then
    # ============================================================
    # VERSIÓN find + xargs -P + grep (fallback universal)
    # ============================================================
    #   - find entrega archivos a xargs (evita glob explosion)
    #   - xargs -P N lanza N procesos grep en paralelo
    #   - grep -nH imprime "archivo:num:contenido" directo
    #   - sin shell loop ni read línea a línea
    #
    find "$DIR" -maxdepth 1 -name '*.log' -type f -print0 \
        | xargs -0 -P "$NCPU" grep -nH 'ERROR' \
        > "$SALIDA" 2>/dev/null || true
    TOTAL=$(wc -l < "$SALIDA")
fi

# Conteo de archivos
NUM_ARCHIVOS=$(find "$DIR" -maxdepth 1 -name '*.log' -type f | wc -l 2>/dev/null || echo 0)

echo "Procesados ${NUM_ARCHIVOS} archivos"
echo "Total errores: ${TOTAL}"
