#!/bin/bash
# Batería visión: LFM 2.5 VL 3B vs GLM-4.6v-flash — orquestador (21-ago-2026)
# Flujo: unload GLM → load LFM → batería LFM → unload LFM → load GLM → batería GLM
set -e
cd /home/jokoalmi/joko-lab
LOG=/tmp/bateria_vision_log.txt
echo "=== BATERÍA VISIÓN $(date '+%H:%M:%S') ===" | tee $LOG

# 1. Descargar GLM (libera VRAM)
echo "[1/6] Descargando GLM..." | tee -a $LOG
lms unload glm-4.6v-flash >/dev/null 2>&1 || true
# Matar llama-server huérfano si retiene VRAM
HUERFANO=$(ps aux | grep llama-server | grep -v grep | awk '{print $2}' | head -1)
if [ -n "$HUERFANO" ]; then kill $HUERFANO 2>/dev/null || true; fi
sleep 4
nvidia-smi --query-gpu=memory.used --format=csv,noheader | tee -a $LOG

# 2. Cargar LFM VL (id real de la API, NO nombre de carpeta — nombre carpeta se cuelga >9min)
echo "[2/6] Cargando lfm2.5-vl-3b..." | tee -a $LOG
lms load lfm2.5-vl-3b 2>&1 | tail -1 | tee -a $LOG
sleep 5

# 3. Batería con LFM
echo "[3/6] Ejecutando batería LFM..." | tee -a $LOG
python3 tools/bateria_vision_compare.py "lfm2.5-vl-3b" 2>&1 | tee -a $LOG

# 4. Descargar LFM
echo "[4/6] Descargando LFM..." | tee -a $LOG
lms unload lfm2.5-vl-3b >/dev/null 2>&1 || true
HUERFANO2=$(ps aux | grep llama-server | grep -v grep | awk '{print $2}' | head -1)
if [ -n "$HUERFANO2" ]; then kill $HUERFANO2 2>/dev/null || true; fi
sleep 4

# 5. Cargar GLM
echo "[5/6] Cargando GLM..." | tee -a $LOG
lms load glm-4.6v-flash 2>&1 | tail -1 | tee -a $LOG
sleep 5

# 6. Batería con GLM
echo "[6/6] Ejecutando batería GLM..." | tee -a $LOG
python3 tools/bateria_vision_compare.py "glm-4.6v-flash" 2>&1 | tee -a $LOG

echo "" | tee -a $LOG
echo "=== COMPARATIVA RÁPIDA ===" | tee -a $LOG
echo "(ver JSONs: /tmp/bateria_vision_LFM2.5-VL-3B-GGUF.json y /tmp/bateria_vision_glm-4.6v-flash.json)" | tee -a $LOG
echo "=== FIN $(date '+%H:%M:%S') ===" | tee -a $LOG
