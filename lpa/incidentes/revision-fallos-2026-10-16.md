---
type: lpa
subtype: incidentes
status: active
created: 2026-10-16
ventana: 2026-10-09 → 2026-10-16
---

# REVISIÓN DE FALLOS — 2026-10-16 (ciclo semanal LPA)

- **Fecha real de la corrida:** viernes **2026-10-16**, `date` = **2026-10-16 14:38 CEST**.
- **Motor (cita literal de `~/.hermes/cron/jobs.json`):** `lpa-revision-incidentes-semanal`, id `05de86a93257`, `expr "30 14 * * 5"`; despacho de hoy `scheduled_at 2026-10-16T14:30:00+02:00` / `dispatched_at 2026-10-16T14:30:56.004557+02:00` → **`on_time` (56,0 s)**. En `executions.db` esta corrida es `bf391ca925974cafb739819c87985604`, estado `running`, `claimed_at` 14:30:56, `progress_at` 14:38:04. `next_run_at`: **2026-10-23T14:30:00+02:00**.
- **Ventana revisada:** 2026-10-09 14:41 CEST (cierre del acta anterior) → 2026-10-16 14:38 CEST.
- **Acta anterior:** `revision-fallos-2026-10-09.md` (D0..D12).
- **Paso 5 (revisión mensual) NO aplica:** esta es la **3ª corrida de octubre** (la mensual fue la del 02-10).

---

## 0. Incidentes de la ventana (paso 1)

**No hay ningún `*-incidentes.md` nuevo.** El único fichero con ese sufijo sigue siendo `2026-09-01-incidentes.md` (mtime **2026-09-03 13:38**) → **43 días sin una sola escritura**. Por esa vía no se promueve nada y no se inventa trabajo.

**Fuente real (D0 del acta 02-10, se mantiene):** `~/.hermes/cron/executions.db` (solo lectura, `mode=ro`) + artefactos en disco.

- `cron_incidents`: **19 filas** = **17 `resolved`** + **1 `alerted`** + **1 `detected`**. **2 abiertas:**

| id | job | estado | tipo | `first_seen_at` → `last_seen_at` | `error` (literal, recortado) |
|---|---|---|---|---|---|
| `9474f6_807bf8724760` | `9474f6f3d224` consolidador-sesiones | `detected` | `unknown` | 01-10 22:30:34 → 15-10 22:31:09 (**15 días**) | *«Restart-safe cron worker exited with status -15 after adopting this execution, without writing a durable terminal state; whether side effects ran is unknown.; worker stderr: <frozen runpy>:130: RuntimeWarning: 'cron.scheduler' found in sys.modules…»* |
| `da39a2_563646c13b70` | `da39a2148b34` rag-reindex-daily | `alerted` | `timeout` | 12-10 08:05:44 → 16-10 08:05:58 | *«Script timed out after 300s: /home/jokoalmi/.hermes/scripts/rag-reindex.sh»* |

- **5 incidencias nuevas dentro de la ventana** (por `first_seen_at`):

| id | job | tipo | `first_seen_at` | estado final | `closed_at` |
|---|---|---|---|---|---|
| `da39a2_563646c13b70` | rag-reindex-daily | `timeout` 300 s | 12-10 08:05:44 | **abierta** (`alerted`) | — |
| `67d5fc_dbacfe302a08` | informe-diario-joko-lab | `script` (exit 1) | 15-10 09:01:35 | `resolved` | 16-10 09:02:32 |
| `210486_ede8adb4a5b0` | Orquestador batch diario | `script` | 15-10 12:01:37 | `resolved` | 16-10 12:02:41 |
| `380a80_98511e9854f8` | Orquestador recuperación horaria | `script` | 15-10 13:15:37 | `resolved` | 15-10 15:15:37 |
| `380a80_40b200f10c09` | Orquestador recuperación horaria | `script` | 15-10 14:15:37 | `resolved` | 15-10 15:15:37 |

- **6 incidencias cerradas dentro de la ventana:** `264c02_761c7f27bcb0` (telegram-watchdog, `script`, abierta desde 16-09 → cerrada 13-10 06:13, **27 días**), `da39a2_d27e3eaf34c5` (rag-reindex, `unknown`, 04-10 → 14-10 08:01), y las 4 de la cascada de arriba.
- `executions` (**retención corta**, ver F3): **1.001 filas** con rango **2026-10-15 14:41:35 → 2026-10-16 14:36:56** = **23 h 55 min** → **998 `completed`, 1 `failed`, 1 `unknown`, 1 `running`** (esta corrida). No hay más `failed` en la cola: los anteriores ya fueron podados.
- Las 3 filas no sanas, literales:

| id (execution) | job | estado | `claimed_at` → `finished_at` | `error` (literal, recortado) |
|---|---|---|---|---|
| `a0b9fd49024a4930a54f09fc0eefed27` | `9474f6f3d224` | `unknown` | 15-10 22:30:35.532 → 22:31:09.638 | *Restart-safe cron worker exited with status -15 … whether side effects ran is unknown.* |
| `f4f370b89c76490982f80d73637f374e` | `da39a2148b34` | `failed` | 16-10 08:00:56.112 → 08:06:00.425 | *Script timed out after 300s: /home/jokoalmi/.hermes/scripts/rag-reindex.sh* |
| `bf391ca925974cafb739819c87985604` | `05de86a93257` | `running` | 16-10 14:30:56.106 → — | (esta corrida) |

---

## 1. Actividad de la ventana (contexto verificado)

- **Telemetría:** 14 ficheros para el 09→15-10 = **7/7 días** con `.json` + `.md`.
- **Informe local diario:** `04-operations/reports/20261010-…` … `20261016-informe-local.txt` = **7/7 días** (incluido el 15-10, regenerado a mano; ver F5).
- **Observaciones:** últimas `OBS-202-uso-rag-2026-10-15.md`, `OBS-201-fallback-rate-2026-10-15.md` → al día hasta el **15-10** (la del 16-10 se genera de madrugada).
- **`git status --porcelain`:** **33 entradas** al medir (sube durante el cierre de esta acta). **No se hace `git add`/`commit`** de los hallazgos (D12 del 02-10, se mantiene).
- **`uptime -s` = 2026-10-16 06:07:39** → la caída de la noche fue **reinicio del host**, no suspensión (contexto de F8).
- **Jobs en estado no sano:** solo 2 — `9474f6f3d224` (`last_status: error`, **`failure_streak: 15`**) y `da39a2148b34` (`error`, `streak: 1`). Los otros 8 jobs inspeccionados (incluidos los 3 de la cadena de F5) están en `ok`, `streak 0`.

---

## 2. Fallos y hallazgos de la ventana

### F1. [CIERRE CON CAUSA RAÍZ] `consolidador-sesiones`: la causa era OOM del worker, y el producto ya está reconstruido
`9474f6f3d224`: **`failure_streak: 15`** y la incidencia abierta desde el 01-10. La causa raíz está en el kernel, verbatim: `hermes invoked oom-killer … oom_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/hermes-worker-cron-9474f6f3d224-exec-a0b9fd49024a4930a54f09fc0eefed27.scope … Killed process 1490413 (hermes) total-vm:5725872kB, anon-rss:4057072kB`. El job moría **por encima del cgroup de 4 GiB** al exportar todas las sesiones (`hermes sessions export`: MAXRSS 11,3 GB, 1.173 MB escritos/día). El síntoma acumulado: **15 noches sin producto ni informe** (`~/.hermes/cron/output/9474f6f3d224/`: 47 ficheros, el último del **30-09 22:31:54**). Mitigación desplegada el 16-10 06:58-07:12, **no por este ciclo**: 46 dumps comprimidos (15,98 GB → 2,51 GB, ratio 6,4×, 94,4 s, 0 fallos, md5 original == md5 de `zstd -dc` antes de borrar) y `consolidador_sesiones.py` reescrito (delta `--newer-than 3d`, **MAXRSS 11,3 GB → 526 MB**), con regeneración manual del producto del 15-10 (`resumen-dia-2026-10-15.md`, 07:03). **Verificación: pendiente la corrida automática de hoy 22:30** → primera prueba real del arreglo (D5).

### F2. [RECURRENCIA, 5º ciclo] El curador escribe a diario con el estado diciendo PAUSED
`hermes curator status` (literal): **`curator: PAUSED`**, `runs: 13`, **`last run: 22d ago`**, `last report: ~/.hermes/logs/curator/20260923-170843`, `consolidate: off`. Frente a eso, `.curator_ledger.jsonl` tiene **2.203 filas** (1.667 `curator` + 536 `agent`) y registra **64 filas en la ventana** (11-10: 35 · 12-10: 9 · 13-10: 4 · 15-10: 3 · 16-10: 13); última fila `2026-10-16T08:39:01.417998+00:00` (`patch` sobre `seguimiento-empleo`). El medidor declarado llevaba 22 días sin correr y el ledger real no paró ningún día.

### F3. [RECURRENCIA, 3er ciclo] El registro de ejecuciones no puede sostener una ventana semanal: tope de 1.000 filas
1.001 filas que abarcan **23 h 55 min** (09-10: eran 27 h). Consecuencia operativa, ya asumida: en `executions` **no se cuenta nada «de la semana»**; la ventana se reconstruye con `cron_incidents` + artefactos + actas + el tramo de `executions` disponible.

### F4. [NUEVO] `rag-reindex-daily`: la incidencia se cerró tras 33 días y reapareció con la misma firma 4 días después
`da39a2_fae825d0fe36` (`timeout` 300 s) se **cerró el 08-10** después de **33 días** abierta; el 12-10 aparece `da39a2_563646c13b70` con **la misma firma** (`timeout` 300 s sobre `rag-reindex.sh`) y sigue **abierta** (`alerted`, `last_seen_at` 16-10 08:05:58; la corrida de hoy acabó `failed` a las 08:06:00). El `resolved` mide «hubo una corrida sana después», no «la causa está reparada». Existe red de seguridad: `rag-reindex-catchup` (`174499853a8b`, `every 60m`) está en `ok` — el índice no está parado, pero la corrida diaria no cabe en 300 s.

### F5. [CIERRE VERIFICADO] La cascada del informe diario del 15-10: 1 causa → 4 filas de incidencia en 3 jobs
Una sola causa (bug del productor: `informe-diario-local.sh: línea 60: $2: variable sin asignar`, con `⚠️ resumen inválido → degradado`) generó la fila del productor **y** tres filas en dos jobs consumidores, todas con el texto *«orquestador-batch: FALLO (fuente_ausente: no existe …/20261015-informe-local.txt) en 'informe-json'»* — **ningún job de orquestación estaba roto**. Arreglo del productor el 15-10 15:47, producto regenerado 15:49. **Cierre verificado hoy:** las 4 filas están `resolved` y los 3 jobs de la cadena en `last_status: ok`, `streak 0`, **sin haber sido tocados**. Origen del patrón **CP-014** (nuevo, D2).

### F6. [RECURRENCIA, 3er ciclo] `retrabajo_ledger.jsonl` lleva 21 días congelado
**566 B, mtime 25-09** (eran 14 días el 09-10). La fecha de evaluación fijada en el acta del 09-10 sigue sin ejecutarse y el instrumento no se ha movido solo. **Contraste medido el mismo día:** el productor del informe diario (con consumidores que se quejan cada hora) se arregló y se verificó en horas; el ledger, sin consumidor, sigue muerto. D6.

### F7. [RECURRENCIA, 3er ciclo] `[truncated]` en 4 ficheros de skills
3 ficheros vivos + 1 `.bak-20250726`. No rompe ejecución, pero es el mismo hallazgo declarado tres ciclos seguidos. D9.

### F8. [NUEVO · CP-013, 2ª noche medida] Ventana muerta de 6 h 18 min 49 s y ráfaga de 10 jobs sin un solo `unknown`
Última ejecución del 15-10: `2026-10-15T23:50:07.180312+02:00` → primera del 16-10: `2026-10-16T06:08:56.397293+02:00` = **6 h 18 min 49 s** muertas. `uptime -s` = **2026-10-16 06:07:39** → **reinicio del host** (77 s antes de la primera corrida), no suspensión. La ráfaga de arranque son **10 jobs** entre `06:08:56.397293` y `06:08:56.734307` = **337 ms**, todos `completed` (el 09-10 hubo 2 `unknown`; esta vez ninguno). Hallazgo nuevo: **la composición de la ráfaga depende de la hora del apagado** — el 15-10 el host cayó a las 23:50, después de los jobs diarios de 22:15-22:35 (113 filas en `executions` entre 22:00 y 23:59), así que la ráfaga contiene **solo jobs de intervalo**. CP-013 no se falsa y suma su 2ª noche medida.

### F9. [NUEVO · borde de instrumento] La evidencia directa de CP-013 (`last_dispatch`) es efímera
Medido hoy a las 14:38, 8 h después del arranque: **0 filas** con `last_dispatch.kind != 'on_time'` y **0** con `lateness_seconds > 600`, pese a la ráfaga de las 06:08. El campo se sobrescribe en el siguiente despacho y los 10 jobs de la ráfaga son de intervalo (`every 60m`), así que ya habían vuelto al calendario. La ventana muerta **sí** es medible, pero con `executions.claimed_at` por hora + `uptime -s`. No invalida CP-013: invalida una de las dos formas de medirlo (LEC-021, D11).

### F10. [NUEVO · punto ciego] El vigía que lee informes es ciego a la corrida que muere antes de escribir, y era clasificador de un falso ok
Dos caras del mismo sesgo, ambas medidas: (a) **15 corridas sin informe** (F1) invisibles para el vigía de informes, porque su señal es el informe y el OOM mata la corrida antes de escribirlo; el hueco fue registrado por el usuario en `pendientes.md` el **16-10 07:36:35** como «PUNTO CIEGO 3»; (b) **falso ok**: los dos informes fallidos del 15-10 (`cron/output/67d5fcc5b69e/2026-10-15_09-01-35.md`, 363 B, y `cron/output/210486645f20/2026-10-15_12-01-37.md`, 359 B, ambos con `**Status:** script failed`) **pasaron como ok** en el barrido de las 12:00:37 del 15-10, porque el script reconocía otras dos señales. Arreglado el **16-10 07:48** (3ª señal + `CABECERA` 200→600 B). Origen del patrón **CP-015** (nuevo, D3). **El hueco (a) NO queda cerrado** con ese arreglo.

---

## 3. Aciertos de la ventana

- **7/7 días** de telemetría y de informes locales; observaciones al día hasta el 15-10.
- **Cierre verificado** de la cascada del informe diario (F5): 4 filas cerradas, 3 jobs en `ok`, sin tocar ningún consumidor.
- **Causa raíz real identificada** para el consolidador (OOM, no «worker reiniciado») y **producto reconstruido** el mismo día, con datos verificados por md5 antes de comprimir (F1).
- **CP-012 y CP-013 reexaminados con evidencia nueva** y sin falsación: CP-012 gana un borde (un `unknown` que tapa un fallo real, no un reinicio) y CP-013 su 2ª noche medida.
- **El laboratorio archivó sin borrar:** 46 dumps comprimidos con verificación md5, y se documentó que no eran copias redundantes (47 ids del dump del 31-jul no aparecen en el del 30-sep) → `/` pasó de 107 a 120 GB libres.
- **2 patrones nuevos promovidos con condición de falsación** (CP-014, CP-015) en la misma sesión, tras 4 ciclos sin ascensos.

---

## 4. Patrones (paso 3)

| patrón | ocurrencias en la ventana | decisión |
|---|---|---|
| **CP-014** (nuevo) «El fallo de una cadena de jobs se registra en el consumidor» | 4 filas / 3 jobs / **1 evento raíz** | **Promovido a incubación**, E0. Revisión 23-10 y 02-11 |
| **CP-015** (nuevo) «La corrida que muere sin artefacto no deja señal» | 3 (15 corridas sin informe + 2 falsos ok + punto ciego registrado) | **Promovido a incubación**, E0. Revisión 23-10 y 02-11 |
| CP-013 (incubando) | 10 jobs desplazados en 1 ráfaga + 6 h 18 min 49 s de ventana muerta | **Sobrevive** (2ª noche medida, sin falsación). Se corrige cómo se mide (D11) |
| CP-012 (incubando) | 1 `unknown` resuelto en el artefacto (efectos NO, correcto) | **Sobrevive**, sin falsación. Borde nuevo: el `unknown` tapaba un fallo real (OOM) |
| CP-010 (**E1-008**, en KNOWN) | 7ª: curador PAUSED 22d vs 64 filas reales · 8ª: `resolved` = 17/19 con reapertura a los 4 días | **Sin cambio de nivel.** Amplía familia de instrumento, no dominio |
| CP-009 (**E1-007**, en KNOWN) | retrabajo 21 días · lecciones 7 días congeladas · 4 `[truncated]` · streak 15 | **Sin cambio de nivel** (3er ciclo) |
| CP-011 (incubando) | — (el `[truncated]` sigue sin tocarse) | Sin ocurrencia nueva |

**Ningún ascenso a `KNOWN.md`/`HYPOTHESIS.md` este ciclo** (paso 5 no aplica y las condiciones de ascenso de CP-012/CP-013 —segundo host/experimento— siguen sin cumplirse).

---

## 5. Lecciones registradas (paso 4)

3 lecciones nuevas en `04-operations/metrics/lecciones_ledger.jsonl` (**dominio `proceso`**), tras 7 días congelado el ledger:

| id | título | ref |
|---|---|---|
| `LEC-20260814-020` | Un fallo en cadena se registra a nombre del consumidor: contar causas, no filas | `cron_incidents` (4 filas, 15-10) · CP-014 |
| `LEC-20260814-021` | La evidencia de `catch_up` en `last_dispatch` es efímera: la ventana muerta se mide con `executions` | `executions` 15-10 23:50:07 → 16-10 06:08:56 · CP-013 |
| `LEC-20260814-022` | Antes de comprimir o renombrar un producto de datos, buscar sus consumidores por nombre | `verificar_hel.py:60`, `registrar_hel_diario.py:145` · CP-015 |

**No se ha tocado ninguna skill por patch en este ciclo:** las 3 lecciones son de proceso/instrumentación del lab y ya tienen su sitio en el ledger + los CP. Las skills afectadas (`hermes-cron-jobs`) documentan procedimientos que este ciclo **no cambia**: el barrido ya fue corregido por el usuario hoy y se verificó leyendo el script, no ejecutándolo.

---

## 6. Cadena incidente → lección → mejora

| incidente | lección | mejora aplicada | estado |
|---|---|---|---|
| Cascada 15-10 (4 filas, 3 jobs) | **LEC-020** | Diagnosticar aguas arriba + contar causas, no filas → **CP-014** | Cerrado y verificado (F5) |
| 10 jobs desplazados en 337 ms, invisibles en `last_dispatch` | **LEC-021** | Medir con `executions` por hora + `uptime -s` (aplicado en esta acta) → CP-013 §reexamen | Aplicado |
| 46 dumps comprimidos → 2 consumidores leen por nombre | **LEC-022** | `grep` de consumidores antes de archivar → CP-015 | Documentado (ninguno en cron) |
| `consolidador-sesiones` 15 noches sin producto (OOM) | — (ya en CP-009) | Compresión + script reescrito (MAXRSS 11,3 GB → 526 MB) | **Pendiente de verificación** (hoy 22:30) |
| `rag-reindex-daily` reapertura a los 4 días | — | Red de seguridad activa (`rag-reindex-catchup` `ok`) | **Abierto** (`alerted`) |
| Vigía de informes: corrida sin artefacto + falso ok | — | 3ª señal del barrido (16-10 07:48) | **Parcial:** el falso ok está arreglado; el hueco «sin informe» sigue abierto → **CP-015** + D4 |

---

## DECISIONES (2026-10-16)

- **D0 [MANTENER]** Fuente real de la revisión = `executions.db` (solo lectura) + artefactos en disco. El registro declarado `*-incidentes.md` lleva **43 días** sin una sola escritura y no se usa como fuente.
- **D1 [CERRADO Y VERIFICADO]** F5 (cascada del informe diario del 15-10): arreglo del productor 15-10 15:47, producto regenerado 15:49; hoy, **4 filas `resolved`** y los 3 jobs en `ok`/`streak 0` **sin tocar consumidores**. Sin acción pendiente.
- **D2 [NUEVO]** Promover **CP-014** (el fallo de una cadena se registra en el consumidor) a `lpa/pattern-incubator/`, con 7 campos y condición de falsación; E0 por proceder de **un solo evento raíz**; revisión **23-10** y **02-11**.
- **D3 [NUEVO]** Promover **CP-015** (la corrida que muere sin artefacto no deja señal) a incubación, con falsación; revisión **23-10** y **02-11**. Relación declarada con CP-012 (su límite) y CP-010 (misma familia de instrumento).
- **D4 [ABIERTO, fecha tope 23-10]** Cerrar el hueco estructural del vigía de informes (corrida que muere antes de escribir). El arreglo del **falso ok** (3ª señal del barrido, 16-10 07:48) se acepta; el hueco exige **cruzar una segunda fuente** (`failure_streak`/`last_run_at` de `jobs.json` y filas no sanas de `executions`). Toca `~/.hermes/scripts/watchdog-informes-cron.py` → **no se ejecuta sin autorización explícita**; queda anotado en `pendientes.md`.
- **D5 [VERIFICACIÓN PENDIENTE HOY 22:30]** `consolidador-sesiones`: el arreglo (compresión + `consolidador_sesiones.py`, MAXRSS 11,3 GB → 526 MB) **no se da por bueno hasta la corrida automática de esta noche**. Criterio de cierre de la incidencia `9474f6_807bf8724760`: producto del 16-10 en disco **y** `failure_streak` = 0. Si vuelve a morir por OOM: acotar el delta o subir el cgroup del worker — **no tocar el host**.
- **D6 [MANTENER, 3er ciclo · decisión del usuario]** `retrabajo_ledger.jsonl` 21 días congelado. Opciones, sin ejecutar ninguna: (a) darle disparador automático, (b) declararlo no-instrumento y retirarlo, (c) fijar fecha tope. **Fecha tope propuesta: 23-10.**
- **D7 [MANTENER]** `lecciones_ledger.jsonl` se descongela hoy con LEC-…-020..022. Su disparador real sigue siendo este ciclo: **si una ventana no produce lecciones, no se rellena**.
- **D8 [MANTENER]** El curador sigue `PAUSED` (22 días) mientras su ledger real registra 64 filas semanales. **No se reactiva** sin decisión explícita del usuario (CP-010, E1-008).
- **D9 [MANTENER, 3er ciclo]** `[truncated]` en 4 ficheros de skills: declarado, no resuelto (no rompe ejecución).
- **D10 [MANTENER, 3er ciclo]** El tope de 1.000 filas de `executions` deja **23 h 55 min** de histórico: no se cuenta «la semana» ahí.
- **D11 [NUEVO · instrumento]** Sustituir la medición de CP-013: `last_dispatch` solo vale dentro de la ventana del job; el histórico se mide con `executions` por hora + `uptime -s`. **Aplicado ya en esta acta.**
- **D12 [MANTENER]** No se hace `git add`/`commit` de los hallazgos (D12 del 02-10).
- **D13 [NUEVO · EJECUTADO]** Añadidos a `pendientes.md` los puntos abiertos de esta ventana como **3 pendientes con fecha tope 2026-10-23** (vigía de informes: separando el falso ok ya cerrado del hueco aún abierto · `rag-reindex-daily` reabierto · `retrabajo_ledger` congelado) + la verificación pendiente de hoy 22:30. Escritura medida: `04-operations/backlogs/pendientes.md` **312.519 → 315.513 B** (1.348 → 1.354 líneas, bloque de 2.993 B + 1 B de separador); backup `pendientes.md.bak-lpa-revision-20261016` (312.519 B, md5 `6d7ce2e42191a87f82fbea90fe694ca2` == estado previo); original intacto byte a byte (`head -c 312519 | cmp`), `grep -c LPA-REV-20261016` = 1, 0 marcadores de formato sin interpolar.

---

## 7. Próxima revisión

**Viernes 2026-10-23, 14:30 CEST** (`next_run_at` literal: `2026-10-23T14:30:00+02:00`). Prioridades: (1) **verificar la corrida del consolidador de hoy 22:30** (D5) y el cierre de `9474f6_807bf8724760`; (2) comprobar si `rag-reindex-daily` sigue abriendo `timeout` (F4) o ya tiene un arreglo; (3) buscar el **segundo evento raíz** de CP-014 (sin él, no sube de E0); (4) reexamen semanal de CP-012/CP-013/CP-015. La **mensual** (paso 5, revisión del incubator → `KNOWN.md`/`HYPOTHESIS.md`) es la 1ª corrida de noviembre.

---

## 8. Integridad y backups (RULE-008)

Backups `.bak-20261016` creados **antes** de tocar nada (14:37):

- `lpa/pattern-incubator/CP-009-instrumento-sin-forzado-se-degrada.md` → 14.588 B
- `lpa/pattern-incubator/CP-010-instrumento-no-validado-miente.md` → 12.428 B
- `lpa/pattern-incubator/CP-012-estado-unknown-se-resuelve-en-el-artefacto.md` → 9.804 B
- `lpa/pattern-incubator/CP-013-jobs-en-ventana-de-apagado-no-corren-a-su-hora.md` → 8.491 B
- `04-operations/metrics/lecciones_ledger.jsonl` → 17.013 B (19 filas → 22 tras las 3 de hoy)
- `04-operations/backlogs/pendientes.md` → 312.519 B (`pendientes.md.bak-lpa-revision-20261016`, md5 == estado previo) antes de anexar D13

Ficheros **nuevos** (sin backup, no existían): `CP-014-fallo-en-cadena-se-registra-en-el-consumidor.md`, `CP-015-la-corrida-que-muere-sin-artefacto-no-deja-senal.md`, esta acta.

**No se ha ejecutado ningún comando que cambie el sistema**: no se ha parado, reiniciado, recreado ni actualizado ningún contenedor o servicio; no se ha tocado `n8n`, ni `/mnt/ssd_ia_datos/*`, ni ninguna skill. Todas las consultas a `executions.db` fueron en modo lectura (`mode=ro`).

---

## Anexo · literal vs resumen

- **Citas literales usadas:** textos de `cron_incidents` y `executions` de §0; `curator: PAUSED / runs: 13 / last run: 22d ago` (§F2); `oom_memcg=…hermes-worker-cron-9474f6f3d224-exec-…scope` y `anon-rss:4057072kB` (§F1); `informe-diario-local.sh: línea 60: $2: variable sin asignar` (§F5); `Script timed out after 300s: /home/jokoalmi/.hermes/scripts/rag-reindex.sh` (§F4).
- **Lo que NO aparece en la salida y por tanto no se afirma:** el número y la naturaleza de las incidencias **futuras**; el resultado de la corrida del consolidador de esta noche (aún no ejecutada); si el arreglo del barrido (3ª señal) funciona en una noche real con fallo (no se ha ejecutado desde el 16-10 07:48); el número total de puntos ciegos previos (en `pendientes.md` solo aparece con esa etiqueta literal la entrada «PUNTO CIEGO 3»).
- **Correcciones a actas anteriores:** F3 refina (no contradice) la nota de retención del acta del 09-10: la ventana útil de `executions` es incluso más corta (23 h 55 min frente a 27 h).

---
*Acta generada por el ciclo semanal LPA (`lpa-revision-incidentes-semanal`, 05de86a93257). Próxima: 2026-10-23.*
