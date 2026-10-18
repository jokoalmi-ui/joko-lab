---
type: operations
subtype: decision
status: active
tags: [operations, decision]
created: 2026-07-28
---
# DEC-001: No usar Qwen 3.5 9B
===================================

## Datos basicos

  ID: DEC-001
  Fecha: 2026-07-26
  Estado: ACTIVA
  Autor: jokoalmi
  Revisar cuando: exista una nueva version de Qwen 3.5

## Decision

  No utilizar Qwen 3.5 9B para ninguna tarea en Joko Lab.

## Motivo

  0/5 tests utiles en la comparativa de 7 modelos.
  Content vacio en 3 de 5 tests. finish=length en los 2 restantes.
  No se encontro ninguna configuracion (max_tokens, temperatura,
  top_p) que produjera resultados aceptables.

## Evidencia

  - EXP-20260726-001: Tests 11 a 15
  - Ficha de modelo: ~/joko-lab/01-knowledge/models/qwen-3.5-9b.md
  - Anti-patron: FATAL - Usar Qwen 3.5 9B para cualquier tarea

## Consecuencias

  - No se invierte tiempo en调试configuracion de Qwen 3.5
  - Si aparece una version nueva, se re-evaluara
  - Mientras tanto, usar Qwen3 14B como alternativa minima

## Revisar cuando

  - LM Studio reciba una actualizacion de Qwen 3.5
  - Aparezca Qwen 3.6 o superior
  - Se disponga de un modelo de mayor tamaño de la serie Qwen

## Notas

  Este modelo se descarto despues de 35 experimentos comparativos
  con 7 modelos. No es una decision apresurada. Si se revisa y
  la nueva version sigue fallando, actualizar esta decision en
  lugar de crear una nueva.
