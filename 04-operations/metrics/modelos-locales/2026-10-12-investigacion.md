# Investigacion semanal de modelos locales — 2026-10-12

Cron: `investigacion-modelos-locales-semanal` (v2). Hardware objetivo: RTX A2000 12GB.
Registro (memoria del cron): `04-operations/metrics/modelos-locales/candidatos-modelos-locales.json`
Backup previo a esta escritura: `candidatos-modelos-locales.json.bak-2026-10-12-1406` (50 entradas -> 58).

## Metodo de esta corrida
1. PASO 0: lectura del registro (50 entradas antes de hoy), `01-knowledge/modelos_por_tarea.yaml`
   (roles: veracidad_critica qwen3.6-35b-a3b, vision glm-4.6v-flash, codigo dolphin3.0-llama3.1-8b-cyber-lora,
   redaccion_datos gemma-4-12b-qat, grounding r1-distill-14b, razonamiento gpt-oss-20b; nulos: interactivo,
   generacion_imagen, transcripcion), `alucinaciones_ledger.jsonl` y busqueda de los nombres nuevos en
   `01-knowledge/experiments/` y `01-knowledge/objects/` (0 coincidencias -> ninguno estaba ya probado).
2. Barrido: agregador semanal, r/LocalLLaMA, HuggingFace (trending + GGUF por createdAt y por likes),
   repos oficiales y de terceros verificados por API de HuggingFace (`?blobs=true` para tamanos reales por
   fichero), y API de GitHub para el estado real de cada PR de llama.cpp citado.
3. Filtro: solo publicados o con cambio material del 28-sep al 12-oct-2026, que quepan en 12GB (o MoE con
   offload viable) y con GGUF publicado. Todo lo que ya estaba en el registro se ha SALTADO.

## Novedades registradas hoy (8 entradas nuevas, avisado=false; 6 OBSERVAR + 2 DESCARTADO)

### 1. LiquidAI `d1-3B` / `d1-omni-600M` — OBSERVAR
- Pesos el 05-oct-2026 (d1-3B 324 likes / 11.866 descargas; d1-omni-600M 110 likes / 10.942; licencia `other`).
  NO generan texto: estado (texto/JSON/imagen; d1-omni tambien audio) + preguntas tipadas -> probabilidad por
  opcion en un solo forward pass, con CERO tokens de salida.
- `d1-3B` = 3,12B sobre **LFM2.5-VL-3B**, que el lab ya tiene instalado; card: 48,57 en Decision Index 0.2.1
  ("best decision model under 10B", por delante en su tabla de Decision 1.0 Lux 9.7B 43,49 y Jet v6.2 4.7B 42,60),
  74,1 en 11 benchmarks de imagen y 8 ms/decision en RTX 4090 bf16.
- GGUF oficiales verificados: Q4_K_M **1,67GB** / Q8_0 2,87GB / F16 5,40GB + mmproj Q8 0,58GB -> cabe holgado.
- Soporte: PR **30110** merged 07-oct (d1-3B) y **30114** merged 08-oct (d1-omni); el soporte de
  LFM2.5-Encoder-350M/230M (base del omni) entro en el PR **29862** el 03-oct.
- Encaje: el lab no tiene bucket de decision/routeo (rule-based) -> OBSERVAR, no entra en cola. Es la
  alternativa de 3B al `clef-flash` de 9B (ya OBSERVAR desde el 05-oct), misma API Jev/SystemOne.

### 2. `h2oai/h2o-lightning-4b` (v1.1) — OBSERVAR
- 02-oct-2026, **apache-2.0** (57 likes / 1.578 descargas). Decision multimodal (documento + imagenes) sobre
  Qwen3.5-4B: tipos choice / noul (si-no) / score, una probabilidad por opcion, un forward pass y UN token.
- Card: **#1 en JevBench v1.6.1 el 07-oct-2026** en el tablon de pesos abiertos con **72,5**, por delante del
  propio Jev (71,5) y de todos los abiertos de 12B/26B/31B; corre sobre vLLM 0.30.0 + un shim.
- GGUF verificados: `h2oai/h2o-lightning-4b-gguf` (10-oct) Q4_K_M **2,71GB** / Q5_K_M 3,07GB / Q8_0 4,48GB /
  BF16 8,42GB + mmproj 0,67GB; `...-native-gguf` (11-oct); `mradermacher/...-GGUF` (05-oct); tambien ONNX y MLX.
- Frente a d1-3B: licencia limpia y mas traccion. Mismo rol sin bucket en el lab -> OBSERVAR.

### 3. `autotrust` JEV-27B-VL / GEV-26B-Decide / JEV-35B — DESCARTADO (tamano + rol duplicado)
- La familia de decision con mas traccion de la semana: JEV-27B-VL (30-sep, 3.787 likes, 1.550.455 descargas),
  GEV-26B-Decide (02-oct, 2.338 likes, 1.025.186 descargas), JEV-35B (11-oct, 126 likes) + JEV-35B-NVFP4.
- Son **adaptadores** sobre bases ajenas (Qwen3.8-27B denso y gemma-4-26B-A4B-it); JEV-35B si es finetune
  completo de Qwen3.5-35B-A3B. GGUF de terceros ya existen (mradermacher/GEV-26B-Decide-GGUF: Q4_K_M 16,80GB /
  Q3_K_M **13,29GB** / IQ4_XS 14,06GB; JEV-35B-GGUF creado hoy).
- Motivos: el mas pequeno de los tres (26B-A4B a Q3_K_M) ya pide 13,29GB -> offload de expertos obligatorio
  (como con qwen3.6-35b-a3b, 10.686 MiB medidos), y el rol lo cubren d1-3B (1,67GB) y h2o-lightning-4b (2,71GB)
  enteros en VRAM. Se registra para NO re-investigarlo cada semana.

### 4. JetBrains `Mellum2.1-12B-A2.5B-Thinking` — OBSERVAR (GGUF oficial nuevo)
- Repo base del 20-sep (107 likes); el cambio material de la ventana es el **GGUF oficial del 07-oct** (69 likes,
  20.646 descargas): MXFP4_MOE **7,03GB** / Q4_K_M **8,07GB** / Q6_K 10,88GB / Q8_0 12,93GB / BF16 24,31GB.
- config.json verificado: `mellum`, 28 capas, hidden 2304, 64 expertos y 8 por token -> MoE 12B con ~2,5B activos;
  la arquitectura lleva en llama.cpp desde el PR **23966** (02-jun) -> carga con builds actuales, sin PR nuevo.
- Aviso: NO es un modelo nuevo, es la version 2.1 del Mellum2-12B-A2.5B que ya esta OBSERVAR desde el 24-ago;
  lo nuevo es el modo thinking y el GGUF. Sin medicion propia comparable (dolphin3.0 7/7) -> OBSERVAR.

### 5. `LightOnOCR-3` (4B / 1B / 0.8B) — OBSERVAR (primer OCR dedicado con GGUF del registro)
- LightOn: LightOnOCR-3-4B (06-oct, 73 likes, 3.222 descargas), -1B y -0.8B (07-oct), apache-2.0, layout,
  tablas, formularios y visual grounding (paper arXiv 2601.14251).
- config.json verificado: `qwen3_5` -> arquitectura ya soportada por llama.cpp. GGUFs de terceros del 08-oct:
  4B Q4_K_M **2,71GB** + mmproj-q8 0,37GB (2.284 descargas); 0.8B Q4_K_M **0,53GB** + mmproj 0,12GB.
- Encaje: OCR/documentos, hoy cubierto por glm-4.6v-flash (26,4 tok/s, 9.984 MiB, 7/7); un OCR de 0,8-4B
  liberaria VRAM del VLM. Su unico argumento de calidad es el "Best OCR model" del propio card, sin
  reproduccion independiente -> OBSERVAR; si hace falta OCR por lotes de PDF, es el primero a medir.

### 6. `microsoft/AesCode-8B` — OBSERVAR (codigo HTML/diseño)
- 29-sep-2026, apache-2.0 (44 likes / 140 descargas; 17,5GB en safetensors). config.json: `qwen3_vl` sobre
  Qwen3-VL-8B-Instruct, afinado con RL para codigo HTML/diseño (tags code-generation, html, design).
- GGUF bartowski del 11-oct (2.072 descargas en un dia): Q4_K_M **5,21GB** / Q5_K_M 6,24GB / Q8_0 8,71GB /
  mmproj 1,16GB; tambien AesCode-32B y MLX del 12-oct. Cabe a Q4-Q5.
- tok/s en A2000: no publicado. El card no da numeros comparables, y es especialista en HTML/diseño, no en
  codigo general -> OBSERVAR, no PROBAR (el rol `codigo` tiene 7/7 y 29,8 tok/s medidos).

### 7. `google/embeddinggemma-2` (+ GGUF) — OBSERVAR (embeddings multimodales)
- Base del 14-sep (fuera de ventana: 1.836 likes, 115.763 descargas, 1,49GB ~300M); el cambio material es doble:
  soporte en llama.cpp (PR **30054** merged 06-oct, "support embeddinggemma2 (text+vision+audio)") y GGUFs del
  06-oct: `ggml-org/embeddinggemma-2-GGUF` (BF16 0,56GB / Q8_0 0,31GB / mmproj BF16 0,98GB) y
  `unsloth/embeddinggemma-2-GGUF` (272 likes, 71.914 descargas).
- Encaje: el RAG del lab indexa con bge-m3 y nomic-embed-text-v1.5; un embedding multimodal abriria indexar
  imagen/audio en el mismo espacio. OBSERVAR: cambiar el embedding obliga a re-indexar (~21K filas LanceDB)
  y esa decision es del usuario, no del cron.

### 8. Bucket "otros detectados (09-oct a 12-oct)" — DESCARTADO
- Resto de la familia decision sin bucket en el lab y peor encaje que d1-3B/h2o: `pplx-decider` (soporte PR
  **30044** merged 06-oct), `vllm-sr/d3` (10-oct, 70 likes, finetune de Qwen3.8-27B) y `vllm-sr/Vela-2.0-9B`
  (02-oct), `neuphonic/neudecide` (06-oct), nimble (PR **29844**), API `/v1/systemone` con laya/julia-1/lev/
  openjev/kev (PR **29818**).
- Otros: `ConwayResearch/Underdog-Saluki-27B-1.0` (08-oct, 345 likes, 242.329 descargas) = port IQ2 sobre
  `ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF` -> variante de una entrada YA PENDIENTE, no candidato nuevo;
  MiniCPM-V 4.7 (soporte merged PR **29416** el 10-oct pero pesos no publicados de forma verificable);
  `tencent/Youtu-Parsing-Omni` (09-oct, arquitectura propia `youtu_vita`, sin soporte ni GGUF propio);
  `Cloudflare/clef-omni` (09-oct, finetune de Qwen3-Omni-30B-A3B -> familia clef ya OBSERVAR).
- Tamanos NO re-verificados hoy en este bucket: se descartan por rol o por familia ya registrada.

## Cambios materiales en entradas YA existentes (no son novedades)
- **Qwen-Image-2.1** (PENDIENTE, rol generacion_imagen): aparecen `Qwen/Qwen-Image-2.1-Turbo` (09-oct, 590 likes,
  6.787 descargas, text-to-image, license:other, finetune de Qwen-Image-2.1) y una variante PE de terceros
  (12-oct) -> son la misma familia de la entrada PENDIENTE; se probarian, si acaso, por esa entrada.
- **Qwen3.8-27B-GSQ-RCO** (PENDIENTE): re-verificado hoy `ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF` -> 2.169 likes,
  1.482.471 descargas, mismos tamanos que el 05-oct (IQ2_XS 8,42GB / IQ2_S 9,26GB / IQ3_XXS 10,09GB /
  IQ3_S 11,77GB, mmproj 0,93GB). Sin cambio de veredicto ni EXP asociado.

## Detectado pero NO registrado
- TTS: `KittenML/kitten-tts-2` (30-sep, 75 likes, 17.056 descargas) y `canberkkkkkk/ema-lightning` (01-oct,
  370 likes, 20.310 descargas). No hay rol de voz/TTS en `modelos_por_tarea.yaml` ni evidencia de que el
  pipeline de video necesite otro motor -> fuera del ambito del registro.
- ASR: `FermionResearch/Phonon-2` (28-sep, 287 likes, cc-by-4.0, base parakeet-tdt-0.6b-v3). La transcripcion
  del lab va con whisper en CPU y no hay bucket ASR declarado.
- `lightx2v/Qwen-Image-2.1-PE` y `JetBrains/Mellum2-12B-A2.5B`: la API devolvio 401 (gated) hoy -> no se
  registra nada que no se haya podido comprobar.

## Estado del registro tras esta corrida
58 candidatos: 9 EN_USO, 4 PENDIENTE, 20 OBSERVAR, 25 DESCARTADO. Sin duplicados.
Pendientes heredados: 4 (el mas viejo, `Ministral-3-14B-Instruct`, en cola desde el 24-ago-2026 -> 7 semanas).

## Reglas respetadas
No se ha descargado ni cargado ningun modelo. No se ha tocado n8n, Docker ni systemd. Sin sudo.
Todas las cifras de tamano/licencia/fechas/descargas salen de la API de HuggingFace y de la API de GitHub
consultadas el 12-oct-2026; velocidad y calidad que no existen en fuentes verificables figuran como
"no publicado". Ninguna entrada previa del registro se ha borrado ni re-investigado.
