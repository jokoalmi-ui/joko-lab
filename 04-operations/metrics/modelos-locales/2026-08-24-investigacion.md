---
title: "Investigación semanal de modelos locales — 2026-08-24"
type: operations
---

# Investigación semanal de modelos locales — 2026-08-24

**Hardware objetivo:** RTX A2000 12GB VRAM (PCIe 3.0) · **Inventario actual:** R1-Distill-14B (razonamiento), GLM-4.6V-Flash (visión), LFM2.5-2.6B (tool calling), granite-4.1-8b (JSON), dolphin3.0-8b (chat), gemma-4-12B (creatividad).

## Fuentes consultadas
- artificialanalysis.ai/models/qwen3-5-9b
- huggingface.co/lmstudio-community/Qwen3.5-9B-GGUF
- huggingface.co/mistralai/Ministral-3-14B-Reasoning-2512-GGUF
- willitrunai.com/models/ministral-3-14b · llm-bench.io/models/ministral-3-14b
- huggingface.co/JetBrains/Mellum2-12B-A2.5B-Instruct-GGUF-Q4_K_M · recipes.vllm.ai/JetBrains/Mellum2-12B-A2.5B-Thinking
- reddit.com/r/LocalLLaMA/comments/1tukilx (Mellum2 open source)
- unsloth.ai/docs/models/deepseek-v4 · runlocalai.co/models/deepseek-v4
- willitrunai.com/blog/qwen-35-vram-requirements-complete-guide · lmstudio.ai/models/qwen/qwen3.5-9b
- local-ai-models.ai (cheat sheet, actualizado 20-ago-2026) · promptquorum.com/local-llms

## Tabla de candidatos

| Candidato | Tamaño GGUF | VRAM estimada (ctx 8K) | tok/s estimado | Calidad | Veredicto |
|---|---|---|---|---|---|
| Qwen 3.5 9B (Alibaba, abr-2026) | Q4_K_M ~5.5GB (lmstudio-community ✓) | ~6-7GB total | no publicado A2000; estimado 35-50 (denso 9B Q4) | AA I-I **22** (mediana 9); MMLU-Pro 82.5; multimodal | **PROBAR** |
| Ministral 3 14B Reasoning (Mistral, dic-2025) | Q4_K_M ~8.5GB (GGUF oficial ✓) | ~10-11GB total | no publicado A2000; media comunitaria 43 (llm-bench.io) | Mistral: comparable a Small 3.2 24B; AA no publicado | **PROBAR** |
| Mellum2-12B-A2.5B (JetBrains, jun-2026) | Q4_K_M ~7.5GB (GGUF oficial ✓) | ~8-9GB total | no publicado A2000; estimado 40-70 (2.5B activos) | LiveCodeBench v6 69.9; AIME 58.4 (Thinking) | OBSERVAR |
| DeepSeek V4 Flash/Pro | no hay GGUF viable; mínima build UD-IQ1_S 82.5GB RAM | >82GB RAM total | n/a | frontier MoE 745B/38B activos | DESCARTAR (no cabe) |
| Qwen 3.6 27B / 35B-A3B | 27B Q4 ~16.5GB; 35B-A3B ya probado | no cabe / ya descartado (~10 tok/s) | — | — | DESCARTAR (sin versión <27B oficial) |

## Por qué PROBAR (2 candidatos)

1. **Qwen 3.5 9B — PROBAR.** Es el mejor "denso pequeño" del momento: AA I-I 22 ≈ clase del R1-14B con la mitad de peso, GGUF oficial en LM Studio (lmstudio-community/Qwen3.5-9B-GGUF) y Ollama, cabe holgado (6-7GB a 8K). Puede reemplazar a granite-4.1-8b (JSON) y dolphin3.0-8b (chat rápido) con margen, y servir de chat/agente veloz; además trae visión ligera que podría complementar a GLM-4.6V-Flash. Es el candidato más polivalente de la semana.
2. **Ministral 3 14B Reasoning — PROBAR.** Rival directo del R1-14B en el rol de razonamiento: 14B denso Q4 (~8.5GB), GGUF oficial de Mistral, con visión incluida y 43 tok/s de media comunitaria. Si supera a R1-14B en benchmark-razonamiento.py, releva al actual en ese rol. Nota: es de dic-2025 (no es novedad de esta semana, pero el lab no lo ha probado).

## Por qué OBSERVAR

- **Mellum2-12B-A2.5B:** Apache 2.0, MoE 12B/2.5B activos, GGUF oficial. Fuera de serie en código (LiveCodeBench 69.9). El lab no tiene rol de "código/agente"; si se decide crear uno (n8n/automatización), es el mejor candidato de la semana. Falta madurar fuera de código.

## Descartados con motivo

- **DeepSeek V4:** 745B totales/38B activos; la build más pequeña (UD-IQ1_S) pide 82.5GB RAM. Ni con offload parcial en PCIe 3.0.
- **Qwen 3.6:** solo abrió 27B denso (~16.5GB Q4) y 35B-A3B (ya descartado por el lab, ~10 tok/s). No hay Qwen 3.6 pequeño oficial; los GGUFs "14B-A3B" comunitarios no son lanzamientos validados.
- **Llama 4 Scout, gemma4-26b-a4b, qwen3.6-35b-a3b, kimi-cat3, mistral-nemo, llama4-scout:** ya descartados con pruebas reales; sin novedad que los rehabilite.

## Recordatorio

Ningún candidato se incorpora sin pasar las pruebas del lab: `benchmark-razonamiento.py` + batería exigente. **JL-006: la evidencia del laboratorio prevalece.** Esta semana no se descarga ni se carga nada; solo investigación.
