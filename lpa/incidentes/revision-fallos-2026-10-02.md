---
type: lpa
subtype: incidentes
status: active
created: 2026-10-02
ventana: 2026-09-25 → 2026-10-02
---

# REVISIÓN DE FALLOS — 2026-10-02 (ciclo semanal LPA · incluye revisión mensual del incubator)

- **Fecha real de la corrida:** viernes **2026-10-02**, despachada a las **14:30:55 CEST** (`date` = 2026-10-02 14:31:09 CEST; `executions.db` → id de este job `05de86a93257`, estado `running`).
- **Motor (cita literal de `~/.hermes/cron/jobs.json`):** `lpa-revision-incidentes-semanal`, id `05de86a93257`, `expr "30 14 * * 5"`; despacho de hoy `scheduled_at 2026-10-02T12:30:00+00:00` / `dispatched_at 2026-10-02T12:30:55Z` → **`on_time` (55,8 s)**.
- **Ventana revisada:** 2026-09-25 14:35 CEST (mtime del acta anterior) → 2026-10-02 14:31 CEST.
- **Acta anterior:** `revision-fallos-2026-09-25.md` (D0..D9).
- **Esta acta es también la revisión MENSUAL** del incubator (paso 5): el motor sitúa la primera corrida de octubre HOY (D9 del acta 25-09), no el 01-10. Ver §8.

---

## 0. Incidentes de la ventana (paso 1)

**No hay ningún `*-incidentes.md` nuevo.** El único fichero con ese sufijo sigue siendo `2026-09-01-incidentes.md` (8.988 B, mtime 2026-09-03 13:38) → **31 días sin una sola escritura**. Por esa vía no se promueve nada y no se inventa trabajo.

**Sí hay incidentes reales de la ventana, y están en otro registro del que el ciclo no tira.** Medido en solo lectura sobre `~/.hermes/cron/executions.db`:

- `cron_incidents`: **13 incidencias** en total (7 `resolved`, 4 `alerted`, 2 `detected`).
- `executions` con `claimed_at >= 2026-09-25`: **1.001 filas** → `completed` 991, **`unknown` 5**, **`failed` 4**, `running` 1 (esta corrida). Es decir: **9 ejecuciones sin estado terminal sano en 7 días**.

Listado literal de los 9 (job, hora de reclamo, estado, `error`):

1. `d824bcf4a2ff` — Recordatorio publicar L5 (1-oct) — 01-10 09:00:29 — `unknown` — *"Scheduler restarted after this execution's owner exited before a durable terminal state; whether side effects ran is unknown."*
2. `4d64ff821685` — vigilar-canales-ig — 01-10 13:30:51 — `unknown` — mismo literal.
3. `1d06754e7c9a` — Entrenador emocional diario 22:00 — 01-10 22:00:16 — `unknown` — *"Restart-safe cron worker exited with status -15 after adopting this execution, without writing a durable terminal state; whether side effects ran is unknown."* (+ `RuntimeWarning: 'cron.scheduler' found in sys.modules after import of package 'cron'`)
4. `abffcc12711c` — kel-revalidacion-diaria — 01-10 22:12:15 — `failed` — *"Script exited with code 1 … File "/home/jokoalmi/joko-lab/tools/revalidar_kos.py", line 35, in <module> import yaml → ModuleNotFoundError: No module named 'yaml'"*
5. `9474f6f3d224` — consolidador-sesiones — 01-10 22:30:15 — `unknown` — literal del punto 3.
6. `3d18a82cfd79` — Bolsa autonoma scan EXP-002 — 01-10 22:30:16 — `unknown` — literal del punto 3.
7. `67d5fcc5b69e` — informe-diario-joko-lab — 02-10 09:19:54 — `failed` — *"Script timed out after 300s: /home/jokoalmi/.hermes/scripts/informe-diario-local.sh"*
8. `da39a2148b34` — rag-reindex-daily — 02-10 09:19:54 — `failed` — *"Script timed out after 300s: …/rag-reindex.sh"* (incidencia `alerted` con `first_seen_at 2026-09-05T08:05:25` → **27 días de recurrencia**)
9. `174499853a8b` — rag-reindex-catchup — 02-10 09:19:54 — `failed` — *"Script timed out after 300s: …/rag-catchup.sh"* (resuelta 02-10 10:26:46)

---

## 1. Actividad de la ventana (contexto verificado)

- **Commit del repo del lab:** `git status --porcelain` → **0 ficheros sin commitear** (el 25-09 eran 23). El hallazgo P0 de la ventana anterior está cerrado.
- **Telemetría:** 7/7 días presentes (25, 26, 27, 28, 29, 30-09, 01-10) a las 22:00 → el instrumento dispara sin depender de memoria.
- **Observaciones:** hasta `OBS-160`; los tres diarios (`decisiones-por-politica`, `fallback-rate`, `uso-rag`) se escriben cada día, incluido el 01-10 22:00.
- **Sesiones (productos del `consolidador`):** `sesiones-20260925/26/28/29/30.jsonl` presentes; **falta `sesiones-20261001.jsonl`**; `resumen-dia` hasta `2026-09-29`.
- **Informe diario:** `20261002-informe-local.txt` **existe** (mtime 02-10 14:13) pese al timeout de las 09:19 → regenerado después del reinicio.
- **Arranque de la máquina:** `uptime -s` = `2026-10-02 09:56:48`. La ventana previa al arranque explica los despachos tardíos (ver F7).
- **Curador de skills (medido en `.curator_ledger.jsonl`):** filas por día 25-09…02-10 = **171, 80, 74, 57, 90, 112, 83, 36** = **703 operaciones en 7 días**; última fila `2026-10-02T12:16:38Z` (actor `curator`, patch sobre `hermes-cron-jobs`), es decir **14 min antes de esta corrida**. `hermes curator status` responde a la vez: `curator: PAUSED; last run: 8d ago` (ver F2).
- **Bloques truncados:** siguen ahí los 2 de la ventana anterior; uno de ellos **sobrevivió a una reescritura del fichero de hoy** (ver F5).

---

## 2. Fallos y hallazgos de la ventana

### F1. [RECURRENCIA, 3er ciclo] `consolidador-sesiones`: ni producto ni verdad — ahora el motor admite que no sabe

El 25-09 el hallazgo fue «despachado a tiempo (`on_time`) y sin producto». Hoy el registro dice más: la ejecución del **01-10 22:30 quedó `unknown`** (*restart-safe worker exited with status -15*), el motor no escribió estado terminal y el producto **no existe** (`sesiones-20261001.jsonl` ausente; `resumen-dia` parado en el 29-09).

**Dato nuevo y relevante:** el estado del motor no resuelve la duda, pero **el artefacto sí**. Comprobado: no hay sesiones del 01-10 → los efectos no ocurrieron. Es exactamente el antídoto que faltaba (ver CP-012).

### F2. [RECURRENCIA, 3er ciclo] El curador escribe 703 operaciones en 7 días con el comando de estado diciendo PAUSED

Medido hoy, literal:

- `hermes curator status` → `curator: PAUSED` / `last run: 8d ago` / intervalo 7d / **98 skills curator-managed (69 activas / 29 stale)**.
- `.curator_ledger.jsonl` → **703 filas con fecha ≥ 25-09** (171/80/74/57/90/112/83/36), última **hoy 14:16:38 CEST**, coincidiendo con `joko-lab/validacion-instrumentos-medicion/SKILL.md` (mtime **02-10 14:16:16**, 66.857 B).

Es decir: el instrumento de estado y el registro de actividad **vuelven a discrepar**, y esta vez de forma sostenida (8 días seguidos). Y el bloque `[truncated]` de ese mismo fichero **ha sobrevivido a la reescritura** (F5). RULE-018 ya tiene la explicación medida: `pause` no detiene el pase; el corte efectivo es la propiedad de la skill (`created_by`) y `pin`.

### F3. [RECURRENCIA, 2º ciclo] `lecciones_ledger.jsonl` congelado: 12 líneas, mtime 25-09 14:37 → 7 días sin crecer

El registro declarado de lecciones sigue parado desde la última acta (LEC-…-012). La causa no es «no hay lecciones»: en esta misma acta se registran **4** que estaban sin escribir. Tercera ocurrencia del mismo mecanismo (≤ 18-09, 25-09, 02-10).

### F4. [RECURRENCIA, 2º ciclo] `retrabajo_ledger.jsonl`: 1 entrada (25-09), 7 días sin movimiento

Instrumento de experimento sin disparador. El argumento del 25-09 («un evento, no un instrumento muerto») queda debilitado: sigue en 1 con una ventana entera por delante.

### F5. [RECURRENCIA, 3er ciclo] D8 sigue SIN ejecutar: el truncado sobrevive a la reescritura del fichero

| fichero | línea | longitud de la línea | final literal | mtime |
|---|---|---|---|---|
| `render-html-a-imagen/SKILL.md` | 128 | 1.838 | `…la pregunta al visor debe NOMBRAR los modos de fallo (texto cortado, solapado, fuera de lienzo, ilegible, desce...[truncated]` | 30-09 11:21 (42.170 B) |
| `joko-lab/validacion-instrumentos-medicion/SKILL.md` | 36 | 2.873 | `…Un **cero o lista vacía de tu propio extractor** tampoco e...[truncated]` | **02-10 14:16** (66.857 B) |

Ambos bloques cortan a mitad de frase y la línea siguiente ya es otro punto (no hay continuación). El segundo fichero ha sido **reescrito por el curador 3 h después de empezar la ventana** y el marcador sigue dentro → el daño **se hereda edición tras edición**. No se ha reparado porque el contenido perdido no está en las copias (`.bak-20260918` también lo tiene) y **RULE-018 prohíbe a un proceso de fondo escribir contenido de skills sin OK explícito** (ver D5 y D11). `~/.hermes/skills/` **no es un repo git** (comprobado) → no hay vía de recuperación por historial.

### F6. [NUEVO] El KEL dejó de revalidar: `import yaml` roto en `tools/revalidar_kos.py`

`kel-revalidacion-diaria` (22:12 diario, `kel-revalidacion.sh` → `tools/revalidar_kos.py`) falla con `ModuleNotFoundError: No module named 'yaml'` en la línea 35. Es la **máquina de estados OBS→DEC→REVALIDAR→RETIRAR** del programa LPA: sin ella, ninguna KO se revalida por vía automática. `cron_incidents` lo sitúa como `first_seen 2026-10-01T22:12:17`, `state: alerted`, sin `acked_at`.

### F7. [DATO] La guarda de 300 s convirtió una ventana perdida en «fallo del script»

Los tres timeouts del 02-10 no son (solo) un problema de los scripts: `last_dispatch` de ese día dice `dispatched_at 09:19:53` con **`lateness_seconds` 1.193,7 (informe, programado a las 09:00) y 4.793,7 (rag-reindex, programado a las 08:00)**, `kind: late`; el arranque medido es `2026-10-02 09:56:48` y el informe se regeneró a las 14:13. Leer `lateness_seconds` **antes** de culpar al script cambia el diagnóstico (y el fix).

### F8. [NUEVO, con consecuencia para el usuario] El recordatorio `once` del 01-10 quedó en `unknown`

`Recordatorio publicar L5 (1-oct)`, `kind: once`, `run_at 2026-10-01T09:00:00+02:00` → ejecución `unknown` (reinicio del planificador). Un `once` que no corre **no tiene reprogramación**: la ventana se perdió y no se puede saber por el motor si el aviso salió o no. Es el caso que más justifica el antídoto «mirar el artefacto» (aquí: si el aviso está en el chat o no).

### F9. [DATO] El Experimento 002 (bolsa) perdió el scan del 01-10

`Bolsa autonoma - scan diario EXP-002` (`30 22 * * 1-5`) quedó `unknown` a las 22:30. Barrido de artefactos de 01-10 21:00 → 02-10 00:30: solo telemetría/OBS/lancedb de las 22:00 → **no hay producto de scan**. Día perdido del experimento, y tampoco está anotado en `retrabajo_ledger.jsonl` (1 entrada, F4): **el fallo de un experimento no genera retrabajo registrado**.

---

## 3. Aciertos de la ventana (verificables, sin promoción)

- **A1.** Repo limpio: `git status --porcelain` = 0 (25-09: 23 ficheros). P0 cerrado.
- **A2.** Telemetría 7/7 días; los 3 OBS diarios también (hasta OBS-160).
- **A3.** El informe diario del 02-10 se regeneró (14:13) pese al timeout: la pérdida no se quedó como «normal».
- **A4.** El lab **se autocorrigió una fecha mal medida**: los commits de `modelo cleanup` (12→10 modelos) y `router IA v3` incluyen la rectificación de las fechas de verificación declaradas antes. Es el mecanismo de RULE-012 funcionando sobre el propio registro.
- **A5.** RULE-018 **se aplicó** en el momento del hallazgo del 30-09: medir → parar → reportar, sin duplicar la regla en la skill. La regla nació de un incidente y se está usando como regla, no como texto.

---

## 4. Patrones (paso 3)

- **CP-012 [NUEVO, promovido a la incubadora hoy]** — *«El estado `unknown` del motor no se resuelve en el motor: se resuelve en el artefacto»*. 5 ejecuciones `unknown` en **5 jobs distintos con 5 propósitos distintos** (recordatorio `once`, vigilancia IG, entrenador emocional, scan de bolsa, consolidador de sesiones) en una sola jornada (01-10), disparadas por 3 reinicios del planificador (09:00, 13:30, 22:00+). Fichero: `pattern-incubator/CP-012-estado-unknown-se-resuelve-en-el-artefacto.md` (TEMPLATE con los 7 campos, incluida condición de falsación).
- **CP-009** («instrumento sin disparador se degrada») → **ampliado a 9 ocurrencias**: F3 (+7 días congelado), F4 (+7 días en 1 entrada), el registro de incidentes declarado (31 días muerto frente a `cron_incidents` con 13), D8 sin ejecutar 3 semanas, y el informe/`resumen-dia` ausentes. **Candidato a E1 → ascenso ejecutado en §8.**
- **CP-010** («instrumento no validado miente») → **ampliado**: el 5º dominio llega con F2 sostenido 8 días (estado `PAUSED` vs 703 operaciones reales). **Ascenso ejecutado en §8.**
- **CP-008** («estado real vs documentado») → **una ocurrencia nueva** (doc: revisión semanal «lunes»/`hermes curator status`; realidad: motor viernes 14:30 ya citado en D9 del 25-09 + 703 ops con PAUSED). Sigue incubando: su antídoto (muestreo periódico documento↔fuente) es distinto del de CP-009 (disparador) y del de CP-010 (etiqueta de validez) → **no se fusiona**.
- **CP-011** («escritura truncada sin fallo») → **una ocurrencia nueva y más fuerte**: el bloque truncado **sobrevive a la reescritura** del fichero (02-10 14:16) y D8 lleva 3 semanas sin ejecutar. Sigue incubando; **no se fusiona con CP-010** (antídoto distinto: comprobación de tamaño/cola al escribir vs etiqueta de validez del número).
- **CP-001 … CP-007**: sin evidencia nueva en la ventana → siguen incubando sin cambios (§8).

---

## 5. Lecciones registradas (paso 4)

Registradas en `04-operations/metrics/lecciones_ledger.jsonl` con `tools/registrar_leccion.py add` (`LEC-20260814-013` … `-016`, fecha de registro 2026-10-02 14:37). El script sí hace backup RULE-008 antes de escribir (verificado en su línea 38-41) — **con una pega medida: el sufijo está hardcodeado (`.bak-20260814`), así que cada escritura sobrescribe el backup anterior y no hay copia fechada** → escalado a `pendientes.md`. **No se han parcheado skills**: RULE-018 prohíbe a un proceso de fondo escribir contenido de skills sin OK explícito (D5/D11).

- **LEC-20260814-013 · dominio `proceso`** — «Un estado `unknown` no se resuelve en el motor: se resuelve en el artefacto». *Fix:* ante `unknown`, comprobar primero el producto (fichero/fila/mensaje) y solo después el estado; no re-lanzar automáticamente jobs con efectos externos.
- **LEC-20260814-014 · dominio `proceso`** — «El ciclo semanal de incidentes leía un registro muerto». *Fix:* leer siempre `~/.hermes/cron/executions.db` (`executions` con `status not in ('ok','completed')` + `cron_incidents`) además de `lpa/incidentes/*-incidentes.md` (31 días sin escrituras).
- **LEC-20260814-015 · dominio `proceso`** — «Antes de culpar al script, mirar `lateness_seconds` del despacho». *Fix:* citar `last_dispatch` (lateness + kind) en el diagnóstico; un timeout con despacho tardío es una ventana perdida, no un script lento.
- **LEC-20260814-016 · dominio `proceso`** — «Un bloque truncado sobrevive a la reescritura del fichero». *Fix:* comprobar el marcador `[truncated]` en cada pasada y **no** reescribir por encima sin resolverlo; subir a P0 mientras siga dentro.

**Patch propuesto (pendiente de OK) — sin ejecutar:** en la skill `lpa` (sección de la operativa del ciclo): (a) paso 1 pasa a leer `cron_incidents`/`executions` como fuente primaria; (b) paso 4 declara que las lecciones de proceso van al ledger y que **el parche de skill se propone**, citando RULE-018. Texto listo en D11.

---

## 6. Cadena incidente → lección → mejora

| Incidente | Lección | Mejora |
|---|---|---|
| 5 ejecuciones `unknown` (01-10, 5 jobs) | LEC-013 | Antídoto escrito + CP-012 en incubadora; comprobación por artefacto en cada revisión |
| Ciclo leyendo `*-incidentes.md` (31 días muerto) | LEC-014 | Esta acta nace del registro del motor; patch propuesto para la skill `lpa` (D11) |
| 3 timeouts de 300 s con despacho 20-80 min tardío | LEC-015 | Regla de diagnóstico: `lateness_seconds` primero |
| `[truncated]` sobrevive a la reescritura | LEC-016 | P0 en el backlog + D5 (no reparar sin OK) |
| `retrabajo_ledger` sin la pérdida del scan EXP-002 | (F9) | Ocurrencia para CP-009: el fallo de un experimento no genera retrabajo registrado |
| Curador 703 ops con `PAUSED` | RULE-018 ya medido | Ocurrencia para CP-010; corte real = `pin`/`created_by` |

---

## DECISIONES (2026-10-02)

- **D0 — Fuente de incidentes del ciclo.** Se declara que `lpa/incidentes/*-incidentes.md` **no es la fuente real** (único fichero 01-09, 31 días sin escrituras) y que la fuente es `~/.hermes/cron/executions.db`. A partir de esta acta, el paso 1 lee **ambas**, y el `.md` solo se usa si alguien lo escribe a mano. (No se borra ni se reescribe el pasado; LEC-014.)
- **D1 — `consolidador-sesiones` (F1).** No se toca el job. Se declara el 01-10 como noche sin producto y se resuelve la incertidumbre por artefacto (no hay `sesiones-20261001.jsonl`). **No se re-ejecuta** nada sin OK explícito.
- **D2 — Curador (F2).** Se mide y se reporta; no se pausa, no se reanuda y no se tocan skills por mi parte (RULE-018). El corte efectivo medido es `hermes curator pin <skill>` por propiedad (no `pause`). Pendiente de decisión del usuario: qué skills del lab se pinean.
- **D3 — `lecciones_ledger` (F3).** Se registran HOY las 4 lecciones de la ventana (hecho en §5). El ledger se comprueba por `mtime` en cada ciclo: si el mtime es anterior a la fecha del acta, es fallo de la ventana, no ausencia de lecciones.
- **D4 — `retrabajo_ledger` (F4).** Sin cambios en el instrumento (sigue en 1 entrada). Se concede una ventana más: si el 09-10 sigue en 1, se propone fusionarlo con `lecciones_ledger` o darle disparador.
- **D5 — Bloque truncado (F5) / D8 del 25-09.** **No se repara en esta corrida**: el contenido perdido no existe en ninguna copia y RULE-018 prohíbe a un proceso de fondo escribir contenido de skills sin OK explícito. Se escala a **P0** en `pendientes.md` con los dos ficheros, la línea exacta y el texto que falta reconstruir. Requiere OK del usuario (o instrucción de reescribir el bloque desde cero).
- **D6 — `kel-revalidacion-diaria` (F6).** Se propone (no se ejecuta) arreglar `tools/revalidar_kos.py` línea 35: instalar PyYAML en el intérprete que usa el cron **o** sustituir `import yaml` por el parser ya disponible en el lab. Mientras no se arregle, la revalidación de KOs del KEL queda **sin vía automática**: anotado como estado del programa, no como fallo del ciclo.
- **D7 — Timeouts y `lateness_seconds` (F7).** Regla de diagnóstico adoptada (LEC-015). No se sube el timeout de 300 s a ciegas: primero hay que ver un despacho **puntual** que dure >300 s.
- **D8 — Recordatorio `once` del 01-10 (F8).** Es el único hallazgo con consecuencia directa para el usuario: el aviso «publicar L5» puede no haber salido y **no se puede reprogramar solo**. Se reporta al usuario en el resumen de esta corrida.
- **D9 — Experimento 002 (F9).** Día 01-10 perdido en la simulación de bolsa; **no se re-ejecuta** automáticamente. Se anota como ocurrencia de CP-009 (el fallo de un experimento no llega al `retrabajo_ledger`).
- **D10 — Revisión mensual del incubator (§8).** Ascensos ejecutados: **CP-009 → E1-007** y **CP-010 → E1-008** en `KNOWN.md` (con la limitación declarada: toda la evidencia es del Experimento 004, joko-lab → E1 «patrón observado», **no** E2 y sin derechos de regla estructural). **Sin fusiones**: CP-008, CP-010 y CP-011 conservan identidad porque sus antídotos son distintos (muestreo periódico / etiqueta de validez / comprobación de tamaño y cola). CP-001…CP-007 siguen incubando sin cambios.
- **D11 — Conflicto operativa ↔ RULE-018.** Se detecta que el paso 4 de esta operativa («lecciones … van directas a la skill … vía `skill_manage`») **contradice RULE-018** (`scope: skills_del_lab`: ningún proceso de fondo escribe contenido de skills sin OK). Mientras el usuario no decida, el ciclo funciona con el **ledger** como canal de registro y el patch de skill queda **propuesto**. Patch propuesto textualmente, pendiente de OK: paso 1 → «leer `executions`/`cron_incidents` de `~/.hermes/cron/executions.db` (fuente primaria) **y** `lpa/incidentes/*-incidentes.md`»; paso 4 → «registrar en el ledger; el patch de skill se **propone** en la acta (RULE-018)».
- **D12 — `CP-012`.** Promovido a la incubadora en esta misma sesión (TEMPLATE de 7 campos + falsación). Su antídoto (comprobar el artefacto) queda escrito; si en la próxima ventana aparece un caso donde el artefacto **también** engaña, se reevalúa la fusión con CP-010.

---

## 7. Próxima revisión

**Viernes 2026-10-09, 14:30 CEST** (`expr "30 14 * * 5"` del motor, id `05de86a93257`). Comprobaciones mínimas: (1) `executions` no sanos de la semana + `cron_incidents` sin resolver; (2) mtime de `lecciones_ledger.jsonl` y `retrabajo_ledger.jsonl`; (3) `[truncated]` en las skills (D5); (4) `hermes curator status` vs filas del ledger del día; (5) si D6 sigue sin arreglar, `kel-revalidacion-diaria` seguirá en `alerted`. **Revisión mensual siguiente:** primera corrida de noviembre (el motor sitúa el mes por la corrida de octubre).

---

## 8. Revisión mensual del incubator (paso 5) — 2026-10-02

**Criterio aplicado:** el mismo que usa la incubadora (2+ ocurrencias en contextos distintos) más el de `EPISTEMOLOGY.md` para E1. **Limitación declarada por delante:** toda la evidencia de CP-008/009/010/011/012 procede del **Experimento 004 (joko-lab)**; ninguna tiene aún un segundo experimento. Los ascensos se hacen, por tanto, como **E1 «patrón observado»**, citando la limitación, y **no habilitan reglas estructurales**. Las condiciones de falsación de cada CP se conservan y **se copian literalmente** a `KNOWN.md`.

- **CP-009 → `KNOWN.md` E1-007** (ascendido): «Un instrumento sin disparador no se usa: el que depende de que alguien se acuerde se degrada». 9 ocurrencias / 7 dominios distintos, medibles en disco. Falsación copiada: N=10 instrumentos nuevos, 2 ciclos, ≥8 con uso sostenido sin disparador → el patrón cae.
- **CP-010 → `KNOWN.md` E1-008** (ascendido): «Un instrumento no validado miente en silencio». 6 ocurrencias / 5 dominios (el 5º, la gobernanza del conocimiento: `PAUSED` vs 703 ops reales). Falsación copiada: N=10 instrumentos usados para decidir, 2 ciclos, ≥9 con la cifra correcta sin validación previa → el patrón cae.
- **CP-008** → **sigue en incubación** (12→13 ocurrencias). Antídoto distinto (muestreo periódico documento↔sistema). Revisión: mensual de noviembre.
- **CP-011** → **sigue en incubación** (2 ocurrencias +1 reforzada: el marcador sobrevive a la reescritura). Falta el denominador (cuántas ediciones largas salen bien) y D5 sin resolver.
- **CP-012** → **entra hoy** con 5 ocurrencias / 5 propósitos. Primer reexamen: ciclo del 09-10.
- **CP-001 … CP-007** → **sin cambios**: no hay evidencia nueva en la ventana; CP-006 y CP-007 siguen con 3 ocurrencias en 24 h y 1 solo dominio (necesitan un segundo dominio antes de moverse).
- **Ninguna fusión ejecutada** (D10). Ninguna descartada.

**Estado del programa:** KNOWN.md pasa de 6 E1 a 8 E1 (y de 15 a 17 afirmaciones con nivel); HYPOTHESIS.md y UNKNOWN.md sin cambios en esta revisión.

---

## Anexo · Instrumentos citados (trazabilidad)

- `~/.hermes/cron/jobs.json` (schedule, `last_status`, `failure_streak`, `last_dispatch.lateness_seconds`).
- `~/.hermes/cron/executions.db` → tablas `executions` y `cron_incidents` (consulta de solo lectura, `mode=ro`).
- `.curator_ledger.jsonl` (recuento por día y por actor).
- `hermes curator status` (salida literal `PAUSED`, `last run 8d ago`).
- `git status --porcelain`, `uptime -s`, `date`, `stat -c '%y %s %n'`, `grep -n '\[truncated\]'`.
- Productos: `04-operations/metrics/sesiones/`, `04-operations/reports/`, `01-knowledge/observations/`, `04-operations/metrics/telemetria/`.

**Backups RULE-008 creados en esta corrida** (`.bak-20261002`, en la misma carpeta del original): `lpa/KNOWN.md`, `lpa/CHANGELOG.md`, los 4 CP tocados y `04-operations/backlogs/pendientes.md`.

FIN DEL ACTA.
