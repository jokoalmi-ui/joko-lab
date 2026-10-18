---
title: "EXP-20261009-008 — ¿--moe-cache-mib acelera el MoE con expertos en CPU? (RTX A2000 12 GB)"
type: EXP
---

# EXP-20261009-008 — Caché GPU de expertos MoE (`--moe-cache-mib`)

**Estado:** DISEÑO — redactado 2026-10-09 17:52 CEST. **NO EJECUTADO.** Requiere liberar VRAM y RAM (F0) y OK explícito; el barrido ocupa la GPU ≈40-50 min en ventana aislada.
**Tipo:** octavo experimento secuencial del lab; eje «rendimiento de inferencia local». Cierra el pendiente que dejó OBS-111 y la referencia `offload-moe-vram-insuficiente` de la skill de medición.
**Método:** medición comparada con **baseline contemporáneo intercalado** y **una sola variable**. Ventana aislada en `:8099`. NO se toca LM Studio (`:1234`), Ollama (`:11434`), ComfyUI (`:8188`), ni n8n. Solo lectura sobre los instrumentos; se escribe únicamente el registro del propio experimento (`/tmp/exp008/` + esta ficha).
**Origen:** A4 `research/analisis-nichonauta-llamacpp-optimizacion-20261009.md` §7 (verificación en solo lectura: `--moe-cache-mib` existe SOLO en el runtime 2.55.0 que LM Studio ya trae; el bloqueo es el lanzador `lms`) + commit `4b1e425`. Antecedente medido: `OBS-111-offload-moe-frontera-12gb-2026-09-16.md`.

## Pregunta e hipótesis

**Pregunta:** ¿existe un cambio de **una sola variable** (añadir `--moe-cache-mib C` a un reparto MoE ya fijado) que suba los tok/s de generación sin cambiar hardware?

**Semántica verificada del flag** (cadenas literales extraídas hoy del binario 2.55.0, `libllama-common.so.0.6.0`):

> "GPU cache size in MiB for the MoE experts kept in the CPU. with multiple GPUs, it is split among them like the layers (--tensor-split) (default: 0, disabled)"

> "keep all Mixture of Experts (MoE) weights in the CPU" · "keep the Mixture of Experts (MoE) weights of the first N layers in the CPU"

Es decir: los expertos que viven en RAM por `--n-cpu-moe N` ganan una **caché en VRAM**; con acierto, el experto ya está en la GPU y no se vuelve a copiar por PCIe.

**H-EXP-008:** con `--n-cpu-moe N` fijo, añadir `--moe-cache-mib C > 0` **sube** los tok/s de generación porque los expertos «calientes» dejan de re-transferirse por PCIe. Predicciones falsables (solo signo; la magnitud la fija el ruido medido, RULE-015):

- **P1** — entrada **ESTRUCTURADA** (routing repetitivo): tok/s(C>0) > tok/s(C=0) en todas las rondas.
- **P2** — entrada **PROSA** (routing de cola larga): la ganancia es menor que en E1, y puede ser nula o negativa (cada fallo de caché cuesta una copia host→GPU).
- **P3** — monotonía por tamaño: tok/s(C₂) ≥ tok/s(C₁) si C₂ > C₁, al menos hasta que el acierto sature.
- **P4** — VRAM pico(C=N) ≈ VRAM pico(C=0) + N (± fragmentación) → existe un C máximo que arranca, y la caché **roba VRAM al reparto de capas** (coste de oportunidad: esa VRAM podría sostener más expertos en GPU).
- **P5** — a temperatura 0 y semilla fija el texto debe ser **idéntico** al de C=0 (una caché no debe cambiar la salida). Si cambia, es hallazgo (bug/fallback), no mejora.

**Qué la falsearía:** en E1, tok/s(C>0) ≤ tok/s(C=0) fuera del ruido. Entonces el mecanismo no compensa en esta máquina y el flag sale del catálogo de futuribles.

## Reconocimiento previo (solo lectura, 2026-10-09)

### R1 — El flag y su único runtime

23 runtimes llama.cpp en `~/.lmstudio/extensions/backends/` (2.16.0 → 2.55.0). Solo `llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.55.0` (`libllama-common.so.0.6.0`) contiene `--moe-cache-mib`; `-n-cpu-moe` está en todos. `lms load` **no** expone flags de llama.cpp (solo `--gpu`, `-c/--context-length`, `--parallel`, `--ttl`, `--speculative-draft-*`, `--identifier`, `--estimate-only`, `-y`) → hay que lanzar `llama-server` **a mano**. No hay nada que compilar: el runtime ya está en disco.

### R2 — El modelo del antecedente ya no está en disco (hay que re-basar)

OBS-111 midió con `unsloth/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (22.663.387.424 B = 21,1 GiB), **borrado el 02-10-2026** (`04-operations/reports/2026-10-01-lista-borrado-modelos.md`). Hoy el único MoE grande en disco es:

`/mnt/ssd_ia_datos/LM STUDIO/noctrex/Qwen3.6-35B-A3B-MXFP4_MOE-GGUF/Qwen3.6-35B-A3B-MXFP4_MOE.gguf` = **20.267.153.760 B (18,9 GiB)**, arch `qwen35moe`, + `mmproj-F16.gguf` (899.283.296 B).

Consecuencia: **la cifra 1,44 tok/s no es reproducible** (otro fichero, otro build) y NO sirve como test de entrada; la línea base se re-mide en F1.

### R3 — Instrumento y su test de entrada

Fuente de las cifras: `timings.predicted_per_second` y `prompt eval` del propio `llama-server` (log JSON), `nvidia-smi` para VRAM pico, `free`/`swapon` para paging, `date` para las ventanas. Test de entrada (F1): (a) la ayuda del binario, con `LD_LIBRARY_PATH` al vendor CUDA, se imprime y contiene `--moe-cache-mib`; (b) **control de dirección conocida**: `-ngl 0` (CPU puro) debe rendir mucho menos que el reparto híbrido (OBS-111: ×3,9). Si (b) no se cumple, el medidor no discrimina y se para antes de gastar más cargas.

### R4 — Estado de la máquina hoy (bloqueante, medido 17:5x)

- **VRAM** 12.282 MiB: usados **9.892**, libres **2.006**. Atribución real: llama-server de LM Studio (GLM 4.6V, runtime 2.55.0) 7.982 · node 612 · ComfyUI 190 · Telegram 107 · Chrome 94 · nautilus 46 · papers 45 (≈9.076) + escritorio ≈816.
- **RAM** 30.915 MiB: libres 3.754. **Swap 7.470 de 8.191 MiB usados** → la máquina está paginando.
- Con la máquina paginando, cualquier tok/s absoluto es basura; y sin liberar GLM (+7.982 MiB) no hay sitio ni para el arranque del baseline.

## Diseño

### F0 — Precondiciones (solo liberar; requiere OK explícito)

1. **Descargar el VLM** GLM 4.6V por su CLI oficial (`lms unload`) → +7.982 MiB de VRAM. **Apuntar la ficha exacta de recarga** para restaurarla en la misma sesión: `glm-4.6v-flash`, context **21504**, parallel **4**; y `text-embedding-bge-m3` (437,78 MB, context 8192, TTL 1 h → quedaban 58 min).
2. **ComfyUI (`:8188`)**: corriendo (190 MiB VRAM + worker). Detenerlo o aceptar dejarlo, registrándolo como co-variable.
3. **RAM/swap**: decidir qué se suelta (chrome 684 MB, thunderbird 789 MB, node 1.387 MB, LM Studio…). Criterio de entrada: **no medir con swap en uso** (objetivo `SwapFree` ≈ total). Si no se logra, se registra y las cifras absolutas se degradan a comparación intra-sesión, declarándolo.
4. Comprobar `:8099` libre (hoy lo está) y anotar el estado final a restaurar.

No se toca: n8n, Ollama, el puerto `:1234` de LM Studio (salvo descargar los dos modelos *por su CLI*, que es la operación que la skill autoriza).

### F1 — Instrumento y línea base re-basada (2-3 cargas)

1. `--help` del binario 2.55.0 con `LD_LIBRARY_PATH=<vendor linux-llama-cuda12-vendor-v1>` → debe listar `--moe-cache-mib`. Si falla, parar (falta entorno, no se mide).
2. Localizar el reparto que arranca con el fichero NUEVO: `-ngl 99 -ncmoe N`, arrancando en **N=24** (el que valía para el fichero grande, hoy inexistente). Si no arranca, subir N (OBS-111: pedir menos capas en GPU hace SUBIR la VRAM pedida).
3. Control de dirección conocida: misma config con `-ngl 0` (CPU puro) → debe ser mucho más lento. Prueba de que el medidor ve lo que dice ver.
4. Registrar VRAM pico real del baseline → **techo del barrido** de caché (regla: no bajar de ~300 MiB de margen).

### F2 — Barrido de la variable única (cargas sucesivas, baseline intercalado)

Reparto **FIJO** `-ngl 99 -ncmoe N` (el de F1). Cambia SOLO `--moe-cache-mib C`:

`C = 0` (baseline) · `256` · `512` · `1024` · `2048` — subiendo hasta el primer OOM o hasta agotar el margen medido.

- **Ronda 1:** 0 → 256 → 512 → 1024 → (2048 si cabe).
- **Ronda 2 (intercalado, anti-deriva):** 0 → C_mejor → C_2º. Segunda medida del baseline y de los dos candidatos: es lo que da la banda de ruido.
- Dos clases de entrada, prompts **fijos en fichero**, `n_predict=128`, `temp=0`, semilla fija, `--no-cache-prompt`:
  - **E1 ESTRUCTURADA** — lista/plantilla/JSON de dominio del lab (routing repetitivo).
  - **E2 PROSA** — texto libre sobre el mismo tema (routing de cola larga).
- Una **carga completa por celda** (~84 s con page-cache frío, medido en OBS-111): 9-10 celdas ≈ **35-45 min** de máquina ocupada.
- Muestreo por celda: `nvidia-smi` cada 2 s (VRAM pico durante carga y generación), `free`/`swapon` al inicio y al fin (si hay paging → la celda se invalida y se dice).

### F3 — Veredicto

Tabla por celda y clase: C · VRAM pico · tiempo de carga · prompt tok/s · generación tok/s · RSS · texto idéntico sí/no (P5). Signo del efecto en E1 y en E2 comparado contra el **ruido medido** en la ronda 2; **ningún umbral a priori** (RULE-015). Decisión operativa contra las anclas YA medidas en el lab, no contra impresiones:

| Ancla | Cifra | Fuente |
|---|---|---|
| CPU puro | 0,37 tok/s | OBS-111 (fichero borrado → referencia) |
| Híbrido con expertos en CPU | 1,44 tok/s | OBS-111 (fichero borrado → referencia) |
| Modelo que cabe entero | ~40 tok/s | OBS-110 |

Frase obligatoria del veredicto: si el mejor C sigue a ~1-2 tok/s, el flag mejora una cifra pero **no convierte el offload en opción de trabajo**; si llega al orden de los ~11 tok/s que el lab ya obtiene con R1-14B, cambia la regla operativa y merece ficha de recarga.

## Criterios de éxito (no binarios)

- **Éxito:** P1 y P3 se cumplen y el mejor C cabe bajo el techo de VRAM → el flag es un futurible real y se documenta la configuración.
- **Neutro:** efecto dentro del ruido en las dos clases → no aporta en esta máquina; se anota y sale del catálogo.
- **Negativo:** E1 no mejora o empeora → hipótesis falseada; se documenta que la caché no compensa su coste de VRAM.
- En cualquier caso se registra: ruta y tamaño del GGUF, runtime (2.55.0), reparto N, valores C, VRAM pico, tok/s y la condición de swap.

## Riesgos y límites

- **Co-variable de build:** OBS-111 midió en 2.38.0 («llama.cpp propio»); aquí se usa 2.55.0, el único con el flag. **El 2.38.0 con CUDA no está entre los backends** (solo hay `llama.cpp-linux-x86_64-avx2-2.38.0`, sin CUDA) → no se puede aislar el efecto build; la comparación con OBS-111 es cualitativa (misma dirección), nunca de cifras.
- **Co-variable de quant:** el fichero de OBS-111 (UD-Q4_K_M) ya no existe; éste es MXFP4 (18,9 GiB). No se extrapolan cifras absolutas.
- **Paginación:** si el swap no se libera, las cifras absolutas no valen; se declara en el veredicto.
- **n=2 rondas:** es un baseline, no una conclusión. Diferencias dentro del ruido → «inconcluso» es el resultado honesto.
- **No se mide:** calidad de respuesta (solo P5, igualdad de texto a temp 0), contextos grandes, KV cuantizada, ni el combinado MTP / `--spec-draft-n-cpu-moe`.
- **Riesgo de tocar servicios:** mitigado con ventana aislada, `kill` por **PID literal**, verificación final (`ss -ltnp`, `lms ps`, `nvidia-smi`) y restauración verificada de la ficha de GLM en la misma sesión. Sin `sudo`, sin `rm`, sin Docker.

## Pendiente / dependencias

1. **OK explícito** para F0: descargar GLM + bge-m3, decidir ComfyUI y qué suelta RAM/swap.
2. Fijar los **dos prompts** (E1 estructura / E2 prosa).
3. Fijar el presupuesto de tiempo (≈40-50 min de GPU en ventana aislada, con Hermes sin competir por la máquina).
4. Decidir si se añade la celda opcional de build (hoy **no factible**: no hay 2.38.0 con CUDA en disco).

## Trazabilidad

- Origen: `research/analisis-nichonauta-llamacpp-optimizacion-20261009.md` §7 + commit `4b1e425`.
- Antecedente medido: `01-knowledge/observations/OBS-111-offload-moe-frontera-12gb-2026-09-16.md`.
- Procedimiento: skill `medicion-aceleracion-inferencia-local` (+ `references/offload-moe-vram-insuficiente.md`); criterios de validez del medidor: skill `validacion-instrumentos-medicion`.
- Semántica del flag: cadenas literales del binario 2.55.0 (extraídas 2026-10-09).
- Datos crudos a producir: `/tmp/exp008/` (jsonl por celda + log del servidor por celda).
