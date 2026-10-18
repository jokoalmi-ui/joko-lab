# EXP-20261009-008 — F3: veredicto

**Fecha:** 2026-10-09 (viernes), 18:36 CEST. **Datos:** `f1-resultados.md` (11 celdas, `/tmp/exp008/cells.jsonl`).

## Resultado contra la hipótesis

**H-EXP-008 — CONFIRMADA (signo).** Añadir `--moe-cache-mib C > 0` a un reparto MoE fijo (`-ngl 99 -ncmoe 28`) sube los tok/s de generación **con la misma máquina, el mismo fichero y la misma configuración**: E1 5,55 → **8,54 tok/s** (×1,54) y E2 7,54 → **11,88 tok/s** (×1,58), con réplicas intercaladas cuyos rangos **no se solapan** y una banda de ruido medida de 9-11 %.

## Predicciones falsables, una a una

| Pred. | Enunciado | Resultado | Evidencia |
|---|---|---|---|
| **P1** | tok/s(C>0) > tok/s(C=0) en E1, todas las rondas | **CONFIRMADA** | 3/3 réplicas de C=0 caen bajo las 3 de C=1024, sin solape |
| **P2** | En PROSA la ganancia es menor, nula o negativa | **FALSADA** | E2 gana **+58 %**, igual o más que E1 (+54 %) |
| **P3** | Monotonía por tamaño hasta saturar | **PARCIAL** | 0 < 256 (×1,35) < 512-1024 (≈8,5-9,0); a partir de 512-1024 **satura**; 2048 ni arranca |
| **P4** | La caché roba VRAM al reparto de capas; existe un C máximo | **CONFIRMADA (literal)** | Pico ≈ baseline + C MiB; C=2048 → `failed to allocate CUDA0 buffer of size 2147450880` → `failed to initialize the context: failed to allocate the MoE cache buffers` |
| **P5** | Texto idéntico a temp 0 | **PARCIAL** | E1: mismo `text_md5` (`36c5a8f0…`) en las 4 celdas. **E2: el texto CAMBIA** entre C=0 (`c8640783…`, 595 chars) y C=1024 (`36f1ac76…`, 597 chars) → la ruta con caché puede variar un token; el determinismo entre configuraciones no está garantizado |

**Hallazgo no previsto (el valor real del experimento):** la ganancia **no depende de la clase de entrada**. El diseño esperaba que la prosa (routing de cola larga) no aprovechara la caché; los datos dicen lo contrario. Es un dato que corrige el modelo mental «la caché solo paga con routing repetitivo».

## Lectura operativa (contra las anclas del diseño)

| Ancla | Cifra | Fuente |
|---|---|---|
| CPU puro | 0,37 tok/s | OBS-111 (fichero borrado → referencia cualitativa) |
| Híbrido con expertos en CPU, **sin** caché | 5,55 tok/s (medido hoy) · 1,44 (OBS-111, no comparable) | esta sesión |
| **Híbrido con caché (C=1024)** | **8,54 tok/s E1 · 11,88 tok/s E2** | esta sesión |
| Modelo que cabe entero | ~40 tok/s | OBS-110 |
| Referencia de trabajo del lab (R1-14B) | ~11 tok/s | contexto del lab |

**La frase obligatoria del diseño se resuelve en la rama buena:** el mejor C **no** deja el MoE en 1-2 tok/s; lo pone en **8,5-11,9 tok/s**, en el orden de la referencia de trabajo del lab. La caché MoE convierte el offload de «cifra de laboratorio» en **opción usable**, y aun así no alcanza a un modelo que cabe entero (~40 tok/s).

**Recomendación de configuración:** **C=512 MiB** (o 256) por coste/beneficio — con 256 ya se captura el ×1,35 y con 512 se llega al techo práctico (~9 tok/s) gastando la mitad de VRAM que C=1024. C=1024 (+1 GB de VRAM) compra +0,0-0,5 tok/s sobre 512: solo si esa VRAM no hace falta para otra cosa (p. ej. GLM 4.6V).

## Límites (declarados, no ocultos)

1. **Swap al 100 % (8.191/8.191 MiB) durante toda la medición** → las cifras absolutas incluyen el coste de paginación y no son extrapolables a una máquina quieta. La comparación es intra-sesión e intercalada.
2. **ComfyUI (`:8188`, 190 MiB) corriendo** durante el barrido (co-variable declarada).
3. **n pequeño:** 3 réplicas en C=0 y C=1024; **1 sola** en C=256 y C=512 (la de ronda 1 de C=512 quedó contaminada y se descartó).
4. **Desviación de F1:** reparto `-ncmoe 28` con `-c 2048 -ub 128` (el diseño preveía 24 / 4096 / 512; con esos valores el arranque muere en los compute buffers).
5. **No se aísla el efecto build:** OBS-111 midió en 2.38.0, y no hay 2.38.0 con CUDA en disco; la comparación con OBS-111 es solo de dirección.
6. **No se mide:** calidad de respuesta (solo igualdad de texto a temp 0), contextos grandes, KV cuantizada, MTP / `--spec-draft-n-cpu-moe`.

## Consecuencia práctica (bloqueo del lanzador)

`lms load` **no** expone flags de llama.cpp, así que LM Studio no puede pedir la caché. Para usarla hay que lanzar el servidor a mano (comando verificado y reproducible):

```
LD_LIBRARY_PATH=/home/jokoalmi/.lmstudio/extensions/backends/vendor/linux-llama-cuda12-vendor-v1 \
/home/jokoalmi/.lmstudio/extensions/backends/llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.55.0/llama-server \
  -m "/mnt/ssd_ia_datos/LM STUDIO/noctrex/Qwen3.6-35B-A3B-MXFP4_MOE-GGUF/Qwen3.6-35B-A3B-MXFP4_MOE.gguf" \
  --host 127.0.0.1 --port 8099 -c 2048 -ngl 99 -ncmoe 28 --moe-cache-mib 512 -t 6
```

Siguiente paso natural (no ejecutado aquí): envolverlo en un script del lab que compruebe VRAM libre antes de arrancar y que no toque `:1234`/n8n/Ollama.
