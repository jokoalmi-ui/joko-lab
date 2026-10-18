# Análisis: aihero.dev (Matt Pocock) — inventario completo de skills y valor para el LAB
**VERACIDAD:** [VERIFICADO]

**Fecha:** 2026-09-03 | **Origen:** "de esta web he sacado la skill grill-me, analízala en profundidad por si las otras skills y más contenido son útiles"
**Método:** web_extract de aihero.dev + artículo "5 Agent Skills I Use Every Day" + repo github.com/mattpocock/skills (README, árbol git completo, SKILL.md crudos de las candidatas).
**VERACIDAD: [VERIFICADO]** — contenido de los SKILL.md reales del repo (raw.githubusercontent), no de memoria.

## 1. Qué es aihero.dev
Web de Matt Pocock (autor de Total TypeScript, muy conocido en TypeScript/agentes). Contenido: cursos/cohorts de pago, newsletter (~60k devs), artículos libres de proceso, y el repo público de skills `mattpocock/skills` (MIT, activo — último commit agosto 2026) usado por Claude Code/Codex/otros agentes. Filosofía declarada en el README: "skills pequeñas, fáciles de adaptar, componibles; funcionan con cualquier modelo; basadas en décadas de ingeniería". No es software a instalar en el lab: son prompts/metodología + artículos.

## 2. Inventario completo (34 skills, árbol verificado 03-sep-2026)
- **engineering (17):** ask-matt, code-review, codebase-design, diagnosing-bugs, domain-modeling, grill-with-docs, implement, improve-codebase-architecture, prototype, research, resolving-merge-conflicts, setup-matt-pocock-skills, tdd, to-spec, to-tickets, triage, wayfinder, wizard
- **productivity (7):** grill-me, grilling, handoff, teach, to-questionnaire, wait-what, writing-for-agents
- **misc (3):** git-guardrails-claude-code, migrate-to-shoehorn, scaffold-exercises, setup-pre-commit
- **in-progress (7):** claude-handoff, implement-spec, loop-me, retro, setup-ts-deep-modules, writing-beats, writing-fragments, writing-shape

## 3. Mapa conceptual del README (failure modes → fix)
1. "The Agent Didn't Do What I Want" → grill-me / grill-with-docs (alinear antes de construir)
2. "The Agent Is Way Too Verbose" → domain-modeling (lenguaje compartido / glosario de dominio)
3. "The Code Doesn't Work" → pasos pequeños deliberados (tdd)
4. "We Built A Ball Of Mud" → improve-codebase-architecture / codebase-design
Kit diario del autor (artículo 5-agent-skills): grill-me · to-spec · to-tickets · tdd · improve-codebase-architecture. Flujo actual declarado: domain-model → to-spec → to-tickets → tdd.

## 4. Contenido real de las candidatas (SKILL.md leídos)
- **grilling** (productivity): versión COMPLETA del grill-me — mapa como design tree, rondas de la "frontera" (todas las preguntas cuyos prerrequisitos están resueltos), formato por ronda: ❓Qn título+cuerpo+➡️ respuesta recomendada. grill-me es el resumen de 3 frases; grilling es la mecánica explícita.
- **to-spec**: sintetiza la conversación → spec con plantilla (Problem Statement desde la perspectiva del usuario, Solution, lista LARGA de user stories "As a... I want... so that...", y **seams**: esbozar dónde se va a testear ANTES de escribir, el seam más alto posible, idealmente uno solo). Publica en issue tracker con label.
- **to-tickets**: spec/plan → tickets "tracer-bullet" verticales que DECLARAN sus aristas de bloqueo (edges), con vocabulario del glosario de dominio.
- **domain-modeling**: disciplina activa de glosario de dominio (challenging terms, edge-case scenarios, escribir el glosario y decisiones al cristalizar) + estructura CONTEXT.md + ADRs.
- **wait-what**: micro-skill (3 líneas): cuando el agente no entiende al usuario, pedir re-pitch en ASD-STE100 (técnico simplificado) + lenguaje del dominio.
- **writing-for-agents**: referencia de escritura de docs para agentes — "context pointers" (el wording del puntero, no su objetivo, decide cuándo se alcanza el material), "one trigger per branch", y el marco de los DOS costes: **context load** (lo que siempre pesa en la ventana) vs **cognitive load** (lo que paga el humano). Enlaza SKILL-MECHANICS.md del repo.

## 5. Clasificación contra el mapa de capacidades del lab
### a) VALIDACIÓN externa (el lab YA lo tiene, a menudo más fuerte)
| Skill del repo | Equivalente en el lab |
|---|---|
| tdd | skill test-driven-development (superpowers) + verificación real con salidas |
| code-review | requesting-code-review + github-code-review |
| diagnosing-bugs | systematic-debugging (4 fases) |
| research | investigacion-web (flujo completo con research/ + backlog) |
| handoff | cross-session-awareness + patrones de handoff |
| teach | lpa-profesor |
| git-guardrails | **joko-git-recibos (MÁS fuerte: gate por hash de árbol, no por convención)** |
| codebase-design / improve-codebase-architecture | ai-architecture + auditoria-arquitectonica + refactor-seguro |
| grill-me (ya analizado 03-sep en analisis-grill-me-aihero-20260903.md) | grill-idea (skill del lab, fase 0) + RELEVANTE bajo demanda |
| setup-pre-commit / scaffold / migrate-shoehorn / setup-ts / wizard / triage / implement / prototype / merge-conflicts / ask-matt / to-questionnaire | No aplican (flujo de coding TS/Claude Code; el lab no es repo de producto) |

### b) Candidatas con SEÑAL real (no duplican; podrían enriquecer)
1. **writing-for-agents + SKILL-MECHANICS.md** — señal ALTA: el lab escribe/edita skills constantemente (164 skills, skill-compaction para coste de contexto). El marco "context load vs cognitive load" y "one trigger per branch" son validación + posible refinamiento de cómo el lab escribe descriptions/pointers. Comparar con hermes-agent-skill-authoring del lab.
2. **grilling (formato de rondas/frontera)** — señal MEDIA: complementa el research de grill-me (que recomendaba "sesión grill adaptada"); grilling da el formato EXACTO de rondas numeradas con recomendación. Podría absorberlo la skill grill-idea del lab cuando se use para decisión grande.
3. **to-spec (patrón SEAMS)** — señal MEDIA: "esbozar los seams de testeo ANTES de escribir el spec, el más alto posible, idealmente uno" — el lab hace PRD→TDD pero no formaliza los puntos de testeo en la fase de spec. Refinamiento posible del patrón PRD PROMPT 17-ago.
4. **to-tickets (tracer-bullet con aristas de bloqueo)** — señal MEDIA-BAJA: el lab usa kanban nativo + backlog; el patrón "cada ticket declara QUÉ lo bloquea" podría copiarse al planificar dependencias del graph de delegación.
5. **domain-modeling (glosario)** — señal BAJA-MEDIA: el lab es un proyecto personal; el "lenguaje compartido" importa menos que en un equipo. Sus DEC/RULE ya cumplen parte del papel. Referencia si el lab crece.

### c) La web como contenido
Artículos libres de proceso (grill-me viral, 5-agent-skills, mecánica de skills) = la mina. Cursos/cohorts = de pago, no aplican hoy. Newsletter: opcional si se quiere seguir las skills nuevas (señal débil — el repo ya se puede vigilar por RSS/git).

## 6. Veredicto
**La web es relevante por su REPO DE SKILLS y artículos de proceso; el lab ya tiene equivalente (a menudo más fuerte) de ~60% de las skills. Valor neto: 2 candidatas a estudiar más a fondo (writing-for-agents/SKILL-MECHANICS por la escritura de skills; grilling como formato de sesión grill para decisiones grandes) y 2 patrones copiables de bajo coste (seams en specs; aristas de bloqueo en tickets).** Nada a instalar como sistema. Coste 0 (prompts).

## 7. Fuentes
- https://www.aihero.dev/ + /skills + /5-agent-skills-i-use-every-day (web, 03-sep-2026)
- github.com/mattpocock/skills — README.md, árbol git (34 skills), SKILL.md crudos de: to-spec, to-tickets, domain-modeling, grilling, wait-what, writing-for-agents (verificados 03-sep-2026)
- research/analisis-grill-me-aihero-20260903.md (análisis previo de grill-me, esta web)

## 8. Cierre del futurible 1 — comparación writing-for-agents/SKILL-MECHANICS vs hermes-agent-skill-authoring (03-sep-2026)
SKILL-MECHANICS.md (2.6K chars) leído y comparado con la skill local del lab. VEREDICTO: la skill local ya cubre el 90% de la materia (context load = "la description paga cada turno", punteros, jerarquía, compactación por coste). Lo aportado y absorbido en la skill local (patch 03-sep, backup .bak-20260903-mechanics):
1. El marco explícito de los DOS costes: context load (lo siempre cargado) vs cognitive load (el humano como índice — no minimizarlo, es el precio de la agencia).
2. Regla de invocación (matiz Hermes): si una skill solo se usa manualmente → description de UNA línea sin ramas de trigger (no pagar descubrimiento ni auto-disparos). disable-model-invocation NO existe en Hermes; el equivalente es description mínima.
3. Router skills para familias de skills manuales numerosas (1 cosa a recordar en vez de N).
4. Referencia compartida entre skills manuales → archivo plano externo (patrón ya usado: research/, GUIA-JOKO-LAB.md).
No se implementa nada estructural nuevo en el lab: es refinamiento conceptual de la skill authoring.

## 9. Fuentes adicionales
- https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/writing-for-agents/SKILL-MECHANICS.md (leído 03-sep-2026)
