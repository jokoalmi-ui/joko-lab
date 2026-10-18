---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-09-18
---
# CP-010: Un instrumento no validado miente en silencio

**ID:** CP-010
**Fecha:** 2026-09-18
**Estado:** E0 — Candidate Pattern
**Origen:** Revisión de fallos 2026-09-18 (ciclo semanal LPA, D0/INC-005) — 3 casos medidos en la ventana 14→18 sep, en 3 dominios distintos
**Nivel de confianza:** Medio (3 ocurrencias en 3 contextos distintos; todas con patrón oro independiente) + 1 caso fresco el 18-09 (el estado del propio scheduler, §2.4)

---

## 1. Qué ocurrió

En una sola semana, tres instrumentos del lab devolvieron un número **falso** sobre algo que el lab necesitaba decidir. Las tres veces el fallo estaba en la MEDICIÓN, no en lo medido, y las tres veces el error fue silencioso (nadie avisó):

- **(1) La tasa de la copia de rescate (disco).** La velocidad de escritura al USB se midió con `du -sm` sobre el DESTINO mientras el `rsync` seguía escribiendo: **0,43 MB/s ⇒ «~7 h»**, cifra que estuvo a punto de descartar el rsync por «inviable». La cifra real del mismo proceso, leída al final de su log (`rsync --stats`), fue **9,00 MB/s para 11,11 G** (≈20 min) — **20× más**. Causa: en FAT32 con miles de ficheros pequeños `du` no refleja lo escrito sin `sync`. Prueba independiente: escritura secuencial con `dd conv=fsync` → **274 MB/s**.
- **(2) La salud del conocimiento (panel del lab).** El panel midió **10 huecos donde había 12**: `tools/knowledge_health.py` no encontraba `yaml` en el intérprete con el que se lanzaba y los 2 huecos de conocimiento **desaparecían en silencio**. La cifra MEJORÓ sin que nada se hubiera arreglado.
- **(3) La transcripción de un carrusel (visión).** GLM-4.6V devolvió **3.540 chars / 517 palabras** para una tarjeta con **~180-300 palabras medibles**, y un **crop de 255 px** «leyó» tres secciones completas (físicamente imposible): el VLM **rellena** desde su conocimiento del tema. Lo delató una métrica sin modelo (densidad de tinta con PIL/numpy).

**Ampliación 2026-09-25 (ventana 18→25 sep) — el caso (4) se vuelve REPRODUCIBLE y aparece un cuarto dominio: la gobernanza del propio conocimiento:**
- **(5) El caso (4) no fue un accidente de una noche: es intermitente y ya lleva 3 noches seguidas.** Medido el 25-09: `consolidador-sesiones` **volvió a producir** las noches del 18, 19 y 21-sep (o sea, sí funciona a veces) y **no produjo ninguna** de las del 22, 23 ni 24-sep, con `last_run_at` congelado en **2026-09-21T22:31:07**, `last_status: ok` y `failure_streak: 0` durante los cuatro días, y el último despacho `on_time` (24-sep 22:30:20, lateness 20,8 s). Productos: `sesiones-*` hasta 20260921 y `resumen-dia-*` hasta 2026-09-20. El campo con el que el lab comprueba «¿produjo el job?» devuelve `ok` sobre tres noches vacías — y ahora el fallo es **reproducible**, que es justo lo que le faltaba al caso (4).
- **(6) El resumen de estado del curador miente sobre el curador.** `hermes curator status` → **`curator: PAUSED`** (leído el 25-09 a las 14:3x, con `last report` del 23-sep) mientras su ledger registra **36 entradas `actor: curator` del propio 25-09** (05:47:50 → 11:34:35 UTC). Mismo mecanismo que el caso (2) —un resumen que no mide lo que resume— pero ahora en la gobernanza del conocimiento, no en la instrumentación de un experimento.

## 2. Evidencia que lo respalda

- (1) `04-operations/backlogs/pendientes.md`, 17-sep 23:33 (líneas 71-75): cifras literales `du -sm` «0,43 MB/s ⇒ ~7 h» frente a «`rsync --stats`: 9,00 MB/s (11,11 G) — veinte veces más»; `dd … conv=fsync`: 274 MB/s; moraleja escrita por el propio fallo: «para decidir con una tasa, medirla con el instrumento del propio proceso, no con `du` a media escritura».
- (2) `04-operations/backlogs/pendientes.md`, 17-sep 22:59 (línea 61): «El panel llegó a medir 10 huecos porque `tools/knowledge_health.py` no encontraba `yaml` en el intérprete con el que se lanzaba; los 2 huecos de conocimiento desaparecían en silencio. […] Si algún día vuelve a marcar 10, es un medidor ciego, no una mejora». Arreglo aplicado en el CONSUMIDOR (abre hueco P1 con el error literal en vez de ocultarlo).
- (3) `~/.hermes/skills/media/instagram-content-extraction/SKILL.md` (líneas 548-566): medición del reel `DdXLhSlogX1` con la densidad real medida sin modelo y la regla «si el modelo devuelve 2-3× más palabras que las medidas, marcar la transcripción como NO literal».
- **(4) El estado del propio sistema de control (hallazgo del 18-09, distinto del resto por ser el medidor de la ejecución, no de un fenómeno externo).** El job `consolidador-sesiones` (`30 22 * * *`) fue **despachado a tiempo el 17-09 a las 22:30:15** (`last_dispatch.kind: on_time`, `fire_claim` tomado por `milinux:2496`), pero su `last_run_at` sigue en **2026-09-15T22:30:47** y **no produjo el `resumen-dia` de 15, 16 ni 17-sep**; su `last_status` dice **`ok`** y su `failure_streak` es **0**. Es decir: el campo con el que el lab comprueba «¿se ejecutó el job?» devuelve un dato falso sobre el producto. Sin `~/.hermes/cron/logs/` (ese directorio no existe) no hay evidencia de por qué arrancó y no completó.
- Regla previa del lab que ya apuntaba al mismo principio: **RULE-015** + skill `validacion-instrumentos-medicion` (pitfalls «instrumento ciego», «el mismo instrumento puede medir en tu shell y estar ciego en otro contexto de ejecución», «toda cifra DERIVADA se contrasta con los datos crudos»).
- Antecedente en otra semana: umbral A4 fijado a priori → falsos positivos masivos (01-sep), que motivó RULE-015.
- Ampliación 25-09: `~/.hermes/cron/jobs.json` → `consolidador-sesiones` (`9474f6f3d224`, script, `no_agent`, `30 22 * * *`): `last_run_at` **2026-09-21T22:31:07.365243+02:00**, `last_status: ok`, `failure_streak: 0`, `repeat.completed: 42`, `last_dispatch` {scheduled 2026-09-24T22:30:00, dispatched **22:30:20.764760**, lateness 20.8 s, `kind: on_time`}; rejilla de productos en `04-operations/metrics/sesiones/` → `sesiones-*` hasta 20260921 (sin 0916, 0917, 0920, 0922, 0923, 0924) y `resumen-dia-*` hasta 2026-09-20. `hermes curator status` literal (`curator: PAUSED`, `last report: ~/.hermes/logs/curator/20260923-170843`) frente a `~/.hermes/skills/.curator_ledger.jsonl` (**1.282 líneas**; **36 entradas `actor: curator` del 25-09**, de 05:47:50.448327+00:00 a 11:34:35.343375+00:00).
- **(7) La ventana declarada no puede medirse con ese instrumento: el registro de ejecuciones tiene tope de 1.000 filas.** Acta `revision-fallos-2026-10-02.md` §0: «`claimed_at >= 2026-09-25`: **1.001 filas** … Es decir: **9 ejecuciones sin estado terminal sano en 7 días**». Medido el 09-10 en `~/.hermes/hermes-agent/cron/executions.py`: `MAX_TERMINAL_EXECUTIONS = 1000` (línea 33) con poda por `finished_at` (`ORDER BY julianday(finished_at) DESC`, líneas 201-209) → el tope **ya estaba vigente el 02-10** (1.001 filas «en 7 días» solo es posible si la tabla está limitada: a ~1.000 filas/día, 7 días serían ~7.000). El número **no era falso**; la **etiqueta temporal sí**: la ventana real era de ~21-27 h. Comprobado hoy: 1.001 filas que abarcan 08-10 11:30:21 → 09-10 14:32:34 (**27 h**), 998 `completed` + 2 `unknown` + 1 `running`. Mismo mecanismo que (2) —un medidor que no mide lo que su etiqueta declara— aunque aquí no hay ceguera, hay diseño.

## 3. Contradicciones o limitaciones

- **Los tres casos se detectaron por casualidad, no por control sistemático:** no existe hoy una comprobación periódica de que los instrumentos del lab estén vivos y calibrados (el panel del lab persigue huecos del sistema, no la salud de sus propios medidores).
- El contraste exige un patrón oro que no siempre existe: para (1) fue el log del propio proceso + `dd`; para (3) la densidad sin modelo. Sin patrón oro, la etiqueta correcta es «NO VALIDADA / orden de magnitud» — nunca presentar la estimación como dato.
- Validar todo antes de usarlo es caro: el patrón NO dice «valida siempre», dice «valida antes de DECIDIR con el número» y deja la etiqueta de validez en la entrega.
- Un instrumento ya validado se **desvalida** si cambia su contexto de ejecución (intérprete, cgroup, sistema de ficheros, carga). El caso (2) es exactamente eso.
- No está medido cuánto resuelve la etiqueta de validez y cuánto exige un control automático (antídoto pendiente de evidencia).

## 4. Principio que parece emerger

> La cifra que decide tiene que venir de un instrumento validado contra una fuente independiente para ESE caso y ESE contexto de ejecución. Un instrumento no validado no devuelve «un dato con ruido»: devuelve un número falso con apariencia de dato, y su modo de fallo típico es silencioso (0,43 en vez de 9,00; 10 en vez de 12; texto generado en vez de leído). **Firma que lo delata: la cifra mejora sin que nada haya cambiado.** Ante un número que sorprende — por bueno o por malo — lo primero que se valida es el medidor, no la conclusión.

## 5. ¿En qué otros proyectos podría aplicarse?

- Cualquier lab o equipo que decida con números: observabilidad, benchmarks de modelos, ETL, informes de coste.
- Sistemas con dashboards: distinguir «el sistema mejoró» de «el medidor se rompió» (una métrica que baja sola es sospechosa).
- Evaluación de LLM/VLM: el modelo que genera contenido plausible sobre material que no ha leído es este mismo fallo con otro disfraz.
- Instrumentación de copias/backups: medir con el instrumento del propio proceso, nunca con un snapshot externo tomado a mitad de operación.

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

Sería **FALSO** si, sobre **N=10 instrumentos** del lab usados para decidir durante **2 ciclos LPA consecutivos**, comparados contra su patrón oro, **al menos 9** devuelven la cifra correcta (dentro de la tolerancia declarada) **sin** validación previa ni etiqueta de validez; es decir, si fiarse del número funciona ≥90% de las veces. También lo falsaría que los fallos aparecieran solo en instrumentos que nadie usa para decidir (ruido, no riesgo).

## 7. Decisión

**Revisión mensual 2026-10-02 — ASCENDIDO.** Acta: `incidentes/revision-fallos-2026-10-02.md` (D10).

- [x] Asciende a KNOWN.md como **E1-008** («Un instrumento no validado miente en silencio»)
- [ ] Asciende a procedures/ como procedimiento LPA (el antídoto —etiqueta de validez vs control automático contra patrón oro— todavía no está medido)
- [ ] Sigue en incubación — **cerrada el 2026-10-02**: la incubación se resolvió con el ascenso
- [ ] Se descarta (no sobrevive a otro dominio / fue falseado)
- [ ] Se fusiona con otro patrón (candidatos: **CP-008 estado-real-vs-documentado** — comparten «la fuente de verdad no es el registro»; CP-010 lo lleva al medidor. **CP-006 verification-by-evidence** — CP-006 dice «afirmar exige evidencia»; CP-010 añade «la evidencia puede venir de un medidor roto». **No fusionado el 2026-10-02:** antídotos distintos — CP-010 se arregla con etiqueta de validez/patrón oro; CP-011 (escritura truncada) con comprobación de tamaño y cola; CP-008 con muestreo periódico)

**Ascenso:** 2026-10-02 → `KNOWN.md` **E1-008**. Ocurrencias: 5 (ventana anterior) → **6 en 4 dominios**, con el 5º caso **sostenido 8 días**: `hermes curator status` = `PAUSED` / `last run 8d ago` frente a **703 operaciones** reales en `.curator_ledger.jsonl` con fecha ≥ 2026-09-25 (171/80/74/57/90/112/83/36; última 2026-10-02T12:16:38Z). Falsación copiada literalmente a `KNOWN.md`; **limitación declarada:** toda la evidencia es del Experimento 004 → E1 «patrón observado».
**Fecha de revisión:** 2026-10-23 (semanal — **revisado el 2026-10-16: sobrevive**) y 2026-11-02 (mensual) — o inmediata si aparece evidencia de un segundo experimento.
**Última revisión:** 2026-10-16
**Justificación:** 3 ocurrencias en 3 contextos distintos (tasa de copia a disco, salud del conocimiento, transcripción por VLM), todas con cifras contrastadas y reproducibles, más una regla previa (RULE-015) que ya apuntaba al mismo principio. **Añadido 25-09: +2 ocurrencias → 5**, y el 4º dominio ya está (la gobernanza del conocimiento): el caso (4) reproducido tres noches seguidas con `last_status: ok` y el resumen de estado del curador frente a su propio ledger. Falta medir el antídoto (etiqueta de validez vs control automático).

**Reexamen 2026-10-16 (E1-008, sin cambio de nivel).** Ciclo semanal 09→16-10; acta `incidentes/revision-fallos-2026-10-16.md`.
- **7ª ocurrencia (misma forma, cifras nuevas):** `hermes curator status` sigue en **`PAUSED`, `runs: 13`, `last run: 22d ago`**, con `last report` = `~/.hermes/logs/curator/20260923-170843`, mientras `.curator_ledger.jsonl` acumula **64 filas nuevas** en la ventana (**11-10: 35 · 12-10: 9 · 13-10: 4 · 15-10: 3 · 16-10: 13**) y **2.203 filas** en total (por actor: `curator` 1.667 / `agent` 536). Última fila: `2026-10-16T08:39:01.417998+00:00`, acción `patch` sobre `seguimiento-empleo`. El medidor declarado lleva 22 días sin ejecutarse y el ledger que mide trabajo real no ha parado ningún día.
- **8ª ocurrencia (forma nueva: la etiqueta `resolved` del registro de incidencias):** `cron_incidents` = **17 de 19 filas en `resolved`**, y `resolved` mide «hubo una corrida sana de ese job después», **no** «la causa está reparada». Dos pruebas medidas el mismo día: (a) `da39a2_fae825d0fe36` (rag-reindex, `timeout`) se cerró el **08-10** tras **33 días** abierta y **4 días después reaparece la misma firma** (`da39a2_563646c13b70`, `timeout 300 s`, `alerted`, abierta a 16-10) → el cierre no reparó nada; (b) las dos filas del `380a80273240` (Orquestador recuperación horaria) se cerraron a la vez el **15-10 15:15:37**, cuando el productor no se arregló hasta las **15:47** y el producto se regeneró a las **15:49** → cierre y causa desalineados en 31 min. Es exactamente el mecanismo del patrón: **la etiqueta promete más de lo que el instrumento mide.**
- **Nivel sin cambio (E1-008):** 3er ciclo semanal consecutivo sin cambio de nivel; la ocurrencia nueva **no amplía dominio** (sigue en el Experimento 004) pero sí amplía **familia de instrumento** (del estado de salud y del ledger al contador de incidencias resueltas).
