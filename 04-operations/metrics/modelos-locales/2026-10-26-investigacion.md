# Investigación de modelos locales — ventana 19–26 oct 2026

**Fecha de ejecución:** 2026-10-26
**Hardware diana:** RTX A2000 12 GB VRAM
**Registro de memoria:** `candidatos-modelos-locales.json` → 65 entradas antes / 69 después (backup: `candidatos-modelos-locales.json.bak-2026-10-26-1400`)
**Regla aplicada (v2, 14-sep-2026):** solo novedades reales. Todo lo que ya está en el registro no se re-investiga, no recibe veredicto nuevo y no se repite aquí.

---

## Resumen

3 novedades reales registradas + 1 bucket de descartes. Solo **una** merece cola de prueba.

| # | Modelo | GGUF | VRAM (8K) | Veredicto |
|---|---|---|---|---|
| 1 | nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B | SÍ (oficial + unsloth + ggml-org) | ~6,5–7,5 GB con Q4 (estimación) | **PROBAR** (tool_calling) |
| 2 | RecursiveSI/flint (40B-A2.5B) | SÍ (unsloth/ggml-org/LM Studio) | no cabe: mínimo 11,35 GB sin KV | DESCARTAR |
| 3 | XHToken Spark-X2.6-4B | SÍ (oficial, Q4 3,54 GB) | ~4–5 GB | OBSERVAR |

---

## 1. NVIDIA Nemotron-3.5-Bolt-E4B — PROBAR

**Qué es.** Post-entreno de NVIDIA sobre **Gemma-4-E4B-it** (así lo declara la card): 8B totales / **4B efectivos** por el esquema de embeddings por capa de Gemma E4B. Licencia **OpenMDW-1.1** (uso comercial permitido). Contexto 64K. Multilingüe con español entre los idiomas.

**Por qué entra en esta ventana y no en la del 12-oct.** Los repos de pesos son del 05-oct (BF16, 3.418 descargas; variante `-4GB` 35.608), pero **el cambio material son los GGUF del 23-oct**: unsloth (113 likes / **56.882 descargas**), ggml-org y el Q4_K_M dentro del propio repo de NVIDIA. En la ventana anterior no había artefacto ejecutable en llama.cpp.

**Tamaños GGUF verificados (API `?blobs=true`, 26-oct):**

| Repo | Ficheros |
|---|---|
| unsloth | UD-IQ2_M **3,53 GB** · UD-Q3_K_XL 4,22 · UD-Q4_K_XL **5,06** · UD-Q5_K_XL 5,83 · UD-Q6_K_XL 7,26 · UD-Q8_K_XL 8,19 · BF16 15,05 · mmproj BF16 0,99 / Q8 0,56 · drafter DFlash Q8 0,40 |
| ggml-org | BF16 15,05 · Q8_0 8,03 · dflash NVFP4 0,60 |
| nvidia (repo `-4GB`) | un único Q4_K_M **6,18 GB** (imatrix) |

**VRAM estimada a 8K:** ~6,5–7,5 GB con Q4_K_XL/Q4_K_M. Es estimación propia, no medición: la card no publica mínimos. Ojo al matiz de E4B: los embeddings por capa viven en RAM del sistema, así que el reparto VRAM/RAM no es el de un modelo denso equivalente.
**tok/s en A2000:** no publicado.

**Soporte:** arquitectura Gemma-4-E4B (la misma que el lab ya tiene instalada), GGUF de ggml-org publicados y receta en la card con `llama.cpp` imagen `server-cuda13-b11459`. No requiere fork.

**Calidad** (tabla de la card, harness NeMo Gym de NVIDIA, **sin reproducción independiente**; BF16 / Q4_K_M, con Gemma4-E4B-it y Qwen3.5-4B al lado):

| Benchmark | Nemotron E4B | Gemma4-E4B-it | Qwen3.5-4B |
|---|---|---|---|
| BFCL-v3 | 68,51 / 67,31 | 66,39 / 65,03 | **70,95** / 70,56 |
| Tau2-Bench | 55,10 / 52,32 | 38,50 / 38,72 | **75,06** / 61,74 |
| ToolSandbox | 68,77 / **74,13** | 65,43 / 68,31 | 69,54 / 74,51 |
| When2Call multi-turno | **63,36** / 60,50 | 62,90 / 61,12 | 37,85 / 42,88 |
| IFBench | **63,79** / 64,00 | 42,84 / 42,67 | 58,91 / **66,67** |
| IHEval | **84,79** / 82,40 | 67,04 / 66,61 | 60,57 / 62,87 |
| MultiChallenge | **53,10** / 55,60 | 42,08 / 39,36 | 51,76 / 52,23 |
| RoleBench | **67,05** / 71,21 | 49,95 / 60,51 | 53,66 / 52,35 |
| RAGTruth | **77,59** / 77,88 | 76,97 / 77,17 | 75,60 / 74,08 |
| EQ-Bench v3 | 39,40 / 38,15 | **41,17** / 39,77 | 32,92 / 32,07 |
| RULER 64K | 86,99 / 85,76 | 86,55 / 86,14 | **95,15** / 95,37 |

Lectura: gana a su base en todo lo que huele a herramientas, roles e instrucciones (IFBench +21 puntos, IHEval +18, MultiChallenge +11, Tau2 +16), **pierde** en EQ-Bench v3 y en contexto largo frente a Qwen3.5-4B. El Q4 aguanta casi sin pérdida, incluso sube en varias filas.

**Por qué PROBAR y por qué en ese rol.** El rol `tool_calling` del lab lo ocupa `lfm2.5-2.6b`, que **no tiene medición propia**. Este modelo es post-entreno del **mismo base ya medido por el lab** (`google/gemma-4-e4b`: 7/7, 29,2 tok/s, batería 06-ago-2026), así que la comparación es directa y cuesta 5–6 GB. Protocolo: banco de JSON tool-calling + juez, no benchmarks de razonamiento.

**Riesgo a vigilar:** toda la evidencia de calidad es del propio fabricante; el salto de IFBench/MultiChallenge es grande y hay que confirmarlo con el banco del lab antes de darle el rol.

---

## 2. Recursive flint (40B-A2.5B) — DESCARTAR

**Qué es.** El lanzamiento con más tracción de la semana: apache-2.0, publicado el 21-oct (889 likes / 8.470 descargas en el repo de pesos; GGUFs el 20–22 oct con 125.188 en unsloth, 57.635 en lmstudio-community). MoE de **39,8B totales / ~2,5B activos**, 49 capas (2 densas + 47 MoE), 256 expertos con 6 activos + 1 compartido, ventana deslizante de 513 tokens, 262.144 de contexto, corte de conocimiento jun-2026. Declarado para agentes de código (investigar repos, arreglar bugs, escribir tests).

**Tamaños verificados:**

| Repo | Quant | GB |
|---|---|---|
| unsloth | UD-IQ1_M | **11,35** |
| unsloth | UD-IQ2_XXS | 11,86 |
| unsloth | UD-Q2_K_XL | 13,56 |
| ggml-org | Q4_K_M | 23,39 |
| ggml-org | Q8_0 | 42,35 |
| RecursiveSI (BF16) | — | 79,63 |

**Motivo del descarte (dos, independientes).**
1. **No cabe.** El quant más pequeño ocupa 11,35 GB de 12 y no deja sitio para KV cache a 8K; a 4 bits (23,39 GB) se va al doble. El repo oficial solo documenta SGLang en B300 o H200 por réplica.
2. **No hay rol.** El lab no tiene bucket de código/agente **local**: `opencode` va contra DeepSeek cloud y el bucket `codigo` lo cubre `dolphin3.0-8b` (7/7, 6,3 s medidos).

Calidad declarada por el fabricante, sin reproducción independiente: Terminal-Bench 2.1 54,9 · SWE-bench Pro v2 89,7 · SWE-bench Verified 74,2. Registrado para no re-investigarlo.

---

## 3. XHToken Spark-X2.6-4B — OBSERVAR

**Qué es.** Pesos el 19-oct (610 likes / 4.726 descargas), apache-2.0, base `Spark-X2.6-4B-Base`. Sucesor de Spark-X2.5-4B con **la misma arquitectura** (config verificado: `spark2_5` / `Spark2_5ForCausalLM`, 36 capas, hidden 2560, 1.048.576 posiciones): la mejora es de post-entreno —código, agente, contexto largo, multilingüe— más presupuesto de pensamiento en 3 niveles (none/low/high).

**Soporte:** PR #27868 (`Support for Spark2_5ForCausalLM`) cerrado 06-sep-2026 → sin fork. GGUF **oficial** del 19-oct con 69.669 descargas: Q4_K_M **3,54 GB**, Q8_0 4,38 GB, BF16 8,23 GB; además bartowski y mradermacher.

**Calidad:** la card solo publica **gráficos** ("best-in-class entre 4B", "matching or exceeding modelos de 9B") **sin tabla numérica** → *no publicado* en texto y sin evaluación independiente. tok/s en A2000: no publicado.

**Por qué no entra en cola.** No hay hueco claro: `ligero_masivo` lo cubre granite-4.2-8b con 36,9 tok/s y 0/81 alucinaciones medidos, y el rol `tool_calling` se le da al Nemotron E4B, que sí trae tabla. **Reabrir** si el Nemotron decepciona: sería el segundo 4B a medir en ese rol.

---

## 4. Bucket de descartes de la ventana (no volver a investigar)

| Modelo / artefacto | Fecha | Dato que lo descarta |
|---|---|---|
| Nanbeige4.3-33B | 24-oct | Denso 33B, apache-2.0, 524 likes; Q4 23,5 GB |
| InternScience Sage-A1.5 35.5B | 21-oct (1er GGUF) | Q4_K_M 21,7 GB |
| shisa-ai shisa-de-2.1 25.2B | 20-oct | Q4_K_M 16,8 GB |
| ornith-ai Ornith-1.5-122B | 20-oct | Q4_K_M 75,8 GB |
| tencent/Hy-Memory-30B-A3B | pesos 15-oct, GGUF 19-oct | Q3_K_M 14,45 / Q4_K_M 18,24 GB no caben; los únicos que entran son Q8_0-expsIQ1_M 8,03 y expsIQ2_XXS 9,14 GB (expertos a 1–2 bits) para un rol de memoria de agente que el lab no tiene |
| taronaeo/Granite-4.2-3B-BE | 18-oct | No es modelo nuevo: `granite-4.2-3b` con bytes intercambiados para IBM Z / LinuxONE (big-endian) → inútil en x86 |
| MiniCPM-OCR 1.0 | 22-oct (soporte mtmd, PR #30979) | Pesos **no localizables** en openbmb por API → no evaluable; el rol OCR ya está en LightOnOCR-3 (OBSERVAR) |
| ccore/Qwen3.5-4B-3D-Coder | 25-oct | Sin rol 3D en el lab; Q4 3,9 GB |

*Tamaños de Sage-A1.5, shisa-de-2.1, Ornith y Nanbeige tomados del listado de primeros GGUF (localllm.az-arte.com / recentmodel.com), no re-verificados fichero a fichero. Los de Hy-Memory, flint, Spark y Nemotron sí están verificados con la API de HuggingFace.*

---

## Estado del registro y pendientes heredados

- **Entradas:** 69 (9 EN_USO · 5 PENDIENTE · 25 OBSERVAR · 30 DESCARTADO).
- **Cambios de esta ejecución:** solo 4 altas. Ninguna entrada existente modificada, nada borrado.
- **PENDIENTES HEREDADOS: 4** (Ministral-3-14B-Instruct 63 días · Qwen3.8-27B-GSQ-RCO 49 · MiniCPM5-2B 35 · Qwen-Image-2.1 28) **+ 1 nuevo** (Nemotron-3.5-Bolt-E4B, 0 días).

## Fuentes consultadas

- HuggingFace API (`/api/models`, `/tree/main?recursive=true`, `/raw/main/README.md` y `config.json`): verificación de fechas de publicación, likes, descargas, licencias y tamaños exactos de cada GGUF.
- Cards oficiales: `nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB`, `XHToken/Spark-X2.6-4B`, `RecursiveSI/flint`, `taronaeo/Granite-4.2-3B-BE-GGUF`.
- GitHub API: PRs de ggml-org/llama.cpp (#27868 soporte Spark2_5, #30979 mtmd MiniCPM-OCR, #31167/#31168 DSpark para Spark2.6).
- Agregadores: localmodelwatch.tsuchitsuchi.com, localllm.az-arte.com/en/models/new, recentmodel.com, HF trending GGUF.
- Interno: `candidatos-modelos-locales.json`, `01-knowledge/modelos_por_tarea.yaml`, `alucinaciones_ledger.jsonl`, `01-knowledge/experiments/` y `01-knowledge/objects/` (0 coincidencias para los nombres nuevos → ninguno probado antes por el lab).

**No se ha descargado, cargado ni ejecutado ningún modelo. Sin sudo, sin tocar Docker/n8n/systemd.**
