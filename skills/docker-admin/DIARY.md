# docker-admin — Diario de descubrimientos

> Registro cronológico de cada verificación sobre el stack Docker.
>
> **Regla:** El conocimiento nuevo se registra primero aquí. Una vez verificado y estable, puede migrarse a KNOWLEDGE.md.

## 2026-07-06

### Datos del stack (verificados con salida real)

| Servicio | Puerto | Código HTTP | Contenedor |
|----------|--------|-------------|------------|
| n8n | 5678 | 200 | n8n |
| Ollama | 11434 | 200 (api/tags) | ollama |
| PostgREST | 8000 | 404 (raíz, esperado) | postgrest |
| Blocky | 8081 | 200 | blocky |


- **Volúmenes (6):** postgrest-data, n8n_data, ollama_models, n8n_shared, blocky_config, blocky_log
- **Red:** automation-stack_default (bridge)
- **Variables clave:** OLLAMA_HOST=0.0.0.0, N8N_PORT=5678, N8N_PROTOCOL=http
- **GPU:** NVIDIA RTX A2000 12GB, driver 550.120, CUDA 12.4
- **Build local:** pdf-cleaner se construye desde Dockerfile.local
- **Policy de reinicio:** unless-stopped en todos los servicios

### Herramientas creadas

| Script | Propósito | Verificado |
|--------|-----------|------------|
| scripts/healthcheck.sh | Healthcheck unificado (modo interactivo y --cron) | ✔ |
| scripts/backup-volumen.sh | Backup de volúmenes Docker | ✔ (n8n: 419 MB) |
| scripts/restore-volumen.sh | Restauración con confirmación | ✔ (estructura) |
| scripts/auditar-stack.sh | Auditoría completa (Docker + Hermes + disco + backups + GPU) | ✔ |
| scripts/install-cron.sh | Instala cron jobs del sistema | ✔ |

### Cron jobs instalados

- **Healthcheck:** cada hora (minuto 5) → logs/healthcheck.log, notificación notify-send si falla
- **Backup n8n:** diario a las 3:00 → logs/backup-n8n.log
- **Backup ollama:** diario a las 3:30 → logs/backup-ollama.log

### Integración

- docker-admin → hermes-expert: `auditar-stack.sh` ejecuta `hermes-diag.sh` como parte de la auditoría
- hermes-expert/INTEGRATION.md actualizado con estado de docker-admin
