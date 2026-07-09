# hermes-expert — Roadmap

## Etapa actual: 4 — Optimizar

### Completado de etapa 1 (Comprender)

- [x] **Estructura de ~/.hermes/** — 20 subdirectorios mapeados (2026-07-05)
- [x] **Skills** — 18 instaladas, 4 con SKILL.md (2026-07-05)
- [x] **Configuración** — deepseek-v4-flash, context 65536, 14 personalidades, Ollama como custom_provider (2026-07-05)
- [x] **Memoria** — MEMORY.md + USER.md verificados (2026-07-05)
- [x] **No existe profiles/** — documentación oficial incorrecta (2026-07-05)
- [x] **cron/ y hooks/ vacíos** — sin tareas programadas (2026-07-05)

### Completado de etapa 2 (Diagnosticar)

Prioridad alta:
- [x] **Leer secciones de config.yaml** — todas verificadas (2026-07-06)
- [x] **Verificar carga de skills** — 13 con DESCRIPTION.md, 4 con SKILL.md (2026-07-06)
- [x] **Explorar logs de Hermes** — agent.log (7708), errors.log (749), update.log (147), curator (1 ejec) (2026-07-06)
- [x] **hermes doctor ejecutado** — 1 issue (API keys faltantes) (2026-07-06)

Prioridad media:
- [x] **Ver variables de entorno en .env** — 12 activas (2026-07-06)
- [x] **Explorar esquema de state.db** — 2 tablas: sessions, messages (2026-07-06)
- [x] **Probar hermes --help** — 79 subcomandos (2026-07-06)

### Completado de etapa 3 (Actuar)

- [x] **Procedimiento de integración de skills** — INTEGRATION.md creado (2026-07-06)
- [x] **Script de diagnóstico rápido** — hermes-diag.sh funcional (2026-07-06)
- [x] **Límites seguros para config.yaml** — SAFE_LIMITS.md creado (2026-07-06)

### Completado de etapa 4 (Optimizar)

- [x] **Automatizar auditoría periódica de Hermes** — cron de Hermes creado (`auditoria-hermes`, cada 24h, ~/.hermes/scripts/hermes-diag.sh) + script instalador de crons del sistema (`scripts/install-system-crons.sh`) (2026-07-06)
- [x] **Detectar cambios en config.yaml** — `scripts/detect-config-changes.sh` funcional (hash md5, snapshot automático, alerta en cambios) (2026-07-06)
