#!/usr/bin/env bash
# Wrapper de transcribir_youtube_fallback.py
# LD_LIBRARY_PATH con libcublas.so.12 ANTES de arrancar Python (patrón validado).
export LD_LIBRARY_PATH="$HOME/.hermes/hermes-agent/venv/lib/python3.11/site-packages/nvidia/cublas/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec /home/jokoalmi/.hermes/hermes-agent/venv/bin/python3 /home/jokoalmi/joko-lab/tools/transcribir_youtube_fallback.py "$@"
