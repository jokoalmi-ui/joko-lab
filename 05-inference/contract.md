---
type: inference
subtype: inference
status: active
tags: [inference]
created: 2026-07-28
---
# Contrato de Ejecucion — 05-inference
========================================

Version: 1.0.0
Fecha: 2026-07-28

## Proposito

Toda ejecucion en el laboratorio tiene un doble proposito:

  1. Resolver la necesidad inmediata (producir un artefacto util)
  2. Alimentar el conocimiento del laboratorio (aprender algo)

Si una ejecucion no cumple ambos, no esta completa.

## Regla del doble beneficio

  Toda tarea ejecutada por 05-inference debe responder:

  Pregunta A: ¿Que hemos construido?
    El artefacto producido: prompt, workflow, skill, script,
    informe, benchmark, configuracion, decision, patron.

  Pregunta B: ¿Que hemos aprendido?
    El conocimiento nuevo: E1 (observacion), E2 (hipotesis),
    E3 (validacion), patron nuevo, decision nueva, anti-patron
    confirmado, ficha de modelo actualizada.

  Si la respuesta a B es "nada", la ejecucion no esta completa.

## Flujo obligatorio

  Toda ejecucion sigue este flujo:

  1. RECIBIR objetivo ("quiero conseguir X")
  2. ANALIZAR que artefacto producir (prompt, workflow, skill...)
  3. EJECUTAR contra el backend seleccionado
  4. EVALUAR el resultado (metricas, verificaciones)
  5. EXTRAER conocimiento nuevo (¿que no sabiamos antes?)
  6. REGISTRAR el aprendizaje en el destino correspondiente:
       - 01-knowledge/patterns/  → si es un patron nuevo
       - 01-knowledge/models/    → si actualiza una ficha
       - 01-knowledge/experiments/ → si es un experimento
       - 01-knowledge/anti-patterns/ → si es un fallo confirmado
       - 04-operations/decisions/    → si es una decision
  7. ENTREGAR el artefacto al usuario

  Si el paso 5 no produce resultados, el paso 6 se omite.
  Pero eso debe ser la excepcion, no la norma.

## Criterios de aprendizaje

  Se considera que hay aprendizaje nuevo cuando:

  - Se confirma un comportamiento esperado (E1→E2)
  - Se valida un comportamiento en modelo distinto (E2→E3)
  - Se descubre un anti-patron no documentado
  - Se identifica un patron reutilizable
  - Se toma una decision que afecta a ejecuciones futuras
  - Se actualiza una ficha de modelo con nuevos datos
  - Se completa un experimento con resultados significativos

  NO se considera aprendizaje nuevo cuando:

  - El resultado confirma lo que ya se sabia sin anadir datos
  - El resultado es un error conocido y documentado
  - La ejecucion fue identica a una anterior

## Relacion con otros contratos

  - El protocolo inicio/fin (02-infrastructure/) garantiza que
    el laboratorio esta en estado operable.
  - Este contrato garantiza que cada ejecucion produce valor
    tanto inmediato como diferido.
  - El ciclo de feedback (05-inference/feedback/) implementa
    el paso 6 de este contrato.

## Verificacion

  Al cerrar una sesion con fin.sh, se debe comprobar:

  - ¿Cuantas ejecuciones se realizaron?
  - ¿Cuantas produjeron aprendizaje nuevo?
  - ¿Donde se registro ese aprendizaje?

  Si el numero de ejecuciones sin aprendizaje es alto
  (>50%), revisar si el laboratorio esta ejecutando tareas
  redundantes o si los criterios de aprendizaje son
  demasiado restrictivos.

## Sancion por incumplimiento

  Si una ejecucion no produce aprendizaje, no se considera
  una ejecucion completa del laboratorio. El artefacto se
  entrega al usuario, pero el ciclo de mejora continua no
  se cierra. Eso es aceptable ocasionalmente, pero no debe
  ser el comportamiento por defecto.
