# n8n-admin

Skill para gestionar el servicio n8n de Joko Lab.

**Versión:** 0.3.0 | **Etapa:** 3 — Actuar (Completada)

## ¿Qué permite?

- Diagnosticar el estado del contenedor n8n (logs, recursos, conectividad)
- Ejecutar healthcheck específico con 5 tests (healthcheck-n8n.sh)
- Exportar workflows desde el contenedor (export-workflows.sh)
- Leer logs de n8n para detectar errores
- Aplicar cambios controlados al docker-compose.yml (backup previo)
- Verificar configuración del stack (env, volúmenes, límites de recursos)
- Comprobar el estado de los runners (JS Task Runner, Python Task Runner)
- Realizar backup manual desde docker-admin

## ¿Qué NO permite?

- No reiniciar n8n sin confirmación explícita
- No modificar credenciales, workflows ni datos persistentes
- No parar el servicio sin autorización
- No tocar volúmenes de datos
- No exponer el API de n8n sin autenticación

## Estado actual

| Indicador | Valor |
|-----------|-------|
| Versión | 2.27.4 |
| Contenedor | Up |
| Límites RAM | 2G máx / 512M reserva |
| Workflows activos | 1 (ENVIO WHATSAPP) |
| JS Task Runner | ✔ Registrado |
| Python Task Runner | ✗ No disponible |
| Conectividad Ollama | ✔ Confirmada |
| Healthcheck | 5/5 tests OK |

## Dependencias

- Docker y Docker Compose v2
- Stack en `/home/jokoalmi/automation-stack/docker-compose.yml`
- Volumen de datos en `/mnt/ssd_ia_datos/n8n`
- docker-admin skill para backups cronificados
- wget (disponible en contenedor n8n) para healthcheck interno

## Archivos de la skill

| Archivo | Propósito |
|---------|-----------|
| SKILL.md | Metadatos y versión |
| README.md | Esta página |
| KNOWLEDGE.md | Conocimiento técnico profundo |
| COMMANDS.md | Comandos y procedimientos |
| SAFETY.md | Riesgos y protecciones |
| ROADMAP.md | Progreso por etapas |
| CHANGELOG.md | Historial de cambios |
| DIARY.md | Descubrimientos y bitácora |
| healthcheck-n8n.sh | Healthcheck específico (ejecutable) |
| export-workflows.sh | Exportación de workflows (ejecutable) |

## Documentación relacionada

- `HERMES.md` — filosofía y normas del laboratorio
- `docs/arquitectura.md` — detalles técnicos del stack
- `docs/decisiones/` — registro de decisiones sobre n8n
- `skills/docker-admin/` — skill base para gestión Docker
