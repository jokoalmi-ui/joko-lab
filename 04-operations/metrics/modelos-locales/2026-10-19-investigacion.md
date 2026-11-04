# Investigacion semanal de modelos locales — 2026-10-19

Cron: `investigacion-modelos-locales-semanal` (v2). Hardware objetivo: RTX A2000 12GB.
Registro (memoria del cron): `04-operations/metrics/modelos-locales/candidatos-modelos-locales.json`
Backup previo a esta escritura: `candidatos-modelos-locales.json.bak-2026-10-19` (58 entradas -> 65).

## Metodo de esta corrida
1. PASO 0: lectura del registro (58 entradas antes de hoy), `01-knowledge/modelos_por_tarea.yaml`
   (roles: veracidad_critica qwen3.6-35b-a3b, vision glm-4.6v-flash, codigo, redaccion gemma-4-12b-qat,
   grounding r1-distill-14b, razonamiento gpt-oss-20b; buckets generacion_imagen = ComfyUI/SDXL,
   transcripcion), `alucinaciones_ledger.jsonl` (0 coincidencias con los nombres nuevos) y busqueda de cada
   nombre nuevo en `01-knowledge/experiments/` y `01-knowledge/objects/` -> 0 coincidencias, ninguno estaba
   ya probado por el lab (no hay EXP que cite estos modelos).
2. Barrido 05-oct a 19-oct: API de HuggingFace por autor (Qwen, google, ibm-granite, mistralai, unsloth,
   LiquidAI, allenai, HuggingFaceTB, microsoft, nvidia) filtrando `createdAt`, feed de `createdAt` por
   pipeline_tag, busquedas por nombre y `?blobs=true` para tamanos reales por fichero. Estado real de cada PR
   citado via API de GitHub (no por el texto del PR).
3. Filtro: solo publicado o con cambio material en las ultimas 2 semanas, que quepa en 12GB (o MoE con offload
   viable), con GGUF publicado o convertible. Todo lo que ya estaba en el registro se ha SALTADO (no se
   re-veredicta ni se re-lista).

## Novedades registradas hoy (7 entradas nuevas, avisado=false; 4 OBSERVAR + 3 DESCARTADO)

### 1. OpenBMB `MiniCPM-V-4.7` (1B + 35B-A3B) — OBSERVAR
- Cambio clave: el 12-oct figuraba como "pesos NO publicados de forma verificable"; **ya lo estan**.
  Repos 06-07-oct, apache-2.0: 35B-A3B 35.212.875.824 params (1.033 likes / 76.410 descargas); 1B (390 / 33.388).
- GGUF **oficiales** del 06-oct: 35B-A3B-gguf (169 likes / 170.728 descargas), 1B-gguf (88 / 53.412).
  Tamanos verificados: 35B-A3B **IQ3_XS 14,48GB** / IQ3_M 15,44GB / Q4_K_M ~21GB, + mmproj F16 1,12GB
  -> NO cabe entero en 12GB (solo con offload de expertos, 3B activos). 1B **Q4_K_M 0,65GB** + mmproj
  -> ~0,8GB, cabe de sobra.
- Soporte: PR **29416** "[Model] Support MiniCPM-V 4.7" **merged 10-oct** -> builds actuales lo cargan;
  la card declara llama.cpp/Ollama. LM Studio: no verificado. Trae drafter **DSpark** (0,79GB en 35B,
  0,44GB en 1B) para decodificacion especulativa, que mitigaria la lentitud del offload.
- Calidad: la card solo publica graficos Pareto, **sin tabla numerica** -> "no publicado" en texto; sin fuente
  independiente. Encaje: el rol `vision` ya lo cubre glm-4.6v-flash (7/7, 26,4 tok/s, 9.984 MiB).
  Unico test barato: el 1B (~0,8GB). El 35B no compite en velocidad con esa VRAM.

### 2. NVIDIA `Nemotron Labs Dory 1.0 4B` — DESCARTADO (sin soporte upstream)
- 16-oct-2026, licencia `other` (OpenMDW), 127 likes / 1.779 descargas (BF16). GGUF **oficial**
  `nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-GGUF` (40 likes / 5.196 descargas) con un unico quant verificado:
  **Q5_K_M 3,67GB** -> cabria de sobra en 12GB.
- Modelo "looped" (reutiliza capas): el vendor declara SWE-bench 61,8 **con 4 loops** (4x compute) e IFBench 79;
  conocimiento general flojo, orientado a codigo.
- Bloqueo real: llama.cpp PR **30306** sigue **DRAFT/abierto** (actualizado 17-oct) y vLLM PR **60149** abierto
  (19-oct) -> hoy no carga en llama.cpp ni LM Studio. Mismo criterio que K2-Horizon: DESCARTAR por soporte y
  **REABRIR** cuando entre en upstream (es el 4B de codigo con mejor pinta de la ventana).

### 3. NVIDIA `Nemotron 3.5 Bolt 74B-A9B` / `Super VL 120B-A12B` — DESCARTADO (tamano)
- Bolt 74B-A9B (07-15 oct): GGUF oficial **22,02GB**; unsloth (14-oct) con minimo **UD-IQ1_S 18,51GB**.
- Super VL 120B-A12B (12-15 oct): Q4_K_M ~82GB, UD-IQ2_XXS por shards. Soporte llama.cpp merged
  (PR **30520**, 15-oct) y GGUFs oficiales + unsloth, pero 18,51GB a 1 bit no cabe en 12GB y 9B activos con
  offload no es viable en A2000. Sin rol nuevo (el MoE de razonamiento ya lo cubre qwen3.6-35b-a3b).

### 4. LiquidAI `LFM2.5-24B-A2B` — OBSERVAR (no cabe entero)
- Pesos 09-oct, licencia `other`, 484 likes / 14.151 descargas; GGUF oficial del 09-oct (212 likes /
  120.509 descargas). Quant mas pequeno **QAD-Q4_0 13,58GB**; Q4_K_M 14,53GB; Q5_K_M 17,03GB.
- MoE 24B con ~2B activos -> offload de ~2-3GB seria viable, pero el rol MoE ya lo cubre qwen3.6-35b-a3b
  (7,7 tok/s medidos) y no hay dato de que este sea mas rapido. tok/s en A2000: **no publicado**.

### 5. IBM `granite-switch-4.1-8b` — OBSERVAR (sin GGUF publicado)
- Release final 4.1 el 14-oct-2026 (antes solo previews de mayo): 8.776.400.896 params (~8,8B), **apache-2.0**,
  30 likes / 980 descargas; tambien `granite-switch-4.1-30b` el mismo dia.
- Arquitectura "switch": adaptadores aLoRA embebidos -> sirve como chat Y como modelo de **decision**
  (`/v1/systemone`) sin invalidar cache. Soporte llama.cpp: PR **30676** merged **17-oct** (+30693, 256 opciones).
- No hay GGUF: busqueda por API solo devuelve `barha/granite-switch-4.1-3b-preview-GGUF` (preview 3B) -> habria
  que convertirlo (a Q4 ~5GB cabria). Mismo hueco que clef / d1-3B / h2o-lightning-4b, todos en OBSERVAR.

### 6. BFL `flux-3-image-klein` — OBSERVAR (generacion_imagen, ComfyUI)
- 13-14 oct: `flux-3-image-klein` (512 likes / 62.006 descargas), `-base`, **`-comfy` (873 / 393.062)** y `-pup`.
- GGUF de difusion de unsloth el 16-oct (17 likes / 6.396 descargas): **Q4_K_M 3,67GB** / UD-Q4_K_XL 3,93GB /
  Q8_0 6,09GB / BF16 11,1GB -> cabe entero en 12GB. Relevante para `generacion_imagen` (skill
  `generacion-imagen-local`; ComfyUI fuera de cgroup por OOM 18G/8,9G): 3,7GB de difusion reduce presion de VRAM.
- No hay evals de calidad ni tiempo por imagen en A2000 (**no publicado**). Estos GGUF no se cargan con
  LM Studio/llama.cpp, van en ComfyUI. No verificado que mejore el rotulado de las infografias, que es el punto critico.

### 7. Bucket 12-oct a 19-oct — DESCARTADO (para no repetirlos)
- `orcarouter/OrcaCyber-Nano-1.0` (16-oct, VLM de ciberseguridad, GGUF 13G/15,7G + mmproj -> no cabe, gated, sin rol);
  `Nemotron-3.5-Rerank-8B` (15-oct, reranker, sin rol); `microsoft/UserRepGen-4B` (14-oct, sin rol);
  `mistralai Timestral-5M/28M/123M/209M` (14-oct, series temporales, no LLM); `Voxtral-Mini-4B-Realtime-Arabic`
  y `LIDstral-Arabic` (08-oct, solo arabe); `allenai/HiRO-ACEv2` (12-oct, sin pesos); arquitectura `maion-coder`
  (PR 29778 merged 14-oct) sin pesos localizables; `DeepSeek-V4.1-Flash-1017` (17-oct, nombre fechado de familia
  ya DESCARTADA); `Muse-Spark-Open-816B-A42B` y `Beam-1.0-501B-A23B` (16-oct, fuera de rango).

## Actualizaciones de entradas ya existentes (solo nota + ultima_mencion)
- `Mellum2.1-12B-A2.5B-Thinking`: soporte **MTP merged** en llama.cpp (PR 30612, 16-oct) -> decodificacion
  especulativa nativa disponible. Sigue OBSERVAR (GGUF oficial Q4_K_M 8,07GB ya cabe).
- `Ternary-Bonsai-2-27B`: publicados los drafters especulativos el 19-oct. Sigue OBSERVAR.
- `LightOnOCR-3`: llama.cpp PR 30600 (15-oct) quita el forzado de lado mayor 1540 -> resolucion nativa por defecto.

## Estado del registro tras esta corrida
- 65 entradas: 9 EN_USO / 4 PENDIENTE / 24 OBSERVAR / 28 DESCARTADO.
- PENDIENTES HEREDADOS (4): Ministral-3-14B-Instruct (24-ago, **56 dias / 8 semanas**), Qwen3.8-27B-GSQ-RCO
  (07-sep), MiniCPM5-2B (21-sep), Qwen-Image-2.1 (28-sep). El mas viejo lleva 8 semanas sin ejecutarse.
- No se ha descargado, cargado ni probado ningun modelo; no se ha tocado n8n, Docker ni systemd.
