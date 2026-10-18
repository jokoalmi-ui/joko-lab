---
title: "Análisis — Post techyy_banda: carrusel «AI Agents» (48 items, 23 bloques temáticos) (14-sep-2026)"
type: research
---

# Análisis — Post techyy_banda: carrusel «AI Agents»

**Fuente:** https://www.instagram.com/p/DdEBtm8CP2D/ (shortcode `DdEBtm8CP2D`)
**Autor:** @techyy_banda (perfil: Abhinav Gupta) — canal **NO vigilado**
**Fecha del post:** 9-sep-2026 · **Métricas:** 270 me gusta / 296 comentarios (propio de «engagement bait»)
**Caption literal:** «🔗 Want the link? 👇 Comment "LINK" and I'll send it to you 📩🔥» (no aporta contenido)
**Método:** navegador → HTML a disco → 15 imágenes CDN descargadas (1440×1920) → transcripción con **GLM-4.6V-Flash servido con llama.cpp headless (:1235)** → conteo y comparación sobre las transcripciones con script (no a ojo).
**VERACIDAD:** [VERIFICADO]

> **CORRECCIÓN de la v1 de este informe (14-sep):** la primera versión afirmaba «34 preguntas de 47 con 13 huecos» y «slides cortadas a mitad de frase (#33, #45)». **Ambas cosas eran erróneas** (dato arrastrado de un resumen de sesión, no verificado). El conteo real es **48 items numerados 1-48, sin ningún hueco**, y **no hay texto cortado**: las 15 slides cierran su contenido. Esta versión sustituye a la anterior.

## CONTENIDO

Carrusel de 15 imágenes rotuladas «[ AI Agents ] - Page [1..15]», con **48 items numerados 1-48** al estilo «preguntas de entrevista», cada uno con su respuesta.

**Paginación (regular):** la página 1 lleva 6 items (1-6); las páginas 2-15 llevan 3 items cada una (7-48). **46 son preguntas** y 2 son secciones del documento (#5 «Agent Workflow Diagram», #6 «Key Takeaways»).

**Los 23 bloques temáticos reales** (agrupación propia sobre los 48 items; los números entre corchetes son los items):

| # | Bloque | Items | Se repite |
|---|--------|-------|-----------|
| 1 | ReAct (Reason+Act) y ReAct Agent | 10, 22, 27, 28 | 4× |
| 2 | Herramientas: tools / tool use / tool calling | 12, 18, 24, 26 | 4× |
| 3 | Agentic AI, workflow agéntico y patrones | 13, 33, 34, 36 | 4× |
| 4 | Agentic RAG | 30, 37, 41, 43 | 4× |
| 5 | Qué es un agente / autónomo / vs chatbot | 1, 32, 46 | 3× |
| 6 | Componentes y funcionamiento (percepción-razón-acción) | 2, 4, 5 | 3× |
| 7 | Frameworks (LangChain, AutoGen, CrewAI, Bee, LlamaIndex, Semantic Kernel) | 7, 29, 47 | 3× |
| 8 | Casos de uso, aplicaciones reales y empresa | 9, 38, 42 | 3× |
| 9 | Multi-Agent System (MAS) | 11, 14, 31 | 3× |
| 10 | Tipos de agentes (arquitectura / objetivo) | 3, 35 | 2× |
| 11 | RAG (Retrieval-Augmented Generation) | 16, 20 | 2× |
| 12 | Desafíos / limitaciones y futuro | 39, 48 | 2× |
| 13 | Key takeaways (no es pregunta) | 6 | — |
| 14 | Ejemplo práctico / construir un agente | 8 | — |
| 15 | Comunicación entre agentes | 15 | — |
| 16 | LangChain | 17 | — |
| 17 | Prompt engineering | 19 | — |
| 18 | Alucinaciones en LLMs | 21 | — |
| 19 | Chain-of-Thought (CoT) | 23 | — |
| 20 | Memoria del agente | 25 | — |
| 21 | Diferencia LLM vs agente | 40 | — |
| 22 | MCP (Model Context Protocol) | 44 | — |
| 23 | Function calling | 45 | — |

## HALLAZGOS (verificados)

1. **48 items para 23 conceptos: 25 items redundantes (52 %).** Cuatro conceptos aparecen cuatro veces cada uno (ReAct, herramientas, agentic AI, agentic RAG) y cinco aparecen tres veces.
2. **Una sola frase clonada literalmente**: la definición de MAS («A Multi-Agent System (MAS) is a system where multiple AI agents work together (or interact) to achieve a common goal or solve a complex problem.») aparece idéntica en los items 11, 14 y 31. El resto de repeticiones **no son copias**: son redacciones distintas del mismo concepto (similitud texto a texto del 10-26 %). Es decir, el carrusel se repite en temario, no en texto.
3. **Nivel: básico-divulgativo.** Definición + «Key Points» + tabla comparativa + diagrama de cajas. El único código es un snippet clásico de LangChain (item 8). No hay implementación real, ni datos, ni benchmarks, ni fuentes.
4. **Sin nombres inventados:** LangChain, AutoGen, CrewAI, LlamaIndex, Semantic Kernel, MCP y function calling son correctos; «Bee» existe (Bee Agent Framework, de IBM). No hay cifras que contrastar.
5. **El valor está en las slides, no en el caption**: el caption solo pide comentarios (296 comentarios para 270 me gusta).

## VALOR

**Para el LAB: bajo.** Nada accionable: ninguna técnica, dato ni herramienta nueva respecto a lo que el lab ya opera (agentes, RAG con LanceDB, MCP, memoria, medición de modelos).

**Para una serie DIVULGATIVA de IA y agentes: útil como MAPA, no como texto.**
- Los 23 bloques son un **índice ya ordenado** de los temas que el público busca («qué es…», «diferencia entre…», «cómo funciona…»). Sirve para planificar piezas, no para redactarlas.
- Donde el autor **se repite** (ReAct 4×, agentic RAG 4×, tools 4×, MAS 3×) es exactamente donde el público se lía: ReAct vs CoT, RAG vs agentic RAG, tools vs tool calling vs function calling, agente vs LLM vs chatbot, agente único vs MAS. Esos son los temas con más recorrido divulgativo.
- **El texto del post no es publicable tal cual**: definiciones planas, sin ejemplos, sin datos y con 52 % de repetición. Cada pieza necesita aportar lo que aquí falta: un ejemplo real, una comparativa y un dato medible.

## CLASIFICACIÓN POR NIVELES (de lo básico a lo más avanzado) — 14-sep-2026

Decidida con el usuario el 14-sep-2026. **Sustituye** a la propuesta previa de «7 piezas»:
misma materia, reordenada por dificultad y con los dos niveles que el post no cubría.

Los 23 bloques temáticos del carrusel se reordenan en **6 niveles**; cada nivel = una pieza de la serie.

| Nivel | Tema | Bloques del post (items) | Usos (para qué sirve) |
|---|---|---|---|
| **0 — Fundamentos** *(hueco: el post no lo cubre)* | Qué es un LLM: tokens, siguiente palabra, ventana de contexto, parámetros; IA vs ML vs DL vs LLM | — (solo implícito) | Chat, resumir, redactar, clasificar, traducir |
| **1 — Se usa hablando: instrucciones** | Prompt engineering; few-shot, rol, formato de salida, temperatura/top-p/max tokens | 17 | Asistentes, redacción, extracción de datos de un texto |
| **2 — El modelo conectado al mundo (datos y herramientas)** | RAG, embeddings y base vectorial, tools / tool use / tool calling, function calling, MCP, chain-of-thought | 11, 2, 23, 22, 19 | Preguntar a tus documentos, calcular, llamar APIs |
| **3 — El agente: el bucle** | Qué es un agente / vs chatbot / LLM vs agente; percibir→razonar→actuar; tipos de agentes; ReAct; memoria; ejemplo práctico | 5, 21, 6, 10, 1, 20, 14 | Tareas de varios pasos (buscar → decidir → ejecutar → revisar) |
| **4 — De uno a muchos: agentes que colaboran** | RAG vs agentic RAG; agentic AI y patrones de workflow; MAS; comunicación entre agentes; frameworks y LangChain | 4, 3, 9, 15, 7, 16 | Pipelines de investigación, redactar+revisar, especialidades |
| **5 — Producción: fiabilidad, coste y límites** *(casi ausente en el post)* | Alucinaciones y verificación; evals y observabilidad; coste y latencia (cloud vs local); seguridad y permisos; desafíos/futuro y casos de uso | 18, 12, 8 (parcial: 39, 48) | Poner agentes a trabajar sin que rompan nada |

**Huecos verificados del mapa original:** el post cubre bien los niveles 2-4, **no tiene nivel 0** y dedica solo 2 items sueltos al nivel 5. La repetición (52 %) se concentra en la frontera 2↔3↔4 (ReAct ×4, herramientas ×4, agentic RAG ×4), que es donde el público se lía y donde conviene una pieza por confusión.

El bloque 13 («Key Takeaways») no es tema: es el cierre del post.

## SUBNIVELES POR NIVEL (escalera homogénea de 5 pasos) — 14-sep-2026

Criterio decidido con el usuario el 14-sep: **cada pieza de cada nivel repite la misma escalera de 5 pasos**, para que la serie salga homogénea. El paso 5 (dato medible) **solo se publica con dato verificado y su fuente** (gate de veracidad / RULE-013 y RULE-015); si no hay dato, se mide o se deja fuera.

### NIVEL 0 — Fundamentos: qué es un LLM
| Subnivel | Contenido |
|---|---|
| 0.1 Qué es | Un modelo que **genera** texto prediciendo el fragmento siguiente (token) tras leer mucho texto. No consulta una base de datos. |
| 0.2 Cómo funciona | Texto → tokens → probabilidad de cada siguiente token → se elige uno y se repite, en cadena. |
| 0.3 Confusión típica | «La IA busca en internet» / «sabe cosas como una enciclopedia». Realidad: genera por patrones, por eso **se inventa cosas** (puerta al nivel 5). IA generativa ≠ buscador. |
| 0.4 Ejemplo real | Pedirle el autor de un documento interno que no ha visto → lo inventa. El mismo caso con RAG (nivel 2) → responde citando. |
| 0.5 Dato medible | Coste por millón de tokens y **ventana de contexto** de un modelo concreto (con modelo, fuente y fecha). *Pendiente de verificar antes de publicar.* |

### NIVEL 1 — Se usa hablando: instrucciones
| Subnivel | Contenido |
|---|---|
| 1.1 Qué es | El **prompt**: la instrucción que fija tarea, formato de salida y rol. |
| 1.2 Cómo funciona | La instrucción es contexto: condiciona la probabilidad de cada token. *Few-shot* = dar ejemplos. Formato exigido = salida parseable. |
| 1.3 Confusión típica | «Prompt engineering = trucos mágicos» o «cuanto más largo mejor». Y confundir temperatura con «inteligencia» (sube variedad, rompe consistencia de formato). |
| 1.4 Ejemplo real | La misma pregunta con y sin «responde solo con JSON» → salida usable por código vs texto libre. |
| 1.5 Dato medible | % de salidas que cumplen el formato exigido. **Ejemplo propio ya medido:** batería JSON/tool calling del lab (`tools/evaluar_json_tool_calling.py` → 6/8 y 3/3 en un modelo local, 14-sep-2026). |

### NIVEL 2 — El modelo conectado al mundo (datos y herramientas)
| Subnivel | Contenido |
|---|---|
| 2.1 Qué es | Dar al modelo (a) **tus datos** (RAG) y (b) **acciones** (herramientas), para que deje de adivinar. |
| 2.2 Cómo funciona | **RAG:** trocear → convertir en vectores (embeddings) → buscar por similitud → meter los fragmentos en el prompt. **Herramientas:** el modelo devuelve una llamada estructurada → tu código la ejecuta → le devuelve el resultado. **CoT:** razonar antes de responder. |
| 2.3 Confusión típica | **tools vs tool calling vs function calling vs MCP** (cuatro nombres, tres cosas y un estándar). Y **RAG vs fine-tuning** (¿recuerdo o reentreno?). |
| 2.4 Ejemplo real | «¿Cuánto gasta el lab al mes en cloud?» → RAG sobre las facturas + una función que suma (el modelo **no** calcula: llama). |
| 2.5 Dato medible | % de respuestas con cita correcta, latencia de la búsqueda, % de llamadas a herramienta bien formadas. *Pendiente de medir/verificar.* |

### NIVEL 3 — El agente: el bucle
| Subnivel | Contenido |
|---|---|
| 3.1 Qué es | LLM + bucle (pensar → actuar → observar) + herramientas + memoria, con un **objetivo**, sin que tú dictes cada paso. |
| 3.2 Cómo funciona | **ReAct:** pensamiento → acción → observación → repite hasta cerrar la tarea. Memoria corto plazo (la conversación) vs largo plazo (lo que persiste). |
| 3.3 Confusión típica | **ReAct vs CoT** (CoT = pensar antes de responder, una sola vuelta; ReAct = pensar y **actuar** en bucle con el entorno). Agente vs chatbot. |
| 3.4 Ejemplo real | «Busca el precio de este producto en 3 tiendas y hazme una tabla» → varias iteraciones, no una respuesta. |
| 3.5 Dato medible | Pasos por tarea, coste por tarea resuelta, **% de tareas completadas**. *Pendiente de medir.* |

### NIVEL 4 — De uno a muchos: agentes que colaboran
| Subnivel | Contenido |
|---|---|
| 4.1 Qué es | Varios agentes con roles (o un **workflow** con pasos fijos) repartiéndose el trabajo. |
| 4.2 Cómo funciona | Patrones: secuencial, paralelo, fan-out/fan-in, supervisor. Mensajes entre agentes + estado compartido. **Agentic RAG:** el propio agente decide si volver a buscar. |
| 4.3 Confusión típica | **Workflow (pasos fijos) vs agente (decide los pasos)**; «multi-agente» de verdad vs «varios prompts en cadena»; **RAG vs agentic RAG**. |
| 4.4 Ejemplo real | Escritor + crítico + verificador; o RAG agéntico que reformula la búsqueda cuando no encuentra. |
| 4.5 Dato medible | Coste y latencia multi-agente vs un solo agente; nº de reintentos; mejora de precisión al añadir crítico. *Pendiente de medir.* |

### NIVEL 5 — Producción: fiabilidad, coste y límites
| Subnivel | Contenido |
|---|---|
| 5.1 Qué es | Mantener agentes fiables: medir, verificar, limitar permisos y controlar el gasto. |
| 5.2 Cómo funciona | **Evals** con casos de prueba (golden set), **verificación** de salidas (citas, JSON válido), **permisos mínimos**, **observabilidad** (traza de los pasos), límites de coste. |
| 5.3 Confusión típica | «Si funciona en la demo, funciona». Y creer que la alucinación es cosa de modelos malos: es **estadística**, se mide. |
| 5.4 Ejemplo real | **Instrumento del lab**: batería de 81 casos trampa (`tools/evaluar_alucinaciones.py` + `tools/golden_set_alucinaciones.json`) para medir la tasa de alucinación de un modelo local antes de aceptarlo. |
| 5.5 Dato medible | Tasa de alucinación (%), coste por 1.000 consultas, latencia percentil 95. **Ejemplo propio medido:** un modelo local dio **0 de 81** alucinaciones en modo directo (14-sep-2026, modo directo; con razonamiento la tasa bruta fue 9,9 % y real 1,2 %). |

> **Rectificación (30-sep-2026).** Las cifras del bloque 5.4/5.5 se re-midieron contra el crudo antes de
> usarlas en la pieza L5 y dos no se sostienen. El texto de arriba NO se reescribe: queda a la vista.
> - «81 casos trampa» → el set tiene **27 casos** (`tools/golden_set_alucinaciones.json`, categorías
>   contexto 6 / memoria 6 / trampa 8 / ficha 4, más 2 `contexto_ausente` y 1 `ficha_ausente` que deben
>   abstenerse). **81 son respuestas**, no casos: 27 × 3 pasadas.
> - «0 de 81 alucinaciones» → **0 de 27 en cada una de las 3 pasadas** con el razonamiento desactivado
>   (seeds 42/43/44, 14-sep-2026, `ibm/granite4.2:8b-q4_K_M` vía Ollama); equivale a 0 de 81 respuestas.
> - «tasa bruta 9,9 %» → es la **media** de las 3 pasadas con razonamiento no invalidadas
>   (11,11 / 14,81 / 3,70 % → 9,88 %), y **mide al contador, no al modelo**: el clasificador cuenta como
>   invención rechazos honestos. Una cuarta pasada (3,70 %) quedó **invalidada** por ese mismo motivo
>   (`04-operations/metrics/alucinaciones_ledger.jsonl`, tanda 20).
> - «real 1,2 %» → **no aparece en el crudo**: ninguna de las 23 tandas del ledger tiene una tasa entre
>   0,6 % y 1,8 %. Sin fuente: no se publica.
>
> Crudo de la pieza: `research/infografias/serie-ia-agentes/leccion-5-produccion-fiabilidad-coste-y-limites/medicion-alucinaciones-20260914.json`
> (7 pasadas literales). Coste por 1.000 consultas y latencia p95: **sin medir**.

**Estado de los datos medibles:** los subniveles 0.5, 2.5, 3.5 y 4.5 usan cifras de referencia **todavía sin verificar con fuente** → no se publican hasta comprobarlas. Los de 1.5 y 5.4/5.5 son **mediciones propias ya existentes en el lab** (ficheros citados).

**Pendiente (usuario, 14-sep):** los subniveles están construidos (arriba); siguiente paso = verificar los datos medibles y decidir la primera pieza.

## VEREDICTO

- **No accionable** para el sistema del lab; **sí utilizable como índice temático** para la serie divulgativa de IA/agentes.
- Archivado como referencia de contenido, no como conocimiento técnico.
- **Canal @techyy_banda:** repetitivo y de nivel principiante (recomendación: no añadir a la vigilancia; sí reutilizar su temario como checklist).
- **Pendiente de decisión del usuario:** qué piezas de la serie divulgativa se arrancan y en qué orden.
