# Investigación semanal modelos locales — 2026-11-09

Ventana analizada: 02-nov-2026 → 09-nov-2026 (con borde abierto a 26-oct para primeros GGUF).
Hardware techo: RTX A2000 12GB. Regla aplicada: solo novedades no registradas en `candidatos-modelos-locales.json` (73 entradas antes de hoy).

## Novedad real con veredicto PROBAR (1)

### PLaMo 3 Translate — 0.8B / 2B / 8B / 31B · Preferred Networks · pesos 05-nov-2026

| Dato | Valor | Verificado |
|---|---|---|
| Especialidad | traducción, 53 idiomas (card lista `es`), contexto circundante y glosarios | card HF |
| Entrada+salida máx. | 32.768 tokens combinados | card HF |
| Licencia | PLaMo Community: personal/no comercial gratis; comercial < 1.000 M JPY con registro | blog PFN |
| Q4_K_M 0.8B / 2B / 8B / 31B | **0,57 GB / 1,81 GB / 5,28 GB / 19,50 GB** | API `?blobs=true` |
| VRAM 8K (0.8B/2B/8B) | 1,36 / 2,72 / 6,25 GB (**estimación de terceros, NO medida**) | localllm |
| tok/s A2000 | **no publicado** | — |
| GGUF oficial | sí, Q2_K→Q8_0 + MLX 4bit; primeros GGUF 27-oct, actualizados 09-nov | API HF |
| Descargas (0.8B/2B/8B) | 25.670 / 16.886 / 15.046 | API HF |

**Por qué entra en cola (rol traducción):** es el primer modelo de la ventana que ataca una tarea recurrente del lab (pasar cards/papers en inglés a español y viceversa) con un coste de 1,81 GB. La casa afirma que el 0.8B supera a traductores especializados con 30× más parámetros en ja↔en y ja↔otros; **no hay ninguna cifra publicada para es↔en**, que es justo lo que hay que medir.
**Veredicto: PROBAR** — lote es↔en/en↔es contra el modelo actual del bucket `redaccion_datos`. Si el 2B no bate al actual, no se escala al 8B.

## Cabe y es interesante, pero sin rol (1)

**Microsoft Mage-VL-Cowork 4B** (30-oct, Apache-2.0): VLM de computer-use que alterna acciones de GUI y bash en una sola política; 66,0% OSWorld-Verified (vendor). El cambio material está en la ventana: **GGUF oficial de ggml-org el 07-nov** — Q4_K_M **2,72 GB** + mmproj Q8 **0,35 GB** (~4 GB a 8K, estimación propia); tok/s A2000 no publicado; 3.714 descargas del repo base y 7.232 del GGUF de Hansda. **Veredicto: OBSERVAR** — `modelos_por_tarea.yaml` no tiene bucket `computer_use` y el lab no tiene harness de captura/acciones. Aviso: daría shell y control de escritorio, en conflicto con la regla de no actuar sin confirmación.

## Descartados con motivo

- **webAI TwIL-8B** (08-nov, 8,79B densos sobre Granite 4.2 8B, 131K ctx, GGUF Q4_K_M **5,35 GB**, 34.546 descargas/244 likes): MATH-500 98,2 reportado por el vendor, sin eval independiente. **DESCARTADO como motor** por licencia *webAI Non-Commercial v1.0* — el lab genera trabajo remunerado; además su baza es la traza larga, contra la velocidad que pide el bucket `code`. Queda como referencia (OBSERVAR) para uso estrictamente personal.
- **NousResearch Arete-27B** (06-nov, Apache-2.0, SFT de Qwen3.8-27B): propaganda 22%→0,9% pero Hermes Bench **65,77→65,60** (sin mejora de capacidad). GGUF: Q4_K_M **17,20 GB**, Q3_K_M **13,17 GB**, Q2_K 10,58 GB, IQ2_XS 8,85 GB. DESCARTADO por tamaño (el primer quant usable ya pasa de 12 GB) y porque la vía sub-2bpw de ese mismo base ya está en cola con Qwen3.8-27B-GSQ-RCO.
- **Kakao Kanana-2-v-decide-3b** (06-nov, 3,67B): devuelve probabilidades, no texto; arquitectura propia sin GGUF ni soporte llama.cpp. DESCARTADO — no hay motor local que lo cargue y ya hay 5 modelos de decisión en OBSERVAR.
- **Bucket 02–09 nov**: Kimi K3.1 Pro (2,8T/104B), Ripple-65B, Hydrogen-1.0 (753B), ERNIE 5.5 Flash Base (280B/14B, pre-entrenamiento), LongCat-2.5 (1,6T, API), Ling-3.2-flash (560B/25B, API), Inkling 2 Small (594B/17B, cerrado), Mistral Large 4 (1T), Particle-1 (API), Clover-35B-A3B-Preview (difusión, offload ~9-10 GB), Hy4 (API), SWE-2 Flash (sin pesos), EKA-1 (sin pesos), Endeavor 1.1 (sin pesos), Dhīr 2B/5B (sin español), SenseNova 6.8 Flash (cerrado), SenseNova-Loop-9B-Preview (Preview, bucle, cola `tool_calling` ya con 6 pendientes), Idol (image→3D, no LLM), surya-ocr-2.5 (OCR 0,6B; el pipeline usa stirling-pdf + visión GLM), Qwen3.6-35B-A3B-BE (big-endian), DeepSeek-V4-Pro-Qwen3.5-9B-heretic (repack de familia descartada).

## Estado del registro

- Entradas totales: **79** (antes 73). Nuevas hoy: 6 (1 PENDIENTE, 2 OBSERVAR, 3 DESCARTADO incluido bucket), todas con `avisado=false`.
- PENDIENTES: 7 → Ministral-3-14B (24-ago, **11 semanas**), Qwen3.8-27B-GSQ-RCO (07-sep), MiniCPM5-2B (21-sep), Qwen-Image-2.1 (28-sep), Nemotron-3.5-Bolt-E4B (26-oct), LFM3-1.7B (02-nov), PLaMo 3 Translate (hoy).
- Backup previo a la escritura: `candidatos-modelos-locales.json.bak-2026-11-09-1400` (87.058 bytes).
- No se ha descargado ni cargado ningún modelo. No se ha tocado n8n, Docker ni systemd.

## Fuentes

- HF API `?blobs=true` sobre pfnet/plamo-3-translate-{0.8b,2b,8b,31b}-GGUF, ggml-org/Mage-VL-Cowork-GGUF, webAI-Official/TwIL-8B, bartowski/NousResearch_Arete-27B-GGUF, kakaocorp/kanana-2-v-decide-3b-2611.
- Cards: pfnet/plamo-3-translate-2b (idiomas/licencia), webAI-Official/TwIL-8B (licencia, MATH-500), microsoft/Mage-VL-Cowork.
- Blogs: preferred.jp/en/blog/tech/plamo-3-translate-weight-release (05-nov).
- Listados: llm-releases.com/changelog (consultado 09-nov), localllm.az-arte.com/en/models/new (primer GGUF + VRAM estimada 8K).
- Búsquedas API: `?search=Arete-27B`, `?search=kanana-2-v-decide`, `?search=SenseNova-Loop-9B`, `?search=Clover-35B-A3B`, `?search=Mage-VL-Cowork`.
