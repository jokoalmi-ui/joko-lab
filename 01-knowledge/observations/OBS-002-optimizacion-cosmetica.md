---
type: knowledge
subtype: observation
status: active
tags: [knowledge, observation]
created: 2026-07-29
---
# OBS-002: Mejora de prompt no se traduce en mejora real
==========================================================

## Datos basicos
  ID: OBS-002
  Fecha: 2026-07-29
  Origen: Autoevaluacion de Joko Lab
  Prioridad: CRITICA

## Observacion

El evaluator_optimizer.py mide la mejora del prompt usando la
rubrica (6 reglas sintacticas). Pero nunca verifica si la respuesta
del modelo destino mejoro realmente.

Un prompt puede pasar de 16% a 83% en la rubrica, pero producir
exactamente la misma respuesta que el original. La optimizacion
fue COSMETICA, no real.

## Contexto

La auditoria de 10 fases del Evaluator-Optimizer identifico este
fallo como "FALTA: prueba contra el modelo destino". Durante la
autoevaluacion del laboratorio (2026-07-29), se confirmo que
evaluate_response() existia como funcion pero no se usaba como
GATE para rechazar optimizaciones cosmeticas.

## Evidencia

  - Auditoria E-O: Fase 5 "Optimizaciones cosmeticas"
  - Evaluacion externa: "Nunca comprobais si realmente mejora la respuesta"

## Solucion implementada

  R1 (29 julio): evaluate_response() ahora actua como GATE.
  Si la respuesta es identica → rechazar optimizacion.
  Si empeora → rechazar.

## Estado

  Cerrada. Resuelta con R1.
