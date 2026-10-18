# EXP-20260916-007 — F2 celda A(T3): servir un MoE de 22,6 GB en 12 GB de VRAM (sesión directa)

- **Fecha**: 2026-09-16, ventana **16:10:44 → 16:12:37 CEST** (1,88 min de reloj).
- **Modo**: A — sesión directa (`deepseek-v4-flash` cloud) con `web_search` + `web_extract` + **verificación por `curl`** y **evidencia local del propio binario**.
- **Tarea T3**: cómo servir un MoE de 22,6 GB (Qwen3.6-35B-A3B Q4_K_M) en una GPU de 12 GB por offload de capas, con fuentes.

## Coste y latencia (medidor, tarifa oficial)

| métrica | valor |
|---|---|
| llamadas | **6** |
| prompt tokens | 440.074 |
| **coste** | **0,012867 USD** |
| franja | 6/6 off-peak |
| ttfb_total | 5,68 s |
| total_ms_total | 46,2 s |
| status ≠ 200 | 0 |

## Calidad (instrumento objetivo: `curl` + cita literal)

- **9 claims reales → 9/9 PASS** (tras corregir el instrumento: ver nota al final).
- **1 control negativo** (cita inventada) → correctamente **no encontrado**.
- CORREGIDO: el claim de `--n-cpu-ffn` **sí verifica** (vía `crudo`). No era un defecto de la cita, sino un **falso negativo del medidor v2**: `norm()` borraba tramos de las fuentes de código al interpretar los `<`/`>` de C++ como etiquetas HTML (ver `f2-instrumento-correccion-v3.md`). **9/9 = 100 %.**

## Evidencia LOCAL de primera mano (no web)

Binario real: `~/.lmstudio/extensions/backends/llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.38.0/llama-server`
→ **`version: 0.4.1-dev (build 1, commit dfe4516)`** (coincide con lo medido en T2).

Su `--help` (necesita `cwd` en su carpeta + `LD_LIBRARY_PATH` con su `vendor/`) confirma **8** flags de offload, entre ellos:

- `-cmoe`, `--cpu-moe` → *keep all Mixture of Experts (MoE) weights in the CPU* (`LLAMA_ARG_CPU_MOE`)
- `-ncmoe`, `--n-cpu-moe N` → *keep the … weights of the first N layers in the CPU* (`LLAMA_ARG_N_CPU_MOE`)
- `-ncffn`, `--n-cpu-ffn N` → FFN densas (no MoE)
- `--override-tensor`, `-ot`
- **`--spec-draft-cpu-moe` / `-cmoed` / `--cpu-moe-draft`** y **`--spec-draft-n-cpu-moe` / `-ncmoed` / `--n-cpu-moe-draft`** → offload MoE **para el modelo draft**

## Hallazgos

1. **El motor que ya tenemos hace el trabajo**: no hay que instalar ni compilar nada para T3 — el backend 2.38.0 (motor `0.4.1-dev`) trae `--n-cpu-moe`.
2. **`--n-cpu-moe` es azúcar sobre `-ot`**: el PR oficial `#15077` (*llama : add --n-cpu-moe option*) lo dice literalmente: funcionan añadiendo *tensor overrides*, y **si usas `--override-tensor` antes, tus overrides tienen prioridad**.
3. **Dirección de conteo no obvia**: la guía de HF advierte de que `--n-cpu-moe` **empieza a contar por las capas de numeración más alta** — de ahí discrepancias al comparar con «las primeras N».
4. **Hallazgo nuevo (no estaba en ningún informe previo del lab)**: existen variantes **para el modelo draft** (`--spec-draft-cpu-moe`, `--spec-draft-n-cpu-moe`). Es decir, en una config **MoE + MTP/especulativo (justo T2)** se puede decidir por separado qué expertos del draft van a CPU. Conecta T2 y T3 y abre una vía de medición que no habíamos considerado.
5. **LM Studio no llega aquí**: desde **0.3.23** solo expone *«Force Model Expert Weights onto CPU/GPU»* (equivale a `--cpu-moe`, **todo o nada**); **no expone `--n-cpu-moe`** (petición abierta en su bug-tracker, issue #840). Para control fino hay que lanzar llama.cpp directo — que es exactamente lo que ya hacemos en el lab.
6. **Aritmética del caso**: 22,66 GB de pesos Q4_K_M en 12 GB de VRAM → hay que ceder **~11-12 GB a RAM**. Con la liberación de hoy (17,2 GiB disponibles) **cabe**, pero la velocidad de generación quedará limitada por el **ancho de banda de RAM**, no por la GPU.
7. **Prompt processing vs generación**: llama.cpp hace *op offload* (copia a GPU los pesos asignados a CPU) para lotes de prompt ≥ **32 tokens**, así que el prompt processing puede ir rápido y la **generación** es la que sufre.
8. **Referencia de la comunidad, NO autoritativa** (marcada como tal): un blog reporta el mismo modelo (Qwen3.6-35B-A3B Q4_K_M) en una RTX 3060 12 GB con `--n-cpu-moe 24`, `-ngl 99`, `-fa on`, `-c 8192` a **~38 tok/s**, ocupando **~9,8 GB VRAM + ~11 GB RAM**. Sirve de **hipótesis de partida para la comprobación empírica**, no como dato validado.

## Nota de fiabilidad de fuentes

Autoritativas: código de `llama.cpp` (`common/arg.cpp`), PR `#15077`, blog oficial de LM Studio 0.3.23, guía de HuggingFace (Doctor-Shotgun).
**No autoritativas** (SEO/comunidad, marcadas): smeltcore, aliteq, insiderllm, runaihome, Reddit. Sus cifras no entran en el veredicto.
