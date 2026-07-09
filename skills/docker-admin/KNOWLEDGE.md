# docker-admin — Conocimiento

## Stack del laboratorio

El stack principal está en `/home/jokoalmi/automation-stack/docker-compose.yml`.

### Servicios

| Servicio | Puerto host | Puerto contenedor | Contenedor | GPU | Build local | Estado |
|---|---|---|---|---|---|---|
| n8n | 5678 | 5678 | n8n | No | No | Up |
| ollama | 11434 | 11434 | ollama | Sí (all) | No | Up |
| stirling-pdf | 8081 | 8080 | stirling-pdf | No | No | Up (healthy) |
| pdf-cleaner | 8000 | 8000 | pdf-cleaner | No | Sí (./pdf-cleaner) | Up |

### Healthcheck real (2026-07-06)

| Servicio | Endpoint | Código HTTP |
|---|---|---|
| n8n | http://localhost:5678/ | 200 |
| ollama | http://localhost:11434/api/tags | 200 |
| pdf-cleaner | http://localhost:8000/ | 404 (endpoint raíz no definido) |
| stirling-pdf | http://localhost:8081/ | 200 |

### Red

Todos los servicios comparten la red `automation_net` (definida como `automation_net` con nombre explícito).

### Datos persistentes

| Servicio | Ruta host | Montaje en contenedor |
|---|---|---|
| n8n | /mnt/ssd_ia_datos/n8n | /home/node/.n8n |
| n8n (exports) | /mnt/ssd_ia_datos/exports | /files |
| n8n (backups) | /mnt/ssd_ia_datos/backups | /backups |
| ollama | /mnt/ssd_ia_datos/ollama | /root/.ollama |

Las rutas de n8n son **zona protegida**: /mnt/ssd_ia_datos/n8n, /mnt/ssd_ia_datos/exports, /mnt/ssd_ia_datos/backups.

### Variables de entorno relevantes

**n8n:**
- `TZ=Europe/Madrid`, `GENERIC_TIMEZONE=Europe/Madrid`
- `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true`
- `N8N_RUNNERS_ENABLED=true`, `N8N_RUNNERS_TASK_TIMEOUT=900`
- `N8N_RESTRICT_FILE_ACCESS_TO=/files;/backups`

**Ollama:**
- `OLLAMA_HOST=0.0.0.0:11434`
- `OLLAMA_CONTEXT_LENGTH=65536`
- `OLLAMA_NUM_PARALLEL=1`
- `OLLAMA_MAX_LOADED_MODELS=1`
- `OLLAMA_KEEP_ALIVE=10m`
- `OLLAMA_FLASH_ATTENTION=1`
- `OLLAMA_KV_CACHE_TYPE=q8_0`

**Stirling-PDF:**
- `SECURITY_ENABLELOGIN=false`

### Políticas de reinicio

Todos los servicios tienen `restart: unless-stopped`.

### Imágenes

| Servicio | Imagen |
|---|---|
| n8n | docker.n8n.io/n8nio/n8n:latest |
| ollama | ollama/ollama:latest |
| stirling-pdf | frooodle/s-pdf:latest |
| pdf-cleaner | pdf-cleaner:latest (build local) |

### Hardware disponible

- CPU: Intel Core i5-9500
- RAM: 32 GB
- GPU: NVIDIA RTX A2000 12 GB VRAM

### Protecciones especiales

- **n8n es zona protegida.** No reiniciar, parar, recrear ni modificar sin confirmación explícita.
- **ollama** usa GPU (device: all). Verificar con `nvidia-smi` antes de asumir disponibilidad.
- **pdf-cleaner** se construye desde `./pdf-cleaner/` (build local). Requiere `docker compose up -d --build pdf-cleaner` si cambia el código.
- **stirling-pdf** tiene healthcheck interno (aparece como `healthy` en `docker ps`).
