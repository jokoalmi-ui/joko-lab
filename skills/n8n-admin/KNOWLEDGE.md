# n8n-admin — Conocimiento

## Servicio

| Atributo | Valor |
|----------|-------|
| Contenedor | n8n |
| Imagen | docker.n8n.io/n8nio/n8n:latest |
| Versión | 2.27.4 (confirmado en logs, 2026-07-06) |
| Puerto | 5678 |
| Puerto interno Task Broker | 5679 |
| Red | automation_net |
| Imagen base | Node.js 24.16.0 (sin curl, sin Python 3) |
| Timeout de tareas | 900 segundos |
| Zona horaria | Europe/Madrid |

## Volúmenes y datos

| Montaje | Ruta host | Tamaño |
|---------|-----------|--------|
| Datos n8n | /mnt/ssd_ia_datos/n8n | 401 MB |
| Exports/archivos | /mnt/ssd_ia_datos/exports | 2.9 GB |
| Backups | /mnt/ssd_ia_datos/backups | 419 MB (1 backup) |

## Variables de entorno activas

```yaml
TZ: Europe/Madrid
GENERIC_TIMEZONE: Europe/Madrid
N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS: true
N8N_RUNNERS_ENABLED: true              # DEPRECATED — eliminar
N8N_RUNNERS_TASK_TIMEOUT: 900
N8N_RESTRICT_FILE_ACCESS_TO: /files;/backups
```

## Task Runners

| Runner | Estado | Notas |
|--------|--------|-------|
| JS Task Runner | ✔ Registrado | Funciona correctamente |
| Python Task Runner (interno) | ✗ No disponible | Falta Python 3 en la imagen oficial |

## Workflows

| Workflow | ID | Estado |
|----------|----|--------|
| ENVIO WHATSAPP | e871evjsXHxJ5bND | ✔ Activado |
| Drafts | 0 | — |
| Publicados | 0 | (sin contar ENVIO WHATSAPP) |

## Conectividad

| Servicio | Desde n8n | Notas |
|----------|-----------|-------|
| Ollama | http://ollama:11434/v1 | n8n no tiene `curl`, la conectividad se prueba desde el host |
| Gradients | — | No configurado actualmente |

## Problemas conocidos

1. **N8N_RUNNERS_ENABLED** está obsoleta en v2.27.4. El log dice eliminarla.
2. **Python Task Runner** no funciona internamente por falta de Python 3 en la imagen oficial.
3. **n8n no tiene curl** — cualquier test de conectividad hay que hacerlo desde el host.
4. **PostHog** muestra un deprecation menor (`sendFeatureFlags`).

## Rutas protegidas (no modificar sin confirmación)

- /mnt/ssd_ia_datos/n8n — datos persistentes de n8n
- /mnt/ssd_ia_datos/exports — archivos exportados/importados
- /mnt/ssd_ia_datos/backups — backups del stack
