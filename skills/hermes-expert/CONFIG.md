# hermes-expert — Configuración

> Verificado parcialmente: 2026-07-05
> Archivo: ~/.hermes/config.yaml (686 líneas, versión 30)

## Secciones conocidas

### model

| Opción | Valor | Notas |
|---|---|---|
| default | deepseek-v4-flash | Modelo principal |
| provider | deepseek | Proveedor activo |
| base_url | https://api.deepseek.com/v1 | API remota |
| ollama_num_ctx | 65536 | Contexto para Ollama |
| context_length | 65536 | Tokens máximos de contexto |
| max_tokens | 4096 | Tokens máximos por respuesta |

### agent

| Opción | Valor | Notas |
|---|---|---|
| max_turns | 150 | Turnos máximos por sesión |
| gateway_timeout | 1800 | Timeout de gateway en segundos (30 min) |
| api_max_retries | 3 | Reintentos de API |
| tool_use_enforcement | auto | Control de uso de herramientas |
| task_completion_guidance | true | Guía para completar tareas |
| parallel_tool_call_guidance | true | Llamadas paralelas |
| environment_probe | true | Sondear entorno al iniciar |
| coding_context | auto | Contexto de codificación |
| verify_on_stop | true | Verificar al detener |
| image_input_mode | auto | Modo de entrada de imágenes |
| reasoning_effort | none | Esfuerzo de razonamiento |

### terminal

| Opción | Valor | Notas |
|---|---|---|
| backend | local | Terminal local |
| timeout | 180 | Timeout en segundos |
| home_mode | auto | Directorio home |

### sessions

| Opción | Valor | Notas |
|---|---|---|
| auto_prune | false | No poda automática |
| retention_days | 90 | Retención de sesiones |
| vacuum_after_prune | true | Optimizar DB tras poda |
| write_json_snapshots | false | No guarda JSON de sesiones |

### Personalidades (14)

helpful, concise, technical, creative, teacher, kawaii, catgirl, pirate, shakespeare, surfer, noir, uwu, philosopher, hype

### toolsets

| Toolset | Descripción |
|---|---|
| hermes-cli | Toolset de línea de comandos |

### platform_toolsets

| Plataforma | Toolsets |
|---|---|
| cli | file, kanban, memory, session_search, terminal, todo, vision, web |
| telegram | hermes-telegram |
| discord | hermes-discord |
| whatsapp | hermes-whatsapp |
| slack | hermes-slack |
| signal | hermes-signal |
| homeassistant | hermes-homeassistant |
| teams | hermes-teams |
| yuanbao | hermes-yuanbao |

### custom_providers

```yaml
  - name: Ollama llama31-8b-64k
  base_url: http://localhost:11434/v1
  api_key: no-key
  model: llama31-8b-64k:latest
  models:
    llama31-8b-64k:latest:
      context_length: 65536
```

### known_plugin_toolsets

- **CLI:** spotify

### lsp

| Opción | Valor |
|---|---|
| enabled | true |
| install_strategy | auto |

### x_search

| Opción | Valor |
|---|---|
| model | grok-4.20-reasoning |
| timeout_seconds | 180 |
| retries | 2 |

### streaming

| Opción | Valor |
|---|---|
| enabled | false |
| transport | auto |
| edit_interval | 0.8 |
| buffer_threshold | 24 |
| cursor | ' ▉' |
| fresh_final_after_seconds | 0.0 |

### onboarding

| Opción | Valor |
|---|---|
| seen.tool_progress_prompt | true |
| seen.busy_input_prompt | true |
| profile_build | ask |

### updates

| Opción | Valor |
|---|---|
| pre_update_backup | false |
| backup_keep | 5 |
| non_interactive_local_changes | stash |

### computer_use

| Opción | Valor |
|---|---|
| cua_telemetry | false |

### secrets

| Opción | Valor |
|---|---|
| bitwarden.enabled | false |
| bitwarden.access_token_env | BWS_ACCESS_TOKEN |
| bitwarden.project_id | '' |
| bitwarden.cache_ttl_seconds | 300 |
| bitwarden.override_existing | true |
| bitwarden.auto_install | true |
| bitwarden.server_url | '' |

## Secciones NO verificadas aún

Todas las secciones de config.yaml están ahora verificadas (2026-07-06).

## state.db (esquema SQLite)

Base de datos de sesiones en `~/.hermes/state.db` (~12 MB).

### Tabla `sessions`

| Columna | Tipo | Descripción |
|---|---|---|
| id | TEXT PRIMARY KEY | Identificador único |
| source | TEXT | Plataforma de origen (terminal, web, etc.) |
| model | TEXT | Modelo usado en la sesión |
| model_config | TEXT | Configuración del modelo (JSON) |
| system_prompt | TEXT | Prompt del sistema |
| parent_session_id | TEXT | Sesión padre (para continuaciones) |
| started_at / ended_at | REAL | Timestamps inicio/fin |
| end_reason | TEXT | Motivo de finalización |
| title | TEXT | Título de la sesión |
| message_count | INTEGER | Contador de mensajes |
| tool_call_count | INTEGER | Llamadas a herramientas |
| input_tokens / output_tokens | INTEGER | Tokens |
| rewind_count | INTEGER | Veces que se rebobinó |
| archived | INTEGER | 0=activa, 1=archivada |
| ... | ... | +10 columnas de costes, billing, handoff |

### Tabla `messages`

| Columna | Tipo | Descripción |
|---|---|---|
| id | INTEGER PK | Auto-incremental |
| session_id | TEXT FK | Referencia a sessions |
| role | TEXT | user, assistant, tool, system |
| content | TEXT | Contenido del mensaje |
| tool_call_id | TEXT | ID de llamada a herramienta |
| tool_calls | TEXT | Datos de herramientas (JSON) |
| timestamp | REAL | Momento del mensaje |
| token_count | INTEGER | Tokens del mensaje |
| active | INTEGER | 1=activo, 0=eliminado |
| compacted | INTEGER | 0=completo, 1=resumido |
| ... | ... | +10 columnas (reasoning, platform, etc.) |

Índices: session_id, timestamp, FTS (búsqueda de texto completo con trigramas).

### Tablas auxiliares

- `schema_version` — versión del esquema
- `state_meta` — metadatos del estado
- `messages_fts*` — índices de búsqueda de texto completo
- `compression_locks` — bloqueos de compresión

## Variables de entorno activas (.env)

Archivo `~/.hermes/.env` — 12 variables realmente activas (resto son comentarios):

| Variable | Valor (parcial) | Propósito |
|---|---|---|
| TERMINAL_MODAL_IMAGE | nikolaik/python-nodejs | Imagen Docker para terminal |
| TERMINAL_TIMEOUT | 60 | Timeout por comando |
| TERMINAL_LIFETIME_SECONDS | 300 | Vida máxima del contenedor |
| BROWSERBASE_PROXIES | true | Proxies del navegador |
| BROWSERBASE_ADVANCED_STEALTH | false | Stealth avanzado |
| BROWSER_SESSION_TIMEOUT | 300 | Timeout sesión navegador |
| BROWSER_INACTIVITY_TIMEOUT | 120 | Timeout inactividad |
| WEB/VISION/MOA/IMAGE_TOOLS_DEBUG | false | Debug de herramientas |
| AGENT_BROWSER_EXECUTABLE_PATH | /usr/bin/google-chrome | Ruta del navegador |
| TERMINAL_ENV | local | Entorno local |
| DEEPSEEK_API_KEY | *** | API key de DeepSeek |
