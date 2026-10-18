---
title: "Análisis — \"New Hermes Agent OS is Crazy Good\" (Julian Goldie SEO, 24-ago-2026)"
type: research
---

# Análisis — "New Hermes Agent OS is Crazy Good" (Julian Goldie SEO, 24-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.youtube.com/watch?v=xFnWn4X6wRk (Julian Goldie SEO, 23-08-2026, 8:05 min, 2.074 views)
**Método:** subtítulos EN (77 KB, ES dio 429) → deduplicados (25.6K→8.6K chars) → análisis completo
**Contexto lab:** el vídeo trata de Hermes Agent (el agente del lab). El lab está en **v0.17.0**; el upgrade a ≥0.20 está CONGELADO por decisión del usuario (esperar a la 0.21).

## ⚠️ Nota de veracidad (regla gate): es 80% publicidad

Julian Goldie es un **avatar digital de una agencia SEO** (Goldie Agency). El vídeo dedica ~60% a vender el "AI Profit Boardroom" (comunidad de pago, 2.800+ miembros, zip file, roadmap 30 días, coaching). El contenido técnico real de la 0.20 ocupa ~40%. La demo es real pero el objetivo es el embudo de venta.

## Qué trae Hermes 0.20 según el vídeo (3 features reales)

### 1. 🎙️ Voz en tiempo real (conversación real)
- Streaming de voz mientras piensa + **interrupciones mid-response** (le cortas y se adapta)
- Wake words que enrutan a distintos perfiles (contenido / research / dashboard)
- "No es un gimmick — es la interfaz de operación"

### 2. 🤝 A2A 1.0 (agent-to-agent) — el más importante
- **MCP = manos** (acceso a herramientas) vs **A2A = conversación entre agentes** (delegar, coordinar, recibir)
- Demo: una misión ("encuentra la historia top de IA y conviértela en oportunidad de YouTube") → Hermes delega a agentes especialistas (research / analysis / content) y **reúne el resultado** — "no hice 5 prompts, solo di un objetivo"
- **Esto ES lo que el lab tiene anotado como A3** (Bot Mode/A2A tras el upgrade ≥0.20)

### 3. 🔗 Webhooks (push signal con HMAC)
- Antes: sistemas externos tenían que **preguntar** ("¿terminaste?"). Ahora: Hermes **empuja** señal (task done, session ended, tool used) a donde quieras, con **firma HMAC** (el receptor verifica que viene de tu Hermes)
- Demo: Hermes termina de rankear → webhook → el sistema de contenido recibe → draft + posts + notificación

### 4. 🖥️ "Agent OS" (el marco que vende)
4 capas: intelligence (Claude/Claude Code) · execution (OpenClaw) · **research/operations (Hermes)** · memory (Obsidian) + dashboard "misión control" (runs, tool calls, kanban, schedules, health)

## Mapeo contra el lab

| Feature 0.20 | En el lab | Estado |
|---|---|---|
| **A2A 1.0** | A3 anotado (Bot Mode/A2A) | 🔴 Requiere ≥0.20 → **congelado esperando 0.21** (decisión 23-ago) |
| **Voz en tiempo real** | `dictado-voz` (Whisper local) — pero es dictado, no conversación con interrupciones | ⚪ Futurible bajo |
| **Webhooks con HMAC** | El lab encadena con **crons + context_from + notify** (equivalente funcional) | ⚪ Ya resuelto por otra vía |
| **"Agent OS" (dashboard + capas)** | El lab ES un agent OS: Hermes + 33 crons + skills + pipeline_obs + kanban + Telegram como misión control | ✅ Ya lo tienes, montado a tu manera |

## Veredicto: VALOR MEDIO-BAJO (validación + 1 confirmación, sin futuribles)

1. **Confirma externamente** que A2A 1.0 está EN 0.20 (no en 0.21) — el checklist del lab ya lo sabía; la decisión de esperar a 0.21 **se mantiene** (lección Gerald: .0 trae bugs).
2. **El "Agent OS" que vende = lo que el lab ya tiene**: Hermes + crons + skills + memoria + dashboard (Telegram). No hay nada que comprar.
3. **Único dato reutilizable**: los webhooks con HMAC podrían servir si algún día el lab quiere que un cron notifique a un sistema externo — pero los crons con `notify_on_complete` ya cubren el caso.
4. **La señal de venta es clara** (comunidad de pago, "descárgate el zip") — se descarta como ruido de marketing.

**Sin acción.** Registrado como validación de que el stack del lab (Hermes + crons + skills) ya implementa el patrón "agent OS" que el vídeo vende, y como confirmación de que el salto pendiente es a 0.20.x+ (A2A incluido) cuando se decida.
