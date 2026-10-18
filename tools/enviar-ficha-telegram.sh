#!/usr/bin/env bash
# enviar-ficha-telegram.sh — envío de ficha/imagen a Telegram con caption SANEADO.
#
# POR QUÉ EXISTE (17-sep-2026, ficha Papyrus Moléculaire): el envío se hacía con
# `hermes send --to telegram:<id> "<i>«saludo»</i>\n\nMEDIA:/ruta.png"` y el
# usuario vio caracteres sueltos al final del saludo. Causa verificada simulando
# el pipeline real de Hermes (extract_media + _media_caption_split + _telegram_format):
#   1) bash NO interpreta `\n` dentro de comillas dobles -> los 4 caracteres
#      `\n\n` llegan literales al final del caption.
#   2) `<i>` fuerza parse_mode=HTML (y si el HTML no parsea, los tags se ven).
# Este wrapper construye el comando él mismo y sanea el saludo, de modo que el
# resultado no depende de cómo lo escriba el agente.
#
# Uso:
#   tools/enviar-ficha-telegram.sh <ruta.png> "<saludo>" [chat_id|dm|canal] [--dry-run]
#
#   chat_id por defecto: canal del lab (-1003968087263); "dm" = 1052590045.
#   --dry-run: imprime el caption EXACTO y el comando, sin enviar nada.
#
# Salidas: 0 = enviado (o dry-run ok) · 2 = saludo vacío · 3 = PNG no existe
#          4 = uso incorrecto · 5 = fallo de hermes send

set -euo pipefail

uso() {
  printf 'Uso: %s <ruta.png> "<saludo>" [chat_id|dm|canal] [--dry-run]\n' "$(basename "$0")" >&2
  exit 4
}

[[ $# -ge 2 ]] || uso
png="$1"; saludo="$2"; shift 2

chat="canal"
dry=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) dry=1 ;;
    dm|canal|-*) chat="$arg" ;;
    *) echo "ERROR: argumento no reconocido: $arg" >&2; uso ;;
  esac
done

case "$chat" in
  dm)    chat_id="1052590045" ;;
  canal) chat_id="-1003968087263" ;;
  *)     chat_id="$chat" ;;
esac

# --- saneado del saludo ------------------------------------------------
# 1) secuencias LITERALES \n \r \t -> espacio
saludo="${saludo//\\n/ }"
saludo="${saludo//\\r/ }"
saludo="${saludo//\\t/ }"
# 2) tags HTML simples -> fuera (evita forzar parse_mode=HTML)
for tag in i b u s em strong code pre; do
  saludo="${saludo//<$tag>/}"
  saludo="${saludo//<\/$tag>/}"
done
# 3) saltos REALES y tabuladores -> espacio, y colapsar espacios repetidos
saludo="$(printf '%s' "$saludo" | tr '\n\t' '  ' | tr -s ' ' | sed -e 's/^ *//' -e 's/ *$//')"

[[ -n "$saludo" ]] || { echo "ERROR: el saludo quedó vacío tras el saneado." >&2; exit 2; }
[[ -f "$png" ]]    || { echo "ERROR: no existe el PNG: $png" >&2; exit 3; }
png="$(realpath "$png")"   # el caption debe llevar ruta ABSOLUTA (hermes send la resuelve)

check="$saludo"
check="${check#«}"; check="${check#\"}"; check="${check#\'}"
case "$check" in
  "Buenos"*) ;;
  *) echo "AVISO: el saludo no empieza por «Buenos días» (regla del lab 01-sep-2026)." >&2 ;;
esac

# --- construcción (el MEDIA: se extrae solo; el caption queda con strip()) ---
caption="$saludo MEDIA:$png"
hermes_bin="${HERMES_BIN:-$(command -v hermes || echo "$HOME/.local/bin/hermes")}"

printf 'caption exacto: %s\n' "$caption"
printf 'destino       : telegram:%s\n' "$chat_id"

if [[ "$dry" == "1" ]]; then
  printf 'comando       : %s send --to telegram:%s "<caption>"\n' "$hermes_bin" "$chat_id"
  echo "(dry-run: NO se ha enviado nada)"
  exit 0
fi

if ! "$hermes_bin" send --to "telegram:$chat_id" "$caption"; then
  echo "ERROR: 'hermes send' ha fallado (exit != 0)." >&2
  exit 5
fi
