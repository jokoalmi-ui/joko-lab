---
title: "Análisis — Vídeo de Joaquín Ruiz (@jokioki): «Jev NO es un LLM (por ESTO es casi GRATIS)»"
type: research
fecha: 2026-09-25
---

# Análisis — Vídeo: «Jev NO es un LLM (por ESTO es casi GRATIS)» (Joaquín Ruiz)

**VERACIDAD:** [VERIFICADO]

## Fuente

- **Vídeo:** `https://youtu.be/FIOXJXRfsZQ` → `https://www.youtube.com/watch?v=FIOXJXRfsZQ` · ID `FIOXJXRfsZQ`
- **Canal:** Joaquín Ruiz — IA para Desarrolladores (**@jokioki**, 9.370 subs) · **no está** en `tools/monitor_yt.py` (canales vigilados: Nichonauta, IBM Technology, Rodolfo Carrasco, Fazt Code, hdeleon.net, Nate Herk, Nick Saraev)
- **Publicado:** 25-09-2026 · **880 s** (14:40) · **60 vistas** en la lectura (55 unos minutos antes)
- **Ficha `yt-dlp`:** leída el 25-09-2026 (`/tmp/vid2_meta2.txt`, 3.123 B)
- **Transcripción:** íntegra, 317 líneas / 13.444 B con timestamps (`/tmp/vid2_trans.txt`)

**Cruce previo anti-duplicado (no se repite lo ya escrito):**
- `research/analisis-jev-typesafe-system-one.md` (18-sep-2026) — análisis de Jev desde un **post de LinkedIn** de Valentin Ayesa. Este documento **no lo sustituye ni lo toca**: añade el mecanismo técnico, la lectura de la fuente primaria y el ecosistema del SDK.
- `research/analisis-jokiruiz-ahorro-tokens-20260908.md` (08-sep-2026) — mismo canal, otro vídeo.

## Qué presenta el vídeo

- **Tesis:** el cuello de botella de la automatización no es la inteligencia del modelo, es **la interfaz**: el LLM habla texto, el software habla tipos, enums, booleanos y números.
- **Cómo funciona:** se le manda *estado* (texto libre, un ticket, un correo) + *preguntas declaradas de antemano* con respuestas cerradas. Devuelve respuesta tipada, distribución de probabilidades completa y confianza. Tres primitivas: **Choice** (una opción de una lista), **Score** (posición en una escala), **Noul** (sí/no).
- **Entrenamiento:** RLHF (preferencia humana) y RLVR (recompensas verificables) frente a **RLCD** (Reinforcement Learning for Calibrated Decisions): se premia que la probabilidad declarada sea honesta (decir 90 % y acertar ~9 de cada 10).
- **Por qué es rápido:** prefill (todos los tokens de entrada a la vez) frente a decode (bucle secuencial, un token condicionado al anterior). Si las respuestas posibles ya están declaradas, **no hay bucle de generación**: todo el trabajo es la fase de entrada. El autor **declara explícitamente** que TypeSafe habla de «arquitectura nueva» y «sampler paralelo» pero **no ha publicado los internos**, y que esa explicación es suya.
- **Precio:** **0,042 $/M tokens de entrada** (~42 $ por 1.000 millones) y **salida gratis** («demasiado barato como para molestarse en medirlo»); compara con los LLM, donde la salida cuesta ~5× la entrada.
- **Cuatro casos de uso:** (1) el «if inteligente» para decisiones difusas; (2) control de agentes y **router de modelos**; (3) **verificar y poner guardarraíles** (juzgar política, detectar jailbreak); (4) volumen y tiempo real.
- **Demos:** bot de **Doom** (10 consultas/s) y **Wikiracing**. **Código:** router con un `choice` + un `noul` resueltos en paralelo en una sola llamada, versión del modelo fijada, y la línea clave: **si la confianza baja del umbral, la petición va a una persona**.

## Verificación externa (fuente primaria)

**Confirmado, literal en el artículo de lanzamiento oficial** (`https://typesafe.ai/blog/introducing-system-one-models-and-jev`, leído íntegro: 13.628 chars):

- Primitivas `Choice` / `Score` / `Noul`, RLCD, «unstructured state in, typed probabilistic decisions out», 70–500 ms, 40×–200×, 3–329 s de los modelos frontera, 0,042 $/M de entrada y salida «FREE (too cheap to meter)», ~5× más caro el output en los LLM.
- **La demo del vídeo:** «the only disagreement with GPT-5.6 Terra is on "Churn likelihood level"… The actual answer seems genuinely ambiguous to us» → el vídeo lo cuenta bien (el ASR escribió «antigua» donde dice **ambigua**). Modelo de comparación: **GPT-5.6 Terra** con razonamiento por defecto.
- **Doom: 10 consultas/s ≈ ~7 $/hora** (verbatim en la fuente; el ASR del vídeo se comió la cifra). Cuadra con el precio publicado: 36.000 consultas/hora ÷ 7 $ → **~4.630 tokens de estado por consulta**. El techo de 1 $/hora exigiría ~661 tokens por consulta.
- **Modelo:** `jev-1.13.0` es el build publicado; `jev-latest` es el alias del SDK. El vídeo dice «fijo la versión, no el alias» y el ASR lo escribió «Jef 1130» → coherente.
- **SDK de Python:** existe y es oficial — `pip install typesafe-sdk`, repo `github.com/typesafe-ai/typesafe-sdk-python` (MIT, 226★). El router del vídeo sale de ahí.
- **Nombre:** Jevons (paradoja de Jevons) **y** Kahneman (System 1, *Thinking, Fast and Slow*) — el vídeo solo menciona lo primero.

**Lo que el vídeo no dice (y sí está en la fuente primaria):**

- El blog admite que **el input corto de la demo «nos pinta en una luz favorable»** y que **no puede probar que su precio no esté subvencionado** («we can't prove it isn't subsidized»).
- **Tope de cardinalidad: 255 opciones.** Por encima, usan un **sistema en 2 etapas**: puntuar por separado y luego elegir explícitamente.
- En Wikiracing los speedups son **menores** porque compara contra los modos **sin razonamiento** de los otros modelos (para hacer la demo llevadera).
- El **0 % de alucinación es «no empírico»**: es garantía de esquema, no una medida. («Our number is not empirical. Schema matching is guaranteed».)
- El **193,6× / 444,6×** sale de **4 workflows hechos por su propio equipo de capabilities**, con sesgo admitido, y contra la media de **GPT-6 Astra y Fable 5.1** como referencia.
- Doom: el estado es **texto estructurado, no píxeles** (aún), y un bot sin IA podría jugar mejor.
- Doom: la demo **lee estado de texto**, no imágenes («not on images (yet…)»).

**No verificado:**

- La explicación prefill/decode: es **inferencia del autor**, y él lo declara. La empresa no publica internos.
- Límites de tasa (250.000 tokens/s, 1.200 peticiones/min): solo en sitios de terceros; no aparecen en la parte de doc oficial leída.

## Lo que este vídeo aporta sobre el análisis del 18-sep

1. **El mecanismo físico del «casi gratis»:** sin conjunto de salida cerrado hay bucle de decode; con él, todo el coste es prefill. Es medible en la GPU del lab, no una creencia.
2. **La verificación como caso de uso de primera clase** («score, judge, verify, guardrail, detect jailbreaks»). Hoy se hace con otro LLM como juez: caro, lento y devuelve **opinión en texto**. Es **exactamente el cuello declarado del lab** (verificador del RSI; gate `granite4.2:8b`).
3. **Hallazgo del lado del SDK:** `github.com/typesafe-ai/system-one-adapter-python` (oficial, MIT, 298★) es un **reemplazo del cliente que corre el MISMO contrato (estado + preguntas tipadas + probabilidades) contra APIs de LLM**, con `llm_answer_mode="probabilities"` y `normalize_probabilities`. **Acepta endpoints OpenAI-compatibles** (`base_url`; por defecto Chat Completions) → permite apuntarlo a **LM Studio (`:1234/v1`) u Ollama (`:11434/v1`)**. El «System One casero» deja de ser un diseño a mano: hay un contrato ya escrito que se puede ejecutar en local y a 0 €. Su propósito declarado es comparar coste/velocidad/inteligencia: **medir, no creer**.

**Aviso de higiene de fuentes:** al buscar «Jev» aparece un ecosistema de **clones SEO** con aspecto oficial (`typesafe-ai.com`, `jevai.wiki`, `jev-agent.com`, `jevtypesafe.org`, y un usuario de GitHub `jev-ai` que declara no ser la empresa). Fuentes válidas: `typesafe.ai`, `docs.typesafe.ai`, `github.com/typesafe-ai`, y las pasarelas Cloudflare AI / OpenRouter / Vercel AI Gateway.

## Relevancia LAB

- **La herramienta Jev: sigue fuera.** Es nube, sin pesos publicados y con clave → roza la política local-first. **No se adopta nada.**
- **El patrón sí toca al lab:** verificador del RSI (cuello declarado), `gate-veracidad` (juez), `ai-router` (enrutado antes de gastar la llamada grande), `telegram-inbox` (clasificar OBS/HYP/EXP/DEC es una decisión tipada, no prosa).
- **Detalle reutilizable:** >255 opciones → 2 etapas (puntuar y luego elegir). Aplicable a clasificar catálogos grandes (colección, cafés, candidatos) si alguna vez se automatiza.
- **Prudencia honesta (RULE-015):** medir **calibración** por tramos exige **cientos** de casos etiquetados. El mayor set etiquetado del lab hoy es el de la evaluación de alucinaciones (**~77 ítems**) → sirve para un primer vistazo grueso, **no** para afirmar «está calibrado». Y los umbrales **no se fijan a priori**.

## Decisión

**No se adopta nada** (0 componentes, 0 descargas, 0 cuentas, 0 €, 0 GPU, ningún servicio tocado). El valor es: (a) criterio para leer el hype («no alucina» = no hay error de tipo, no garantía de acierto; la propia empresa lo separa), (b) el mecanismo prefill/decode como palanca medible en local, y (c) el contrato del SDK como vía barata para probar el patrón con modelos locales.

## Futuribles (con señal de activación; ninguno se ejecuta sin señal ni sin OK)

- **F1 — Probar el patrón en local con un modelo ya instalado.** Preguntar una decisión Noul sobre ítems ya etiquetados y ver si devuelve **probabilidades repartidas o todo ~0,99**. Sin instalar nada de TypeSafe, sin cuentas: validar el instrumento antes de creer la métrica. **Señal:** próxima revisión del verificador del RSI o del enrutado.
- **F2 — Medir calibración** (tramos de confianza vs acierto real) además de acierto y alucinación. **Señal:** al validar el próximo instrumento de medición. Requiere ampliar el set etiquetado.
- **F3 — Clasificación de alta cardinalidad en 2 etapas** si algún día se clasifica un catálogo grande del lab.

## Errores del ASR en este vídeo (para futuras lecturas)

`Jeff`/`JF`/`Jef` → **Jev** · `Type Safe`/`TypeSave` → **TypeSafe** · `Jef 1130` → **jev-1.13.0** · «una pregunta genuinamente **antigua**» → **ambigua** · `Choice/Score/Noul` en general bien, pero `No`/`nul` para **Noul** · `Cloud`/`Yemini` → **Claude**/**Gemini** · la cifra del coste de Doom desapareció por completo («unos $ la hora»).

## Fuentes

- Vídeo y ficha: `yt-dlp` sobre `FIOXJXRfsZQ` (leída 25-09-2026).
- **Leídas íntegras:** `https://typesafe.ai/blog/introducing-system-one-models-and-jev` (13.628 chars, vía navegador con JS); `https://docs.typesafe.ai/sdk/python`; `github.com/typesafe-ai/typesafe-sdk-python`; `github.com/typesafe-ai/system-one-adapter-python`.
- Prensa/terceros consultados: The Register (16-sep), Business Wire/Yahoo Finance (15-sep), `flaviocopes.com/jev/`, `jevai.wiki`, `xiaohu.ai`, `relvehq.com`, mirror `typesafe-ai.com` (de donde sale la cifra de 7 $/hora repetida en 5 sitios).
- No accesible: `typesafe.ai/docs` (404; la doc vive en `docs.typesafe.ai`) y `docs.typesafe.ai/llms.txt` (bloqueado por la herramienta).

## Registro

- **Fichero NUEVO.** No se ha modificado `research/analisis-jev-typesafe-system-one.md` (18-sep) ni `04-operations/backlogs/pendientes.md` ni ningún registro acumulativo.
- **Sin commit** (fuera del alcance de esta autorización).
