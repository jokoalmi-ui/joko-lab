---
title: "REVISIÓN DE FALLOS — 2026-11-20 (ciclo semanal LPA, D0/INC-005)"
type: knowledge
---

# REVISIÓN DE FALLOS — 2026-11-20

> **Fecha real de ejecución:** 2026-11-20 14:30 CET (`date`), viernes. Host `up 2 days, 15 hours, 58 minutes` (`uptime -s` = 2026-11-17 22:33:34).
> **Ventana revisada:** 2026-11-13 17:29 → 2026-11-20 14:30 (7 días).
> **Fuente:** `~/.hermes/cron/executions.db` en **solo lectura** (`mode=ro`), `jobs.json`, artefactos de `~/.hermes/cron/output/<job>/`, `journalctl --user` (gateway, boots, errores de `vision_analyze`), `04-operations/reports/*-informe-local.txt`, `04-operations/metrics/sesiones/`, código de `tools/registrar_hel_diario.py` y `~/.hermes/scripts/consolidador_sesiones.py`, y la API de LM Studio `:1234` (solo lectura).
> **Ningún servicio tocado.** Escrituras: esta acta, 3 reexámenes con backup RULE-008 `.bak-20261120`, **5 lecciones** en el ledger (con backup del propio ledger) y 3 parches de skill **staged, pendientes de aprobación** en `04-operations/proposals/skill-patch-2026-11-20-vision-y-cierres.md` — no aplicados.

---

## 0. Incidentes de la ventana (paso 1)

**No hay ningún `*-incidentes.md` nuevo en `lpa/incidentes/` desde el 01-09-2026.** El único fichero narrativo sigue siendo `2026-09-01-incidentes.md` (mtime 03-09-2026). **No se fuerza ninguna promoción por ese frente.**

La ventana se reconstruye con `cron_incidents` (**33 filas**, antes 31) y con los artefactos. Filas tocadas en la ventana (**3, todas del mismo job**), todas cerradas en el **mismo instante** `2026-11-15T22:35:02.515752`:

- `41a1a4_3c4b8c91fffb` — `first_seen` **13-11 17:23:32**, `script`, «hay dias con sesiones en state.db y sin fichero consolidado».
- `41a1a4_6472980b291b` — **13-11 22:35:22**, mismo `error`.
- `41a1a4_2288feb11262` — **14-11 22:35:02**, mismo `error`.

**Incidencias nuevas desde el 15-11: 0.** El único job con `last_status=error` en `jobs.json` (`bbc1d841e8a7`, empleo-pipeline, fallo del **19-11 18:05**) **no tiene fila en `cron_incidents`** — ver F2.

---

## 1. Actividad de la ventana (contexto verificado)

- **Arranques del host: 4** (`journalctl --user --list-boots`): 14-11 19:51, 14-11 22:32, 16-11 23:07 y 17-11 22:33. Sin arranques desde el 17-11 (racha de 2 d 16 h, la más larga en semanas).
- **`executions`: 1.001 filas**, que cubren solo **2026-11-19 20:54 → 2026-11-20 14:36 (≈ 17 h 42 min)**. Reparto: **1.000 `completed`, 1 `running`, 0 `failed`, 0 `missed`**. El tope de filas sigue recortando: la ventana visible **se ha reducido de 44 h a 18 h** en una semana (D5).
- **`jobs.json`: 65 jobs, 63 activos** (62 `ok`, 1 `error` = `bbc1d841e8a7`, 2 sin estado).
- **Informes diarios (`67d5fcc5b69e`): 7/7 presentes** (14→20-11), todos entre 09:00 y 09:02. Gate: **7 × `OK_INTERNO`**. Motor: **6 con `openai/gpt-oss-20b`**, **1 con `lfm2.5-vl-3b` → `CALIDAD: ERROR (?)`** (16-11). Los otros 6: 4,8 · 5,0 · 4,53 · 5,0 · 4,8 · 5,0.
- **Ficha de perfume (`8bf412ac2ba3`): 8 artefactos** (13→20-11), **uno por día, ninguno de 0 bytes** (85.753–90.791 B). Arranques: 17:57 (catch-up del 13-11), y 10:24–10:54 el resto → **24–54 min después del slot de 10:00**.
- **Gateway:** 4 `Started hermes-gateway` y **3 salidas `UNCLEANLY`** (14-11 19:51, 16-11 23:07, 17-11 22:33), **cero líneas `Stopped`**. En las 3, el `last_heartbeat` cae **~60 min antes** del arranque siguiente (18:49 / 22:06 / 21:33) → ver F6.
- **Vigilante de Telegram (`264c02dae003`, cada 15 min):** 50 artefactos, **todos del 20-11** (≈ 12,5 h de retención). El último dice `OK - gateway conectado y Telegram responde`. **La afirmación del acta anterior («0 reinicios en 5 semanas») no era medible**: el directorio no guarda 5 semanas (D6).
- **Visión (`gemma-4-12b-qat`):** **0 cargas correctas** en toda la semana; **43 líneas** del modelo en 5 días (14, 15, 16, 17, 18-11), de ellas **34 `exited before becoming healthy`**; **18 errores `vision_analyze`** en **7 de 8 días**. El modelo **sí está** en la lista de LM Studio (`state: not-loaded`).

---

## 2. Fallos y hallazgos de la ventana

### F1. [CP-020, 2ª semana · empeora en transparencia] La visión no corre y ahora el veredicto se afirma sin traza
Sigue el fallo de carga (43 líneas, 34 `exited before becoming healthy`, 0 cargas OK). Pero el borde cambió de sitio y es peor:

- **4 fichas afirman un veredicto de visión**: 13-11 «VLM sobre el PNG suelto: sin letras ni marcos inventados»; 14-11 «visión local revisó el fondo suelto → sin letras…»; 18-11 «verificado por visión: lee «Papyrus Moléculaire / Maison Crivelli»»; 19-11 «VLM solo para lo atómico: sin texto inventado».
- **El journal de esos mismos días solo contiene fallos.** El 18-11: `10:07:34` → `Error code: 400 Failed to load model "google/gemma-4-12b-qat"`; `10:25:41` → `Auxiliary vision (async): request to http://localhost:1234/v1/ timed out after 180.0s`. El artefacto con la afirmación se escribió a las **10:26:46**, 65 s después del timeout.
- **1 sola ficha declara la degradación** (17-11: «`vision_analyze` no operativo… identidad avalada por procedencia oficial»). **3 son silenciosas** (15, 16 y 20-11). El 20-11 el intento falló por una **ruta con errata** (`/home/jokoaml/...`, 4 líneas `jokoaml` en el journal) y el informe no menciona visión en absoluto.

**Lo que no se puede afirmar y no se afirma aquí:** no hay prueba de que las 4 fichas mientan. La vía de respaldo documentada (`glm-4.6v-flash`) **existe** en LM Studio y sus llamadas por `curl` no dejan rastro en el journal. Lo que sí está medido es que **la verificación no es trazable**: un `vision_analyze` correcto no escribe ninguna línea. Con esa traza, «verificado por visión» y «no verificado» son indistinguibles — que es exactamente el borde que CP-020 dice que hay que cerrar.

**Condición de falsación nº 2 de CP-020: NO se cumple** (7 fichas con el chequeo ejecutado + aviso de degradación cuando no se ejecuta). Han sido 8 fichas: 0 ejecuciones confirmadas, 1 aviso de 8.

### F2. [NUEVO · credencial, no código] El token OAuth de Gmail está revocado: el pipeline de empleo no puede enviar
`19-11 18:05:04`, job `bbc1d841e8a7` (`empleo-pipeline-diario`), `Status: script failed`, `exit 1`:

```
google.auth.exceptions.RefreshError: ('invalid_grant: Token has been expired or revoked.', ...)
```

Tercera vez en la ventana amplia: **27-10, 11-11 19:37 y 19-11**. Es un fallo de credencial, no de código: no se arregla tocando el script. `jobs.json` lo marca `error`; **`cron_incidents` no tiene fila para ese fallo** (la última del job es del 11-11/12-11). Es decir: **el semáforo se pone rojo y el registro de incidencias no se enteró** → nadie lo está mirando por el canal que sirve para mirar. Requiere acción del usuario (reautorizar OAuth) y no se ha tocado nada.

### F3. [CP-017 · 3er mecanismo de cierre falso] Cerrado «por salida de ventana», no por reparación
El hueco del **12-11** (45 sesiones en `state.db`, sin `sesiones-delta-20261112.jsonl`) generó **3 alertas** y las 3 se cerraron a la vez el **15-11 22:35:02**. El hueco **no se reparó: salió de la ventana de 3 días** que mira `registrar_hel_diario.py` (`objetivo = [hoy-2, hoy-1, hoy]`). El 15-11 ya no se miraba el 12-11, y el job salió `ok`.

Causa literal, verificada en código: el consumidor busca el fichero **nombrado por el día consolidado** (`registrar_hel_diario.py:160-165`: `sesiones-delta-<dd>.jsonl`) y el productor escribe el delta **nombrado por el día en que corre** (`consolidador_sesiones.py:121`: `sesiones-delta-{hoy}`). Cuando el consolidador rellena hacia atrás un día que se perdió, ese día **nunca tendrá delta con su propio nombre** → alerta segura. El resumen diario **sí existe** (`resumen-dia-2026-11-12.md`, mtime 13-11 22:30:50, «Sesiones del dia 2026-11-12: 45»), así que la consolidación se hizo: lo que falta es el nombre del artefacto.

De las 3 alertas, **1 fue verdadera** (13-11 17:23: el resumen aún no existía) y **2 fueron falsas** (13-11 22:35 y 14-11 22:35: el resumen llevaba 4 min escrito). Es **1 causa con alertas repetidas**, no 2 ocurrencias en contextos distintos → **lección, no CP** (D3).

### F4. [CP-017 · cierre nº 3 roto a los 7 días] El pipeline de empleo volvió a fallar sin abrir incidencia
El cierre del 12-11 duró **7 días exactos** y volvió a romperse el **19-11**. Sin fila en `cron_incidents`. El criterio escrito (7 días sin recurrencia) quedó cumplido al día y aun así falló — segunda medición que invalida la cifra fija.

### F5. [CP-010, 10ª ocurrencia] Un solo día con el respaldo y ese día sin veredicto
**1 de 7** informes con `lfm2.5-vl-3b` (16-11) y ese es el único `CALIDAD: ERROR (?)`. La proporción mejora (era 4 de 7) pero el mecanismo es idéntico: el respaldo de carga es un modelo de visión sirviendo de motor de texto y el juez no puede puntuar ese sustrato.

### F6. [CP-016, 6ª semana · y corrección de medición] El vigilante vive dentro de lo vigilado
**3 de 4 arranques** con `exited UNCLEANLY` y **cero `Stopped`**: el gateway no muere por una parada ordenada. Los `last_heartbeat` (18:49 → arranque 19:51; 22:06 → arranque 23:07; 21:33 → arranque 22:33) marcan una hora de silencio **con el host encendido** en los dos últimos casos. El watchdog corre cada 15 min como job de cron de Hermes, es decir **dentro del proceso que debería reiniciar**: si el gateway muere, el watchdog muere con él y no puede levantar nada. Sus artefactos duran ~12,5 h, así que **tampoco hay serie histórica con la que contradecirlo**. La frase del acta anterior («0 reinicios en 5 semanas, antídoto sostenido») **se retira**: no era medible.

### F7. [SIN ACCIÓN] La doble entrega manual de la ficha no se repitió
8 días, **1 ficha por día**, ninguna manual (`source=direct`) en la ventana. La condición que se fijó («3ª vez abre CP») no se cumple. No se abre nada.

### F8. [CP-015, sin novedad] Ningún artefacto de 0 bytes en la ventana
Las 8 fichas pesan 85–90 KB. El par (0 B + `interrupted`) no se ha repetido: no hay evidencia nueva ni a favor ni en contra del criterio propuesto (D6 anterior).

---

## 3. Decisiones D0..D10

**D0 — Fuente y alcance.** Sin `*-incidentes.md` nuevos desde el 01-09. Se revisa `cron_incidents` (33 filas), `executions` (1.001 filas, 17 h 42 min), 8 fichas, 7 informes, journal del gateway y de visión, boots, código de HEL/consolidador y la lista de modelos de LM Studio. **No se fuerza ninguna promoción por falta de material narrativo.**

**D1 — CP-020 sigue abierto y se anota su empeoramiento.** El fallo ya no es «no se ejecuta y se declara»: es «no hay traza que distinga ejecutado de no ejecutado», con 4 fichas afirmando veredicto y 3 en silencio. **Sin ascenso de nivel** (sigue E0): falta el control con VRAM libre y ahora además falta el instrumento de traza. Mejora propuesta, sin aplicar: que `vision_analyze` escriba una línea de éxito (modelo, ms, ruta) además de las de error, en el artefacto o en el journal.

**D2 — F2: fallo de credencial, se separa del código.** El `invalid_grant` no es un patrón de diseño: es un token revocado. **No abre CP** (3 ocurrencias, misma credencial, mismo contexto: renovación OAuth caducada). Se registra lección y se deja como **acción del usuario**: reautorizar el flujo OAuth de Gmail. Mientras no se reautorice, el pipeline de empleo sigue fallando a diario a las 18:05 y **no genera incidencia**.

**D3 — F3: lección, no CP.** Una causa (noche de consolidación perdida el 12-11) con 3 alertas, 2 de ellas falsas por desajuste de nombre productor/consumidor. Se registra lección y se anota el defecto de código. **No se toca** `registrar_hel_diario.py` ni `consolidador_sesiones.py` en este ciclo (herramientas de producción, sin autorización). Recomendación en D9.

**D4 — CP-017: tercer mecanismo de cierre falso documentado.** (1) «hubo una corrida sana»; (2) «cerró el día que se volvió a ejecutar»; (3) **«salió de la ventana de 3 días»**. Se añade la comprobación al ciclo: *¿el cierre coincide con un cambio de causa o con un cambio de ventana?* Sin cambio de procedimiento (toca `procedures/cierre-de-incidencia.md`, decisión del usuario).

**D5 — CP-013 / retención: empeora y desarma el registro.** La ventana visible de `executions` bajó de 44 h a **17 h 42 min** con el mismo tope de ~1.000 filas. **0 `missed` visibles no significa 0 `missed`**: significa que el registro no llega. Con esta retención, **ningún `resolved` es defendible** (D2 del acta anterior queda confirmado, no matizado).

**D6 — CP-016: se retira una afirmación del acta anterior y se anota un fallo estructural.** El watchdog no tiene serie histórica (50 ficheros ≈ 12,5 h) y corre **dentro** del servicio que vigila. La combinación «vigilante dentro de lo vigilado + sin retención» hace que su silencio no sea evidencia de nada. Sigue E0.

**D7 — Ficha diaria: sin acción.** No hay doble entrega ni artefacto vacío. Se anota la latencia de arranque (24–54 min sobre el slot de 10:00) como observación, no como fallo: no hay umbral validado para llamarla fallo (RULE-015).

**D8 — Revisión mensual: no toca.** La mensual es un job aparte (`b2c498369692`, `30 13 2 * *`); la última fue `revision-mensual-2026-11.md` y la próxima cae el **2026-12-02 13:30**. Hoy es la semanal del 20-11. **No se promueve nada a `KNOWN.md`/`HYPOTHESIS.md`.**

**D9 — Recomendaciones, sin ejecutar.**
1. Reautorizar OAuth de Gmail (F2) — requiere al usuario.
2. Traza de éxito en `vision_analyze` (D1).
3. `registrar_hel_diario.py`: aceptar `resumen-dia-<fecha>.md` como prueba de consolidación, o que el consolidador nombre el delta por el día consolidado (F3).
4. Corregir `TZ = timedelta(hours=2)` en las herramientas que fechan a mano (D11 del acta anterior; **sigue sin corregir**, comprobado hoy en `registrar_leccion.py:33`).

**D10 — Escrituras del ciclo.** Acta nueva; reexámenes en `CP-010`, `CP-017` y `CP-020` con backup `.bak-20261120`; **5 lecciones** en `04-operations/metrics/lecciones_ledger.jsonl` (con backup previo del ledger: 34 → 39 filas); 3 parches de skill **staged** en `04-operations/proposals/skill-patch-2026-11-20-vision-y-cierres.md` (**no aplicados**). **Sin commit. Sin tocar servicios, contenedores, n8n ni `tools/`.**

**Nota de instrumento:** `registrar_leccion.py` sigue fechando con `UTC+02:00` fijo. Las 5 lecciones de hoy quedaron selladas a las **15:36 UTC+02:00** cuando la hora real era **14:36 CET (UTC+01:00)**: **+1 h**, el mismo defecto ya anotado (D11 del acta anterior). Los datos son correctos; la hora del sello, no.

---

## 4. Estado de la cadena incidente → lección → mejora

- **Visión (`gemma-4-12b-qat`)** → 43 líneas de fallo, 18 errores, 7/8 días → **CP-020 (D1)** → **sin mejora y con la transparencia a peor**: 4 afirmaciones sin traza, 3 silencios. Es el eslabón más roto: **fallo diario, producto entregado, verificación no auditable**.
- **Gmail (`bbc1d841e8a7`)** → token revocado, 3ª vez, sin incidencia → **D2** → **mejora bloqueada por el usuario**: sin reautorizar, el pipeline no envía.
- **HEL / consolidador** → 3 alertas, 2 falsas, cierre por ventana → **D3** → defecto de nombre localizado en código; mejora barata pendiente.
- **Empleo (cierre nº 3)** → 7 días exactos y se rompió sin incidencia → **D4** → el criterio de cierre sigue sin respaldo empírico.
- **Informe diario** → 1/7 con respaldo y `ERROR (?)` → **D5** → producto verde, calidad no medida.
- **Gateway / watchdog** → 3 UNCLEANLY sin `Stopped`, watchdog ciego y sin serie → **D6** → sin antídoto; una afirmación retirada.

---

## 5. Lecciones registradas (ledger, 20-11)

Fichero `04-operations/metrics/lecciones_ledger.jsonl`, filas 35–39 (backup `.bak-20261120`, 34 filas previas):

| # | Dominio | Lección |
|---|---|---|
| 35 | proceso | Un fallo de credencial revocado no abre incidencia: el semáforo rojo no dice qué arreglar (F2) |
| 36 | observabilidad | Un veredicto afirmado sin traza positiva no es un chequeo (F1) |
| 37 | proceso | El consumidor busca el artefacto por el día que consolida y el productor lo nombra por el día que corre (F3) |
| 38 | observabilidad | La retención del registro decide qué cierres son defendibles: 18 h no sostienen un `resolved` (D5) |
| 39 | observabilidad | El vigilante corre dentro del servicio vigilado y su serie dura 12 h (F6) |

**Patrones promovidos a `pattern-incubator/`: 0.** No hay ningún patrón nuevo con 2+ ocurrencias en contextos distintos en esta ventana: el candidato aparente (productor/consumidor de artefactos) es **1 causa con 3 alertas**, y se ha registrado como lección (fila 37), no como CP. **Patrones descartados: 0** (no había ninguno en condiciones de descarte).

---

## 6. Próxima revisión

**Viernes 2026-11-27, 14:30 CET** (motor `lpa-revision-incidentes-semanal`, id `05de86a93257`, `30 14 * * 5`). Comprobaciones mínimas:
1. ¿Se reautorizó el OAuth de Gmail? Si no, contar días sin envío desde el 27-10.
2. ¿Aparece alguna traza positiva de `vision_analyze` (modelo cargado + análisis devuelto)? Si sigue a 0, CP-020 sube de gravedad, no de nivel.
3. ¿Se repite la doble entrega manual de la ficha? (sigue en 0 desde el 12-11).
4. ¿Abre incidencia el próximo fallo de `bbc1d841e8a7`? Si no, el hueco de cobertura de F2 es estructural.
5. Retención real de `executions`: si sigue bajo 24 h, cerrar incidencias deja de tener sentido y hay que decirlo por escrito.
6. Vigilante: ¿cuántos ficheros conserva y cubre alguna noche completa?
