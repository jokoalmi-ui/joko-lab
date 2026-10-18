---
type: lpa
subtype: incidentes
status: active
created: 2026-10-09
ventana: 2026-10-02 → 2026-10-09
---

# REVISIÓN DE FALLOS — 2026-10-09 (ciclo semanal LPA)

- **Fecha real de la corrida:** viernes **2026-10-09**, `date` = **2026-10-09 14:38:03 CEST**.
- **Motor (cita literal de `~/.hermes/cron/jobs.json`):** `lpa-revision-incidentes-semanal`, id `05de86a93257`, `expr "30 14 * * 5"`; despacho de hoy `scheduled_at 2026-10-09T14:30:00+02:00` / `dispatched_at 2026-10-09T14:30:33.963561+02:00` → **`on_time` (34,0 s)**. En `executions.db` esta corrida es `497bb53553a94fc98ce7711797dfd627`, estado `running`, `claimed_at` 14:30:34, `progress_at` 14:36:42. `next_run_at`: **2026-10-16T14:30:00+02:00**.
- **Ventana revisada:** 2026-10-02 14:31 CEST (cierre del acta anterior) → 2026-10-09 14:38 CEST.
- **Acta anterior:** `revision-fallos-2026-10-02.md` (D0..D12, incluye revisión mensual del incubator).
- **Paso 5 (revisión mensual) NO aplica:** esta es la 2ª corrida de octubre.

---

## 0. Incidentes de la ventana (paso 1)

**No hay ningún `*-incidentes.md` nuevo.** El único fichero con ese sufijo sigue siendo `2026-09-01-incidentes.md` (8.988 B, mtime **2026-09-03 13:38**) → **36 días sin una sola escritura**. Por esa vía no se promueve nada y no se inventa trabajo.

**Fuente real (D0 del acta 02-10, se mantiene):** `~/.hermes/cron/executions.db` (solo lectura, `mode=ro`) + artefactos en disco.

- `cron_incidents`: **14 filas** = **13 `resolved`** + **1 `detected`**. La única abierta es `9474f6_807bf8724760` (job `9474f6f3d224`, consolidador-sesiones): `first_seen_at` 2026-10-01T22:30:34, `last_seen_at` **2026-10-09T07:19:50**, `error` (literal): *«Restart-safe cron worker exited with status -15 after adopting this execution, without writing a durable terminal state; whether side effects ran is unknown.; worker stderr: <frozen runpy>:130: RuntimeWarning: 'cron.scheduler' found in sys.modules after import of package 'cron', but prior to execution of 'cron.scheduler'; this may result in unpredictable behaviour»*.
- **7 incidencias cerradas dentro de la ventana** (por `closed_at`):

| id | job | tipo | `first_seen_at` → `closed_at` |
|---|---|---|---|
| `3d18a8_461a55ce7111` | Bolsa autónoma — scan EXP-002 | `unknown` (worker reiniciado) | 01-10 22:49 → 02-10 22:34 |
| `1d0675_7798067f2f51` | Entrenador emocional diario | `unknown` (worker reiniciado) | 01-10 22:49 → 02-10 22:01 |
| `67d5fc_22755947367a` | informe-diario-joko-lab | `timeout` 300 s | 02-10 09:24 → 03-10 09:01 |
| `abffcc_56e9292450f7` | **kel-revalidacion-diaria** | `script` (`import yaml`) | 01-10 22:12 → **04-10 19:23** |
| `da39a2_d27e3eaf34c5` | rag-reindex-daily | `unknown` | 04-10 08:01 → 05-10 08:02 |
| `da39a2_fae825d0fe36` | rag-reindex-daily | `timeout` 300 s | 05-09 08:05 → **08-10 08:02** (**33 días** de recurrencia) |
| `264c02_761c7f27bcb0` | telegram-watchdog | `script` («API Telegram no responde») | 16-09 06:58 → **08-10 07:09** (**22 días**) |

- `executions` (retención **corta**, ver F3): **1.001 filas** con rango **2026-10-08 11:37:21 → 2026-10-09 14:40:34** = **27 h** → 998 `completed`, **2 `unknown`**, **1 `running`** (esta corrida) — medido dentro de la propia corrida: la fila más antigua se va podando mientras el job avanza. **No hay `failed` en la cola**: los 4 `failed` del 01-10/02-10 ya no existen en la tabla.
- **Los 2 `unknown`** (ambos en la ráfaga de arranque del host, ver F7):

| job | `claimed_at` | `finished_at` | `error` (literal) |
|---|---|---|---|
| `9474f6f3d224` consolidador-sesiones | 09-10 07:17:57.624 | 09-10 07:19:50.012 | *Restart-safe cron worker exited with status -15 after adopting this execution, without writing a durable terminal state; whether side effects ran is unknown.* |
| `8bf412ac2ba3` ficha-perfume-diaria | 09-10 07:17:58.357 | 09-10 07:33:33.960 | *Scheduler restarted after this execution's owner exited before a durable terminal state; whether side effects ran is unknown.* |

---

## 1. Actividad de la ventana (contexto verificado)

- **Telemetría:** 7/7 días con `.json` + `.md` (`2026-10-02` … `2026-10-08`).
- **Observaciones:** últimas `OBS-179-decisiones-por-politica-(2026-10-08).md`, `OBS-180-fallback-rate-2026-10-08.md`, `OBS-181-uso-rag-2026-10-08.md`.
- **Informe local diario:** `04-operations/reports/20261007-informe-local.txt`, `20261008-…`, `20261009-…` (hoy generado).
- **Artefactos de hoy:** `research/infografias/perfume-del-dia-20261009/` (15 ficheros, 07:23→07:52).
- **`git status --porcelain`:** **18 entradas** (medido al cierre: 6 `M` + 12 `??`) sin commitear. **No se hace `git add`/`commit`** de los hallazgos (D12 del 02-10, se mantiene).
- **`uptime -s` = 2026-10-08 08:08:21** → la caída de la madrugada fue **suspensión del host, no reinicio** (contexto de F9).

---

## 2. Fallos y hallazgos de la ventana

### F1. [RECURRENCIA, 4º ciclo] `consolidador-sesiones`: producto parado y `failure_streak` en 8
`jobs.json` → `9474f6f3d224`, `last_status: **error**`, **`failure_streak: 8`**, `last_run_at` 2026-10-09T07:19:50. En disco el último producto es **`04-operations/metrics/sesiones/sesiones-20260930.jsonl`** (824.729.608 B, mtime **2026-09-30 22:31**) y el último resumen **`resumen-dia-2026-09-29.md`** (489 B, mtime 30-09 22:31). **Nada escrito desde el 30-09 22:31 → 8 noches sin producto**, consistente con el streak. La incidencia `9474f6_807bf8724760` lleva **8 días abierta** (`detected`, sin `closed_at`).

### F2. [RECURRENCIA, 4º ciclo] El curador escribe a diario con el estado diciendo PAUSED
`hermes curator status` (literal): **`curator: PAUSED`**, `runs: 13`, **`last run: 15d ago`**, `last report: /home/jokoalmi/.hermes/logs/curator/20260923-170843`. Frente a eso, el ledger real (`~/.hermes/skills/.curator_ledger.jsonl`, 2.139 filas: 1.667 `actor: curator` + 472 `actor: agent`) registra **245 filas en la ventana** (02-10: 52, 03-10: 20, 04-10: 70, 05-10: 14, 06-10: 31, 07-10: 55, 08-10: 3) y **0 el 09-10** (última fila: 2026-10-08T05:16:00+00:00). Estado de skills: 104 gestionadas (79 creadas por agente, 25 bundled) → **75 active / 29 stale / 0 archived**; **11 pinned**; 70 no gestionadas (todas `foreground-created`).

### F3. [NUEVO] El registro de ejecuciones **no puede sostener una ventana semanal**: tope de 1.000 filas
`~/.hermes/hermes-agent/cron/executions.py`: **`MAX_TERMINAL_EXECUTIONS = 1000`** (línea 33) con poda por `finished_at` (`ORDER BY julianday(finished_at) DESC`, líneas 201-209). Medido hoy: 1.001 filas que abarcan **27 h** (2026-10-08 11:37:21 → 2026-10-09 14:40:34), no 7 días. Esto **reescribe el §0 del acta del 02-10**: el «1.001 filas en 7 días» no era falso como número, sí como etiqueta temporal (la ventana real era ~21-27 h). Consecuencia operativa: **en `executions` no se puede contar nada «de la semana»**; la ventana se reconstruye con `cron_incidents` + artefactos + actas.

### F4. [CERRADO] F6 del 02-10 (`kel-revalidacion-diaria`, `import yaml`): causa raíz real y cierre verificado
La incidencia `abffcc_56e9292450f7` está **`resolved` con `closed_at` 2026-10-04T19:23:11**, y el job `abffcc12711c` tiene hoy `last_status: ok`, `failure_streak: 0`, despacho `on_time`.
**Causa raíz real (no era el script):** desde el **01-oct** el `PATH` del cron resuelve `python3` al **python empaquetado de Hermes** (`~/.hermes/tools/python-3.14.7+20260901-linux-x64/bin/python3`), que **no trae PyYAML**. Verificado el 09-10: ese intérprete lanza `ModuleNotFoundError: No module named 'yaml'`; el venv de Hermes y `/usr/bin/python3` sí traen `yaml 6.0.3`. El binario empaquetado está fechado **2026-10-01 07:09**. El arreglo quedó en el **lanzador**, no en el script: `~/.hermes/scripts/kel-revalidacion.sh` (mtime **04-oct 19:21**) fija `PY="$HOME/.hermes/hermes-agent/venv/bin/python3"` con fallback.

### F5. [RECURRENCIA, 2º ciclo] `retrabajo_ledger.jsonl`: 1 entrada, 14 días → **se cumple la condición de D4**
`04-operations/metrics/retrabajo_ledger.jsonl`: **566 B, mtime 2026-09-25 13:29** → **14 días sin asiento nuevo**. La D4 del 02-10 concedió una ventana con condición explícita («si el 09-10 sigue en 1, se propone fusionarlo con `lecciones_ledger` o darle disparador»). **La condición se cumple hoy** → ver D3.

### F6. [RECURRENCIA, 2º ciclo] `[truncated]`: 3 ficheros vivos + 1 copia
`grep -rl '\[truncated\]' ~/.hermes/skills/` → **4 ficheros** (1 marca cada uno): `render-html-a-imagen/SKILL.md`, `joko-lab/validacion-instrumentos-medicion/SKILL.md`, `software-development/perfume-ia/references/capa-lpa-recomendacion.md` y la copia `validacion-instrumentos-medicion/SKILL.md.bak-20260918`. **Sigue sin reparar** (D5 del 02-10): el contenido perdido no está en ninguna copia y RULE-018 prohíbe a un proceso de fondo reescribir skills sin OK. El tercer fichero vivo no aparecía nominalmente en el P0 anterior.

### F7. [NUEVO] Dos `unknown` con la misma forma y distinto desenlace: el antídoto de CP-012 resuelve en las dos direcciones
Los 2 `unknown` de hoy (§0) salen de la **misma ráfaga de arranque** (07:17:57,62 y 07:17:58,35) y en jobs de propósito distinto:
- `9474f6f3d224` (consolidador): producto **ausente** (`sesiones-20261008.jsonl` y `resumen-dia-2026-10-08` no existen) → **efectos NO**.
- `8bf412ac2ba3` (ficha-perfume): producto **presente y completo** (15 ficheros, 07:23→07:52; PNG 1.808.675 B) → **efectos SÍ**; pero **su traza propia no se escribió** (último `.md` en `~/.hermes/cron/output/8bf412ac2ba3/`: 2026-10-08 07:48) y `last_run_at` sigue en 08-10 07:48.
- **El registro de incidencias no cubre todo `unknown`:** `cron_incidents` tiene fila para `9474f6f3d224` pero **ninguna** para `8bf412ac2ba3` (`COUNT(*) WHERE job_id LIKE '8bf412%'` = **0**).

### F8. [RECURRENCIA, 2º ciclo · consecuencia para el usuario] El recordatorio `once` del 01-10 sigue sin ejecutarse
`d824bcf4a2ff` «Recordatorio publicar L5 (1-oct)»: `enabled: true`, `state: scheduled`, **`next_run_at: 2026-10-01T09:00:00+02:00`** (en el pasado), **`last_run_at: null`**, `last_status: null`, `repeat {times: 1, completed: 1}`. **Nunca corrió** y no se reprograma solo (D8 del 02-10, que sigue abierto).

### F9. [DATO] La ventana muerta del host es de 9 h 05 min y explica la ráfaga
Última ejecución del 08-10: **22:12:30** (la del propio job KEL, `expr 12 22 * * *`). Primera del 09-10: **07:17:57**. Entre ambas: **9 h 05 min 27 s sin una sola fila** en `executions`. Al volver, el planificador despachó **todos los vencidos a la vez** (`last_dispatch.kind = catch_up`, mismo `dispatched_at` 07:17:56.697):

| job | hora | `lateness_seconds` |
|---|---|---|
| backup-joko-lab-diario | 22:15 | 32.576,7 |
| backup-hermes-diario | 22:20 | 32.276,7 |
| consolidador-sesiones | 22:30 | 31.676,7 |
| Bolsa autónoma — scan EXP-002 | 22:30 | 31.676,7 |
| registrar-hel-diario | 22:35 | 31.376,7 |
| hel-registro-watchdog | 22:45 | 30.776,7 |
| ficha-perfume-diaria | 07:05 | 776,7 (`kind: late`) |

La hora 07 del 09-10 concentra **48 ejecuciones** (frente a ~55/h repartidas en el resto del día).

---

## 3. Aciertos de la ventana (verificables, sin promoción)

- **7 incidencias cerradas**, dos de ellas con recurrencias larguísimas: `da39a2_fae825d0fe36` (**33 días**, rag-reindex timeout) y `264c02_761c7f27bcb0` (**22 días**, telegram-watchdog).
- **La cola de ejecuciones está sana**: 998/1.001 `completed`, **0 `failed`**; los 2 `unknown` son de la ráfaga y 1 `running` es esta corrida.
- **`kel-revalidacion-diaria` recuperado**: `last_status: ok`, `failure_streak: 0`, `on_time` — el KEL vuelve a tener vía automática (F4).
- **Antídoto de CP-012 verificado en las dos direcciones** (F7), sin que el artefacto engañara al veredicto.
- **Producto diario del experimento 001 intacto**: `perfume-del-dia-20261009/` completo pese al `unknown`.
- **Telemetría 7/7**, **informe local 3/3 días con fichero**, **OBS al día**, **artefactos de hoy escritos**.
- **Paso 5 no forzado**: al no ser la 1ª del mes, no se promueve ni se descarta nada de la incubadora (el motor sitúa la mensual en la 1ª corrida de noviembre).

---

## 4. Patrones (paso 3)

- **CP-013 creado en esta misma sesión** (`lpa/pattern-incubator/CP-013-jobs-en-ventana-de-apagado-no-corren-a-su-hora.md`, 8.491 B, TEMPLATE de 7 campos + falsación). Criterio: **7 despachos vencidos** (`catch_up`/`late`) en **una sola ráfaga** y **6 propósitos distintos** (backups ×2, consolidación de sesiones, experimento 002, experimento HEL ×2, ficha de perfume) → 2+ ocurrencias en contextos distintos. Confianza declarada **E0** (una sola noche medida, un solo host). No colisiona: el incubator solo tenía CP-009..CP-012 vivos en ese rango.
- **CP-012 («estado `unknown` se resuelve en el artefacto»)**: era hoy su **fecha de revisión comprometida**. Se aplicó el antídoto a los 2 `unknown` nuevos y **no se dispara su segunda condición de falsación** (el artefacto no engañó en ningún caso) → **sobrevive, sigue incubando** (5 ocurrencias de la ventana anterior + 2 de hoy). Se añaden dos bordes declarados: (a) puede haber **producto sin traza** en el motor; (b) `cron_incidents` **no registró** uno de los dos `unknown`.
- **CP-010 («instrumento no validado miente»)**: **7ª ocurrencia** — el tope de 1.000 filas produce un conteo correcto con **etiqueta temporal falsa** (F3). Mismo mecanismo que la ocurrencia (2) del patrón: un medidor que no mide lo que su etiqueta declara (aquí por diseño, sin ceguera). Se descarta la fusión de CP-012 con CP-010/CP-011: los antídotos siguen distintos.
- **CP-009 / E1-007 («instrumento sin disparador se degrada»)**: reexamen **sin cambio de nivel**. Evidencia nueva: `retrabajo_ledger` 14 días (F5), `lecciones_ledger` que llegó a 7 días congelado y **hoy se descongela** con las 3 lecciones de §5, y el producto diario de `consolidador-sesiones` con 8 noches sin generarse (F1). Todo sigue en el Experimento 004 → **no amplía dominio**.
- **CP-011 («escritura truncada sin fallo»)**: ocurrencia de la **familia** (pérdida silenciosa sin marca) en un instrumento distinto (el tope de filas de `executions`, F3), con mecanismo distinto del truncado por `patch`. Si reaparece en un tercer instrumento, merece CP propio.
- **CP-008** (estado real vs documentado): el caso F8 (job «scheduled» con `next_run_at` en el pasado y `last_run_at: null`) es otra muestra del mismo principio. **8 ocurrencias** acumuladas; sin cambio de estado en esta revisión.
- **CP-001 … CP-007**: sin evidencia nueva en la ventana; sin cambios.

---

## 5. Lecciones registradas (paso 4)

**Canal: el ledger** (`04-operations/metrics/lecciones_ledger.jsonl`, backup previo `.bak-20261009`). **No se ha parcheado ninguna skill**: el paso 4 de la operativa sigue **contradiciendo RULE-018** mientras el usuario no decida (D11 del 02-10, vigente). 3 lecciones nuevas, dominio `proceso`, fechas **2026-10-09 14:38**:

| id | título | tried → causa raíz → fix |
|---|---|---|
| **LEC-20260814-017** | El registro de ejecuciones del cron tiene tope de 1.000 filas: no puede sostener una ventana semanal | Conteo «≥ 7 días» leído como 9 casos → `MAX_TERMINAL_EXECUTIONS = 1000` + poda por `finished_at` → reconstruir la semana con `cron_incidents`/artefactos y citar siempre el rango `claimed_at` |
| **LEC-20260814-018** | Un job programado dentro de la ventana de apagado del host no corre a su hora: corre en el arranque siguiente, todos a la vez | Job nocturno diagnosticado por su hora/status → host apagado 22:12:30→07:17:57, despacho masivo `catch_up` → leer `last_dispatch.kind`/`lateness_seconds` antes de diagnosticar y no programar producto diario en esa ventana |
| **LEC-20260814-019** | El arreglo puede vivir en el lanzador y no en el script: revisar el intérprete antes de tocar el código | `ModuleNotFoundError: No module named 'yaml'` → el `PATH` del cron resolvía a un python empaquetado sin PyYAML desde el 01-oct → fijar intérprete en el lanzador; verificar el cierre en `cron_incidents`, no solo que el job deje de fallar |

Ledger: **16 → 19 filas**. Con estas 3, el instrumento **vuelve a moverse** (mtime pasa de 02-10 14:37 a 09-10 14:38).

---

## 6. Cadena incidente → lección → mejora

| Incidente | Lección | Mejora |
|---|---|---|
| 2 `unknown` en la ráfaga de arranque (F7) | LEC-018 | CP-013 en incubadora + antídoto de CP-012 revalidado; comprobación por artefacto en cada ciclo |
| Ventana «7 días» medida con la cola de 27 h (F3) | LEC-017 | Regla: citar rango `claimed_at` con todo conteo; semana por `cron_incidents` |
| KEL roto 3 días por el `PATH` (F4) | LEC-019 | Fix en el lanzador (04-10); incidencia `closed_at` verificado; propuesta D4 de generalizar |
| `consolidador-sesiones` con 8 noches sin producto (F1) | — (dato, no lección) | Escalado a decisión del usuario (D1); no se toca el job |
| Recordatorio `once` nunca ejecutado (F8) | — (dato + consecuencia usuario) | Reportado en el resumen de esta corrida (D6); no se reprograma solo |
| `retrabajo_ledger` 14 días sin asiento (F5) | (ocurrencia CP-009) | Condición de D4 cumplida → decisión propuesta (D3) |
| `[truncated]` sigue vivo en 3 ficheros (F6) | (ocurrencia CP-011) | Sigue P0 en `pendientes.md`; no se repara sin OK (RULE-018) |

---

## DECISIONES (2026-10-09)

- **D0 — Fuente de incidentes del ciclo.** Se mantiene la D0 del 02-10: el `.md` de incidentes lleva **36 días muerto** y la fuente real es `executions.db` + artefactos. El **patch a la skill `lpa`** (paso 1 → leer ambos; paso 4 → proponer en la acta en vez de escribir skills) **sigue propuesto y sin ejecutar** (RULE-018, D11 del 02-10).
- **D1 — `consolidador-sesiones` (F1).** **No se toca el job ni se re-ejecuta nada.** Se declara el hallazgo más grave de la ventana: **8 noches sin producto** (`sesiones-20260930.jsonl` es el último) con `failure_streak: 8` y la incidencia abierta desde el 01-10. **Requiere decisión del usuario**: reparar la cadena de consolidación de sesiones o aceptar formalmente que ese producto no se genera. Mientras tanto, el ciclo **comprueba el artefacto**, no el estado del job.
- **D2 — `CP-013` promovido a la incubadora en esta misma sesión** (paso 3). Base: 7 despachos vencidos en una ráfaga, 6 propósitos distintos, ventana muerta medida de 9 h 05 min 27 s. Estado `incubating`, confianza **E0**. Primer reexamen: **ciclo del 16-10**.
- **D3 — `retrabajo_ledger` (F5): se ejecuta la condición de la D4 del 02-10.** A los **14 días** sigue en **1 entrada**. Se **propone al usuario** una de dos: (a) fusionarlo con `lecciones_ledger.jsonl`, o (b) darle disparador automático (que un fallo de experimento genere asiento solo). **No se borra, no se fusiona y no se modifica nada sin OK.**
- **D4 — KEL / F6 del 02-10: CERRADA y verificada** (`closed_at` 2026-10-04T19:23:11 + `last_status: ok` + `failure_streak: 0`). Se **propone** (no se ejecuta): generalizar la regla a **todos** los scripts del cron — fijar el intérprete explícitamente en el lanzador en vez de depender del `PATH`, porque el `PATH` cambió solo con un binario del **01-oct** y rompió un script que era correcto.
- **D5 — `[truncated]` (F6): sin reparar.** Sigue en **P0** (`pendientes.md`) y sigue requiriendo OK explícito (RULE-018). Se **propone al usuario** añadir al P0 el **tercer fichero vivo**: `~/.hermes/skills/software-development/perfume-ia/references/capa-lpa-recomendacion.md` (además de `render-html-a-imagen/SKILL.md` y `validacion-instrumentos-medicion/SKILL.md`). **No se ha escrito nada en el backlog**: RULE-018 exige OK también para escribir en el backlog y en la BD. La copia `SKILL.md.bak-20260918` se deja **intacta** (es la única referencia del estado anterior).
- **D6 — Recordatorio `once` (F8): se reporta al usuario, 2º ciclo.** `last_run_at: null`, `next_run_at` en el pasado, `repeat.completed: 1`. **No se reprograma ni se marca como completado automáticamente**; si el usuario quiere el aviso, hay que decidirlo.
- **D7 — Timeouts de 300 s.** **No aparece ningún timeout nuevo** en la ventana (los 3 de la ventana anterior se cerraron). Se mantiene la D7 del 02-10: **no se sube el timeout a ciegas**.
- **D8 — Curador (F2): se mide y se reporta; no se toca.** Sigue `PAUSED` con `last run: 15d ago` y **245 operaciones reales** en la ventana. **No se pausa, no se reanuda y no se tocan skills por mi parte** (RULE-018). Sigue pendiente de decisión del usuario qué skills del lab se pinean (hoy: **11 pinned**).
- **D9 — Sin ascensos ni descartes (paso 5 no aplica).** `KNOWN.md` (8 E1), `HYPOTHESIS.md` y `UNKNOWN.md` **sin cambios**. El `CHANGELOG.md` tampoco se toca: no hay cambio de nivel que registrar. Revisión mensual: **1ª corrida de noviembre**.

---

## 7. Próxima revisión

**Viernes 2026-10-16, 14:30 CEST** (`expr "30 14 * * 5"`, id `05de86a93257`). Comprobaciones mínimas:
1. `executions` no sanos + `cron_incidents` sin resolver (¿sigue abierta `9474f6_807bf8724760`?).
2. **`consolidador-sesiones`: ¿`failure_streak` > 8? ¿aparece algún `sesiones-2026100X.jsonl`?** (F1, D1).
3. `mtime` de `lecciones_ledger.jsonl`, `retrabajo_ledger.jsonl` y `.curator_ledger.jsonl` (D3, F2).
4. `[truncated]` en las 3 skills/references vivas (F6, D5).
5. `hermes curator status` vs filas reales del ledger del día (F2, D8).
6. Recordatorio `once` (`d824bcf4a2ff`): ¿sigue con `last_run_at: null`? (F8, D6).
7. KEL: mantener `kel-revalidacion-diaria` en `ok` + `failure_streak: 0` (F4).
8. **CP-012 y CP-013**: primer reexamen del 013; el 012 ya sobrevivió su fecha comprometida.

---

## 8. Integridad y backups (RULE-008 / RULE-018)

Copias **`.bak-20261009`** creadas **antes** de tocar los ficheros (no se sobrescribió ninguna copia previa; la `.bak-20260814` del ledger se renombró a `-preservado-20261009`):

| fichero | md5 (antes) |
|---|---|
| `CP-009-instrumento-sin-forzado-se-degrada.md.bak-20261009` | `426f1bbda545d0d5c5b489346be80d48` |
| `CP-010-instrumento-no-validado-miente.md.bak-20261009` | `719e44c7fd6a3903c0495e39f40dc39c` |
| `CP-011-escritura-truncada-sin-fallo.md.bak-20261009` | `368dbed43f07dd552338eeeb7291188d` |
| `CP-012-estado-unknown-se-resuelve-en-el-artefacto.md.bak-20261009` | `9fa59c906bad14a53cab72d584f68653` |
| `04-operations/metrics/lecciones_ledger.jsonl.bak-20261009` | (16 filas) |

Estado de los ficheros al cierre de la sesión:

| fichero | md5 |
|---|---|
| `CP-009-…md` | `607c035973d0e457bfe2112d28dd4adc` |
| `CP-010-…md` | `0f574064042dd4a99b6344c6007b9940` |
| `CP-011-…md` | `40a0d9bad3ea07fb1474cf0dae23aeea` |
| `CP-012-…md` | `cf27069cad3bb42676f00824575f479f` |
| `CP-013-…md` (nuevo) | `c5eb7ee8925d7080de07e2d2efc3fc53` |

`git status --porcelain`: **18 entradas** (6 `M` + 12 `??`, incluida esta acta) sin commitear. **No se hace `git add`/`commit`** de los hallazgos sin OK (D12 del 02-10, se mantiene).

---

## Anexo · Instrumentos citados (trazabilidad)

- `~/.hermes/cron/jobs.json` (schedule, `last_status`, `failure_streak`, `last_dispatch.kind`/`lateness_seconds`).
- `~/.hermes/cron/executions.db` → tablas `executions` (1.001 filas; columnas `id, job_id, source, process_id, pid, process_started_at, status, claimed_at, started_at, finished_at, error, handoff_pending, handoff_started_at, delivery_outcome, scheduled_instant, progress_at`) y `cron_incidents` (14 filas) — consulta de solo lectura, `mode=ro`.
- `~/.hermes/hermes-agent/cron/executions.py` (`MAX_TERMINAL_EXECUTIONS`, poda por `finished_at`).
- `~/.hermes/scripts/kel-revalidacion.sh` (mtime 04-oct 19:21) + `~/.hermes/tools/python-3.14.7+20260901-linux-x64/bin/python3` (symlink 2026-10-01 07:09).
- `.curator_ledger.jsonl` (2.139 filas; recuento por día y por actor) y `hermes curator status`.
- `04-operations/metrics/lecciones_ledger.jsonl`, `…/retrabajo_ledger.jsonl`, `…/sesiones/` (`sesiones-*.jsonl`, `resumen-dia-*.md`).
- `lpa/pattern-incubator/CP-009…CP-013`, `lpa/KNOWN.md`.
- `stat -c`, `md5sum`, `grep -rl '\[truncated\]'`, `uptime -s`, `date`, `git status --porcelain`.
