# n8n-admin — Diario de descubrimientos

## 2026-07-06 — Diagnóstico inicial (Etapa 2)

### Datos confirmados del servicio

- **Versión n8n:** 2.27.4
- **Imagen:** docker.n8n.io/n8nio/n8n:latest
- **Estado:** Up 4 horas en el momento del diagnóstico
- **Puerto:** 5678 (público), 5679 (Task Broker interno)
- **Red:** automation_net (compartida con ollama, stirling-pdf, pdf-cleaner)

### Variables de entorno

Se confirmaron 6 variables activas. Una de ellas está obsoleta:

- `N8N_RUNNERS_ENABLED=true` — el log de arranque indica que ya no es necesaria. La nueva versión lo detecta automáticamente.
- Las demás variables están vigentes.

### Task Runners

- **JS Task Runner:** se registra correctamente. En los 3 arranques vistos en los logs, el runner se registró con IDs diferentes (cada vez que se reinicia se genera un nuevo ID).
- **Python Task Runner (modo interno):** falla porque la imagen oficial de n8n no incluye Python 3. El mensaje de error recomienda usar modo externo.

### Workflows

- Solo hay 1 workflow activo: **ENVIO WHATSAPP** (ID: e871evjsXHxJ5bND).
- No hay drafts ni otros workflows publicados.

### Limitaciones del contenedor

- **Sin curl** — `docker exec n8n curl` devuelve "executable file not found". No se puede probar conectividad HTTP desde dentro del contenedor.
- **Sin Python 3** — el runner interno de Python no funciona.
- **Shell:** /bin/sh (no bash).

### Volúmenes

| Ruta | Tamaño | Contenido |
|------|--------|-----------|
| /mnt/ssd_ia_datos/n8n | 401 MB | Datos persistentes de n8n |
| /mnt/ssd_ia_datos/exports | 2.9 GB | Archivos importados/exportados |
| /mnt/ssd_ia_datos/backups | 419 MB | Backups (1 backup de n8n) |

### Observaciones

- El workflow ENVIO WHATSAPP se activa automáticamente al iniciar n8n.
- No hay errores activos en los logs más allá de los conocidos (Python runner, N8N_RUNNERS_ENABLED deprecated).
- La versión 2.27.4 es estable y no presenta problemas críticos.
- El stack lleva funcionando al menos 4 horas sin incidentes.

### Próximos pasos para etapa 2

- Verificar conectividad real entre n8n y Ollama (por nombre de contenedor)
- Revisar ejecuciones del workflow ENVIO WHATSAPP
- Verificar uso de recursos en reposo y bajo carga
- Comprobar configuración de credenciales

## 2026-07-06 — Sesión de actuación (Etapa 3 + inicio Etapa 4)

### Acciones ejecutadas

1. **Eliminar `N8N_RUNNERS_ENABLED=true`** del docker-compose.yml — variable deprecated, eliminada sin impacto.
2. **Añadir límites de memoria** — 2G máx, 512M reserva. n8n recreado. Límite visible en `docker stats`.
3. **Crear healthcheck-n8n.sh** — script con 5 tests: contenedor Up, healthz HTTP, puerto 5678, logs sin errores, workflows activos.
4. **Crear export-workflows.sh** — exporta workflows desde el host (requiere autenticación, funcionalidad limitada sin API key).
5. **Reescribir COMMANDS.md** — 11 secciones actualizadas con datos reales.
6. **Actualizar toda la skill** — SKILL.md, README.md, ROADMAP.md, CHANGELOG.md, DIARY.md.

### Métricas en reposo (post-cambios)

| Indicador | Valor |
|-----------|-------|
| CPU | 0.25% |
| RAM | 305 MiB / 2 GiB (14.9%) |
| RAM libre sobre límite | 85.1% |
| Disco n8n | 401 MB |
| Disco exports | 2.9 GB |
| Disco backups | 401 MB |
| Healthcheck | 5/5 OK |
| Workflows activos | 1 (ENVIO WHATSAPP) |

### Procesos dentro del contenedor

- `tini` → entrypoint (0.0% CPU)
- `node /usr/local/bin/n8n` → proceso principal (~10.8% CPU en reposo)
- `node @n8n/task-runner` → JS Task Runner (~1.7% CPU en reposo)

### Impacto de los cambios

- Límite de memoria: protege al sistema si un workflow se descontrola
- Healthcheck: permite monitorizar n8n automáticamente
- Documentación: toda la skill está al día, no hay tareas pendientes de etapa 3
- n8n ha sido recreado 2 veces en esta sesión sin impacto en el workflow activo

### Lecciones aprendidas

- n8n se puede recrear sin perder estado (el workflow se reactiva solo)
- `docker compose config` no muestra la sección `deploy.resources` — es normal en Docker Compose standalone
- El healthcheck debe ignorar el error del Python runner (es conocido y no afecta)
- wget dentro del contenedor funciona para healthchecks HTTP básicos

