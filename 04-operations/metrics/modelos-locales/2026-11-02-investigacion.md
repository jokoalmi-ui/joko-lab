# Investigación semanal modelos locales — 2026-11-02

Ventana analizada: 26-oct-2026 → 02-nov-2026. Hardware techo: RTX A2000 12GB.
Regla aplicada: solo novedades no registradas en `candidatos-modelos-locales.json` (73 entradas antes de hoy).

## Novedad real de la semana (1 familia)

### LiquidAI LFM3 — 1.7B texto + VL-2B + Omni-2B + Audio-2B · lanzamiento 27-oct-2026

| Dato | Valor | Verificado |
|---|---|---|
| Params / arquitectura | 1,73B, 24 capas híbridas (13 conv corta con puerta, 5 atención deslizante, 6 global) | card HF |
| Contexto | 256K entrada+salida | card HF |
| Idiomas | 16, incluye español | card HF |
| Licencia | LFM Open License v1.0 (no Apache) | card HF |
| Q4_K_M | **1,10 GB** | API `?blobs=true` |
| QAD-Q4_0 | 1,05 GB | API `?blobs=true` |
| Q8_0 / BF16 | 1,85 GB / 3,47 GB | API `?blobs=true` |
| VRAM estimada 8K | ~1,6–2,5 GB (**estimación propia, NO medida**) | — |
| tok/s A2000 | **no publicado** | — |
| GGUF oficial | sí, QAD-Q4_0 / Q4_K_M / Q5_K_M / Q6_K / Q8_0 / BF16 | repo LiquidAI |
| Motores | card declara llama.cpp, Ollama, LM Studio; PR #31431 llama.cpp (tensor split LFM3) merged | card + GitHub API |
| Descargas GGUF texto | 174.177 (24-oct) | API |

Repos y fechas: LFM3-1.7B 23-oct, LFM3-1.7B-GGUF 24-oct, LFM3-VL-2B 19-oct, LFM3-Omni-2B 21-oct (+GGUF 27-oct, 132.215 descargas), LFM3-Audio-2B-GGUF 27-oct, LFM3-Base 26-oct.

**Por qué entra en cola (rol tool_calling / json):** la card dice literalmente que está post-entrenado para harness de agentes «such as Hermes Agent, Pi, and OpenClaw» — es el único modelo de la ventana que nombra el harness del lab. Además el rol `tool_calling` del lab usa `lfm2.5-2.6b` y no tiene medición propia en el ledger; este es el test más barato de toda la cola (1,1 GB solo texto).

**Calidad:** cifras del vendor (media 49,37 vs 47,24 de Qwen3.5-9B; +35% menos params que LFM2.5-2.6B; LiveClaw 45,60; AutomationBench 41,29; WebArena-Verified 38,42) SIN reproducción independiente. Sí hay test de terceros del 28-oct (MindStudio, MindStudio AI blog) en ~1 GB: pasa JSON estructurado, instrucciones de múltiples restricciones, QA con grounding, matemática multi-paso y doble tool calling con argumentos correctos; **falla** un bug-fix agéntico real (dice que lo arregló sin tocar los números), HTML/JS 2/2 y traducción multilingüe amplia. La propia card avisa: no recomendado para coding agéntico ni razonamiento multi-paso.

**Veredicto: PROBAR** (PENDIENTE). Medir con `tools/evaluar_json_tool_calling.py` + banco del juez, no con benchmarks de razonamiento. Compite en cola con MiniCPM5-2B y Nemotron-3.5-Bolt-E4B.

## Otra novedad de la familia

**d1-2B / d1-Omni-2B** (decision models sobre LFM3-VL-2B, 27-oct). Devuelven respuesta calibrada en un solo forward pass sin generar tokens; la card afirma que supera a d1-3B con menos de 2/3 de su tamaño; 5,7 ms/decisión en H100 (A2000: no publicado). GGUF: d1-2B Q4_K_M 1,1 GB + mmproj 0,2 GB; d1-Omni-2B Q8_0 1,85 GB + mmproj 0,33 GB. **Veredicto: OBSERVAR** — el lab no tiene bucket de decisión/routeo (`tools/decision_router.py` es rule-based), mismo encaje que clef-flash / d1-3B / h2o-lightning-4b.

## Descartados con motivo

- **Nemotron-3.5-Transcribe-30B-A4B** (primer GGUF 28-oct, AtomicChat, 50.291 descargas): quant mínimo Q2_0_M **13,57 GB** > 12 GB, y encima + encoder F16 1,67 GB + drafter. Rol transcripción del lab = whisper CPU. DESCARTADO por tamaño.
- **Qwen3.8-Flash-Next** 177B, **Cyber-Tiel-Coder-35B-A3B** (36B), **ccore/Qwen3.5-4B-GLB-3D-Coder** (4B, sin rol 3D), **kaitchup/Qwen3.8-27B-SLQ** (variante de entrada ya PENDIENTE), **aura-fleet-gguf** (51k descargas en un día pero 0 likes y README no encontrado → procedencia no verificable), **HARP-1B** (no localizable por API).
- **pfnet/plamo-13b-instruct-nc**: verificado por API que el repo es de **2023-10-26** — no es novedad, aunque aparezca en listados de "nuevos GGUF".
- **DeepSeek-V4.1-Flash** y sus repacks: familia ya DESCARTADA.

## Estado del registro

- Entradas totales: **73** (antes 69). Nuevas hoy: 4 (1 PENDIENTE, 1 OBSERVAR, 1 DESCARTADO, 1 bucket).
- PENDIENTES: 6 → Ministral-3-14B (24-ago, **10 semanas**), Qwen3.8-27B-GSQ-RCO (07-sep), MiniCPM5-2B (21-sep), Qwen-Image-2.1 (28-sep), Nemotron-3.5-Bolt-E4B (26-oct), LFM3-1.7B (hoy).
- Backup previo a la escritura: `candidatos-modelos-locales.json.bak-2026-11-02-1400`.
- No se ha descargado ni cargado ningún modelo. No se ha tocado n8n, Docker ni systemd.

## Fuentes

- HF API `?blobs=true` sobre LiquidAI/LFM3-1.7B-GGUF, LFM3-VL-2B-GGUF, d1-2B-GGUF, d1-Omni-2B-GGUF, AtomicChat/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B-GGUF, pfnet/plamo-13b-instruct-nc.
- Cards: huggingface.co/LiquidAI/LFM3-1.7B, /LiquidAI/d1-2B.
- Terceros: mindstudio.ai/blog/liquid-ai-lfm3-1-7b-local-agent-model (28-oct).
- Listados: localllm.az-arte.com/en/models/new, huggingface.co/models?library=gguf.
- GitHub: búsqueda de PRs merged en ggml-org/llama.cpp (PR #31431).
