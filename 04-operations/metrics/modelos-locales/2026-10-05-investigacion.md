# Investigacion semanal de modelos locales — 2026-10-05

Cron: `investigacion-modelos-locales-semanal` (v2). Hardware objetivo: RTX A2000 12GB.
Registro (memoria del cron): `04-operations/metrics/modelos-locales/candidatos-modelos-locales.json`
Backup previo a esta escritura: `candidatos-modelos-locales.json.bak-2026-10-05-1405`.

## Metodo de esta corrida
1. Lectura del registro persistente (41 entradas antes de hoy), `01-knowledge/modelos_por_tarea.yaml`,
   `alucinaciones_ledger.jsonl`, y busqueda de cada nombre candidato en `01-knowledge/experiments/` y
   `01-knowledge/objects/` (0 coincidencias para los nombres nuevos -> ninguno estaba ya probado por el lab).
2. Barrido web: agregador semanal (localmodelwatch, semana 1 de octubre + archivo 09/2026 + paginas 2-3),
   busquedas en HuggingFace (trending + listado de GGUF), r/LocalLLaMA, y verificacion por API de HuggingFace
   (`?blobs=true` para tamanos reales por fichero) y por API de GitHub (estado del PR de llama.cpp).
3. Filtro: solo modelos publicados o con cambio material del 21-sep al 05-oct-2026, que quepan (o MoE con offload
   viable) y con GGUF publicado o promesa de mejora real sobre el inventario. Todo lo que ya estaba en el registro
   se ha SALTADO (no se re-investiga ni se re-lista).

## Novedades registradas hoy (9 entradas nuevas, avisado=false)

### 1. Cloudflare `clef` / `clef-flash` — OBSERVAR
- Pesos el 30-sep-2026, Apache-2.0. NO son LLM de texto: reciben estado (texto/JSON/imagen/video) + esquema de
  preguntas tipadas y devuelven probabilidad por opcion en un solo forward pass, sin parseo de salida. API
  declarada compatible con Jev y SystemOne.
- `clef-flash` = 9B (base Qwen3.5-9B + encoder de vision), 262.144 ctx. `clef` = 27B (base Qwen3.8-27B).
- GGUF: `ggml-org/Clef-Flash-GGUF` (02-oct) Q4_K_M **6,49GB** / Q8_0 9,66GB / BF16 18,16GB;
  `bartowski/Cloudflare_clef-flash-GGUF` (01-oct, 12.661 descargas) desde IQ2_M 3,54GB / Q3_K_M 4,48GB + mmproj 0,92GB.
- `clef` (27B) NO cabe: ggml-org Q4_K_M 19,23GB; en bartowski solo a ~2 bpw (IQ2_XS 8,85GB).
- SOPORTE verificado: PR **29831** de llama.cpp ("model: add support for clef decision model (**text-only**)"),
  **merged el 03-oct-2026** -> el camino de texto entra en upstream; imagen/video del GGUF no lo cubre ese PR.
- tok/s en A2000: no publicado. Calidad: tabla del model card (Decision Index 0.2.1) + prueba propia de
  localmodelwatch; sin reproduccion independiente.
- Encaje: no hay rol clasificador en el lab (routeo rule-based) -> NO entra en cola. Es el candidato local mas
  directo para los futuribles **F1/F2** del analisis Jev (18-sep), que siguen esperando su senal de activacion.

### 2. `OpenJev` / `APUS-OpenJev-v1` — OBSERVAR
- Clones abiertos de Jev (decision de un solo paso). NO caben: `openjev/openjev` 27B (cc-by-nc-4.0, Q4_K_M ~16,5GB)
  ni `ggml-org/OpenJev-GGUF` (27,4B, cc-by-nc-4.0, Q4_K_M 18,97GB / Q8_0 28,6GB / BF16 53,81GB).
- SI caben las variantes `APUS-OpenJev-v1` (**apache-2.0**, GGUF del 23-sep para Ollama/llama.cpp/LM Studio):
  4B Q4_K_M 2,71GB / Q8_0 4,48GB; 9B Q4_K_M 5,63GB / Q8_0 9,53GB / BF16 17,92GB.
- Cifras del publicador (llama-server b11118, RTX PRO 6000; sin reproduccion independiente): 9B **68/80 = 85,00%**
  tanto en Q8_0 como en Q4_K_M con imatrix; el 27B se declara a 1,4 puntos del Jev hospedado.
- Se ejecuta en stock: `ollama run hf.co/apus-ailab/APUS-OpenJev-v1-9B-GGUF:Q8_0 --think=false`.
- Encaje: igual que clef -> sin rol clasificador, NO entra en cola; queda como alternativa Apache-2.0 (no NC) para F1/F2.

### 3. `Altworld/Hemmingway-1` (27B escritura) — OBSERVAR
- Pesos el 20-sep-2026, **cc-by-nc-4.0** (no comercial). 834 likes / 10.205 descargas. 27B denso sobre Qwen3.5-27B
  (config.json: Qwen3_5ForCausalLM, 64 capas, hidden 5120, 262.144 ctx, sin expertos).
- Card con comparativa de juez humano propio: "26 puntos por delante del siguiente modelo"; en peticiones dificiles
  **72%** frente a 9% de GPT-6 Astra. Cifras del vendedor, sin reproduccion independiente.
- GGUF bartowski (02-oct): IQ2_XS 9,09 / IQ2_M 10,52 / Q2_K 10,82 / IQ3_XXS 12,32 / Q3_K_S 12,74 / Q3_K_M 13,40 /
  IQ4_XS 15,48 / **Q4_K_M 17,44** / Q5_K_M 20,92 / Q6_K 23,86 GB.
- Conclusion: en 12GB SOLO entra a 2-3 bits, y el 4-bit real NO cabe -> se degradaria justo la prosa que lo hace
  interesante. Rol `redaccion_creatividad` ya cubierto por gemma-4-12b-qat; segundo motivo: licencia NC. NO entra en cola.

### 4. `google/DiarizationLM-Gemma-4-E4B-v1` — OBSERVAR
- 04-oct-2026, Apache-2.0, 18 likes / 880 descargas. Gemma 4 E4B afinado para diarizacion/transcripcion
  (quien habla y cuando; variantes palabra/utterance, con y sin timestamps).
- **GGUF oficiales en el propio repo**: q4_0 5,15GB y q4_k_m 5,30GB -> cabe holgado. tok/s en A2000: no publicado.
- Cubriria un rol que hoy NO existe (whisper CPU sin etiquetas de hablante). Queda OBSERVAR hasta que haya
  necesidad real de diarizacion en el pipeline de video.

### 5. `allenai/AstaBrief_8B` (informe con citas) — OBSERVAR
- Ai2, Apache-2.0, 8B, **solo ingles**: pregunta de investigacion + extractos recuperados -> informe CON CITAS
  (SFT + DPO offline; card: base_model `AstaBrief_8B_SFT`, dataset `AstaBrief_DPO_Mix`).
- Entra por cambio material (repo base de feb-2026, SFT 10-sep, GGUF de terceros 02-oct):
  `mradermacher/AstaBrief_8B-GGUF` Q2_K 3,28 / Q3_K_M 4,12 / IQ4_XS 4,59 / Q4_K_M 5,03 / Q5_K_M 5,85 GB (1.053 descargas).
- Se parece al flujo RAG+informe del lab, pero en ingles y sobre literatura cientifica; `redaccion_datos` ya cubierto
  por gemma-4-12b-qat en espanol. NO entra en cola.

### 6. `Aleph-Alpha/Kolibri-1` — DESCARTADO (tamano)
02-oct-2026, Apache-2.0, 518 likes. MoE **78B totales / 3,46B activos**, 384 expertos enrutados (6 por token) + 1
compartido, 1M ctx por extrapolacion, pesos FP8. Card: "~78 GB (FP8 weights). Minimum: 2x A100 80GB, 2x H100 SXM5,
1x H200, 1x B200 or 1x B300". GGUF de terceros (Hob-forge, 03-oct): Q4_K_M **47,45GB**, Q8_0 83,14GB. No cabe ni con
offload util. Motivo secundario: tokenizador orientado al aleman.

### 7. `NaiveAI/Naive-N0.5-Flash` — DESCARTADO (tamano)
27-sep-2026, MIT, 166 likes / 2.036 descargas. Repo de **617,8GB** en 49 shards (los mayores de 13,09GB, ~300B a BF16);
sin GGUF verificado. No cabe ni de lejos.

### 8. `ELYZA-Thinking-1.0` (llm-jp-4 32B-A3B / 33B) — DESCARTADO (tamano + idioma)
02-oct-2026, Apache-2.0. GGUFs de terceros (mmnga-o, 03-oct): 32B-A3B Q3_K_S 15,39GB / Q4_K_M 21,4GB;
33B Q3_K_S 14,67GB / Q4_K_M 20,16GB. El build mas pequeno (14,67GB) ya supera los 12GB de la A2000. Foco japones.

### 9. Bucket "otros detectados (28-sep a 05-oct)" — DESCARTADO
`fastino/GLiNER2.5-Decide`, `SupersonicLabs/Julia-1`, `PSRben/VisionHOPE`, `bartowski/FrogNano-4B-2609-GGUF`,
`bartowski/Lythri_Lythri-4B-A2B-GGUF`, `bartowski/OmniJev_OneJev-9B-GGUF`. Sin rol nuevo (vision = glm-4.6v-flash;
routeo = rule-based; tool calling = granite-4.x / MiniCPM5 en cola) y sin evaluacion de terceros. Se registran como
bucket para no volver a investigarlos; tamaños concretos NO re-verificados hoy (se descartan por rol, no por tamano).

## Cambios materiales en entradas YA existentes (no son novedades)
- **Qwen3.8-27B-GSQ-RCO** (PENDIENTE / RE-PROBAR): el repo `ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF` (1.965 likes,
  1.614.312 descargas) incluye ahora IQ2_XS **8,42GB** (8,77GB con -mtp), IQ2_S 9,26GB, IQ3_XXS 10,09GB, IQ3_S 11,77GB,
  + imatrix 0,01GB y mmproj BF16 0,93GB -> mas margen que el 9,3GB anotado el 14-sep, pero sigue siendo ~2 bpw sobre un
  27B denso. Veredicto sin cambios; sigue sin EXP asociado.
- **GLM-5.3-Flash** (DESCARTADO): ya existe GGUF oficial (`ggml-org/GLM-5.3-Flash-GGUF`, 03-oct): Q2_K 133,8GB /
  Q4_K 181,4GB / mmproj 0,65GB / MTP 4,95-9,28GB. Sigue fuera de 12GB por un factor de ~12.

## Detectado pero NO registrado
- `TaichuAI/ZDTaichu5.0-9B`: creado el 04-sep-2026 -> fuera de la ventana de 2 semanas.
- `LiquidAI/LFM2.5-350M-Diffusion-Exp`: repo no verificable hoy (gated) -> no se registra nada que no se haya comprobado.
- `ELYZA-Thinking-1.0-33B` (ficha suelta): 401; los repos reales son los de llm-jp-4 (registrados arriba como descarte).

## Estado del registro tras esta corrida
50 candidatos: 9 EN_USO, 4 PENDIENTE, 14 OBSERVAR, 23 DESCARTADO. Sin duplicados.
Pendientes heredados: 4 (el mas viejo, `Ministral-3-14B-Instruct`, en cola desde el 24-ago-2026 -> 6 semanas).

## Reglas respetadas
No se ha descargado ni cargado ningun modelo. No se ha tocado n8n, Docker ni systemd. Sin sudo.
Todas las cifras de tamano/licencia/fechas salen de la API de HuggingFace o de la API de GitHub el 05-oct-2026;
las de velocidad y calidad que no existen en fuentes verificables figuran como "no publicado".
