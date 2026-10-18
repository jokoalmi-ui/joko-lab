---
title: "Investigación semanal de modelos locales — 2026-09-07"
type: operations
---

# Investigación semanal de modelos locales — 2026-09-07

**Hardware objetivo:** RTX A2000 12GB VRAM (PCIe 3.0) · **Inventario actual:** R1-Distill-14B (razonamiento), GLM-4.6V-Flash (visión), LFM2.5-2.6B (tool calling), granite-4.1-8b (JSON), dolphin3.0-8b (chat), gemma-4-12B (creatividad). +gpt-oss-20b (delegación, 6/6 reales 04-sep).

**PASO 0 (historial del lab):** cruzado contra EXP-20260726-001 (qwen3.5-9b = 0/5, EL PEOR de 7; qwen3-14b 3/5; r1-14b, gemma-4-12b, dolphin, llama-3.1-8b = 5/5), EXP-20260728-002/003, EXP-20260729-004, EXP-20260730-005, EXP-20260804 y ficha de 11 modelos en 01-knowledge/models/. Modelos en disco (LM STUDIO/lmstudio-community/): solo los 6 del inventario + gpt-oss-20b → **granite-4.2, Ministral 3 y Ornith NO están probados por el lab**.

## Fuentes consultadas
- dev.to/klukyanov/the-local-llm-weight-classes-september-2026-what-actually-fits-on-your-machine-128d (06-sep-2026)
- lmmarketcap.com/llm-updates (ago-2026) · huggingface.co/lmstudio-community (recientes)
- byteiota.com/ibm-granite-4-2-free-local-reasoning-models-worth-it · courionai.com/news/2026-08-28-ibm-granite-4-2-open-models · simonpcouch.com/blog/2026-09-02-local-agents-3
- huggingface.co/ornith-ai/Ornith-1.5-9B-GGUF · huggingface.co/AtomicChat/Ornith-1.5-9B-GGUF · atomic.chat/blog/guides/how-to-run-ornith-1-5-locally
- willitrunai.com/blog/mistral-small-4-vram-requirements · pulsemark.ai/run-nemotron-3-5-lightning-locally · canitrun.dev/models/nemotron-3.5-lightning-30b-a3b · runaihome.com/blog/nemotron-35-lightning-consumer-gpu-hardware-guide-2026
- huggingface.co/Distillio/Qwen3.8-27B-GGUF · huggingface.co/lmstudio-community/Qwen3.8-27B-GGUF
- github.com/wiltodelta/small-llm-testing (Ministral 3 14B Q4_K_M ~8.2GB) · Artificial Analysis (vía runaihome, I-I 24 Nemotron)

## Tabla de candidatos (ctx 8K; GGUF no verificado en disco del lab)

| Candidato | Tamaño GGUF | VRAM est. | tok/s est. | Calidad | Veredicto |
|---|---|---|---|---|---|
| granite-4.2-8b (IBM, 25-ago-2026, Apache 2.0) | Q4_K_M ~5GB (no publicado en fuentes; Ollama granite4.2:8b ✓, LM Studio ✓) | ~6-7GB | no publicado A2000 (32 tok/s tercero, hw no A2000) | agente 8/10 = GPT-4.1 (harness simonpcouch 02-sep); razonamiento+RL agente; 128K ctx | **PROBAR** |
| Ministral 3 14B Reasoning (dic-2025, Apache 2.0) | Q4_K_M ~8.2GB (GGUF oficial ✓) | ~10-11GB | no publicado A2000; media comunitaria ~43 | comparable a Small 3.2 24B (Mistral); visión | **PROBAR** (pendiente 24-ago) |
| Ornith 1.5 9B (DeepReinforce, 19-ago, MIT) | Q4_K_M 5.63GB (AtomicChat ✓) | ~7GB (KV híbrida: ~32KB/tok → 8K ≈ 0.26GB) | no publicado | agente 6/10 (simonpcouch); visión+thinking; 262K ctx | OBSERVAR |
| LFM2.5-8B-A1B (Liquid) | Q8 ~9GB / Q4 ~5GB (sin verificación directa) | ~6GB Q4 | no publicado | sin benchmarks publicados en fuentes consultadas | OBSERVAR |
| Nemotron 3.5 Lightning 30B-A3B (11-ago, OpenMDW) | Q4_K_M 18.3-25GB (fuentes discrepan) | ≥20.5GB → NO cabe | n/a (offload PCIe3 inviable) | AA I-I 24; por debajo de qwen3.6-35b en 13/14 tests | DESCARTAR (no cabe) |
| Qwen3.8-27B (14-ago, Apache 2.0) | Q4_K_M 17.77GB (GGUF lmstudio-community ✓) | ~19GB → NO cabe | n/a | BenchLM 68.4; VLM denso; solo 27B abierto, sin <14B | DESCARTAR (no cabe) |
| Mistral Small 4 119B-A6B (16-mar) | Q4_K_M ~72GB | no cabe | n/a | "Small" es marketing (119B) | DESCARTAR (no cabe) |
| qwen3.5-9b | — | — | — | **0/5 en EXP-20260726-001** | **DESCARTAR (corrección)** |

## Por qué PROBAR (2)

1. **granite-4.2-8b — PROBAR (NUEVO esta semana, 25-ago).** Versión nueva del granite-4.1-8b que el lab ya usa para JSON: misma familia densa 8B Apache 2.0, con razonamiento opcional y tool-calling entrenado con RL (8B y 30B). En el harness agente de simonpcouch (02-sep) logra 8/10 y empata con GPT-4.1. Cabe holgado (~6-7GB). Si mantiene la fiabilidad JSON de 4.1 y mejora tool calling, releva al actual en ese rol. **Motivo de re-prueba válido: versión nueva, no probada por el lab.**
2. **Ministral 3 14B Reasoning — PROBAR (pendiente desde informe 24-ago).** Sigue sin ficha ni EXP: nadie lo ha probado (verificado en disco). Es el único rival directo del R1-14B en razonamiento (14B denso Q4 ~8.2GB, GGUF oficial Mistral, ~43 tok/s media comunitaria). Si supera benchmark-razonamiento.py, releva al R1-14B.

## Corrección al informe 24-ago
El informe anterior recomendó **PROBAR qwen3.5-9b**, pero el lab YA lo había probado: **0/5 en EXP-20260726-001** (el PEOR de 7). Error de Paso 0 (no cruzó historial). **JL-006: la evidencia del laboratorio prevalece → qwen3.5-9b queda DESCARTADO y no se vuelve a recomendar.**

## Descartados sin novedad
Mistral Small 4 (119B), Nemotron 3.5 Lightning y Qwen3.8-27B no caben; Hy-MT2-30B-A3B (20-ago, Tencent) sin GGUF verificado y ~17GB+ → offload inviable; Muse Glimmer 30B, Bonsai-27B, GLM-4.7-Flash (18.3GB), gemma-4-31B → no caben; Falcon H1R 7B sin benchmarks publicados (MMLU-Pro "—"). Ya descartados con pruebas y sin novedad que los rehabilite: qwen3.6-35b-a3b, gemma4-26b-a4b, kimi-cat3, mistral-nemo, llama4-scout.

## Recordatorio
Ningún candidato se incorpora sin pasar las pruebas del lab: `benchmark-razonamiento.py` + batería exigente (JSON/tool calling para granite-4.2). **JL-006: la evidencia del laboratorio prevalece.** No se descarga ni se carga nada; solo investigación.
