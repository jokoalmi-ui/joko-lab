# Decisión Técnica: Migración de backups de cron a systemd timer persistent

**Fecha**: 2026-07-10
**Estado**: Aceptada
**Área**: Operación / Automatización

## Contexto

Los backups de volúmenes (n8n, ollama, exports) se ejecutaban mediante cron jobs en el crontab personal del usuario, programados a las 3:00 y 3:30 AM. El sistema se reinició el 2026-07-10 a las 10:05, saltándose los backups programados.

## Problema

Cron ejecuta jobs a horas fijas. Si el sistema está apagado en ese momento, el job simplemente no corre. anacron solo gestiona jobs en `/etc/anacrontab`, no los del crontab personal.

## Alternativas consideradas

1. **Mover jobs a /etc/anacrontab** — Requiere separar en daily (n8n, ollama, exports) y configurar delays. Posible pero anacron no soporta `RandomizedDelaySec` ni integración fina con systemd.

2. **Script wrapper en cron cada hora** — Un script que compruebe "¿corrió hoy el backup?" y lo ejecute si no. Más complejo y propenso a errores de lógica.

3. **Systemd timer con Persistent=true** — Elegida. Si el timer se pierde (sistema apagado), se dispara inmediatamente al arrancar.

## Decisión

1. Crear `joko-backup.service` (oneshot): ejecuta backup de n8n, ollama y exports en serie, más git-backup.sh como PostExec.
2. Crear `joko-backup.timer` con `OnCalendar=daily`, `Persistent=true`, `RandomizedDelaySec=1800`.
3. Eliminar los cron jobs `backup-volumen.sh n8n` y `backup-volumen.sh ollama` del crontab personal.
4. Mantener en crontab: healthchecks, git-backup.sh (subida GDrive) y router horario.

## Motivos

- `Persistent=true` garantiza catch-up tras reinicio sin intervención manual.
- `RandomizedDelaySec=1800` evita picos de carga si múltiples servicios se disparan al arrancar.
- Separar concerns: systemd para operaciones del sistema, cron para tareas ligeras y horarias.
- Git-backup.sh (subida a GDrive) se mantiene en cron por ser independiente y no requerir catch-up.

## Consecuencias

- Los backups correrán ~30 min después del arranque si se perdieron durante el apagado.
- Los logs se escriben en `docker-admin/logs/backup-{n8n,ollama,exports}.log` y `logs/git-backup.log`.
- Si el sistema está encendido a las 00:00, el timer dispara los backups entre las 00:00 y 00:30 (por el randomized delay).

## Referencias

- `scripts/auditor-completo.py` (sección BACKUPS)
- `skills/docker-admin/scripts/backup-volumen.sh`
- `skills/docker-admin/COMMANDS.md`
