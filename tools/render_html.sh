#!/usr/bin/env bash
# render_html.sh — render HTML→PNG/PDF único del Joko Lab (Chrome headless).
# Sustituye a los flags dispersos por research/: un solo sitio decide los flags,
# así que dos piezas distintas no salen con reglas distintas.
#
# USO
#   render_html.sh <entrada.html> <salida.png> [ancho] [alto] [escala]
#   render_html.sh --pdf <entrada.html> <salida.pdf> [ancho] [alto]
#
# OPCIONES
#   --espera=MS   virtual-time-budget (def. 10000). Las fuentes web lo necesitan.
#   --escala=N    force-device-scale-factor (def. 1). 2 -> 2160x2700.
#   --estricto    convierte el aviso de "fuente declarada ausente" en error.
#   --forzar      sobrescribe la salida sin copia .bak previa.
#
# DECISIONES INCORPORADAS (medidas, no supuestas)
#   * NO se usa --disable-gpu: no es causa universal de un PNG sin texto; el caso
#     "33 KB sin texto" era captura PREMATURA (falta de espera). Ver skill infografia-html.
#   * --virtual-time-budget SIEMPRE (los 5 scripts previos del lab ya lo tenían).
#   * file:// con ruta ABSOLUTA siempre: una ruta relativa hace que Chrome capture
#     SU página de error (fondo ~(32,33,36), ~33 KB).
#   * Comprobación de fuente ANTES de renderizar: si la familia declarada no existe,
#     Chrome cae en silencio a la reserva y la pieza sale con otra tipografía y otros
#     cortes de línea sin dar ningún error (medido 24-sep-2026: 5,32 % de píxeles).
#   * 1x por defecto: medido sobre 6 slides, el 2x reescalado a tamaño de publicación
#     no mejora la agudeza de forma consistente y pesa 2,2x más (69 KB -> 152 KB).
#
# SALIDA/EXIT: 0 ok | 2 uso | 3 HTML inexistente | 4 fuente ausente (--estricto)
#              5 salida no generada o sospechosamente pequeña | 6 dimensiones distintas
set -uo pipefail

CHROME="${CHROME:-$(command -v google-chrome-stable || command -v google-chrome || command -v chromium || command -v chromium-browser)}"
MODE=png; ESPERA=10000; ESCALA=1; ESTRICTO=0; FORZAR=0
ARGS=()
for a in "$@"; do
  case "$a" in
    --pdf) MODE=pdf ;;
    --espera=*) ESPERA="${a#*=}" ;;
    --escala=*) ESCALA="${a#*=}" ;;
    --estricto) ESTRICTO=1 ;;
    --forzar) FORZAR=1 ;;
    -h|--help) sed -n '2,25p' "$0"; exit 0 ;;
    *) ARGS+=("$a") ;;
  esac
done
IN="${ARGS[0]:-}"; OUT="${ARGS[1]:-}"
W="${ARGS[2]:-1080}"; H="${ARGS[3]:-1350}"
[ -z "$IN" ] || [ -z "$OUT" ] && { echo "USO: render_html.sh [--pdf] <entrada.html> <salida> [ancho] [alto] [escala]" >&2; exit 2; }
[ -n "$CHROME" ] || { echo "ERROR: no encuentro google-chrome/chromium en el PATH" >&2; exit 2; }
FRAG=""
case "$IN" in *"#"*) FRAG="#${IN#*#}"; IN="${IN%%#*}" ;; esac
[ -f "$IN" ] || { echo "ERROR: no existe el HTML: $IN" >&2; exit 3; }
IN_ABS="$(readlink -f "$IN")"; OUT_ABS="$(readlink -f "$(dirname "$OUT")")/$(basename "$OUT")"

# --- comprobación de fuente (antes de renderizar) ---
if grep -qE '@font-face|fonts\.googleapis|fonts\.gstatic' "$IN_ABS"; then
  echo "NOTA: el HTML carga fuentes web → la comprobación local de fuentes no aplica; con --espera=$ESPERA debería bastar."
else
  FAMILIAS=$(grep -oiE 'font-family:[^;}"]*' "$IN_ABS" | sed 's/.*://' \
             | awk -F',' '{print $1}' \
             | sed "s/['\"]//g; s/^[[:space:]]*//; s/[[:space:]]*$//" | grep -v '^$' | sort -u)
  AVISADO=0
  while IFS= read -r f; do
    case "$f" in
      sans-serif|serif|monospace|cursive|fantasy|system-ui|ui-sans-serif|ui-serif|ui-monospace|inherit|initial|unset|\-apple-system|BlinkMacSystemFont) continue ;;
      var\(*|\$*) continue ;;
    esac
    if ! fc-match -f '%{family}\n' "$f" 2>/dev/null | tr 'A-Z' 'a-z' | grep -qF "$(printf '%s' "$f" | tr 'A-Z' 'a-z')"; then
      echo "AVISO: la PRIMERA familia declarada ('$f') no está instalada -> Chrome usará la reserva en silencio" >&2
      echo "       (la pieza sale con otra tipografía y otros cortes de línea, sin dar ningún error)." >&2
      if [ "$AVISADO" = "0" ]; then
        echo "       Instalación sin sudo (ej. Inter): apt-get download fonts-inter && dpkg-deb -x fonts-inter_*.deb /tmp/i && cp /tmp/i/usr/share/fonts/opentype/inter/*.otf ~/.local/share/fonts/Inter/ && fc-cache -f" >&2
      fi
      AVISADO=1
      [ "$ESTRICTO" = "1" ] && exit 4
    fi
  done <<< "$FAMILIAS"
fi

# --- copia previa (RULE-008) ---
if [ -f "$OUT_ABS" ] && [ "$FORZAR" != "1" ]; then
  BAK="${OUT_ABS}.bak-$(date +%Y%m%d%H%M)"
  cp -p "$OUT_ABS" "$BAK" && echo "copia previa: $BAK"
fi

T0=$(date +%s%N)
if [ "$MODE" = "pdf" ]; then
  "$CHROME" --headless=new --hide-scrollbars --no-pdf-header-footer \
    --virtual-time-budget="$ESPERA" --run-all-compositor-stages-before-draw \
    --print-to-pdf="$OUT_ABS" "file://$IN_ABS$FRAG" >/dev/null 2>&1
  RC=$?
else
  "$CHROME" --headless=new --hide-scrollbars \
    --virtual-time-budget="$ESPERA" --window-size="$W,$H" \
    --force-device-scale-factor="$ESCALA" --screenshot="$OUT_ABS" \
    "file://$IN_ABS$FRAG" >/dev/null 2>&1
  RC=$?
fi
T1=$(date +%s%N)

[ -f "$OUT_ABS" ] || { echo "ERROR: Chrome no generó la salida (rc=$RC): $OUT_ABS" >&2; exit 5; }
BYTES=$(stat -c %s "$OUT_ABS")
if [ "$MODE" = "pdf" ]; then MIN=2000; else MIN=50000; fi
if [ "$BYTES" -lt "$MIN" ]; then
  echo "ERROR: la salida pesa $BYTES B (<$MIN B): sospechoso." >&2
  echo "       Causas típicas: captura prematura (sube --espera), ruta/URL mala o HTML roto." >&2
  exit 5
fi

if [ "$MODE" = "png" ]; then
  DIM=$(magick identify -format '%wx%h' "$OUT_ABS" 2>/dev/null || file -b "$OUT_ABS" | grep -oE '[0-9]+x[0-9]+' | head -1)
  EXP="$(python3 -c "print(int($W*$ESCALA))")x$(python3 -c "print(int($H*$ESCALA))")"
  MD5=$(md5sum "$OUT_ABS" | cut -d' ' -f1)
  echo "ok png $OUT_ABS  ${DIM}  ${BYTES} B  ${EXP} esperado  ${MD5}  $(( (T1-T0)/1000000 )) ms  (escala ${ESCALA}x)"
  [ "$DIM" != "$EXP" ] && { echo "ERROR: dimensiones $DIM != $EXP esperado" >&2; exit 6; }
else
  MD5=$(md5sum "$OUT_ABS" | cut -d' ' -f1)
  PAG=$(pdfinfo "$OUT_ABS" 2>/dev/null | grep -i '^Pages' | awk '{print $2}')
  TXT=$(pdftotext "$OUT_ABS" - 2>/dev/null | tr -s '[:space:]' ' ' | wc -c)
  echo "ok pdf $OUT_ABS  páginas=${PAG:-?}  ${BYTES} B  texto_extraíble=${TXT} B  ${MD5}  $(( (T1-T0)/1000000 )) ms"
  [ "${TXT:-0}" -lt 50 ] && echo "AVISO: el PDF casi no tiene texto extraíble: puede no ser vectorial." >&2
fi
exit 0
