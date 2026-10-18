---
title: "Informe — Batería de pruebas exigentes a modelos locales"
type: operations
---

# Informe — Batería de pruebas exigentes a modelos locales

**Fecha:** 06-ago-2026
**Método:** 7 modelos × 8 dimensiones, temperature 0, endpoint LM Studio, evaluación determinista (keywords/parseo, sin LLM juez)
**Script:** verification/bateria_modelos.py | Resultados: 04-operations/metrics/bateria_modelos.jsonl

---

## Ranking final

| # | Modelo | Pts | Latencia (tok/s) | Fallos |
|---|---|---|---|---|
| 1 | **lfm2.5-2.6b** (2.7B, 1.67 GB) | 7/7 | **55.3** | — |
| 2 | dolphin3.0-llama3.1-8b (8B) | 7/7 | 29.8 | — |
| 3 | google/gemma-4-e4b (2B) | 7/7 | 29.2 | — |
| 4 | granite-4.1-8b (8B) | 7/7 | 25.4 | — |
| 5 | qwen3-14b (14B) | 7/7 | 12.0 | — |
| 6 | deepseek-r1-distill-qwen-14b (14B) | 7/7 | 10.9 | — |
| 7 | meta-llama-3.1-8b-instruct (8B) | 4/7 | 29.3 | A1 razonamiento, A2 restricciones, B2 corregir bug |

Seis modelos perfectos (7/7). La batería de 8 dimensiones NO distingue entre los 6 mejores — son todos capaces en estas pruebas. El diferenciador real es LATENCIA (y VRAM/tamaño).

## Dimensiones que fallaron (detalle)

- **meta-llama-3.1-8b**: responde en formato de tool calling nativo incluso a preguntas de razonamiento ({"name": "probabilidad", ...}) — no resuelve A1/A2/B2 como texto. Es un comportamiento real del modelo para prompts directos.
- Los demás: 0 fallos con el evaluador corregido.

## Correcciones del evaluador durante la batería (documentadas)

1. **reasoning_content**: LFM 2.5 y modelos con razonamiento encubierto devuelven el contenido en `reasoning_content` (content vacío con finish_reason=length). El script concatena ambos.
2. **max_tokens truncaban**: respuestas largas (granite LaTeX, LFM razonando) se cortaban antes del resultado. Subidos a 2000.
3. **LaTeX**: granite escribe \frac{3}{8} — evaluador ampliado para aceptarlo.
4. **Tool calling en 3 formatos**: JSON con fences, JSON plano + razonamiento después, y formato nativo {"name","parameters"} (llama). Evaluador ahora tolera los 3.

## Hallazgos por modelo

| Modelo | Lectura honesta |
|---|---|
| **lfm2.5-2.6b** | El mejor de la batería: perfecto Y el más rápido (55 tok/s, casi 2× el resto). Confirma el estudio de esta mañana: tool calling excelente, razonamiento encubierto, rápido. Cabe en 1.67 GB. |
| dolphin3.0-8b | Sólido y rápido (29.8). El del gabinete de chat — confirmado. |
| gemma-4-e4b | Sólido (29.2). El rival directo del LFM en tamaño — empate en calidad, pierde en latencia. |
| granite-4.1-8b | Confirmado (25.4). El estándar del lab para JSON/RAG — sigue siendo válido. |
| qwen3-14b / deepseek-r1-14b | Perfectos pero MUY lentos (10-12 tok/s): el razonamiento encubierto de los 14B cuesta 5× la latencia del LFM. |
| llama-3.1-8b | El peor: formato tool-call nativo rompe el uso conversacional directo. No recomendado para chat sin adaptador. |

## Recomendación

1. **ADOPTAR lfm2.5-2.6b como 5º cerebro** (tool calling / tareas agénticas ligeras) — el estudio de esta mañana lo proponía como candidato; la batería lo confirma con datos: perfecto en 8 dimensiones y el doble de rápido que el resto.
2. **No tocar granite** (sigue siendo el estándar RAG/JSON del lab).
3. Los 14B (qwen, deepseek) quedan descartados para tareas interactivas por latencia (12/11 tok/s) — solo si se necesita su calidad de razonamiento sin prisa.
4. llama-3.1-8b: no usarlo para chat directo sin adaptador de tool calls.

## Coste

- Descarga LFM: 1.67 GB (Q4_K_M) — 208 GB libres, sin problema
- VRAM: A2000 gestionada por el orquestador (unload/load automático)
- Tiempo total batería: ~20 min (7 modelos + re-runs)

## Verificación

- Script bateria_modelos.py: verificado 14/14 PASS ad-hoc (evaluadores aislados) + 6/6 PASS (fix C1) — logs en /tmp/hermes-verify-*
- Resultados en 04-operations/metrics/bateria_modelos.jsonl (7 filas, JSON válido)
