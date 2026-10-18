# EXP-20261009-008 — F0/F1: ejecución y barrido (2026-10-09, 18:11-18:36 CEST)

**Ejecutor:** Hermes (deepseek-v4-flash) en sesión Telegram, en nombre de Joseba. Ejecución **secuencial, una variable por paso**.
**Alcance:** ventana aislada `:8099`. NO se tocó n8n, Ollama (`:11434`), el puerto `:1234` de LM Studio, ComfyUI ni Docker. Se escribió solo `/tmp/exp008/` y esta carpeta.

## F0 — Precondiciones: lo que se hizo y lo que NO

| Paso | Estado | Evidencia |
|---|---|---|
| Descargar el VLM GLM 4.6V (`lms unload`) | HECHO | `lms ps` al cierre: «No models are currently loaded»; VRAM usada 1.681/12.282 MiB al terminar |
| Esperar el ciclo del indexer (PID **2470**, servicio `joko-indexer`) sin matarlo | HECHO | journal: 17:53:01 → 18:10:39 → «1.591 re-embebidos, 44.309 conservados» |
| Comprobar `:8099` libre | HECHO | libre al arrancar cada celda |
| **Liberar RAM / vaciar swap** | **NO HECHO** | **swap 8.191/8.191 MiB (100 %) durante TODA la medición** |
| **ComfyUI (`:8188`, 190 MiB)** | **se dejó corriendo** | co-variable declarada |

**Consecuencia declarada:** el criterio de entrada del diseño («no medir con swap en uso») **no se cumple**. Las cifras absolutas incluyen el coste de paginación; lo válido es la **comparación intra-sesión con baseline intercalado**.

**Ficha de recarga pendiente (estado a restaurar):** `glm-4.6v-flash` — context 21504, parallel 4 (recargar con el patrón autorizado `lms load glm-4.6v-flash -y` y verificar en `lms ps`). `text-embedding-bge-m3` no se descargó (TTL 1 h, caduca solo).

## F1 — Instrumento y validación

1. **El flag existe en el binario usado:** `--help` de `llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.55.0` con `LD_LIBRARY_PATH` al vendor CUDA se imprime y contiene `--moe-cache-mib` ✅
2. **Reparto que arranca (medido, no supuesto):** con `-ngl 99 -ncmoe 24`, `-c 4096 -ub 512` → los pesos cargan pero **falla la creación de los compute buffers** (`cudaMalloc` OOM de 300 MiB). Con `-c 2048 -ub 128` el mismo reparto arranca; y como la caché necesita margen de VRAM, se fijó **`-ncmoe 28`** (VRAM tras carga 10.056 MiB → margen 2.210 MiB). **Desviación declarada** respecto al diseño (N=24, ctx 4096, ub 512).
3. **Control de dirección conocida:** `-ngl 0` (CPU puro) = **2,055 tok/s** vs híbrido C=0 = **5,55 tok/s** → ×2,7 (OBS-111 midió ×3,9 con otro fichero/quant: se compara solo el signo) ✅
4. **Techo de VRAM del barrido:** pico de la baseline (C=0) = **10.135 MiB** de 12.282 (escritorio ≈2.150 MiB). Margen ≈2.150 MiB → C=2048 no cabe (OOM), C=1024 sí.

Config fija por celda (no varía): `-m Qwen3.6-35B-A3B-MXFP4_MOE.gguf` (20.267.153.760 B), runtime 2.55.0, `-ngl 99 -ncmoe 28 -c 2048 -ub 128 -t 6 --no-warmup`, `n_predict=128`, `temp=0`, `seed=1234`, `ignore_eos`, sin cache de prompt, endpoint `/completion` (timings nativos). Una carga completa por celda.

## Tabla de celdas

**E1 — entrada ESTRUCTURADA** (lista JSON de 12 objetos; 55 tokens de prompt)

| Celda | C (MiB) | tg tok/s | prefill tok/s | carga (s) | VRAM pico (MiB) | RSS fin (MB) | text_md5 |
|---|---|---|---|---|---|---|---|
| E1_C0000 | 0 | **5,235** | 3,749 | 42 | 10.135 | 10.525 | 36c5a8f0a9da… |
| E1_C0000_R2 | 0 | **5,729** | 3,985 | 42 | 10.258 | — | 36c5a8f0a9da… |
| E1_C0000_R2b | 0 | **5,673** | 4,389 | 45 | 9.673 | — | 36c5a8f0a9da… |
| E1_C0256 | 256 | **7,471** | 3,759 | 39 | 10.358 | 9.827 | 36c5a8f0a9da… |
| E1_C0512 | 512 | 6,719 *(contaminada)* | 0,536 | 63 | 10.647 | 10.004 | 36c5a8f0a9da… |
| E1_C0512_R2 | 512 | **8,954** | 4,124 | 36 | 10.772 | — | — |
| E1_C1024 | 1024 | **8,518** | 3,410 | 45 | 11.165 | 9.411 | 36c5a8f0a9da… |
| E1_C1024_R2 | 1024 | **9,007** | 4,052 | 51 | 11.299 | — | — |
| E1_C1024_R2b | 1024 | **8,083** | 5,405 | 48 | 10.680 | — | — |
| E1_C2048 | 2048 | **OOM** | — | 33 | (9.762 antes de morir) | — | — |

**E2 — entrada PROSA** (3 párrafos sobre dispersión de Rayleigh; 65 tokens de prompt)

| Celda | C (MiB) | tg tok/s | prefill tok/s | carga (s) | VRAM pico (MiB) | text_md5 |
|---|---|---|---|---|---|---|
| E2_C0000 | 0 | **7,542** | 5,212 | 39 | 9.650 | `c8640783…` (595 chars) |
| E2_C1024 | 1024 | **11,878** | 4,633 | 36 | 10.679 | `36f1ac76…` (597 chars) |

**Control**

| Celda | config | tg tok/s | VRAM pico | RSS fin |
|---|---|---|---|---|
| CTL_ngl0_CPU | `-ngl 0` (16 tokens) | **2,055** | 2.035 | 15.987 MB |

## Ruido medido y comparación intercalada (ronda 2)

| Clase | C=0 (n=3) | C=1024 (n=3) | ratio |
|---|---|---|---|
| E1 | 5,235 · 5,729 · 5,673 → **media 5,546** (banda 9,4 %) | 8,518 · 9,007 · 8,083 → **media 8,536** (banda 11,4 %) | **×1,54 (+54 %)** |
| E2 | 7,542 (n=1) | 11,878 (n=1) | **×1,58 (+58 %)** |

**Los rangos de las réplicas NO se solapan** (E1: [5,24;5,73] vs [8,08;9,01]) → el efecto está muy por encima del ruido medido.

**Celda contaminada:** `E1_C0512` (ronda 1) sufrió un atasco externo de disco/swap (prefill 0,536 tok/s, 121 s de generación) → se descarta y su valor limpio es el de la ronda 2 (**8,954**).

## Observaciones de mecanismo

- **La caché se asigna al cargar, y se paga en VRAM:** el pico crece ≈ +C MiB (10.135 → 10.358 → 10.647 → 11.165 para 0/256/512/1024).
- **C=2048 no arranca** y el log lo dice sin ambigüedad: `failed to allocate CUDA0 buffer of size 2147450880` (2048 MiB) → `failed to initialize the context: failed to allocate the MoE cache buffers`.
- **Salida idéntica en E1, NO en E2:** las cuatro celdas E1 de la ronda 1 produjeron el **mismo `text_md5`** (`36c5a8f0…`) → en E1 la caché no altera el texto a `temp=0`. **En E2 sí cambia**: `c8640783…` (595 chars) con C=0 frente a `36f1ac76…` (597 chars) con C=1024 → la ruta con caché puede variar un token respecto a la ruta sin caché (orden de reducción distinto). No es mejora ni degradación medida: es un **límite al determinismo entre configuraciones**.
- **Saturación temprana:** la ganancia grande ya está con **256 MiB** (×1,35); a partir de 512 MiB se aplana en ≈8,5-9 tok/s (más caché no compra más, solo consume VRAM).
