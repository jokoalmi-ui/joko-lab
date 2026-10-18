---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-07-24
---
# CP-00X — Workflow como unidad de conocimiento

**Tipo:** Candidate Pattern
**Fecha:** 2026-07-24
**Estado:** Incubación (E0→E1)
**Origen:** Análisis del vídeo de Founders (KAP Fase A+B) + 4 evidencias previas

---

## Qué ocurrió

Durante el análisis del vídeo de Founders sobre IA aplicada al sector creativo, el ponente (Kque) mostró cómo construye workflows con nodos (Magnific Spaces) que luego empaqueta como productos (Flows) para clientes. La crítica ChatGPT identificó que el valor no estaba en la herramienta concreta sino en un principio subyacente.

Al revisar el historial de Joko Lab, el mismo patrón aparece en 4 contextos distintos:

1. **Pipeline GLM→Gemma→Hermes** (patterns-observed #7): extracción de principios desde imágenes de referencia. No se documentó "la imagen final", se documentó el proceso de 3 pasos.

2. **KAP — Knowledge Assimilation Pipeline** (M-001): YouTube → extracción → crítica adversarial → decisión. No se documentó "lo que aprendimos del vídeo", se documentó el método para aprender de cualquier vídeo.

3. **Desarrollo de Perfume IA**: iteraciones documentadas como Hipótesis → Versiones → Críticas → Resultado → Aprendizajes. No se guardó solo la landing final.

4. **Procedures → Skills** en LPA: un procedimiento documentado se adapta como skill cuando madura. La skill es conocimiento ejecutable, no solo documento.

---

## Evidencia que lo respalda

- **5 instancias en dominios distintos:**
  1. **Pipeline GLM→Gemma→Hermes** (patterns-observed #7): extracción de principios desde imágenes
  2. **KAP — Knowledge Assimilation Pipeline** (M-001): YouTube → extracción → crítica → decisión
  3. **Desarrollo de Perfume IA**: iteraciones como workflow documentado
  4. **Procedures → Skills** en LPA: conocimiento ejecutable, no solo documento
  5. **Founders Día 2 — We Make Studio** (evidencia externa, 2026-07-24): estudio profesional que trata sus workflows de Magnific Spaces como activos reutilizables, sin conocer LPA. Misma filosofía, distinto dominio, distinto equipo.
- El patrón aparece tanto en Joko Lab como en entornos profesionales externos → no es idiosincrático
- En todos los casos: no documentar outputs, documentar procesos que generan outputs

---

## Contradicciones o limitaciones

- LPA actualmente modela Observación → Patrón → Procedimiento → Skill, pero no tiene niveles para Workflow (autónomo) ni Producto (monetizable)
- Un Workflow es más que un Procedimiento: no necesita operador humano en cada paso
- Un Producto es más que un Workflow: tiene valor de intercambio

---

## Principio que parece emerger

> La unidad mínima de conocimiento en Joko Lab no debería ser el documento. Debería ser el workflow reutilizable.

Esto implica que LPA necesita dos niveles adicionales después de Skill:

```
Observación → Patrón → Procedimiento → Skill → Workflow → Producto
                                                ↑           ↑
                                         autónomo     monetizable
```

---

## En qué otros proyectos podría aplicarse

- **KAP:** Elevarlo de Fase 1 (prompt) a Workflow (ejecución autónoma con pasos encadenados)
- **Cualquier skill de Hermes:** Determinar si ya es un Workflow o solo un Procedimiento
- **Futuros labs:** Si Joko Lab escala, los workflows son la unidad de transferencia

---

## Condición de falsación

Este patrón sería falso si:

- Intentamos elevar KAP a Workflow y el resultado es peor que el procedimiento manual actual (más errores, más fricción, menos aprendizaje)
- O si descubrimos que el valor real está en la intervención humana entre pasos, no en la automatización

---

## Decisión

Pendiente de revisión. Primera iteración: intentar elevar KAP de Procedimiento a Workflow como experimento de validación.
