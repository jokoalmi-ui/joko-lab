# docker-admin — Auditoría

> Checklist de verificación del stack Docker.
> Cada ítem debe verificarse con salida real del terminal.

## Servicios

- [✔] **4 servicios definidos** en docker-compose.yml — verificado 2026-07-06
- [✔] **4 servicios activos** (`docker compose ps` → todos `Up`) — verificado 2026-07-06
- [✔] **stirling-pdf con healthcheck** (aparece como `healthy`) — verificado 2026-07-06
- [✔] **pdf-cleaner build local** desde `./pdf-cleaner/` — verificado 2026-07-06

## Puertos

- [✔] **n8n:5678** → 200 OK — verificado 2026-07-06
- [✔] **ollama:11434** → 200 OK — verificado 2026-07-06
- [✔] **stirling-pdf:8081** → 200 OK — verificado 2026-07-06
- [✔] **pdf-cleaner:8000** → 404 en raíz (sin ruta /) — verificado 2026-07-06

## Red

- [✔] **Red única:** `automation_net` — verificado 2026-07-06

## GPU

- [✔] **Solo ollama usa GPU** (`gpus: all`) — verificado 2026-07-06

## Volúmenes

- [✔] **n8n:** 3 bind mounts (n8n, exports, backups) en `/mnt/ssd_ia_datos/` — verificado 2026-07-06
- [✔] **ollama:** 1 bind mount en `/mnt/ssd_ia_datos/ollama` — verificado 2026-07-06
- [✔] **stirling-pdf:** sin volúmenes persistentes — verificado 2026-07-06
- [✔] **pdf-cleaner:** sin volúmenes persistentes — verificado 2026-07-06

## Variables de entorno

- [✔] **Ollama:** 7 variables (OLLAMA_HOST, CONTEXT_LENGTH, NUM_PARALLEL, MAX_LOADED_MODELS, KEEP_ALIVE, FLASH_ATTENTION, KV_CACHE_TYPE) — verificado 2026-07-06
- [✔] **n8n:** 6 variables (TZ, GENERIC_TIMEZONE, N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS, N8N_RUNNERS_ENABLED, N8N_RUNNERS_TASK_TIMEOUT, N8N_RESTRICT_FILE_ACCESS_TO) — verificado 2026-07-06
- [✔] **stirling-pdf:** 1 variable (SECURITY_ENABLELOGIN=false) — verificado 2026-07-06

## Pendiente de verificar

- [ ] Consumo real de recursos por contenedor (`docker stats`)
- [ ] Espacio usado por imágenes y volúmenes
- [ ] Versiones de imágenes sin actualizar
