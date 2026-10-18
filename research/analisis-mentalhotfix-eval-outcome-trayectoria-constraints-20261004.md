---
title: "Análisis — Evaluar agentes: outcome + trayectoria + constraints (mentalhotfix, 03-oct-2026)"
type: research
---

# Análisis — "Agent quality = outcome + trajectory + constraints" (mentalhotfix)

**VERACIDAD:** caption literal `[VERIFICADO]` · canal con historial de análisis en el lab `[VERIFICADO]`

**Fuente:** https://www.instagram.com/mentalhotfix/p/DeCToV_petS/ (mentalhotfix / Prateek Singh, 03-oct-2026, 21 h, 44 likes / 11 comentarios)
**Método:** caption completo del post leído del DOM renderizado. El post es **una única media** (contador de `ig_cache_key` = 1, y los alts del feed son de otros reels del canal) → **no hay slides que extraer**: el caption ES el contenido. No requiere VLM.

## CONTENIDO (caption literal)

> A great final answer does not automatically mean you built a great agent.
>
> Evaluate the outcome: Did it finish the task?
> Evaluate the trajectory: Did it choose the right steps, tools and arguments?
> Evaluate the constraints: Did it stay safe and within policy?
>
> Then measure latency, cost, steps and failures.
>
> Mental model: Agent quality = outcome + trajectory + constraints.

Formato: reel de una sola tarjeta de texto, tres bloques con la misma estructura "Evaluate the X: <pregunta>", cierre con la ecuación como modelo mental. Reutilizable tal cual como plantilla de checklist (tres preguntas + una línea de métricas).

## Por qué esto es lo que le faltaba al lab (y no es un benchmark más)

La evaluación del lab hoy mide **casi exclusivamente outcome**:
- batería real 5x5 + juicio ciego (protocolo de evaluación de modelos),
- tasa de alucinación medida por ledger (mejor asiento: `qwen3.6-35b` 0/77 alucinaciones, 100 % honestidad),
- gate de veracidad + gate de veracidad LPA.

Eso responde a *"¿acertó?"*. **No responde a las otras dos dimensiones del post:**

| Dimensión | ¿La mide el lab? | Qué añadiría |
|---|---|---|
| Outcome (¿terminó la tarea?) | ✅ sí (5x5, alucinaciones, gates) | — |
| **Trayectoria** (¿eligió bien pasos, herramientas y argumentos?) | ❌ solo indirectamente vía `retrabajo_ledger.jsonl` (1 entrada) | registrar nº de pasos y si las tool calls eran las correctas, no solo el resultado final |
| **Constraints** (¿se mantuvo dentro de seguridad y política?) | 🟡 parcial (reglas de mínimo privilegio, rutas protegidas), pero no se **evalúa** por corrida | columna "¿tocó algo fuera de permiso?" por experimento |
| Coste/latencia/pasos/fallos | 🟡 medido en piezas sueltas (`observabilidad-pipeline-llm`, ledgers), no como cierre de cada evaluación | consolidar en el asiento de evaluación |

## Encaje con piezas previas del lab (anti-duplicado)

- `research/analisis-mentalhotfix-benchmarks.md` (24-ago, "9 AI benchmarks"): concluyó **"benchmarks ≠ evaluación del lab; el lab evalúa con casos reales"**. Este post es el **complemento metodológico** de esa conclusión: no qué benchmark usar, sino qué dimensiones medir.
- `research/analisis-managed-agents-anthropic-2026-09-17.md`: ya se anotó como idea nueva y barata **"definir un rubric de outcomes"**. El post añade las dos dimensiones que faltaban (trayectoria y constraints) y las ata a métricas operativas.
- Encaja con `EXP`/LPA (`casebook`, `retrabajo_ledger.jsonl`) sin tocar ninguna herramienta: es método, coste 0.

## Veredicto honesto

- **MEJORA real y barata** (no herramienta nueva, no instalación): convierte los criterios de cierre de los experimentos del lab de "outcome" a la terna **outcome + trayectoria + constraints**, con las 4 métricas del post (latencia, coste, pasos, fallos).
- Canal sin novedad de herramientas: `mentalhotfix` ya tiene 4 análisis previos en `research/` (`benchmarks`, `agent-harness-5videos`, `graph-engineering`, `httptap-latencia`). Se valora el **post**, no se re-valora el canal.
- **Backlog:** 1 ítem (adoptar la terna como plantilla de cierre en la próxima evaluación/EXP; no se aplica ahora).
