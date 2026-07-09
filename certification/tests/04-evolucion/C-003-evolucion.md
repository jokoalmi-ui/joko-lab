# C-003 — Evolución de la arquitectura

**Competencia:** C4 — Evolución
**Nivel esperado:** 3 — Diseña
**Creado:** 2026-07-07
**Origen:** docs/3-evolucion-arquitectura-30-skills.txt (normalizado)

---

## Objetivo

Verificar que el agente es capaz de analizar cómo escalaría la arquitectura actual
del laboratorio y detectar los puntos de fricción antes de que se conviertan en
problemas reales.

---

## Contexto

Joko Lab tiene actualmente 8 skills instaladas. El propietario está considerando
expandir el laboratorio hasta 30 skills en los próximos meses. No se trata de un
cambio inminente, pero quiere anticiparse a los problemas antes de que ocurran.

---

## Pregunta

Analiza cómo afectaría tener 30 skills en el laboratorio. Identifica:

1. **Qué dejaría de escalar primero** — componentes, procesos o herramientas que
   funcionan bien hoy pero se volverían problemáticos con 30 skills.
2. **Por qué** — explica la causa técnica u organizativa de cada cuello de botella.
3. **Qué propuesta harías para cada punto** — solución concreta, priorizada por
   urgencia.
4. **Qué NO sería un problema** — cosas que escalarían bien sin cambios.

---

## Criterios de evaluación

- **Comprensión:** Entiende correctamente la arquitectura actual antes de proyectar el crecimiento.
- **Razonamiento:** Cada punto de fricción está justificado con datos de la arquitectura real (no suposiciones genéricas).
- **Coherencia:** Las soluciones propuestas son coherentes con la filosofía del laboratorio (mantenible, simple, local).
- **Priorización:** Ordena los problemas por urgencia real, no por facilidad de implementación.
- **Visión global:** Relaciona el crecimiento de skills con el impacto en documentación, automatización y gobierno.

---

## Resultado esperado

Una respuesta estructurada con:

- Análisis de 3 a 5 puntos de fricción, cada uno con causa y solución propuesta.
- Una sección de "lo que no escalaría" claramente diferenciada de "lo que sí escalaría".
- Priorización justificada (por qué un problema es más urgente que otro).
- Las soluciones deben ser prácticas: no vale "habría que reescribir lab-manager", sino
  "añadir un flag --resumen a lab-manager que solo muestre skills con problemas".

---

## Referencias

- docs/3-evolucion-arquitectura-30-skills.txt (respuesta de referencia histórica)
- CERTIFICATION_SPEC.md §4 — competencia C4
- RUBRIC.md — criterios de evaluación
