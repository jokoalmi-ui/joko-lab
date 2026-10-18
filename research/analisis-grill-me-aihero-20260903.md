# Análisis: /grill-me de Matt Pocock (aihero.dev) — ¿útil para el LAB?
**VERACIDAD:** [VERIFICADO]

Fecha: 2026-09-03 | Origen: petición directa del usuario ("analiza esta herramienta si es útil para LAB")
Método: extracción de la página aihero.dev/skills-grill-me + fuente primaria
(GitHub: repo mattpocock/skills vía API y SKILL.md crudo) + búsqueda de contexto.
**VERACIDAD: [VERIFICADO]** — contenido del skill verificado contra el SKILL.md real del repo.

## 1. Qué es (y qué NO es)

**grill-me NO es una herramienta ni un servicio: es un SKILL** (prompt estructurado,
3 frases de instrucción) creado por Matt Pocock (autor de Total TypeScript / AI Hero,
muy conocido en el mundo TypeScript y agentes de IA). Vive en su repo público
`github.com/mattpocock/skills` ("Skills for Real Engineers. Straight from my .agents directory").

Datos verificados del repo (GitHub API / badges):
- Estrellas: 244k ★ (cifra de la API shields.io, 03-sep-2026)
- Licencia: MIT (OSI, sin matices)
- Actividad: último commit agosto 2026 → proyecto vivo
- Contenido del SKILL.md real (raw.githubusercontent.com, verificado 03-sep-2026):

```markdown
---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching
shared understanding, resolving each branch of the decision tree. Use when user
wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared
understanding. Walk down each branch of the design tree, resolving dependencies
between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.
```

Instalación (para agentes de código): `npx skills@latest add mattpocock/skills --skill=grill-me`

## 2. Cómo funciona

- Toma una idea VAGA y entrevista al usuario hasta poder COMPROMETERSE con ella.
  La vaguedad no es motivo para esperar: es la materia prima de la sesión.
- Pregunta por RONDAS: cada ronda es "toda la frontera" (toda pregunta cuyos
  prerrequisitos ya se han resuelto) → nunca pregunta algo que dependa de una
  respuesta que aún no ha oído.
- UNA pregunta a la vez, cada una CON su respuesta recomendada. Si la respuesta
  se puede obtener explorando el código, explora en vez de preguntar.
- Stateless: no escribe archivos ni deja workspace. Solo deja la idea más nítida.
- Invocación explícita (`/grill-me`): el agente no lo usa por iniciativa propia.
  Sesión NUEVA, plan mode APAGADO (el plan mode empuja a producir un plan pronto,
  que es lo contrario de mantenerse en la indagación).
- Sesiones típicas: ~45 min, ~46 preguntas en 4 rondas ("contad rondas, no preguntas").
- Se acaba cuando la frontera está vacía: cada rama visitada, nada asumido en silencio.

Familia de la que forma parte (mismo autor):
| Skill | Estado | Uso |
|---|---|---|
| grill-me | stateless, sin repo | cualquier idea, también no-código |
| grill-with-docs | stateful: lee el codebase, guarda en CONTEXT.md + ADRs | alinear plan con un codebase |
| wayfinder | mapa de esfuerzo + sesiones grill dentro | esfuerzo demasiado grande para 1 sesión |

Actualización del PROPIO autor: "Dejé de usar /grill-me para coding. Ahora
recomiendo /grill-with-docs cuando quieres alinear un plan con tu codebase".
grill-me queda como pressure-test ligero de un plan. Su workflow actual:
domain-model → to-prd → to-issues → tdd (grill-me "pares bien con domain-model").

## 3. Fallos conocidos (los admite el propio autor)

1. **Pasividad** ("agreed, agreed, agreed" durante 40 preguntas): produces un plan
   que escribió el agente y tú asentiste. Resultado con certeza que no se ha ganado.
   El usuario debe EMPUJAR: rechazar preguntas por debajo de la fidelidad que necesita,
   decir "no sé" de verdad, frenar la deriva de scope.
2. **Preguntas "ungrillable"**: las que necesitan algo que reaccionar (una sensación,
   una UX) no se resuelven hablando → construir prototipo desechable y volver.
   Hablar de más en estas preguntas es donde las sesiones se disparan.
3. **Sesiones demasiado largas** → "dumb zone" (contexto lleno, preguntas peores).
   200 preguntas = scope demasiado grande → partir en piezas y grillar cada una.

## 4. Lo que el lab YA tenía (conexión, no duplicado)

"grill me" ya sonó en el lab 2 veces (verificado en research/):
- `research/analisis-opencode-orquestador-agentes-atareao.md` (líneas 87-119):
  identificado como patrón "preguntar antes de actuar" y registrado como FUTURIBLE:
  *"Skill 'grill me' del lab — skill que haga a Hermes preguntar (2-3 preguntas de
  enfoque) antes de lanzarse a una tarea grande. SEÑAL: cuando una tarea del lab
  requiera 'no lanzarse a ciegas'."*
- `research/prd-graph-delegacion-multiagente.md` (línea 189): el coordinador podría
  preguntar 2-3 preguntas antes de lanzar el graph → integrar en F3.

**Matiz importante**: el grill-me REAL es MÁS INTENSO que el futurible del lab
(2-3 preguntas de enfoque). El real es una entrevista hasta resolver el árbol de
decisión completo (~45 min, rondas). No es lo mismo: el futurible del lab es una
versión LIGERA; grill-me completo es una herramienta de definición PUNTUAL.

## 5. 🎯 Aplicación al lab

Qué valida:
- El lab ya formaliza "preguntar antes de actuar" (confirmación antes de acciones,
  "anota"=solo registrar, RULE-010 ceder control, patrón PRD PROMPT 17-ago, skill
  plan, revisar-decisiones, ciclo OBS→HYP→EXP→DEC). grill-me es validación externa
  del MISMO principio, aplicado al diseño (no a la ejecución).

Dónde encajaría (y dónde se notaría el beneficio):
- Sesiones de DEFINICIÓN antes de lanzar tareas grandes del lab: diseño del graph de
  delegación (F3), un PRD, un refactor, un experimento nuevo, una decisión de
  arquitectura. El beneficio se nota en menos bucles de rework: lo que se decide
  antes no hay que rediseñar después de gastar pipeline.
- También fuera de código (el autor lo usa para decisiones de negocio/escritura):
  encaja con decisiones de contenido o de producto del lab.
- Coste: CERO en pipeline — es un prompt stateless, sin archivos ni servicios.
  El coste real es TIEMPO ACTIVO del usuario (~45 min respondiendo con criterio).
  Por eso NO como hábito diario: choca con su preferencia de control>velocidad,
  una sesión por tema y esperas con fecha tope. Puntual y con time-box sí.

Qué matiza:
- El futurible abierto del lab ("2-3 preguntas") cubre el caso DIARIO; grill-me
  completo cubre el caso PUNTUAL de decisión grande. Son dos piezas, no una.

Qué NO es (anti-humo):
- NO es software a instalar ni servicio que levantar.
- NO automatiza nada ni escribe archivos (a diferencia de grill-with-docs).
- NO sustituye los gates de revisión del lab (revisar-decisiones, verificar_research).
- NO sirve para tareas ya especificables ("si ya puedes especificarla, no la necesitas").
- NO es delegable: exige respuestas activas del dueño de la idea (los subagentes
  con modelos locales no sirven aquí — regla de la skill investigacion-web).

## 6. Veredicto

**RELEVANTE (bajo demanda, no como instalación permanente).** Cierra/enriquece el
futurible que el lab ya tenía registrado. Recomendación concreta: NO instalar
grill-me como skill fijo de Hermes; cuando llegue una decisión grande (F3, PRD,
experimento), ofrecer una sesión grill-me adaptada: sesión nueva, rondas, una
pregunta a la vez con respuesta recomendada, time-box explícito (~30-45 min),
plan mode apagado. El patrón de 3 líneas cabe íntegro en una skill Hermes si algún
día se quiere (formato SKILL.md compatible).

## 7. Fuentes

- https://www.aihero.dev/skills-grill-me (página analizada, 03-sep-2026)
- https://github.com/mattpocock/skills (repo, API + raw SKILL.md verificado)
- https://aihero.dev/my-grill-me-skill-has-gone-viral (autor: sesiones ~45 min)
- https://aihero.dev/5-agent-skills-i-use-every-day (kit: grill-me · to-prd · to-issues · tdd · improve-codebase-architecture)
- research/analisis-opencode-orquestador-agentes-atareao.md + research/prd-graph-delegacion-multiagente.md (arte previo del lab)
