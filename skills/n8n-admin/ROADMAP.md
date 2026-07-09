# n8n-admin — Roadmap

## Etapa 3: Actuar (Completada — 2026-07-06)

**Inicio:** 2026-07-06
**Finalización:** 2026-07-06

### Acciones ejecutadas

- [x] **Eliminar `N8N_RUNNERS_ENABLED`** del docker-compose.yml — deprecated desde v2.27.4 (✔ COMPLETADO, n8n recreado correctamente)
- [x] **Definir límites de recursos** — memoria 2G máx, 512M reserva (✔ COMPLETADO, n8n recreado, límite visible en docker stats)
- [x] **Crear healthcheck específico de n8n** — `healthcheck-n8n.sh` con 5 tests (✔ COMPLETADO, 5/5 OK)
- [x] **Crear script de exportación de workflows** — `export-workflows.sh` (✔ COMPLETADO, exporta a /mnt/ssd_ia_datos/exports/)
- [x] **Integrar backup n8n con docker-admin** — el cron diario a las 3:00 ya lo cubre (✔ COMPLETADO, documentado en COMMANDS.md)
- [x] **Documentar procedimiento de backup** en COMMANDS.md (✔ COMPLETADO)
- [x] **Actualizar toda la documentación de la skill** — COMMANDS.md reescrito, SKILL.md, README.md, ROADMAP.md, CHANGELOG.md actualizados (✔ COMPLETADO)

### No ejecutado (no necesario)

- Instalar curl en contenedor n8n — n8n tiene wget, suficiente. Para diagnósticos avanzados se usa el host.
- Configurar runner externo de Python — no hay workflows Python que lo requieran. Si aparece en el futuro, se aborda entonces.
- Exportación automática via API REST — n8n no tiene API key configurada. Se exporta manualmente desde la UI.

## Etapa 4: Optimizar (Parcialmente completada)

**Inicio:** 2026-07-06

### Completado (sube de etapa 3)

- [x] **Definir límites de recursos** — memoria 2G máx, 512M reserva
- [x] **Programar healthcheck específico de n8n** — `healthcheck-n8n.sh`
- [x] **Integrar backup de n8n con docker-admin** — ya integrado (cron 3:00)

### Pendiente

- [ ] **Separar runners en contenedores independientes** (external mode) — si los workflows JS requieren más aislamiento
- [ ] **Evaluar métricas de rendimiento de workflows largos** — monitorizar el workflow ENVIO WHATSAPP en ejecución real. Línea base en reposo: CPU 0.25%, RAM 305 MiB
- [ ] **Activar endpoint de métricas** — `N8N_METRICS=true` para exponer métricas Prometheus en `/metrics`
- [ ] **Configurar alarma de salud** — healthcheck-n8n.sh ya está en cron cada 30 min. Notifica por notify-send si falla. ✔
- [ ] **Documentar en docs/estado-real.md** — actualizado ✔
- [ ] **Auditar periódicamente** — incluir n8n en la auditoría global del laboratorio
