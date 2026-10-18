---
title: "Análisis — Reel hackproduct: \"What happens inside an AI agent?\" (18-ago-2026)"
type: research
---

# Análisis — Reel hackproduct: "What happens inside an AI agent?" (18-ago-2026)

**Fuente:** https://www.instagram.com/reel/DcKr0Sxu07Z/ (hackproduct — canal conocido del lab, 8.1s, 720×900)
**Método:** video_versions → fetch navegador (MP4 210 KB) → scdet 2 frames → GLM + browser_vision ×2 (ambos frames = mismo contenido)
**VERACIDAD:** [VERIFICADO]
**Nota proceso**: pendiente del 18-ago (backup 18j) — procesado tras reinicio del PC (navegador reparado + GLM recargado). Whisper falló (libcublas, CUDA aún no activo tras reinicio) — no importa: el audio de reels casi nunca aporta.

## CONTENIDO (el flujo interno del agente, verificado)

**Título:** "WHAT HAPPENS INSIDE AN AI AGENT?" — 9 pasos:

1. **UNDERSTAND** — Intent · Constraints · Context
2. **PLAN** — Break steps · Pick tools · Set success
3. **RETRIEVE** — Memory · RAG · State
4. **REASON** — LLM thinks · Choose action · Need answer?
5. **ACT** — Search · API · Code · DB · **MCP Tools**
6. **OBSERVE** — Tool result · Errors · New info
7. **LOOP** — Plan → Reason → Act → Observe — *"This loop is the agent"*
8. **VERIFY** — Evals · Guardrails · Confidence
9. **FINAL ANSWER / ACTION** — Respond · Write · Trigger workflow

## 🎯 APLICACIÓN AL LAB — VALIDA EL DISEÑO DEL AGENTE HERMES

| Paso del reel | En el lab (real, verificado) |
|---|---|
| **UNDERSTAND** (intención, restricciones, contexto) | System prompt con reglas + contexto del usuario |
| **PLAN** (romper pasos, elegir tools) | Tools + skills (cargar skill relevante antes de actuar) |
| **RETRIEVE** (memoria, RAG, estado) | LanceDB (~20K filas recall@5 100%) + memoria + session_search |
| **REASON** (LLM piensa, elige acción) | GLM-4.6v / DeepSeek / R1-14B (router local/cloud) |
| **ACT** (API, código, DB, **MCP**) | **Manim MCP (1º del lab)** + terminal + file + webs |
| **OBSERVE** (resultado, errores) | Tool results + verificación de salidas reales |
| **LOOP** ("este bucle es el agente") | Hermes CLI + Telegram = bucle continuo |
| **VERIFY** (evals, guardrails, confianza) | **Gate de veracidad + suite 219 tests + fail-closed** |
| **FINAL** (responder, escribir, workflow) | Informes + backlog + crons + entregas |

**Este es EL diagrama del lab**: los 9 pasos describen literalmente cómo
funciona Hermes (y por extensión el lab). El que destaca: **VERIFY con
evals + guardrails** — exactamente lo que diferencia al lab (gate de
veracidad, fail-closed) de un agente "demo" (el reel del 18-ago de
mentalhotfix decía lo mismo: "demos work, production breaks" — el harness
importa).

## FORMATO (aislable)

- 9 pasos con sub-elementos — diagrama canónico de un agente
- Reutilizable para TFM/LinkedIn: "así funciona un agente por dentro — y así
  lo implementa el lab (los 9 pasos)"

## Veredicto
**VALIDA EL LAB / DIAGRAMA CANÓNICO.** Reel de hackproduct (canal ya
conocido: LangChain vs LangGraph del 14-ago): "What happens inside an AI
agent?" — 9 pasos (Understand→Plan→Retrieve→Reason→Act→Observe→Loop→Verify→
Final). El lab implementa los 9 con evidencia real (LanceDB, MCP, gate de
veracidad, suite 219, router). El paso VERIFY (evals+guardrails) es el que
separa al lab de un agente demo — coherente con mentalhotfix del 18-ago
("production is where they break"). Material directo para TFM/LinkedIn.
**Nota**: con este queda procesado el 1º de los 3 pendientes del 18-ago.
