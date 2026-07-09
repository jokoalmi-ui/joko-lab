# docker-admin — Roadmap

## Etapa actual: 4 — Optimizar

### Completado de etapa 1 (Comprender)

- [x] Skill creada con 7 archivos base (SKILL, README, KNOWLEDGE, COMMANDS, SAFETY, ROADMAP, CHANGELOG)
- [x] Propósito definido: gestionar y diagnosticar el stack Docker del laboratorio
- [x] README.md con explicación para humanos
- [x] SAFETY.md con riesgos y protecciones

### Completado de etapa 2 (Diagnosticar)

- [x] KNOWLEDGE.md actualizado con datos reales del stack: puertos, volúmenes, redes, variables de entorno, healthchecks
- [x] COMMANDS.md ampliado con 9 categorías de comandos: estado, logs, recursos, GPU, healthcheck, redes, mantenimiento, limpieza, backups
- [x] DIARY.md creado con registro de descubrimientos verificados
- [x] AUDIT.md creado con checklist de 20 ítems
- [x] Todos los servicios verificados con salida real del terminal
- [x] Puertos reales confirmados con curl
- [x] Variables de entorno extraídas del docker-compose.yml real
- [x] Red y volúmenes listados
- [x] GPU verificada con nvidia-smi
- [x] Build local de pdf-cleaner documentado
- [x] Versiones de imágenes registradas
- [x] Policy de reinicio documentada

### Completado de etapa 3 (Actuar)

- [x] Script de healthcheck unificado: `scripts/healthcheck.sh`
- [x] Procedimiento de actualización segura: `scripts/UPDATE_PROCEDURE.md`
- [x] Script de backup de volúmenes: `scripts/backup-volumen.sh`
- [x] Script de restauración de volúmenes: `scripts/restore-volumen.sh`
- [x] Los 3 scripts probados con salida real exitosa
- [x] Backup completo de n8n verificado (419 MB, con workflows, binarios, config, DB SQLite)

### Completado de etapa 4 (Optimizar)

- [x] **Backup automático diario** — cron del sistema: n8n a las 3:00, ollama a las 3:30
- [x] **Healthcheck periódico** — cron del sistema: cada hora (minuto 5)
- [x] **Notificación en fallo** — healthcheck usa `--cron` modo silencioso, notifica con `notify-send` si falla
- [x] **Logs de cron** — directorio `logs/` con rotación natural (healthcheck.log, backup-n8n.log, backup-ollama.log)
- [x] **Script instalador** — `scripts/install-cron.sh` (instala/actualiza los cron jobs)
- [x] **Auditoría integrada** — `scripts/auditar-stack.sh` (healthcheck Docker + hermes-diag.sh + disco + backups + GPU)
- [x] **Integración cruzada** — `hermes-expert/INTEGRATION.md` actualizado con estado de docker-admin

### Pendientes (ideas futuras)

- [ ] Notificación push (Telegram/email) cuando un servicio caiga
- [ ] Dashboard web con histórico de healthchecks
- [ ] Alertas por uso de disco en volúmenes Docker
- [ ] Purga automática de backups antiguos (>30 días)
