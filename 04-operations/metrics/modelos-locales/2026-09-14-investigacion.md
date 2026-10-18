---
title: "Investigación semanal de modelos locales — 2026-09-14"
type: operations
---

# Investigación semanal de modelos locales — 2026-09-14

**Hardware objetivo:** RTX A2000 12GB VRAM (PCIe 3.0). **Inventario actual:** R1-Distill-14B (razonamiento/grounding), GLM-4.6V-Flash (visión), LFM2.5-2.6B (tool calling), granite-4.1-8b (JSON), dolphin3.0-8b (chat), gemma-4-12B-QAT (redacción), qwen3.6-35b-a3b_moe (veracidad), gpt-oss-20b (delegación/razonamiento rápido).

## PASO 0 / 0b (historial del lab) — ejecutado antes de los veredictos

- `grep -ril -E "granite-4\.2|ministral|bonsai|qwen3\.8" 01-knowledge/experiments/ 01-knowledge/objects/` → **0 coincidencias**: ninguno de los candidatos de este informe tiene EXP ni RULE/DEC propia.
- `01-knowledge/modelos_por_tarea.yaml`: `veracidad_critica → qwen3.6-35b-a3b_moe` (evidencia 06-sep: 0/77 alucinaciones, honestidad 100%). Está **EN USO**; no se lista como descartado (JL-006, corrección del desfase 07-sep).
- `04-operations/metrics/alucinaciones_ledger.jsonl` (últimas 3 entradas, 06-sep): qwen3.6-35b-a3b_moe, tasa_alucinacion_global 0.0 y tasa_honestidad 1.0 en seeds 42, 43 y 44 → confirma el YAML.
- Modelos en disco (`/mnt/ssd_ia_datos/LM STUDIO/lmstudio-community/`): solo 6 carpetas (R1-Distill-Qwen-14B, GLM-4.6V-Flash, LFM2.5-2.6B, LFM2.5-VL-3B, gemma-4-12B-it-QAT, gpt-oss-20b). Candidatos de este informe: **no descargados**.
- Informes previos revisados: 2026-08-24 y 2026-09-07 (arrastres: granite-4.2-8b y Ministral 3 14B seguían sin probar).

## Fuentes consultadas (14-sep-2026)

- https://mindpattern.ai/e/qwen3-6-27b · https://theneuralfeed.com/article/release-sota-ggufs-for-qwen3-8-27b-gsq-rco-at-2-5-to-3-0-bpw/lHsXQq6u · https://www.mindstudio.ai/blog/qwen3-8-27b-gsq-rco-quantization · https://mindpattern.ai/e/gguf (trail GGUF; tamaño de GLM-5.3-Flash y auditoría de quants mal etiquetados)
- https://www.reddit.com/r/LocalLLaMA/comments/1v1ya97/ (Terminal-Bench 2.0: Bonsai vs qwen3.5-9b y qwen3.6-35b-a3b) · https://wavect.io/blog/bonsai-27b-phone-local-ai-review/ · https://kenhuangus.substack.com/p/inside-the-1-bit-llm-how-bonsai-fits · https://prismml.com (vía las anteriores)
- https://ollama.com/ibm/granite4.2:8b-q4_K_M/blobs/4730224a8cb6 (blob 5.3GB, 40 capas, 131072 ctx) · https://github.com/ibm-granite/gguf (soporte llama.cpp b9850, Apache 2.0)
- https://huggingface.co/bartowski/mistralai_Ministral-3-14B-Instruct-2512-GGUF (Q4_K_M 8.24GB) · https://lmstudio.ai/models (Ministral 3 3B/8B/14B en catálogo) · https://unsloth.ai/docs/models/tutorials/ministral-3
- https://lmstudio.ai/changelog/lmstudio (09-sep-2026: speculative decoding con visión, drafters DSpark/DFlash) · https://www.promptquorum.com/local-llms/local-llm-model-updates-2026

## Tabla de candidatos (ctx 8K; VRAM = estimación, ningún candidato medido en la A2000)

| Candidato | Tamaño GGUF real | VRAM est. (8K) | tok/s est. A2000 | Calidad | Veredicto |
|---|---|---|---|---|---|
| **granite-4.2-8b** (IBM, Apache 2.0) | **5.3GB** Q4_K_M (blob Ollama verificado; 131072 ctx) | ~6.5-7.5GB | no publicado (no medido en A2000) | harness agente 8/10 (simonpcouch 02-sep); tool calling RL; JSON estructurado | **PROBAR** (pendiente 07-sep) |
| **Qwen3.8-27B GSQ-RCO** (ISTA-DASLab, cuantización nueva) | **8.4 / 9.3 / 10.1GB** (2.50 / 2.75 / 3.00 bpw) + mmproj visión | ~10-11GB con 2.75bpw + KV híbrida | no publicado | *auto-reportado por los autores*: AIME25 100.00 (= BF16), GPQA-D 88.89 vs 89.90, LiveCodeBench 84.57 vs 85.71 | **RE-PROBAR** (motivo fuerte: config distinta) |
| **Ministral 3 14B Instruct 2512** (Apache 2.0) | Q4_K_M **8.24GB** (bartowski) | ~10-11GB | no publicado A2000 | comparable a Small 3.2 (Mistral, marketing); visión + tools; 262K ctx | **PROBAR** (cola, pendiente 24-ago) |
| Bonsai-27B (PrismML, base Qwen3.6-27B) | 1-bit **3.9GB** / ternario **7.59GB** (g64 mainline) | cabe holgado | no publicado A2000 | Terminal-Bench 2.0 (mismo harness): ternario **7.9%** < qwen3.5-9b 9.2% < qwen3.6-35b-a3b **24.3%**; 1-bit no termina el run (14k tokens sin stop) | **DESCARTAR** (calidad) |
| GLM-5.3-Flash (Z.ai, 320B-A18B) | GGUF publicado (beta LM Studio) | **~102GB** RAM+VRAM | n/a | — | DESCARTAR (no cabe) |
| LongCat-Flash-Lite-Sparse (69B-A3B, 1M ctx) | GGUF solo con fork del autor | >35GB | n/a | — | DESCARTAR (no cabe + fork) |

Otros vistos y descartados por tamaño sin más análisis: Qwen3.8-Flash-Next 125B (~75GB RAM), Nemotron 3 Super 120B-A12B, Qwen3.5-122B-A10B, Qwen3-Coder-Next 80B-A3B, Laguna XS 2.1 (33B-A3B, ~20GB Q4), GigaChat3.5-432B-A28B, DeepSeek-V4 (284B), Kimi K3 (2.8T).

## Los 2 que merecen PROBAR

1. **granite-4.2-8b — PROBAR (cierre del pendiente 07-sep).** El informe anterior lo dio por "Q4_K_M ~5GB, no publicado"; ahora está **verificado: 5.3GB** (blob de Ollama `ibm/granite4.2:8b-q4_K_M`, 40 capas, 131072 ctx), familia densa 3B/8B/30B, Apache 2.0, soporte en llama.cpp ≥ b9850 y LM Studio. Es el relevo natural del **granite-4.1-8b que el lab ya usa para JSON**, con tool calling entrenado con RL y razonamiento opcional. Cabe holgado en 12GB. Prueba: batería JSON + tool calling, no solo benchmark de razonamiento.
2. **Qwen3.8-27B GSQ-RCO (2.75bpw, 9.3GB) — RE-PROBAR con motivo fuerte.** El 27B quedó "DESCARTAR (no cabe)" el 07-sep por el Q4_K_M de 17.77GB, **sin EXP** (nunca se probó). Esta cuantización nueva (GSQ + RCO del ISTA-DASLab) publica tres tamaños que **sí caben** (8.4 / 9.3 / 10.1GB) y corre en llama.cpp/Ollama/LM Studio sin parches. Es el único salto real de tamaño (27B denso + visión) que cabe en la tarjeta.
   **Advertencias obligatorias antes de descargar:** (a) los números que igualan o superan a BF16 están **auto-reportados por los autores** de la cuantización y "cuantizar mejor que el base" es señal de cautela; (b) la referencia independiente (quesma, 26-ago, mismo modelo) mide UD-Q2_K_XL 10.7GB con instruction-following estable pero **Terminal-Bench 77% → 72%**, y los quants 1-bit (6.2GB) cayendo a azar en GPQA Diamond; (c) una auditoría de 443 quants GGUF encontró **64 con bpw distinto al del nombre** → verificar bpw real con `llama-gguf` tras descargar; (d) **no sustituye a qwen3.6-35b-a3b en veracidad** (0/77 alucinaciones): candidato para razonamiento/código/visión, no para hechos.

## Correcciones a informes anteriores

- **Bonsai-27B no era "no cabe"** (07-sep): sí cabe (3.9GB 1-bit / 7.59GB ternario g64 en llama.cpp mainline). Se descarta igualmente, pero **por calidad medida**, no por tamaño: en Terminal-Bench 2.0 queda por debajo de qwen3.5-9b, que el lab ya descartó en EXP-20260726-001.
- **Qwen3.8-27B deja de estar "descartado por tamaño"**: pasa a RE-PROBAR por la nueva familia de quants GSQ-RCO.
- Se mantiene **qwen3.6-35b-a3b_moe EN USO** (veracidad_critica, 0/77 alucinaciones): la lista histórica de descartados no lo rehabilita ni lo degrada; manda el YAML + ledger (JL-006).

## Recordatorio

Ningún candidato se incorpora sin pasar las pruebas del lab: `benchmark-razonamiento.py` + batería exigente (JSON/tool calling para granite-4.2; golden set de alucinaciones si se plantea tocar veracidad). **JL-006: la evidencia del laboratorio prevalece sobre la web.** Este informe no descarga ni carga modelos.

---

> **Corrección verificada (14-sep, tras ejecutar la prueba):** `benchmark-razonamiento.py`
> **no existe** en el lab. Los instrumentos reales son `tools/evaluar_alucinaciones.py`
> (golden set de 27 preguntas, 6 categorías) y la batería nueva
> `tools/evaluar_json_tool_calling.py` + `tools/bateria_json_tool_calling.json` (8 casos).
> Resultado de granite-4.2-8b en `2026-09-14-prueba-granite-4.2-8b.md`.
