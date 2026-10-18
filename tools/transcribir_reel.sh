#!/usr/bin/env bash
# Wrapper de extraer_audio_y_transcribir.py
# ⚠️ Necesita LD_LIBRARY_PATH con libcublas.so.12 (CUDA 12 wheel) ANTES de
# arrancar Python — el seteo dentro del script no llega al cargador dinámico
# de CTranslate2 (validado 13-ago-2026).
export LD_LIBRARY_PATH="$HOME/.hermes/hermes-agent/venv/lib/python3.11/site-packages/nvidia/cublas/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
# Pasar "auto" como device de forma segura: si solo hay 1-2 args, auto va como
# 2º o 3º arg según corresponda (el script lee device en sys.argv[3])
ARGS=("$@")
if [ ${#ARGS[@]} -ge 1 ] && [ ${#ARGS[@]} -le 2 ]; then
  ARGS+=("auto")
fi
exec /home/jokoalmi/.hermes/hermes-agent/venv/bin/python3 /home/jokoalmi/joko-lab/tools/extraer_audio_y_transcribir.py "${ARGS[@]}"
