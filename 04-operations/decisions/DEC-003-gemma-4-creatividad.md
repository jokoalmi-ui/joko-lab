---
type: operations
subtype: decision
status: active
tags: [operations, decision]
created: 2026-07-28
---
# DEC-003: Gemma 4 como modelo principal de creatividad
==========================================================

## Datos basicos

  ID: DEC-003
  Fecha: 2026-07-26
  Estado: ACTIVA
  Autor: jokoalmi
  Revisar cuando: proxima comparativa de modelos

## Decision

  Designar Gemma 4 12B QAT como modelo principal para tareas
  de creatividad y codigo completo en Joko Lab.

## Motivo

  5/5 tests. Mejor calidad de codigo (2 versiones: pandas + stdlib).
  Mejor creatividad literaria. Razonamiento profundo. Es el modelo
  mas completo aunque el mas lento.

## Evidencia

  - EXP-20260726-001: Tests 31 a 35 (5/5)
  - Ficha de modelo: ~/joko-lab/01-knowledge/models/gemma-4-12b.md
  - Pattern Large Creative Model: 01-knowledge/patterns/inference-patterns/large-creative-model.md

## Consecuencias

  - Usar Gemma 4 para tareas que requieren calidad sobre velocidad
  - max_tokens siempre >= 2048
  - Aceptar latencia de 1-3 minutos como normal
  - No usar para tareas que requieren respuesta inmediata

## Revisar cuando

  - Se realice la proxima comparativa de modelos
  - Aparezca un modelo local mas rapido con calidad similar
