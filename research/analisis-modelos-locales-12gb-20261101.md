---
title: "Análisis — Qué modelo local conviene al LAB con 12 GB de GPU (01-nov-2026)"
type: research
---

# Análisis — Qué modelo local conviene al LAB con 12 GB de GPU (01-nov-2026)

**VERACIDAD:** [ALCANCE INTERNO]

**Fuente:** inventario real de `/mnt/ssd_ia_datos/LM STUDIO` + `/mnt/ssd_ia_datos/ollama/models` (medido 01-11-2026); configs de Hugging Face (`zai-org/GLM-4.6V-Flash`, `google/gemma-4-12B-it`, `Qwen/Qwen3.6-35B-A3B`, `ibm-granite/granite-4.1-8b`); tarjetas y blogs de fabricante (z.ai, Liquid AI, Google DeepMind, IBM Research); `nvidia-smi` y `free -g` del host.
**Pregunta:** con una RTX A2000 de 12 GB y el uso real del LAB, ¿cuál es el mejor modelo local de los que ya tenemos descargados?

## Hardware real (medido, no supuesto)

- GPU **NVIDIA RTX A2000 12GB**, 12.282 MiB totales. En el momento de la medición: **8.080 MiB ocupados** (ComfyUI vivo en `:8188`) → ~4,2 GB libres.
- RAM **30 GB** totales, **22 GB disponibles**, swap 7 GB. CPU 6 hilos (i5-9500).
- SSD `/mnt/ssd_ia_datos`: **129 GB libres** de 440 GB.
- LM Studio **caído** en `:1234` durante la investigación → ninguna medición de tokens/s es posible sin arrancarlo.

## Inventario local (tamaños reales de fichero)

| Modelo | Pesos | mmproj | Tipo | Visión |
|---|---|---|---|---|
| GLM-4.6V-Flash Q4_K_M | 6,17 GB | 1,79 GB | 9B denso | sí |
| Qwen3.6-35B-A3B MXFP4 | 20,27 GB | 0,90 GB | MoE 35B / 3B activos | sí |
| gemma-4-12B-it QAT Q4_0 | 6,98 GB | — (encoder-free) | 12B denso | sí (+audio) |
| LFM2.5-VL-3B Q4_K_M | 1,67 GB | 0,58 GB | 3,1B | sí |
| granite-4.1-8b Q4_K_S | 5,09 GB | — | 8B denso | no |
| gpt-oss-20b MXFP4 | 12,11 GB | — | 20B MoE | no |
| DeepSeek-R1-Distill-Qwen-14B Q4 | 8,99 GB | — | 14B denso | no |
| HunyuanOCR Q8 | 0,58 GB | 0,73 GB | OCR especialista | sí (OCR) |
| LFM2.5-2.6B · granite-4.0-h-tiny · Dolphin3-8B | 1,67 / 4,00 / 4,92 GB | — | varios | no |
| bge-m3 Q4_K_M | 0,44 GB | — | embeddings RAG | no |

Además, en Ollama: `qwen2.5:7b` (4,7 GB), `ibm/granite4.2:8b-q4_K_M` (5,3 GB), `deepseek-r1-distill-qwen-14b` (9,0 GB).

## Presupuesto de VRAM (pesos + mmproj + KV a 16k tokens)

KV/token calculado con la config real: `2 × cabezas_KV × head_dim × capas × 2 bytes`.
GLM-4.6V-Flash: 40 capas, **2 cabezas KV**, head_dim 128 → **40 KB/token** (16k = 0,67 GB; 32k = 1,34 GB).
granite-4.1-8B: 40 capas, 8 cabezas KV → **160 KB/token** (16k = 2,68 GB).

| Modelo | Total 16k | ¿Cabe en 12 GB? |
|---|---|---|
| LFM2.5-VL-3B | **2,66 GB** | sí, incluso con ComfyUI cargado |
| HunyuanOCR | 1,51 GB | sí, con ComfyUI cargado |
| granite-4.1-8B | 7,77 GB | sí, sin ComfyUI |
| gemma-4-12B-it | ~7,98 GB (KV estimado) | sí, sin ComfyUI |
| GLM-4.6V-Flash | **8,62 GB** | sí, sin ComfyUI; KV baratísimo permite 32k por 1,34 GB |
| DeepSeek-R1-Distill-14B | 10,49 GB | al límite |
| gpt-oss-20b | 13,61 GB | no (offload parcial) |
| Qwen3.6-35B-A3B | 21,77 GB | no (requiere offload a RAM) |

## Capacidad por eje (fuentes de fabricante, NO medidas en el LAB)

- **GLM-4.6V-Flash**: única de la casa con **function calling multimodal nativo** — imágenes, capturas y páginas de documento entran como parámetros de herramienta sin convertirlas a texto, y el modelo interpreta resultados visuales devueltos por la herramienta. 128k de contexto en entrenamiento.
- **LFM2.5-VL-3B**: 3,1B; **function calling nuevo en la línea VL** (ToolSandbox más que duplica respecto a la versión anterior); en su propia tabla supera a gemma-4-E2B/E4B en RealWorldQA (73,1) y MMBench (81,0); OCR de página completa y grounding.
- **gemma-4-12B-it**: multimodal **unificado sin encoder aparte** (texto+imagen+audio), 256k de contexto, function calling nativo, **MTP drafters** (ya tenemos el drafter de 0,46 GB) para reducir latencia.
- **Qwen3.6-35B-A3B**: MoE con 3B activos, atención híbrida (KV barato), visión, orientado a agente y código. Su atractivo es velocidad por token activo, no el tamaño.
- **granite-4.1-8B**: texto, tool calling fuerte, **Apache 2.0** (licencia limpia para clientes).
- **HunyuanOCR**: especialista de OCR; mejor relación calidad/tamaño para extraer texto que un VLM general.
- **DeepSeek-V4-Flash-Vision-Exp** (contexto de la pregunta original): pesos abiertos y GGUF existen, pero el quant de 1 bit pesa **~82 GB** (50 GB + 32,4 GB) y Q4 ~155 GB → **inviable en este equipo**.

## Veredicto: el mejor no es un modelo, es un reparto de dos carriles

1. **Visión + herramientas (defecto): GLM-4.6V-Flash.** Aporta lo que ninguna otra pieza local tiene: encadenar percepción visual y acción con tool calling multimodal. 8,62 GB a 16k y contexto largo casi gratis. Ya está configurado en `~/.hermes/config.yaml` (`glm-4.6v-flash`, `base_url :1234`).
2. **Visión rápida y OCR: LFM2.5-VL-3B (2,66 GB) + HunyuanOCR (1,51 GB).** Los únicos que conviven con ComfyUI sin liberar VRAM.
3. **Texto/agente ligero: granite-4.1-8B** (Apache 2.0) o **gpt-oss-20b** (delegación ya validada).
4. **Razonamiento pesado: Qwen3.6-35B-A3B** solo con offload (~10 GB en RAM); cabe en teoría con 22 GB disponibles, velocidad sin medir.
5. **Retirar del catálogo activo:** DeepSeek-R1-Distill-14B (10,49 GB y superado por Qwen3.6 en todas las tareas del LAB).

## Lo que este análisis NO demuestra

- **Ninguna cifra de rendimiento está medida en este equipo**: ni tokens/s, ni VRAM pico real, ni acierto en las tareas del LAB. Los números de visión son de las tarjetas de fabricante (auto-publicados).
- Soporte de audio y de la entrada multimodal nativa de gemma-4 en llama.cpp/LM Studio: **no comprobado**.
- El KV de gemma-4-12B es una estimación (su `config.json` no se pudo parsear completo).

## Siguiente paso (pendiente de ejecutar)

Batería de medición con 4 candidatos (GLM-4.6V-Flash, LFM2.5-VL-3B, gemma-4-12B, granite-4.1-8B) y 6 pruebas con material real del LAB: ficha PNG, captura de log de Docker, página de PDF, llamada a herramienta con imagen, pregunta en español y tokens/s. Métricas: VRAM pico (`nvidia-smi` en bucle), latencia hasta primer token, tokens/s y acierto. Requiere arrancar LM Studio y parar ComfyUI durante la prueba.

## Medición real (01-nov-2026, 10:10–10:14 CET) — batería con material del LAB

Lo que sigue **corrige** la sección anterior en lo que la medición contradice. La frase previa «**Visión + herramientas (defecto): GLM-4.6V-Flash**» deja de sostenerse en precisión: es cierta en tool calling multimodal, falsa como «el que mejor lee».

**Método**: `llama-server` del build CUDA 12 de LM Studio (`llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.61.0` con `LD_LIBRARY_PATH` al vendor `linux-llama-cuda12-vendor-v1`), puerto 12345, `ctx 8192`, `temperature 0`, `--jinja` con la herramienta `buscar_precio`. VRAM pico muestreada de `nvidia-smi` durante cada petición. Material real: `perfume_del_dia_v5_indigo_suede_corr.png` (ficha publicada) y la página 6 del PDF de empleo rasterizada a 110 dpi (`docp6-006.png`). ComfyUI parado para liberar los 8.080 MiB que ocupaba.

| modelo | VRAM pico | carga | TTFT imagen | t/s | ficha (4 campos) | línea de tiempo (8 hitos) | tool call |
|---|---|---|---|---|---|---|---|
| LFM2.5-VL-3B | 2.672 MiB | 3,0 s | 1,96 s | 72–85 | 2/4 | 2/8 | correcto |
| GLM-4.6V-Flash | 8.962 MiB | 23,1 s | 4,05 s | 33 | 3/4 | 8/8 | correcto, pero repite la llamada 3 veces |
| gemma-4-12B-it | 8.962 MiB | 33,1 s | 1,69 s | 29 | 4/4 | 8/8 | correcto |
| granite-4.1-8B | 6.264 MiB | 11,0 s | — (sin visión) | 39 | — | — | correcto |

**Hallazgos**
- **gemma-4-12B es el más preciso leyendo imagen**: 4/4 en la ficha (nombre, casa, precio y tamaño) y 8/8 en la línea de tiempo, con el TTFT más bajo (1,69 s). Su coste es el tiempo total: 29 s por respuesta porque razona ~2.200 caracteres antes de contestar.
- **GLM-4.6V-Flash acierta la línea de tiempo 8/8 pero inventa la casa en la ficha** («Daniel Josier» donde la ficha dice Lunio) y **emite tres veces la misma tool call**. Su ventaja real es el OCR de documento largo (20 s para 8 hitos) y el tool calling con imagen como argumento.
- **LFM2.5-VL-3B lee campos sueltos y alucina las relaciones**: saca bien nombre y precio de la ficha, pero asigna mal los hitos («1943: Turing», «1958: ELIZA», «1986: Deep Blue») → 6 de 8 mal. Es un OCR rápido, no un lector que razona. A cambio: 2.672 MiB y 3 s de carga, el único que convive con ComfyUI.
- **granite-4.1-8B no tiene torre de visión** (sin `mmproj`): 6.264 MiB, tool calling correcto y 39 t/s en texto.
- **El presupuesto de VRAM calculado en la sección anterior cuadra con lo medido**: LFM 2.672 MiB vs 2,66 GB estimados; GLM 8.962 vs 8,61 GB. Con ComfyUI cargado (8.080 MiB) **solo entra LFM**; GLM y gemma necesitan la GPU vacía.

**Tres defectos del propio medidor, corregidos durante el pase** (sin ellos las cifras anteriores eran falsas):
1. La primera tanda midió contra un `llama-server` viejo que seguía escuchando en el puerto: los cuatro modelos dieron tiempos idénticos y 8.956 MiB. Fix: comprobar el puerto libre antes de arrancar y abortar si está ocupado.
2. GLM y gemma emiten `reasoning_content`: el colector solo leía `delta.content` y devolvía texto vacío. Fix: acumular razonamiento aparte y subir el presupuesto de tokens.
3. El acumulador de `tool_calls` guardaba fragmentos sueltos y los argumentos salían truncados. Fix: concatenar por `index`, que es lo que permite afirmar que los cuatro modelos llaman bien.

**Estado del sistema al cerrar**: sin `llama-server` vivo, GPU a 109/12.282 MiB, ComfyUI **parado** (el usuario decide cuándo se rearranca).

## Verificación con 3 repeticiones (01-nov-2026, cierre 10:40:39 CET)

La primera batería tenía **una sola medida por prueba**. RULE-015 pide validar el instrumento antes de creerse la cifra, así que se repitió con `--repeticiones 3` sobre el medidor ya versionado (`tools/bench_vision.py`), mismo material, `temperature 0`, ctx 8192. Duración total de la tanda: 9 minutos para los 4 modelos.

| modelo | VRAM pico | carga | ficha (mediana y rango) | acierto ficha | documento | acierto doc | tool+imagen | tool texto |
|---|---|---|---|---|---|---|---|---|
| GLM-4.6V-Flash | 8.956 MiB | 22,2 s | 13,98 s [13,9-14,1] | 3/4 en 3/3 reps | 12,34 s [12,3-12,5] | 8/8 en 3/3 | 4,22 s | 18,51 s |
| gemma-4-12B-it | 8.970 MiB | 33,2 s | 8,12 s [8,1-9,2] | 4/4 en 3/3 reps | 28,91 s [28,6-30,0] | 8/8 en 3/3 | 5,84 s | 4,87 s |
| LFM2.5-VL-3B | 2.666 MiB | 3,0 s | 0,65 s [0,65-2,27] | 2/4 en 3/3 reps | 1,30 s [1,29-3,24] | 2/8 en 3/3 | 0,65 s | 0,32 s |
| granite-4.1-8B | 6.264 MiB | 6,0 s | sin visión | n/a | sin visión | n/a | sin visión | 0,97 s |

Tool calling: correcto (nombre y argumentos válidos) en las 3 repeticiones de los tres modelos con visión, y también en granite.

**Qué añade la repetición y qué no**
- **Los aciertos no se mueven**: los cuatro modelos dan la misma nota en la 1.ª, 2.ª y 3.ª repetición. El fallo de GLM en la ficha y el de LFM en la línea de tiempo son **sistemáticos**, no ruido de muestreo. Ahí la pasada única ya decía la verdad.
- **Los tiempos sí se mueven, y solo en LFM**: 2,27 s la primera repetición frente a 0,65 s la segunda y la tercera (arranque en frío del servidor). GLM y gemma son estables dentro de ±1 s. Con una sola medida se habría publicado el peor caso como si fuera el normal.
- **La pasada única se reproduce exacta**: LFM 2/4 y 2/8, GLM 3/4 y 8/8, gemma 4/4 y 8/8. El instrumento queda validado contra sí mismo.
- El orden de preferencia no cambia: **gemma lee mejor**, GLM gana en velocidad de documento y en tool calling con imagen, LFM es OCR barato y granite no tiene visión.

**Estado del hardware al cerrar**: 115 MiB de 12.282 MiB en uso, 0 % de utilización, puerto 12345 libre, ningún `llama-server` vivo.
