# n8n-admin — Changelog

## v0.3.0 — 2026-07-06

### Cambios

- **Etapa:** 2 → 3 (Diagnosticar → Actuar). Etapa 4 parcialmente completada.
- **docker-compose.yml:** Eliminada variable `N8N_RUNNERS_ENABLED` (deprecated) ✔
- **docker-compose.yml:** Añadidos límites de memoria 2G máx / 512M reserva ✔
- **healthcheck-n8n.sh:** Creado — healthcheck específico con 5 tests, 5/5 OK ✔
- **export-workflows.sh:** Creado — exportación de workflows desde el host ✔
- **COMMANDS.md:** Reesrito completamente (11 secciones, datos actualizados, problemas conocidos)
- **SKILL.md:** v0.2.0 → v0.3.0, etapa 3 completada, datos actualizados
- **README.md:** Reesrito — tabla de estado, archivos de la skill, enlaces
- **ROADMAP.md:** Reesrito — acciones ejecutadas, pendientes de etapa 4
- **DIARY.md:** Actualizado con registro de cambios del día
- **Backup:** `docker-compose.yml.backup-20260706_235351` creado antes del primer cambio

### Logros

| Acción | Estado |
|--------|--------|
| Variable deprecated eliminada | ✔ Contenedor recreado, sin impacto |
| Límites de memoria configurados | ✔ 2G máx / 512M reserva |
| Healthcheck específico funcional | ✔ 5/5 tests OK |
| Script de exportación creado | ✔ Listo para usar |
| Integración docker-admin documentada | ✔ Backup ya cronificado |
| Documentación completa actualizada | ✔ 8 archivos al día |
