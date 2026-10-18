---
type: knowledge
subtype: hypothesis
status: active
tags: [knowledge, hypothesis, multiagente, supervision, coste, latencia]
created: 2026-09-16
---
# HYP-004: La supervision multi-agente no compensa en tareas que el lab ya resuelve en sesion directa

**Origen:** fuente externa `research/analisis-cron-ig-20260916-lote-4.md` (post EP8 «Supervisor & Specialist» y «Single vs Multi-Agent» de @mentalhotfix, 15-sep-2026) cruzada con un dato interno suelto: el piloto `hermes kanban swarm` del 01-sep-2026 (6 cards, ~15 min, perfil cloud `default`, 16 fuentes verificadas) y la regla ya escrita en la skill `graph-lab` («lo simple NO necesita graph: sesion directa»).
**Fecha:** 2026-09-16
**Estado:** propuesta

## Observacion
El lab tiene dos formas de hacer una tarea con fuentes: **sesion directa** (un solo agente, la sesion) y **supervision multi-agente** (`hermes kanban swarm`: workers -> verifier -> synthesizer, o el procedimiento de `graph-lab` coordinador -> investigador -> redactor -> revisor). La regla de uso actual («lo simple = sesion directa») es un criterio CUALITATIVO, sin dato que la respalde: no existe ninguna comparacion medida entre los dos modos ni coste/latencia por tarea resuelta. La unica cifra disponible es de un unico piloto (kanban, ~15 min, 6 cards), sin contraste. La fuente externa añade el mecanismo concreto a vigilar: una supervision debil produce «ping-pong» entre agentes, trabajo duplicado, contexto creciente, latencia y coste.

## Hipotesis
En tareas que el lab ya resuelve en sesion directa (investigacion acotada con fuentes verificables), el modo con supervision multi-agente **no mejora la calidad verificada** y **sí aumenta** el coste (tokens x precio) y/o la latencia por tarea resuelta. La supervision solo compensa cuando el trabajo se puede aislar de verdad (contexto, herramientas, permisos, paralelismo o rol separado), no por complejidad aparente.

## Prediccion
Si la hipotesis es correcta, ejecutando la MISMA tarea (mismo objetivo y mismo criterio de exito) en los dos modos con el MISMO modelo:
  - modo A: sesion directa (cloud, perfil de la sesion)
  - modo B: supervision (`hermes kanban swarm`, perfil `default` cloud, y/o graph procedural en sesion)
se observara:
  - coste EUR por tarea y tokens totales (in/out) **mayores en B**
  - latencia de reloj por tarea **mayor o igual en B** (aunque los workers corran en paralelo)
  - **ninguna mejora** en la calidad verificada: nº de claims con URL verificada y errores detectados por el revisor, iguales o mejores en A
Medible con: latencia (min), tokens in/out, coste EUR (precios vigentes del lab), nº de traspasos/reintentos entre nodos, claims con URL verificada, errores detectados en revision.
**Umbral: NO se fija a priori (RULE-015).** Primero baseline: N=3 tareas repetidas en cada modo, rondas intercaladas (A,B,A,B...) para repartir la carga de la maquina (leccion de la bateria MTP: el thrashing falsea la medida). El umbral se fija despues de ver el baseline.

## Validacion
- [ ] Baseline de 3 tareas x 2 modos, rondas intercaladas, mismo modelo en ambos
- [ ] EXP-20260916-007 disenado (contrato: mismo objetivo, mismo criterio de exito, mismo modelo) -> `01-knowledge/experiments/EXP-20260916-007-supervision-vs-sesion-directa/diseno.md`
- [ ] EXP-20260916-007 ejecutado
- [ ] Resultado: [confirma | refuta | inconcluso]

## Limitaciones conocidas
- El modo B con modelos locales esta DESCARTADO hoy (decision F4 de `graph-lab`): la supervision fiable pasa por cloud, asi que la comparacion es cloud vs cloud.
- La latencia del swarm incluye tiempo de dispatcher (intervalo 60 s); no es solo tiempo de modelo.
- 3 tareas es un baseline, no una conclusion: si el coste difiere poco, el resultado sera «inconcluso», no «refuta».

## Decision derivada
- DEC-XXX (si confirma: la regla «lo simple = sesion directa» pasa de criterio a dato medido, y se documenta el dintel de cuando si compensa el swarm)
- Si refuta: la supervision se convierte en la via por defecto para este tipo de tarea y se revisa la regla del PRD.

## Conexiones
- [[HYP-002]] — el coste no esta unido a la decision (sin precio por tarea no se puede cerrar esta medicion)
- skill `graph-lab` — regla cualitativa que esta hipotesis quiere convertir en dato
- `research/analisis-cron-ig-20260916-lote-4.md` — origen externo (EP8 / single-vs-multi)
