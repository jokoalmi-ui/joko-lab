#!/bin/bash
# Servidor OCR del Joko Lab: HunyuanOCR (1,1B, Q8_0) sobre llama-server.
# Escucha SOLO en 127.0.0.1:8099. No usa `lms` (su daemon no arranca en este host).
set -euo pipefail

B=/home/jokoalmi/.lmstudio/extensions/backends/llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.62.1
VENDOR=/home/jokoalmi/.lmstudio/extensions/backends/vendor/linux-llama-cuda12-vendor-v1
M="/mnt/ssd_ia_datos/LM STUDIO/ggml-org/HunyuanOCR-GGUF"

PORT="${OCR_PORT:-8099}"
CTX="${OCR_CTX:-8192}"

[ -x "$B/llama-server" ] || { echo "ERROR: no encuentro llama-server en $B" >&2; exit 1; }
[ -f "$M/HunyuanOCR-Q8_0.gguf" ] || { echo "ERROR: falta $M/HunyuanOCR-Q8_0.gguf" >&2; exit 1; }
[ -f "$M/mmproj-HunyuanOCR-Q8_0.gguf" ] || { echo "ERROR: falta el mmproj" >&2; exit 1; }

export LD_LIBRARY_PATH="$B:$VENDOR"
exec "$B/llama-server" \
  -m "$M/HunyuanOCR-Q8_0.gguf" \
  --mmproj "$M/mmproj-HunyuanOCR-Q8_0.gguf" \
  -ngl 99 -c "$CTX" --host 127.0.0.1 --port "$PORT" --no-webui
