---
type: operations
subtype: decision
status: active
tags: [operations, decision]
created: 2026-07-28
---
# DEC-002: DeepSeek R1 como modelo principal de razonamiento
==============================================================

## Datos basicos

  ID: DEC-002
  Fecha: 2026-07-26
  Estado: ACTIVA
  Autor: jokoalmi
  Revisar cuando: proxima comparativa de modelos

## Decision

  Designar DeepSeek R1 Distill Qwen 14B como modelo principal
  para tareas de razonamiento estructurado en Joko Lab.

## Motivo

  5/5 tests en la comparativa. Consistente en todas las tareas.
  JSON impecable, codigo con type hints, razonamiento paso a paso.
  Es el modelo mas equilibrado entre calidad y velocidad para
  tareas que requieren logica estructurada.

## Evidencia

  - EXP-20260726-001: Tests 21 a 25 (5/5)
  - Ficha de modelo: ~/joko-lab/01-knowledge/models/deepseek-r1-14b.md

## Consecuencias

  - Usar DeepSeek R1 por defecto para tareas de razonamiento
  - max_tokens siempre >= 2048
  - temperature entre 0.2 y 0.5

## Revisar cuando

  - Se realice la proxima comparativa de modelos
  - Aparezca un modelo local que supere sus metricas
