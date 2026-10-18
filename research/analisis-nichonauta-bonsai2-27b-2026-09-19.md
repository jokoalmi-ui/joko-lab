---
title: "Análisis — Prism ML Bonsai 2 27B (ternario) probado a fondo por Nichonauta (18-sep-2026)"
type: research
fecha: 2026-09-19
---

# Análisis — Prism ML Bonsai 2 27B (ternario) probado a fondo por Nichonauta (18-sep-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/hNRMVLejcEg — **[Nichonauta] «Probamos Bonsai 2 27B a fondo»**, directo de **3 h 07 min**, publicado **18-sep-2026** (4.462 vistas en la entrega del cron). Transcripción ES auto-generada, 1.393.335 B → limpia+dedup **151.100 chars / 27.665 palabras**. Análisis: **19-sep-2026, 17:39 CEST** (hora medida con `date`, RULE-012).

**Modelo (capa vendor, 17-18 sep 2026 — NO reproducido en el lab):**
- Autor **Prism ML**; base **Qwen3.8-27B** (27,36B: 24,35B backbone + 2,54B embedding/LM head + 0,46B torre de visión). HF: `prism-ml/Ternary-Bonsai-2-27B-gguf`.
- Pesos **ternarios g128 {−1,0,+1}** con escala FP16 por grupo de 128 → **1,72 bits/peso**; **5,9 GB** frente a ~54 GB en FP16 (~9,3×).
- **Retención declarada 98,2 %** (score agregado 83,9 vs 85,4 del FP16 en 20 benchmarks; 84,78 vs 86,32 en los 14 de modo razonamiento). Su predecesor (Bonsai 1, base Qwen3.6-27B) declaraba 95 %. Comparan contra IQ2_XXS convencional (72,59 en 9,4 GB).
- Contexto **262K**; arquitectura híbrida (~75 % linear attention Gated DeltaNet / ~25 % full attention); rotación Hadamard para outliers. Velocidad declarada: **143 tok/s en RTX 5090**, ~47 tok/s en Apple M5 Max. Visión no cuantizada (add-on GGUF de 0,63 GB).
- Incluye variantes **Q1** (más pequeña, más agresiva) y **Q2** (la que conserva «casi toda la inteligencia»).

**Lo medido por Nichonauta (RTX 3060 12 GB, llama.cpp con fork):**
- Usó **PQ2_0**. En la landing page: **55.000 tokens y 22 minutos**, promedio **42 tok/s**. Repitió con **Q1 + KV cache Q8** para que cupiera completo: **26 tok/s**, y su estimación para la misma petición: **«40 y tantos minutos»**.
- Con **112.000 tokens de contexto ≈ 35 tok/s**. El cuello real no son los pesos: es la **KV cache del Qwen 3.8 27B**, que sigue ocupando mucha VRAM (pariente directo del análisis del 24-ago: KV en Q8 = mitad de VRAM).
- **Sin MTP** por defecto (el Qwen 3.8 original sí lo trae) → peor rendimiento en contextos largos y GPU que calienta más.
- **Requiere un fork especial de llama.cpp**; **no es compatible con Ollama** («lo que te recomiendo es no usar Ollama»).
- Prueba práctica: landing page y simulador de fluidos → **Bonsai 2 respondió mejor que el Qwen 3.8 27B original a la primera**; el JavaScript funciona; bug en la primera iteración del simulador (no se muestran los fluidos).

**Veredicto del autor (verbatim, limpio):**
> «Bonsai 2 27B no es igual al modelo original Qwen 3.8 27B, pero se sigue comportando de forma muy similar, tanto para lo bueno como para lo malo» — pesando ~1/10.
> «**No estoy de acuerdo en que mantenga el 98,2 % de calidad** como ellos dicen, pero sí sigue siendo superior a modelos más pequeños, aún en código.»
> «Bonsai está interesante cuando queremos un Qwen 3.8 27B en poco hardware, sin embargo, no solo existe Qwen 3.8 27B.»
> Con esfuerzo de razonamiento bajo «ni siquiera merece la pena»; para respuestas rápidas recomienda **Gemma 4 12B / Gemma 4 4B**.

## 🔴 Mapeo contra el lab (A2000 12 GB)

| Pregunta | Respuesta |
|---|---|
| ¿Cabe en 12 GB? | **Sí** (5,9 GB de pesos; Q1 + KV Q8 entra completo en una 3060 12 GB). |
| ¿Es usable para trabajo del lab? | **NO como modelo interactivo**: 26 tok/s en una 3060 y ~40 min por una tarea de landing. El coste está en **tokens y tiempo**, no en VRAM. |
| ¿Cambia la regla del lab del 24-ago («si solo cabe a 1-2 bits, no conviene»)? | **La matiza**: `analisis-nichonauta-qwen27b-cuantizado.md` demostró que IQ1-S (cuantización *post-hoc* de llama.cpp) genera basura. Bonsai 2 es ternario **entrenado** y Nichonauta lo describe como funcionalmente cercano al original. La regla sigue vigente para cuantización extrema *no entrenada*; el ternario entrenado es una excepción parcial, no una refutación. |
| ¿Sustituye a gpt-oss-20b? | **NO** — el pitfall de velocidad/tiempo lo descarta hoy. |
| Fricción de integración | Requiere **fork de llama.cpp**; el lab usa LM Studio / Ollama → integración no soportada por la vía normal. |
| ¿Y el futurible F6 (24 GB)? | Sin cambio: con 24 GB el camino sigue siendo Qwen 3.8 27B **en Q4** (regla del lab), no ternario. |

## Veredicto: **VALOR MEDIO-ALTO — hallazgo nuevo, sin acción inmediata**

1. **NUEVO (lo que aporta):** matiza una regla vigente del lab. «1-2 bits ⇒ inservible» era cierto para IQ1-S; un ternario **entrenado** (1,72 bits/peso, base Qwen 3.8 27B) conserva el comportamiento del original con 1/10 del peso. Queda registrado como excepción condicionada (coste en tokens/tiempo + fork obligatorio).
2. **NUEVO (dimensión de medida):** el veredicto del canal no se decide por tok/s sino por **tokens por tarea × minutos**. Mismo eje que el pitfall de «effort de pensamiento» del análisis de midudev (20-ago). Refuerza el criterio del lab de medir el pipeline completo y no solo la velocidad.
3. **CONFIRMA:** para 12 GB, gpt-oss-20b sigue siendo el caballo de batalla; el salto real a Qwen 3.8 27B pide ~24 GB (futurible F6, sin fecha).
4. **Riesgo de fuente:** el 98,2 % es **claim del vendor** (no reproducido); el propio autor lo rechaza. RULE-017: cifra con fuente y fecha, nunca sin ellas.

**Sin acción.** No se descarga nada (7,2 GB + fork). No se toca el stack.

*Nota honesta: transcripción auto-generada con deformaciones («Qen 3.827B» = Qwen 3.8 27B; «Bonsai 227B» = Bonsai 2 27B; «PQ2-0»). Directo con 3 h de charla: los datos duros son los fragmentos citados, no el conjunto. Las cifras del vendor provienen de la model card / nota de prensa del 17-sep-2026, no de una prueba del lab. El criterio del usuario aplicado aquí: si no aporta nada, no se le da entrada; sí se registra porque **sí aporta** (matiza una regla).*
