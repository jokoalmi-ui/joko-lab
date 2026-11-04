# Caché de expertos MoE en GPU (`--moe-cache-mib`) en A2000 12 GB

Fecha: 2026-10-18 23:05 CEST
Hardware: i5-9500, 32 GB RAM (30 GiB visibles), RTX A2000 12 GB (12.282 MiB)
Backend: llama.cpp build `2a66703` (0.7.0-dev) incluido en LM Studio 2.60.0

## Qué se ha medido

El flag `--moe-cache-mib N` (env `LLAMA_ARG_MOE_CACHE_MIB`) mantiene N MiB de
expertos MoE en VRAM aunque el resto del modelo viva en RAM vía `-cmoe`.
Viene del PR ggml-org/llama.cpp#29887, **mergeado el 2026-10-13**. Ya está
presente en el binario del backend que usa el lab:

    $ llama-server --help | grep moe-cache
    --moe-cache-mib N   GPU cache size in MiB for the MoE experts kept in the CPU

Modelo: `gpt-oss-20b-MXFP4.gguf`, 12,11 GB (MoE, 3,6B activos).
Comando base: `-cmoe -ngl 99 -c 4096 -t 6 --flash-attn on --jinja`.
Medición: endpoint `/completion`, `temperature 0`, `top_k 1`, `cache_prompt false`,
128 tokens, 2 rondas, timings nativos del servidor.

## Resultados

| `--moe-cache-mib` | tok/s (media) | tok/s r1 / r2 | VRAM tras carga |
|---|---|---|---|
| 0 (off) | 13,23 | 12,22 / 14,25 | 4.082 MiB |
| 1.024 | **5,39** | 5,07 / 5,72 | 5.104 MiB |
| 2.048 | 8,54 | 8,39 / 8,70 | 6.129 MiB |
| 4.096 | 16,77 | 15,64 / 17,89 | 8.171 MiB |
| 6.144 | **30,11** | 30,36 / 29,85 | 10.225 MiB |

Test largo de validación (220 tokens, prompt de prosa): off 12,87 tok/s →
6.144 MiB **40,30 tok/s** (+213 %).

La VRAM asignada coincide exactamente con el valor pedido (+1.022 / +2.047 /
+4.089 / +6.143 MiB), lo que confirma que la caché está activa. El log del
servidor no imprime el desglose de buffers, así que la verificación es por
`nvidia-smi`.

## Hallazgo principal: no es "más es mejor"

Con 1.024 y 2.048 MiB el rendimiento **cae por debajo del baseline sin caché**
(5,4 y 8,5 frente a 13,2 tok/s). Con esa caché tan pequeña los expertos activos
no caben, se produce thrashing de copias RAM→GPU y encima se resta memoria al
KV. El umbral útil en esta GPU está en ~4 GiB; a partir de ahí la curva sube.

## La salida no es bit-idéntica

Mismo prompt, temp 0, 220 tokens, off vs 6.144 MiB: similitud **0,7076**,
primera divergencia en el carácter 437. El contenido es equivalente (misma
calidad, mismo tema, mismos datos), pero la redacción diverge porque el orden
de acumulación en punto flotante cambia según el experto se evalúe en GPU
(cacheado) o en CPU. No es un defecto del flag: es aritmética distinta.

## Límites reales en este equipo

- **qwen3.6-35b-a3b_moe** (20,27 GB, el MoE grande del store) necesita ~17-18 GB
  de expertos residentes en RAM. Con 30 GiB totales y ~16 GiB disponibles no
  entra sin liberar memoria (navegador, Thunderbird, procesos Python).
- Con 6.144 MiB de caché la VRAM queda en 10.225 de 12.282 MiB: ~2 GB de
  margen. Subir contexto a 8k recorta ese margen.
- Docker en este equipo consume solo ~810 MB (7 contenedores); no es el
  problema de RAM.
- `gpt-oss` razona antes de responder: con `max_tokens` cortos el campo
  `content` sale vacío y el texto aparece en `reasoning_content`.

## Executor

`~/joko-lab/05-inference/executors/local/moe-cache-server.sh` (start|status|stop,
`--mib --ctx --port --modelo`). Verificado end-to-end:

    $ moe-cache-server.sh start --mib 6144 --ctx 4096
    OK pid=577396 puerto=8098 ctx=4096 mib=6144 modelo=gpt-oss-20b-MXFP4.gguf vram=10230 MiB

    $ curl .../v1/chat/completions  ->  content "París.", reasoning aparte, 46 tokens
    $ moe-cache-server.sh stop     ->  parado, vram=2393 MiB

Avisa si la RAM disponible es menor que el tamaño del modelo antes de arrancar.

## Conclusión

La técnica es real y ya está disponible sin compilar nada: **+128 % a +213 %**
en gpt-oss-20b con 6 GiB de caché en una GPU de 12 GB. El requisito es que el
modelo MoE entre en RAM; el 125B de Strata (66-84 GB) sigue fuera de este
equipo con 32 GB.

## Pendiente para la próxima sesión (equipo en frío)

**Barrido `--ncmoe N` con Qwen3.6-35B-A3B** contra el baseline de LM Studio
(~7,7 tok/s), con swap vacío y sin navegador abierto.

Contexto medido el 18-10 en condiciones NO válidas (swap al 100 %):
`-cmoe` + `--moe-cache-mib 6144`, ctx 4096 → arranca en 54 s, VRAM 11.494 de
12.282 MiB, **4,73 tok/s** de escritura y **2,01 tok/s** de lectura de prompt.
Sin baseline y con la máquina paginando, la cifra NO es publicable; solo
indica que el offload total es peor que los 7,7 tok/s actuales.

Para el barrido hace falta añadir `--ncmoe N` al executor (hoy solo tiene
`-cmoe` total) y medir 20/22/24 capas en GPU con caché 4096-6144, cada valor
con su baseline contemporáneo y comprobando el pico de VRAM en la recarga.

