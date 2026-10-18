#!/usr/bin/env bash
# descargar_simple_icons.sh — Descarga logos REALES de Simple Icons (SVG) a disco local.
# Uso: bash descargar_simple_icons.sh [slug1 slug2 ...]
#   - sin argumentos: usa la lista por defecto de marcas del lab
#   - salida: ~/joko-lab/assets/simple-icons/<slug>.svg (SVG monocromo, fill heredable)
# Origen: https://cdn.simpleicons.org/<slug> (CDN oficial de Simple Icons)
# Nota: los SVG son MONOCROMO (un solo color). Para colorearlos en CSS:
#   .icono { color: #X; }  +  <svg class="icono" ...> con fill="currentColor"
#   o inyectar el SVG inline y usar CSS: svg path { fill: currentColor; }
# Validado 19-ago-2026: github, docker, python, telegram, linux, n8n, ollama, comfyui → HTTP 200.

set -euo pipefail

DEST="${HOME}/joko-lab/assets/simple-icons"
mkdir -p "$DEST"

DEFAULT="github docker python telegram linux n8n ollama comfyui google cloudflare openai"

SLUGS=("$@")
if [ ${#SLUGS[@]} -eq 0 ]; then
    read -r -a SLUGS <<< "$DEFAULT"
fi

ok=0; fail=0
for slug in "${SLUGS[@]}"; do
    # El slug puede tener la forma "org/repo" → convertir a ruta de archivo segura
    fname=$(echo "$slug" | tr '/' '-')
    out="$DEST/$fname.svg"
    if curl -s -f -m 15 -o "$out" "https://cdn.simpleicons.org/$slug"; then
        # sanity: debe ser SVG y no vacío
        if head -c 1 "$out" | grep -q '<'; then
            echo "✅ $slug → $out ($(wc -c < "$out") bytes)"
            ok=$((ok+1))
        else
            echo "⚠️ $slug: descarga no parece SVG, eliminando"
            rm -f "$out"
            fail=$((fail+1))
        fi
    else
        echo "❌ $slug: fallo de descarga (¿slug correcto?)"
        fail=$((fail+1))
    fi
done

echo ""
echo "Resumen: $ok OK, $fail fallos. Directorio: $DEST"
[ "$fail" -eq 0 ]
