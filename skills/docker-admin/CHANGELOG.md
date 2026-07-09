# docker-admin — Changelog

## 2026-07-06 (v0.4.0)

- **Etapa:** 3 → 4 (Optimizar)
- **Archivos nuevos:** `scripts/install-cron.sh`, `scripts/auditar-stack.sh`, `logs/`
- **Scripts modificados:** `healthcheck.sh` (modo `--cron` con notificación `notify-send`)
- **Cron del sistema instalado**
  - Healthcheck cada hora (minuto 5)
  - Backup n8n diario a las 3:00
  - Backup ollama diario a las 3:30
- **Integración con hermes-expert:** `auditar-stack.sh` ejecuta `hermes-diag.sh`
- **Archivos actualizados:** SKILL.md, ROADMAP.md, DIARY.md, COMMANDS.md (pendiente)

## 2026-07-06 (v0.3.0)

- **Etapa:** 2 → 3 (Actuar)
- **Archivos nuevos:** `scripts/healthcheck.sh`, `scripts/backup-volumen.sh`, `scripts/restore-volumen.sh`, `scripts/UPDATE_PROCEDURE.md`
- **Scripts probados:** healthcheck (4/4 OK), backup n8n (419 MB)
- **Archivos actualizados:** SKILL.md, ROADMAP.md, DIARY.md

## 2026-07-06 (v0.2.0)

- **Etapa:** 1 → 2 (Diagnosticar)
- **Archivos nuevos:** DIARY.md, AUDIT.md
- **Archivos actualizados:** SKILL.md, KNOWLEDGE.md, COMMANDS.md, ROADMAP.md, CHANGELOG.md
- **Datos reales del stack registrados:** puertos, volúmenes, redes, variables de entorno, GPU, build local

## 2026-07-06 (v0.1.0)

- **Etapa:** 0 → 1 (Comprender)
- **Archivos base creados:** SKILL.md, README.md, COMMANDS.md, SAFETY.md, KNOWLEDGE.md, ROADMAP.md, CHANGELOG.md
- Estructura inicial de la skill
