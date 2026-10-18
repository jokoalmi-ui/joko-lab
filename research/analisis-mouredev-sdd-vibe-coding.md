---
title: "Análisis: MoureDev — \"El fin del Vibe Coding: crea software robusto\" (SDD)"
type: research
---

# Análisis: MoureDev — "El fin del Vibe Coding: crea software robusto" (SDD)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.youtube.com/live/5HaOxAAA5qI · Live de MoureDev (Brais Moure)
**Fecha:** 02-sep-2026 · Transcripción: 132 KB, 2h03min · Canal conocido (no es "ya visto": sin duplicado)
**Formato:** Masterclass/curso completo (no patrocinado; al final promociona MoureDev Pro y su comunidad — filtrar)

---

## Qué es (tesis)

Curso completo de **Spec Driven Development (SDD)**: desarrollar software con agentes de IA de forma profesional usando especificaciones. Título de clickbait ("El fin del Vibe Coding") — el contenido real es un curso paso a paso de SDD con un proyecto Python real (Habits CLI: registrar hábitos de estudio y calcular rachas).

**Mensaje central:** SDD no es nada nuevo — es el ciclo de vida clásico del software (planificar → analizar → diseñar → implementar → testear → desplegar) que llevamos 40-60 años haciendo, ahora con IA. No se inventa nada: se adapta.

**Por qué NO vibe coding** (crítica concreta):
- El código nunca es el correcto (no sabes qué hará la IA)
- Seguridad "terrible" y deuda técnica garantizada (funciona hoy, se rompe en un mes)
- No escala a equipos, empresas ni clientes
- **No aprendes**: si solo escribes prompts eres "una pieza del puzzle prescindible"

## Taxonomía SDD (3 niveles según compromiso con la spec)

1. **Spec First** — la spec arranca el desarrollo, la IA implementa y la spec "muere"; la fuente de verdad es el CÓDIGO (compromiso bajo)
2. **Spec Anchored** — la spec acompaña siempre al código, sincronizada; doble fuente de verdad (compromiso medio) ← **el recomendado**
3. **Spec as Source** — la spec ES el programa; si el código no resuelve, se reescribe la spec (compromiso máximo, código no se revisa)

Su recomendación: entre Spec First y Spec Anchored (donde el código importa y se revisa).

## El flujo que enseña (fases)

1. **AGENTS.md** — documento "Biblia pequeñita" del proyecto: descripción, estructura, comandos, estilos, reglas (no sobrecargar)
2. **Constitution** (docs/constitution.md) — principios INNEGOCIABLES, se escribe una vez
3. **Spec** — requisitos funcionales (RF 1..11), no funcionales, casos límite, fuera de alcance, criterios de finalización
4. **Clarificación** — prompt tipo QA: "revisa la spec como QA profesional, lista ambigüedades/contradicciones/casos límite/conflictos con Constitution, NO propongas soluciones todavía"
5. **Plan** — estructura de módulos, modelo de datos, algoritmo, decisiones técnicas, estrategia de test
6. **Tasks** — tareas de 20-30 min con dependencias, cada una referenciando el requisito funcional que cubre
7. **Implementación** — TDD: "escribe primero los test, luego el código, ejecuta, muestra resultado, marca la tarea, indícame qué RF cubre, párate" (UNA tarea por prompt)
8. **Validación** — "recorre la spec requisito por requisito, indica qué cubre el resultado, si algo falla dilo claramente, comprueba criterios de finalización y da un veredicto: spec cumplida"

**Human in the loop** en cada paso: revisar plan, spec, código y tests generados por IA ("la IA se puede equivocar, nos puede estar mintiendo... tu jefe no va a despedir a la IA, te va a despedir a ti").

## Nivel avanzado (rápido)

- **Skills por fase** (spec-generator: proceso + template + preguntas) — empaquetar cada fase como skill reutilizable
- **Subagente especialista en SDD** dentro del harness (con su propio contexto/prompt)
- **MCP a Jira** — leer historias de usuario y marcar completadas
- Insight clave: los frameworks (Kiro, Bimat, Spec Kit de GitHub, Open Spec, Specid) **son prompts y skills por debajo** — si no entiendes el flujo, usas frameworks "como una máquina de copiar y pegar sin saber lo que hace"

---

## Comparación con el LAB (lo que ya tenemos)

| Fase SDD (MoureDev) | El lab YA lo tiene |
|---|---|
| AGENTS.md (Biblia del proyecto) | AGENTS.md + RULE-008 + gates por repo |
| Constitution (principios innegociables) | RULES del lab + skills con reglas duras |
| Spec (requisitos, casos límite, fuera de alcance) | Plan mode (`skill plan`) + decisiones OBS→HYP→EXP→DEC |
| Clarificación (QA sobre la spec ANTES de código) | Gates fail-closed + verifier independiente (kanban) + revisor |
| Plan técnico | Arquitectura de skills + plan.md del modo plan |
| Tasks (20-30 min, trazables a RF) | Kanban nativo con workers (jerarquía validada 5/5) |
| Implementación con TDD | Skill TDD + test-driven-development |
| Validación (requisito por requisito, veredicto) | `verificar_research.py` (1/0) + verifier con gate PASS/FAIL + SVP |
| Skills por fase | **Biblioteca de ~60 skills** del lab |
| Subagente SDD | delegacion-subagentes + graph-lab |
| MCP a herramientas externas | MCP: lab-db, animation-server, lancedb... |

**Conclusión: VALOR MEDIO-ALTO como VALIDACIÓN.** El lab no está haciendo vibe coding: ya implementa SDD a su manera (documentación → decisiones → verificación → gates fail-closed → humano en el bucle). El curso confirma la dirección, no la descubre.

## Matices NUEVOS (los únicos que aportaría)

1. **Clarificación como fase explícita y separada**: prompt de QA sobre la spec que lista ambigüedades/contradicciones SIN proponer soluciones todavía (modo plan) — el lab lo hace distribuido en gates, no como fase con su propio prompt
2. **Tasks de 20-30 min con trazabilidad bidireccional** a requisitos funcionales individuales ("tarea 2 cubre RF 9 y 11") — el kanban del lab traza a nivel de card, no a nivel de requisito
3. **Constitution separada del AGENTS.md** — el lab tiene AGENTS.md y RULES, pero sin la distinción conceptual de "principios que se escriben una vez" vs "instrucciones operativas"
4. **Skills por fase del pipeline de desarrollo** (una skill que genera specs, otra que las clarifica...) — el lab tiene skills temáticas, no una cadena de skills por fase de un flujo

## Futurible (valoración honesta)

- NINGUNO de los matices requiere cambio: el lab YA cumple la tesis del vídeo (anti-vibe-coding, control, trazabilidad, validación)
- El matiz 1 (clarificación separada) podría afinarse como mejora del modo plan si se decide — bajo beneficio, ya cubierto por el revisor humano
- El proyecto del curso (Habits CLI) es un ejercicio de aprendizaje, no algo que aporte al lab

**Filtrar:** la parte final promociona Mouredev Pro (comunidad, mentorías, masterclasses) — no es contenido técnico.

---

## Ficha rápida

- **Tema:** curso SDD (Spec Driven Development) para desarrollo con agentes de IA
- **Público:** programadores (junior a senior) y gente que hace vibe coding sin fundamentos
- **Ejemplo práctico:** Habits CLI (Python, stdlib + pytest, TDD)
- **Repositorio:** material completo (templates, prompts, proyecto acabado) — referenciado en el vídeo
- **Ejercicio propuesto:** rehacer Habits CLI paso a paso sin copiar código
