# hermes-expert — Estructura de Hermes

> Verificado: 2026-07-05

## Árbol completo de ~/.hermes/

```
~/.hermes/
│
├── config.yaml                  # Configuración principal (686 líneas, v30)
├── .env                         # Variables de entorno (23 KB)
├── SOUL.md                      # Prompt del sistema (~18 KB)
├── .hermes_history              # Historial plano de sesiones (41 KB)
├── .skills_prompt_snapshot.json # Snapshot de skills cargadas (42 KB)
├── .update_check                # Última comprobación de actualización
├── auth.json                    # Credenciales de autenticación
├── auth.lock                    # Bloqueo de autenticación
├── context_length_cache.yaml    # Caché de contextos
├── interrupt_debug.log          # Log de depuración de interrupciones
├── models_dev_cache.json        # Caché de modelos (3 MB)
├── ollama_cloud_models_cache.json
├── provider_models_cache.json
├── processes.json               # Procesos activos registrados
│
├── state.db                     # SQLite: sesiones e IDs (12 MB)
├── state.db-shm                 # SQLite shared memory (32 KB)
├── state.db-wal                 # SQLite WAL (1.3 MB)
│
├── memories/                    # Memoria persistente
│   ├── MEMORY.md                # Notas personales de Hermes
│   ├── USER.md                  # Perfil del usuario
│   ├── MEMORY.md.lock
│   └── USER.md.lock
│
├── skills/                      # Skills instaladas (18 directorios)
│   ├── apple/                   #   → subskills: apple-notes, apple-reminders, findmy, imessage
│   ├── autonomous-ai-agents/    #   → subskills: claude-code, codex, hermes-agent, opencode
│   ├── computer-use/            #   → SKILL.md (cargada como skill activa)
│   ├── creative/                #   → subskills: ascii-art, p5js, excalidraw, comfyui...
│   ├── data-science/            #   → subskills: jupyter-live-kernel
│   ├── diagnostico-stack-local/ #   → SKILL.md (cargada como skill activa)
│   ├── dogfood/                 #   → SKILL.md (cargada como skill activa)
│   ├── email/                   #   → subskills: himalaya
│   ├── github/                  #   → subskills: code-review, issues, pr-workflow...
│   ├── media/                   #   → subskills: gif-search, heartmula, songsee...
│   ├── mlops/                   #   → subskills: evaluation, huggingface-hub, models...
│   ├── note-taking/             #   → subskills: obsidian
│   ├── productivity/            #   → subskills: notion, airtable, google-workspace...
│   ├── research/                #   → subskills: arxiv, blogwatcher, llm-wiki...
│   ├── smart-home/              #   → subskills: openhue
│   ├── social-media/            #   → subskills: xurl
│   ├── software-development/    #   → subskills: plan, spike, tdd, debugging...
│   └── yuanbao/                 #   → SKILL.md (cargada como skill activa)
│
├── hermes-agent/                # Código fuente de Hermes (35 subdirectorios)
├── sessions/                    # Snapshot de sesiones (1 archivo JSON)
├── state-snapshots/             # Snapshots de estado (5 subdirectorios)
├── logs/                        # Logs de ejecución
├── cache/                       # Caché general
├── audio_cache/                 # Caché de audio
├── image_cache/                 # Caché de imágenes
├── images/                      # Imágenes
├── pastes/                      # Pegado de contenido
├── scripts/                     # Scripts del usuario
├── sandboxes/                   # Entornos aislados
├── bin/                         # Binarios auxiliares
├── node/                        # Node.js runtime (7 subdirectorios)
├── cron/                        # Tareas programadas (vacío)
├── hooks/                       # Hooks (vacío)
└── pairing/                     # Emparejamiento de dispositivos
```

## Notas sobre la estructura

- **No existe** `~/.hermes/profiles/`. Hermes usa un perfil único plano.
- **memories/** contiene solo 2 archivos: MEMORY.md y USER.md. Ambos con lock.
- **cron/** y **hooks/** están vacíos. No hay tareas programadas ni hooks activos.
- **skills/** tiene 18 directorios pero solo 4 con SKILL.md propio.
- **state.db** es SQLite. Contiene sesiones, IDs de conversación y metadatos.
- **hermes-agent/** es el código fuente del agente, no documentación.
