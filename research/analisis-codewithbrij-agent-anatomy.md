---
title: "Análisis — \"One diagram. Every AI agent. Ever\" (codewithbrij, 22-ago-2026)"
type: research
---

# Análisis — "One diagram. Every AI agent. Ever" (codewithbrij, 22-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/reel/DcV7tohOyH7/ (codewithbrij, 22-08-2026, 17 likes)
**Método:** caption íntegro extraído (browser_console). Reel animado (formato diagrama en movimiento).

## Contenido: los 7 componentes de TODO agente de IA (en bucle)

| Componente | Qué es |
|---|---|
| 👁 **Perception** | Texto, API, sensores, eventos — normalizado antes de que el modelo lo vea |
| 🧠 **Reasoning** | LLM con chain-of-thought, ReAct o plan-and-execute. Pregunta en bucle: ¿puedo responder directo o necesito actuar? |
| 📋 **Planning** | Objetivo grande → subtareas ordenadas. "La pieza que todos omiten en el prototipo y sufren al integrarla después" |
| 💾 **Memory** | Corto plazo (contexto conversación) + largo plazo (vector stores, patrones aprendidos) — DOS sistemas, no uno |
| ⚙️ **Tools** | MCP, APIs, ejecución de código, BBDD, filesystem — donde el agente toca el mundo |
| 🛡 **Guardrails** | A lo largo de TODO el bucle (lado izquierdo), no solo en la entrada — "un gate en la entrada no hace nada sobre lo que el agente decide en el paso 4" |
| 📡 **Observability** | Traces, logs, coste, latencia — ancho completo: "no puedes depurar un bucle mirando una caja" |

**Los 2 diamantes donde el agente DECIDE**: "¿puedo responder directamente?" y "¿objetivo logrado?".
> "Cuando los agentes fallan en producción, casi nunca es por razonamiento malo. Es por esas dos comprobaciones mal definidas."

**Frase de cierre**: agente vs workflow → *"si el sistema elige su propio siguiente paso, es un agente"*.

## 🔴 Para el LAB — VALOR: ALTO (validación estructural del diseño)

**Los 7 componentes están TODOS en el lab:**
- Perception: entrada normalizada (Telegram, IG, cron) ✅
- Reasoning: LLM (DeepSeek/gpt-oss/GLM) con gate + revisor ✅
- Planning: skills con pasos validados + planning mode ✅
- Memory: MEMORY.md + MEP-001 + session_search (corto) + LanceDB RAG (largo) ✅ — "dos sistemas, no uno" ✅
- Tools: MCPs (lab-db, lancedb, animation-server) + terminal + file ✅
- Guardrails: gate veracidad + hardline + tirith fail-closed + redact_secrets ✅ — y la frase del post ("a lo largo del bucle, no solo en la entrada") = EXACTAMENTE la decisión del lab (tirith fail-closed, cron_mode deny, MCP solo lectura)
- Observability: proxy :9911 + telemetría + informe diario + watchdogs ✅

**Los 2 diamantes**: el lab los tiene (gate decide si responde o actúa; verificar_research decide si está bien).

## 🎯 Sobre el FORMATO (lo que le gusta al usuario)
Reel animado de diagrama en movimiento — el lab YA tiene la capacidad de hacerlo:
`gen_video_corto.sh` (imágenes + zoompan + xfade + voz edge-tts, todo local, 0 €) y Manim MCP (animaciones tipo 3Blue1Brown). El formato "diagrama animado que construye los 7 componentes en bucle" es reproducible con Manim o con escenas SDXL + movimiento.

**Sin futuribles de acción** (el diseño ya está). Futurible FORMATO: si el usuario quiere, se puede hacer un reel del lab con la misma estructura (diagrama animado de los 7 componentes del agente Hermes del lab) — material LinkedIn/IG educativo.
