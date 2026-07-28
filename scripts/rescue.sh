#!/bin/bash
# rescue.sh — Copia de rescate para Joko Lab
# Respalda lo IRREMPLAZABLE y genera inventario de lo REEMPLAZABLE.
# Destino: USB externo (/run/media/jokoalmi/New Volume/joko-lab-rescue/)
set +e

DEST="/run/media/jokoalmi/New Volume/joko-lab-rescue"
FECHA=$(date +%Y-%m-%d_%H-%M)
DIR="$DEST/$FECHA"

# Si el USB no está montado, abortar
if [ ! -d "$DEST" ]; then
    echo "ERROR: USB externo no montado en /run/media/jokoalmi/New Volume"
    exit 1
fi

mkdir -p "$DIR"

PASS=0
FAIL=0
TOTAL=0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  RESCATE — Copia de seguridad ($FECHA)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ═══════════════════════════════════════════════════════
# PARTE 1: COPIAR LO IRREMPLAZABLE
# ═══════════════════════════════════════════════════════

echo "── IRREMPLAZABLE ──"
echo ""

# 1. Configs del sistema
((TOTAL++))
echo -n "  [$TOTAL] Configs sistema (.bashrc, .profile, crontab, systemd)... "
mkdir -p "$DIR/system-config"
cp ~/.bashrc "$DIR/system-config/" 2>/dev/null
cp ~/.profile "$DIR/system-config/" 2>/dev/null
crontab -l > "$DIR/system-config/crontab.txt" 2>/dev/null
cp -r ~/.config/systemd/user/*.service "$DIR/system-config/" 2>/dev/null
cp -r ~/.config/systemd/user/*.timer "$DIR/system-config/" 2>/dev/null
cp -r ~/.config/autostart/*.desktop "$DIR/system-config/" 2>/dev/null
echo "✓ ($(ls "$DIR/system-config" | wc -l) archivos)"
((PASS++))

# 2. SSH keys
((TOTAL++))
echo -n "  [$TOTAL] SSH keys... "
mkdir -p "$DIR/ssh"
cp ~/.ssh/id_* "$DIR/ssh/" 2>/dev/null
echo "✓"
((PASS++))

# 3. Runtime environment (uv, cargo, local/bin)
((TOTAL++))
echo -n "  [$TOTAL] Runtime (uv, cargo, local/bin)... "
mkdir -p "$DIR/runtime"
if [ -d ~/.local/share/uv ]; then
    tar -czf "$DIR/runtime/uv.tar.gz" -C ~/.local/share uv 2>/dev/null
    echo -n "uv($(du -h "$DIR/runtime/uv.tar.gz" | cut -f1)) "
fi
if [ -d ~/.cargo/bin ]; then
    tar -czf "$DIR/runtime/cargo-bin.tar.gz" -C ~/.cargo bin 2>/dev/null
    echo -n "cargo($(du -h "$DIR/runtime/cargo-bin.tar.gz" | cut -f1)) "
fi
if [ -d ~/.local/bin ]; then
    cp ~/.local/bin/* "$DIR/runtime/" 2>/dev/null
    echo -n "local-bin($(ls "$DIR/runtime" | grep -v tar | wc -l) archivos) "
fi
# Guardar lista de lo que hay instalado (uv, cargo tools)
ls ~/.local/bin/ 2>/dev/null > "$DIR/runtime/local-bin-list.txt"
ls ~/.cargo/bin/ 2>/dev/null > "$DIR/runtime/cargo-bin-list.txt"
echo "✓"
((PASS++))

# 3. Hermes (config + skills + state.db)
((TOTAL++))
echo -n "  [$TOTAL] Hermes config + skills... "
hermes backup -o "$DIR/hermes-backup.zip" > /dev/null 2>&1
if [ -f "$DIR/hermes-backup.zip" ]; then
    SIZE=$(du -h "$DIR/hermes-backup.zip" | cut -f1)
    echo "✓ ($SIZE)"
    ((PASS++))
else
    echo "✗ (usando fallback tar)"
    tar -czf "$DIR/hermes-config.tar.gz" -C ~/.hermes config.yaml .env skills/ 2>/dev/null
    if [ -f "$DIR/hermes-config.tar.gz" ]; then
        echo "  → fallback OK"
        ((PASS++))
    else
        ((FAIL++))
    fi
fi

# 4. n8n (workflows + credenciales)
((TOTAL++))
echo -n "  [$TOTAL] n8n (workflows)... "
tar -czf "$DIR/n8n-backup.tar.gz" -C /mnt/ssd_ia_datos n8n 2>/dev/null
if [ -f "$DIR/n8n-backup.tar.gz" ]; then
    tar -tzf "$DIR/n8n-backup.tar.gz" >/dev/null 2>&1 && echo "✓ (verificado)" || echo "✗ (corrupto)"
    SIZE=$(du -h "$DIR/n8n-backup.tar.gz" 2>/dev/null | cut -f1)
    echo "  → $SIZE"
    ((PASS++))
else
    echo "✗"
    ((FAIL++))
fi

# 5. exports (documentos)
((TOTAL++))
echo -n "  [$TOTAL] exports... "
tar -czf "$DIR/exports-backup.tar.gz" -C /mnt/ssd_ia_datos exports 2>/dev/null
if [ -f "$DIR/exports-backup.tar.gz" ]; then
    tar -tzf "$DIR/exports-backup.tar.gz" >/dev/null 2>&1 && echo "✓ (verificado)" || echo "✗ (corrupto)"
    SIZE=$(du -h "$DIR/exports-backup.tar.gz" 2>/dev/null | cut -f1)
    echo "  → $SIZE"
    ((PASS++))
else
    echo "✗"
    ((FAIL++))
fi

# 6. lab-state (policies + secrets)
((TOTAL++))
echo -n "  [$TOTAL] lab-state (policies + secrets)... "
tar -czf "$DIR/lab-state.tar.gz" -C /mnt/ssd_ia_datos lab-state 2>/dev/null
if [ -f "$DIR/lab-state.tar.gz" ]; then
    tar -tzf "$DIR/lab-state.tar.gz" >/dev/null 2>&1 && echo "✓ (verificado)" || echo "✗ (corrupto)"
    SIZE=$(du -h "$DIR/lab-state.tar.gz" 2>/dev/null | cut -f1)
    echo "  → $SIZE"
    ((PASS++))
else
    echo "✗"
    ((FAIL++))
fi

# 7. perfume-ia (git bundle)
((TOTAL++))
echo -n "  [$TOTAL] perfume-ia... "
if [ -d ~/perfume-ia/.git ]; then
    cd ~/perfume-ia && git bundle create "$DIR/perfume-ia.bundle" --all 2>/dev/null
    echo "✓ (bundle)"
    ((PASS++))
else
    tar -czf "$DIR/perfume-ia.tar.gz" -C ~/ perfume-ia 2>/dev/null
    echo "✓ (tar, sin git)"
    ((PASS++))
fi

# 8. joko-lab
((TOTAL++))
echo -n "  [$TOTAL] joko-lab... "
tar -czf "$DIR/joko-lab.tar.gz" -C ~/ joko-lab 2>/dev/null
SIZE=$(du -h "$DIR/joko-lab.tar.gz" 2>/dev/null | cut -f1)
echo "✓ ($SIZE)"
((PASS++))

# 9. hermes-lab (git bundle)
((TOTAL++))
echo -n "  [$TOTAL] hermes-lab (git bundle)... "
cd ~/hermes-lab && git bundle create "$DIR/hermes-lab.bundle" --all 2>/dev/null
if [ -f "$DIR/hermes-lab.bundle" ]; then
    # Verificar integridad del bundle
    if git bundle verify "$DIR/hermes-lab.bundle" >/dev/null 2>&1; then
        echo "✓ (verificado)"
        ((PASS++))
    else
        echo "✗ (bundle corrupto)"
        ((FAIL++))
    fi
else
    echo "✗"
    ((FAIL++))
fi

# 10. automation-stack (docker-compose.yml)
((TOTAL++))
echo -n "  [$TOTAL] automation-stack... "
cp ~/automation-stack/docker-compose.yml "$DIR/docker-compose.yml" 2>/dev/null
cp ~/automation-stack/AGENTS.md "$DIR/AGENTS.md" 2>/dev/null
echo "✓"
((PASS++))

# ═══════════════════════════════════════════════════════
# PARTE 2: INVENTARIO DE LO REEMPLAZABLE
# ═══════════════════════════════════════════════════════

echo ""
echo "── INVENTARIO (reemplazable) ──"
echo ""

INV="$DIR/inventario.md"

cat > "$INV" << 'HEADER'
# Inventario de restauración — Joko Lab

Este archivo describe qué instalar/descargar para reconstruir el sistema.
NO contiene los datos en sí, solo las instrucciones para obtenerlos.

HEADER

echo "**Fecha:** $FECHA" >> "$INV"
echo "" >> "$INV"

# --- Ollama models ---
((TOTAL++))
echo -n "  [$TOTAL] Inventario Ollama... "
echo "## Modelos Ollama" >> "$INV"
echo "" >> "$INV"
echo '```bash' >> "$INV"
docker compose -f ~/automation-stack/docker-compose.yml exec ollama ollama list 2>/dev/null | tail -n +2 | while read -r NAME ID SIZE REST; do
    echo "ollama pull $NAME   # $SIZE" >> "$INV"
done
echo '```' >> "$INV"
echo "" >> "$INV"
echo "✓"
((PASS++))

# --- Docker images ---
((TOTAL++))
echo -n "  [$TOTAL] Inventario Docker... "
echo "## Imágenes Docker" >> "$INV"
echo "" >> "$INV"
echo '```bash' >> "$INV"
docker compose -f ~/automation-stack/docker-compose.yml images 2>/dev/null | tail -n +2 | while read -r CONTAINER REPO TAG IMAGE_ID SIZE; do
    echo "docker pull $REPO:$TAG   # $SIZE" >> "$INV"
done
echo '```' >> "$INV"
echo "" >> "$INV"
echo "✓"
((PASS++))

# --- LM Studio models ---
((TOTAL++))
echo -n "  [$TOTAL] Inventario LM Studio... "
echo "## Modelos LM Studio" >> "$INV"
echo "" >> "$INV"
if curl -s --max-time 5 http://localhost:1234/api/v0/models > /tmp/lms_models.json 2>/dev/null; then
    echo '```' >> "$INV"
    python3 -c "
import json
with open('/tmp/lms_models.json') as f:
    d = json.load(f)
for m in d.get('data', []):
    print(f'LM Studio → {m[\"id\"]}  ({m.get(\"size\",\"?\")} bytes)')
" >> "$INV" 2>/dev/null
    echo '```' >> "$INV"
    echo "✓"
    ((PASS++))
else
    echo "LM Studio no accesible (puerto 1234 no responde)" >> "$INV"
    echo "⚠ (LM Studio no responde)"
    ((PASS++))
fi
echo "" >> "$INV"

# --- Python packages (Hermes venv) ---
((TOTAL++))
echo -n "  [$TOTAL] Inventario Python (Hermes)... "
echo "## Paquetes Python (Hermes venv)" >> "$INV"
echo "" >> "$INV"
echo '```bash' >> "$INV"
~/.hermes/hermes-agent/venv/bin/pip freeze 2>/dev/null | head -30 >> "$INV"
echo '# ... (truncado a 30 líneas)' >> "$INV"
echo '```' >> "$INV"
echo "" >> "$INV"
echo "✓"
((PASS++))

# --- Git repos ---
((TOTAL++))
echo -n "  [$TOTAL] Inventario Git... "
echo "## Repositorios Git" >> "$INV"
echo "" >> "$INV"
echo '```' >> "$INV"
for repo in ~/hermes-lab ~/perfume-ia; do
    if [ -d "$repo/.git" ]; then
        REMOTE=$(cd "$repo" && git remote get-url origin 2>/dev/null || echo "sin remote")
        BRANCH=$(cd "$repo" && git branch --show-current 2>/dev/null || echo "?")
        echo "$repo  → $REMOTE  ($BRANCH)" >> "$INV"
    fi
done
echo '```' >> "$INV"
echo "" >> "$INV"
echo "✓"
((PASS++))

# --- Apt packages ---
((TOTAL++))
echo -n "  [$TOTAL] Inventario paquetes sistema... "
echo "## Paquetes del sistema (apt)" >> "$INV"
echo "" >> "$INV"
echo '```bash' >> "$INV"
apt list --installed 2>/dev/null | grep -v "snap\|loop\|automatic" | head -50 >> "$INV"
echo '# ... (truncado a 50 líneas)' >> "$INV"
echo '```' >> "$INV"
echo "" >> "$INV"
echo "✓"
((PASS++))

# --- Rutas y estructura ---
((TOTAL++))
echo -n "  [$TOTAL] Inventario rutas... "
echo "## Estructura de directorios clave" >> "$INV"
echo "" >> "$INV"
echo '```' >> "$INV"
echo "~/.hermes/            → Configuración, skills, memoria de Hermes" >> "$INV"
echo "~/hermes-lab/          → Documentación, scripts, decision-engine" >> "$INV"
echo "~/perfume-ia/          → Perfume IA (gabinete, DB, research)" >> "$INV"
echo "~/joko-lab/            → Inbox, instruments" >> "$INV"
echo "~/automation-stack/    → Docker Compose (n8n, ollama, stirling, pdf-cleaner)" >> "$INV"
echo "~/lmstudio_real_monitor/ → Monitor Flask de LM Studio" >> "$INV"
echo "/mnt/ssd_ia_datos/     → SSD datos: n8n, ollama, exports, backups, lab-state" >> "$INV"
echo '```' >> "$INV"
echo "" >> "$INV"
echo "✓"
((PASS++))

# --- Instrucciones de restauración ---
cat >> "$INV" << 'RESTORE'

## Instrucciones de restauración rápida

### 1. Restaurar configs del sistema
```bash
cp rescue/YYYY-MM-DD_HH-MM/system-config/.bashrc ~/
cp rescue/YYYY-MM-DD_HH-MM/system-config/.profile ~/
crontab rescue/YYYY-MM-DD_HH-MM/system-config/crontab.txt
cp rescue/YYYY-MM-DD_HH-MM/system-config/*.service ~/.config/systemd/user/
cp rescue/YYYY-MM-DD_HH-MM/ssh/id_* ~/.ssh/
source ~/.bashrc
```

### 2. Restaurar Hermes
```bash
unzip rescue/YYYY-MM-DD_HH-MM/hermes-backup.zip -d ~/.hermes/
```

### 3. Restaurar n8n + exports
```bash
tar -xzf rescue/YYYY-MM-DD_HH-MM/n8n-backup.tar.gz -C /mnt/ssd_ia_datos/
tar -xzf rescue/YYYY-MM-DD_HH-MM/exports-backup.tar.gz -C /mnt/ssd_ia_datos/
```

### 4. Descargar modelos (desde el inventario)
```bash
# Ollama — ejecutar las líneas 'ollama pull' del inventario
# Docker — ejecutar las líneas 'docker pull' del inventario
# LM Studio — descargar desde la interfaz gráfica
```

### 5. Restaurar git repos
```bash
git clone rescue/YYYY-MM-DD_HH-MM/hermes-lab.bundle ~/hermes-lab
git clone rescue/YYYY-MM-DD_HH-MM/perfume-ia.bundle ~/perfume-ia
```

### 6. Levantar servicios
```bash
cd ~/automation-stack
docker compose up -d
systemctl --user enable --now hermes-gateway.service
```
RESTORE

# ═══════════════════════════════════════════════════════
# RESUMEN
# ═══════════════════════════════════════════════════════

TOTAL_SIZE=$(du -sh "$DIR" 2>/dev/null | cut -f1)
USB_FREE=$(df -h "$DEST" 2>/dev/null | awk 'NR==2 {print $4}')

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  RESCATE COMPLETADO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Destino:  $DIR"
echo "  Tamaño:   $TOTAL_SIZE"
echo "  Pasos:    $PASS/$TOTAL OK"
echo "  USB libre: $USB_FREE"
echo ""
echo "  Irremplazable:  copiado (comprimido)"
echo "  Reemplazable:   inventario en inventario.md"
echo ""

# Limpiar rotación: mantener 2 copias
COPIAS=$(find "$DEST" -maxdepth 1 -type d -name "20*" | sort -r)
COPIAS_A_BORRAR=$(echo "$COPIAS" | tail -n +3)
if [ -n "$COPIAS_A_BORRAR" ]; then
    echo "$COPIAS_A_BORRAR" | xargs rm -rf 2>/dev/null
    echo "  Rotación: $(echo "$COPIAS_A_BORRAR" | wc -l) copia(s) antigua(s) eliminada(s)"
else
    echo "  Rotación: nada que borrar ($(echo "$COPIAS" | wc -l) copia(s) en disco)"
fi

# Notificar al escritorio
notify-send -u normal "Joko Lab — Rescue" "Backup completado: $FECHA\n$TOTAL_SIZE en USB. Puedes apagar el disco." 2>/dev/null || true
