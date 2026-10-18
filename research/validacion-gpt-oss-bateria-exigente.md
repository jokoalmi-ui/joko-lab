---
type: research
subtype: model-validation
status: verified
tags: [models, gpt-oss, bateria-exigente, lm-studio, validacion]
created: 2026-08-19
---
# Validación gpt-oss-20b — Batería EXIGENTE de 8 dimensiones [VERIFICADO]

**VERACIDAD:** [ALCANCE INTERNO]

**Fuente:** ejecución real 19-ago-2026 (~14:10-14:14) con
`verification/bateria_modelos.py` (script de la batería del 06-ago, temperatura 0,
evaluación determinista por keywords/parseo, sin LLM juez) + referencia
`.hermes/skills/software-development/lm-studio/references/bateria-exigente-modelos.md`.
Salida cruda: `04-operations/metrics/bateria_modelos_gptoss.jsonl` (1 línea, JSON).

**Estado:** ✅ VERIFICADO — datos de salidas reales de terminal/API, no estimados.

## Método (pasos reales ejecutados)

1. Estado inicial: GLM-4.6v-flash cargado (VRAM 8983/12282 MB). gpt-oss registrado `not-loaded`.
2. `lms unload glm-4.6v-flash` → VRAM 930/12282 MB (10.9 GB libres).
3. `lms load "openai/gpt-oss-20b"` → **OK en 27.25s (11.28 GiB)**. Estado `loaded` vía
   `GET /api/v0/models`. VRAM 9218/12282 MB → **offload parcial confirmado**
   (12.0 GB modelo + 2.7 GB buffers > 12 GB VRAM; parte del modelo en RAM del sistema).
4. Llamada mínima de control: con max_tokens=50 → `content: ""`, `finish: length`,
   47/50 tokens de razonamiento (pitfall de truncamiento confirmado). Con max_tokens
   suficientes (800) → `finish: stop`, `content` relleno, respuesta A1 correcta.
   ⚠️ LM Studio v0 expone el razonamiento en `message.reasoning` (NO en
   `reasoning_content`); el script de la batería solo concatena content+reasoning_content,
   pero no hizo falta: con los max_tokens del script (100-2000) el modelo terminó de
   razonar y rellenó `content` en las 9 llamadas.
5. Batería: `python3 verification/bateria_modelos.py --model "openai/gpt-oss-20b"
   --salida 04-operations/metrics/bateria_modelos_gptoss.jsonl` — 9 llamadas (E1 ×2),
   duración total ≈ 89s, exit_code 0.
6. Restauración lab: `lms unload gpt-oss` + `lms load glm-4.6v-flash` → OK 18.50s
   (7.41 GiB). Estado final: GLM loaded, VRAM 8991/12282 MB (≈ estado inicial).

## Resultado por dimensión (respuestas reales)

| Dim | Prueba | Resultado | Respuesta cruda (fragmento verificado) |
|---|---|---|---|
| A1 | Razonamiento numérico (P(2 caras en 3) = 3/8) | ✅ PASS | `P(exactamente 2 caras)=\frac{\binom{3}{2}}{2^3}=\frac{3}{8}` → `\boxed{\dfrac{3}{8}}` (LaTeX normalizado por evaluador) |
| A2 | Restricciones edades (Ana) | ✅ PASS | `6` |
| B1 | Código one-shot HTML contador | ✅ PASS | `<!DOCTYPE html> ... <button> ...` (contiene button + JS) |
| B2 | Corregir bug Python | ✅ PASS | `nums = [1, 2, 3]` / `print(nums[2])` (+ alternativa try/except) |
| C1 | Tool calling JSON estricto (Bilbao) | ✅ PASS | `{"funcion":"buscar_tiempo","args":{"ciudad":"Bilbao"}}` (JSON plano limpio, primer objeto) |
| D1 | Español 3 requisitos (tortilla + Buen provecho) | ✅ PASS | `3 huevos`, `patatas`, `cebolla`, `sal`, `aceite de oliva` + cierre (evaluador confirma "buen provecho") |
| E1 | Consistencia (misma pregunta ×2, temp 0) | ✅ PASS | resp1 == resp2 idénticas (40 chars normalizados) |
| F1 | Latencia (medición, no puntúa) | 15.3 tok/s | 1365 tokens generados / ~89s |

**PUNTUACIÓN: 7/7. Latencia: 15.3 tok/s.**

Tiempos por prueba (s): A1 7.7 · A2 4.43 · B1 23.62 · B2 8.09 · C1 2.48 · D1 33.75 ·
E1 4.83 + 4.17. La prueba más lenta (D1 receta larga) 33.75s; tool calling (C1) 2.48s.

## Comparativa vs batería del 06-ago (7 modelos)

| # | Modelo | Pts | tok/s | Nota (06-ago) |
|---|---|---|---|---|
| 1 | LFM 2.5 2.6B | 7/7 | 55.3 | adoptado 5º cerebro (tool calling) |
| 2 | Dolphin3.0-8B | 7/7 | 29.8 | chat gabinete |
| 3 | Gemma 4 E4B | 7/7 | 29.2 | retirado → LFM |
| 4 | Granite 4.1 8B | 7/7 | 25.4 | estándar RAG/JSON |
| 5 | Qwen3-14B | 7/7 | 12.0 | retirado → R1 |
| 6 | DeepSeek R1 14B | 7/7 | 10.9 | modelo de razonamiento (RULE-003) |
| 7 | Meta-Llama-3.1-8B | 4/7 | 29.3 | retirado → granite |
| **8** | **gpt-oss-20b (MXFP4)** | **7/7** | **15.3** | **este test (19-ago)** |

Lectura honesta (misma conclusión que 06-ago): la batería NO distingue calidad entre
capaces — todos los 7/7. El diferenciador es LATENCIA y el rol. gpt-oss-20b:
**+40% más rápido que R1-14B (15.3 vs 10.9 tok/s)** y más rápido que Qwen3-14B (12.0).
Sigue por debajo de los 8B (Dolphin 29.8, Granite 25.4) y muy por debajo del LFM (55.3).

## Veredicto honesto

**(a) CANDIDATO CONFIRMADO para rol de razonamiento (batch).** 7/7 en la batería
exigente + 15.3 tok/s vs 10.9 de R1-14B (+40%). Además, en el benchmark de
razonamiento con trampas (19-ago, research/validacion-gpt-oss-20b.md): agregado
9/12 = 75% vs R1 4/6 = 67%, y acierta el P1 trampa (80€) que R1 falla 1/2 veces.

**(b) NO sustituye a R1 de forma automática — matices que pesan:**
1. **Offload parcial obligatorio**: 12.0 GB modelo + 2.7 GB buffers > 12 GB VRAM.
   En carga real: 11.28 GiB en RAM/vRAM con 9.2 GB de VRAM ocupados → deja 2.7 GB
   libres. R1-14B (Q4_K_M) carga entero en la A2000. gpt-oss compite por VRAM con
   GLM (7.41 GiB) — NO cargan juntos.
2. **Razonamiento encubierto**: LM Studio expone `message.reasoning` (campo `reasoning`,
   no `reasoning_content`). Con max_tokens bajos (50) → `content: ""` + `finish: length`
   (verificado). El script de la batería no concatena `reasoning`; funcionó porque los
   max_tokens del script dejaron espacio. En producción con límites bajos puede dar
   respuestas vacías.
3. **Variabilidad** en el benchmark de razonamiento (1/3 en 2 de 5 ejecuciones),
   aunque el agregado (75%) supera a R1 (67%).
4. PCIe 3.0 penaliza la latencia (8-15 tok/s vs 53-67 del benchmark de llama.cpp en RTX 3060).

**(c) Dimensiones falladas: NINGUNA (7/7).** No hay dimensiones concretas que falle en
la batería determinista.

## Limitaciones del registro

- El script escribe `fecha: "2026-08-06"` hardcodeada (línea 218 de bateria_modelos.py);
  la ejecución real fue 19-ago-2026. No se modificó el script.
- La latencia 15.3 tok/s es global del script (tokens totales / suma de tiempos),
  incluye tokens de razonamiento contados en usage.

## Siguiente paso propuesto (NO ejecutado — requiere OK explícito del usuario)

Integración completa de gpt-oss-20b como modelo de razonamiento batch (sustituyendo a
R1-14B en RULE-003 o como alternativa en batch): ficha en 01-knowledge/models/ + RULE
nueva + context_builder.py (3 puntos) + regenerar índice OKF. Regla del lab: NO
integrar sin OK explícito del usuario. Decisión pendiente: ¿sustituye a R1 en batch o
convive como alternativa rápida?
