---
title: "Análisis — 7 Ways to Speed Up AI Agents In Production (mentalhotfix, reel 102s)"
type: research
---

# Análisis — 7 Ways to Speed Up AI Agents In Production (mentalhotfix, reel 102s)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 13-ago-2026 (12:30 CEST)
**Fuente:** https://www.instagram.com/p/Db8ZWnPJ-Im/ — mentalhotfix (Prateek Singh)
**Tipo:** Reel 102s — pipeline completo del lab (audio whisper small + 12 frames + GLM)
**Método:** analizar_reel_completo.sh → 12 frames + transcripción (1.939 chars)

---

## Contenido (del AUDIO — las 7 técnicas completas con detalle)

> "Your AI agents might be slow, even if you are using a faster model, because
> the model is only one part of the delay. Your agent may be wasting tokens,
> overthinking simple tasks, waiting for tools, and taking the longest
> possible path."

### Las 7 técnicas (audio completo)
1. **Model Routing** — modelo pequeño/rápido para clasificación y decisiones
   simples; modelos fuertes solo para razonamiento difícil; **código normal
   cuando la IA no hace falta**
2. **Token Budgeting** — límites separados para contexto de entrada, razonamiento
   y salida final. "Una decisión de routing simple no debe tener el mismo
   presupuesto que una investigación profunda"
3. **Context Pruning** — NO enviar toda la conversación, ni toda la memoria, ni
   las 100 definiciones de tools en cada petición. Recuperar solo lo que el
   paso actual necesita
4. **Caching** — cachear las partes estables del prompt, definiciones de tools,
   resultados recuperados y estado de sesión en vez de recomputarlos
5. **Parallel Execution** — ejecutar búsquedas y tool calls independientes
   juntas; incluso **speculative execution** (empezar el siguiente paso probable
   antes)
6. **Reduce Round Trips** — agrupar operaciones en una; **programmatic tool
   calling** para que filtrado/paginación/bucles ocurran en código, no en
   "20 ciclos modelo-tool-modelo"
7. **Progressive Delivery** — no dejar al usuario mirando un spinner; hacer
   stream del progreso real. Optimizar para **time to first useful result**
   (no solo time to first token)

**Mnemónico del autor: Routing, Budgeting, Pruning, Caching, Parallelization,
Collapsing, Streaming.**

---

## 🎯 Veredicto — RELEVANCIA ALTÍSIMA (el lab YA hace 5 de 7, y hay 2 gaps reales)

| Técnica | Lab | Estado |
|---|---|---|
| **1. Model Routing** | `llm-router.sh` (batch→R1, visión→GLM, interactivo→DeepSeek) | ✅ **SÍ — implementado** (y el "código normal cuando no hace falta IA" = scripts deterministas del lab) |
| **2. Token Budgeting** | max_tokens por script/uso | 🟡 Parcial — no hay límites separados por rol (entrada/razonamiento/salida) |
| **3. Context Pruning** | Skills compactadas, progressive disclosure, contextos por tarea | ✅ **SÍ — en marcha** (compactación 12-ago, -180KB) |
| **4. Caching** | Prompt caching de Hermes, reranker, modelos cargados | ✅ SÍ |
| **5. Parallel Execution** | delegate_task batch (3), GLM lote 3 | ✅ SÍ (sin speculative execution) |
| **6. Reduce Round Trips** | Scripts deterministas, pipeline directo | ✅ SÍ |
| **7. Progressive Delivery** | Watchdogs, notificaciones | 🟡 **GAP — el lab no hace stream de progreso** (pero es un lab local, sin usuarios mirando spinners) |

### 🟡 Los 2 insights más accionables para el lab

1. **Token Budgeting separado** (técnica 2): el lab podría fijar presupuestos
   distintos para contexto/razonamiento/salida según la tarea — conecta con la
   palanca de coste DeepSeek (99% contexto). Es la técnica que más impacto
   tendría en el coste del lab.

2. **Context Pruning explícito** (técnica 3): "no enviar las 100 tool
   definitions en cada petición" — el lab ya restringe toolsets en crons, pero
   la sesión principal envía todo. Valida el patrón de `enabled_toolsets`.

### Nota honesta
- El autor promociona un blog al final (ignorar)
- La técnica 7 (progressive delivery) aplica a productos con usuarios — el lab
  es local, impacto bajo, pero el principio de "progreso temprano" es útil
- El mnemónico (routing/budgeting/pruning/caching/parallelization/collapsing/
  streaming) es útil como checklist de arquitectura

---

## Conclusión

**RELEVANCIA ALTÍSIMA — valida el router del lab (técnica 1) y revela 2
mejoras accionables**: Token Budgeting separado (impacto directo en coste) y
Context Pruning explícito (validado por los toolsets restringidos). El audio
fue esencial: los frames mostraban iconos (Route, Budget, Prune, Cache...),
la voz dio las 7 técnicas con detalle de implementación.
