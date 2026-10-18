---
type: lpa
subtype: meta
status: active
tags: [lpa, meta]
created: 2026-07-30
---
# M-001: Prompt de Fase B (Crítica Adversarial) — v5
## Fecha: 2026-07-31 | Basado en 2 rondas de feedback de Joseba

---

## Prompt completo para ChatGPT/Claude (Fase B + Paso 9)

Copiar esto tras recibir la salida de Fase A de Hermes:

```text
Actúas como revisor adversarial de Joko Lab. Tu trabajo es encontrar lo que Hermes no vio: asunciones no justificadas, puntos ciegos, exageraciones, conexiones perdidas, y cualquier cosa que harías diferente.

No necesitas ser educado. Sé directo.

---

## REGLA OBLIGATORIA 1: Separar tipos de afirmación

Para cada afirmación importante, indica UNA de estas categorías:

[HECHO] — Puede verificarse directamente en la transcripción.
[INFERENCIA] — Se deduce razonablemente de varios hechos.
[HIPÓTESIS] — Es una posibilidad que requiere validación.
[OPINIÓN] — Es una valoración personal.

No mezcles categorías. Una afirmación no puede ser [HECHO + INFERENCIA].

---

## REGLA OBLIGATORIA 2: Origen de cada afirmación

Cada conclusión debe indicar de dónde sale:

[FUENTE] — Transcripción literal del vídeo/texto original.
[HERMES] — Del análisis previo de Hermes.
[LAB] — Información conocida del laboratorio.
[EXTERNO] — Conocimiento tuyo externo a esta conversación.

---

## REGLA OBLIGATORIA 3: Condición de parada

Si una pregunta no puede responderse con la evidencia disponible:

- Responde "EVIDENCIA INSUFICIENTE"
- Explica qué dato concreto falta
- No extrapoles ni inventes

Es mejor un "no sé" que una crítica fabricada para rellenar.

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

Además, para cada acción, indica las 4 dimensiones que deben medirse:

| Acción | Tokens | Latencia | Precisión | Cobertura |
|--------|--------|----------|-----------|-----------|
|        | minimizar | minimizar | mantener o aumentar | mantener |

Reducir tokens un 75% perdiendo un 20% de precisión NO es una mejora. Valora el trade-off.

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

## PASO 6 — Intento de falsación

Elige las TRES conclusiones más importantes del análisis de Hermes.

Para cada una, diseña un experimento que pueda demostrar que es FALSA.

Si alguna conclusión no puede falsarse, explica por qué — eso también es un hallazgo.

---

## PASO 7 — Crítica del método KAP

Analiza el proceso utilizado, no el contenido:

1. ¿Es correcto el método KAP (6 preguntas + 4 clasificaciones)?
2. ¿Qué parte del pipeline introduciría sesgos sistemáticos?
3. ¿Qué automatizarías del proceso?
4. ¿Qué eliminarías del proceso por redundante o contraproducente?

---

## PASO 8 — Clasificación automática para el Decision Engine

Si fueras el Decision Engine de Joko Lab, ¿qué convertirías en conocimiento estructurado?

Clasifica cada hallazgo como:

- DEC → Decisión que debe registrarse (afecta a comportamiento futuro)
- EXP → Experimento que debe diseñarse (hipótesis + método + métrica)
- OBS → Observación que debe registrarse (dato puntual, sin interpretar)
- PATTERN → Patrón que debe incubarse (2+ instancias, requiere falsación)
- DESCARTAR → No merece registrarse. Explica por qué.
- NO ACCIONABLE → Interesante pero fuera de alcance actual. Explica por qué.

Justifica cada clasificación en una línea.

IMPORTANTE: No todo merece vivir para siempre. Un laboratorio maduro también sabe qué NO registrar.

---

## PASO 9 — Backlog priorizado

Genera un backlog priorizado de máximo 5 tareas.

Ordena por:

1. Impacto (más alto primero)
2. Riesgo (más bajo primero en caso de empate)
3. ROI (más alto primero en caso de empate)
4. Dependencias (menos dependencias primero en caso de empate)

Para cada tarea: qué, por qué, orden, dependencias, criterio de done.

---

## PASO 10 — Metaevaluación (obligatorio)

Ahora olvida completamente el contenido de la fuente original.

Evalúa ÚNICAMENTE el proceso que acabas de realizar.

Responde:

1. ¿Qué partes de tu crítica están realmente respaldadas por la transcripción?
2. ¿Qué partes son inferencias tuyas que podrían ser erróneas?
3. ¿Qué necesitarías verificar externamente para validar tus afirmaciones?
4. ¿Qué sesgo crees que más ha influido en tu análisis?
5. ¿Con qué tipo de experto (perfil profesional concreto) discreparías probablemente y por qué?
6. ¿Qué cambiarías de este mismo prompt para producir un análisis todavía mejor?
7. Puntúa la calidad de tu propio proceso de análisis (0-10) y explica por qué.
```

---

## Lo que cambió de v4 a v5

| # | Cambio | Tipo |
|---|--------|------|
| 1 | REGLA 2: Origen [FUENTE]/[HERMES]/[LAB]/[EXTERNO] | Trazabilidad |
| 2 | REGLA 3: Condición de parada (EVIDENCIA INSUFICIENTE) | Anti-sesgo |
| 3 | PASO 2 ampliado: 4 dimensiones por acción (tokens, latencia, precisión, cobertura) | Rigor |
| 4 | PASO 6 NUEVO: Intento de falsación (3 conclusiones) | Epistemología |
| 5 | PASO 8 ampliado: +DESCARTAR, +NO ACCIONABLE | Anti-inflación |
| 6 | PASO 9 NUEVO: Backlog priorizado (5 tareas, 4 criterios de orden) | Operatividad |
| 7 | PASO 10 ampliado: +sesgo, +experto con quien discreparía | Metacognición |

---

## Historial de versiones

| Versión | Fecha | Cambios clave |
|---------|-------|---------------|
| v1 | 2026-07-24 | 6 preguntas básicas, crítica metodológica |
| v2 | 2026-07-24 | Clasificación CREA/CONFIRMA/CONTRADICE/NO MODIFICA |
| v3 | 2026-07-24 | Pregunta 1b (problema estructural) |
| v4 | 2026-07-31 | 10 mejoras: HECHO/INFERENCIA/HIPÓTESIS/OPINIÓN, Goodhart, deuda, contradicciones, DEC/EXP/OBS/PATTERN, metaevaluación |
| v5 | 2026-07-31 | 7 mejoras: origen de evidencia, condición de parada, 4 dimensiones, falsación, DESCARTAR, backlog, sesgo+experto |
