# hermes-expert — Auditoría de Hermes

> Lista de verificación sistemática de todo lo que hay que conocer de Hermes.
> ✔ = verificado | ✖ = no existe | ? = pendiente

## Estructura del sistema

- [✔] Árbol completo de ~/.hermes/ — 2026-07-05
- [✔] No existe ~/.hermes/profiles/ — 2026-07-05
- [✔] cron/ y hooks/ vacíos — 2026-07-05
- [✔] state.db: SQLite 12 MB — 2026-07-05
- [✔] Logs identificados: agent.log (7945), errors.log (770), update.log (147), curator (1 ejec) — 2026-07-06
- [✔] state.db esquema: 2 tablas (sessions 28 col, messages 18 col) + FTS trigramas — 2026-07-06
- [?] Contenido de cache/

## Skills

- [✔] Skills instaladas: 18 directorios — 2026-07-05
- [✔] Skills con SKILL.md: 4 (computer-use, diagnostico-stack-local, dogfood, yuanbao) — 2026-07-05
- [✔] Carga de skills con DESCRIPTION.md vs SKILL.md — 2026-07-06 (13 con DESCRIPTION.md, 4 con SKILL.md)
|- [?] Número máximo de skills activas simultáneas
- [?] Cómo se añade una skill nueva (copy vs link vs install)
- [?] Skills de hermes-lab: cómo integrarlas

## Configuración

- [✔] Modelo y proveedor — 2026-07-05
- [✔] Agente (max_turns, timeout, etc.) — 2026-07-05
- [✔] Terminal backend — 2026-07-05
- [✔] Personalidades (14) — 2026-07-05
- [✔] Toolsets por plataforma — 2026-07-05
- [✔] Custom providers (Ollama) — 2026-07-05
- [✔] Plugins (spotify) — 2026-07-05
- [✔] LSP — 2026-07-05
- [✔] x_search — 2026-07-05
- [✔] Sección providers: {} (objeto vacío) — 2026-07-06
- [✔] Sección fallback_providers: [] (vacío) — 2026-07-06
- [✔] Sección streaming: disabled — 2026-07-06
- [✔] Sección onboarding: seen+profile_build — 2026-07-06
- [✔] Sección updates: pre_update_backup false — 2026-07-06
- [✔] Sección computer_use: cua_telemetry false — 2026-07-06
- [✔] Sección secrets: bitwarden desactivado — 2026-07-06
- [✔] Variables de entorno en .env: 12 activas (DEEPSEEK_API_KEY, TERMINAL_*, BROWSER_*, VISION/IMAGE/MOA/WEB_TOOLS_DEBUG) — 2026-07-06

## Memoria

- [✔] MEMORY.md y USER.md existen — 2026-07-05
- [?] Tamaño máximo de MEMORY.md (límite de 2200 chars conocido)
- [?] Formato interno y reglas de inyección

## Sesiones

- [✔] auto_prune: false — 2026-07-05
- [✔] retention: 90 días — 2026-07-05
- [?] Formato de state.db (tablas, esquema)
- [?] Cómo se almacenan y recuperan las sesiones
- [?] Límite de sesiones antes de impacto en rendimiento

## Gateway

- [✔] gateway_timeout: 1800s — 2026-07-05
- [?] Comportamiento con tareas que exceden el timeout
- [?] gateway_auto_continue_freshness: 3600s (ver si aplica)

## SOUL.md

- [✔] Existe y contiene la personalidad activa — 2026-07-05
- [?] Cómo se combina con HERMES.md si existe
- [?] Prioridad entre SOUL.md, HERMES.md y USER.md

## Plugins

- [✔] spotify como plugin CLI conocido — 2026-07-05
- [?] Estado real del plugin (instalado, funcional)
- [?] Cómo se instalan nuevos plugins

## Comandos

- [✔] hermes doctor — mencionado en documentación
- [?] Lista completa de comandos CLI de Hermes
- [?] hermes config, hermes skill, hermes memory
