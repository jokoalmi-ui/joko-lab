# RLM — Recursive Language Models (análisis de fuente primaria)
**VERACIDAD:** [VERIFICADO]

- **Fecha del análisis:** 2026-09-18 16:22 CEST (hora medida con `date`, RULE-012)
- **Análisis previo del lab:** `research/analisis-prime-agent-vs-hermes-rodolfocarrasco.md` (16-ago-2026) — RLM llegó aquí de segunda mano (vídeo de Prime Agent), con el futurible «estado persistente entre tareas».
- **Este documento:** fuente primaria completa. No sustituye a aquel; lo corrige y lo cuantifica.
- **Método:** descarga de la fuente (`curl`) y lectura literal. **0 GPU, 0 descargas de modelos, 0 ejecución del código de RLM, 0 cambios en el lab.**

## 1. Fuente primaria (identificada)

| Dato | Valor |
|---|---|
| Título | *Recursive Language Models* |
| Autores | Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL) |
| Paper | arXiv **2512.24601v1** (`arxiv.org/html/2512.24601v1`) |
| Blog | `alexzhang13.github.io/blog/2025/rlm/` — cita declarada: Zhang & Khattab, **octubre 2025** |
| Código | `github.com/alexzhang13/rlm` (oficial) + `github.com/alexzhang13/rlm-minimal` |
| Hilo original | `x.com/a1zhang/status/1978469116542337259` |
| Financiación | Laude Institute (parcial) |

**Nota honesta sobre la fecha:** el blog declara octubre-2025 y el identificador arXiv apunta a **diciembre-2025**. El post de Instagram que lo trajo era divulgación tardía (17-sep-2026). Es decir: **esto no es nuevo** — el lab ya lo tenía identificado; lo que faltaba era la fuente y los números.

## 2. Qué es exactamente (mecanismo)

**Definición formal del paper:** dado un modelo `M`, una consulta `q` y un contexto `C = [c1..cm]`, se define un scaffold fino `RLM_M(q, C)` que expone **la misma interfaz** (texto → texto) que `M(q, C)`. La diferencia es la existencia de un *tool call* `RLM_M(q̂, Ĉ)` que abre un sub-RLM aislado con su propio entorno, y cuyo resultado vuelve al entorno del llamador. El entorno `E` decide el control de flujo. El caso trivial `E0` (preguntar al modelo con q y C) **es** una llamada base → el RLM es una generalización de la llamada al modelo, no otra cosa.

**Instanciación concreta que evalúan:**
1. El prompt `P` se carga **como variable dentro de un REPL de Python**.
2. Al modelo raíz se le dice que `P` existe ahí y **cuánto mide** — *no lo ve*: literal del blog, "the root LM does not see the context at all — it only knows its size".
3. El modelo **escribe código** para inspeccionar, trocear y mapear sobre `P`, y para lanzar sub-llamadas al modelo (o a uno más pequeño) sobre los trozos.
4. Itera observando los efectos de la ejecución y cierra con `FINAL()` / `FINAL_VAR()`.
5. En los experimentos: **profundidad de recursión = 1** (el raíz llama LMs, no RLMs).

**Patrones que emergen solos (observados en trayectorias):**
- **Peek:** al arrancar, el raíz no ve nada; mira el tamaño y luego, "como un programador", los primeros 2000 caracteres para entender la estructura.
- **Grep/regex:** reduce el espacio de búsqueda por palabras o patrones, **sin** retrieval semántico.
- **Partition + Map:** trocea y lanza sub-llamadas para etiquetar/mapear semánticamente cada parte.
- **Summarization:** degeneración del anterior; generaliza las estrategias clásicas de resumen.
- **Long-input / long-output:** el caso interesante. LoCoDiff (seguir un diff largo de git): con historiales >75k tokens, **GPT-5 no resuelve ni el 10 %**; el RLM a veces lo resuelve de un tirón *programáticamente* (aplicando los diffs en código en vez de "razonándolos" en tokens).

## 3. Qué NO es (la confusión más fácil de cometer)

El propio paper lo delimita. Tres distinciones que importan para el lab:

| No es | Por qué | Qué lo separa |
|---|---|---|
| **RAG / agentic-RAG** | No hay embeddings, ni índice, ni búsqueda vectorial. El acceso al contexto es **por código** (slicing, regex, `len`). El paper usa BM25/retrieval solo como *baseline a batir*. | En `agentic-rag` el agente **vuelve a recuperar**; aquí el contexto **ya está entero dentro** del entorno y el modelo decide cómo mirarlo. |
| **Context compaction / summarization** | No resume para meter en la ventana: **deja el contexto fuera** y nunca lo mete entero. | El "Summary agent" es uno de los baselines que el RLM supera. |
| **Agentes / subagentes (delegación)** | Los agentes descomponen **por tarea** (intuición humana del experto); el RLM descomponen **por contexto** y la decisión es del modelo. | Literal del blog: "we retain the view that LM calls can be decomposed by the context". |

Y la frase que resume el objetivo: **"no single language model call should require handling a huge context"**.

## 4. Datos duros (verificados en la fuente)

Benchmarks: CodeQA, BrowseComp-Plus (1K), OOLONG, OOLONG-Pairs. Tabla 1, root **GPT-5** (formato `score (coste medio API ± desv.)`; `*` = choca con el límite de contexto):

| Método | CodeQA (23K–4,2M tok) | BrowseComp+ 1K (6M–11M tok) | OOLONG (131K) | OOLONG-Pairs (32K) |
|---|---|---|---|---|
| GPT-5 base | 24.00* ($0.13) | **0.00*** (N/A) | 44.00 ($0.14) | 0.04 ($0.16) |
| RLM (GPT-5 raíz) | **62.00** ($0.11) | **91.33** ($0.99) | **56.50** ($0.43) | **58.00** ($0.33) |
| RLM sin sub-llamadas | 58.00 ($0.18) | 88.00 ($0.44) | 46.00 ($0.37) | 43.93 ($0.69) |
| Summary agent | 58.00 ($1.31) | 70.47 ($0.57) | 46.00 ($0.13) | 0.01 ($0.13) |
| CodeAct + BM25 | 22.00* ($0.06) | 51.00 ($0.71) | 38.00 ($0.61) | 24.67 ($0.75) |

Con **Qwen3-Coder-480B** como raíz: RLM 56.00 / 44.66 / 48.00 / 23.11 frente a base 20.00* / 0.00* / 36.00 / 0.06.

**Observaciones literales del paper:**
1. **Escala a 10M+ tokens** y supera a base LMs y scaffolds task-agnostic "hasta 2×", con coste comparable o menor. S-NIAH, OOLONG, OOLONG-Pairs se escalan de 2^13 a 2^18 tokens; la ventana de GPT-5 es 272K.
2. **El REPL es necesario para contextos largos; la recursión aporta en contexto denso en información.** La ablación *sin* sub-llamadas ya supera al base y escala más allá; pero en CodeQA y BrowseComp+ con Qwen3-Coder llega a superar al RLM completo (+17,9 % y +3 %).
3. **La degradación del RLM es mucho más lenta** que la del base, y **por encima de 2^14 tokens el RLM gana consistentemente**… pero *"el LM base supera al RLM en el régimen de contexto pequeño"* → **hay un punto de cruce**: no es mejor para todo.
4. **Coste: mediana comparable, colas caras.** "Comparable o inferior en el percentil 50, pero aumentos bruscos en la cola" por trayectorias largas (varianza alta).

**Dato económico concreto:** en BrowseComp-Plus (1K), que GPT-5-mini ingiera 6–11M tokens cuesta **$1.50–$2.75**; RLM(GPT-5) sale a **$0.99 medio** y supera a los baselines de resumen y retrieval en **>29 %**. En OOLONG, RLM(GPT-5-mini) supera a GPT-5 en **+34 puntos (~114 %)** a 132k tokens y **+15 puntos (~49 %)** a 263k, con coste por consulta menor de media.

## 5. Resultados NEGATIVOS que declara el propio paper (Apéndice A)

Esto es lo más útil para el lab y lo que ningún post de Instagram cuenta:

1. **El mismo system prompt entre modelos es problemático.** El prompt se escribió con ejemplos para GPT-5; con Qwen3-Coder producía trayectorias indeseadas y hubo que **añadir una frase** para evitar el exceso de sub-llamadas.
2. **Modelos sin capacidad de código suficiente fracasan como RLM.** Cita literal: Qwen3-8B "struggled without sufficient coding abilities". El RLM **depende** de razonar y operar el contexto en un REPL.
3. **Modelos "thinking" sin suficientes tokens de salida fallan.** Con Qwen3-235B-A22B las trayectorias **se quedaban sin tokens** porque el *thinking* se comía el máximo de salida por llamada (mejoraba, pero mucho menos que los modelos de la tabla).
4. **RLM sin llamadas asíncronas es lento.** Implementaron las sub-llamadas como bloqueantes/secuenciales: "slow, especially compared to just the base model". Y en el blog: cada consulta va de **unos segundos a varios minutos** según la partición, y **no usaron prefix caching**.
5. **Distinguir "pensamiento" de "respuesta final" es frágil.** Se hace con etiquetas `FINAL()`/`FINAL_VAR()`; el modelo a veces **emite su plan como respuesta final**. Mitigado con salvaguardas menores, no resuelto.

## 6. Limitaciones declaradas (§5)

- Mecanismo óptimo **sin explorar**; probaron síncrono + REPL Python.
- **Profundidad 1** por decisión (no por límite).
- **Sin entrenar** modelos para ser RLM: "current models are inefficient decision makers over their context".
- Sin garantías fuertes sobre **coste total ni tiempo total** de una llamada (solo el número máximo de iteraciones).

## 7. Lectura para el lab (Joko Lab)

### Lo que NO se sostiene en local hoy (4 bloqueos reales)

1. **Capacidad de código del modelo raíz.** Los negative results 2 y 3 son exactamente el perfil de los modelos locales del lab: pequeños y con *thinking* que consume salida. Un raíz local flojo produciría trayectorias malas — y el lab ya tiene medido que el modelo local va a **7,7 tok/s**.
2. **Paralelismo.** La ventaja estructural del RLM (raíz caro + sub-llamadas baratas masivas) **depende de ejecutarlas en paralelo**. Con **una GPU de 12 GB** no hay paralelismo real → se paga el modo secuencial que el paper declara lento (negative result 4).
3. **El REPL es ejecución de código generado por el modelo.** Eso choca de frente con la postura del lab: gate fail-closed, mínimo privilegio, RULE-010 (ceder control), comandos nunca automáticos. Adoptarlo exigiría un **sandbox read-only, sin red y sin acceso al stack protegido** antes de cualquier prueba.
4. **Cruce de régimen.** Observación 3: en contextos pequeños el modelo base **gana** al RLM. La mayoría de consultas del lab caben en ventana → un RLM ahí sería coste y latencia sin mejora.

### Lo que SÍ es accionable (la lectura local-first)

- **Híbrido que el lab ya tiene montado:** raíz en **cloud** (barato y con contexto grande) + sub-llamadas **locales**. Es el patrón del `ai-router` (cloud para orquestar, local para volumen) aplicado a contexto. No hay que inventarlo: hay que probarlo.
- **El caso de uso natural no es el RAG, son los corpus grandes que hoy se leen enteros o se trocean mal:** `sesiones-*.jsonl` (histórico completo, megas), el backlog (756 KB), los `04-operations/metrics/`, los **873 `SKILL.md`** de la biblioteca externa, `MEMORY.md`/`USER.md` acumulados.
- **Lo que el paper demuestra y el lab puede aprovechar sin comprar nada:** para preguntas de **conteo/agregación sobre muchos registros** (¿cuántas veces…?, ¿en qué sesiones…?), iterar en código sobre el fichero **es más fiable que pedirle al modelo que "lo recuerde"** — que es literalmente el fallo que el lab vigila con el gate de veracidad.

### Veredicto

**Futurible con señal, no implementación.** El lab ya tiene los componentes conceptuales (contexto como variable lo tiene a medias: RAG + skills + ficheros; el REPL persistente ya estaba anotado como futurible el 16-ago). Lo nuevo que aporta la fuente es: (a) **el punto de cruce** (por debajo de ~2^14 tokens el RLM no compensa) y (b) **cinco resultados negativos** que explican por qué en local no saldría gratis.

## 8. Experimento mínimo propuesto (NO ejecutado, NO autorizado)

- **Hipótesis:** en una pregunta de agregación sobre un corpus local grande (p. ej. contar/ubicar un patrón real en `sesiones-*.jsonl`), un *RLM-lite* (raíz cloud + 2 herramientas: `peek` y `grep`/regex por código, sub-llamadas locales) acierta **más** que (a) el RAG actual y (b) el mismo modelo recibiendo fragmentos recuperados.
- **Instrumento antes de confiar en la métrica** (RULE-015): definir la verdad de referencia **contando a mano con `grep`/Python**, no con el propio modelo.
- **Métrica:** acierto/error por pregunta + tiempo total + nº de sub-llamadas. Nada de estimaciones.
- **Criterio de decisión previo:** si no supera al RAG actual en acierto **y** el tiempo se mantiene dentro de lo usable, se descarta y se archiva como negativo.
- **Requisito de seguridad previo:** REPL en sandbox sin red, sin `sudo`, read-only sobre el corpus, sin acceso a `/mnt/ssd_ia_datos/n8n` ni al stack protegido.
- **Estado:** propuesto, sin fecha. Depende de OK explícito.

## 9. Qué NO se ha hecho en este análisis

- No he descargado ni cargado ningún modelo.
- No he ejecutado ni clonado el código de RLM (`rlm` / `rlm-minimal`): solo he leído su README.
- No he tocado GPU, ComfyUI, LM Studio, Ollama ni Docker.
- No he modificado nada del lab más allá de este fichero y su registro en el backlog.

## 10. Fuentes

- arXiv 2512.24601v1 — `https://arxiv.org/html/2512.24601v1` (leído: 96.723 caracteres de texto).
- Blog del autor — `https://alexzhang13.github.io/blog/2025/rlm/` (leído: 34.972 caracteres).
- README oficial — `https://github.com/alexzhang13/rlm` (15.220 B) y `rlm-minimal` (3.082 B).
- Cifras de la sección 4: Tabla 1 y Observaciones 1–4 del paper; Apéndice A para los resultados negativos; §5 para limitaciones.
