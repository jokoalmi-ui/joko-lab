---
type: knowledge
subtype: observation
status: active
tags: [knowledge, observation]
created: 2026-07-29
---
# OBS-001: Router con dos fuentes de verdad
===============================================

## Datos basicos
  ID: OBS-001
  Fecha: 2026-07-29
  Origen: Autoevaluacion de Joko Lab
  Prioridad: ALTA

## Observacion

El decision_router.py consulta dos fuentes distintas para decidir
que modelo recomendar:

  1. Una tabla ROUTING_TABLE hardcodeada en el codigo (6 entradas)
  2. Consultas al RAG via decision_search()

Si manana se crea DEC-004, la tabla hardcodeada no la detecta.
Las dos fuentes pueden divergir silenciosamente.

## Contexto

Detectado durante la autoevaluacion del laboratorio (2026-07-29).
El pipeline completo (Context Builder → Knowledge Resolver →
Decision Router) revelo esta debilidad estructural.

## Siguiente paso

  → HYP-001: "Si las fuentes divergen, el router tomara decisiones inconsistentes"

## Estado

  Abierta. Pendiente de formular hipotesis.

## Conexiones

- [[HYP-001]] — HYP-001: fuentes duales causan decisiones inconsistentes
- [[RULE-002]] — RULE-002: política derivada del router
