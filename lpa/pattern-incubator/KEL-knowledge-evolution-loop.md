---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-07-30
---
# Knowledge Evolution Loop (KEL)

**Tipo:** Observación arquitectónica — E0
**Fecha:** 2026-07-31
**Origen:** Síntesis de Joseba sobre KAP → v4 → v5 → CP-003

---

## Qué es

Un modelo del ciclo de vida completo del conocimiento en Joko Lab. No es un pipeline. No es un procedimiento. Es una **máquina de estados** por la que pasa cada pieza de conocimiento.

---

## Estados del conocimiento

```
OBS (E0)
  ↓  ¿Patrón en 2+ contextos?
HIPÓTESIS (E1-E2)
  ↓  ¿Experimento diseñado?
EXP (E3)
  ↓  ¿Evidencia suficiente?
EVIDENCIA
  ↓  ¿Cambia comportamiento futuro?
DEC
  ↓  ¿Aplicada?
MONITORIZACIÓN (4 dimensiones)
  ↓  ¿Mejoró realmente?
  Sí → Conservar, subir confianza
  No → Reabrir DEC, degradar confianza
  ↓
REVALIDACIÓN periódica
  ↓  ¿Sigue siendo válida?
  Sí → Mantener
  No → Retirar (Knowledge Pruning)
```

---

## Lo que lo diferencia de KAP y KVC

| | KAP | KVC | KEL |
|---|-----|-----|-----|
| Qué modela | Asimilación de fuentes externas | Validación de una decisión | Ciclo de vida completo del conocimiento |
| Input | Fuente externa (vídeo, paper) | Análisis + crítica | Cualquier pieza de conocimiento |
| Output | Clasificación CREA/CONFIRMA/CONTRADICE | DEC monitorizada | Conocimiento conservado o retirado |
| Memoria | No | Sí (monitorización) | Sí (revalidación periódica) |
| Olvido | No | No | Sí (Pruning) |

---

## Propiedad clave

KEL incorpora **olvido** como operación de primer orden.

Un sistema que solo acumula conocimiento se degrada. KEL introduce:
- Revalidación periódica de DEC antiguas
- Detección de conocimiento obsoleto
- Retirada de patrones refutados
- Fusión de decisiones redundantes

---

## Estado actual en Joko Lab

| Fase | Estado |
|------|--------|
| OBS → HIPÓTESIS | ✅ patterns-observed.md + pattern-incubator |
| HIPÓTESIS → EXP | ✅ Experimentos LPA (5 casos) |
| EXP → EVIDENCIA | ✅ Métricas + 4 dimensiones (v5) |
| EVIDENCIA → DEC | ✅ Decision Engine + DEC-001..003 |
| DEC → MONITORIZACIÓN | 🔄 CP-003 (v2) lo define, no implementado |
| MONITORIZACIÓN → REVALIDACIÓN | ❌ No existe |
| REVALIDACIÓN → RETIRAR | ❌ No existe (Knowledge Pruning pendiente) |

---

## El siguiente cuello de botella

Cuando el laboratorio tenga cientos de DEC, EXP, OBS, PATTERN acumulados, la pregunta no será:

> "¿Qué hemos aprendido?"

Será:

> **"¿Qué conocimiento ha quedado obsoleto?"**

Knowledge Pruning — el proceso de revalidar, degradar y retirar conocimiento — es el siguiente salto arquitectónico.
