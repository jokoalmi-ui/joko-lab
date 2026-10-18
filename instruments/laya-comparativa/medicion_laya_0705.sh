#!/usr/bin/env bash
# =====================================================================
# Medicion de Laya sobre el set congelado v3 (299 casos) — rig
# LAYA-COMPARATIVA.  Lo lanza el cron de Hermes a las 07:05.
#
# NO descarga nada: los pesos (convaiinnovations/laya) y los encoders
# (answerdotai/ModernBERT-large, jhu-clsp/mmBERT-base) ya estan en la
# cache HF.  NO toca ningun servicio del stack: solo usa la GPU.
# =====================================================================
set -u
RIG=/home/jokoalmi/joko-lab/instruments/laya-comparativa
cd "$RIG" || { echo "ERROR: no existe $RIG"; exit 1; }

TS=$(date +%Y%m%d_%H%M)
LOG="$RIG/medicion_laya_${TS}.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== MEDICION LAYA (set v3, 299 casos) — INICIO $(date '+%F %T %Z') ==="
echo "log: $LOG"
echo
echo "--- GPU antes ---"
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu \
  --format=csv,noheader 2>&1
echo
echo "--- python / torch / cuda ---"
.venv/bin/python - <<'PY'
import torch, transformers
print("torch", torch.__version__, "cuda_ok", torch.cuda.is_available(),
      "|", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "-")
print("transformers", transformers.__version__)
PY
echo
echo "--- selftest del motor de metricas (debe dar PASS/0 FALLO) ---"
.venv/bin/python run_test.py --selftest
echo "selftest exit=$?"
echo

FALLOS=""
for CK in router english multilingual typed-decisions; do
  echo
  echo "################ CHECKPOINT $CK ################"
  T0=$(date +%s)
  .venv/bin/python run_test.py --backend laya --checkpoint "$CK" --set v3
  RC=$?
  T1=$(date +%s)
  echo ">>> checkpoint $CK: exit=$RC  duracion=$((T1 - T0)) s"
  [ "$RC" -ne 0 ] && FALLOS="$FALLOS $CK(exit=$RC)"
  echo "--- GPU tras $CK ---"
  nvidia-smi --query-gpu=memory.used,utilization.gpu,temperature.gpu \
    --format=csv,noheader 2>&1
done

echo
echo "=============== COMPARATIVA (misma puntuacion para todos) ==============="
.venv/bin/python comparar_modelos.py \
  numctx8192_granite_v3.json \
  numctx8192_qwen_v3.json \
  numctx8192_r1_v3.json \
  resultados_laya_router_v3.json \
  resultados_laya_english_v3.json \
  resultados_laya_multilingual_v3.json \
  resultados_laya_typed-decisions_v3.json

echo
echo "--- ficheros generados ---"
ls -l resultados_laya_*_v3.json 2>&1
echo
echo "--- sha256 de los resultados (calculado, nunca transcrito) ---"
sha256sum resultados_laya_*_v3.json 2>&1
echo
echo "=== FIN $(date '+%F %T %Z') — checkpoints con fallo:${FALLOS:- ninguno} ==="
