# Análisis: mejor modelo local para OpenCode (agente de coding) en RTX A2000 12GB
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 2026-09-03
**Origen:** prueba real opencode+ollama/r1-14b (24 min sin completar un smoke) → investigación del estado del arte para la tarea "agente de coding local" en la A2000.
**Método:** fuentes externas (insiderllm guía tiers VRAM 2026; arXiv 2604.00362 "In harmony with gpt-oss"; rapidmlx benchmark MLX; theaibench use-case agents; TheFocus.AI "Which Open Model Should You Actually Run Locally") + tamaños GGUF reales en disco + ficha local models-reference.md (ai-router).
**VERACIDAD: [VERIFICADO]** (datos de fuentes citadas + disco local)

## Restricción de hardware (medida real)
- RTX A2000 12 GB (12282 MB). Con GLM cargado quedan ~880 MB; liberado (wrapper opencode-local.sh) ~11.7 GB.
- Un agente tipo OpenCode necesita: pesos + KV cache de contexto largo (8-16k mínimo) + overhead runtime. En la práctica: pesos GGUF ≤ ~9-10 GB.

## Modelos locales descargados (tamaño GGUF real en disco)
| Modelo | GGUF | Tamaño | ¿Cabe? |
|---|---|---|---|
| gpt-oss-20b | MXFP4 | 12 GB | ❌ No (12 GB solo pesos; paper: 16 GB mínimo para uso agente) |
| DeepSeek-R1-Distill-Qwen-14B | Q4_K_M | 8.4 GB | ✅ pesos, ❌ usable (razonamiento interminable; no coder/tool-calling) |
| gemma-4-12B-it-QAT | Q4_0 | 6.5 GB | ✅ (tool-calling es su punto débil, 20/25 en la 26B) |
| GLM-4.6V-Flash | Q4_K_M | 5.8 GB | ✅ (VLM, no coder) |

## Estado del arte 2026 para agentes de coding locales (fuentes)
- **La frontera agentic local está en 16-24 GB**: Qwen3-Coder-30B-A3B (entrenado para agentic), Devstral Small 2 24B (para Cline/OpenHands), Qwen 3.6-27B (~17 GB Q4, 77.2% SWE-bench V), gemma-4-26b-a4b (~15-16 GB, 95% en 4 min). NINGUNO cabe en 12 GB.
- **Tier 6-12 GB explícito** (theaibench): "Not for autonomous agent loops" — modelos <14B para tool calling simple, no loops.
- **<20B no se auto-corrige** (TheFocus, experimento 4B: 0 mejoras en 8 retries con error devuelto). Para loops iterativos de código: ≥20B con thinking, o cloud.
- **gpt-oss-20b**: tool calling 0/25 con thinking OFF, 23/25 con thinking ON (TheFocus). Y llama tools de su training distribution aunque no estén definidas (apply_patch 860× — arXiv). Necesita formato nativo harmony (SUPPORTS_NATIVE_TOOL_FORMAT; rapidmlx: 17%→80% con el flag). En 12 GB descartado igualmente (12 GB pesos + KV).
- **Qwen 2.5-Coder 14B** (~9 GB): el mejor código single-shot que cabe en 12 GB; las guías lo ponen para tab-complete/chat, NO para agent loops.

## Veredicto
Para la RTX A2000 12 GB NO existe hoy un modelo local que dé un agente de coding (OpenCode) fiable en loops multi-archivo. Los modelos del tier que caben (<14B) fallan en tool-calling encadenado y auto-corrección iterativa (evidencia externa + prueba real r1-14b de hoy).

Opciones ordenadas:
1. **OpenCode con deepseek-v4-flash (cloud)** — validado hoy: creó script+tests en segundos; ~0.00046 USD/consulta off-peak. Es la vía pragmática (y lo que el lab ya usa).
2. **Local para coding acotado**: qwen2.5-coder:14b (~9 GB, pull a Ollama, num_ctx 16k NO 64k) — mejor código single-shot que cabe. Aceptar degradación en loops largos. Candidato a probar cuando se quiera (descarga ~9 GB).
3. **Descargados que NO valen para esto**: r1-14b (descartado hoy), gpt-oss-20b (no cabe agente en 12 GB; sí como motor batch con thinking), gemma-4-12B (tool-calling débil), GLM (VLM).
4. Nota: ficha models-reference.md del lab está DESACTUALIZADA (lista granite-4.1-8b y llama31-8b-64k que NO están descargados hoy; ollama solo tiene r1-14b).

## Referencia futura (señal: si algún día hay GPU ≥16 GB)
gpt-oss-20b (ya descargado, con thinking ON y formato harmony), Qwen3-Coder-30B-A3B, Devstral Small 2 24B, Qwen 3.6-27B, gemma-4-26b-a4b. En ese momento re-evaluar opencode local en serio.
