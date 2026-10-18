---
type: lpa
subtype: lpa
status: active
tags: [lpa]
created: 2026-07-24
---
# Patterns Observed

> Cuaderno de laboratorio.
> Observaciones de comportamiento emergente en la colaboracion humano-IA.
> No forma parte del core de LPA. No tiene nivel de evidencia.
>
> Cada entrada es una observacion unica (E0).
> Solo cuando un patron aparezca en contextos distintos y se repita,
> merecera convertirse en procedimiento LPA.
>
> **Estado:** abierto. Se anotan observaciones sin compromiso de formalizacion.

---

## 2026-07-22 — Constitutional review emerge espontaneamente

**Contexto:** Discusion sobre si implementar la skill `/grill-me` de Matt Pocock.

**Observacion:** Durante la conversacion, Hermes no pregunto "como implemento esto".
Pregunto "merece la pena implementar esto ahora?".
Ese comportamiento surgio sin instruccion explicita — no habia ninguna skill,
procedimiento ni prompt que lo ordenara.

**Forma:** Ante una propuesta de cambio en el sistema, la respuesta no fue
ejecutora sino evaluadora: revisar si encaja en las prioridades actuales,
si hay evidencia suficiente, si el momento es el correcto.

**Potencial:** Si este patron se repite, podria formalizarse como un
procedimiento de "constitutional review" — una pausa obligatoria antes de
cualquier expansion del sistema que verifique necesidad, evidencia y alineacion
con prioridades.

**Registro:** No documentar como procedimiento hasta que aparezca al menos
2 veces mas en contextos distintos.

---

## 2026-07-22 — Las preguntas de una en una producen mejores decisiones

**Contexto:** Analisis de grill-me (Matt Pocock) y su metodo de entrevista.

**Observacion:** El formato de "una pregunta cada vez con recomendacion"
produce respuestas mas meditadas que las descargas de preguntas.
Grill-me lo implementa como skill. En LPA aparece naturalmente en
conversaciones de diseno cuando Hermes no acelera.

**Forma:** El agente propone una pregunta, da su respuesta recomendada,
espera. No acumula. No presupone.

**Potencial:** Si se confirma como patron recurrente, podria integrarse
en cualquier procedimiento de revision futura.

**Registro:** Primera observacion. Esperar a que aparezca en otro contexto
(por ejemplo, revision de arquitectura o diseno de experimentos).

---

## 2026-07-22 — Separacion procedimiento/skill como principio emergente

**Contexto:** Discusion sobre portabilidad del conocimiento entre agentes.

**Observacion:** Se identifico que la unidad real de conocimiento no es la
skill (atada a un agente concreto) sino el procedimiento (independiente del
runtime). Esto implica que LPA deberia gobernar procedimientos, no skills.

**Forma:** La skill es solo un adaptador. El procedimiento es el activo.
Hermes es un runtime temporal. Si Hermes desaparece, los procedimientos
deben sobrevivir.

**Potencial:** Esto tiene implicaciones en como se estructura el
conocimiento de LPA. Si se confirma, podria afectar a la definicion de
que pertenece a LPA core y que pertenece a la configuracion del agente.

**Registro:** Primera observacion. Esperar a que aparezca en una decision
de arquitectura real (no solo teorica).

---

## 2026-07-22 — Resistencia a crear documentos innecesarios

**Contexto:** Propuesta de documentar constitutional-review como procedimiento
LPA formal.

**Observacion:** Se rechazo la formalizacion por falta de evidencia suficiente.
Se propuso en su lugar un cuaderno de observaciones sin compromiso.
El patron detectado fue: "primero evidencia, luego formalizacion, luego
automatizacion" — tres estados que replican el sistema E0-E4 de LPA pero
aplicado a procedimientos en lugar de a principios.

**Forma:** Ante la tentacion de escribir un documento formal, se eligio
un archivo minimo sin estatus oficial. La pregunta "que evidencia tenemos?"
actuo como freno.

**Potencial:** Si este comportamiento se repite, podria indicar que el
sistema E0-E4 de LPA es generalizable a cualquier tipo de activo de
conocimiento (principios, procedimientos, instrumentos), no solo a
afirmaciones sobre el dominio.

**Registro:** Primera observacion. Esperar a que ocurra en otra decision
de documentacion.

---

---

## 2026-07-22 — Patron de deliberacion especializada

**Contexto:** Discusion sobre la arquitectura del criterio de diseno.
Se propuso un "Design Council" con 6 roles fijos (Critic, Historian,
Brand Guardian, Accessibility, UX, Judge).

**Observacion:** Emerge la intuicion de que decisiones complejas de diseno
mejoran cuando son deliberadas desde perspectivas especializadas antes de
sintetizarse. La propuesta concreta (6 roles) puede ser solo la primera
implementacion de algo mas general.

**Forma:** Ante una decision de diseno, separar el juicio en multiples
perspectivas independientes que deliberan por separado, y un rol separado
que sintetiza. Cada perspectiva tiene un ambito fijo de competencia.

**Potencial:** Si el patron se confirma en otros dominios (arquitectura
software, evaluacion juridica, investigacion), podria revelar un mecanismo
general de deliberacion para LPA que trasciende el diseno. El "Design Council"
seria simplemente un experimento para validar la hipotesis subyacente.

**Registro:** No escribir Design Council como procedimiento ni como skill.
Solo esta entrada. Para considerar formalizacion: que el patron aparezca en
al menos 2 dominios distintos (ej: diseno + arquitectura) y que la forma
concreta (roles fijos, orden de intervencion, sintesis) se repita
naturalmente sin necesidad de forzarla.

---

## 2026-07-22 — Meta-patron: resistencia a estructurar

**Contexto:** Toda la conversacion desde grill-me hasta Design Council,
pasando por skills, procedimientos e instrumentos.

**Observacion:** Cada vez que surge una idea nueva, la pregunta que se repite
no es "como se implementa" sino "tenemos suficiente evidencia para convertir
esto en estructura". Esto ha ocurrido con:
- el cuarto documento de Experience
- los codigos de governance
- Candidate Framework
- las skills de Hermes
- Design Council

**Forma:** El sistema (humano+agente) detecta automaticamente que una idea
novedosa no deberia formalizarse hasta que haya evidencia de que el problema
que resuelve es recurrente. No hay un procedimiento que ordene este
comportamiento — emerge naturalmente.

**Potencial:** Si este patron es real y no un artefacto de esta conversacion,
podria indicar que LPA ha interiorizado su propio principio de resistencia
a la formalizacion prematura. Eso no requiere documentarse como procedimiento
porque ya funciona sin el. Documentarlo ahora seria petrificar algo que
opera mejor como comportamiento emergente.

**Registro:** No documentar como procedimiento. Simplemente observar si
el patron se mantiene en sesiones futuras sin intervencion. Si dentro de
6 meses sigue apareciendo, sera evidencia de que LPA efectivamente se aplica
a si mismo de forma natural. Si desaparece, era un artefacto temporal.

---

## 2026-07-22 — Pipeline GLM → Gemma → Hermes como metodo de extraccion de principios

**Contexto:** Desarrollo de la landing page de Perfume IA a partir de una
imagen de referencia generada por ChatGPT. Tras 8 versiones que no conseguian
transmitir "espacio habitable", se implemento un pipeline de 3 modelos locales.

**Observacion:** Un unico modelo (GLM-4.6V-Flash) producia descripciones
literales de la imagen. Al encadenarlo con Gemma-4-12B (extraccion de
principios) y Qwen-3.5-9B (implementacion), el resultado mejoraba pero Qwen
no tenia contexto de Perfume IA y generaba codigo generico. La solucion fue
usar los principios extraidos por Gemma para que Hermes construyera la V8
manualmente.

**Forma:** El pipeline opera en 3 pasos: (1) GLM analiza la imagen como
arquitecto (planos, luz, materiales, recorrido visual), (2) Gemma extrae
principios universales sin elementos concretos, (3) Hermes implementa esos
principios en HTML/CSS respetando el contexto del proyecto.

**Potencial:** Este metodo permite usar cualquier imagen de referencia sin
copiarla, extrayendo su logica espacial en lugar de sus elementos visuales.
Aplicable a cualquier dominio donde se necesite aprender de referencias
visuales sin reproducirlas.

**Registro:** El pipeline funciono parcialmente. Gemma produjo 10 principios
solidos. Qwen fallo como implementador (alucino un ecommerce). Hermes
aplicando manualmente los principios fue la via efectiva. Probar en otro
dominio distinto a diseno web para validar si el patron se mantiene.

---

## 2026-07-22 — Limite del CSS puro para transmitir presencia

**Contexto:** Se construyeron 8 versiones de la landing (H1, H2, H3, V2, V3,
V4, V5, V6, V7, V8) iterando sobre fondo, composicion, paleta, capas y
principios espaciales. Todas fueron evaluadas con glm-4.6v-flash.

**Observacion:** Ninguna version CSS pura fue percibida como "un espacio
fisico habitable" por el modelo de vision. La V8 (construida con 10 principios
espaciales extraidos de la referencia) seguia siendo descrita como "pagina
web con diseno minimalista." La unica version que transmitio presencia fue
VIMG, que usaba la imagen real como fondo.

**Forma:** CSS puede simular gradientes, texturas, capas y luz direccional,
pero no puede crear la sensacion de "un lugar que existia antes de que
llegara el visitante." Para eso se necesita una imagen con textura, luz y
profundidad reales, o un medio distinto (WebGL, video, fotografia).

**Potencial:** Documentar este limite evita futuras iteraciones infinitas
sobre CSS. Cuando el objetivo sea "presencia" o "espacio habitable", la
respuesta no esta en refinar gradientes sino en usar imagenes reales o
cambiar de medio.

**Registro:** Evidencia solida (8 versiones + 3 evaluaciones de modelo de
vision). Si aparece un caso donde CSS SI transmite presencia, este patron
debe revisarse. Hasta entonces, considerar como conocimiento operativo.

---

## 2026-07-24 — External Knowledge Assimilation Pipeline (segunda instancia confirmada)

**Contexto:** Propuesta de Joseba para un pipeline YouTube→Hermes→ChatGPT→Hermes
para extraer y validar conocimiento externo. Probado hoy mismo con el vídeo
"Intensivo IA aplicada al sector creativo" de Founders (1h 05min, ~78 KB de
transcripcion).

**Observacion:** El pipeline funciono. Hermes extrajo 13 ideas clasificadas.
ChatGPT hizo una critica metodologica que identifico el sesgo principal:
"Hermes esta pensando demasiado en el contenido del video y no en que cambia
realmente Joko Lab." La critica fue quirurgica y mejoro sustancialmente la
seleccion final: de 13 ideas a 5, y de ahi a 0 (ninguna cambiaba una decision
real del laboratorio).

Pero el verdadero hallazgo es que **el pipeline en si mismo es el patron**,
no el contenido del video. El metodo funciona para extraer conocimiento de
cualquier fuente externa. Esto es la segunda instancia confirmada del patron
multi-modelo (entrada 7: GLM→Gemma→Hermes).

**Forma:** El patron abstracto es:

```
Recurso externo (video, libro, articulo, conferencia, podcast, paper, curso)
        ↓
    Hermes (extrae + clasifica)
        ↓
    Modelo externo (critica adversarial)
        ↓
    Hermes (decide con criterio de impacto real)
        ↓
    LPA (solo entra lo que cambia decisiones)
```

La fuente da igual. El metodo es el mismo.

**Potencial:** Esto ya no es un pipeline para YouTube. Es un mecanismo general
de asimilacion de conocimiento externo. Si aparece en un tercer dominio
distinto (ej: libro, paper academico), el patron asciende de E0 a E1.

**Registro:** M-001 documenta el procedimiento concreto. Este caso es la
primera ejecucion real y confirma que la Fase B (critica adversarial) es
el paso que mas valor aporta. La entrada 7 (GLM→Gemma→Hermes) y esta entrada
forman juntas la evidencia del patron multi-modelo.

**Leccion aprendida:** El sesgo natural de Hermes es extraer contenido del
recurso. Hace falta el revisor externo para forzar la pregunta "¿esto cambia
algo en Joko Lab?" Sin ese paso, el pipeline produce resúmenes, no conocimiento.

**Mejoras incorporadas a M-001 (v2):** La crítica real de ChatGPT identificó
5 mejoras estructurales: (1) shift mental de "qué ideas hay" a "qué cambia en
Joko Lab", (2) 5 preguntas obligatorias con orden fijo, (3) filtro de
transferibilidad, (4) Regla de Oro, (5) pregunta sobre aceleración de
resultados físicos. M-001 fue reescrito incorporando todas.

---

## 2026-08-07 — Activación del razonamiento antes de responder (el lab gobierna la validación, no la generación)

**Contexto:** Análisis de un texto externo (otro LLM) que proponía un "Panel
Dialéctico" (debate multi-persona con síntesis forzada) y, posteriormente, la
reformulación de H-HEL-001 como fallo de ACTIVACIÓN del proceso, no de
conocimiento. Contraste contra CP-004 (roles epistemológicos), CP-003 (KVC)
y la spec real de PIL.

**Observacion:** El lab gobierna la validación (KVC, MEL, PIL, Evidence
Contract) pero no la generación de la respuesta. Los fallos recientes no son
de conocimiento sino de ACTIVACIÓN: la respuesta se emite desde la primera
asociación disponible (memoria) sin activar el contraste. Todos los gates
posteriores habrían pasado: no había marcador, estado declarado ni revisión.
Los gates son REACTIVOS (se disparan con señal); si la activación no ocurre,
ningún gate existe. PIL mide disciplina procedimental y no puede detectar
"razoné antes de responder" (ni pretende hacerlo). La cadena causal está
documentada en research/reasoning-gate-diseno.md (06-ago): incidentes 0.19?,
0.20.1 y V003 — la propuesta RULE-PROC-001..005 ya diseñaba el clasificador de
tipo de pregunta y la Evidence Arbitration Layer. Casos con fuente:
analisis-hermes-quicksilver.md (0.19? — verificar versión, sin contrastar),
reasoning-gate-diseno.md 9.1 (A2A), VERIFIER (falso negativo sistemático). El
caso "Granite" no está localizado como incidente de activación (solo existe el
banco de evaluación history.jsonl): PENDIENTE DE VERIFICAR. [INFERENCIA sobre
el mecanismo del fallo, no hecho demostrado]

**Forma:** Ante una tarea, el flujo observado es Problema → Memoria →
Respuesta → (fin). El patrón propuesto: Problema → Activación deliberada
(según tipo de pregunta: factual → consultar fuente; estado → contrastar
memoria; estratégica → generar ≥2 alternativas; diseño → síntesis) → Respuesta
→ Validación. El selector previo (¿requiere activación?) ya está diseñado en
reasoning-gate-diseno.md (RULE-PROC-005 State Question Detector + Evidence
Arbitration Layer); falta decidir la vía EVF, no el diseño. Métricas de activación con distinción DECLARADA (auto-reporte)
vs VERIFICADA (evidencia de ejecución en el Operations Ledger): la declarada
sin verificar no es métrica (lección KVC-001; patrón SVP-A/SVP-B contra
Goodhart). La síntesis forzada solo aplica a diseño/decisión, no a hechos.

**Potencial:** Patrón de razonamiento (no componente, no capa): activación
deliberada del razonamiento antes de responder cuando la tarea requiere
contraste. Si H-HEL-001 se confirma experimentalmente en varios casos,
candidata a familia de patrones en thinking-patterns. No renombrar a
RAL/CAP: sigla nueva sin definición operativa nueva. No crear capa: choca con
FREEZE, JL-005 y la dirección proyecto→LPA. Esta E0 NO es un hallazgo nuevo:
formaliza como hipótesis falsable el diseño previo reasoning-gate-diseno.md
(06-ago).
Caracterización (07-ago): POLÍTICA de activación, no componente — la decide
RULE-PROC-005 y la ejecuta el mecanismo existente tools/activation_engine.py;
PIL verifica, MEL mide. Evidencia directa 07-ago: caso de la imagen LangGraph
(activación deliberada forzada → gap analysis específico en vez de respuesta
genérica de memoria). Decisión de Joseba (07-ago): vía C — instrumentar
MOR/MTE primero, sin componente nuevo. La sesión 2 (mission-contract-diseno.md
+ mission.schema.json, 07-ago) confirma la separación de planos: ejecución
(CAPA 2/3) vs cognición (CAPA 4); mismo principio de activación deliberada,
piezas distintas.

**Registro:** E0. No formalizar. Conexión directa con H-HEL-001
(HYPOTHESIS.md) y con la entrada de deliberación especializada del 2026-07-22.
Criterio para reconsiderar: si H-HEL-001 muestra reducción medible de errores
de primera respuesta con coste justificado por la distribución real (EXP vía
C), o si el patrón aparece en un tercer contexto.

---

## Notas

- Este archivo no tiene formato estricto. Cada entrada debe incluir:
  fecha, contexto, observacion, forma del comportamiento, potencial
  y criterio para reconsiderar.
- No cerrar entradas. Dejarlas abiertas hasta que el patron se confirme
  o se disuelva.
- Si un patron de este archivo aparece 2+ veces en contextos distintos,
  considerar moverlo a `pattern-incubator/` para maduracion estructurada.
  Usar `TEMPLATE.md` como guia.
- El incubator es el paso obligatorio antes de KNOWN.md. Ver `lpa/pattern-incubator/`.
- Revisar periodicamente. El 80% de las entradas probablemente habran
  desaparecido. El 20% restante seran candidatos a incubacion.
