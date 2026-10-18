---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-07-30
---
# CP-003: Knowledge Validation Cycle (KVC)

**ID:** CP-003
**Fecha:** 2026-07-31 (v2: misma fecha, ampliado con monitorización)
**Estado:** E0 — Candidate Pattern
**Origen:** Observación de Joseba durante iteración KAP v4→v5

---

## Qué ocurrió

Durante la mejora iterativa del prompt de Fase B del KAP, Joseba observó que el laboratorio ya no solo ejecuta KAP. Está emergiendo un ciclo más amplio con una propiedad nueva: **el propio análisis se convierte en objeto de análisis.**

---

## El ciclo completo (v2)

```
Observación (E0)
      ↓
Análisis (Fase A KAP)
      ↓
Crítica adversarial (Fase B — modelo externo)
      ↓
Falsación (Paso 6 v5)
      ↓
DEC / EXP / OBS / PATTERN (Paso 8 v5)
      ↓
Aplicación (cambio real en el sistema)
      ↓
Monitorización (4 dimensiones: tokens, latencia, precisión, cobertura)
      ↓
¿Mejoró realmente?
      ↓
   Sí → Conservar DEC, subir confianza
   No → Reabrir DEC, registrar contraevidencia
```

---

## Principio que emerge

> La unidad de progreso no es el componente, es la decisión validada.

Corolario: **una decisión sin monitorización no es una decisión — es una apuesta.**

---

## Propiedades nuevas respecto a KAP

| KAP (M-001) | KVC (CP-003) |
|-------------|--------------|
| Pipeline lineal (3 fases) | Ciclo cerrado (con realimentación) |
| El análisis es el output | El análisis es objeto de análisis (metaevaluación) |
| Clasifica conocimiento | Además monitoriza si la decisión funcionó |
| No tiene memoria del resultado | Reabre DEC si la evidencia contradice |
| Extraer → Criticar → Asimilar | Extraer → Criticar → Falsar → Decidir → Aplicar → Monitorizar → Revalidar |

---

## Evidencia que lo respalda

1. **KAP v1 (2026-07-24):** 3 fases lineales. Extraer, criticar, asimilar.
2. **v4 (2026-07-31):** Se añade metaevaluación — el análisis analiza cómo analiza.
3. **v5 (2026-07-31):** Falsación, 4 dimensiones, backlog priorizado, condición de parada.
4. **Auditorías anteriores:** Evaluator aprobaba mejoras cosméticas (Goodhart). v5 cierra ese agujero con métricas multidimensionales.
5. **Patrón transversal:** Las mejoras más valiosas ya no son nuevos componentes sino mecanismos de validación.

---

## Filtro anti-DEC-inflación (REGLA)

Después de cada DEC, responder obligatoriamente:

> **¿Esta decisión cambia realmente el comportamiento futuro del sistema?**

Si la respuesta es NO → no es DEC, es OBS.
Si la respuesta es SÍ → DEC válida, registrar con condición de monitorización.

Esto evita que el repositorio de decisiones crezca con ruido.

---

## En qué otros proyectos podría aplicarse

- Perfume IA: ¿el post-filtro v3 es mejor que v2? → KVC
- Decision Engine: ¿una DEC sigue siendo válida? → KVC
- RAG: ¿reducir tokens degrada calidad? → KVC con 4 dimensiones
- Cualquier mejora: ¿es realmente una mejora? → KVC

---

## Condición de falsación

Este patrón sería FALSO si:

1. Las mejoras sin KVC resultan sistemáticamente mejores que las validadas con KVC.
2. KVC añade overhead sin mejorar la tasa de acierto de las decisiones.
3. En 3 iteraciones, las decisiones validadas no superan a las intuitivas en test ciego.
4. La fase de monitorización nunca detecta una DEC que deba reabrirse (KVC sería un trámite, no un filtro real).

---

## Relación con patrones existentes

| Patrón | Relación |
|--------|----------|
| CP-001 (colaboración multi-modelo) | KVC requiere modelo externo para crítica adversarial |
| CP-002 (pensar antes de codificar) | KVC = "validar antes de decidir, monitorizar después" |
| KAP (M-001) | KVC extiende KAP con falsación + monitorización + revalidación |
| Knowledge Pruning (futuro) | KVC alimenta Pruning: DECs que fallan monitorización → candidatas a retirada |
