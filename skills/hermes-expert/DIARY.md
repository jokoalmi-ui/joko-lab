# hermes-expert — Diario de descubrimientos

> Registro cronológico de cada verificación sobre Hermes.
>
> **Regla:** El conocimiento nuevo se registra primero aquí. Una vez verificado y considerado estable, se integra en el documento temático correspondiente (KNOWLEDGE.md, LIMITATIONS.md, PATTERNS.md, etc.) y se deja una referencia en esta entrada. Si ya no aporta valor, se elimina la entrada de DIARY.md.

## 2026-07-05 (sesión 1)

### Verificado

- **Estructura de ~/.hermes/:** 20 subdirectorios. No existe profiles/. Skills: 18 directorios, 4 con SKILL.md. memorias: MEMORY.md + USER.md. cron/ y hooks/ vacíos.
- **Configuración:** deepseek-v4-flash, context 65536, 14 personalidades, Ollama como custom_provider. Config v30. 686 líneas.
- **state.db:** SQLite 12 MB. auto_prune: false. retention: 90 días.
- **Skills de hermes-lab:** No están en ~/.hermes/skills/. Son independientes.

### Descartado

- **Existencia de perfiles:** La documentación oficial menciona profiles/ pero no existe en esta instalación.
- **Carga automática de skills de hermes-lab:** Las skills documentadas en hermes-lab/ no son cargadas por Hermes automáticamente.

### Aprendido

- Las skills con SKILL.md propio son: computer-use, diagnostico-stack-local, dogfood, yuanbao
- Los plugins conocidos son: spotify (CLI)
- x_search usa grok-4.20-reasoning como modelo de búsqueda

### Pendiente para próxima sesión

- Leer secciones completas de config.yaml (providers, fallback_providers, streaming, onboarding, updates, computer_use)
- Verificar carga de skills con DESCRIPTION.md vs SKILL.md
- Comprobar límite de skills activas simultáneas
- Ver variables de entorno en .env
- Explorar contenido de state.db

---

## 2026-07-05 (sesión 2)

### Hecho
- **Reestructuración completa de la skill:** 7 → 12 archivos. Nuevos: STRUCTURE.md, CONFIG.md, LIMITATIONS.md, DIARY.md, AUDIT.md, PATTERNS.md.
- **Etapa:** 1 → 2 (Diagnosticar).
- **Regla documentada:** El conocimiento nuevo va primero a DIARY.md; una vez estable, se integra en el documento temático.

### Verificado (integrado en documentos destino)
- Estructura de ~/.hermes/ → STRUCTURE.md
- Config detallada (model, agent, toolsets, custom_providers) → CONFIG.md
- Límites conocidos (no profiles, skills aisladas, cron/hooks vacíos) → LIMITATIONS.md
- Patrones de experiencia (skill no encontrada, demasiadas preguntas, docs contradictorias, contenedor Up sin respuesta) → PATTERNS.md

### Creado
- **PATTERNS.md:** 4 patrones iniciales basados en experiencia real de la sesión.

### Pendiente para próxima sesión (los mismos, todavía sin verificar)
- Leer secciones completas de config.yaml (providers, fallback_providers, streaming, onboarding, updates, computer_use)
- Verificar carga de skills con DESCRIPTION.md vs SKILL.md
- Comprobar límite de skills activas simultáneas
- Ver variables de entorno en .env
- Explorar contenido de state.db

---

## 2026-07-06 (sesión 3)

### Hecho (etapa 2 — Diagnosticar completada)

- **Secciones config verificadas:** providers ({}), fallback_providers ([]), streaming (disabled), onboarding (seen+profile+skill_arrays+truncation), updates (check_interval: 1h, auto_update: false), computer_use (disabled), secrets (bitwarden desactivado).
- **Logs:** agent.log (7945 líneas), errors.log (770, solo WARNINGs de Nous/OpenRouter no autenticados), update.log (147 líneas), curator/ (1 ejecución vacía).
- **Skills con DESCRIPTION.md:** 13 de 18 skills.
- **hermes doctor:** Todos los checks pasados. 1 issue: API keys para herramientas opcionales no configuradas.
- **state.db esquema:** 2 tablas: sessions (28 columnas), messages (18 columnas + FTS trigramas).
- **.env:** 14 variables activas. DEEPSEEK_API_KEY presente.
- **hermes --help:** 79 subcomandos.
- **Herramientas auxiliares:** 14 clientes (vector, webresearch, shellcode, deploy, docker, google, deepmem, etc.) sin autenticar.

### Hecho (etapa 3 — Actuar completada)

- **INTEGRATION.md:** Procedimiento para copiar skills de hermes-lab a ~/.hermes/skills/.
- **hermes-diag.sh:** Script ejecutable de diagnóstico rápido (config, state.db, logs, .env, skills, permisos, espacio).
- **SAFE_LIMITS.md:** Guía de secciones seguras/peligrosas de config.yaml con procedimiento de backup.

### Hecho (etapa 4 — Optimizar completada)

- **Cron de auditoría:** `auditoria-hermes` (cada 24h, script hermes-diag.sh en ~/.hermes/scripts/).
- **Detector de cambios config.yaml:** `scripts/detect-config-changes.sh` (hash md5, snapshot automático, alerta en cambios).
- **Instalador de crons del sistema:** `scripts/install-system-crons.sh` (alternativa sin gateway).

### Integrado en documentos destino

- Secciones config → CONFIG.md (actualizado)
- Logs + DESCRIPTION.md → KNOWLEDGE.md (actualizado)
- state.db + .env + hermes --help → CONFIG.md (actualizado)
- Límites auxiliary clients + curator → LIMITATIONS.md (actualizado)
- Auditoría completa → AUDIT.md (actualizado)
- Roadmap actualizado a etapa 4

### Documentos creados

- INTEGRATION.md — procedimiento de integración
- hermes-diag.sh — script de diagnóstico
- SAFE_LIMITS.md — límites seguros de configuración
- scripts/detect-config-changes.sh — detector de cambios
- scripts/install-system-crons.sh — instalador de crons
