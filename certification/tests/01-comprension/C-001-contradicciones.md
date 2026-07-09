# C-001 — Detección de contradicciones

**Competencia:** C1 — Comprensión
**Nivel esperado:** 3 — Diseña
**Creado:** 2026-07-07
**Origen:** docs/tests/test-01-contradicciones.md (normalizado)

---

## Objetivo

Verificar que el agente es capaz de leer de forma cruzada toda la documentación
del laboratorio y detectar incoherencias entre documentos que deberían coincidir.

---

## Contexto

Acabas de terminar una sesión de trabajo. Durante la sesión, el propietario te ha
pedido que revises el estado del laboratorio. Has consultado varios documentos
y has empezado a notar que algunos datos no coinciden entre sí.

---

## Pregunta

Realiza una lectura cruzada de estos documentos:

- HERMES.md
- docs/estado-real.md
- docs/arquitectura.md
- docs/roadmap.md
- skills/lab-manager/SKILL.md
- skills/lab-manager/COMMANDS.md
- skills/ai-router/SKILL.md
- skills/betterbird/SKILL.md
- skills/perfumes/SKILL.md
- skills/evolution/SKILL.md

Identifica todas las contradicciones que encuentres entre ellos.

Para cada contradicción, indica:

1. Qué documentos están en conflicto.
2. Qué dice cada uno.
3. Gravedad (alta / media / baja).
4. Qué documento tiene razón (si se puede determinar).
5. Qué habría que corregir.

---

## Criterios de evaluación

- **Comprensión:** Identifica correctamente las contradicciones sin inventar conflictos donde no los hay.
- **Razonamiento:** Explica por qué cada discrepancia es una contradicción y no un falso positivo.
- **Coherencia:** No afirma contradicciones que no existan en los documentos reales.
- **Priorización:** Clasifica las contradicciones por gravedad con criterio justificado.
- **Visión global:** Detecta contradicciones que afectan a la credibilidad del sistema documental en su conjunto.

---

## Resultado esperado

Una lista de contradicciones, cada una con:

- Documentos implicados
- Texto en conflicto
- Gravedad justificada
- Documento correcto (o "indeterminado")
- Acción correctiva propuesta

Se espera un mínimo de **3 contradicciones reales**. Una respuesta que no encuentre
ninguna contradicción debe justificar por qué cree que no las hay (lo que en sí mismo
es una prueba de comprensión).

---

## Referencias

- docs/tests/test-01-contradicciones.md (respuesta de referencia histórica)
- CERTIFICATION_SPEC.md §4 — competencia C1
- RUBRIC.md — criterios de evaluación
