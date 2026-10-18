---
type: candidate_pattern
id: CP-012
status: incubating
created: 2026-10-02
confidence: E0 (2+ ocurrencias en contextos distintos)
domain: procesos-del-lab / automatizacion
---

# CP-012 · El estado `unknown` del motor no se resuelve en el motor: se resuelve en el artefacto

> Promovido el **2026-10-02** desde el ciclo semanal LPA (acta `incidentes/revision-fallos-2026-10-02.md`, decisión D12). 5 ocurrencias en 5 jobs distintos en una sola jornada.

## 1. Patrón candidato

Cuando un motor de ejecución admite que **no sabe** si una tarea corrió (`unknown`, tras un reinicio que interrumpe al worker), ese estado **no se puede resolver consultando el motor**: la única resolución disponible está en el **artefacto** (el fichero, la fila, el mensaje, el log con el efecto esperado). El estado `unknown` es honesto, pero es **terminal para el motor y no para el operador**: mientras el operador no vaya al artefacto, la incertidumbre se hereda de ciclo en ciclo.

Formulación operativa: **ante un `unknown`, la pregunta no es «¿qué dice el motor?» sino «¿existe el producto?»**.

## 2. Contextos / dominio(s)

Automatización del lab (Hermes cron / `restart-safe worker`). 5 jobs de propósito distinto en la misma jornada:

1. Recordatorio `once` (aviso puntual al usuario).
2. Vigilancia de canales (scraping programado diario).
3. Entrenador emocional diario (job de contenido personal).
4. Scan diario de un experimento (bolsa, EXP-002).
5. Consolidador de sesiones (job de datos del lab).

## 3. Evidencia (ocurrencias)

Medido en solo lectura sobre `~/.hermes/cron/executions.db`, ventana 01-10-2026 (3 reinicios del planificador: 09:00, 13:30, 22:00+):

| job | hora de reclamo | estado | producto esperado | ¿existe? |
|---|---|---|---|---|
| `d824bcf4a2ff` Recordatorio publicar L5 (1-oct) | 01-10 09:00:29 | `unknown` | mensaje de aviso | **no comprobable** (job `once`, sin efecto en disco) |
| `4d64ff821685` vigilar-canales-ig | 01-10 13:30:51 | `unknown` | registro de vigilancia | no aparece en la salida |
| `1d06754e7c9a` Entrenador emocional diario | 01-10 22:00:16 | `unknown` | artefacto del entrenador | no aparece en la salida |
| `9474f6f3d224` consolidador-sesiones | 01-10 22:30:15 | `unknown` | `sesiones-20261001.jsonl` | **NO existe** (confirmado) |
| `3d18a82cfd79` Bolsa autonoma scan EXP-002 | 01-10 22:30:16 | `unknown` | producto de scan | **no hay** (barrido 01-10 21:00 → 02-10 00:30: solo telemetría/OBS/lancedb de las 22:00) |

Literal del motor (cita textual del campo `error`): *«Scheduler restarted after this execution's owner exited before a durable terminal state; whether side effects ran is unknown.»* y *«Restart-safe cron worker exited with status -15 after adopting this execution, without writing a durable terminal state; whether side effects ran is unknown.»*

**Contraejemplo útil (define el borde del patrón):** el barrido de artefactos del 02-10 09:19-09:25 clasificó los 3 timeouts como `failed` **con causa explícita** (`Script timed out after 300s`) → aquí el motor **sí** dice algo fiable y el artefacto no hace falta para saber qué pasó (sí para saber por qué: el despacho llegó 20-80 min tarde). El patrón aplica a `unknown`, no a `failed`.

**Observación de honestidad del motor:** el motor no se declara `ok` cuando no lo sabe; el fallo de esta ventana es **del ciclo**, que no leía este registro (el `.md` declarado llevaba 31 días muerto) y por tanto ni veía la incertidumbre.

**Ampliación 2026-10-09 (ciclo semanal siguiente, ventana 02→09-10). El antídoto se aplicó y resuelve en las DOS direcciones.** Dos `unknown` nuevos, en la misma ráfaga de arranque (09-10 07:17:57,62 y 07:17:58,35) y en jobs de propósito distinto:

| job | estado | artefacto esperado | ¿existe? | veredicto |
|---|---|---|---|---|
| `9474f6f3d224` consolidador-sesiones | `unknown` 09-10 07:17:57,62 | `sesiones-20261008.jsonl` + `resumen-dia-2026-10-08` | **NO existen** (último `sesiones-20260930.jsonl`, 824 MB; `resumen-dia` hasta 29-09) | efectos **NO** |
| `8bf412ac2ba3` ficha-perfume-diaria | `unknown` 09-10 07:17:58,35 (`finished_at` 07:33:33) | `research/infografias/perfume-del-dia-20261009/` | **SÍ**, completo (15 ficheros, 07:23→07:52; PNG final 1.808.675 B) | efectos **SÍ** |

- **No se dispara la segunda falsación (§5):** en ninguno de los dos casos el artefacto engañó al antídoto — en uno el producto existe y está completo, en el otro falta. Ambas direcciones del veredicto quedan cubiertas por evidencia.
- **Matiz nuevo (no refuta, acota):** en `8bf412ac2ba3` **el producto sí existe pero la traza propia de la corrida, no** — el `.md` de `~/.hermes/cron/output/8bf412ac2ba3/` no se escribió ese día (último, 08-10 07:48) → hay efectos sin registro en el motor. Y **si el producto llegó al canal no es comprobable** con lo consultado: «el artefacto existe» prueba la generación, no la entrega.
- **El registro de incidencias no es fiable para todo `unknown`:** `cron_incidents` (14 filas, volcado completo) abrió/actualizó fila para `9474f6f3d224` (`9474f6_807bf8724760`, estado `detected`, `last_seen_at` 09-10 07:19:50, sin cerrar) pero **ninguna** para `8bf412ac2ba3` (`SELECT COUNT(*) … WHERE job_id LIKE '8bf412%'` = **0**) → **un `unknown` puede no llegar al registro de incidencias**. DUDOSO declarado en el acta (D9); el antídoto «artefacto primero» sigue siendo el único fiable.
- **Mecanismo raíz más completo:** estos 2 casos no nacen de un reinicio del planificador dentro de la jornada, sino del **arranque tras la ventana de apagado del host** (08-10 22:12:30 → 09-10 07:17:57), con la ráfaga de `catch_up` despachando ≥8 jobs en <1 s (ver **CP-013**). El `unknown` y la ráfaga de arranque comparten, por ahora, contexto de ejecución.

## 4. Mecanismo propuesto

Un reinicio durante una ejecución adoptada deja al worker `-15` sin estado terminal. El motor, en vez de asumir «no corrió» (falso) o «corrió» (falso), escribe `unknown`. El estado es correcto pero **no accionable**: no se puede reintentar a ciegas (riesgo de duplicar efectos) ni cerrar por diseño, así que la resolución se delega al operador. Si el ciclo no lee el registro de ejecuciones, el operador nunca se entera: la incertidumbre se queda sin resolver indefinidamente.

## 5. Condición de falsación

Sería **FALSO** si, sobre **N=10 ejecuciones** que terminan en `unknown` en el lab y durante **2 ciclos LPA consecutivos**, **8 o más** se resuelven consultando únicamente el estado del motor (sin ir al artefacto) con un veredicto correcto (efectos sí / efectos no) verificado después contra el producto.

Segunda vía de falsación (más probable): si en la próxima ventana aparece un `unknown` cuyo **artefacto sí existe pero está incompleto o es engañoso** (el producto existe y no prueba los efectos), entonces el antídoto propuesto aquí se cae y CP-012 debe fusionarse con **CP-010** (instrumento no validado miente) o con **CP-011** (escritura truncada), quedando como ocurrencia suya.

## 6. Antídoto propuesto (sin medir)

1. **Artefacto primero:** ante `unknown`, comprobar el producto antes de leer cualquier estado. No re-lanzar automáticamente.
2. **No re-ejecutar** un job con efectos externos por un `unknown`: primero el artefacto decide.
3. **Los ciclos deben leer el registro real** (`~/.hermes/cron/executions.db`: `executions` con `status not in ('ok','completed')` + `cron_incidents`), porque el registro declarado a mano puede estar muerto (31 días en el caso medido → CP-009).
4. En jobs `kind: once` sin efecto en disco (p. ej. un recordatorio), la única resolución es **preguntar al destinatario**: declarar el caso como no resoluble por instrumento.

## 7. Decisión

Incubar (E0). Promovido el 2026-10-02 con **5 ocurrencias en 5 contextos distintos** (supera el umbral de 2), pero **un solo mecanismo raíz** (reinicio del planificador) y un solo experimento (joko-lab): no asciende todavía.

- [ ] Asciende a KNOWN.md como E1 (falta un segundo experimento y un `unknown` resuelto por artefacto que no sea del mismo mecanismo)
- [ ] Asciende a procedures/ como procedimiento LPA (el antídoto «artefacto primero» ya se aplica en el ciclo, pero no está medido)
- [x] Sigue en incubación
- [ ] Se descarta (no sobrevive a otro dominio / fue falseado)
- [ ] Se fusiona con otro patrón (candidato declarado: **CP-010** — si el artefacto también engaña; y **CP-009** — el registro real que nadie lee. Antídoto propio y distinto: comprobar el producto)

**Fecha de revisión:** 2026-10-23 (semanal — **revisado el 2026-10-16: sobrevive**) y 2026-11-02 (mensual).
**Justificación:** 5 ocurrencias en 5 jobs de propósito distinto en una sola noche fue la evidencia más fuerte del ciclo del 02-10, pero compartían causa raíz (3 reinicios) y no había un caso que probara que el artefacto resuelve **siempre**: el recordatorio `once` es un contraejemplo declarado (no hay artefacto que mirar).
**Reexamen 2026-10-09 (era la fecha de revisión comprometida):** dos `unknown` nuevos, ya no por reinicio intradía sino por el arranque tras el apagado del host, resueltos en las **dos** direcciones (producto presente / producto ausente) y sin que el artefacto engañara al antídoto → **no se dispara la falsación de §5** y el patrón **sigue en incubación**. Aparecen dos bordes nuevos: (a) puede haber **producto sin traza** en el motor, así que el veredicto «efectos sí» no cubre la entrega; (b) `cron_incidents` **no registró** uno de los dos `unknown`, de modo que el registro sigue siendo incompleto como fuente única. La fusión con CP-010/CP-011 **no procede todavía** (el artefacto no engañó); la relación con **CP-013** (ráfaga de arranque) queda declarada.

**Reexamen 2026-10-16 (2ª revisión semanal consecutiva, sin cambio de nivel).** Ventana 09→16-10; acta `incidentes/revision-fallos-2026-10-16.md`.
- **El `unknown` de la ventana es uno:** fila de `executions` del job `9474f6f3d224` (consolidador-sesiones), `2026-10-15T22:30:35 → 22:31:09`, cola `SIGTERM (-15)`. **Resuelto por artefacto: efectos NO** — y el veredicto es correcto en el efecto (el producto del 15-10 no existía y hubo que regenerarlo a mano el 16-10 07:03), pero **no dice nada de la causa**: la causa real fue un **OOM del worker** en su cgroup de 4 GiB (`oom_memcg=…hermes-worker-cron-9474f6f3d224-exec-….scope`, `Killed process … anon-rss:4057072kB`), no un reinicio benigno del planificador.
- **Borde decisivo para §5:** un `unknown` puede estar **tapando un fallo real**. Hasta ahora la serie mostraba `unknown` por reinicio (incertidumbre benigna); este caso muestra que la misma etiqueta cubre un job muerto por el kernel. El antídoto «artefacto primero» sigue siendo válido (decide efectos) pero es **insuficiente como diagnóstico**: la causa vive en otra fuente (kernel/cgroup), no en el artefacto.
- **Relación declarada, sin fusión: CP-015** (nuevo, 16-10) — cuando la corrida muere antes de escribir el artefacto, «efectos NO» es correcto **y** insuficiente a la vez: dice que no hay producto, no por qué. CP-012 conserva su antídoto; CP-015 nombra su límite.
- **No se dispara la falsación de §5** (el artefacto no engañó al antídoto) y **sigue en incubación**; la generalidad mejora ligeramente: primer `unknown` de la serie con causa de fallo real y no de reinicio.
