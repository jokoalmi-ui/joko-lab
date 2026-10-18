---
title: "Investigación semanal de modelos locales — 2026-09-28"
type: operations
---

# Investigación semanal de modelos locales — 2026-09-28

**Hardware objetivo:** RTX A2000 12GB VRAM (Ampere). **Ventana de novedad:** 14-sep → 28-sep-2026 (o cambio material en esa ventana).
**Registro/memoria:** `candidatos-modelos-locales.json` (backup previo: `candidatos-modelos-locales.json.bak-2026-09-28-1401`). Ningún candidato ya registrado se re-investiga ni se re-lista.

## PASO 0 — historial del lab (ejecutado antes de cualquier veredicto)

- `grep -rl -E "Qwen-Image|MiMo-V2\.6|Tev1|LensVLM|K2-Horizon|DSpark|V4\.1-Flash"` sobre todo `joko-lab/` → **6 ficheros**, ninguno con un EXP de prueba de estos modelos. Desglose real de coincidencias:
  - `04-operations/metrics/modelos-locales/candidatos-modelos-locales.json` (el propio registro; MiniCPM5-2B menciona "drafter DSpark").
  - `04-operations/metrics/modelos-locales/2026-09-14-investigacion.md` (changelog LM Studio 09-sep: speculative decoding con visión, drafters DSpark/DFlash).
  - `04-operations/backlogs/2026-07-31-backlog.md` y `04-operations/backlogs/pendientes.md`: **DeepSeek-V4.1-Flash es el modelo CLOUD** que el lab ya usa con nombre legacy `deepseek-v4-flash`.
  - `01-knowledge/experiments/EXP-20260916-007-supervision-vs-sesion-directa/f2-A-T1.md` y `f2-par-T1.md`: EXP-007 ficha la tabla de precios oficial y confirma que `deepseek-v4-flash` **se sirve hoy con V4.1-Flash** (el F0 del EXP-006 queda obsoleto).
  - → Conclusión PASO 0: ninguno de los candidatos de hoy tiene EXP de rendimiento propio; **V4.1-Flash sí tiene medición del lab, pero como modelo cloud (EXP-20260916-007)** → su veredicto local es DESCARTAR citando el experimento, nunca PROBAR.
- `01-knowledge/modelos_por_tarea.yaml`: los 10 roles/entradas siguen igual (veracidad→qwen3.6-35b-a3b_moe, visión→glm-4.6v-flash, redacción→gemma-4-12b-qat, grounding→R1-Distill-14B, razonamiento/fallback→gpt-oss-20b, tool_calling→lfm2.5-2.6b). **Ninguno de los candidatos de hoy ocupa un rol hoy vacío**, salvo el de imagen (ver Qwen-Image-2.1).
- `04-operations/metrics/alucinaciones_ledger.jsonl`: no entra ningún modelo nuevo del informe (no hay filas nuevas de modelos candidatos).

## Novedades registradas hoy (7 entradas nuevas, `primera_aparicion: 2026-09-28`, `avisado: false`)

| Candidato | GGUF real | VRAM | tok/s en A2000 | Veredicto |
|---|---|---|---|---|
| **Qwen-Image-2.1** (Qwen, 20-21 sep; 7B DiT + encoder Qwen3-VL-8B) | unsloth/Qwen-Image-2.1-GGUF (solo denoiser): Q4_K_M **3,9GB** · Q6_K_XL 6,3GB · Q8_0 7,1GB · F16 13,3GB; + VAE 0,63GB + encoder ~5,0GB | no medida en la A2000; la fuente estima 8,5GB para Q8_0 **solo denoiser** → ~9,5-10GB con encoder+VAE residentes (offload a RAM posible) | no publicado (36,5 s/imagen en el hardware de la fuente, sin especificar) | **PROBAR** (rol `imagen_infografias`) |
| **MiMo-V2.6-Distill-Qwen-9B** (Xiaomi, 22-sep; 9B SFT de Qwen3.5-9B, agéntico código/ciberseg.) | bartowski (llama.cpp b10964): Q4_K_M **5,84GB** · Q6_K 7,79GB · Q8_0 9,55GB · bf16 17,92GB (imagen con mmproj) · Ollama `maternion/mimo-v2.6`: 5,6/7,4/9,5GB | ~7GB a 8K (estimación propia sobre Q4_K_M + 20%; no medida) | no publicado | **OBSERVAR** (no hay rol código/agente local; veredicto del vendedor: SWE Verified 61,1 vs 60,0 de Qwen3.5-9B) |
| **Tev1-4B / Tev1-0.8B-experimental** (Together AI, 23-26 sep) | "GGUF builds"; arquitectura registrada en llama.cpp/vLLM/MLX | "4GB+" según la fuente; no medido en la A2000 | no publicado | **OBSERVAR** (clasificador estructurado; el lab no tiene rol clasificador) |
| **LFM2.5-VL-3B-DSpark** (LiquidAI; pesos 18-sep, blog 24-sep) | un único GGUF **F16 ~567MB** (repo `LFM2.5-VL-3B-DSpark-GGUF`; safetensors también) | +8,9% sobre el target (280M BF16) | no publicado (todo medido en FP16 por el vendedor, sin reproducción independiente) | **OBSERVAR** — bloqueado: LM Studio no está documentado como runtime y el blog excluye targets cuantizados |
| **K2-Horizon-7B** (IFM/MBZUAI, Apache 2.0, 03-sep) | 0xzknw: Q4_K_M 5,21GiB · Q6_K 6,89GiB · Q8_0 8,92GiB (BF16 16,76GiB ⇒ ~9B params) | cabe con holgura | no publicado | **DESCARTAR hoy, no cerrado**: "K2 Horizon support is not yet in a released upstream llama.cpp build" + PR en curso → exige fork `MBZUAI-IFM/llama.cpp#model/K2Horizon`. Reabrir en cuanto el soporte entre en upstream: el vendedor declara SWE-bench Verified **70,6**, HLE 18,6, LCR 68,0 y Terminal-Bench 2.1 39,1 en un denso de ~9B |
| **LensVLM-9B** (Apple+Duke, 22-24 sep) | GGUF builds citados (4GB+ VRAM); Apple no publica cifra de disco ni VRAM mínima | cabe (sin cifra oficial) | no publicado | **DESCARTAR** (licencia apple-amlr = sólo investigación no comercial + el mecanismo exige el bucle `Expand(k)` de `ml-lensvlm`; autorreportado 41,9 vs 31,1 en MMLongBench-Doc a 15×) |
| **DeepSeek-V4.1-Flash** (MIT, 10-sep; 552B/763B) | GGUF comunitario (smalinin) sólo CUA y sólo con su rama: **Q2_K+Q5_K Engram 335,4GB** (3,58 bpw) … MXFP4 508GB (5,43 bpw) | **no cabe** (ni el mínimo, 335GB) | n/a | **DESCARTAR** (tamaño + runtime propio no-upstream; además ya es el modelo cloud del lab — EXP-20260916-007) |

## Cambio material en un PENDIENTE ya registrado (no es candidato nuevo)

- **Qwen3.8-27B-GSQ-RCO** (PENDIENTE, RE-PROBAR): `ultima_mencion` → 2026-09-28. Motivo (verificado hoy): la cuantización 2,75bpw que estaba sólo auto-reportada **ya circula como GGUF de terceros en mainline** — `ukisai/Swift-1.5-Qwen3.8-27B-GSQ-RCO-GGUF` (**117 likes, 28.802 descargas** según el conteo semanal de localmodelwatch; variante IQ2_S documentada en la tarjeta) — y además la familia tiene GGUF estándar de bartowski con mmproj: **IQ2_XXS 9,39GB · IQ2_XS 9,99GB · IQ2_S 10,3GB · IQ2_M 10,9GB** (+ `mmproj-Qwen3.8-27B-f16.gguf`), y `peculiar-ragdoll/Dirk-Qwen3.8-27B-GGUF` (41.121 descargas/mes) publica UD-Q3_K_XL 13,1GB / UD-IQ4_XS 14,3GB (estos dos ya no caben en 12GB). Es decir: la puerta realista en 12GB son IQ2_XXS/IQ2_XS con mmproj. Sigue **sin medición propia en el lab** → sigue pendiente, no se re-lista como novedad.

## Fuentes consultadas (28-sep-2026)

- https://localmodelwatch.tsuchitsuchi.com/en/2026/09/page/2/ · /page/3/ · /page/4/ · /page/5/ (artículos 21-27 sep) · weekly https://localmodelwatch.tsuchitsuchi.com/en/2026/09/28/open-weight-models-weekly-2026-09-26 (47 artículos; **19 modelos nuevos**, de los que 7 caben estimadamente en 12GB y 5 en 8GB; 17 builds convertidos añadidos a artículos previos)
- https://localmodelwatch.tsuchitsuchi.com/en/2026/09/24/qwen-image-2-1-guide · https://localmodelwatch.tsuchitsuchi.com/en/2026/09/23/unsloth-qwen-image-2-1-gguf-2 · https://localmodelwatch.tsuchitsuchi.com/en/2026/09/23/unsloth-qwen-image-2-1-fp8-int8 · https://huggingface.co/unsloth/Qwen-Image-2.1-GGUF · https://www.kombitz.com/2026/09/20/how-to-use-qwen-image-2-1-gguf-in-comfyui/ · https://huggingface.co/AlperKTS/Qwen-Image-2.1-GGUF
- https://huggingface.co/LiquidAI/LFM2.5-VL-3B-DSpark · https://www.liquid.ai/blog/lfm2-5-vl-dspark · https://www.orcarouter.ai/blog/lfm2-5-vl-3b-dspark-explained (la ruta de localmodelwatch para el drafter NO existe: datos verificados en HF y en el blog del 24-sep)
- https://localmodelwatch.tsuchitsuchi.com/en/2026/09/24/tev1-4b-experimental-released (4B, Qwen3.5-4B, 262.144 ctx, decision-making) · https://localmodelwatch.tsuchitsuchi.com/en/2026/09/28/apple-lensvlm-9b-2 (ficha: repo apple/LensVLM-9B, publicado 22-sep, licencia apple-amlr, arXiv:2605.07019)
- https://ollama.com/maternion/mimo-v2.6 · https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF · https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Distill-Qwen-9B
- https://huggingface.co/0xzknw/K2-Horizon-7B-GGUF (Q8_0 8,92GiB · Q6_K 6,89GiB · Q4_K_M 5,21GiB; BF16 16,76GiB ⇒ ~9B params reales; "K2 Horizon support is not yet in a released upstream llama.cpp build", validado con el fork `model/K2Horizon`) · https://huggingface.co/IFM/K2-Horizon-7B-GGUF (repo del publicador, citado por la tarjeta de 0xzknw)
- https://localmodelwatch.tsuchitsuchi.com/en/2026/09/28/apple-lensvlm-9b-2 · https://groundtruth.day/news/apple-lensvlm-9b-selective-document-context-expansion.html · https://arxiv.org/pdf/2605.07019v1
- https://huggingface.co/smalinin/DeepSeek-V4.1-Flash-GGUF · vLLM v0.30.0 (22-sep)

## Límites de este informe (honestidad de datos)

- **Ninguna VRAM ni velocidad está medida en la A2000**: los tres campos que no existían en fuente se han escrito como "no publicado" / "no confirmado"; las estimaciones van marcadas como tales.
- No se ha descargado, cargado ni probado ningún modelo. Todo veredicto PROBAR/OBSERVAR es una propuesta de cola que requiere OK explícito del usuario.
- Los tamaños GGUF vienen de las tablas publicadas por los repos de cuantización (unsloth, 0xzknw, AlperKTS) y de los blobs/tablas de Ollama; no de estimaciones propias. La cifra de ~9B params de K2-Horizon-7B se deriva del BF16 de 16,76GiB que publica 0xzknw (16,76GiB ÷ 2 B/param), no de una ficha de parámetros.
- MiMo-V2.6-Distill-Qwen-9B: la única evaluación disponible es la del informe técnico de Xiaomi (SWE Verified 61,1 vs 60,0 de Qwen3.5-9B; SWE Pro 44,6 vs 32,0; Terminal Bench 2.1 37,1 vs 27,0; AutomationBench 30,3 vs 5,0) — cifras del vendedor, no reproducidas por terceros.

## Pendientes heredados (no re-listados)

**3**: Ministral-3-14B-Instruct (desde 24-ago-2026, **35 días**), Qwen3.8-27B-GSQ-RCO (07-sep), MiniCPM5-2B (21-sep). Hoy se añade Qwen-Image-2.1 como cuarto PENDIENTE (nuevo, con motivo: rol de imagen/infografías).
