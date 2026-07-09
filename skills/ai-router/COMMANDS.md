# ai-router — Comandos

## Diagnóstico (solo lectura)

### Comprobar modelos en Ollama

```bash
curl -s http://localhost:11434/v1/models | python3 -m json.tool 2>/dev/null || curl -s http://localhost:11434/v1/models
```

### Comprobar modelos en LM Studio (si el API Server está activo)

```bash
curl -s http://localhost:1234/api/v0/models | python3 -m json.tool 2>/dev/null || curl -s http://localhost:1234/api/v0/models
```

### Verificar VRAM disponible

```bash
nvidia-smi --query-gpu=memory.free,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits
```

### Verificar RAM disponible

```bash
free -h | grep Mem
```

### Comprobar si un modelo específico existe en Ollama

```bash
curl -s http://localhost:11434/api/tags | python3 -c "import json,sys; data=json.load(sys.stdin); [print(m['name']) for m in data.get('models',[])]" 2>/dev/null
```

## Árbol de decisión rápido (para usar en terminal)

```bash
# 1. ¿Privacidad? pregunta primero al usuario
# 2. ¿VRAM suficiente?
VRAM_LIBRE=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits)
if [ "$VRAM_LIBRE" -lt 4096 ]; then
  echo "VRAM baja ($VRAM_LIBRE MB) → recomendar modelo ligero"
else
  echo "VRAM suficiente ($VRAM_LIBRE MB) → modelo completo disponible"
fi
```

## Enrutamiento manual

### Usar Ollama para una consulta

```bash
curl -s http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2","messages":[{"role":"user","content":"Tu consulta aquí"}],"stream":false}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['choices'][0]['message']['content'])"
```

### Usar DeepSeek (a través de Hermes)

DeepSeek se usa por defecto en Hermes. Para forzar un cambio temporal, se modifica el proveedor en la configuración de Hermes (requiere confirmación del usuario).

## Sin comandos de acción automáticos aún

Los comandos de acción requieren confirmación explícita del usuario antes de ejecutarse.

### Usar el script ai-router.py

```bash
# Ver estado completo del sistema
python3 ~/hermes-lab/skills/ai-router/ai-router.py --diagnostico

# Consulta simple (detecta automáticamente el proveedor)
python3 ~/hermes-lab/skills/ai-router/ai-router.py "Explica qué es Docker Compose"

# Visión local (usa LM Studio si tiene modelo VLM cargado)
python3 ~/hermes-lab/skills/ai-router/ai-router.py --vision ~/Descargas/foto.jpg "Describe esta imagen"

# Ayuda
python3 ~/hermes-lab/skills/ai-router/ai-router.py --help
```

Nota: El script usa las herramientas del sistema (curl, nvidia-smi, python3). Si falta alguna, fallará con un mensaje claro.

## Gestión de LM Studio

LM Studio no tiene API para cargar/descargar modelos desde terminal. La gestión se hace desde su interfaz gráfica. Estos comandos ayudan a saber qué está pasando sin abrir la GUI.

### Comprobar estado actual de modelos en LM Studio

```bash
# Ver todos los modelos instalados y su estado (cargado/no cargado)
curl -s http://localhost:1234/api/v0/models | python3 -c "
import json,sys
data = json.load(sys.stdin)
print('Modelos en LM Studio:')
print('─' * 50)
for m in data['data']:
    estado = '✅ CARGADO' if m['state'] != 'not-loaded' else '  No cargado'
    tipo = m.get('type','?')
    print(f'{estado:15s} | {tipo:12s} | {m[\"id\"]}')
"

# Versión compacta (solo nombres)
curl -s http://localhost:1234/api/v0/models | python3 -c "
import json,sys
data = json.load(sys.stdin)
for m in data['data']:
    if m['state'] != 'not-loaded':
        print(f'✅ {m[\"id\"]}')
"
```

### Saber cuánta VRAM usa LM Studio

```bash
nvidia-smi | grep -A1 "Processes" | tail -1
# Buscar específicamente LM Studio
nvidia-smi | grep -i "lm-studio"
```

### Cuándo descargar un modelo (liberar VRAM)

Ejecuta esto antes de cargar un modelo grande:

```bash
# Ver VRAM libre antes de cargar
echo "VRAM libre: $(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits) MB"

# Si ves que no hay suficiente (menos de ~6 GB para modelo 12B):
# 1. Abre LM Studio GUI
# 2. Busca el modelo cargado (tiene check verde)
# 3. Haz clic en "Unload" o el botón de descarga
# 4. Vuelve a verificar
nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits
```

### Liberar VRAM de Ollama (para dejar espacio a LM Studio)

```bash
# Ver qué modelo tiene cargado Ollama
curl -s http://localhost:11434/api/ps | python3 -m json.tool 2>/dev/null

# Descargarlo de VRAM (no lo borra del disco)
curl -s http://localhost:11434/api/generate -d '{"model":"<nombre-del-modelo>","keep_alive":0}'

# Verificar VRAM liberada
nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits
```

### Recomendación práctica

| Situación | Acción |
|---|---|
| VRAM libre > 8 GB | Cargar gemma-4-12b-qat (máximo detalle) |
| VRAM libre 4-8 GB | Cargar gemma-4-e4b (rápido, suficiente calidad) |
| VRAM libre < 4 GB | Descargar modelo actual de Ollama o LM Studio antes de cargar |
| Quieres usar Ollama y LM Studio alternativamente | Descargar uno antes de cargar el otro (no caben ambos a la vez)
