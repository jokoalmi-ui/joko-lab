---
title: "Análisis — Nichonauta: llama.cpp, precompilado vs compilar y optimización para GPUs (fragmento del live de MinAgent)"
type: research
---

# Análisis — Nichonauta: «IA Local con llama.cpp 🚀 Guía de OPTIMIZACIÓN para Modelos y GPUs»
**VERACIDAD:** [VERIFICADO]

**Fuente**: https://www.youtube.com/watch?v=zR7nPlyLQGo — canal **Nichonauta** · 12:26 · publicado **09-10-2026** · 61 vistas / 2 likes / 1 comentario (leídos 09-10-2026, 17:33 CEST con `yt-dlp --print`).

**Veredicto honesto: VALOR MEDIO-BAJO como material técnico nuevo · VALOR ALTO como VALIDACIÓN de decisiones ya tomadas en el lab.**

Primer renglón de relación (Paso 0 del método): **el TEMA ya estaba analizado en el lab aunque este vídeo sea nuevo** → este informe es **VALIDACIÓN, no hallazgo**. Lo que CONFIRMA: el binario precompilado de llama.cpp ya rinde sin compilar, el patrón «modelo grande / GPU pequeña» con expertos MoE a CPU, que Qwen va por delante de Gemma en uso agéntico, y la preferencia por skill/system prompt frente a LoRA. Lo que AÑADE (poco y concreto): **(a)** la comprobación de las tres afirmaciones técnicas del autor **a nivel de código fuente** del repo `ggml-org/llama.cpp` (con fichero y línea), **(b)** un flag que no aparece en ningún análisis previo del lab: `--moe-cache-mib`, **(c)** el detalle de NCCL como ruta específica de CUDA para multi-GPU.

**Relación con análisis previos (no se duplican sus tablas):**
| Análisis previo | Fecha | Qué cubre ya |
|---|---|---|
| `research/analisis-tutorial-llamacpp-rendimiento.md` | 13-ago-2026 | Mismo canal, vídeo `FMuUEe-QWXg`: elección de binario, elección de modelo, QAT, MTP, KV Q8 |
| `research/estudio-moe-12gb-lab.md` | 10-ago-2026 | MoE grandes en 12 GB con expertos a CPU; LM Studio expone `ncmoe` para Qwen pero NO `cmoe/nmoe` para Gemma |
| `research/veredicto-qwen-35b-a3b-lab.md` | 10-ago-2026 | Medición real en el lab: 9,4 GB VRAM, 2,7 tok/s en resumen de 400 tokens → inutilizable |

---

## 1. Qué es el vídeo (no es un tutorial)

Es un **corte de 12:26 de la sesión de preguntas y respuestas** de un live de **1:51:48** — https://www.youtube.com/watch?v=5R1nMCMORgs, «Mejor Harness IA Local⚡ MinAgent» (27-09-2026, 4.859 vistas / 82 likes, verificado con `yt-dlp`). El propio autor lo declara en la primera línea de la descripción. El tema del live es **MinAgent**, su harness propio (`Nichonauta/MinAgent` en GitHub — verificado el 09-10-2026 vía API: *«A lightweight terminal AI coding agent with workspace-aware tools, file editing, image input, and support for OpenAI-compatible APIs»*, 20 estrellas, JavaScript, creado 24-09-2026, último push 01-10-2026).

Índice del propio autor (descripción, literal):

| min | Bloque |
|---|---|
| 00:00 | Introducción y uso de agentes de IA |
| 01:11 | Diferencias entre variantes GGUF y MLX |
| 03:01 | Optimización de llama.cpp para NVIDIA RTX |
| 04:40 | Cuantización y caché KV |
| 05:26 | Rendimiento de modelos en GPUs con poca VRAM |
| 07:15 | Comparativa entre modelos Gemma y Qwen |
| 09:14 | Rendimiento multi-GPU y optimizaciones |
| 10:58 | Recomendaciones para modelos grandes en hardware limitado |

**No hay ni un comando literal ni una cifra medida por el autor.** Todo son respuestas a preguntas del chat (varias llevan cifras *de quien pregunta*, no suyas). Es material de **criterio**, no de implementación.

## 2. Tesis del autor (resumen fiel al audio)

1. **Compilar vs precompilado** (pregunta: RTX 3060 12 GB, Windows, CUDA 13): *«te conviene descargar la versión precompilada oficial. Compilarla tú mismo no debería darte una mejora apreciable de rendimiento en condiciones normales»*. Razón que da: el binario oficial CUDA **no** depende de PTX genérico recompilado por JIT — *«aunque los binarios oficiales se construyen con `GGML_NATIVE` off, la configuración de llama.cpp incluye explícitamente `86-real`»* → *«el binario oficial ya trae SM86 nativo»*. Matiz explícito: compilar **sí** tiene sentido si (a) quieres **opciones CUDA especiales** o (b) tu GPU es **de nicho** (antigua o Intel), donde no hay comunidad ni desarrollo.
2. **KV cache cuantizada**: *«el build estándar compila actualmente determinadas combinaciones como Q4, Q8, F16, BF16, pero no todas las combinaciones posibles»* → compilar ahí no es «por velocidad», es **para añadir funcionalidad que no viene por defecto**.
3. **Poca VRAM**: para 8 GB de VRAM + 32 GB de RAM recomienda **Qwen 3.6 35B A3B pasando expertos a CPU y RAM** y remite a su playlist «modelo grande / GPU pequeña».
4. **Qwen vs Gemma**: *«comúnmente los Qwen son mejores para uso agéntico y de desarrollo»*; a un usuario con Gemma 4 26B A4B le dice que **Qwen 3.6 35B A3B le da varias vueltas** para agente de desarrollo.
5. **Aprendizaje continuo con LoRA** (pregunta del chat): *«a lo mejor un skill te logra lo mismo sin tanta complejidad de implementación ni de ejecución»*; el LoRA *«es un paso más que te pudieras evitar»*.
6. **Multi-GPU** (usuario con 2×7900 XTX + 32 GB de RAM y Qwen 3.6 27B MTP Q8 a 50 tok/s que describe como «un infierno»): dividir en dos GPUs *«va a dar más complejidad, más cuello de botella, menor velocidad»*; *«solo en las GPU Nvidia el multi-GPU funciona más optimizado y mejor que en otras tarjetas, sean AMD o Intel»*.
7. **Consejo transversal** a quien se pierde entre tantas pruebas y benchmarks: *«quédate con el que te funciona y no sigas probando»*.
8. **Demo del modo `ask` de MinAgent** (lo más interesante para el lab): el modelo intentó **borrar todo el directorio** desde la terminal y el harness **preguntó antes**. Comentario del autor: *«el modelo sí está intentando seguir los prompts, pero a veces se los va a saltar»*; otro: *«el directorio está vacío; intenta ver los archivos desde terminal y escribe el comando de eliminación»*. Conclusión suya: el mérito del modo `ask` es *«que nos dé la posibilidad de preguntarnos antes de ejecutarlo»*, y la responsabilidad de aceptar el comando es del usuario.

## 3. Verificación a nivel de código (esto es lo NUEVO del informe)

Contrastado el 09-10-2026 contra `ggml-org/llama.cpp` (rama `master`, ficheros descargados con `curl`):

**3.1 El binario oficial ya trae código nativo para RTX 3000 — CIERTO, y también vale para el A2000 del lab.**
`ggml/src/ggml-cuda/CMakeLists.txt`: el conjunto por defecto cuando la build **no** es nativa es `50-virtual 61-virtual 70-virtual` + **`75-virtual 80-virtual 86-real`** (+ `89-real 90-virtual` con CUDA ≥ 11.8, + `120a-real`/`121a-real` en Blackwell). El propio fichero lo documenta: línea 34 *«XX-virtual == compile CUDA code as PTX, do JIT compilation to binary code on first run»*; línea 35 *«XX-real == compile CUDA code as device code for this specific architecture»*; línea 29 *«86 == RTX 3000, needs CUDA v11.1»*; líneas 38-39: la build no nativa **«build virtual architectures as needed… and to also build real architectures for the most commonly used GPUs»**.
En `.github/workflows/release.yml` las builds de release van con **`-DGGML_NATIVE=OFF`** (10 ocurrencias) y el job `ubuntu-cuda` lleva el comentario literal **«# no CMAKE_CUDA_ARCHITECTURES: use the broad default arch set from»** + `-DGGML_CUDA=ON` → **el binario CUDA distribuido sale del conjunto por defecto, que sí incluye `86-real`.**
**Aplicabilidad directa**: `nvidia-smi --query-gpu=name,compute_cap` en el lab → **`NVIDIA RTX A2000 12GB, 8.6, 12282 MiB, 595.99.02`** → **la GPU del lab es 8.6 = el mismo `86-real` del binario oficial.** No hay nada que compilar para ganar velocidad en esta máquina.

**3.2 KV cache: las combinaciones que compila el build estándar son exactamente las que dice — Q4, Q8, F16, BF16.**
`docs/build.md` (tabla de opciones de build, línea 334): `GGML_CUDA_FA_QUANTS` → por defecto **`q4_0-q4_0;q8_0-q8_0;f16-f16;bf16-bf16`**; `all` compila **todas** las combinaciones «but compilation takes much longer»; el resto es una lista separada por `;` de pares `type_K-type_V`; **f16-f16 siempre se compila**; las combinaciones **no compiladas caen al kernel `f16-f16` con un aviso**; tipos legales: `f16, bf16, q4_0, q4_1, q5_0, q5_1, q8_0`. (`GGML_CUDA_FA_ALL_QUANTS` sigue existiendo como alias deprecado de `GGML_CUDA_FA_QUANTS=all`.)
→ El claim del autor es **literalmente** el default del repo. **Dato extra que el vídeo no dice y que sí importa**: una combinación asimétrica (p. ej. **K q8_0 / V q4_0**) **no** está compilada por defecto → no solo «no se acelera»: degrada al kernel f16-f16 con aviso. Es decir, la pregunta del chat sobre recuperar ~118 MB de VRAM con KV asimétrica tiene un coste oculto que el autor despacha como «sobreoptimizar».

**3.3 Los flags reales del patrón «modelo grande / GPU pequeña»** (`common/arg.cpp`, líneas verificadas): `-cmoe/--cpu-moe` (2763), **`-ncmoe/--n-cpu-moe N`** (2770), **`--moe-cache-mib N`** (2780), `-ncffn/--n-cpu-ffn N` (2790, **solo densos**, con la nota *«for MoE expert weights use --n-cpu-moe»*), y en el modelo borrador: `--spec-draft-cpu-moe` (4142) y `--spec-draft-n-cpu-moe` (4149). Ayuda literal de `--moe-cache-mib`: *«GPU cache size in MiB for the MoE experts kept in the CPU. with multiple GPUs, it is split among them like the layers (--tensor-split) (default: 0, disabled)»*. `-ctk/--cache-type-k` existe también (2440), que es el flag que se usaría para esa KV asimétrica.

**3.4 Multi-GPU**: el repo sí lleva una ruta específica de CUDA para multi-GPU — el job `ubuntu-cuda` compila con `-DGGML_CUDA_NCCL=OFF`, es decir, existe un camino **NCCL** que se activa cuando se quiere. La afirmación del autor («NVIDIA mejor optimizado que AMD o Intel») no se ha medido aquí; se registra como opinión, con este dato del repo como contexto.

## 4. Para el lab

| Afirmación del vídeo | Qué tiene el lab | Acción |
|---|---|---|
| «No compiles llama.cpp para una GPU mainstream» | A2000 = compute cap **8.6** → cubierta por el `86-real` del binario oficial (verificado hoy) | **CONFIRMA**: no compilar. Ahorra horas de build y mantenimiento |
| «El build estándar solo trae Q4/Q8/F16/BF16» | El lab usa KV Q8 puntualmente (`analisis-tutorial-llamacpp-rendimiento.md`) | **CONFIRMA** + **MATIZA**: la combinación asimétrica K q8/V q4 **no está compilada** → cae a f16-f16 con aviso |
| «Modelo grande en poca VRAM → expertos a CPU» | Ya medido: Qwen 3.6 35B A3B con expertos a CPU = **9,4 GB VRAM y 2,7 tok/s** (400 tokens, 146,7 s); 8,5-9,0 tok/s en tareas cortas y mayormente en `reasoning`. El cuello es la **CPU** (i5-9500 6C/6T), no la GPU | **CONFIRMA** lo ya documentado. **NO** replicar: el resultado del lab es peor que el «42 tok/s» que circula (ese dato era una RTX 4070 con CPU de 12 núcleos) |
| «Qwen por delante de Gemma para agéntico» | `estudio-moe-12gb-lab.md` ya concluyó Qwen 3.6 35B A3B como ganador; R1-14B sigue siendo la referencia (11 tok/s) | **CONFIRMA** |
| «Un skill antes que un LoRA» | Filosofía del lab (skills + system prompt; sin fine-tuning) | **CONFIRMA** |
| «Quédate con el que te funciona y no sigas probando» | Norma del lab de no sobre-optimizar (RULE-015: sin umbral a priori) | **CONFIRMA** |
| Demo: el modelo intenta borrar el directorio; el harness pregunta | El gate del lab ya bloquea ejecución sin confirmación | **CONFIRMA**: es el mismo patrón, y el autor admite *«a veces se los va a saltar»* → el harness que pregunta es la defensa, no el prompt |

## 5. Clasificación (NUEVO / MEJORA / MATIZA / CONFIRMA)

- **NUEVO para el repo**: la prueba a nivel de código de que el binario CUDA oficial incluye `86-real` (con `GGML_NATIVE=OFF` en release) y que el A2000 es 8.6; el conjunto exacto de combinaciones KV compiladas por defecto; `--moe-cache-mib`.
- **MATIZA**: la KV cuantizada asimétrica tiene un coste oculto (fallback a f16-f16 con aviso) que la regla «KV Q8 cuando hace falta» del lab no contemplaba.
- **CONFIRMA**: todo lo demás (MoE a CPU, Qwen > Gemma, skill > LoRA, no sobre-optimizar, harness que pregunta).

## 6. CLAIMS NO CONTRASTADOS (RULE-017)

Afirmaciones del vídeo (o de usuarios del chat repetidas sin verificar) que **no** se han podido contrastar aquí y **no** deben citarse como hechos:

- «La **NVIDIA Spark** sirve solo para modelos mezcla de expertos; con densos va a ser un infierno» — recomendación a un tercero que quería IA local para documentación médica. Sin fuente y sin verificar el producto.
- «**Muse Glimmer 30B**» (nombre deformado por el ASR): *«ya lo hemos probado… 131.000 tokens de ventana de contexto, denso, sin MTP, requiere mucha memoria»*. Nombre y cifras **sin contrastar**.
- «RTX 5060 8 GB → 25-30 tok/s» (lo dice **un usuario del chat**, no el autor).
- «2×7900 XTX, Qwen 3.6 27B MTP Q8 → 50 tok/s» (**usuario del chat**).
- «GTX 1050 Ti con 4 GB de RAM usando Gemma» (**usuario del chat**; 4 GB de RAM es incompatible con cargar un modelo grande — se registra tal cual se dijo).
- «En RTX 3060 12 GB, Gemma 26B A4B a 43 tok/s»: el dato ya está en `estudio-moe-12gb-lab.md` como referencia **de un artículo de Habr (RTX 4070)**, no de este vídeo.

## 7. Futurible real (uno solo)

**`--moe-cache-mib`** (llama.cpp ≥ actual): reserva N MiB de caché **en GPU** para los expertos MoE que viven en CPU; con varias GPU se reparte como las capas. Es el único camino plausible para subir los **2,7 tok/s** del patrón actual **sin cambiar hardware**: hoy cada token activa expertos desde la CPU. **Condición de aplicabilidad al lab**: requiere **llama.cpp propio** (LM Studio no expone este flag; su GUI solo tiene «Number of layers for MoE onto CPU» = `ncmoe`), así que antes de plantearlo hay que comprobar que el `llama-server` de GLM que ya usa el lab permite fijar el flag. **No se propone experimento hoy**: sin ese paso previo no hay camino de ejecución. Ningún otro futurible: el resto de modelos citados son opiniones del chat.

**Actualización (2026-10-09 17:43:30 CEST, comprobación en SOLO LECTURA autorizada por el usuario)**: la condición «exige llama.cpp propio» es **imprecisa**. Medido en esta máquina:
- El flag **existe en el motor que el lab ya tiene**: de los **23 runtimes** de llama.cpp instalados por LM Studio (2.16.0 → 2.55.0), **solo el más nuevo** — `llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.55.0` (`libllama-common.so.0.6.0`) — contiene la cadena `moe-cache-mib`. En `2.52.0` (mismo `libllama-common.so.0.6.0`) y en los 21 anteriores: **no aparece**. `n-cpu-moe` sí está en todos (desde `libllama-common.so.0.0.1`).
- El **lanzador** no lo expone: `lms load --help` lista `--gpu`, `-c/--context-length`, `--parallel`, `--ttl`, `--speculative-draft-*`, `--identifier`, `--estimate-only`, `-y` — **ningún flag de llama.cpp**.
- El `llama-server` del backend **no arranca suelto tal cual**: falla con `error while loading shared libraries: libcudart.so.12: cannot open shared object file` (exit 127). El runtime **sí está** en el equipo: `~/.lmstudio/extensions/backends/vendor/linux-llama-cuda12-vendor-v1/libcudart.so.12` → lanzarlo a mano con `LD_LIBRARY_PATH` al backend + vendor es **técnicamente posible, NO probado** (eso sería un experimento, no una comprobación de solo lectura).
- **Conclusión corregida**: no hay que compilar ni instalar nada. El bloqueo es del **lanzador**, no del binario. El futurible sigue **sin poder activarse** desde el flujo normal del lab (LM Studio) y **no se propone experimento**.

## 8. Método y límites

- **Método**: `yt-dlp` (auto-subs `es-orig`, VTT) → limpieza y dedup por n-gramas → texto limpio. **VTT 123.646 chars → 13.565 chars limpios (ratio 0,11; dentro del rango ES validado 0,10-0,12)**. Metadatos y descripción con `yt-dlp --print`; verificación técnica contra `docs/build.md`, `.github/workflows/release.yml`, `ggml/src/ggml-cuda/CMakeLists.txt` y `common/arg.cpp` del repo oficial (descargados el 09-10-2026).
- **Límites**: es un **fragmento** de Q&A, no un vídeo cerrado; el ASR deforma nombres propios (`SLnichonuta/minagent` → `Nichonauta/MinAgent`; `cuent/quen` → Qwen; `Gema` → Gemma) y el dedup deja frases repetidas; el texto limpio **termina a mitad de frase** en la última pregunta, así que el cierre exacto del vídeo no se cita. Las cifras de rendimiento que aparecen son **de quien pregunta**, nunca medidas por el autor.
- **Transcripción archivada** en `research/transcripciones/zR7nPlyLQGo-nichonauta-llamacpp-optimizacion.txt` (material técnico reutilizable).
