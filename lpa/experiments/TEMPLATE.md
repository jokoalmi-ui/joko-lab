---
type: lpa
subtype: experiment
status: template
tags: [lpa, experiment]
created: 2026-07-19
---
# Experimento LPA — [NOMBRE]

## Metadata

| Campo | Valor |
|-------|-------|
| ID | EXP-XXX |
| Dominio | [nombre del dominio] |
| Categoría | [A/B/C/D/E/F/G — ver EPISTEMOLOGY.md] |
| Fecha inicio | YYYY-MM-DD |
| Fecha fin | YYYY-MM-DD |
| Estado | [Planificado / En curso / Completado / Abandonado] |

---

## Propósito de falsificación

**¿Qué afirmación(es) de KNOWN.md o HYPOTHESIS.md intenta falsear este experimento?**

- [ ] Afirmación 1: [ID y texto]
- [ ] Afirmación 2: [ID y texto]

**Pregunta de UNKNOWN.md que este experimento podría ayudar a responder:**

- [ ] PXXX: [texto]

---

## Descripción del dominio

### ¿Por qué es radicalmente distinto a los experimentos anteriores?

[Explicar qué categoría distinta aporta y qué supuesto de LPA pone a prueba.]

### ¿Qué hace que este dominio sea un buen candidato para romper LPA?

---

## Diseño del experimento

### Hipótesis nula (lo que asumimos que ocurrirá si LPA NO aplica)

> [Ej: "Los documentos core de LPA requerirán modificaciones estructurales para adaptarse a este dominio."]

### Qué construir

[Una pantalla, un prototipo, un documento, un diseño de servicio...]

### Método

1. Partir de los documentos core de LPA (EXPERIENCE_OS, LAWS, ANATOMY, PHYSIOLOGY) sin modificarlos.
2. Construir el artefacto sin crear nuevos documentos conceptuales.
3. Documentar cada decisión de diseño y su trazabilidad al core.
4. Medir IE (Índice de Emergencia) e IMD (Índice de Madurez Documental).
5. Registrar qué conceptos del core sobrevivieron sin cambios y cuáles requirieron adaptación.

---

## Resultados

### IE (Índice de Emergencia)

- Decisiones totales: ___
- Decisiones nuevas (sin trazabilidad al core): ___
- IE = ___ / ___ = ___%

### IMD (Índice de Madurez Documental)

- Decisiones trazables: ___
- Decisiones repetidas (misma referencia): ___
- IMD = (___ - ___) / ___ = ___%

---

## Supervivencia del core

| Documento core | ¿Sobrevivió sin cambios? | Cambios requeridos |
|---------------|------------------------|--------------------|
| EXPERIENCE_OS | [Sí / No] | |
| LAWS | [Sí / No] | |
| ANATOMY | [Sí / No] | |
| PHYSIOLOGY | [Sí / No] | |

---

## Afirmaciones afectadas

| Afirmación | Nivel antes | Nivel después | Justificación |
|-----------|------------|--------------|---------------|
| [ID] | [E0-E4] | [E0-E4 o E∅] | |

---

## Gaps detectados

Conceptos que el core no cubría y que emergieron durante la construcción:

| Gap | ¿Requiere nuevo concepto? | ¿Candidato a EMERGENT_CONCEPTS? |
|-----|--------------------------|-------------------------------|
| | | |

---

## Nuevas preguntas

Preguntas que este experimento generó y que no existían antes:

- PXXX: [texto]

---

## Conclusión

[¿El experimento falseó la afirmación objetivo? ¿La reforzó? ¿Fue inconcluso?]

---

## Artefactos producidos

- [ ] Prototipo: [ruta]
- [ ] Auditoría: [ruta]
- [ ] Métricas: [ruta]

---

FIN DE LA PLANTILLA
