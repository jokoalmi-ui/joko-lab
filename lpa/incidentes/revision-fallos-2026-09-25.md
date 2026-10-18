# REVISIÓN DE FALLOS — 2026-09-25 (ciclo semanal LPA)

> **Ciclo:** `lpa-revision-incidentes-semanal` (id `05de86a93257`), decisión D0/INC-005 (reactivado el 02-09-2026).
> **Cadencia real del motor (leída en `~/.hermes/cron/jobs.json`, no en el acta anterior):** `30 14 * * 5` → **viernes 14:30**; `next_run_at` = **2026-10-02T14:30:00+02:00**; `repeat.completed` = 3; run anterior `last_run_at` = 2026-09-18T14:41:04. Este run: `last_dispatch` = {scheduled_at 2026-09-25T14:30:00, dispatched_at 2026-09-25T14:30:17.610266, lateness 17.6 s, `kind: on_time`}.
> **Fecha real verificada con `date`:** 2026-09-25 14:32:14 CEST (viernes).
> **Revisión anterior:** `revision-fallos-2026-09-18.md` (D0..D7).
> **Ventana cubierta:** 2026-09-18 → 2026-09-25 (8 días, con actividad todos los días laborables).

---

## 0. Incidentes de la ventana (paso 1)

**No hay ningún fichero de incidentes nuevo. No se promueve nada *desde incidentes*: no hay FALLO/ACIERTO/DUDOSO/HIPOTESIS que leer.**

| Comprobación (solo lectura, 25-09) | Resultado real |
|---|---|
| `ls -la lpa/incidentes/` | `2026-09-01-incidentes.md`, `2026-09-02-auditoria-estado-lab.md`, `revision-fallos-2026-09-01.md`, `revision-fallos-2026-09-14.md`, `revision-fallos-2026-09-18.md`. **El más reciente con formato `*-incidentes.md` sigue siendo el del 01-09** |
| Búsqueda `*incidentes*.md` en `lpa/incidentes/` | **total_count = 1** (solo el del 01-09) |

→ El registro diario `YYYY-MM-DD-incidentes.md` acumula **24 días sin materializarse** (01-09 → 25-09; 3ª semana consecutiva que este ciclo lo declara). Sigue sin disparador; ya fue lección LEC-20260814-007 (14-09) y ocurrencia (2) de CP-009.

Las promociones de esta semana **no** salen de incidentes declarados, sino de evidencia medida en disco (≥2 contextos verificables por patrón), que es lo que el paso 3 exige.

---

## 1. Actividad de la ventana (contexto verificado)

- **Instrumentos con disparador que SÍ produjeron (contraste positivo):** `04-operations/metrics/telemetria/` con `.json` + `.md` para **los 8 días de la ventana** (2026-09-17 … 2026-09-24; el de hoy 25-09 corresponde a las 22:00); `01-knowledge/observations/` hasta `OBS-138` (24-09: fallback-rate, uso-rag, decisiones-por-politica).
- **Backups diarios presentes:** `~/joko-lab.BACKUP.20260918|19|21|23|24` y `~/hermes-lab.BACKUP.20260923|24` (no existe `~/joko-lab/04-operations/backups`; la ruta real es la del home).
- **Git en `~/joko-lab`: el P0 del 18-09 queda CERRADO.** El acta anterior verificó que `.git` **no existía**; hoy hay repo (`master`, sin remoto) con **4 commits de hoy**: `19bed8c` (arnés RSI v0 + informe), `67861a0` (ronda 3), `a3034a5` (informe + sección 6.1: primer asiento del ledger de retrabajo), `e70b612` (ronda 3b; **HEAD**). Quedan **23 entradas** en `git status --porcelain`.
- **Backlog/pendientes:** `04-operations/backlogs/pendientes.md` con **372 líneas / 111.635 B**, entradas del 22, 24 (×2) y 25-sep.
- **Trabajo concurrente durante esta revisión:** `research/analisis-rsi-lab-2026-09-25.md` (18.962 B, mtime **14:31**) y `research/rsi-v0/` (mtime **14:33**) → hay una sesión activa escribiendo mientras este ciclo lee. Los datos de este acta son una foto de ese momento; el HEAD de git citado puede haberse movido después.

---

## 2. Fallos y hallazgos de la ventana

### F1. [RECURRENCIA, 2º ciclo] `consolidador-sesiones`: despachado a tiempo y sin producto — ahora 3 noches seguidas, y un día sí / otro no

`consolidador-sesiones` (id `9474f6f3d224`, script, `no_agent`, `30 22 * * *`) — leído hoy en `jobs.json`:

- `last_run_at` = **2026-09-21T22:31:07.365243+02:00** — congelado desde el 21-sep.
- `last_status` = **`ok`**, `failure_streak` = **0**, `repeat.completed` = 42, `next_run_at` = 2026-09-25T22:30:00.
- Último `last_dispatch` = {scheduled 2026-09-24T22:30:00, dispatched **22:30:20.764760**, lateness 20.8 s, **`kind: on_time`**}.
- **Productos:** `sesiones-*.jsonl` presentes hasta **20260921** (la serie trae 0907, 0908, 0909, 0914, 0915, 0918, 0919, 0921 → **sin 0916, 0917, 0920, 0922, 0923, 0924**); `resumen-dia-*` presente hasta **2026-09-20** (escrito el 21-09) → **sin 19, 21, 22, 23 ni 24-sep**.

**Lectura ajustada a los datos:** el 18-09 el acta declaró «arrancó y no completó» y lo dejó como hallazgo aislado. Hoy hay dos hechos nuevos: (a) el job **sí** volvió a producir las noches del 18, 19 y 21-sep (no está muerto: es **intermitente**); (b) desde el 21-sep **no hay producto alguno** pese a despachos `on_time` (el último medido, 24-sep 22:30:20). El campo de estado dice `ok` los cuatro días. En este setup **no existe `~/.hermes/logs/` del cron** para ver por qué → no se afirma causa. **No se toca el job ni ninguna configuración sin confirmación explícita.**

Encaja con **CP-010** (el «ok» del propio sistema de control es una cifra con apariencia de dato), **matiza CP-009** (tener disparador no basta si el disparador falla en silencio) y **refuerza LEC-20260814-008** (verificar el PRODUCTO).

### F2. [NUEVO] Dos skills con la escritura TRUNCADA (`[truncated]` literal), y la que lo manda buscar es una de ellas

Medido hoy en `~/.hermes/skills/`:

| Fichero | Línea | Cola del bloque | stat | Causa identificada |
|---|---|---|---|---|
| `joko-lab/validacion-instrumentos-medicion/SKILL.md` | **32** | «…Un cero o lista vacía de tu propio extractor** tampoco e**[truncated]» | 44.859 B, mtime **25-09 07:48:50** | `patch` de `actor: curator` sobre esa skill a las **05:48:50.716103+00:00** (= **mismo segundo**) |
| `render-html-a-imagen/SKILL.md` | **119** | «…ilegible, desce**[truncated]» | 23.461 B, mtime **25-09 08:16:08** | 4 `patch` de `curator` a las 06:15:59 + `write_file` a las **06:16:08.675240+00:00** (= **mismo segundo**) |

- La regla que ordena buscar el marcador tras cada edición larga («*Un patch de más de ~1 KB puede quedar escrito TRUNCADO…*») está escrita **en la propia línea 32 que quedó truncada**.
- **Ya se había detectado y NO se reparó:** `pendientes.md` 24-sep 08:00 (línea 357): «Defecto detectado sin arreglar: esa SKILL.md ya traía un marcador literal `[truncated]` en la línea 32 (edición anterior truncada por el arnés); requiere OK para reescribir ese final».
- **El texto perdido no es recuperable:** búsqueda de los fragmentos cortados en `~/hermes-backup-pre-021` y `~/.hermes/profiles/**` → **0 coincidencias**. Reparar = reescribir el bloque (D8), no restaurar.
- **Candidata descartada:** `software-development/perfume-ia/references/capa-lpa-recomendacion.md` línea 33 (`from modules.[truncated] import recomendar`) — el fichero continúa después y el bloque está completo → compatible con redacción manual; **no se cuenta como ocurrencia**.

→ Patrón nuevo: **CP-011**.

### F3. [NUEVO] El registro de lecciones declarado no es el que recibe: dos registros de lo mismo, y el manual lleva 7 días congelado

- `04-operations/metrics/lecciones_ledger.jsonl`: **9 líneas / 7.987 B, mtime 18-sep 14:40** — sin un solo cambio desde la revisión anterior (última: `LEC-20260814-009`).
- `~/.hermes/skills/.curator_ledger.jsonl`: **1.282 líneas**, con actividad **todos** los días de la ventana; solo sobre las dos skills de F2 acumula 99 entradas; **36 entradas con `actor: curator` del día 25-09** (de 05:47:50 a 11:34:35 UTC = 07:47 a 13:34 CEST).
- En la ventana se aprendieron lecciones que **solo** entraron por el canal automático o por patch directo: el 24-sep el propio acta anota «**Lecciones en skills: NO se escriben aquí (evitar duplicado)** […] El curador ya las consolidó […] Traza: `.curator_ledger.jsonl`, ids `4a55249e29b0`, `4fa91bace86c`, `e03e1576f508`»; el 25-sep se consolidó una lección en `edicion-aditiva-registros` vía `skill_manage` (mutación `31fd87cf70ed`, con el dato de método de que el primer intento por script **no aparecía** en el ledger del curador).

→ El «registro de lecciones del lab» (el que este ciclo alimenta) y el registro donde realmente quedan las lecciones son **dos ficheros distintos que no se hablan**. Amplía **CP-008** y **CP-009** (no se crea CP nuevo: solapa con ambos y con el solape declarado para la mensual).

### F4. [NUEVO/VERIFICADO] El resumen de estado del curador no refleja lo que el curador escribe

- `hermes curator status` (leído hoy, 14:3x) → **`curator: PAUSED`**; `runs: 13`, `last run: 1d ago`, `last summary: auto: 16 marked stale, 6 archived, 6 reactivated; llm: skipped (consolidation off)`, `last report: ~/.hermes/logs/curator/20260923-170843`.
- Ledger del curador: **36 entradas `actor: curator` del 25-09**, la última a las **11:34:35 UTC (13:34 CEST)** → la actividad registrada del curador es **posterior** al `last report` (23-09) y **anterior** al estado leído hoy.
- El 25-sep 10:06 `pendientes.md` ya lo había apuntado como «CONFIRMA (no es nuevo, queda verificado)» mezclando estado `ENABLED` y 6 mutaciones. Hoy el estado se lee **PAUSED**: **no se establece cuándo ni quién lo pausó** (los logs del curador son del 23-09), y por eso el hecho se registra como divergencia medida, no como causa.

→ Amplía **CP-008** (el resumen de estado es un documento con estado que caduca) y **CP-010** (el campo que resume la actividad no mide la actividad).

### F5. [NUEVO] La revisión mensual declarada (01-10) no tiene corrida en el motor

- Actas anteriores fijan la revisión **mensual el 2026-10-01** (paso 5 del ciclo: incubadora → ascensos a `KNOWN.md`/`HYPOTHESIS.md`, descartes o fusiones; hay **11 CP** incubando, CP-001..CP-011).
- El motor dice: `30 14 * * 5` con `next_run_at` = **2026-10-02** → **el 01-10 (jueves) no hay ninguna corrida programada**; la primera del mes es el 02-10.

→ No es un fallo de datos, es una **cadencia documentada que no existe en el motor** (mismo tipo que F3 del acta del 18-09). Decisión propuesta: **D9**.

---

## 3. Aciertos de la ventana (verificables, sin promoción)

- **A1 — Hipótesis refutada con la condición de aborto pre-registrada cumplida (24-sep).** El subtipo `cuantificador` (n=20, 20/20 de Laya) se amplió a un set congelado de **n=120** (`casos_cuant_n120.json` 163.044 B, sha256 `d7e423a81f72d54d…`; 60 TRUE/60 FALSE; auditoría por conteo literal: 0 de 120 contradicciones ↔ 107 de 120 respuestas SI, pese a campos ausentes en el texto). Resultado: Laya `typed-decisions` **0,5083** frente al umbral de aborto declarado de antemano («si con n≥100 baja de 0,9, se descarta») → **hipótesis REFUTADA**, tarjeta `t_d35590c6` a `done`, **sin trabajo derivado**, 0 €. El 20/20 era **coincidencia del subconjunto homogéneo** (sus 10 falsos eran todos del mismo campo). Uso ejemplar del instrumento de decisión: condición de aborto escrita ANTES de medir.
- **A2 — `retrabajo_ledger.jsonl` recibe su PRIMERA entrada, 22 días después de su diseño (25-sep).** 1 línea / 566 B, mtime **25-09 13:29**: `{"fecha":"2026-09-25","sesion_id":"20260925_090159_b65803","tipo":"E6","causa_raiz":"reescritura de la instruccion (4 variantes) sin cubrir el RF: los mismos 2 casos fallan en las 5 y la metrica no se mueve (6/8 en todas)","tokens_estimados_correccion":4710,"tiempo_min":0.7,…}`. Cierra el caso (3) de CP-009 — con una matización: el asiento entró por **escritura manual durante una sesión**, no por un disparador (el instrumento «se usó» cuando alguien se acordó de él).
- **A3 — El P0 de control de versiones está cerrado (ver §1):** `.git` inexistente el 18-09 → hoy 4 commits del mismo día y `master` local. Es la primera vez, en 3 semanas de este ciclo, que un P0 abierto se cierra con evidencia.
- **A4 — El trabajo del RSI v0 dejó traza auditable:** 4 commits por rondas (r1, r2, r3, r3b), `research/rsi-v0/` con `resumen_r1..r3b3.json` + `log_r*.txt`, backup del arnés (`rsi_v0_json.py.bak-20260925-ronda3`) e informe de 18.962 B. La ronda 3b añade «los niveles de think son indistinguibles (95,6-98,2 s de mediana)» → refuta el óptimo de la pasada única.
- **A5 — El propio laboratorio detectó el marcador `[truncated]` el 24-09** y lo declaró como defecto abierto en vez de taparlo (ver F2). La autodetección funcionó; lo que falló fue la reparación.

---

## 4. Patrones (paso 3)

**Promovido (nuevo): CP-011 — «Una escritura larga se trunca sin fallar: el artefacto queda a medias y con una marca que nadie busca»**
→ `lpa/pattern-incubator/CP-011-escritura-truncada-sin-fallo.md` (E0, los 7 campos del TEMPLATE + condición de falsación).
Ocurrencias (**2 contextos confirmados**): (1) `validacion-instrumentos-medicion/SKILL.md` línea 32 (44.859 B, mtime 25-09 07:48:50 = `patch` de `curator` 05:48:50.716103+00:00); (2) `render-html-a-imagen/SKILL.md` línea 119 (23.461 B, mtime 25-09 08:16:08 = `write_file` de `curator` 06:16:08.675240+00:00). + 1 ocurrencia previa ya detectada el 24-09 y no reparada. − 1 candidata descartada (`capa-lpa-recomendacion.md` línea 33: el fichero continúa después → redacción manual, no corte).

**Ampliados (sin ascenso — la revisión mensual decide):**

- **CP-008 (estado real ≠ documentado)**: **+2 ocurrencias nuevas** — (a) `hermes curator status` = `PAUSED` frente a 36 entradas `actor: curator` del mismo día en el ledger; (b) el registro de lecciones declarado (9 líneas, congelado) frente al registro que realmente recibe (1.282 líneas, actividad diaria). Total: 8 + 2 + 2 = **12**.
- **CP-009 (un instrumento sin disparador no se usa)**: **+2 ocurrencias + 1 caso cerrado** — (6) `lecciones_ledger.jsonl` congelado 7 días mientras el registro automático crece; (7) `resumen-dia`: produjo 3 de las 8 noches de la ventana (último 2026-09-20) pese a tener cron → matiza de nuevo «con disparador sí escribe»; (8) **caso (3) CERRADO**: el ledger de retrabajo recibió su primer asiento (A2), por escritura manual, no por disparador. Total: 5 + 2 + 2.
- **CP-010 (un instrumento no validado miente en silencio)**: **+2 ocurrencias** — (5) recurrencia **reproducible** del caso (4): 3 noches consecutivas sin producto con despacho `on_time`, `last_run_at` congelado en 21-09 y `failure_streak 0` (F1); (6) el resumen de estado del curador frente a su propio ledger (F4). Total: 3 + 1 + 2.

**Descartados:** ninguno.

**No promovidos por falta de evidencia (dudosos declarados):**

- **«Dos registros de lo mismo que no se hablan»** (F3) — tiene 2-3 escrituras en canales distintos y es tentador como CP-012, pero **se declara dudoso y NO se promueve**: solapa con CP-008 (documento vs sistema) y con CP-009 (instrumento sin disparador), y crear un tercer patrón antes de la mensual garantiza trabajo de fusión. Se resuelve en la revisión del 02-10 con más contexto.
- **Tercer fichero con `[truncated]`** (`capa-lpa-recomendacion.md`) — no ajusta al mecanismo (el fichero continúa) → duda anotada, no ocurrencia.
- **La «mejora en latencia» de Laya** — preguntada por el usuario el 24-sep; la evidencia real (0,5083 de accuracy, SI en 107/120) la deja sin sustento → no es patrón, es un resultado refutado.

---

## 5. Lecciones registradas (paso 4)

Registradas en `04-operations/metrics/lecciones_ledger.jsonl` (dominio `proceso`; backup previo propio: `lecciones_ledger.jsonl.bak-20260925`; el ledger pasa de **9 a 12 líneas**, verificado con `wc -l`):

| id | Título | Causa raíz | Fix |
|---|---|---|---|
| **LEC-20260814-010** | Una edición larga puede quedar truncada sin fallar: comprobar tamaño y cola, y buscar el marcador `[truncated]` | El canal de escritura devuelve OK aunque escriba menos: el fichero existe, se lee y el corte sólo se ve en la cola | Tras cada edición >1 KB: `stat` + leer la cola + buscar el marcador; escribir por piezas con `write_file`; si ya se perdió, declarar el hueco (no rellenar de memoria) |
| **LEC-20260814-011** | El resumen de estado de una herramienta no es su registro de actividad: contar el ledger por actor y fecha | `curator status` resume corridas programadas/pausa; las mutaciones las escribe cada sesión con `actor: curator` | Antes de afirmar el estado: contar entradas por `actor` y fecha en `.curator_ledger.jsonl`; citar ambos datos y decir cuál es el medido |
| **LEC-20260814-012** | El «registro de lecciones» del lab y el del curador son dos registros: una lección existe sólo en el canal donde se escribió | Cada canal escribe con su instrumento (ledger manual vs skill/ledger del curador) y nadie compara | Al registrar una lección: declarar el canal; si va a skill, anotar la referencia en el ledger del lab o declarar canónico el del curador; los CIclos leen sólo uno |

**Patches de skill aplicados (misma sesión, vía `skill_manage`; consolidados dentro de secciones existentes, sin bloque nuevo):**

1. `hermes-cron-jobs` → **pitfall 15** ampliado con la recurrencia medida (job intermitente: produce 18/19/21-sep y cae 22/23/24-sep con `last_status: ok` en los cuatro días) y el método de la **rejilla**: comparar los productos esperados de la ventana, no el último fichero.
2. `detectar-sin-uso` → hallazgo «job despachado que no produce» ampliado con la misma rejilla y el dato de los 3 días seguidos, para que el pase semanal no dé por bueno un job caído hace 3 noches.

---

## 6. Cadena incidente → lección → mejora

| Eslabón | Estado 25-09 |
|---|---|
| **Incidente** | INC-005 (01-09) + hallazgos medidos de la ventana: F1 (job intermitente, 3 noches sin producto), F2 (2 skills truncadas), F3 (dos registros de lecciones), F4 (estado del curador vs ledger), F5 (mensual sin corrida en el motor) |
| **Lección** | LEC-20260814-010, -011 y -012 (dominio `proceso`), registradas hoy; backup previo `.bak-20260925` |
| **Patrón** | CP-011 promovido (E0); CP-008, CP-009 y CP-010 ampliados con evidencia medida |
| **Mejora** | 2 patches de skill aplicados (`hermes-cron-jobs` pitfall 15, `detectar-sin-uso`); ampliaciones escritas en los 4 CP (backups `.bak-20260925`); 4 propuestas nuevas pendientes de OK (D8-D10) + 4 arrastradas (D4-D7) |

---

## DECISIONES (25-09)

- [x] **D0 (INC-005 — vigilancia):** no hay incidentes nuevos (**0** `*-incidentes.md` nuevos desde el 01-09; el registro suma **24 días** sin materializarse) → **no se fuerza ninguna promoción desde incidentes**. Las promociones de hoy salen de evidencia medida en disco.
- [x] **D1 (patrón nuevo):** **CP-011** promovido a la incubadora con los 7 campos y condición de falsación (2 ocurrencias confirmadas en 2 contextos, cada una atada al segundo del `patch`). Backups RULE-008 `.bak-20260925` hechos **antes** de tocar nada (4 ficheros).
- [x] **D2 (patrones vivos):** CP-008, CP-009 y CP-010 ampliados con evidencia literal de la ventana (sin ascensos: la mensual decide). Se declara **descartado como CP nuevo** el hallazgo F3 (solapa con CP-008/CP-009) y **no ocurrencia** el tercer `[truncated]`.
- [x] **D3 (lecciones):** 3 lecciones de proceso registradas (LEC-010, -011, -012) + 2 patches de skill aplicados. Estado verificado por salida real (`wc -l` = 12).
- [ ] **D4 (decisión del usuario — abierta desde el 14-09, sigue abierta):** EXP-20260903-001 → (a) reanudar con disparador, (b) cerrar como «sin datos», (c) retirar. **Matiz nuevo:** su instrumento (`retrabajo_ledger.jsonl`) ya no está a 0, pero el asiento de hoy (A2) es del **RSI v0**, no del EXP-20260903-001, cuyo informe sigue sin existir. El one-shot `8717d7fa34ad` (`pendientes-12-rsi-y-curador`) **sí se ejecutó** (25-09 12:07:28, `last_status: ok`, `next_run_at: null`) y presentó los 4 puntos; no consta respuesta registrada para éste.
- [ ] **D5 (propuesta, NO ejecutada — disparador del registro de incidentes):** dar al registro `YYYY-MM-DD-incidentes.md` un disparador real o **declararlo retirado** y que este ciclo semanal sea el único registro de fallos (evita mantener dos instrumentos, uno de ellos muerto). Requiere confirmación explícita.
- [ ] **D6 (propuesta, NO ejecutada — diagnóstico de F1):** `consolidador-sesiones` con **3 noches seguidas sin producto** y estado `ok`. Propuesta: añadirle un «producto esperado» que haga fallar el job cuando no escriba, y comprobar la rejilla (no el último fichero). **No se toca el job, ni el stack, ni n8n sin confirmación.**
- [ ] **D7 (propuesta, NO ejecutada — cadencia):** el motor manda: viernes `30 14 * * 5`, próxima **2026-10-02**. Decisión del usuario: mantener viernes (actual) o volver a lunes. (Ya era D7 el 18-09.)
- [ ] **D8 (propuesta NUEVA, NO ejecutada — reparar F2):** reescribir los 2 bloques truncados (`validacion-instrumentos-medicion/SKILL.md` línea 32; `render-html-a-imagen/SKILL.md` línea 119). **El texto perdido no es recuperable** (0 coincidencias en las copias) → la reparación es reescritura, no restauración; se hará con OK y con el contenido que conozca quien lo escribió, sin rellenar de memoria.
- [ ] **D9 (propuesta NUEVA, NO ejecutada — mensual del 01-10):** la revisión mensual (paso 5) **no tiene corrida** en el motor (próxima: 02-10). Opciones: (a) hacerla en la corrida del **02-10** (1 día tarde) o (b) lanzar un one-shot para el **01-10**. Decisión del usuario.
- [ ] **D10 (propuesta NUEVA, NO ejecutada — registro de lecciones):** decidir cuál es el registro canónico (el del lab alimentado por este ciclo, o el del curador) y, si se mantienen los dos, escribir en ambos la referencia. Sin decisión, las lecciones de la ventana existen sólo en uno de los dos.

---

## 7. Próxima revisión

- **Semanal:** **2026-10-02 (viernes 14:30)**, según el motor (`30 14 * * 5`, `next_run_at` 2026-10-02T14:30:00+02:00; `repeat.completed` = 3). **Corrige** el «2026-10-01» que figuraba como fecha de mensual (F5).
- **Mensual (paso 5):** **incubadora completa CP-001..CP-011** → ascenso a `KNOWN.md`/`HYPOTHESIS.md`, descarte o fusión. Solapes declarados a resolver: CP-008 / CP-009 / CP-010 (estado documentado, instrumento sin disparador, instrumento que miente) **+ CP-011** (el escritor que devuelve OK). Candidatos a E1 con más evidencia: CP-009 (5+2 ocurrencias) y CP-010 (3+2).
- **Vigilar en la próxima:** (1) si `consolidador-sesiones` produce algo antes del 02-10 (la noche del 25-09 es la primera prueba tras la racha de 3 fallos); (2) si alguien repara los 2 bloques truncados (D8) o vuelven a aparecer nuevos; (3) si el curador sigue escribiendo con el estado leyéndose `PAUSED`; (4) el resultado del RSI v0 (¿se decide el rumbo del bucle?) y los 23 ficheros sin commitear.

---

*Documento generado: 2026-09-25 (viernes). Fecha/hora verificadas con `date` (14:32:14 CEST). Hora del ciclo según `jobs.json`: dispatched 2026-09-25T14:30:17.610266 (`on_time`, lateness 17.6 s).*
*Fuentes citadas (todas leídas/medidas en esta sesión; sólo lectura salvo las escrituras declaradas en D1-D3): `lpa/incidentes/` (ls + búsqueda), `~/.hermes/cron/jobs.json` (`lpa-revision-incidentes-semanal` 05de86a93257, `consolidador-sesiones` 9474f6f3d224, one-shot 8717d7fa34ad), `04-operations/metrics/sesiones/` (rejilla `sesiones-*` y `resumen-dia-*`), `04-operations/metrics/telemetria/` (17→24 sep), `01-knowledge/observations/` (OBS-134..138), `04-operations/metrics/retrabajo_ledger.jsonl` (contenido literal), `04-operations/metrics/lecciones_ledger.jsonl` (wc -l = 9 antes), `~/.hermes/skills/.curator_ledger.jsonl` (1.282 líneas; conteo por actor/fecha; ts de los patches), `~/.hermes/skills/joko-lab/validacion-instrumentos-medicion/SKILL.md` (stat + líneas 28-36), `~/.hermes/skills/render-html-a-imagen/SKILL.md` (stat + líneas 115-124), `~/.hermes/skills/software-development/perfume-ia/references/capa-lpa-recomendacion.md` (línea 33), `hermes curator status` (literal), `git -C ~/joko-lab log/status`, `~/joko-lab.BACKUP.*` y `~/hermes-lab.BACKUP.*`, `04-operations/backlogs/pendientes.md` (líneas 303-372).*
