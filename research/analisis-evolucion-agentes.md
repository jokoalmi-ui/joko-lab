---
title: "Análisis — Reel Instagram: 5 niveles de evolución de AI Agents (dailydoseofds_)"
type: research
---

# Análisis — Reel Instagram: 5 niveles de evolución de AI Agents (dailydoseofds_)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 05-ago-2026
**Fuente:** https://www.instagram.com/p/Dbpf6wQgefc/ — dailydoseofds_ (Daily Dose of Data Science)
**Nota:** Post del 04-ago, caption completo extraído (texto + alt de imagen)

---

## Los 5 niveles (según el post)

| Nivel | Arquitectura | Capacidad |
|---|---|---|
| 1 | LLM ventana pequeña | Chatbot básico (ChatGPT 4K tokens) |
| 2 | LLM ventana grande | Parsea docs largos (Claude/ChatGPT) |
| 3 | LLM + tool usage (**era RAG**) | Datos frescos + APIs (search, calculadoras, DBs) |
| 4 | Multimodal + tools + **memoria** | Texto+imagen+audio; persistencia entre interacciones |
| 5 | Agente con **razonamiento + memoria** | Memoria corto/largo plazo/episódica + tool calling + ReAct |

**Frase clave:** "Esta es la era de los agentes de IA en la que vivimos hoy"
(nivel 5). Pregunta final del autor: ¿cuál será el siguiente nivel?

---

## Posición de Joko Lab en el mapa

| Nivel | Estado en el lab |
|---|---|
| 3 (RAG) | ✅ Completo — LanceDB + BGE-M3 + reranker |
| 4 (multimodal) | ✅ GLM 4.6V (visión) vía LM Studio |
| 5 (razonamiento + memoria) | ✅ Casi total — memory persistente, skills, decision-ledger, file bus multi-sesión |

**El lab está en el nivel 5** — el más avanzado del gráfico.

**Mapeo de la "memoria episódica" del gráfico:**
- Memoria corto plazo → contexto de sesión Hermes
- Memoria largo plazo → knowledge objects + LanceDB + skills
- Memoria episódica → decision-ledger.jsonl + session history + file bus
  (team-context/) creado hoy

**Razonamiento + ReAct** → el bucle agente-herramientas de Hermes
(decision-engine + delegate_task + tools)

---

## Nota

Post divulgativo de alta calidad (Daily Dose of Data Science, cuenta
especializada). Confirma que la arquitectura del lab (nivel 5) es la cima
actual de la evolución de agentes. No requiere acción — validación de posición.

**Bonus:** el mismo autor tiene post sobre "Claude Code unpacked" (métricas de
uso de Claude Code) — relacionado con el análisis de OpenCode del mismo día.
