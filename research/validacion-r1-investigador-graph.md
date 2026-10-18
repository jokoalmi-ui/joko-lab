---
title: "Validación R1-14B como investigador — PRUEBA INVALIDA + Claims MCP verificados (18-ago-2026)"
type: research
---

# Validación R1-14B como investigador — PRUEBA INVALIDA + Claims MCP verificados (18-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Contexto:** F4 del PRD graph (research/prd-graph-delegacion-multiagente.md) —
validar si deepseek-r1-distill-qwen-14b (delegation.model nuevo, 18-ago 18:32,
backup config bak-20260818-r1) puede sustituir a llama31-8b como nodo
INVESTIGADOR del graph, tras el veredicto definitivo de llama31 (3º uso,
deleg_143086fd: NO fiable para investigación web, ni siquiera acotada).

## 🔴 RESULTADO: PRUEBA INVÁLIDA (dato de proceso, no de modelo)

| Dato | Valor |
|---|---|
| Delegación | deleg_77902cd7 |
| Tema | MCP (1 concepto, acotado) |
| Modelo REAL usado | **llama31-8b-64k** (NO R1-14B) |
| api_calls | 2 (pedido mínimo 3) |
| Salida | incompleta (no entregó JSON con 3 claims) |
| Tiempo | 76.6s |

**Por qué fue inválida (verificado con ps/date/config):**
- La config en disco SÍ apunta a R1-14B desde las 18:32 (grep `^delegation:` →
  `model: deepseek-r1-distill-qwen-14b`).
- La sesión CLI desde la que se lanzó la delegación arrancó a las **16:52**
  (PID 7143/7166, `ps -p ... -o lstart`), es decir, **1h40 ANTES** del cambio.
- Hermes carga `delegation.model` al arrancar la sesión; una sesión viva NO
  recarga la config en caliente. Por eso el subagente corrió con llama31
  (el resultado lo dice explícitamente: `Model: llama31-8b-64k`).

**Conclusión:** el fallo de deleg_77902cd7 NO prueba nada sobre R1-14B. Es el
mismo fenómeno que deleg_07677a11 (handoff 19:12: "el proceso activo seguía
usando llama31; config vieja en memoria"). **R1-14B sigue SIN validar como
investigador.**

**Requisito para una prueba VÁLIDA:** lanzar la delegación desde una sesión
Hermes arrancada DESPUÉS del cambio de config (18:32). Es decir: /new en CLI
(o reiniciar el proceso Hermes) y desde la sesión nueva delegar 1 concepto
acotado con prompt JSON cerrado. Comprobar en el resultado que
`Model: deepseek-r1-distill-qwen-14b` ANTES de mirar api_calls/JSON.

## ✅ CLAIMS MCP VERIFICADOS EN SESIÓN (entregados al usuario)

Dado que la delegación falló, la investigación se hizo EN SESIÓN con
web_search + curl directo (regla definitiva del graph: investigador en sesión).

| # | Claim | URL | HTTP | Cita literal |
|---|---|---|---|---|
| 1 | MCP es un estándar abierto para conectar aplicaciones de IA a sistemas externos (datos, herramientas, flujos de trabajo) | https://modelcontextprotocol.io/ | 200 | "MCP (Model Context Protocol) is an open-source standard for connecting AI applications to external systems. Using MCP, AI applications like Claude or ChatGPT can connect to data sources (e.g. local files, databases), tools (e.g. search engines, calculators) and workflows" |
| 2 | MCP fue creado en Anthropic por David Soria Parra y Justin Spahr-Summers; presentado el 25-nov-2024 | https://www.anthropic.com/news/model-context-protocol | 200 | "Introducing the Model Context Protocol ... Nov 25, 2024" y "MCP was created at Anthropic by David Soria Parra and Justin Spahr-Summers." |
| 3 | MCP resuelve las integraciones fragmentadas con un estándar universal único | https://www.anthropic.com/news/model-context-protocol | 200 | "It provides a universal, open standard for connecting AI systems with data sources, replacing fragmented integrations with a single protocol." |

Fechas de acceso: 18-ago-2026. Nota: web_extract NO disponible (backend
DuckDuckGo solo-búsqueda) → extracción con curl + parse HTML.

## Estado F4 tras esta sesión

- llama31-8b: DESCARTADO para investigación web (1/5 usos válidos, suerte aislada).
- R1-14B: configurado en disco, disponible en Ollama (8.98 GB, Q4_K_M, 14.8B,
  ctx 131072, capability SOLO "completion" — ver /api/tags), **SIN validar**.
- Hipótesis abierta: R1-14B no lista capability "tools" en Ollama → puede que
  el tool-calling no funcione para web_search en subagentes. Si la prueba
  válida da api_calls=1 sin JSON, sería la causa.
- Regla actual del graph: investigación SIEMPRE en sesión (no cambia hasta
  que R1 demuestre lo contrario).

## 🔴 VEREDICTO FINAL F4 (18-ago-2026, opción B elegida por el usuario)

**La delegación local de investigación queda DESCARTADA — R1-14B no es viable
en la RTX A2000 12 GB.** Secuencia validada con datos:

1. Prueba deleg_bc20ef6c (sesión nueva, 20:19): Model: deepseek-r1-distill-qwen-14b
   ✓ — la config y la sesión nueva YA funcionan (bloqueo anterior resuelto).
2. Bloqueador real: Modelfile trae PARAMETER num_ctx 8192 (verificado con
   /api/show); Hermes exige >= 64000 tokens de contexto runtime para tool use
   fiable. El subagente murió en 0.37s antes de llamar a web_search (error de
   runtime, no de modelo ni de tool-calling).
3. VRAM (nvidia-smi): 12282 MiB total · 8745 usados · 3154 libres; LM Studio
   (GLM) ocupa 8134 MiB. R1-14B Q4_K_M pesa ~9 GB solo de pesos → no cabe con
   GLM residente. A 64K contexto: ~12.2 GB totales (pesos + KV cache Q8) → al
   límite absoluto de la GPU, con riesgo de OOM y offload CPU.
4. Vía A evaluada y descartada (descargar GLM + regenerar Modelfile con
   num_ctx 65536 + reiniciar contenedor Ollama): mucho esfuerzo para un
   resultado probablemente inestable.

**Regla definitiva e inmutable hasta señal de activación: la investigación
con fuentes SIEMPRE en sesión con web_search directa; NO delegar investigación
con modelos locales (ni llama31 ni R1-14B).** Única vía futura: pinear
delegation.model a cloud (F4, señal: volumen de contenido alto ≥3 posts/semana
y cuello de botella en tiempo de investigación en sesión). El graph queda como
PROCEDIMIENTO de sesión: investigador (sesión) → verificación URLs (sesión) →
redactor (sesión) → revisor (sesión).
