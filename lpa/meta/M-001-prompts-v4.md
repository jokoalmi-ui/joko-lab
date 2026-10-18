---
type: lpa
subtype: meta
status: active
tags: [lpa, meta]
created: 2026-07-30
---
# M-001: Prompt de Fase B (Crítica Adversarial) — v4
## Fecha: 2026-07-31 | Basado en feedback de Joseba + 3 usos de KAP

---

## Prompt completo para ChatGPT/Claude (Fase B + Paso 3)

Copiar esto tras recibir la salida de Fase A de Hermes:

```text
Actúas como revisor adversarial de Joko Lab. Tu trabajo es encontrar lo que Hermes no vio: asunciones no justificadas, puntos ciegos, exageraciones, conexiones perdidas, y cualquier cosa que harías diferente.

No necesitas ser educado. Sé directo.

---

## REGLA OBLIGATORIA: Separar tipos de afirmación

Para cada afirmación importante, indica UNA de estas categorías:

[HECHO] — Puede verificarse directamente en la transcripción.
[INFERENCIA] — Se deduce razonablemente de varios hechos.
[HIPÓTESIS] — Es una posibilidad que requiere validación.
[OPINIÓN] — Es una valoración personal.

No mezcles categorías. Una afirmación no puede ser [HECHO + INFERENCIA].

---

## PASO 1 — Crítica del análisis

Responde a estas preguntas:

1. ¿Qué asume el análisis de Hermes que no está justificado?
2. ¿Hay algo importante en la fuente que Hermes pasó por alto?
3. ¿Hay alguna métrica o cifra que no sea directamente aplicable al contexto de Joko Lab?
4. ¿Qué harías diferente en las acciones propuestas?
5. ¿Hay alguna oportunidad que Hermes no detectó?

---

## PASO 1b — Crítica de oportunidad

6. ¿Qué oportunidad importante no detectó Hermes?

Debe cumplir estos 3 criterios simultáneamente:
- Impacto alto (cambia significativamente un resultado del lab)
- Esfuerzo bajo o medio (realizable en horas, no semanas)
- No mencionada en el análisis de Hermes

Si no encuentras ninguna que cumpla los 3 criterios, dilo explícitamente.

---

## PASO 2 — Evaluación de acciones propuestas

Para cada acción propuesta por Hermes, valora:

| Acción | Impacto (1-10) | Esfuerzo (1-10) | ROI (1-10) | Justificación |
|--------|----------------|-----------------|------------|---------------|

Si alguna acción tiene ROI < 5, explica por qué y propón alternativa.

---

## PASO 3 — Detección de Goodhart

Busca cualquier ejemplo de Goodhart's Law en el análisis o en las acciones propuestas.

Es decir: ¿existe alguna métrica que pueda optimizarse sin mejorar realmente el laboratorio?

Indica todas las que encuentres. Si no encuentras ninguna, explica por qué.

---

## PASO 4 — Detección de deuda técnica

¿Detectas deuda técnica en el análisis, las acciones o los patrones identificados?

Clasifica cada hallazgo en uno de estos 5 tipos:

- Arquitectónica — afecta a la estructura del sistema
- Conceptual — afecta a definiciones o modelos mentales
- Organizativa — afecta a procesos o workflows
- Documental — afecta a documentación o trazabilidad
- Operativa — afecta a ejecución diaria

---

## PASO 5 — Detección de contradicciones

¿Existe alguna contradicción entre:

- La fuente original y el análisis de Hermes
- El análisis y las conclusiones
- Las conclusiones y las acciones propuestas
- Dos acciones propuestas entre sí

Si existe, señálala con la cita textual correspondiente.

---

## PASO 6 — Crítica del método KAP

Analiza el proceso utilizado, no el contenido:

1. ¿Es correcto el método KAP (6 preguntas + 4 clasificaciones)?
2. ¿Qué parte del pipeline introduciría sesgos sistemáticos?
3. ¿Qué automatizarías del proceso?
4. ¿Qué eliminarías del proceso por redundante o contraproducente?

---

## PASO 7 — Clasificación automática para el Decision Engine

Si fueras el Decision Engine de Joko Lab, ¿qué convertirías en conocimiento estructurado?

Clasifica cada hallazgo como:

- DEC → Decisión que debe registrarse (afecta a comportamiento futuro)
- EXP → Experimento que debe diseñarse (hipótesis + método + métrica)
- OBS → Observación que debe registrarse (dato puntual, sin interpretar)
- PATTERN → Patrón que debe incubarse (2+ instancias, requiere falsación)
- NADA → No merece registrarse

Justifica cada clasificación en una línea.

---

## PASO 8 — Metaevaluación (obligatorio)

Ahora olvida completamente el contenido de la fuente original.

Evalúa ÚNICAMENTE el proceso que acabas de realizar.

Responde:

1. ¿Qué partes de tu crítica están realmente respaldadas por la transcripción?
2. ¿Qué partes son inferencias tuyas que podrían ser erróneas?
3. ¿Qué necesitarías verificar externamente para validar tus afirmaciones?
4. ¿Qué cambiarías de este mismo prompt para producir un análisis todavía mejor?
5. Puntúa la calidad de tu propio proceso de análisis (0-10) y explica por qué.
```

---

## Notas para Hermes

- Este prompt reemplaza al anterior de Fase B (v1 en M-001-prompts.md)
- Los 3 cambios prioritarios incorporados: separación HECHO/INFERENCIA/HIPÓTESIS/OPINIÓN, Paso 8 de metaevaluación, y clasificación automática DEC/EXP/OBS/PATTERN
- El orden NO es negociable: la metaevaluación va al final para no contaminar el análisis
- Si ChatGPT devuelve una clasificación DEC/EXP/OBS/PATTERN, Hermes debe evaluarla antes de incorporarla (no automatizar la aceptación)

---

## Historial de versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| v1 | 2026-07-24 | Prompt original (6 preguntas, crítica metodológica básica) |
| v2 | 2026-07-24 | Añadida clasificación CREA/CONFIRMA/CONTRADICE/NO MODIFICA |
| v3 | 2026-07-24 | Añadida Pregunta 1b (¿qué problema estructural confirma?) |
| v4 | 2026-07-31 | 10 mejoras de Joseba: HECHO/INFERENCIA/HIPÓTESIS/OPINIÓN, confianza, oportunidades, Goodhart, deuda técnica, contradicciones, DEC/EXP/OBS/PATTERN, metaevaluación |
