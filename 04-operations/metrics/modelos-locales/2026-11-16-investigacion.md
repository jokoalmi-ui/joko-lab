# Investigación semanal modelos locales — 2026-11-16

Ventana analizada: 09-nov-2026 → 16-nov-2026 (borde abierto para anuncios del 10-13 nov).
Hardware techo: RTX A2000 12GB. Regla aplicada: solo novedades no registradas en `candidatos-modelos-locales.json` (79 entradas antes de hoy).

## Novedades con veredicto PENDIENTE (2)

### 1. Qwen3.6-35B-A3B MACaQ-R — cuantización del modelo que YA está en uso · Huawei CSL · GGUF 11-nov-2026

| Dato | Valor | Verificado |
|---|---|---|
| Qué es | cuantización "refinada" con MACaQ-R del Qwen3.6-35B-A3B (el `veracidad_critica` actual) | card HF |
| Fichero | un único `Q4_K_XL` = **22,36 GB** (22.360.455.968 B) | API `?tree/main` |
| Motor | llama.cpp estándar (`llama cli` / `llama serve`), sin build propio, sin bloque MTP | card HF |
| Calidad declarada | KL a FP16 **0,013367** vs **0,015731** del UD-Q4_K_XL de Unsloth **al mismo tamaño** | tabla del repo |
| Licencia | Apache-2.0 | card HF |
| tok/s A2000 | **no publicado** | — |
| Tracción | 2.291 descargas, 13 likes en 5 días | API HF |

**Por qué entra:** no es un modelo nuevo, es el mismo que ya corre el lab con ~15% menos divergencia declarada y **coste de VRAM idéntico**. No cabe entero en 12 GB (22,36 GB), así que necesita el mismo offload que el fichero actual — eso es lo que hace la prueba barata: solo cambia el fichero.
**Aviso:** la tabla KL es del publicador; no hay medida independiente. La prueba sería la batería de alucinaciones contra el fichero actual, no una impresión subjetiva.

### 2. QVAC BotPsy-0.8B — tool calling sub-1B · Tether AI Research · pesos 10-nov-2026

| Dato | Valor | Verificado |
|---|---|---|
| Tamaño | 0,8B (base Qwen3.5-0.8B), ctx nativo **262.144** | cabecera GGUF |
| GGUF llama.cpp | **q4_k_m-imat 0,53 GB** / q8_0 0,81 GB / bf16 1,52 GB | API `?tree/main` |
| BFCL v4 | **44,0** (base 23,4 · Qwen3.5-2B 37,7) | vendor, no reproducido |
| ToolSandbox | **64,6** (base 30,5) | vendor, no reproducido |
| Licencia | Apache-2.0 | card HF |
| tok/s A2000 | **no publicado** | — |

**Por qué entra:** es el candidato más barato de toda la cola (0,53 GB) y el único de la ventana con tabla de tool-use publicada; además declara negarse cuando ninguna herramienta encaja. El propio vendor lo limita a dificultad baja/media, así que **entra al final de la cola** de `tool_calling`, detrás de MiniCPM5-2B, Nemotron-Bolt-E4B y LFM3-1.7B.

## Cabe y es relevante, pero no entra en cola (1)

**IBM Granite 4.1 8B / 3B LLMON Preview** (anuncio 12-nov, Apache-2.0, GGUF de terceros 12-13 nov): entrenados en markup LLMON, que separa instrucciones de datos no confiables — el texto de un PDF o una web entra marcado como dato, no como orden. **Veredicto: OBSERVAR.** Es la primera propuesta de un 8B contra un riesgo real del lab, pero sigue en Preview, no hay eval independiente y el markup lo tiene que emitir el harness (n8n, MCP, lectores de PDF); sin adaptarlo no aporta nada. Revisitar si sale estable con card de evaluación.

## Descartados con motivo (2)

- **MiniMax-H3-Image** (03-nov, DiT single-stream de 33,1B, 16MP, 6 pasos): GGUF podado con Q3_K_M **8,91 GB** y Q4_K_M **11,57 GB**, pero son **solo del denoiser** — el encoder de texto H3 va aparte, así que en 12 GB no entra el conjunto. Además el rol `imagen_infografias` ya tiene Qwen-Image-2.1 PENDIENTE desde el 21-sep y SDXL en uso, con tipografía legible como requisito; la baza de H3-Image es fotorrealismo. Licencia community, no Apache.
- **Bucket 09–16 nov**: Agnes 2.5 Pro Theta (187,8B/375,5 GB), Inkling 2 Small (pasó a Apache 2.0 el 12-nov pero 594B/17B y ~500 GB de VRAM: cambio de licencia, no de encaje), Qwen4-Max (2,4T, propietario), Hy4 flash (solo API), LongCat-2.5 (1,6T), Ling 3.1 Flash, Nemotron 3.5 Super VL, Praxis-1 (robot, no hay bucket), Edge0-145B/120B (29 GB de pico y motor propio), Decider v1.3 (27B, no cabe) y Decider Flash v1.3 (4B, cabría pero la cola de decisión ya tiene 6 en OBSERVAR y el router es rule-based), HeyGen Decision 1 (API), Lara Mini Base (7,2B/0,6B MoE, **base sin instruct**, gated, CC BY-NC-SA), plamo-3-fin-instruct (japonés financiero), Salience-27B-R6, Orion-26B-A4B-v1.1, Axion-1.0-35B, qwen-concept-27b, Drama-3-Japanese, gemma-4-31B-heretic, Qwen3.8-27B-Ultimate-Heretic, nova-uncensored-qwen3-swallow-8b. **No son modelos**: llama.cpp y ggml v1.0.0 (13-nov, compromiso de versionado, mismo commit que antes), MoEShift, llama-modchip, Claris Harbor, Exact.

## Estado del registro

- Entradas totales: **84** (antes 79). Nuevas hoy: 5 (2 PENDIENTE, 1 OBSERVAR, 2 DESCARTADO incluido bucket), todas con `avisado=false`.
- PENDIENTES: 9 → Ministral-3-14B (24-ago, **12 semanas**), Qwen3.8-27B-GSQ-RCO (07-sep), MiniCPM5-2B (21-sep), Qwen-Image-2.1 (28-sep), Nemotron-3.5-Bolt-E4B (26-oct), LFM3-1.7B (02-nov), PLaMo 3 Translate (09-nov), MACaQ-R y BotPsy-0.8B (hoy).
- Backup previo a la escritura: `candidatos-modelos-locales.json.bak-2026-11-16-1400` (99.696 bytes).
- No se ha descargado ni cargado ningún modelo. No se ha tocado n8n, Docker ni systemd.

## Fuentes

- HF API `?tree/main` y `?blobs=true` sobre huawei-csl/Qwen3.6-35B-A3B-MACaQ-R-GGUF, qvac/BotPsy-0.8B-GGUFs, Abiray/MiniMax-H3-Image-GGUF, lidon-ai/granite-4.1-*-llmon-preview*-GGUF, vblanco y fxoz pplx-decider-flash-v1.3.
- Cards: huawei-csl MACaQ-R (tabla KL), qvac BotPsy-0.8B-GGUFs, Abiray (tabla VRAM por quant), MiniMaxAI/MiniMax-H3-Image, ibm-granite/granite-4.1-8b-llmon-preview.
- Listados: llm-releases.com/changelog (consultado 16-nov, ítems 12-16 nov), toolhalla.ai/news (16-nov), artificialprism.com/weekly/2026-w46, openmodeldrops.com.
- Búsquedas API: `?search=BotPsy`, `?search=macaq`, `?search=MiniMax-H3-Image`, `?search=LLMON`, `?search=decider`, `?filter=gguf&sort=createdAt`.
- Nota: localmodelwatch.tsuchitsuchi.com **no cubre la ventana** (su última entrada es del 05-oct, páginas con fecha de actualización 11-13 nov): no se ha usado como fuente de novedades.
