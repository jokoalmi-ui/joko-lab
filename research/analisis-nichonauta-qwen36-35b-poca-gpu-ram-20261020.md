---
title: "Análisis — Nichonauta: Qwen 3.6 35B A3B con llama.cpp en 12 GB de VRAM (20-oct-2026)"
type: research
---

# Análisis — «Qwen 3.6 35B con llama.cpp: MODELOS GRANDES con poca GPU y RAM»

**VERACIDAD:** [VERIFICADO] contra transcripción íntegra.

**Fuente**: https://youtu.be/nkoId8SX9mM · canal **Nichonauta** · publicado **2026-10-20** · **11:51** · 42 vistas (leído 20-10-2026 con `yt-dlp --print`, exit 0).
**ID**: `nkoId8SX9mM` · **Transcripción**: `/tmp/clean_nkoId8SX9mM.txt` (12.721 B) obtenida con `--write-auto-subs --sub-langs es-orig,es` y limpieza de VTT (timestamps fuera, dedupe de bloques repetidos).

**Naturaleza de la fuente**: es un **directo** (el autor habla de OBS, Chrome y OpenCode abiertos mientras carga el modelo). Los subtítulos son automáticos: el ASR destroza nombres propios («cuen» = Qwen, «Gema» = Gemma, «yubatch» = ubatch). No se usa el audio para nombres de modelos.

## Relación con análisis previos del lab (no se duplican sus tablas)

| Previo | Fecha | Qué cubre ya |
|---|---|---|
| `research/analisis-nichonauta-qwen36-35b-a3b.md` (vídeo `L5CCF3IPcoY`, 6:17) | 06-sep-2026 | Prueba del mismo 35B A3B en una 3060 de 12 GB, MXFP4 + visión, 11 GB de VRAM consumida, descarte del 27B denso |
| `research/estudio-moe-12gb-lab.md` | 10-ago-2026 | Mediciones de caché MoE del lab (0 → 13,23 tok/s; 6.144 MiB → 30,11 tok/s) y el descarte del 35B por swap |

Este vídeo es **el mismo modelo que el del 06-09, en otro vídeo y con otro hardware**: el autor sube a **64 GB de RAM**, se queda con **una sola 3060** (dice que quitó la segunda GPU y los 128 GB) y añade lo que el análisis de septiembre no tenía: la ventana **completa de 262.144**, KV en Q8, cuatro slots simultáneos y la receta de reparto de expertos.

**Veredicto de relación: CONFIRMA** el descarte del lab y **AÑADE** la variable que el lab no había aislado — **el techo es la RAM del sistema, no la VRAM**.

## Receta del autor (citas literales de la transcripción)

- Reparto: «todo lo importante del modelo, las partes iniciales y finales del modelo, así como el contexto, eso sí, 100% en GPU»; los expertos que quepan en GPU y el resto **enteros** en CPU: «no cosas divididas medio raro, que puede hacer peor la velocidad».
- «KV cache en Q8», razonamiento activado, «speculative decoding con MTP».
- Margen de seguridad: «conviene dejar un GB libre de VRAM» → «en vez de que 35 expertos estén en CPU, mejor que estén 36».
- Memoria: «llegamos ni a 32 GB de RAM, sería mejor 64». Con visión (`mmproj`) y Chrome, OpenCode y OBS abiertos.
- MultigPU: «va a funcionar más lento en vez de más rápido» «por el cuello de botella de la comunicación».

## Rendimiento que reporta

- 35B A3B a 4 bits, ventana completa, visión y hasta 4 respuestas en paralelo: «poquito arriba de 40» tok/s (**41**), y **sigue por encima de 40 tras 6.000 tokens** del mismo hilo.
- Gemma 4 12B en la misma máquina: **39** tok/s («nunca llegó a 40»).
- VRAM estabilizada en **10.8** GB de 12.
- Con **8 GB** de VRAM el modelo no cabe con 262K; bajando el contexto a la mitad (~131.000) entra en 8,4 GB.

**Advertencia metodológica:** esos tok/s son de una **RTX 3060 12 GB con 64 GB de RAM**. La A2000 del lab es otra tarjeta. **No se trasladan sin medir.**

## Encaje en el LAB (medido el 20-10-2026 a las 09:49:39 CEST)

El modelo **ya está en disco**; no hay que descargar nada:

- `Qwen3.6-35B-A3B-MXFP4_MOE.gguf` → **18,88 GB** (más `mmproj-F16.gguf`, 0,84 GB), en `/mnt/ssd_ia_datos/LM STUDIO/noctrex/`.
- VRAM: **9885 MiB usados de 12.282** (28 % de utilización) → quedan **2397 MiB**.
- RAM: **15,924 MB disponibles** de 30,916 MB totales.
- Swap: **8 GB con 5,5 GB ya usados** antes de cargar nada.

**La cuenta que decide:** 18,88 GB de pesos. Si ~11 GB van a VRAM, quedan **~8 GB en RAM** solo para los expertos, más el KV cache del contexto. El autor necesita «<32 GB» de RAM con 64 disponibles y el resto del sistema casi vacío; el lab parte de **15,924 MB libres** y **ya está paginando**.

## Veredicto

**La GPU sí puede; la RAM de este host no.** El techo no es la VRAM (los expertos MoE van a CPU/RAM por diseño), es la memoria del sistema: con la configuración del vídeo faltan del orden de **8 a 16 GB**. Con contexto recortado (8K-32K) y un solo slot el consumo baja y **podría** entrar en los 15,924 MB libres, pero el swap ya está al 69 % → el riesgo real es thrashing, no lentitud.

Esto **no contradice** `estudio-moe-12gb-lab.md`: lo reatribuye. El lab descartó el 35B «por swap», y este vídeo explica **por qué** había swap. Lo aprovechable sin comprar nada: KV en Q8, MTP a 2 tokens, expertos enteros a CPU, 1 GB de VRAM de margen y **un solo slot** mientras la RAM esté justa.

Camino que sí abriría el modelo: subir a 64 GB de RAM (2×32 GB). No se ha consultado precio ni compatibilidad con la placa actual.

## Lo que NO se ha verificado

- Tok/s en la A2000. Los 41 son de una 3060 con 64 GB de RAM.
- Que el GGUF MXFP4 del lab **cargue**: no se ha intentado. Hacerlo exige liberar VRAM y RAM, y acepta el riesgo de mandar al swap el resto del sistema.
- El «<32 GB de RAM» del autor es su lectura en vivo durante el directo, no un instrumento del lab.
- La afirmación de que dos GPUs van más lento: es experiencia del autor, no una medición del lab (el lab tiene una sola GPU).
