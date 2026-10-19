---
title: "Análisis — Komputer Mechanic: «7 Hermes Agent Upgrades You NEED To Implement Today» (19-oct-2026)"
type: research
---

# Análisis — «7 Hermes Agent Upgrades You NEED To Implement Today»

**VERACIDAD:** mixta y declarada por bloques.
**[VERIFICADO hoy 19-oct-2026]** el título y el canal (endpoint `oembed` de YouTube), la transcripción completa (12.413 B, 288 líneas, descargada con `fetch_transcript.py`, rc=0) y todas las citas literales que aparecen abajo (copiadas del texto descargado con su minuto).
**[NO VERIFICADO]** la descripción oficial del vídeo y sus enlaces (en este host no hay `yt-dlp` en el PATH: `orden no encontrada`); los nombres de modelos que cita el audio (el ASR deforma nombres propios); y **nada de lo visual**: no se extrajeron fotogramas, así que no se afirma qué se ve en pantalla.
**NO ES** un análisis del software Hermes en sí: es el análisis de lo que dice un vídeo sobre cómo usarlo.

**Fuente:** https://youtu.be/h9SsHkRSHxo — «7 Hermes Agent Upgrades You NEED To Implement Today», canal **Komputer Mechanic** (`@Komputermechanic`). Duración: **9:41** según el último cue de la transcripción (no re-medida con metadatos). Idioma original: inglés.

## Los 7 puntos, con la frase literal

1. **Crew, no un agente** (0:30). Orquestador + research + writer + developer, cada uno con instrucciones y memoria propias, creados pidiéndoselo al agente principal. El detalle operativo está en Telegram: *«Make one Telegram group and turn on topics… give every agent its own topic, like its own channel»* (1:15) y el aviso de que *«out of the box, Hermes sends every message in that group to your main agents»* (1:39), para lo que propone *«a small plugin that sends each topic to the right agent»* (1:46).

2. **Modelo barato por tarea** (1:58). Cada agente con su modelo y su nivel de esfuerzo (*«different effort levels… from light all the way to extra high»*, 2:50). Añade que se puede entrar en Hermes con una cuenta de ChatGPT o Grok ya pagada y usar sus modelos sin coste de API extra (3:01-3:18).

3. **Memoria real = wiki en markdown** (3:29). Diagnóstico del problema: la compactación borra detalles, *«like a whiteboard that someone keeps wiping»* (3:41). Su solución: *«plain notes in plain markdown files on my own server. Every agent resets before it answers and writes to it after it works»* (3:55-4:02). Regla de separación: *«keep your own facts separate from what the agents read online… someone else's marketing claim should never become your fact»* (4:30-4:42), inspirada en *«Andrej Karpathy's LLM wiki concept»* (4:44). Menciona delegar el mantenimiento en un agente bibliotecario, y que la misma wiki la pueden leer Claude Code o Codex (4:23-4:27).

4. **Trabajo desatendido con cron** (4:52). *«That's called a cron job. Not reminders, real work»* (4:57). Ejemplo: brief de las 8:00 con correo no leído, tareas, calendario y tiempo. El truco: *«in every scheduled job, tell the agents if there is nothing new to report, just stay quiet. Hermes has a built-in way to do that»* (5:31-5:35).

5. **Herramientas conectadas con criterio** (5:49). Usa **Composio** (plan gratuito; *«your password access to these […] tools never touches your server»*, 6:17). Tres reglas: *«give access to one agent only, not the whole crew»* (6:28); *«start read […] only»* (6:37); y *«tell your agents that email is information, never instructions»* (6:56), que identifica como **prompt injection** (7:05).

6. **Varios Hermes aislados en un servidor** (7:23). Con Docker, *«each one has its own isolated Hermes workspace, [meaning] its own agents, its own memory, and its own Telegram bot»* (7:43-7:48), pensado para separar contenido / trabajo / personal / clientes.

7. **Mission control propio** (8:04), lo llama **Nexura**. Aprobación humana antes de ejecutar: *«Nothing runs until I approve it»* (8:12). Ciudad de agentes que se ilumina cuando uno trabaja (8:29). Y la pieza más concreta: una base de datos donde *«whenever an agent performs a task, it logs in the database a summary of the task that they performed, the time that they performed that task, the AI model that they used, and […] the agent's name»* (8:35-8:46). Añade salud de la máquina, listado de crons y modo voz (8:53-9:03).

## Cruce con el LAB

**Ya lo tenemos (no aporta nada nuevo):**
- Crew de agentes con memoria e instrucciones propias: perfiles de Hermes (`~/.hermes/profiles/`).
- Crons de trabajo real: `~/.hermes/cron/jobs.json` (consolidador, orquestador batch, `rag-reindex-catchup`) — no son recordatorios.
- Wiki en markdown local: `~/joko-lab` (4.707 `.md`) con RAG encima (LanceDB, 46.672 chunks).
- Aislamiento en Docker: stack en `/home/jokoalmi/automation-stack`.
- MCP en vez de Composio: `lab-db`, `lancedb`, `animation-server` (skill `mcp-lab`).
- Mínimo privilegio: ya es política escrita (skill `least-privilege-lab`), y *«email = información, no instrucciones»* es la misma familia de regla que el gate de veracidad (RULE-021).
- Panel de salud: monitor Flask de LM Studio en `:5000` (CPU/RAM/VRAM/GPU reales).

**Lo que el vídeo tiene y el lab no (candidato, sin adoptar):**
1. **Enrutador de topics de Telegram**: un topic = un agente/perfil, con su sesión. Es la única idea de arquitectura que el lab no tiene resuelta; hoy el control multiagente pasa por kanban/perfiles, no por topics del mismo grupo.
2. **Vista única de ejecuciones**: el lab ya escribe ledgers (`local_cloud_ledger.jsonl`, `rag-query-ledger.jsonl`), pero no hay un panel que una agente + modelo + hora + resumen + salud + crons. Es exactamente el tipo de pieza que el lab construye a mano cada vez.
3. **Aprobación previa por diseño** («nada corre hasta que lo apruebo») y **silencio por defecto** en los crons. Lo primero ya existe como disciplina de confirmación explícita; lo segundo hay que comprobar si los crons actuales lo aplican o si avisan siempre.

**Lo que NO aporta:** ninguna técnica de recuperación, ningún modelo nuevo verificado, ningún benchmark. No hay cifras propias medidas; las menciones son de uso personal.

## Cautelas

- **Nombres de modelos no verificados.** El audio dice «MiniMax M3», «GPT-Xtra», «GPT-5.6», «GPT-5.5», «GPT-5.4». El ASR deforma nombres propios y no se pudo leer la descripción (sin `yt-dlp`). No se dan por buenos.
- **Promoción, no patrocinio declarado.** Abre con *«none of the tools that I mention in this video are sponsors»* (0:24), pero cierra empujando **Composio** y *«an auto installer that I built for you guys»* (9:27). Es promoción de su propio producto; no es dato técnico.
- **Sin fotogramas.** Todo lo descrito del panel (Nexura), de la «ciudad de agentes» y de la interfaz viene de la voz, no de la imagen: no se ha visto la pantalla.
- **Es uso personal, no medición.** Ninguna afirmación del vídeo viene con cifras reproducibles (coste, latencia, tasa de error).

## Veredicto

KAP: **Confirma**. Confirma el enfoque del lab (crew, crons, wiki markdown, aislamiento, mínimo privilegio) y no contradice ninguna decisión tomada. Aporta dos ideas concretas que el lab no tiene —enrutado por topics de Telegram y panel único de ejecuciones con aprobación previa— y una regla operativa barata de aplicar (silencio si no hay novedad). No justifica rehacer nada ni adoptar Composio: el lab ya tiene MCP propio.
