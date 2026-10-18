# REVISIÓN DE FALLOS — 2026-09-18 (ciclo semanal LPA)

> **Ciclo:** `lpa-revision-incidentes-semanal` (id `05de86a93257`), decisión D0/INC-005 (reactivado el 02-09-2026).
> **Cadencia real del motor (leída en `~/.hermes/cron/jobs.json`, no en el acta anterior):** `30 14 * * 5` → **viernes 14:30**; `next_run_at` = **2026-09-25**; `repeat.completed` = 2; run anterior `last_run_at` = 2026-09-14T07:17:17. Este run: `last_dispatch` = {scheduled_at 2026-09-18T14:30:00, dispatched_at 2026-09-18T14:30:58, `kind: on_time`}.
> **Fecha real verificada con `date`:** 2026-09-18 14:39:15 CEST (viernes).
> **Revisión anterior:** `revision-fallos-2026-09-14.md` (D0..D5).
> **Ventana cubierta:** 2026-09-14 → 2026-09-18 (5 días, con actividad los 5).

---

## 0. Incidentes de la ventana (paso 1)

**No hay ningún fichero de incidentes nuevo. No se promueve nada *desde incidentes*: no hay FALLO/ACIERTO/DUDOSO/HIPOTESIS que leer.**

| Comprobación (solo lectura, 18-09) | Resultado real |
|---|---|
| `ls -la lpa/incidentes/` | `2026-09-01-incidentes.md`, `2026-09-02-auditoria-estado-lab.md`, `revision-fallos-2026-09-01.md`, `revision-fallos-2026-09-14.md`. Ningún `*-incidentes.md` nuevo |
| Búsqueda `*-incidentes.md` en `lpa/incidentes/` | **total_count = 1** (solo el del 01-09) |

→ El registro diario `YYYY-MM-DD-incidentes.md` acumula **17 días sin materializarse** (2ª semana consecutiva; ya fue lección LEC-20260814-007 el 14-09). Es el mismo hallazgo del ciclo anterior: **el instrumento de registro de fallos sigue sin disparador**.

Las promociones de esta semana **no** salen de incidentes declarados, sino de evidencia real medida en disco (≥2 contextos verificables por patrón), que es lo que el paso 3 exige.

---

## 1. Actividad de la ventana (contexto verificado)

- **Instrumentos con disparador que SÍ han producido:** `04-operations/metrics/telemetria/2026-09-14..17.{json,md}` a las 22:00 cada día; `01-knowledge/observations/` con OBS-112..117 (16 y 17-09, 22:00); `backup-joko-lab-diario` y `prediction-log-watchdog` con `last_run_at` = 2026-09-17.
- **Ficheros de sesiones:** último `resumen-dia-*` = **2026-09-14** (escrito el 15-09 a las 22:30); existen `sesiones-20260914.jsonl` y `sesiones-20260915.jsonl` (508 MB). **No hay `resumen-dia` de 15, 16 ni 17-sep** (ver F2).
- **Backlog/pendientes:** entradas los días 15, 16, 17 y 18 de septiembre en `04-operations/backlogs/pendientes.md` (líneas 30-86) y en el backlog activo (`2026-07-31-backlog.md`).
- **Pendiente P0 del 18-09 aún sin ejecutar:** el control de versiones en `~/joko-lab` (`git init` + commits). Verificado hoy: `ls -d /home/jokoalmi/joko-lab/.git` → **no existe**.

---

## 2. Fallos y hallazgos de la ventana

### F1. RULE-012 — 4º fallo declarado: hora afirmada sin `date` previo (15-09)

Evidencia literal (`04-operations/backlogs/2026-07-31-backlog.md`, línea 1992):

> «Verificado (15-sep-2026): `date` real **2026-09-15 17:22:53 CEST** (comprobado DESPUÉS de escribir: RULE-012 exige `date` ANTES de afirmar hora — fallo declarado); escritura de las notas con mtime **17:21** (el sello 17:20 con que se escribió era una estimación sin `date` previo — RULE-012 — y se corrigió a 17:21 tras comprobarlo)»

- Serie: 15-ago, 02-sep (×2) y 15-sep → **reincidencia**, no caso aislado. El fallo se autodocumentó y se corrigió en la misma sesión; no queda pendiente abierto.
- **Aplicado a este documento:** ninguna hora de este acta se afirma sin `date` previo (14:39:15 CEST) o sin cita literal del motor (`jobs.json`).

### F2. [NUEVO — hallazgo de la semana] Un job despachado que no produce, y su estado dice «ok»

`consolidador-sesiones` (id `9474f6f3d224`, script, `no_agent`, `30 22 * * *`):

- `last_dispatch` = {scheduled_at **2026-09-17T22:30:00**, dispatched_at **22:30:15**, lateness 15.1 s, **kind: `on_time`**} y **`fire_claim` tomado** el 17-09 a las 22:30:15 por `milinux:2496`.
- Pero `last_run_at` sigue en **2026-09-15T22:30:47**, `repeat.completed` = 39, **`last_status`: `ok`** y **`failure_streak`: 0**.
- Producto real: `04-operations/metrics/sesiones/` → último `resumen-dia-*` = **14-09** (escrito el 15-09 a las 22:30). **Sin `resumen-dia` de 15, 16 ni 17-sep.**
- Contraste: otro job del mismo minuto, `Bolsa autonoma - scan diario EXP-002` (`30 22 * * 1-5`), `last_run_at` = **2026-09-17T22:32:55**; los de 22:00/22:05/22:15/22:35 también corrieron.

**Interpretación ajustada a los datos:** el job **arrancó y no completó**; el marcador de ejecución no se actualizó y **ninguna alarma se enciende** (`failure_streak: 0`). No existe `~/.hermes/cron/logs/` en este setup → **cero evidencia de por qué**. No se toca el job ni ninguna configuración sin confirmación explícita.

Encaja con **CP-010** (un dato con apariencia de medición que es falso: aquí el «ok» del propio sistema de control) y **matiza CP-009** (tener cron no garantiza el registro: el disparador puede fallar en silencio).

### F3. [NUEVO] Una cadencia documentada que no es la del motor

- El acta anterior cerró con «Semanal: **2026-09-21 (lunes)**» (`revision-fallos-2026-09-14.md`, §6).
- El motor dice: `30 14 * * 5` → **viernes 14:30**, `next_run_at` = **2026-09-25**; `repeat.completed` = 2 y `last_run_at` = 2026-09-14T07:17:17 (compatible con una cadencia ANTERIOR de lunes ~07:15). Hoy **viernes 18-09** el motor lo ha ejecutado en tiempo (`on_time`) → la cadencia vigente es viernes.
- **No consta quién cambió el schedule ni cuándo** (no se afirma intención). El hecho es que el documento de gobernanza quedó descolgado del motor: es CP-008 (estado documentado ≠ estado real) y enseña que **la cadencia de un ciclo se lee en el motor, no en el acta**.

### F4. [NUEVO] Registro de negocio a medias: filas de uso con carpeta pero sin registro, y la decisión de no corregir

Entrada de `pendientes.md` del 18-09 08:02 (líneas 82-85): decisión del usuario = **registrar solo el uso de hoy y NO corregir la BD**; las discordancias quedan anotadas para otro día (fichas con carpeta y sin fila en `uso_diario`: 10-sep Zefiro, 11-sep Y EDP, 12-sep Soleil, 13-sep Alexandria II, 15-sep Afternoon Swim; nombre discordante el 08-sep: carpeta `Perseus` vs `uso_diario` `Bois Mystique`). Registrado hoy (autorizado): `uso_diario` **id 74 → perfume_id 1195** (Yesterday, Room 1015), decant 154, fecha `2026-09-18`; backup previo `coleccion.db.BACKUP.20260918_yesterday` (348.160 B); ficha enviada a Telegram.

**Verificado hoy sobre la BD real (`~/perfume-ia/data/coleccion.db`, solo lectura):** últimas 3 filas de `uso_diario` = id 74 (2026-09-18, creada 06:02:43), id 73 (2026-09-17, Papyrus Moléculaire, decant 208) e id 72 (2026-09-16, Molecule 01 + Iris). `count(*)` = **72** con `id` máximo **74** → **2 ids ausentes**; no se investiga en esta revisión (se anota como **duda**, no como hallazgo: puede ser legítimo).

Patrón: la **ficha** (pieza) tiene disparador diario y no falla; el **registro** (fila en la tabla) no tiene comprobación periódica → deriva silenciosa. Es CP-009 + CP-008.

### F5. [NUEVO] Instrumento del EXP-20260903-001: 3ª semana sin alimentar y decisión del 14-09 sin respuesta

- `04-operations/metrics/retrabajo_ledger.jsonl`: **0 bytes, 0 líneas**, mtime **2026-09-03 14:56** (medido hoy, 15 días después).
- El informe previsto **sigue sin existir**: `ls research/ | grep -i exp-` devuelve solo el diseño `exp-20260903-roi-metacognicion.md` (4.927 B, 03-09 14:54).
- La **D2 del 14-09 sigue abierta** y es decisión del usuario (a/b/c). Sin respuesta, el estado sigue «bloqueado», no «cerrado» → **no se rellena nada a posteriori**.

### F6. [NUEVO] Transcripción por VLM: el medidor rellena (con antídoto ya aplicado)

Origen del patrón CP-010: GLM-4.6V devolvió 3.540 chars / 517 palabras para una tarjeta de ~180-300 palabras medibles, y un crop de 255 px «leyó» tres secciones completas. Lo delató la **densidad de tinta medida sin modelo** (PIL/numpy). Antídoto escrito en la skill `instagram-content-extraction` (líneas 548-566): «si el modelo devuelve 2-3× más palabras que las medidas, marcar como NO literal».

---

## 3. Aciertos de la ventana (verificables, sin promoción)

- **Copia de rescate al USB hecha y verificada** (`pendientes.md`, 17-sep 23:33): `rsync --stats` 9,00 MB/s (11,11 G) frente al falso `du -sm` 0,43 MB/s; integridad con md5, `gzip -t` y `rsync --checksum` (0 ficheros con contenido distinto).
- **Panel del lab arreglado** tras detectar el «medidor ciego» (marcaba 10 huecos donde había 12 porque `tools/knowledge_health.py` no encontraba `yaml` en el intérprete de lanzamiento): el arreglo abre hueco P1 con el error literal en vez de ocultarlo (`pendientes.md`, 17-sep 22:59).
- **One-shot del 17-09 a las 12:20** (análisis «Claude Managed Agents»): completó su entregable sin intervención (job con skills + workdir declarados) → contraste positivo frente al trabajo no recurrente.
- **Founderz:** clases 11 y 12 absorbidas con notas, backups y verificación de escrituras (15-09).

---

## 4. Patrones (paso 3)

**Promovido (nuevo): CP-010 — «Un instrumento no validado miente en silencio»**
→ `lpa/pattern-incubator/CP-010-instrumento-no-validado-miente.md` (E0, 7 campos del TEMPLATE + condición de falsación).
Ocurrencias (3 contextos + 1 caso fresco): (1) tasa de copia a disco (F, 17-sep); (2) panel de salud del lab (gobernanza/conocimiento); (3) transcripción por VLM (visión, F6); (4) **hallazgo de hoy**: el `last_status: ok` del propio scheduler con 0 producto (F2).

**Ampliados (sin ascenso — la revisión mensual del 01-10 decide):**

- **CP-008 (estado real ≠ documentado)**: +2 ocurrencias nuevas (F3 cadencia del acta vs motor; F4 registro vs BD). Total: 8 + 2.
- **CP-009 (instrumento sin disparador se degrada)**: +2 ocurrencias nuevas (F4 registro a medias; F5 ledger del EXP con 0 líneas tras 15 días) **y una matización medida hoy**: el contraste «con cron sí escribe» tiene excepción (F2: job con cron despachado que no produce) → tener disparador no basta si el disparador falla en silencio. Sigue en incubación; **candidato a E1 el 01-10**.

**Descartados:** ninguno.

**No promovidos por falta de evidencia (dudosos declarados):**

- «El contexto no declarado no existe» — 1 solo contexto de fallo (el worker multiagente del 16-09, que no alcanza `localhost` ni aplica las reglas del lab; `pendientes.md` línea 35) frente a 1 contraste positivo (el one-shot del 17-09 con skills y workdir declarados). **No se crea CP-011** hasta una 2ª ocurrencia en otro contexto.
- Los 2 `id` ausentes en `uso_diario` (72 filas, id máximo 74) → duda anotada, sin patrón.

---

## 5. Lecciones registradas (paso 4)

Registradas en `04-operations/metrics/lecciones_ledger.jsonl` (dominio `proceso`; el ledger pasa de 7 a **9 líneas**, verificado con `wc -l`):

| id | Título | Causa raíz | Fix |
|---|---|---|---|
| **LEC-20260814-008** | «El estado 'ok' de un cron job no prueba que produjo: verificar el PRODUCTO» | El campo de estado informa del *runner* (arrancó y no reportó error), no del *entregable*: un script que arranca y no completa deja `last_run_at` congelado sin encender alarma | Comparar el fichero fechado producido contra `last_run_at` y `last_dispatch.kind` |
| **LEC-20260814-009** | «La cadencia de un ciclo se lee en el MOTOR, no en el acta anterior» | El `schedule` puede cambiar sin actualizar el documento de gobernanza (acta 14-09: lunes; motor hoy: `30 14 * * 5`) | Leer `schedule` + `next_run_at` + `last_run_at` en `jobs.json` y citarlos literalmente; anotar la divergencia, no reescribir el pasado |

**Patches de skill aplicados (misma sesión, vía `skill_manage`):**

1. `hermes-cron-jobs` → **pitfall 15** («`last_status: ok` NO prueba que el job produjo: un job DESPACHADO puede arrancar y no completar sin encender ninguna alarma»), con el caso literal y el diagnóstico diferencial frente a «no se ejecutó» y «script roto».
2. `detectar-sin-uso` → comprobación manual nueva en el pase semanal: para cada job activo con salida fechada, cruzar `last_run_at`/`last_dispatch` contra el fichero producido (el detector mira la *definición* del cron, no su *producto*).

---

## 6. Cadena incidente → lección → mejora

| Eslabón | Estado 18-09 |
|---|---|
| **Incidente** | INC-005 (01-09) + hallazgos medidos de la ventana: F2 (job que no produce), F3 (cadencia), F4 (registro a medias), F5 (EXP sin alimentar) |
| **Lección** | LEC-20260814-008 y LEC-20260814-009 (dominio `proceso`), registradas hoy |
| **Patrón** | CP-010 promovido (E0); CP-008 y CP-009 ampliados |
| **Mejora** | 2 patches de skill aplicados (`hermes-cron-jobs`, `detectar-sin-uso`); 4 propuestas pendientes de confirmación del usuario (D4-D7) |

---

## DECISIONES (18-09)

- [x] **D0 (INC-005 — vigilancia):** no hay incidentes nuevos (0 `*-incidentes.md` nuevos desde el 01-09) → **no se fuerza ninguna promoción desde incidentes**. El registro diario suma 17 días sin materializarse. Sin acción unilateral.
- [x] **D1 (patrón nuevo):** **CP-010** promovido a la incubadora (3 contextos + 1 caso fresco) con los 7 campos y condición de falsación. Backups RULE-008 (`.bak-20260918`) hechos antes de tocar nada.
- [x] **D2 (patrones vivos):** CP-008 y CP-009 ampliados con evidencia literal de la ventana. Ambos siguen en incubación; su ascenso/descarte se decide el 01-10 (no antes).
- [x] **D3 (lecciones):** 2 lecciones de proceso registradas + 2 patches de skill aplicados. Estado verificado por salida real (`wc -l` = 9 en el ledger).
- [ ] **D4 (decisión del usuario — sigue abierta desde el 14-09):** EXP-20260903-001 → (a) reanudar con disparador, (b) cerrar como «sin datos», (c) retirar. Ledger a 0 y sin informe; **no se rellena nada a posteriori**.
- [ ] **D5 (propuesta, NO ejecutada — infraestructura de crons):** dar al registro de incidentes un disparador real (el propio ciclo semanal rellena la semana desde `pendientes.md`/backlog; el observador diario genera el diario) y añadir a los watchdogs una comprobación de **producto** (¿existe el entregable con fecha de hoy?), no solo de estado. **Requiere confirmación explícita** (ya era propuesta el 14-09 y sigue sin ejecutar).
- [ ] **D6 (propuesta, NO ejecutada — diagnóstico de F2):** investigar por qué `consolidador-sesiones` arranca y no completa desde el 16-09 (sin logs del cron disponibles) y decidir si se le añade un «producto esperado» para que falle cuando no escriba. **No se toca el job sin confirmación.**
- [ ] **D7 (propuesta, NO ejecutada):** alinear la cadencia declarada en los documentos LPA con la del motor (`30 14 * * 5`; próxima 2026-09-25). Decisión del usuario: mantener viernes (actual) o volver a lunes.

---

## 7. Próxima revisión

- **Semanal:** **2026-09-25 (viernes 14:30)**, según el motor (`30 14 * * 5`, `next_run_at` 2026-09-25). *Corrige* el «2026-09-21 (lunes)» del acta anterior (F3).
- **Mensual (1ª del mes):** **2026-10-01** → revisar la incubadora completa (CP-001..CP-010): ascenso a `KNOWN.md`/`HYPOTHESIS.md`, descarte o fusión. Solape declarado a resolver: CP-008 / CP-009 / CP-010 (estado documentado, instrumento sin disparador, instrumento no validado).

---

*Documento generado: 2026-09-18 (viernes). Fecha/hora verificadas con `date` (14:39:15 CEST). Hora del ciclo según `jobs.json`: dispatched 2026-09-18T14:30:58 (`on_time`).*
*Fuentes citadas (todas leídas/medidas en esta sesión, solo lectura salvo las escrituras declaradas en D1-D3): `lpa/incidentes/` (ls + búsqueda `*-incidentes.md`), `~/.hermes/cron/jobs.json` (`lpa-revision-incidentes-semanal` 05de86a93257, `consolidador-sesiones` 9474f6f3d224, `Bolsa autonoma`), `04-operations/metrics/sesiones/` (ls), `01-knowledge/observations/` (ls), `04-operations/metrics/telemetria/` (ls), `04-operations/metrics/retrabajo_ledger.jsonl` (stat+wc), `04-operations/metrics/lecciones_ledger.jsonl` (wc -l + tail), `04-operations/backlogs/pendientes.md` (líneas 35, 52, 64, 71, 75, 82-85), `04-operations/backlogs/2026-07-31-backlog.md` (línea 1992), `~/perfume-ia/data/coleccion.db` (sqlite3 modo solo lectura), `research/` (ls).*
