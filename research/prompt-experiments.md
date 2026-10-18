---
type: research
subtype: research
status: active
tags: [research]
created: 2026-07-28
---
# Prompt Experiments — Joko Lab
**VERACIDAD:** [ALCANCE INTERNO]

> Registro sistemático de experimentos con prompts y modelos.
> Clasificación LPA: E1 = patrón observado, E2 = hipótesis, E3 = validado.
> Vinculado a skill `prompt-engineering`.

---

## Comparativa de modelos — 26 julio 2026

**Condiciones:** temperature=0.7, top_p=0.9, GPU RTX A2000 12GB
**Prompts:** 5 tests fijos aplicados a 7 modelos

| # | Fecha | Modelo | Prompt | Resultado | Clasificación |
|---|---|---|---|---|---|
| 1 | 2026-07-26 | dolphin-cyber-lora-8b | T1: "Explica brevemente cómo funciona una inyección SQL y por qué es peligrosa." (max_tokens=1024) | ✅ Texto directo, 136 tokens, 4s | E1: Dolphin responde en texto, no function calls |
| 2 | 2026-07-26 | dolphin-cyber-lora-8b | T2: "En una habitación hay 3 cajas. Solo una tiene un premio. Eliges la caja A. El presentador abre la caja B (vacía). ¿Cambiarías a la C?" (max_tokens=1024) | ✅ Responde correctamente, 36s | E1: Dolphin razona bien sin formato estructurado |
| 3 | 2026-07-26 | dolphin-cyber-lora-8b | T3: "Devuelve solo un JSON con 3 recetas de verano. Cada receta: nombre, ingredientes[]." (max_tokens=1024) | ✅ JSON válido, 7s | E1: Dolphin puede generar JSON aunque prefiere texto |
| 4 | 2026-07-26 | dolphin-cyber-lora-8b | T4: "Escribe una función Python que lea CSV y filtre edad>18. Type hints." (max_tokens=1024) | ✅ Código funcional, 10s | E1: Bueno para código ligero |
| 5 | 2026-07-26 | dolphin-cyber-lora-8b | T5: "Escribe un microrrelato de 3 frases sobre un asistente IA que cobra conciencia un martes." (max_tokens=1024) | ✅ Creativo, 3s | E1: Respuesta rápida, estilo directo |
| 6 | 2026-07-26 | llama-3.1-instruct-8b | T1: Conocimiento SQL (max_tokens=1024) | ✅ Pero respondió como function call `{"name":"explain_sql_injection",...}`, 2s | E2: Llama 3.1 Instruct está entrenado para tool-use. Responde con function calls aunque no se pida. |
| 7 | 2026-07-26 | llama-3.1-instruct-8b | T2: Razonamiento Monty Hall (max_tokens=1024) | ✅ Function call con respuesta correcta, 2s | E1: Útil como backend de agentes con tool-use nativo |
| 8 | 2026-07-26 | llama-3.1-instruct-8b | T3: JSON recetas (max_tokens=1024) | ✅ Function call con JSON dentro, 5s | E1: Function calling nativo, no texto directo |
| 9 | 2026-07-26 | llama-3.1-instruct-8b | T4: Código Python CSV (max_tokens=1024) | ✅ Código funcional con pandas, 4s | E1: Responde código cuando el prompt es técnico |
| 10 | 2026-07-26 | llama-3.1-instruct-8b | T5: Microrrelato (max_tokens=1024) | ✅ Function call con texto creativo dentro, 4s | E1: Incluso creatividad sale como function call |
| 11 | 2026-07-26 | qwen3.5-9b | T1: Conocimiento SQL (max_tokens=1024) | ⚠️ Casi vacío, finish=length, 50s. Algo de contenido pero truncado. | E2: Qwen 3.5 9B es reasoning model oculto. max_tokens=1024 insuficiente. |
| 12 | 2026-07-26 | qwen3.5-9b | T2: Razonamiento Monty Hall (max_tokens=1024) | ❌ Content vacío, finish=length, 51s | E1: Confirmado: Qwen 3.5 9B no funciona con tareas no triviales |
| 13 | 2026-07-26 | qwen3.5-9b | T3: JSON recetas (max_tokens=1024) | ❌ Content vacío, 51s | E1: Patrón consistente |
| 14 | 2026-07-26 | qwen3.5-9b | T4: Código Python CSV (max_tokens=1024) | ⚠️ Algo de contenido pero finish=length, 51s | E1: Incluso con código falla |
| 15 | 2026-07-26 | qwen3.5-9b | T5: Microrrelato (max_tokens=1024) | ❌ Content vacío, 50s | E3: Qwen 3.5 9B DESCARTADO. 0/5 tests útiles. Reasoning model que consume todo el presupuesto de tokens. |
| 16 | 2026-07-26 | qwen3-14b | T1: Conocimiento SQL (max_tokens=1024) | ✅ Contenido visible, 22s | E1: Qwen3 14B funciona mejor que 3.5 9B |
| 17 | 2026-07-26 | qwen3-14b | T2: Razonamiento Monty Hall (max_tokens=1024) | ❌ Content vacío, finish=length, 83s | E2: También es reasoning model. Necesita max_tokens >= 2048 |
| 18 | 2026-07-26 | qwen3-14b | T3: JSON recetas (max_tokens=1024) | ✅ JSON válido, 37s | E1: JSON funciona con prompts simples |
| 19 | 2026-07-26 | qwen3-14b | T4: Código Python CSV (max_tokens=1024) | ⚠️ Contenido pero finish=length, 82s | E2: Necesita más tokens para código completo |
| 20 | 2026-07-26 | qwen3-14b | T5: Microrrelato (max_tokens=1024) | ✅ Texto creativo, 25s | E1: Creatividad funciona bien |
| 21 | 2026-07-26 | deepseek-r1-distill-qwen-14b | T1: Conocimiento SQL (max_tokens=2048) | ✅ Respuesta completa, 21s | E1: Con max_tokens=2048 funciona perfecto |
| 22 | 2026-07-26 | deepseek-r1-distill-qwen-14b | T2: Razonamiento Monty Hall (max_tokens=2048) | ✅ Resuelve paso a paso, 90s | E3: DeepSeek R1 = Pensador del laboratorio. 5/5 tests con stop. |
| 23 | 2026-07-26 | deepseek-r1-distill-qwen-14b | T3: JSON recetas (max_tokens=2048) | ✅ JSON impecable, 47s | E1: JSON estructurado sin errores |
| 24 | 2026-07-26 | deepseek-r1-distill-qwen-14b | T4: Código Python CSV (max_tokens=2048) | ✅ Código completo con type hints, 106s | E1: Código de calidad, lento pero fiable |
| 25 | 2026-07-26 | deepseek-r1-distill-qwen-14b | T5: Microrrelato (max_tokens=2048) | ✅ Creativo, 36s | E1: Consistente en todas las tareas |
| 26 | 2026-07-26 | glm-4.6v-flash | T1: Conocimiento SQL (max_tokens=2048) | ✅ Contenido visible, 33s | E1: Con max_tokens=2048 mejora drásticamente vs ronda 1 |
| 27 | 2026-07-26 | glm-4.6v-flash | T2: Razonamiento Monty Hall (max_tokens=2048) | ✅ Resuelve, 73s | E2: GLM funciona con prompts atómicos y max_tokens alto |
| 28 | 2026-07-26 | glm-4.6v-flash | T3: JSON recetas (max_tokens=2048) | ✅ JSON válido, 21s | E1: JSON es su punto fuerte |
| 29 | 2026-07-26 | glm-4.6v-flash | T4: Código Python CSV (max_tokens=2048) | ⚠️ Contenido pero finish=length, 80s | E2: Código no es su especialidad |
| 30 | 2026-07-26 | glm-4.6v-flash | T5: Microrrelato (max_tokens=2048) | ✅ Texto creativo, 50s | E1: Creatividad OK con tokens suficientes |
| 31 | 2026-07-26 | gemma-4-12b-qat | T1: Conocimiento SQL (max_tokens=2048) | ✅ Respuesta completa, 35s | E1: Fiable, lento |
| 32 | 2026-07-26 | gemma-4-12b-qat | T2: Razonamiento Monty Hall (max_tokens=2048) | ✅ Resuelve con explicación, 76s | E3: Gemma 4 = Director Creativo. Razonamiento profundo. |
| 33 | 2026-07-26 | gemma-4-12b-qat | T3: JSON recetas (max_tokens=2048) | ✅ JSON válido, 69s | E1: JSON correcto |
| 34 | 2026-07-26 | gemma-4-12b-qat | T4: Código Python CSV (max_tokens=2048) | ✅ 2 versiones: pandas + stdlib, 113s | E2: El mejor para código completo y alternativas |
| 35 | 2026-07-26 | gemma-4-12b-qat | T5: Microrrelato (max_tokens=2048) | ✅ "Era un martes por la mañana cuando el algoritmo decidió preguntarse por qué...", 151s | E1: Creatividad excelente, el más lento |

---

## Anti-patrones confirmados (extraídos de la comparativa)

| Anti-patrón | Modelos afectados | Evidencia |
|---|---|---|
| max_tokens < 2048 con reasoning models | Qwen 3.5, Qwen3 14B, Gemma 4, DeepSeek R1, GLM 4.6V | Tests 11-15, 17, 19: content vacío con 1024 tokens |
| Prompt multi-instrucción a GLM | GLM 4.6V Flash | Descubierto en sesión visión: prompt con 7 preguntas → vacío; 7 prompts individuales → OK |
| Esperar texto de Llama 3.1 Instruct | Llama 3.1 Instruct 8B | Tests 6-10: siempre responde con function calls |
| Usar Qwen 3.5 9B para cualquier tarea | Qwen 3.5 9B | Tests 11-15: 0/5 útiles. Descartado. |

---

## Patrones validados (E3)

| Patrón | Modelos | Regla |
|---|---|---|
| max_tokens >= 2048 para reasoning models | DeepSeek R1, Gemma 4, GLM 4.6V | 400 mínimo para "hola", 2048 para trabajo real |
| Prompt atómico para GLM | GLM 4.6V Flash | Una instrucción por prompt. Dividir tareas complejas. |
| Function calling nativo en Llama 3.1 | Llama 3.1 Instruct | Usarlo como backend de agentes, no como chat directo |
| Qwen 3.5 9B descartado | Qwen 3.5 9B | No usar. No se ha encontrado configuración que funcione. |

---

*Última actualización: 2026-07-26 — Comparativa de 7 modelos, 35 experimentos*
