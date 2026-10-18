---
title: "Análisis — Post de LinkedIn (Valentin Ayesa): Jev de TypeSafe AI y los modelos «System One» que no generan texto"
type: research
fecha: 2026-09-18
---

# Análisis — Post de LinkedIn (Valentin Ayesa): Jev de TypeSafe AI y los modelos «System One» que no generan texto

**VERACIDAD:** [VERIFICADO]

**Fuente:** post de LinkedIn de **Valentin Ayesa** — «🐴 Dejad de usar un LLM que tarda 10 segundos para decidir algo que un "sí o no" resuelve en 70 milisegundos…». Enlace corto `https://lnkd.in/p/e4phu648` → `https://www.linkedin.com/posts/valentinayesa_dejad-de-usar-un-llm-que-tarda-10-segundos-share-7506644103200235520-vNB0/`. Lectura: **18-sep-2026, 23:54 CEST** (hora del sistema verificada con `date`). Estado del post en la lectura: autor marca **«12 h»** de antigüedad, **14 reacciones**, **5 comentarios** (3 no visibles sin sesión). Cuerpo del post (medido con `innerText` sobre el `article`): **2.031 caracteres**.

**Comentarios visibles (2 de 5), literales:**
- **Roberto Holgado Cid** (1 reacción): «Yo la estoy usando para clasificar correos por ahora mientras busco más casos de uso. Me estoy planteando para revisar copy..»
- **Iván López Herráez** (1 reacción): «Yo tengo acceso a la beta y estos días lo estaré probando.💪 A ver qué tal.»

**Método de extracción:** navegador con sesión no iniciada (el enlace corto `lnkd.in` redirige solo; `curl` da 403 por el bloqueo de bots de LinkedIn) + lectura del `article` completo con JS (`innerText`) + contraste con fuentes independientes por `web_search`/`web_extract`. Sin GPU, sin modelos cargados, sin cuentas nuevas, 0 €.

## Qué dice el post (contenido literal resumido)

- **Jev**, en beta, de **TypeSafe AI** («ex-OpenAI, gente que estuvo detrás de RLHF»), rompe con «un modelo grande para todo».
- **No genera texto libre**: entrega valores estructurados con probabilidad calibrada, y el post **atribuye a la empresa** («afirman») que no puede alucinar porque el error de tipo es matemáticamente imposible.
- **Caso que cita**: un usuario con acceso a la beta lo puso en producción real como **«puerta de intención»**, para clasificar qué quiere hacer el usuario antes de enrutar a otro modelo, con **casi 70 casos de prueba repetidos tres veces**: acertó todos, **media de 250 ms**. «Eso es lo que de verdad importa: no la demo, el benchmark con casos reales».
- **Límites que declara**: no acepta imágenes, no da salida en prosa, **no es compatible con la API de OpenAI** («no lo cambias en un config, hay que programarlo de cero»). «No es un sustituto de tu LLM conversacional, es una pieza nueva para un problema distinto: decisiones rápidas y baratas dentro del código».
- **Negocio**: input **0,042 $/millón de tokens**, output **gratis**. Nombre por **Jevons**: cuando algo se abarata mucho no se consume menos, se consume más; la apuesta es que aparezcan casos de uso que antes no salían a cuenta.

## Verificación externa

**Confirmado por fuentes independientes (comunicado y prensa, 15-16-sep-2026):**

- **TypeSafe AI salió de stealth el 15-sep-2026** con **40 M$ de semilla liderados por DCVC** (comunicado vía Business Wire, replicado en Yahoo Finance; Business Wire y StartupHub lo fechan el 15-sep). Fundada en **2024**, **San Francisco**, por **Diogo Almeida** (ex-OpenAI, co-autor de RLHF/InstructGPT, ChatGPT y GPT-4), **Erik Gafni** (fundador de la genómica Ravel) y **Sasha Sheng** (ex-Meta FAIR). Fuentes: Business Wire/Yahoo Finance (15-sep), The Register (16-sep), StartupHub.ai, ts2.tech, byteiota, InfoWorld, The Decoder.
- **Jev es el primer modelo «System One»**: modelos pequeños y rápidos para **decidir**, no para generar texto. La API recibe un `state` (texto, objeto o lista) y una lista de preguntas tipadas; devuelve una respuesta por pregunta **en un solo paso paralelo** (no autoregresivo). En palabras de TypeSafe: «frontier-intelligence function call: unstructured state in, typed probabilistic decisions out».
- **Tres primitivas, y nada más** (documentadas en la API de TypeSafe, el cliente Elixir y el catálogo de Cloudflare AI):
  - **Noul** (sí/no): devuelve `noul`, probabilidad de 0 a 1. La API no da `confidence` aparte (un «no» seguro y un «sí» seguro son igual de seguros); los clientes la derivan con `max(noul, 1-noul)`, que nunca baja de 0,5.
  - **Choice** (una opción de una lista): devuelve la opción ganadora, la distribución completa (`probabilities`, suman 1) y `confidence` (cuánto de apuntada está la distribución en el ganador). Hasta **255 opciones**; se recomienda incluir una opción `other` para no forzar siempre la opción más parecida.
  - **Score** (posición en una escala ordenada): devuelve **puntuación fraccionaria** entre niveles (p. ej. `1.6`), la probabilidad por nivel y `confidence`. Hasta **10 niveles**.
  - Ejemplo real de respuesta (docs de Cloudflare): `{"department": {"choice": "billing", "confidence": 0.8, "probabilities": {"billing": 0.87, "sales": 0, "technical": 0.13}}}` con `usage: input 426 / output 73` tokens.
- **Entrenamiento declarado: RLCD (Reinforcement Learning for Calibrated Decisions)**, no RLHF. RLHF optimiza lo que el humano prefiere; RLCD optimiza **calibración**: lo que se responde con 90 % de probabilidad debería acertar ~90 % de las veces en agregado. TypeSafe lo presenta como la distinción central de su investigación.
- **Latencia y precio declarados**: **<100 ms** según el comunicado («hasta 100 veces más rápido y menos caro»); **70-500 ms** y «40x-200x más rápido» según The Register; **~100 ms** en la mayoría de llamadas según el análisis técnico de **flaviocopes.com/jev/** (17-sep-2026). Demos de la compañía: **0,114 s** frente a **8,566 s** de un modelo frontera de chat; bot de **Doom** con decisiones de estado en tiempo real a **10 consultas por segundo** y ~**7 $/hora**. Precio: **0,042 $/M tokens de entrada, salida gratis** («too cheap to meter»). Los **250 ms** del usuario de la beta del post caen dentro del rango declarado.
- **Disponibilidad real, no solo waitlist**: Jev aparece ya en **Cloudflare AI** (`typesafe/jev`) y en **OpenRouter** (`~typesafe/jev-latest`, endpoint `api/alpha/decisions`). Es decir: es accesible por API, pero **en la nube de terceros**.
- **Un detalle que el post no menciona**: como la respuesta no es texto libre, **no hay nada que parsear ni superficie de inyección de prompt en la salida** — la forma es el contrato de la API (documentación del cliente System One).

**Matizado (es la corrección de fondo):**

- **«No puede alucinar» es garantía ESTRUCTURAL, no de acierto.** Es imposible un **error de tipo**: la respuesta no puede contener un valor fuera del esquema definido (TypeSafe declara **0 % de tasa de alucinación** y lo etiqueta explícitamente como **garantía de diseño, medida aparte de sus resultados de test**). **Nada impide una elección equivocada dentro de las opciones permitidas**: un ticket etiquetado «billing» puede pertenecer a soporte técnico y la validación de formato pasa igual (gadgetsnow India Times, ts2.tech, The Decoder, orcarouter). La propia TypeSafe separa **type safety** de **verdad**.
- **`confidence` NO es una garantía de calibración.** La documentación es explícita: mide **cuánto de apuntada está la distribución en esa respuesta concreta**, «no es lo mismo que la probabilidad de que esta sea la respuesta correcta». Es una propiedad de la distribución devuelta para ese `state`.
- **Los grandes números son auto-publicados.** El «193,6 veces más rápido y 444,6 veces más barato» sale de **cuatro flujos de ejemplo probados por TypeSafe**, y sus benchmarks comparan contra **modelos grandes envueltos para producir respuestas compatibles con Jev**, algo que la empresa dice que mejora la precisión pero que puede encarecer y ralentizar al rival (ts2.tech, byteiota, gadgetsnow). Las cifras de velocidad y coste **no están verificadas de forma independiente** y variarán por carga y ubicación de red.
- **Jev no es único en «salida estructurada»**: OpenAI tiene Structured Outputs y el **Vercel AI SDK 7** (desde 7.0.105) incorpora `experimental_evaluate` con **TypeSafe como provider nativo**, además de adaptadores para OpenAI/Anthropic/Google. Lo diferencial declarado es latencia, coste y devolver la **distribución completa en paralelo**, no el hecho de estar restringido a un esquema.

**No verificado en ninguna fuente (queda como afirmación del post):**

- Los **«casi 70 casos de prueba repetidos tres veces, todos acertados, media de 250 ms»**. No aparecen en el comunicado, ni en la prensa, ni en el análisis de Flavio Copes, ni en los 2 comentarios visibles; **el post no cita de dónde salen**.
- **«No compatible con la API de OpenAI»**: no confirmado ni desmentido en lo leído (Flavio describe un provider propio en el SDK de Vercel, coherente pero no probatorio).
- **«No acepta imágenes»**: coherente con un modelo de decisión tipada, pero no leído explícitamente en ninguna fuente. (OpenRouter sí indica que **acepta texto** como `state`.)

## El patrón replicable (vale sin Jev)

1. **Separar DECIDIR de ESCRIBIR.** La decisión va en el código, tipada y con probabilidad; el LLM aparece solo cuando hace falta texto.
2. **Devolver probabilidad calibrada en vez de un booleano.** Permite que el código decida actuar, revisar o escalar.
3. **Los umbrales viven en TU código, no en el modelo, y se miden, no se suponen.** TypeSafe lo dice en su propia documentación: los umbrales de confianza **dependen del caso de uso y hay que probarlos contra tus propios ejemplos etiquetados**. Es exactamente **RULE-015** (los umbrales no se fijan a priori) y **RULE-013** (la cifra solo vale si está medida).
4. **Test de calibración, barato y sin infraestructura de ML** (procedimiento documentado, replicable aquí): tomar unos cientos de casos ya etiquetados, preguntar la decisión que importa, agrupar las respuestas por la confianza declarada y comprobar si el grupo de 0,9 acierta ~90 %, el de 0,7 ~70 %… Un modelo bien calibrado dibuja la diagonal; uno que solo es «confiado» amontona todo por encima de 0,9 y acierta el 70 %. **De ese mismo test salen los umbrales**: automatizar el grupo alto y mandar la banda media al modelo caro o a un humano.
5. **Garantía de forma ≠ garantía de verdad.** Un esquema cerrado elimina el error de tipo y deja intacto el error de juicio. Es la misma separación que el lab ya aplica con el **verificador de fidelidad determinista** (`tools/verificador_fidelidad.py`, 25-ago-2026): el que genera no se valida a sí mismo.
6. **El benchmark con casos reales, no la demo** (lo dice el propio post) y **desconfiar de las cifras auto-publicadas**, incluidas las de este producto.

## Relevancia LAB

- **Jev como herramienta: no entra.** Es **nube** (con lista de espera en el sitio propio, pero ya servido desde Cloudflare y OpenRouter), **sin pesos publicados** y **sin versión local** → choca con la política local-first del lab. El lab no manda datos a APIs de terceros sin decisión explícita.
- **El patrón sí aplica, y el equivalente local existe ya**: **decodificación restringida por gramática** (GBNF en `llama.cpp`, *structured output* en LM Studio) con un modelo pequeño devolviendo una elección de un conjunto cerrado en una sola llamada. Eso es un «System One» casero: 0 € y los datos dentro de casa.
- **Dónde toca del lab, concretamente**:
  - **`ai-router`** (capa de sesión): enrutar antes de gastar la llamada del modelo grande es literalmente su función.
  - **`telegram-inbox`**: clasificar cada mensaje en OBS / HYP / EXP / DEC es una decisión tipada, no prosa.
  - **Medición**: la **calibración** es una métrica que el lab **no mide hoy** (mide acierto y alucinación). El test por buckets del punto 4 es replicable tal cual y encaja con RULE-015 y con el gate de veracidad.
  - **Seguridad**: una respuesta sin texto libre tampoco tiene superficie de inyección de prompt en la salida — argumento reutilizable para justificar clasificadores cerrados frente a «pídele al LLM un JSON».
- **Lo que el lab ya hace y este caso valida desde fuera**: modelo pequeño para decidir + modelo grande para redactar (roles separados en `lm-studio`), verificación determinista de los datos antes de emitir (`verificador_fidelidad.py`) y umbrales medidos en vez de supuestos.

## Decisión

**No se adopta nada** (0 componentes, 0 descargas, 0 cuentas, 0 €, 0 GPU, ningún servicio tocado). Jev no es instalable ni local, y el patrón que lo hace interesante **ya es replicable hoy con lo que el lab tiene**. El valor del análisis es (a) **criterio técnico** para leer el hype («no puede alucinar» = no puede equivocarse de forma; `confidence` ≠ probabilidad de acierto), (b) un **patrón de arquitectura** con nombre — decidir ≠ escribir, con probabilidad calibrada y umbrales medidos — y (c) **material** para LinkedIn (System One, RLCD, calibración, coste como palanca de la paradoja de Jevons).

## Futuribles (con señal de activación; no se ejecuta ninguno sin la señal ni sin OK del usuario)

- **F1 — Réplica local del patrón System One**: clasificador con gramática restringida + modelo pequeño midiendo **latencia y acierto** contra la llamada al LLM actual. **Señal**: la próxima vez que haya que tocar el enrutado (`ai-router`) o un clasificador de entrada.
- **F2 — Clasificador del `telegram-inbox`** con conjunto cerrado de categorías, **umbral medido** y escalada al modelo grande solo por debajo del umbral. **Señal**: próxima revisión de esa skill.
- **F3 — Medir calibración** (buckets de confianza vs acierto real, no solo acierto global) en las evaluaciones del lab. **Señal**: al validar el próximo instrumento de medición (RULE-015).

## Registro

- Backlog acumulativo activo: `04-operations/backlogs/2026-07-31-backlog.md`, entrada fechada el 18-sep-2026, con backup previo `2026-07-31-backlog.md.bak-20260918-jev` (RULE-008).
- Cruce previo anti-duplicado: `search_files` en `research/` → **no había** análisis previo de Jev ni de TypeSafe.

## Fuentes

- Post: `https://lnkd.in/p/e4phu648` (LinkedIn, Valentin Ayesa, leído 18-sep-2026 23:54 CEST).
- Comunicado de salida de stealth: Business Wire, 15-sep-2026, vía `https://finance.yahoo.com/technology/ai/articles/typesafe-ai-emerges-stealth-40m-190000776.html`.
- `https://typesafe.ai/blog/introducing-system-one-models-and-jev` (blog oficial; en esta sesión devolvió vacío por falta de clave del backend de extracción — citado solo como referencia, no leído).
- `https://flaviocopes.com/jev/` (Flavio Copes, 17-sep-2026) — análisis técnico, leído.
- `https://developers.cloudflare.com/ai/models/typesafe/jev/` y `https://typesafe-api.hexdocs.pm/system_one.html` (documentación de la API y del cliente: primitivas, límites, `confidence`).
- `https://openrouter.ai/~typesafe/jev-latest` (disponibilidad por terceros).
- Prensa: The Register (16-sep-2026), StartupHub.ai, ts2.tech, byteiota, gadgetsnow India Times, The Decoder, InfoWorld, OrcaRouter.
