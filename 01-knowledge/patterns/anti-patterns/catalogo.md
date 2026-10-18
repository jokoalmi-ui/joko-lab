---
type: knowledge
subtype: pattern
status: active
tags: [knowledge, pattern]
created: 2026-07-28
---
# Catalogo de Anti-Patrones — Joko Lab
# v2 — Umbral E3 actualizado segun auditoria de Claude (2026-07-28)
# Cambio: E3 requiere 3+ condiciones distintas (temperatura, max_tokens, tipo tarea)

========================================

Clasificacion por gravedad:
- FATAL:  El modelo falla siempre o casi siempre. No usar.
- ALTA:   Alta probabilidad de fallo. Evitar o mitigar.
- MEDIA:  Falla ocasional. Tener en cuenta.
- BAJA:   Falla raramente. Documentado pero no critico.

## FATAL

| Anti-patron | Modelos | Contexto |
|---|---|---|
| max_tokens < 1024 con reasoning models | Qwen3 14B, Qwen 3.5 9B | Content vacio por consumo del presupuesto en reasoning |
| max_tokens < 2048 con DeepSeek R1 | DeepSeek R1 14B | Content vacio o finish=length |
| max_tokens < 400 con Gemma 4 | Gemma 4 12B | Se come el presupuesto en reasoning |
| Prompt multi-instruccion a GLM | GLM 4.6V Flash | 3+ instrucciones → content vacio |
| Usar Qwen 3.5 9B para cualquier tarea | Qwen 3.5 9B | 0/5 tests utiles. Descartado. |
| Esperar texto de Llama 3.1 Instruct | Llama 3.1 Instruct | Siempre responde con function calls |

## ALTA

| Anti-patron | Modelos | Contexto |
|---|---|---|
| temperature > 0.3 en tareas tecnicas | Todos | Alucinaciones, imprecision |
| max_tokens < 2048 con GLM 4.6V | GLM 4.6V Flash | finish=length en codigo |
| JSON como instruccion a Dolphin | Dolphin Cyber LoRA | Responde texto, no JSON |
| Prompt espanol en modelo solo-ingles | Dolphin, Llama, Granite | Degradacion de calidad |
| Temperatura > 0.8 en DeepSeek R1 | DeepSeek R1 14B | Degradacion del razonamiento |

## MEDIA

| Anti-patron | Modelos | Contexto |
|---|---|---|
| Codigo extenso a GLM | GLM 4.6V Flash | finish=length en ~50% de los casos |
| max_tokens < 2048 con Qwen3 14B | Qwen3 14B | finish=length en codigo |
| Preguntas abiertas a Llama 3.1 | Llama 3.1 Instruct | Responde con calls (no es error, es comportamiento esperado) |

## BAJA

| Anti-patron | Modelos | Contexto |
|---|---|---|
| Esperar respuesta rapida de Gemma 4 | Gemma 4 12B | Es lento por diseno, no por error |

## Nota sobre el umbral E3 (actualizado 2026-07-28)

Siguiendo recomendacion de auditoria externa (Claude, 2026-07-28):

Un anti-patron se clasifica como E3 (validado) solo si se ha
observado en al menos 3 condiciones distintas:
- Temperatura diferente (ej: 0.2, 0.5, 0.7)
- max_tokens diferente (ej: 512, 1024, 2048)
- Tipo de tarea diferente (ej: codigo, creatividad, JSON)

Los anti-patrones marcados como FATAL con un solo test
(valoracion 0/5 como Qwen 3.5) se mantienen como FATAL por
contundencia del resultado, pero su clasificacion LPA se
revisara cuando haya datos en condiciones distintas.

## Historial de cambios

| Fecha | Cambio | Fuente |
|---|---|---|
| 2026-07-26 | Catalogo inicial (7 modelos, 35 tests) | EXP-20260726-001 |
| 2026-07-28 | Umbral E3 actualizado: 3 condiciones minimas | Auditoria Claude |
