---
type: candidate_pattern
id: CP-013
status: incubating
created: 2026-10-09
confidence: E0 (7 ocurrencias / 6 propósitos distintos, todas en una sola ventana)
domain: automatizacion-del-lab / host
---

# CP-013 · Un job programado dentro de la ventana de apagado del host no corre a su hora: corre todas juntas en el arranque siguiente

> **Estado:** Incubación (E0→E1)
> **Fecha:** 2026-10-09
> **Origen:** Ciclo semanal LPA, ventana 02→09-10-2026 (acta `incidentes/revision-fallos-2026-10-09.md`, decisión D2)
> **Nivel de confianza:** Medio-alto (7 ocurrencias, 6 propósitos distintos, medible en `jobs.json`; pero **una sola noche medida** y un solo host)

---

## 1. Qué ocurrió

El host del lab no está encendido de madrugada. La última ejecución del cron de un día es a las **22:12:30** y la primera del día siguiente a las **07:17:57** (medido 08→09-oct-2026 sobre `~/.hermes/cron/executions.db`): una ventana muerta de **9 h 05 min**.

Todos los jobs cuya hora programada cae dentro de esa ventana ven pasar su hora sin ejecutarse. Cuando el host vuelve, el planificador los despacha **todos a la vez** —con la etiqueta `catch_up` en `last_dispatch`— en una ráfaga de menos de un segundo. Para el operador que mira la hora de la última corrida, `last_run_at` o el `status` de un job, el efecto se lee como «retraso raro», «job lento» o «job roto», cuando en realidad es el calendario del host: **el job nunca tuvo la culpa**.

La etiqueta existe en el motor y dice la verdad: `last_dispatch.kind = catch_up` con `lateness_seconds ≈ 31.000` (8,7 h). El fallo no es del motor; es de diagnóstico: quien no lee `kind`/`lateness_seconds` interpreta el retraso como avería.

## 2. Evidencia que lo respalda

Medido en solo lectura (`~/.hermes/cron/executions.db`, `~/.hermes/cron/jobs.json`) el **09-10-2026**:

| job | hora programada | `kind` | `lateness_seconds` | despachado realmente |
|---|---|---|---|---|
| `40cd94440294` backup-joko-lab-diario | 22:15 | `catch_up` | 32.576,7 | 09-10 07:17:56 |
| `5119c2e881ad` backup-hermes-diario | 22:20 | `catch_up` | 32.276,7 | 09-10 07:17:56 |
| `9474f6f3d224` consolidador-sesiones | 22:30 | `catch_up` | 31.676,7 | 09-10 07:17:56 |
| `3d18a82cfd79` Bolsa autonoma — scan EXP-002 | 22:30 | `catch_up` | 31.676,7 | 09-10 07:17:56 |
| `41a1a42060f4` registrar-hel-diario (EXP-HEL-001) | 22:35 | `catch_up` | 31.376,7 | 09-10 07:17:56 |
| `2371b6491039` hel-registro-watchdog | 22:45 | `catch_up` | 30.776,7 | 09-10 07:17:56 |
| `8bf412ac2ba3` ficha-perfume-diaria | 07:05 | `late` | 776,7 | 09-10 07:17:56 |

**7 jobs / 6 propósitos distintos** (backs del lab, backup de Hermes, consolidación de sesiones, experimento de bolsa, registro emocional, watchdog, ficha diaria). Los seis primeros tienen lateness de **~8,5-9,0 h** (el apagado); el séptimo, de 13 min, porque el arranque (07:17:56) llegó **después** de su hora (07:05).

Bordes medidos de la ventana:
- Última ejecución del día anterior: **08-10 22:12:30**; primera del día siguiente: **09-10 07:17:57**.
- `uptime -s` = **2026-10-08 08:08:21** → el host **no se reinició**: la ventana es **suspensión/apagado del host** (o parada del planificador), no un arranque nuevo de máquina.
- En la ventana no hay **ninguna** fila en `executions` (ni `completed` ni otra): no es que los jobs fallaran, es que no se despacharon.
- El `lateness_seconds` grande ya se había visto antes y se atribuyó a otra causa: el acta 02-10 (F7) midió lateness de **1.193,7 s y 4.793,7 s** con `uptime -s` = 02-10 09:56 y lo leyó como «la guarda de 300 s convirtió una ventana perdida en fallo del script». Aquí están las dos caras de lo mismo, ya con la hora del apagado acotada al minuto.

## 3. Contradicciones o limitaciones

- **Una sola noche medida a nivel de minuto.** La tabla es del 09-10; que la ventana 22:12→07:17 sea *estable* cada noche no está medido todavía (hace falta comparar ≥3 días).
- **No se distingue suspensión de parada del planificador.** `uptime -s` descarta un reinicio del host, pero no separa «el PC estaba suspendido» de «el PC estaba encendido y el planificador parado». Ambas producen el mismo `catch_up`. (Memoria del lab: el wifi se apaga 00:00-07:00 y hay un bug conocido de suspensión con NVIDIA.)
- **Job `no_agent` vs job de agente.** Los 7 casos son de propósito distinto, pero no está medido si un job de agente (LLM, minutos de duración) sufre además algo distinto al correr dentro de la ráfaga de arranque: 2 de estos despachos acabaron en `unknown` ese mismo minuto (el consolidador y la ficha diaria), lo que sugiere que **la ráfaga de arranque tiene coste propio** (ver CP-012). No se ha aislado.
- **No es lo mismo «no corre a su hora» que «no corre»**: en los 7 casos el job **sí** corre, con ~8,7 h de retraso. El patrón describe el desplazamiento de la hora, no necesariamente la pérdida del producto (el consolidador lleva 8 noches sin producto, pero eso es F1 de la acta y puede tener causa adicional).
- **Un host encendido 24/7 haría desaparecer el patrón** sin que ningún mecanismo del lab cambie: el antídoto puede ser de calendario, no de software.

## 4. Principio que parece emerger

> Un job programado dentro de la ventana en que su host no está encendido no se ejecuta a su hora: se ejecuta **todas las veces juntas** en la primera comprobación posterior, y el motor lo marca honestamente (`catch_up` + `lateness_seconds`). Por tanto: **antes de diagnosticar un job por su hora de ejecución o por su `status`, se lee `last_dispatch.kind` y `lateness_seconds`** — un despacho `catch_up` explica el retraso sin que el job esté roto. Y al diseñar la rejilla de horas: cualquier job cuya hora exacta importe (o que deba producir un producto diario) no se programa dentro de la ventana de apagado del host.

Corolario operativo medido: el arranque del host concentra N jobs vencidos en **una ráfaga sub-segundo**; esa ráfaga es un contexto de ejecución distinto (recursos, arranques simultáneos del planificador) y merece su propia comprobación de producto.

## 5. ¿En qué otros proyectos podría aplicarse?

- Cualquier laboratorio doméstico o servidor que no esté 24/7 (portátiles, PCs de trabajo, mini-PCs con horario).
- Rejillas de cron de producción en hosts con ventanas de mantenimiento: el mismo `catch_up` existe en `anacron`, `systemd timers` (`Persistent=true`), Airflow, Jenkins.
- Pipelines con SLA por hora: confundir un `catch_up` con un fallo de cómputo dispara diagnósticos falsos y «arreglos» innecesarios.
- Cualquier sistema donde un job deba producir un producto diario y el operador mire la hora de la última corrida como prueba de salud.

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

Sería **FALSO** si, sobre **N=10 jobs con hora fija dentro de la ventana de apagado** y durante **2 ciclos semanales consecutivos**, **8 o más** se despachan dentro de **±5 min** de su hora programada (`last_dispatch.kind = on_time`), es decir, si el host permanece encendido en esas horas o el planificador recupera el calendario sin desplazarlo. También lo falsaría que el desplazamiento no tuviera efecto observable: si los jobs despachados por `catch_up` producen su producto diario con la misma fiabilidad que los despachados `on_time`, el patrón sería una nota de calendario sin consecuencia.

## 7. Decisión

- [ ] Asciende a KNOWN.md como E1 (falta: la ventana medida en ≥3 noches y un segundo host/entorno)
- [ ] Asciende a procedures/ como procedimiento LPA (el antídoto «leer `kind`/`lateness_seconds` primero» **ya se está aplicando** en el ciclo desde el 02-10 vía LEC-015, pero sin documento propio)
- [x] Sigue en incubación
- [ ] Se descarta
- [ ] Se fusiona con otro patrón (candidato declarado: **CP-012**, por la ráfaga de arranque como contexto de ejecución propia; y **CP-010**, por el instrumento «hora de última corrida» leído como salud cuando no lo es; hoy tienen antídotos distintos: comprobar el artefacto / validar la cifra)

**Fecha de revisión:** 2026-10-23 (semanal — **revisado el 2026-10-16: sobrevive, 2ª noche medida**) y 2026-11-02 (mensual) — o inmediata si aparece un segundo host/entorno.
**Justificación:** 7 ocurrencias en 6 propósitos distintos superan el umbral de 2, y la ventana está acotada al minuto, pero **todo procede de una sola noche y un solo host**, y el mecanismo (suspensión vs planificador parado) no está aislado: es evidencia fuerte de frecuencia, todavía débil de generalidad.

**Reexamen 2026-10-16 (2ª noche medida, sin cambio de nivel).** Ventana 09→16-10; acta `incidentes/revision-fallos-2026-10-16.md`.
- **Ventana muerta medida al minuto:** última ejecución antes del apagado `2026-10-15T23:50:07.180312+02:00` → primera del día siguiente `2026-10-16T06:08:56.397293+02:00` = **6 h 18 min 49 s**. `uptime -s` = `2026-10-16 06:07:39` → fue **reinicio del host** (77 s antes de la primera corrida), no suspensión: el efecto sobre el planificador es el mismo, el mecanismo **no** (el del 09-10 fueron 3 reinicios intradía).
- **Ráfaga de arranque: 10 jobs en 340 ms, todos `status: completed`.** Ningún `unknown` esta vez (el 09-10 hubo 2). Sin falsación de §6: el host no permanece encendido en esas horas ni el planificador recupera el calendario sin desplazar.
- **Hallazgo nuevo — la composición de la ráfaga depende de la hora del apagado:** el 15-10 el host cayó a las 23:50, **después** de los jobs diarios de 22:15-22:35 (backups, consolidador), que sí corrieron dentro del día (113 filas en `executions` entre el 15-10 22:00 y 23:59) → la ráfaga del 16-10 contiene **solo jobs de intervalo**. La consecuencia operativa es que «cuántos jobs se desplazan» no es propiedad del patrón, sino de **dónde caiga el apagado** respecto al calendario diario.
- **Borde nuevo (limitación del instrumento, no falsación):** la evidencia directa de este patrón —`last_dispatch.kind != 'on_time'` / `lateness_seconds > 600` en `jobs.json`— es **efímera**: medida hoy a las 14:38, 8 h después del arranque, devuelve **0 filas** en ambos filtros, porque el campo se sobrescribe en el siguiente despacho y los 10 jobs de la ráfaga son de intervalo (ya habían vuelto al calendario). `last_dispatch` sirve para diagnosticar **dentro** de la ventana del job; el histórico de la ventana muerta hay que reconstruirlo con `executions` por hora + `uptime -s` (lo que este ciclo hizo). No invalida el patrón: **invalida una de las dos formas de medirlo**.
