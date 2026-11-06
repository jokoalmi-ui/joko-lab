---
title: "REVISIÓN MENSUAL LPA — 2026-11 (ciclo mensual, deuda del 02-11 cerrada)"
type: knowledge
---

# REVISIÓN MENSUAL LPA — 2026-11

> **Fecha real de ejecución:** 2026-11-06 17:40 CET (`date`), viernes.
> **Nominal del ciclo:** 2 de noviembre, 13:30. Se ejecuta **4 días y 4 h tarde** (catch-up): el job `b2c498369692` (`lpa-revision-mensual`, `30 13 2 * *`) existe desde el 06-11 y **nunca se ha ejecutado** (`last_status: null` en `~/.hermes/cron/jobs.json`). No hay acta de noviembre anterior: esta es la primera.
> **Alcance:** parte **mensual** de la operativa de la skill `lpa`. No repite el trabajo del ciclo semanal (`lpa-revision-incidentes-semanal`, acta `revision-fallos-2026-11-06.md`, ya ejecutado hoy a las 14:35).
> **Escrituras:** esta acta, `KNOWN.md` (3 ascensos), `CHANGELOG.md`, y 3 fichas de CP. Backups RULE-008 `.bak-20261106` de cada fichero modificado. **Sin commit. Sin tocar producción, servicios ni n8n.**

---

## 0. Idempotencia

No existía `lpa/incidentes/revision-mensual-2026-11.md` (listado del directorio, 06-11 17:40): la revisión de este mes **no estaba hecha** y se hace ahora. Las demás actas del directorio son semanales (`revision-fallos-*`) o de septiembre (`*-incidentes.md`, `auditoria-estado-lab.md`).

---

## 1. Criterio aplicado (declarado antes de decidir)

Un CP se promueve si cumple **las tres**:

1. **≥ 2 ocurrencias en contextos distintos** (no dos lecturas del mismo evento).
2. **Condición de falsación escrita** en su ficha, citable literalmente.
3. **Sin hueco declarado de instrumento o denominador** que haga poco fiable el recuento de ocurrencias. Un CP en E0 cuyo recuento depende de un registro que no retiene la ventana **no se promueve**: ausencia de registro no es ausencia de fallo.

No se ha promovido nada «por antigüedad» ni por número de menciones en el backlog. Cuatro fichas (CP-001, CP-002, CP-003, CP-00X) llevaban **tres meses sin decisión** (fecha de revisión 2026-08-01, nunca ejecutada): se mantienen con razón escrita y **fecha tope nueva**, no se promueven por compensación.

---

## 2. Inventario de la incubadora (20 fichas)

`CP-001` … `CP-019` + `CP-00X` = **20**. (Además hay `H-001`, `KEL` y `TEMPLATE`, que no son CP.)

| CP | Tema | Nivel | Decisión 2026-11 |
|---|---|---|---|
| CP-001 | Colaboración > modelo único | E0 | Mantener |
| CP-002 | Pensar antes de codificar | E0 | Mantener |
| CP-003 | Ciclo de validación del conocimiento (KVC) | E0 | Mantener |
| CP-004 | Roles epistemológicos | E0 | Mantener |
| CP-005 | Gobernanza del conocimiento | E0 | Mantener |
| CP-006 | Verificación por evidencia | E0 | Mantener |
| CP-007 | Auditar antes de actuar | E0 | Mantener |
| CP-008 | Estado real ≠ estado documentado | E0 | **PROMOVER → E1-009** |
| CP-009 | Instrumento sin disparador se degrada | **E1-007** | Ya promovido (2026-10-02) |
| CP-010 | Instrumento no validado miente | **E1-008** | Ya promovido (2026-10-02) |
| CP-011 | Escritura truncada sin fallo | E0 | Mantener |
| CP-012 | El `unknown` se resuelve en el artefacto | E0 | **PROMOVER → E1-010** |
| CP-013 | Jobs en ventana de apagado no corren a su hora | E0 | Mantener |
| CP-014 | Fallo en cadena se registra en el consumidor | E0 | Mantener |
| CP-015 | La corrida que muere sin artefacto no deja señal | E0 | Mantener |
| CP-016 | Vigilante reinicia servicio sano por falta de red | E0 | Mantener |
| CP-017 | `resolved` mide la corrida siguiente, no la reparación | E0 | **PROMOVER → E1-011** |
| CP-018 | La firma incluye el dato que cambia cada intento | E0 | Mantener |
| CP-019 | La entrega del turno de medianoche cae en el apagado | E0 | Mantener (nuevo, 06-11) |
| CP-00X | Workflow como unidad de conocimiento | E0 | Mantener |

**Totales:** 20 fichas · 3 promovidas hoy · 2 ya estaban promovidas (CP-009, CP-010) · **15 mantenidas en incubación** · **0 descartadas**.

---

## 3. Promociones a `KNOWN.md` (3)

### 3.1 CP-008 → `E1-009` «El estado documentado diverge del estado real, y la divergencia no se detecta sin muestreo»

- **Ocurrencias:** **13** (12 del recuento de la ficha + 1 nueva en la ventana 25-09→02-10), en **8+ dominios** (systemd, kanban, docs canónicos, salud del conocimiento, repo git, memoria, config, logs) y en **3 fechas distintas** (02-09 las 8 primeras; 18-09 cadencia doc↔motor y BD↔registro; 25-09 registro de lecciones declarado vs real y resumen del curador vs su ledger), más 4 correcciones previas del backlog.
- **Falsación (literal, copiada):** «Sería FALSO si: durante 2 ciclos LPA consecutivos (2 meses), un muestreo de 10 afirmaciones de estado extraídas de documentos del lab contra su fuente real NO encuentra ninguna divergencia relevante (que hubiera llevado a una acción incorrecta de haber actuado sobre el documento).»
- **Por qué se promueve:** es la ficha con más evidencia de la incubadora y la única con las tres fechas separadas en el tiempo. Cumple el criterio completo.
- **Limitación declarada:** todas las ocurrencias son del Experimento 004 (joko-lab) → **E1 «patrón observado»**, no habilita reglas estructurales.

### 3.2 CP-012 → `E1-010` «El estado `unknown` no se resuelve en el motor: se resuelve en el artefacto»

- **Ocurrencias:** 5 en 5 jobs distintos (02-10) + 2 reexámenes independientes que **no dispararon la falsación** (09-10: dos `unknown` resueltos en las dos direcciones, producto presente y producto ausente; 16-10: el `unknown` del consolidador tapaba un OOM real, no un reinicio; 20-10: incidencia cerrada en el mismo segundo en que apareció el producto, 79.753 B).
- **Salto de mecanismo que faltaba:** la serie empezó con `unknown` por reinicio del planificador (incertidumbre benigna). El 16-10 aparece el **primer `unknown` con causa de fallo real (OOM del worker en su cgroup de 4 GiB)** → ya no es un solo mecanismo.
- **Falsación (literal, copiada):** «Sería FALSO si, sobre N=10 ejecuciones que terminan en `unknown` en el lab y durante 2 ciclos LPA consecutivos, 8 o más se resuelven consultando únicamente el estado del motor (sin ir al artefacto) con un veredicto correcto (efectos sí / efectos no) verificado después contra el producto.» (segunda vía: artefacto existente pero incompleto o engañoso).
- **Limitación declarada:** un solo experimento (joko-lab) → E1 «patrón observado». El antídoto decide **efectos**, no **causa** (esto último queda como límite escrito, ya en CP-015).

### 3.3 CP-017 → `E1-011` «`resolved` mide la corrida siguiente, no la reparación»

- **Ocurrencias:** 3 medidas en 2 jobs distintos y **4 fechas**: dos cierres sin reparación (23-10), el historial sobrescrito de la fila `264c02_761c7f27bcb0` (13-10 → 23-10 → 26-10, tres lecturas de la misma fila), y la reapertura del 01-11 que volvió a cerrar el 02-11 sobrescribiendo `closed_at` del 28-10 (acta 06-11, F3).
- **Contraejemplos declarados:** 2 cierres **sí** con reparación verificable (`bbc1d8` el 28-10 con OAuth renovado; `da39a2` el 26-10 con mtime del productor + 10 salidas limpias). Un patrón que admite contraejemplos es más fuerte, no más débil: el defecto es el criterio, no la imposibilidad de cerrar bien.
- **Falsación (literal, copiada):** «Sería FALSO si, sobre 10 incidencias cerradas del lab en 2 ciclos consecutivos, en 8 o más el cierre coincidiera con un cambio verificable en el productor (script/config con mtime posterior al `first_seen_at` y producto generado después) y el registro conservara el histórico de ocurrencias (reabrir no borra el cierre anterior). También lo falsaría que el lab no usara nunca `resolved` como prueba de reparación.»
- **Limitación declarada:** un solo registro de incidencias (`cron_incidents`) → E1 «patrón observado».
- **Pendiente que NO se resuelve aquí:** el §8 de la ficha (criterio de cierre de 3 condiciones + 7 días sin recurrencia) **asciende a `procedures/` o no** — ver §7, decisión del usuario.

---

## 4. Mantenidos en incubación (15) y por qué

- **CP-001** (colaboración > modelo único, 6 instancias / 5 dominios): cumple el recuento, pero **nunca se ha reexaminado desde julio** (revisión 2026-08-01 sin ejecutar) y sus instancias son del corpus de diseño de LPA, no de un instrumento que se pueda volver a medir. Promoverlo hoy sería promover por el texto de la ficha, no por evidencia nueva. **Tope 2026-12-02**: recontar instancias y decidir.
- **CP-002** (pensar antes de codificar): sin recuento de ocurrencias propio en la ficha; misma deuda de revisión. **Tope 2026-12-02**.
- **CP-003** (KVC): sin ocurrencias medidas; es un procedimiento propuesto, no un patrón observado. Cumple el criterio recién cuando se aplique y se mida. **Tope 2026-12-02**.
- **CP-004** (roles epistemológicos): su propia condición es «evidencia en 2+ dominios» y hay uno. No cumple.
- **CP-005** (gobernanza): su condición es «>20 DECs y primeros conflictos de autoridad»; sigue sin cumplirse. No cumple.
- **CP-006** (verificación por evidencia, 3 ocurrencias): las tres son **de un mismo día (24 h)**. Cumple contexto, no ocasiones distintas. **Tope 2026-12-02**.
- **CP-007** (auditar antes de actuar, 3 ocurrencias): igual, todas en 24 h (01-09). **Tope 2026-12-02**.
- **CP-011** (escritura truncada): 2 ocurrencias en 2 skills + 1 reforzada, pero **falta el denominador** (cuántas ediciones largas salen bien) → hueco de instrumento, no se promueve. Los bloques truncados citados en el acta del 25-09 (D8) **no se han remedido hoy**: no se afirma que sigan ahí.
- **CP-013** (ventana de apagado): 7 ocurrencias / 6 propósitos, **3 noches medidas** (09-10, 15-16-10, 22-23-10) pero **un solo host** y el mecanismo (suspensión vs reinicio) no está aislado. Falta segundo host/entorno.
- **CP-014** (fallo en cadena): 4 filas / 3 jobs, pero **todas nacen de un solo evento raíz** → no cumple «contextos distintos».
- **CP-015** (corrida sin artefacto): 3 caras medidas, **un solo job silencioso y un solo vigía**. Su antídoto está verificado en 1 job (productor con exit 3) pero el vigía `watchdog-informes-cron.py` sigue sin leer la cabecera declarativa.
- **CP-016** (vigilante reinicia servicio sano): antídoto aplicado (script corregido 26-10 17:45) y **0 reinicios en 7 días** frente a 4 en 3 noches. La falsación pide **10 noches con red caída y host encendido**: hay 2. Y el instrumento no da para más (§6.2: los artefactos del vigilante retienen ~21 h).
- **CP-018** (firma con dato variable): 6 ocurrencias + 2 contrastes en 2 jobs, **un solo registro**; y la 7ª fila de hoy (acta 06-11, F1) confirma el patrón. No se promueve mientras el antídoto exija tocar el núcleo de Hermes (RULE-016) y no haya un segundo registro donde medirlo.
- **CP-019** (entrega del turno de medianoche, creado hoy): 9 noches de fallo de entrega medidas + 3 jobs con el mismo síntoma, pero **causa raíz no asignada** (apagado vs red vs `send_path_degraded`). Entra a incubación, no a KNOWN.
- **CP-00X** (workflow como unidad de conocimiento, 5 instancias): cumple recuento y falsación, pero su identificador no es un número de serie (`00X`) y **nunca se ha revisado**; el paso previo que su propia ficha propone (elevar KAP de procedimiento a workflow) no se ha ejecutado. **Tope 2026-12-02**, y renumerar la ficha como CP-020.

**Ninguna fusión y ningún descarte.** Relaciones ya declaradas y sin cambios: CP-008/CP-009/CP-010 (antídotos distintos), CP-011/CP-010 (no se fusionan, 02-10), CP-012/CP-015 (caras complementarias), CP-017/CP-010 (objetos distintos: regla de cierre vs instrumento cualquiera).

---

## 5. Deudas con fecha (leídas de `04-operations/backlogs/pendientes.md`, 1.874 líneas)

### Vencidas

| Deuda | Fecha tope | Estado real medido hoy |
|---|---|---|
| Revisión mensual LPA de noviembre | **2026-11-02** | **VENCIDA (4 días). Se cierra con esta acta.** |
| `retrabajo_ledger` con ≥1 asiento real | **2026-11-02 23:59** | **VENCIDA e incumplida en plazo.** El asiento llegó el **03-11 07:39** (7 h 40 min tarde): 2 líneas, 1.569 B. Cumple el contenido (E6, 28.250 tokens) pero **contradice la declaración de no-instrumento del 30-10** (`retrabajo_ledger.STATUS.md` prohíbe citarlo). Sigue pendiente de decisión (F7 / D7 del acta 06-11). |
| Vigía de informes: leer la cabecera declarativa (`GATE_OMITIDO`) y/o `jobs.json` | 2026-10-23 → 30-10 | **VENCIDA y abierta.** El falso ok del 15-10 quedó cerrado por el barrido (16-10), y el productor ya sale con exit 3 (26-10), pero `watchdog-informes-cron.py` sigue sin mirar `failure_streak`/`last_run_at`. Toca `~/.hermes/scripts/` → **requiere autorización explícita**. |
| CP-017 criterio de cierre (§8) | 2026-10-30 | **VENCIDA en parte.** El criterio se aplica en las actas desde el 23-10, pero **no está en `procedures/`** y no existe campo append-only de ocurrencias. Hoy el CP asciende a E1; el procedimiento sigue pendiente (§7). |

### Cumplidas (verificadas hoy, no se dan por buenas de memoria)

- **B — `rag-reindex-daily`** (tope de verificación 2026-11-02): **CUMPLIDA.** 50 artefactos retenidos (`2026-09-14` → `2026-11-06 08:04`); los **6** `timed out` que contienen son todos anteriores al cambio (**17-09, 28-09, 02-10, 07-10, 12-10, 16-10**) y **ninguno posterior**. El cierre del 26-10 se sostiene.
- **D — CP-016 antídoto del vigilante** (tope 2026-10-30): **CUMPLIDA** en su parte aplicable. Script corregido (mtime 26-10 17:45); **0** apariciones de `Reiniciando gateway` en los 50 artefactos del vigilante (05-11 20:57 → 06-11 17:55).
- **Revisión del `retrabajo_ledger`** (decisión C del 30-10: declararlo no-instrumento): cumplida, y **hoy contradicha por el uso real** (fila del 03-11).

### Abiertas, sin fecha tope declarada

- Juez de calidad del informe: el acta semanal de hoy cuenta **4 de 7 días sin veredicto** (`ERROR (?)` y `omitido`) con exit 0 en varios de ellos. **Cifra no remedida hoy** (viene del acta `revision-fallos-2026-11-06.md`). Toca el gate → decisión del usuario.
- Parche pendiente del Paso 0B de la skill `perfume-del-dia` (id `87bd1748`), staged por `skills.write_approval` (según el acta semanal del 06-11; no verificado hoy).
- CP-019: medir si las 4 reentregas en cola (20-10, 29-10, 01-11, 05-11) se entregaron.

---

## 6. Límites de instrumento vigentes (medidos hoy, solo lectura)

### 6.1 `executions` retiene ~1 día

`~/.hermes/cron/executions.db` (modo `ro`): **1.001 filas**, rango **2026-11-05T16:15:10 → 2026-11-06T17:55:21** = **25 h 40 min**. Estados: 1.000 `completed`, 1 `running`. Tope de 1.000 filas.

Consecuencia operativa: **ninguna revisión puede reconstruir el mes desde esta tabla**. La fila del `7b5207` del 03-11 que citaba el acta semanal ya no existe (no se puede verificar ni desmentir). Toda la evidencia de este acta viene de fichas, `jobs.json`, artefactos y `pendientes.md`, no de `executions`.

### 6.2 Los artefactos del vigilante de Telegram también retienen ~1 día

`~/.hermes/cron/output/264c02dae003/`: **50 ficheros**, del **2026-11-05 20:57** al **2026-11-06 17:55** (≈ 21 h). **0** líneas `Reiniciando gateway`.

Consecuencia: el antídoto de **CP-016** se mide con un instrumento que solo ve el último día, mientras su falsación pide **10 noches**. La cuenta «0 reinicios» es correcta sobre lo retenido, no sobre la ventana de la falsación. El patrón no se promueve por esto.

### 6.3 `cron_incidents` conserva histórico, pero cuenta mal

28 filas, todas `resolved`; el cierre se concede con la corrida siguiente (CP-017) y la firma incluye la fecha (CP-018) → sirve para saber qué está rojo, **no** para contar ocurrencias. Es el argumento más fuerte para arreglar la firma.

### 6.4 `retrabajo_ledger` es un no-instrumento que volvió a escribir

2 líneas; la segunda, del **03-11 07:39**, después de la declaración del 30-10. No se cita como dato en esta acta.

---

## 7. Pendiente de decisión del usuario (no se ha ejecutado nada)

1. **CP-017 §8 → `procedures/`**: ¿se escribe el procedimiento «`resolved` es hipótesis: exigir mtime del productor + producto posterior + 7 días sin recurrencia + no sobrescribir `closed_at`»? Cambia cómo se cierran incidencias, así que no se escribe sin autorización.
2. **CP-018 — antídoto en el núcleo de Hermes** (normalizar la firma antes de firmar; campo `occurrence_count`): RULE-016 prohíbe tocar Hermes sin 5 días de incidencias. Sin decisión.
3. **Retención de `executions`**: subir el tope de 1.000 filas. Tiene coste; sin decidir. Mientras no se decida, toda revisión mensual arrastra el §6.1.
4. **`retrabajo_ledger`**: la declaración de no-instrumento (30-10) y el `STATUS.md` están desactualizados respecto al uso real (fila del 03-11). ¿Se retira, se le da disparador, o se corrige la declaración?
5. **Juez de calidad del informe**: 4/7 días sin veredicto y 3 con exit 0. Toca el gate de producción.
6. **Job mensual `b2c498369692`**: existe con `30 13 2 * *`, **nunca ejecutado** (`last_status: null`). Hoy ha corrido como catch-up. Decidir si se mantiene el día 2 (y se acepta que el acta llegue un día después de la ventana mensual) o se mueve al día 1 a las 13:30. La deuda del 30-11 queda cubierta por la existencia del job, pero **no por su historial** (0 ejecuciones).
7. **CP-00X**: renumerar como CP-020 o retirar la ficha con identificador no numérico.

---

## 8. Escrituras de este ciclo

| Fichero | Cambio | Backup |
|---|---|---|
| `lpa/incidentes/revision-mensual-2026-11.md` | nuevo (esta acta) | — |
| `lpa/KNOWN.md` | +E1-009, +E1-010, +E1-011; resumen E1 8→11, total 17→20 | `.bak-20261106` |
| `lpa/CHANGELOG.md` | entrada 2026-11-06 (3 ascensos, limitación declarada) | `.bak-20261106` |
| `lpa/pattern-incubator/CP-008-…md` | §7: promovido a E1-009 + `status: promoted` | `.bak-20261106` |
| `lpa/pattern-incubator/CP-012-…md` | §7: promovido a E1-010 + `status: promoted` | `.bak-20261106` |
| `lpa/pattern-incubator/CP-017-…md` | §7: promovido a E1-011 + `status: promoted` | `.bak-20261106` |

Registro aditivo: no se ha reescrito histórico; los bloques de reexamen anteriores se conservan íntegros y los ascensos se añaden como bloque nuevo.

**No se ha tocado**: producción, servicios, `n8n`, `~/.hermes/scripts/`, el núcleo de Hermes, ni ningún cron. Sin `sudo`. Sin commit git.

---

FIN DEL ACTA
