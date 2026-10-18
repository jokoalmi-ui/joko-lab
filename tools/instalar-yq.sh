#!/usr/bin/env bash
# instalar-yq.sh — instala/actualiza yq v4 (mikefarah, Go) en ~/.local/bin, SIN sudo,
# verificando el SHA-256 contra el `digest` oficial que publica la API de GitHub.
#
#   uso:   instalar-yq.sh [tag]      # p.ej. v4.54.1 ; sin argumento: ultima release
#   reglas: no usa sudo; escribe SOLO en ~/.local/bin (o $YQ_DEST); idempotente
#           (si el binario instalado ya tiene el sha256 del release objetivo, no toca nada).
#   aviso:  NO usar `apt install yq` en Ubuntu — ese paquete es python-yq 3.4.3
#           (wrapper de jq), sin `--front-matter` ni `-i`.
#   origen: verificacion por digest de la API, no por el asset `checksums`
#           (que en este repo es una tabla multi-algoritmo, no formato sha256sum).
set -euo pipefail

case "$(uname -m)" in
  x86_64)        ASSET="yq_linux_amd64" ;;
  aarch64|arm64) ASSET="yq_linux_arm64" ;;
  *) echo "ABORTO: arquitectura no contemplada aqui: $(uname -m)"; exit 1 ;;
esac

REPO="mikefarah/yq"
DEST="${YQ_DEST:-$HOME/.local/bin}"
mkdir -p "$DEST"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

API="https://api.github.com/repos/$REPO"
if [ -z "${1:-}" ]; then
  curl -fsSL -o "$WORK/latest.json" "$API/releases/latest"
  TAG="$(/usr/bin/python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["tag_name"])' "$WORK/latest.json")"
else
  TAG="$1"
fi
[ -n "$TAG" ] || { echo "ABORTO: no puedo determinar el tag"; exit 1; }
echo "release objetivo: $TAG"

curl -fsSL -o "$WORK/release.json" "$API/releases/tags/$TAG"
EXP="$(/usr/bin/python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
m=[a for a in d["assets"] if a["name"]==sys.argv[2]]
print(m[0].get("digest","") if m else "")' "$WORK/release.json" "$ASSET")"
[ -n "$EXP" ] || { echo "ABORTO: la API no publica digest para $ASSET"; exit 1; }

curl -fsSL -o "$WORK/$ASSET" "https://github.com/$REPO/releases/download/$TAG/$ASSET"
GOT="sha256:$(sha256sum "$WORK/$ASSET" | awk '{print $1}')"
echo "oficial : $EXP"
echo "descarga: $GOT"
[ "$EXP" = "$GOT" ] || { echo "ABORTO: el sha256 no coincide -> no instalo"; exit 1; }

if [ -x "$DEST/yq" ]; then
  CUR="sha256:$(sha256sum "$DEST/yq" | awk '{print $1}')"
  if [ "$CUR" = "$EXP" ]; then
    echo "ya instalado el mismo binario ($TAG) en $DEST/yq -> no toco nada"
    "$DEST/yq" --version
    exit 0
  fi
  echo "AVISO: existe $DEST/yq con otro sha256 -> se sustituye (copia previa .bak)"
  cp -p "$DEST/yq" "$DEST/yq.bak-$(date +%Y%m%d-%H%M%S)"
fi

install -m 0755 "$WORK/$ASSET" "$DEST/yq"
echo "instalado: $DEST/yq"
"$DEST/yq" --version
HLP="$("$DEST/yq" --help 2>&1 || true)"
case "$HLP" in
  *front-matter*) echo "identidad OK: es mikefarah v4 (tiene --front-matter)" ;;
  *) echo "AVISO: no veo --front-matter; revisar que no sea el python-yq" ;;
esac
case ":$PATH:" in
  *":$DEST:"*) ;;
  *) echo "AVISO: anade $DEST al PATH" ;;
esac
