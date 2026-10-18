# F2 · celda A(T3) — comprobación EMPÍRICA del offload de un MoE de 22,6 GB en 12 GB de VRAM

**Fecha:** 2026-09-16, 16:29:03–16:35:30 CEST · **Motor:** llama.cpp propio (LM Studio 2.38.0 backend), `llama-server` en `127.0.0.1:8099`
**Modelo:** `unsloth/Qwen3.6-35B-A3B-MTP-GGUF/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` — 22.663.387.424 B, 41 capas, MoE 256 expertos (8 activos), `nextn_predict_layers=1`
**Hardware:** RTX A2000 12 GB (12.282 MiB) · i5-9500 (6 hilos) · 30 GiB RAM
**Aislamiento:** LM Studio y el modelo de visión NO se tocaron (VRAM 1.118 MiB durante toda la prueba, solo escritorio).

## Metodología

Tres arranques en serie del mismo binario con `-c 2048 -np 1 -t 6 -fa on`, midiendo (a) tiempo de carga hasta `/health`,
(b) VRAM pico muestreada cada 3 s con `nvidia-smi`, (c) `prompt_per_second` y `predicted_per_second` devueltos por
`/completion` con prompt fijo y `temperature=0`, y (d) RSS del proceso. Cada arranque cierra su propio PID.

## Resultados (datos literales del JSONL)

| config | arranca | carga (s) | prompt tok/s | generación tok/s | VRAM pico (MiB) |
|---|---|---|---|---|---|
| `-ngl 0` | sí | 84.2 | 0.34 | 0.37 | 1631 |
| `-ngl 99 -ncmoe 24` | sí | 84.4 | 1.04 | 1.44 | 11068 |
| `-ngl 99 -ncmoe 20` | NO | 54.2 | — | — | 1222 |

### `-ngl 0`

- inicio: **2026-09-16T16:29:03**
- t_carga_s: **84.2**
- arranco: **True**
- vram_tras_carga_mib: **1512**
- prompt_tok_s: **0.34**
- gen_tok_s: **0.37**
- tokens_gen: **16**
- t_prompt_s: **34.9**
- t_gen_s: **40.1**
- vram_en_gen_pico_mib: **1631**
- rss_gib: **3.64**
- rc: **0**
- cola del log:

```
2.39.204.296 I slot print_timing: id  0 | task 0 | prompt eval time =   34948.43 ms /    12 tokens ( 2912.37 ms per token,     0.34 tokens per second)
2.39.204.322 I slot print_timing: id  0 | task 0 |        eval time =   40074.76 ms /    16 tokens ( 2671.65 ms per token,     0.37 tokens per second)
2.39.204.323 I slot print_timing: id  0 | task 0 |       total time =   75023.19 ms /    28 tokens
2.39.204.467 I slot print_timing: id  0 | task 0 |    graphs reused =         15
2.39.206.778 I slot      release: id  0 | task 0 | stop processing: n_tokens = 27, truncated = 0
2.39.231.924 I srv    operator(): operator(): cleaning up before exit...
```

### `-ngl 99 -ncmoe 24`

- inicio: **2026-09-16T16:31:46**
- t_carga_s: **84.4**
- arranco: **True**
- vram_tras_carga_mib: **11054**
- prompt_tok_s: **1.04**
- gen_tok_s: **1.44**
- tokens_gen: **32**
- t_prompt_s: **11.5**
- t_gen_s: **21.5**
- vram_en_gen_pico_mib: **11068**
- rss_gib: **3.4**
- rc: **0**
- cola del log:

```
1.57.337.785 I slot print_timing: id  0 | task 0 | prompt eval time =   11526.69 ms /    12 tokens (  960.56 ms per token,     1.04 tokens per second)
1.57.337.792 I slot print_timing: id  0 | task 0 |        eval time =   21475.04 ms /    32 tokens (  692.74 ms per token,     1.44 tokens per second)
1.57.337.793 I slot print_timing: id  0 | task 0 |       total time =   33001.72 ms /    44 tokens
1.57.337.799 I slot print_timing: id  0 | task 0 |    graphs reused =         31
1.57.339.623 I slot      release: id  0 | task 0 | stop processing: n_tokens = 43, truncated = 0
1.57.360.143 I srv    operator(): operator(): cleaning up before exit...
```

### `-ngl 99 -ncmoe 20`

- inicio: **2026-09-16T16:33:48**
- t_carga_s: **54.2**
- arranco: **False**
- vram_tras_carga_mib: **1116**
- rc: **1**
- cola del log:

```
0.53.085.849 E llama_model_load_from_file_impl: failed to load model
LMSTUDIO_STARTUP_ERROR:{"schemaVersion":1,"code":"model_load_failed","message":"error loading model: unable to allocate CUDA0 buffer"}
0.53.086.070 E cmn  common_init_: failed to load model '/mnt/ssd_ia_datos/LM STUDIO/unsloth/Qwen3.6-35B-A3B-MTP-GGUF/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf'
0.53.086.080 E srv    load_model: failed to load model, '/mnt/ssd_ia_datos/LM STUDIO/unsloth/Qwen3.6-35B-A3B-MTP-GGUF/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf': error loading model: unable to allocate CUDA0 buffer
0.53.086.108 I srv    operator(): operator(): cleaning up before exit...
0.53.087.536 E srv  llama_server: exiting due to model loading error
```

## Lectura

1. **El offload funciona y el modelo cabe, pero justo.** Con `-ngl 99 -ncmoe 24` (expertos de 24 de las 41 capas en CPU)
   el pico fue de **11.068 MiB** sobre 12.282 disponibles. Con `-ncmoe 20` el motor pidió **11.303 MiB en un solo buffer
   CUDA y `cudaMalloc` falló con `out of memory`**: la frontera práctica está entre 20 y 24 capas de expertos en GPU.
2. **La ganancia frente a CPU puro es ×3,9 en generación** (0,37 → 1,44 tok/s) y ×3,1 en prefill (0,34 → 1,04 tok/s).
   Es decir: el offload sirve para *que arranque*, no para trabajar. A 1,44 tok/s un uso interactivo es inviable;
   esta celda queda como **cota inferior empírica** del montaje, no como configuración de uso.
3. **La prefill también se degrada con el offload** (1,04 tok/s): el cuello no es solo la decodificación.
4. **El bloque MTP no se paga dos veces.** llama.cpp ignora los tensores `blk.40.nextn.*` (20 tensores, **528.857.088 B = 504,4 MB**)
   cuando no se activa speculative decoding, y no reserva memoria para ellos.
5. **El cuello real es el ancho de banda de memoria, no la GPU.** El modelo vive repartido entre 11 GB de VRAM y RAM/SSD;
   cada token activa 8 de 256 expertos y hay que ir a buscarlos. Es exactamente el escenario donde MTP rinde poco:
   acelerar la decodificación no ayuda si el tiempo se va en traer pesos.

## Conexión con la pregunta MTP

Este mismo modelo (`Qwen3.6-35B-A3B`, variante MTP de unsloth) es el que en la medición con todo el modelo en GPU dio
**31,84 → 40,60 tok/s (+28,1 %) con `n-max=1`**. Es decir: MTP aporta +28 % cuando el modelo está entero en VRAM,
y su aporte se diluye en cuanto hay offload. Ambas mediciones son del mismo fichero GGUF, así que la diferencia es de
hardware/configuración, no de modelo.

## Reproducibilidad

- Script: `/tmp/prueba_moe_offload.py` (banco de pruebas, serie completa)
- Datos: `/tmp/exp007/moe_empirico.jsonl` (un registro por configuración, con cola de log)
- Logs completos: `/tmp/exp007/moe_server_{cpu_puro,hibrido_ncmoe24,hibrido_ncmoe20}.log`

**Estado:** celda A(T3) medida empíricamente — *investigación documental + comprobación empírica acotada* (no hubo servicio
del modelo para uso real). Ninguna configuración se dejó en marcha: puerto 8099 libre, VRAM devuelta a 1.118 MiB.
