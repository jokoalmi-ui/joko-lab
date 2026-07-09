# n8n-admin — Comandos

> **Regla:** Todos los comandos de esta sección son de solo lectura. Los que modifican el sistema están marcados con ⚠️ y requieren confirmación explícita.

---

## 1. Estado del contenedor

```bash
# Estado básico
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml ps n8n

# Estado detallado (incluye contenedor parado)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml ps -a

# IP y red del contenedor
docker inspect n8n --format='{{range $net,$conf := .NetworkSettings.Networks}}{{$net}}: {{$conf.IPAddress}}{{"\n"}}{{end}}'

# Versión de n8n
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs --tail=5 n8n | grep "Version"
```

## 2. Logs

```bash
# Últimas 80 líneas
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs --tail=80 n8n

# Logs en tiempo real
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs -f n8n

# Logs con timestamps
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs -t --tail=80 n8n

# Logs filtrados por workflow activo
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs --tail=100 n8n | grep "Activated workflow"

# Logs filtrados por runners
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs --tail=80 n8n | grep -i "runner"
```

## 3. Healthcheck (2 métodos)

```bash
# Healthcheck rápido desde el host (endpoint /healthz)
curl -s http://localhost:5678/healthz
# → {"status":"ok"}

# Healthcheck completo específico de n8n (5 tests)
bash ~/hermes-lab/skills/n8n-admin/healthcheck-n8n.sh
# Tests: contenedor Up, /healthz OK, puerto 5678, sin errores, workflows activos
```

## 4. Variables de entorno activas

```bash
# Ver todas las variables del contenedor n8n
docker inspect n8n --format='{{range $v := .Config.Env}}{{println $v}}{{end}}' | grep -iE "n8n_"

# Variables actuales de n8n (2026-07-06):
#   N8N_RUNNERS_TASK_TIMEOUT=900
#   N8N_RESTRICT_FILE_ACCESS_TO=/files;/backups
#   N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true
#   N8N_RELEASE_TYPE=stable
```

## 5. Recursos del contenedor

```bash
# Uso de CPU y RAM en tiempo real
docker stats n8n --no-stream

# Uso de disco del volumen n8n
du -sh /mnt/ssd_ia_datos/n8n/

# Tamaño de exports
du -sh /mnt/ssd_ia_datos/exports/

# Tamaño de backups
du -sh /mnt/ssd_ia_datos/backups/

# Límites configurados: memoria 2G máx, 512M reserva
docker inspect n8n --format='{{.HostConfig.Memory}} {{.HostConfig.MemoryReservation}}'
```

## 6. Conectividad con Ollama

> **Nota:** n8n tiene `wget` pero no `curl`. Desde dentro del contenedor se usa `wget`.

```bash
# Verificar modelos de Ollama (desde el host)
curl -s http://localhost:11434/api/tags | python3 -m json.tool 2>/dev/null || curl -s http://localhost:11434/api/tags

# Probar conectividad n8n → Ollama por nombre de contenedor (desde dentro de n8n)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml exec n8n wget -q -O - http://ollama:11434/api/tags

# Modelos disponibles (2026-07-06):
#   qwen2.5:7b (4.7 GB)
#   llama31-8b-64k (4.9 GB)
#   llama3.1:8b (4.9 GB)
```

## 7. Backups

El backup de n8n ya está integrado con docker-admin. Hay un cron diario a las 3:00.

```bash
# Ver backups existentes
ls -lt /mnt/ssd_ia_datos/backups/ | head -10

# Backup manual de n8n (rsync, preserva estructura)
bash ~/hermes-lab/skills/docker-admin/scripts/backup-volumen.sh n8n

# Backup manual de exports
bash ~/hermes-lab/skills/docker-admin/scripts/backup-volumen.sh exports

# Backup manual de todo el volumen n8n (tarball comprimido alternativo)
tar czf /mnt/ssd_ia_datos/backups/n8n-full-$(date +%Y%m%d_%H%M%S).tar.gz -C /mnt/ssd_ia_datos n8n/

# Ver log del último backup automático
tail -20 ~/hermes-lab/skills/docker-admin/logs/backup-n8n.log
```

## 8. Exportación de workflows (⚠️ requiere confirmación)

```bash
# Exportar todos los workflows via script
bash ~/hermes-lab/skills/n8n-admin/export-workflows.sh
# Exporta a /mnt/ssd_ia_datos/exports/workflows-export-<fecha>/

# Exportar manualmente desde la UI
# Ir a http://localhost:5678 → cada workflow → "Download"
```

## 9. Red y conectividad

```bash
# Ver todos los contenedores en la red automation_net
docker network inspect automation_net --format='{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'

# n8n está en 172.18.0.4
# Puede alcanzar: ollama (172.18.0.5), stirling-pdf (172.18.0.3), pdf-cleaner (172.18.0.2)
```

## 10. Acciones sobre n8n (⚠️ requieren confirmación explícita)

```bash
# Recrear n8n (aplica cambios de docker-compose.yml)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml up -d n8n

# Reiniciar n8n (sin recrear)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml restart n8n

# Parar n8n
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml stop n8n

# Levantar n8n (si está parado)
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml up -d n8n

# Actualizar n8n (nueva versión de la imagen)
# 1. Hacer backup primero
# 2. Pull de nueva imagen
# 3. Recrear contenedor
bash ~/hermes-lab/skills/docker-admin/scripts/backup-volumen.sh n8n
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml pull n8n
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml up -d n8n
```

## 11. Problemas conocidos

| Problema | Estado | Impacto |
|----------|--------|---------|
| Python Task Runner no disponible | Permanente (falta Python 3) | Bajo — JS Runner funciona |
| sendFeatureFlags deprecated | Aviso PostHog | Ninguno — solo informativo |
| Sin autenticación API | No configurada | Exportación automática no disponible |
