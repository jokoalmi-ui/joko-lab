---
title: "Análisis — \"OpenCode como orquestador de agentes\" (atareao.es, podcast T8)"
type: research
---

# Análisis — "OpenCode como orquestador de agentes" (atareao.es, podcast T8)

**Fuente:** https://atareao.es/podcast/opencode-como-orquestador-de-agentes/
(recibido vía enlace LinkedIn lnkd.in/egEyf88x → safety redirect)
**Autor:** atareao (blog/podcast Linux de referencia en español)
**Formato:** podcast 30:43 + artículo completo (Temporada 8, 17-ago-2026)
**VERACIDAD:** [VERIFICADO]

## Qué presenta (resumen)

Cómo pasar de usar OpenCode como asistente personal (un solo agente que hace
todo) a un **equipo de agentes especializados coordinados por un supervisor**,
aplicado a la redacción de artículos de blog (agnóstico al dominio: sirve para
presentaciones, investigación, etc.). Todo desde la terminal, con archivos
Markdown, sin infraestructura.

**Problema que resuelve**: la "degeneración del contexto" — cuando un solo
agente hace algo complejo de varios pasos, el resultado se degrada según
avanza la conversación (el modelo mezcla conceptos, olvida instrucciones del
inicio). Analogía del autor: un becario al que pides 5 cosas a la vez y hace
mal las 5; en una obra no pides al albañil que haga de fontanero.

## El método (patrón supervisor + pipeline de 5 fases)

**Esquema**: SUPERVISOR (coordinador, modelo grande, SOLO Task/delegación) →
investigador (solo leer, modelo pequeño) / redactor (escribe, modelo medio-alto)
/ SEO (solo metadatos, modelo pequeño) / revisor (solo leer, modelo pequeño) /
[publicador opcional].

**Fases**:
- F1 Planificación: el coordinador define estructura, secciones, tono,
  extensión. Incluye un skill llamado **"grill me"** que hace que el agente
  PREGUNTE al usuario antes de empezar (no se lanza a ciegas).
- F2 Investigación: agente bibliotecario. SOLO busca datos con fuentes
  verificadas (docs oficiales, GitHub, ejemplos). No escribe, no opina.
  Modelo pequeño, temperature 0.1, permisos: solo webfetch/lectura.
- F3 Redacción: agente periodista. Recibe datos del investigador y escribe en
  Markdown con el tono de la casa. Modelo medio-alto (Claude Sonnet / GPT-4o),
  temperature 0.7, permisos de edición. No sabe nada de SEO.
- F4 SEO: agente comercial. Optimiza SOLO metadatos (title buscable, meta
  description <160 chars, tags, keyword). No cambia el fondo. Modelo pequeño,
  temperature 0.2.
- F5 Revisión: agente editor. Examina todo y devuelve un INFORME (no edita):
  título con keyword, longitud de meta, tags, estructura, tono, formato.
  Modelo pequeño, temperature 0.1, permisos mínimos.

**Bucle de retroalimentación**: revisor → informe → si no OK, el coordinador
repite la fase fallida → vuelve a pasar por SEO y revisión hasta el visto
bueno. "Lo que diferencia un sistema multi-agente bien hecho de un pipeline
lineal".

**Configuración técnica (lo más valioso del artículo)**:
- Cada agente = archivo Markdown con frontmatter: `description` (puerta de
  entrada que ve el coordinador, con negativas y output esperado), `mode`
  (primary/subagent), `model`, `temperature`, `permission`.
- **Permisos granulares por allowlist**: coordinador con `task: {"*": "deny",
  investigador: allow, redactor: allow, ...}` + edit/bash/write deny → "no
  puede hacer NADA, solo delegar". Subagentes SIN permiso Task → no pueden
  invocar subagentes (evita el caos de delegación anidada).
- El prompt del coordinador lleva exclusiones en MAYÚSCULAS ("NO HAGAS EL
  TRABAJO TÚ MISMO. SOLO PLANIFICA, DELEGA Y SUPERVISA").

**Errores comunes** (lecciones):
1. El coordinador no delega (hace el trabajo él) → descripción explícita +
   permisos solo Task + exclusiones en mayúsculas.
2. Descripciones pobres en subagentes → el coordinador no sabe cuándo usarlos
   (descripción = qué hace, cuándo NO usarlo, qué output devuelve).
3. Permisos excesivos → solo el coordinador tiene Task.
4. Mito del coste multiplicado → FALSO: contexto aislado = menos tokens de
   entrada; modelos pequeños/baratos para tareas simples; solo coordinador y
   redactor usan modelos grandes. Puede ser MÁS barato que un solo agente.
5. Subagentes como caja negra → navegación entre sesiones + logging.

**Cuándo merece la pena**: contexto que se satura, problema descomponible,
especialidades distintas, pipeline con revisión. "Para cambiar una bombilla no
necesitas un equipo de cinco".

**Filosofía**: "la parte del becario la hace la IA, la parte de la mente la
pongo yo" — el humano guía y decide el enfoque; la IA ejecuta.

**Demo real**: artículo sobre `fd` (300 palabras, investigación ligera): el
coordinador preguntó con "grill me", trazó el plan, lanzó investigador →
redactor → SEO → revisor, OK a la primera iteración, "apenas unos minutos".

## Relevancia para el LAB (validación externa potente)

| Punto | Aplicación |
|---|---|
| **VALIDA el patrón del lab** | Hermes + delegate_task ES el patrón supervisor: subagentes con contexto aislado, modelos propios, ejecución en background. El lab ya implementa esto (leaf/orchestrator, max_concurrent_children=3) |
| **"Degeneración del contexto"** | Es exactamente el problema que el lab ya ataca: detector-perdida-contexto, skill-compaction, cross-session-awareness. Validación externa del diagnóstico |
| **VALIDA least-privilege-lab** | El artículo usa el mismo principio: coordinador solo Task, subagentes sin Task (allowlist con *: deny), permisos mínimos por agente. El lab lo tiene como política (least-privilege-lab) |
| **VALIDA el revisor/evaluator** | Revisor solo-lectura que devuelve informe → el lab tiene critic-layer, evaluator_optimizer, verificar_research, revisar-decisiones |
| **Skill "grill me"** | Preguntar antes de actuar = patrón que el usuario ya exige al lab (preguntar antes de gastar pipeline; "anota" = registrar; confirmación antes de acciones) — un skill así formalizaría el hábito |
| **Coste argumentado** | Contexto aislado + modelos pequeños = más barato que un solo agente: argumento útil para el diseño de delegación del lab (R1 llama31-8b dio informes pobres → elegir modelos por tarea, toolsets MÍNIMOS) |
| **OpenCode** | El lab tiene skill `opencode` (delegar coding a OpenCode CLI). El patrón supervisor aplica 1:1 si se usa OpenCode para tareas de redacción/investigación |

## Veredicto

**Validación externa del diseño multi-agente del lab, sin novedad técnica
nueva para el lab.** El lab ya implementa el patrón supervisor (delegate_task),
la delegación con contexto aislado, el mínimo privilegio y la capa de revisión.
Lo que aporta el artículo: (1) la configuración CONCRETA de permisos por
allowlist (task: {"*": deny, ...}), (2) el skill "grill me" como patrón de
preguntar antes de actuar, (3) el argumento de coste (aislamiento de contexto
= más barato, no más caro), (4) validación del revisor como agente solo-lectura.
Es didáctico y bien explicado, útil como material de referencia para explicar
el lab y para contenido LinkedIn (marca empleo).

## Futuribles (registrar)

1. **Skill "grill me" del lab** — skill que haga a Hermes preguntar (2-3
   preguntas de enfoque) antes de lanzarse a una tarea grande. Encaja con el
   hábito del usuario (confirmar antes de actuar) y con el patrón PRD PROMPT
   (17-ago). SEÑAL: cuando una tarea del lab requiera "no lanzarse a ciegas".
2. **Pipeline de redacción multi-agente para contenido LinkedIn Lab** —
   investigador → redactor → revisor con Hermes (subagentes) para los posts
   educativos de marca empleo. SEÑAL: cuando se active la producción regular
   de contenido LinkedIn.
3. **Referencia cruzada en la skill opencode**: patrón supervisor aplicable a
   OpenCode CLI (config de permisos task por allowlist) — actualizar la skill
   si se usa OpenCode con subagentes.

Archivo: `research/analisis-opencode-orquestador-agentes-atareao.md`
