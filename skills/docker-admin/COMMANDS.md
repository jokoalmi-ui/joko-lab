# docker-admin — Comandos

> **Regla:** Todos los comandos de esta sección son de solo lectura salvo que se indique lo contrario.
> Los comandos que modifican el sistema están marcados con ⚠️ y requieren confirmación explícita.

---

## 1. Diagnóstico general

```bash
# Estado de todos los servicios
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml ps

# Estado detallado (incluye contenedores parados)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml ps -a

# Ver configuración completa del stack (resuelve variables, muestra la configuración real)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml config
```

## 2. Logs

```bash
# Logs de un servicio concreto (últimas 80 líneas)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs --tail=80 <servicio>

# Logs en tiempo real (seguir salida)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs -f <servicio>

# Logs con timestamps
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs -t --tail=80 <servicio>

# Logs de todos los servicios a la vez
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs --tail=40
```

## 3. Recursos y sistema

```bash
# Uso de CPU, RAM y procesos por contenedor
docker stats --no-stream

# Espacio en disco usado por Docker
docker system df

# Imágenes descargadas, tamaño y fecha
docker images

# Volúmenes Docker y su tamaño
docker volume ls

# Redes Docker
docker network ls
```

## 4. GPU NVIDIA

```bash
# Estado completo de la GPU
nvidia-smi

# Métricas clave limpias (nombre, VRAM usada/total, % GPU, temperatura)
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits

# Procesos que usan GPU
nvidia-smi pmon -c 1
```

## 5. Healthcheck manual

```bash
# Healthcheck unificado (interactivo)
bash ~/hermes-lab/skills/docker-admin/scripts/healthcheck.sh

# Healthcheck modo cron (silencioso, solo exit code + log)
bash ~/hermes-lab/skills/docker-admin/scripts/healthcheck.sh --cron
```

## 6. Auditoría completa

```bash
# Auditoría: Docker + Hermes + disco + backups + GPU
bash ~/hermes-lab/skills/docker-admin/scripts/auditar-stack.sh
```

## 7. Backups

```bash
# Backup de un servicio (ej: n8n, ollama)
bash ~/hermes-lab/skills/docker-admin/scripts/backup-volumen.sh n8n

# Restaurar un servicio desde backup
bash ~/hermes-lab/skills/docker-admin/scripts/restore-volumen.sh n8n 20260706_203839

# Los backups se guardan en: /mnt/ssd_ia_datos/backups/<servicio>-<fecha>/
```

## 8. Gestión de cron

```bash
# Instalar/actualizar cron jobs (healthcheck cada hora + backups diarios)
bash ~/hermes-lab/skills/docker-admin/scripts/install-cron.sh

# Ver cron jobs activos
crontab -l

# Logs de cron
cat ~/hermes-lab/skills/docker-admin/logs/healthcheck.log
cat ~/hermes-lab/skills/docker-admin/logs/backup-n8n.log
cat ~/hermes-lab/skills/docker-admin/logs/backup-ollama.log
```

## 9. Redes

```bash
# Listar contenedores en la red del stack
docker network inspect automation_net

# Puertos abiertos del sistema relacionados
ss -ltnp | grep -E '5678|11434|8000|8081'
```

## 10. Mantenimiento (⚠️ requieren confirmación)

```bash
# Levantar todos los servicios
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml up -d

# Levantar un servicio concreto
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml up -d <servicio>

# Parar un servicio concreto
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml stop <servicio>

# Reconstruir y levantar (para servicios con build local como pdf-cleaner)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml up -d --build <servicio>

# Descargar nuevas versiones de las imágenes
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml pull <servicio>
```

## 11. Limpieza de Docker (⚠️ alta peligrosidad)

Estos comandos pueden borrar datos no respaldados. Siempre pedir confirmación explícita.

```bash
# Limpiar todo lo no usado (contenedores, redes, imágenes, volúmenes huérfanos)
docker system prune -a --volumes

# Solo volúmenes no usados
docker volume prune

# Solo imágenes no usadas
docker image prune -a
```

## 12. Procedimiento de actualización segura

```bash
# Ver procedimiento completo
cat ~/hermes-lab/skills/docker-admin/scripts/UPDATE_PROCEDURE.md

# Flujo resumido: backup → pull → up → verificar
bash scripts/backup-volumen.sh <servicio>
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml pull <servicio>
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml up -d <servicio>
bash scripts/healthcheck.sh
```
