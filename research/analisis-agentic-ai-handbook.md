---
title: "Análisis — AGENTIC AI Handwritten Handbook (codedsoul_05, 20 páginas)"
type: research
---

# Análisis — AGENTIC AI Handwritten Handbook (codedsoul_05, 20 páginas)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 05-ago-2026
**Fuente:** https://www.instagram.com/p/Dbp71gRDYLv/ (codedsoul_05 — 20 páginas carrusel)
**Material:** Notas manuscritas "AGENTS v1.0 — Beginner to Production"
**Imágenes:** `/tmp/agentic_ai/pagina_01..20.jpg` (descargadas del CDN)

---

## Índice del handbook (19 secciones)

| Pág | Sección | Tema |
|---|---|---|
| 1 | Portada | AGENTIC AI Handbook — Building LLM Agents that Plan, Use Tools, Remember, Finish Jobs |
| 2 | 01 | ¿Qué es Agentic AI? (definición, autonomía, capacidades, cuándo usarlo) |
| 3 | 02 | Componentes/Arquitectura del agente |
| 4 | 03 | **The Agent Loop** (THINK→SELECT→EXECUTE→OBSERVE→UPDATE) |
| 5 | 04 | Herramientas y function calling ("las manos del agente") |
| 6 | 05 | Planning Patterns (cómo decide el siguiente paso) |
| 7 | 06 | Sistemas de memoria |
| 8 | 07 | **State, Workflows & Durability** (máquina de estado) |
| 9 | 08 | **Multi-Agent Systems** (supervisor/worker, pipeline, debate) |
| 10 | 09 | Orchestration Layer (primitivas, ruteo de modelos, build vs buy) |
| 11 | 10 | **RAG meets Agents** (RAG fundamenta, agentes deciden cuándo recuperar) |
| 12 | 11 | **Evaluación** ("si no puedes puntuar al agente, no lo lanzas") |
| 13 | 12 | Seguridad y guardrails (defensa en profundidad, 7 capas) |
| 14 | 13 | Fiabilidad y modos de fallo (tabla fallo→acción) |
| 15 | 14 | Observabilidad y tracing |
| 16 | 15 | Costo, latencia y enrutamiento de modelos |
| 17 | 16 | **Production Reference Stack** (7 capas) |
| 18 | 17 | Patrones de diseño de agentes (10 patrones con WHEN) |
| 19 | 18 | Q&A de entrevistas (agente vs chatbot, bucles infinitos) |
| 20 | 19 | Recap & Cheat Sheet |

---

## Las ideas clave (lo que de verdad importa)

### 1. Definición (pág 2)
> **Agentic AI = LLM + tools + memory + control loop hacia un objetivo**

Espectro de autonomía: Script/RPA → Chatbot → Tool-calling → Agentic workflow → Multi-agent.

### 2. El Agent Loop (pág 4) — la página clave
> "Cada agente serio es una máquina de estado envuelta alrededor de una llamada a LLM"

THINK/PLAN → SELECT TOOL → EXECUTE → OBSERVE → UPDATE STATE/MEMORY → repetir.

### 3. Herramientas (pág 5)
- "Las manos del agente": tipadas, permitidas, conscientes de efectos secundarios
- Especificación: nombre, descripción, esquema JSON, autenticación, idempotencia, timeout, rate limit
- Categorías: solo lectura / escritura / sandbox código / navegador / recuperación (RAG)
- **Regla: privilegios mínimos**

### 4. Durabilidad (pág 8)
- Los agentes de producción son flujos de trabajo duraderos
- Máquina de estado con puntos de control → continuar desde el último paso
- "Los agentes solo por prompt mueren al reiniciar el proceso"
- Estilos: bucles (code-first), flujos gráficos, sagas por eventos

### 5. Multi-agente (pág 9)
- Patrones: Supervisor/Worker, Pipeline, Debate/Critic, Especialistas paralelos
- **Tradeoffs: más agentes ≠ más inteligencia; impuesto de coordinación; memoria compartida = conflictos**

### 6. RAG meets Agents (pág 11)
- RAG fundamenta las respuestas; el agente decide cuándo y qué recuperar
- Búsqueda vectorial/SQL con filtros semánticos/ACL/timestamps

### 7. Evaluación (pág 12)
> "Si no puedes puntuar al agente, no lo lanzas"

- Unit (esquemas), Trajectory (¿herramientas correctas en orden?), Outcome (estado final), Rubric (juez LLM), Online (likes/escalación)
- **Métricas: tasa de éxito, pasos, costo, latencia, errores de herramientas, alucinaciones, seguridad = 0**

### 8. Seguridad (pág 13)
- Defensa en profundidad: política + filtros + allowlist herramientas + filtros salida + aprobación humana + sandbox + auditoría inmutable
- Amenazas: inyección de prompt, exfiltración, gasto descontrolado, confused deputy

### 9. Costo (pág 16)
> "Los agentes multiplican tokens — el presupuesto es una restricción arquitectónica"

- **North-star metric: costo por TAREA EXITOSA, no por llamada**

### 10. Stack de producción (pág 17)
7 capas: Clientes → Gateway API/Auth → Runtime agente (bucle/estado/presupuestos) → Gateway modelo → Herramientas (conectores/sandbox/secrets) → Memoria & RAG (vector+SQL+KV) → DB workflow/cola

---

## 🔗 Aplicación directa al LAB (lo más valioso)

| Concepto del handbook | El lab ya tiene | Gap |
|---|---|---|
| Agent Loop (THINK→SELECT→EXECUTE→OBSERVE) | ✅ L2 Loop Engineering (diseño 04-ago) | Coincide 1:1 |
| Herramientas con especificación + privilegios mínimos | ✅ Skills de Hermes + toolsets | — |
| Durabilidad (estado persistente, no morir al reiniciar) | ✅ file bus + shared-state + ledger | — |
| Multi-agente con tablero compartido | ✅ File bus por dominio + team-context | Patrón supervisor (Hermes orquesta) |
| **Evaluación: "si no puedes puntuar, no lo lanzas"** | 🟡 Verifier con bug (falso negativo TD-001) | **Falta: métricas de éxito por tarea** |
| **RAG meets Agents (agente decide cuándo recuperar)** | ✅ RAG con re-rank + query enriquecida | **Falta: el agente decida el QUÉ recuperar (tool call)** |
| **Observabilidad y tracing (pág 15)** | ✅ F4 implementado HOY (telemetría por paso) | Falta: traces multi-agente |
| **Costo por tarea exitosa** | 🟡 Solo se mide tokens RAG (P1 98.4%) | **Falta: costo por tarea del agente** |
| Patrones de diseño con WHEN (10 patrones) | 🟡 Patrón WHEN/TEMPLATE/PITFALLS (ya anotado) | Coincide con la idea del handbook 50 patrones |

**Conclusiones para el lab:**
1. El **L2 Loop Engineering es EXACTAMENTE el Agent Loop** del handbook — validación externa del diseño
2. El handbook **refuerza el patrón WHEN** (pág 18) — los KOs con formato WHEN/TEMPLATE/PITFALLS son la práctica estándar
3. Los **gaps reales**: evaluación con métricas por tarea, el agente decidiendo qué recuperar en RAG, y costo por tarea exitosa

---

## Nota sobre el post
- El caption pide "Comment 'Agentic' and I'll send the complete pdf in your dm" (trampa de DM)
- Las 20 páginas están completas en el carrusel (verificado: 20/20 descargadas y analizadas)
- Autor: codedsoul_05 — mismo creador del "50 Coding Patterns Handbook" (pagado 5€ por Joseba)
