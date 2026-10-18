---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-09-14
---
# CP-009: Un instrumento sin disparador no se usa

> **Estado:** Incubación (E0→E1)
> **Fecha:** 2026-09-14
> **Origen:** Revisión de fallos 2026-09-14 (ciclo semanal LPA, D0/INC-005) — hallazgos C1 y C2
> **Nivel de confianza:** Medio-alto (5 ocurrencias en 5 contextos distintos; evidencia en disco, verificable)
> **Ampliado:** 2026-09-18 (ciclo semanal LPA; ventana 14→18 sep) — 2 ocurrencias nuevas (§1). Sigue en incubación; candidato a E1 en la revisión mensual del 01-10.

---

## 1. Qué ocurrió

Tres mecanismos del lab fueron creados/DECIDIDOS con una función clara y **nunca produjeron un solo registro**, pese a que había actividad real y material que registrar:

- **(1) Ficheros de conocimiento LPA:** ningún fallo ascendió a `patterns-observed.md`/`pattern-incubator` entre el 31-07 y el 01-09. Es el fallo INC-005, el que motivó reactivar el ciclo semanal el 02-09.
- **(2) Registro diario de incidentes** (`lpa/incidentes/YYYY-MM-DD-incidentes.md`), creado como remedio de INC-005: **0 ficheros desde el 01-09** (12 días) con 193 sesiones de actividad en 6 de esos días.
- **(3) Ledger del EXP-20260903-001** (`04-operations/metrics/retrabajo_ledger.jsonl`), aprobado por el usuario el 03-09 para 7 días de registro prospectivo: **0 bytes / 0 líneas** el 14-09, tras 6 días de actividad, y con al menos 1 evento de la taxonomía cerrada E1-E7 documentado el primer día de la ventana (`pendientes.md`: 04-09 ~14:15, GPU ocupada → `llama-server 'exited before becoming healthy'` = E4).

En los tres casos el instrumento existía, estaba decidido y era barato de usar (~1 línea por evento). Lo que faltaba era **el disparador**: los tres dependen de que el agente recuerde escribir en el momento.

Contraste medido en la misma ventana: los mecanismos que **sí** producen fichero cada día son los que tienen cron (`observador diario` → OBS-098..103 + `telemetria/*.json|.md`; backups hermes-state 22:20). Los que dependen de disciplina muestran huecos verificables (backlog grande: sin entradas los días 04, 05 y 07-09).

**Ampliación 2026-09-18 (ventana 14→18 sep) — el caso que mejor ajusta el patrón es un instrumento a MEDIAS:**

- **(4) El registro diario de incidentes sigue a 0 — 2ª semana consecutiva.** Último `*-incidentes.md`: `2026-09-01-incidentes.md`. Verificado el 18-09 con listado del directorio y búsqueda del patrón → **1 solo fichero**: 17 días sin materializarse, pese a actividad documentada TODOS los días de la ventana en `pendientes.md` (entradas del 15, 16, 17 y 18-sep). El remedio de INC-005 nació sin disparador y sigue sin él.
- **(5) Un instrumento con disparador en una mitad y sin disparador en la otra.** El pipeline diario de fichas de perfume (script + checklist + verificación) SÍ produce la ficha cada día; lo que no se cierra es la fila del registro `uso_diario`: 5 fichas de la ventana sin registro (10, 11, 12, 13 y 15-sep), la primera pendiente desde el 15-sep. No es olvido puro — hay una compuerta que exige el OK del usuario — pero NO existe ninguna comprobación periódica que detecte el pendiente acumulado y lo exija: resultado, 5 huecos en 8 días.
- **Contraste positivo mantenido:** donde hay disparador automático hay registro (`telemetria/*.json|.md` y las OBS del observador diario, 14-09 07:10). Tercer dato de la ventana: el job cron de un solo uso del 17-09 12:20 produjo su entregable sin intervención — el disparador automático funcionó también para trabajo NO recurrente.

**Ampliación 2026-09-25 (ventana 18→25 sep) — 2 ocurrencias más y 1 caso CERRADO a medias, que es el dato más informativo:**
- **(6) El registro de lecciones del lab: 7 días sin una línea, mientras el registro automático crecía todos los días.** `lecciones_ledger.jsonl` sigue en **9 líneas (mtime 18-sep 14:40)**; el ledger del curador (`~/.hermes/skills/.curator_ledger.jsonl`, 1.282 líneas, 36 entradas solo el 25-09) recibe lo que el manual no recibe. No es «0 eventos»: la ventana produjo lecciones reales que entraron por otro canal (acta 24-sep: «Lecciones en skills: NO se escriben aquí […] Traza: ids `4a55249e29b0`, `4fa91bace86c`, `e03e1576f508`»).
- **(7) Un instrumento CON disparador que produce 3 de 8 noches → matiza otra vez el antídoto.** `resumen-dia`: presentes 17, 18 y 20-sep; ausentes 19, 21, 22, 23 y 24-sep, con el job despachado `on_time` cada noche y `last_status: ok` (detalle en CP-010 y en F1 del acta del 25-09). El disparador evitó el 0 absoluto (el instrumento no murió) pero **no garantiza el registro**: sin comprobar el PRODUCTO, un disparador que falla en silencio deja el mismo hueco que la falta de disparador.
- **(8) El caso (3) queda CERRADO — y se cierra por disciplina, no por mecanismo.** `retrabajo_ledger.jsonl` recibe su **PRIMERA entrada 22 días después de su diseño**: 1 línea / 566 B, mtime **25-09 13:29** (`tipo: E6`, `sesion_id: 20260925_090159_b65803`, `causa_raiz`: «reescritura de la instruccion (4 variantes) sin cubrir el RF: los mismos 2 casos fallan en las 5 y la metrica no se mueve (6/8 en todas)», `tokens_estimados_correccion: 4710`, `tiempo_min: 0.7`). El asiento entró durante una sesión de trabajo, leyéndolo y escribiéndolo a mano: **el instrumento funcionó cuando alguien se acordó de él**. Es la mejor evidencia a favor del principio y, a la vez, la advertencia: sin disparador, el siguiente asiento vuelve a depender de la memoria.

## 2. Evidencia que lo respalda

- `retrabajo_ledger.jsonl`: 0 bytes, mtime 2026-09-03 14:56 (verificado con `stat` y `wc -l` el 14-09).
- `lpa/incidentes/`: sin ningún `*-incidentes.md` posterior al 01-09 (verificado con `ls -la` y `find`).
- Aprobación y pausa flexible del experimento: `04-operations/backlogs/2026-07-31-backlog.md` líneas 1631-1635 y 1643-1647 (03-09 14:56 y 15:06).
- Evento E4 documentado fuera del ledger: `04-operations/backlogs/pendientes.md` (04-09 ~14:15).
- Mecanismos con disparador activos el mismo periodo: OBS-098/099/100 (09-09 22:00), OBS-101/102/103 (14-09 07:10), `telemetria/2026-09-14.json`.
- Antecedente de la misma familia: INC-005 (01-09) con el diagnóstico «el problema no es el documento, es el hábito» → hipótesis refutada por C2 (misma causa, 12 días después).
- Ampliación 18-09: `ls -la lpa/incidentes/` + búsqueda de `*-incidentes.md` → 1 único fichero (`2026-09-01-incidentes.md`, 8.988 B); `pendientes.md` líneas 82-85 (18-sep 08:02) para las 5 fichas de la ventana sin fila en `uso_diario` y la decisión del usuario de no corregir la BD.
- Tercer instrumento sin alimentar, ya detectado por el panel del lab en la misma ventana: los logs de vigilancia `docker_health` y `n8n_health` figuran como «vacíos/inexistentes» (`pendientes.md` 17-sep, líneas 59-60) — instrumentos que no producen su registro. (Solo lectura; n8n es zona protegida.)
- Ampliación 25-09: `wc -l` + `stat` de `04-operations/metrics/lecciones_ledger.jsonl` (**9 líneas**, 7.987 B, mtime 18-sep 14:40) frente a `~/.hermes/skills/.curator_ledger.jsonl` (1.282 líneas; 36 entradas `actor: curator` del 25-09). Rejilla real de productos de `consolidador-sesiones` en `04-operations/metrics/sesiones/`: `sesiones-*` hasta **20260921** (serie 0907, 0908, 0909, 0914, 0915, 0918, 0919, 0921 — sin 0916, 0917, 0920, 0922, 0923, 0924) y `resumen-dia-*` hasta **2026-09-20**; cruzada con `~/.hermes/cron/jobs.json` (`last_run_at` 2026-09-21T22:31:07.365243+02:00, `last_status: ok`, `failure_streak: 0`, `last_dispatch` 2026-09-24T22:30:20.764760 `on_time`). Contenido literal del ledger de retrabajo: `cat 04-operations/metrics/retrabajo_ledger.jsonl` → **1 línea**, 566 B, mtime 25-09 13:29. Contraste positivo: `telemetria/*.json|.md` con los 8 días de la ventana (17→24-sep).

## 3. Contradicciones o limitaciones

- **No se puede separar «no hubo eventos» de «no se registraron»** en el caso (3): 0 líneas no es lo mismo que «0 incidentes E1-E7». En (1) y (2) el hueco es indiscutible (documentos y ficheros ausentes).
- El caso (3) tiene un factor atenuante real: el experimento pasó a pausa flexible el mismo día por ausencia del usuario (LAB apagado). Aun así, el diseño mantenía el registro activo en días de actividad y hubo 6 días así.
- Casos de «no usar un instrumento» por decisión consciente (herramientas manuales, experimentos aparcados a propósito) NO son evidencia del patrón: hay que distinguir instrumento muerto de instrumento en espera declarada. El caso (5) es mixto: la compuerta de OK humano es deliberada, el pendiente acumulado sin comprobación no.
- No está medido cuánto del problema se resuelve simplemente con una comprobación periódica (auditoría) frente a exigir un disparador automático. Ambas soluciones son hipótesis.
- Un disparador automático tiene coste (cron, código, ruido si no hay nada que registrar). El patrón no dice que todo deba automatizarse: dice que un instrumento sin disparador NI verificación periódica tiende a 0.

## 4. Principio que parece emerger

> Un instrumento que depende de que alguien recuerde usarlo tiende a cero. Todo mecanismo con función operativa (registro, ledger, promoción, revisión) necesita al menos uno de estos dos: (a) un disparador automático que lo ejecute, o (b) una comprobación periódica dentro de un ciclo que ya funciona, que detecte que sigue a 0 y lo exija. La disciplina no es un mecanismo: es un deseo. Y un instrumento creado no es un instrumento en uso: la prueba de que funciona es el primer registro real, no el fichero vacío.

## 5. ¿En qué otros proyectos podría aplicarse?

- Cualquier operación que cree ledgers, registros de incidentes, métricas de salud o ciclos de revisión «para más adelante».
- Labs y equipos con documentación de proceso viva (gobernanza de conocimiento, post-mortems, comités de calidad).
- Sistemas multi-agente/multi-sesión: un instrumento creado por una sesión no lo ve ni lo usa la siguiente si no está enganchado a algo automático.
- Observabilidad: distinguir «métrica en 0» de «métrica sin datos» (una serie vacía no es un cero).
- Auditorías de higiene (skill `detectar-sin-uso`): los instrumentos no alimentados son candidatos naturales a hallazgo.

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

Sería **FALSO** si, medido sobre **N=10 instrumentos nuevos** del lab (ledger/registro/ciclo creados sin disparador automático ni comprobación periódica) durante **2 ciclos consecutivos**, al menos 8 de ellos acumulan registros reales en su primer periodo de uso **sin** que nadie los verifique ni los dispare desde fuera. Es decir: si el uso sostenido por pura disciplina ocurre ≥80% de las veces, el patrón no se sostiene y el problema es de otro tipo (diseño del instrumento, coste de uso, utilidad percibida).

## 7. Decisión

**Revisión mensual 2026-10-02 — ASCENDIDO.** Acta: `incidentes/revision-fallos-2026-10-02.md` (D10).

- [x] Asciende a KNOWN.md como **E1-007** («Un instrumento sin disparador no se usa: el que depende de que alguien se acuerde se degrada»)
- [ ] Asciende a procedures/ como procedimiento LPA (el antídoto —disparador automático vs comprobación periódica— todavía no está medido)
- [ ] Sigue en incubación — **cerrada el 2026-10-02**: la incubación se resolvió con el ascenso, no con más ocurrencias
- [ ] Se descarta (no sobrevive a otro dominio / fue falseado)
- [ ] Se fusiona con otro patrón (**candidato: CP-008** «estado real vs documentado» — su principio ya incluye «una métrica en 0 que nadie mira equivale a no tener métrica»; CP-009 lo extiende a todo mecanismo y añade el criterio del disparador vs la comprobación periódica. **Añadido 18-09: CP-010 instrumento-no-validado-miente** — CP-009 trata el instrumento que no se usa; CP-010, el que se usa y miente. **No fusionado el 2026-10-02:** los antídotos son distintos — CP-009 se arregla con disparador, CP-008 con muestreo periódico documento↔fuente, CP-010 con etiqueta de validez)

**Ascenso:** 2026-10-02 → `KNOWN.md` **E1-007**. Ocurrencias: 7 (ventana anterior) → **9 en 7 dominios** (se añaden las 2 de la ventana 25-09→02-10: `lecciones_ledger` congelado 7 días con `retrabajo_ledger` en 1 entrada; y el registro declarado de incidentes muerto 31 días frente a las 13 incidencias reales del motor). Falsación copiada literalmente a `KNOWN.md`; **limitación declarada:** toda la evidencia es del Experimento 004 (joko-lab) → E1 «patrón observado», no habilita reglas estructurales.
**Fecha de revisión:** 2026-10-23 (semanal — **revisado el 2026-10-16: sobrevive**) y 2026-11-02 (mensual) — o inmediata si aparece evidencia de un segundo experimento.
**Última revisión:** 2026-10-16
**Justificación:** 5 ocurrencias en 5 contextos distintos (gobernanza de conocimiento, registro de incidentes —2 veces—, instrumentación de experimento, registro diario de negocio, logs de vigilancia) + contraste verificado con mecanismos que sí tienen disparador. **Añadido 25-09: +2 ocurrencias** (el registro de lecciones del lab congelado frente al registro automático; un instrumento CON disparador que produce 3 de 8 noches) **= 7 ocurrencias en 7 contextos**, más el caso del ledger de retrabajo cerrado a mano 22 días después de su diseño. Falta medir el antídoto (disparador automático vs comprobación periódica) y desambiguar «0 registros» de «0 eventos».

**Reexamen 2026-10-09 (E1-007, sin cambio de nivel).** Ciclo semanal 02→09-10; acta `incidentes/revision-fallos-2026-10-09.md`.
- `retrabajo_ledger.jsonl`: **566 B, mtime 25-09 13:29** → **14 días sin asiento nuevo**; la fecha de evaluación que le puso el acta del 02-10 (D4) venció sin que el instrumento se moviera solo.
- `lecciones_ledger.jsonl`: llegó a los **7 días congelado** (mtime 02-10 14:37) y **hoy se descongela** con 3 lecciones nuevas (LEC-…-017..019) → deja de contar como ocurrencia activa, pero confirma el mecanismo: solo lo mueve un ciclo que se acuerda de él.
- `resumen-dia`/`sesiones-*`: **`sesiones-20260930.jsonl` es el último** (824 MB) y `resumen-dia` llega hasta el 29-09, mientras `consolidador-sesiones` acumula **`failure_streak` = 8** y `last_run_at` de hoy → el producto diario lleva 8 noches sin generarse y el job «existe y corre». Es la ocurrencia original del patrón, repitiéndose.
- **Nivel sin cambio (E1):** la evidencia nueva refuerza el mecanismo, no amplía el dominio (todo sigue en el Experimento 004 / joko-lab).

**Reexamen 2026-10-16 (E1-007, sin cambio de nivel).** Ciclo semanal 09→16-10; acta `incidentes/revision-fallos-2026-10-16.md`.
- `retrabajo_ledger.jsonl`: **566 B, mtime 25-09** → **21 días sin asiento nuevo** (eran 14 el 09-10). La fecha de evaluación del acta del 02-10 (D4) y la del 09-10 (D3) **siguen sin ejecutarse**: el instrumento no se ha movido solo en ningún momento. **3er ciclo semanal consecutivo** en que el patrón se manifiesta por el mismo sitio.
- `lecciones_ledger.jsonl`: llegó a los **7 días congelado** (mtime 09-10 14:38) y **hoy se descongela otra vez**, con 3 lecciones nuevas (LEC-…-020..022). **2ª vez consecutiva** que el disparador de facto del instrumento es este ciclo: sin él, sigue muerto.
- `[truncated]`: **4 ficheros** (3 vivos en `~/.hermes/skills/` + 1 `.bak-20250726`) → **3er ciclo sin tocarse desde que se midió**.
- Cron del motor: el job `9474f6f3d224` (consolidador-sesiones) acumula **`failure_streak` = 15** con `last_run_at` de anoche y su producto no se generaba desde el **30-09**; el del 15-10 lo regeneró **un humano a mano** (16-10 07:03). Es la misma manifestación que el 09-10 (entonces streak 8), agravada: ningún mecanismo automático detectó las 15 noches.
- **Contraste medido (lo que sí funciona):** el mismo día, el `informe-diario-joko-lab` (productor con consumidores que se quejan cada hora) se arregló y **se verificó** — 4 filas de incidencia cerradas y los 3 jobs de la cadena en `ok`. La diferencia no es la gravedad del fallo, es que **tiene consumidor**: el `retrabajo_ledger`, sin consumidor, lleva 21 días congelado. Refuerza el mecanismo (disparador externo > comprobación periódica) sin ampliar dominio.
- **Nivel sin cambio (E1):** sigue siendo solo Experimento 004 (joko-lab).
