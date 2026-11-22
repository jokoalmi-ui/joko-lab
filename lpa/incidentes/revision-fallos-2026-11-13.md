---
title: "REVISIÓN DE FALLOS — 2026-11-13 (ciclo semanal LPA, D0/INC-005)"
type: knowledge
---

# REVISIÓN DE FALLOS — 2026-11-13

> **Fecha real de ejecución:** 2026-11-13 17:23 CET (`date`), viernes; host `up 2 minutes` (`uptime -s` = 2026-11-13 17:21:52). El host estuvo apagado desde el 12-11 21:52 hasta las 17:22 de hoy.
> **Ventana revisada:** 2026-11-06 14:34 → 2026-11-13 17:23 (7 días).
> **Fuente:** `~/.hermes/cron/executions.db` en **solo lectura** (`mode=ro`), `~/.hermes/cron/jobs.json`, artefactos de `~/.hermes/cron/output/<job>/`, `journalctl --user` (gateway y `--list-boots`), `04-operations/reports/*-informe-local.txt`, `~/.hermes/config.yaml` (solo lectura) y `nvidia-smi`.
> **Ningún servicio tocado.** Las únicas escrituras son las de este ciclo en `joko-lab`: esta acta, 1 expediente nuevo (CP-020), 4 reexámenes con backup RULE-008 `.bak-20261113`, 4 lecciones en el ledger (con backup) y 1 parche de skill **staged, pendiente de aprobación** (`/skills pending`, id `9ca06b6e`) — no aplicado todavía.

---

## 0. Incidentes de la ventana (paso 1)

**No hay ningún `*-incidentes.md` nuevo en `lpa/incidentes/` desde el 01-09-2026.** El único fichero de incidentes narrativos sigue siendo `2026-09-01-incidentes.md` (mtime 03-09). **No se fuerza ninguna promoción por ese frente.**

La ventana se reconstruye, como las semanas anteriores, con `cron_incidents` (31 filas: 29 `resolved`, 1 `closed`, 1 `detected`) y con los artefactos. Filas tocadas en la ventana (**4**):

- `8bf412_a4b094b52ae0` (job `8bf412ac2ba3`, ficha-perfume-diaria): `first_seen` **07-11 10:24:13**, `error = "interrupted"`, `failure_type=unknown`, cerrada el **07-11 12:17:05**.
- `bbc1d8_aba390737219` (job `bbc1d841e8a7`, empleo-pipeline): `first_seen` **11-11 18:05:52**, `timeout`, `Script timed out after 300s`, cerrada el **12-11 18:05:17**.
- `bbc1d8_a5731c9ceec0` (mismo job): `first_seen` 24-10, `last_seen` **11-11 19:37:18**, `script`, cerrada **12-11 18:05:17** (sobrescribiendo el cierre del 02-11).
- `41a1a4_3c4b8c91fffb` (job `41a1a42060f4`, registrar-hel-diario): `first_seen` **13-11 17:23:32**, `script`, `Script exited with code 2`, estado **`detected`** al cerrar esta acta.

---

## 1. Actividad de la ventana (contexto verificado)

- **Arranques del host: 10** (`journalctl --user --list-boots`), uno por día salvo los dobles del 07-11 (09:38 apagón → 09:39 arranque) y 10-11 (22:53, 2 min). El apagón del 12-11 → 13-11 duró **19 h 30 min** (21:52:16 → 17:22:04): el más largo de las últimas semanas.
- **`executions`: 1.005 filas**, que solo cubren **2026-11-11 21:14 → 2026-11-13 17:24 (≈ 44 h)**. Reparto: 980 `completed`, **19 `missed`**, 5 `running`, 1 `failed`. El tope de filas sigue recortando la semana (D10 del acta anterior, sin cambio).
- **`jobs.json`: 64 jobs, 62 activos** (61 con `last_status=ok`, 1 con `error` = `41a1a42060f4`).
- **Informes diarios (job `67d5fcc5b69e`): 7/7 presentes** (07→13-11). Motor `openai/gpt-oss-20b` en 5 y **`lfm2.5-vl-3b` en 2** (10 y 12-11). Gate: **7 × `OK_INTERNO`**. Juez de calidad: **4 con veredicto** (5.0, 5.0, 4.73 y el del 13-11 omitido) → **3 sin veredicto** (`omitido` 07-11 y 13-11; `ERROR (?)` 10-11 y 12-11). El del 13-11 se generó a las **17:23**, no a las 09:00 (catch-up tras el arranque).
- **Ficha de perfume (`8bf412ac2ba3`): 8 artefactos** en la ventana (07-11: 2, uno de **0 bytes**; 08→12-11: 1 diario; 12-11: **2 corridas `direct`** además de la de la mañana).
- **Gateway:** 2 salidas `UNCLEANLY` en la ventana (07-11 09:39 y 13-11 17:22), ambas con `suspected_oom=False` y `last_heartbeat` en la franja del apagado nocturno → **la señal sigue sin discriminar** (D8 del acta anterior).
- **Vigilante de Telegram (`264c02dae003`): 0 líneas `Reiniciando gateway`** en todos sus artefactos. A la vez, **2 de sus turnos se marcaron `missed`** (noches del 11 y 12), es decir: no vigiló justo las noches de apagón.

---

## 2. Fallos y hallazgos de la ventana

### F1. [NUEVO · CP-020 abierto] El modelo de visión no carga y el producto se entrega sin el chequeo
`vision_analyze` apunta a `google/gemma-4-12b-qat` en LM Studio `:1234` (`config.yaml`, bloque de visión). En la ventana: **50 líneas `Failed to load model "google/gemma-4-12b-qat"`** (`engine … exited before becoming healthy. exitCode=1`), **6 líneas `Model is unloaded.`** y **17 marcas de tiempo distintas en 6 días consecutivos** (07, 08, 09, 10, 11, 12-11 — ningún día se libra). Cada intento quema 6,2–6,4 s hasta el 400 y después **180 s de timeout** del cliente auxiliar antes de caer al respaldo.

El consumidor no falla: **entrega el producto sin el chequeo** y lo declara solo dentro del artefacto. Cita literal (`cron/output/8bf412ac2ba3/2026-11-12_07-25-15.md`, línea 424):

> «**Chequeo visual por VLM no ejecutado**: `gemma-4-12b-qat` no carga (comfyui ocupa 8.080/12.282 MiB) y parar el servicio está bloqueado en modo cron (…). Por tanto **el fondo klein no ha sido revisado por visión** para descartar letras inventadas — solo validado estructuralmente.»

Medición de hoy (`nvidia-smi`): `8368 MiB / 12282 MiB` ocupados por `llama-server` de LM Studio (8.276 MiB). El ocupante cambia (ComfyUI el 12-11, `llama-server` hoy), el resultado no: quedan ~3,9 GB y un 12B no entra. **La causa propuesta no está aislada** (no se ha hecho el control con VRAM libre) y así consta en el expediente.

### F2. [CP-017, 2º cierre roto] El cierre «verificado» del 02-11 duró 9 días
`bbc1d8_a5731c9ceec0` se cerró el **02-11** y volvió a fallar el **11-11**: a las 18:05:52 `Script timed out after 300s` (artefacto de 229 B) y a las 19:37:18 una re-ejecución que **produjo un artefacto de 16.044 B y aun así terminó `exit 1`**, con un `stderr` que solo contiene un `FutureWarning` de `google-api-core` sobre Python 3.11. Los dos fallos se cerraron **en bloque el 12-11 18:05:17**. El criterio escrito (7 días sin recurrencia) lo habría dado por bueno **por dos días** → primera medición de que el umbral de 7 días tampoco basta.

### F3. [CP-010, 9ª ocurrencia] El respaldo de carga sustituye el instrumento y el producto sale sin veredicto
7 informes: **3 sin veredicto de calidad** (07-11 `omitido`, 10-11 `ERROR (?)`, 12-11 `ERROR (?)`, 13-11 `omitido` → 4 sin veredicto contando el de hoy) y **los 2 días que cayeron al respaldo `lfm2.5-vl-3b` dieron `ERROR (?)` los dos**. El respaldo configurado (`respaldo_carga`, por defecto `lfm2.5-vl-3b` en `tools/llm-router.sh:58-59`) es un modelo de **visión** de 3B sirviendo como motor de **texto**: el juez validado contra `gpt-oss-20b` no puede puntuar ese sustrato.

### F4. [NUEVO · lección] Falso fallo por orden de ejecución en el catch-up del arranque
Hoy a las **17:23:32** el job `41a1a42060f4` (`registrar-hel-diario`, cron `35 22 * * *`) terminó con **exit 2**: `ALERTA: hay dias con sesiones en state.db y sin fichero consolidado`. **36 segundos después** (17:24:08) el job `9474f6f3d224` (`consolidador-sesiones`, cron `30 22 * * *`) escribió `OK: 44 sesiones de 2026-11-12 — resumen en resumen-dia-2026-11-12.md`. Es decir: **el consumidor corrió antes que su productor** porque el catch-up no respeta el orden de dependencia, y abrió la incidencia `41a1a4_3c4b8c91fffb` (`detected`) por un hueco que dejó de existir 36 s después. El hueco era real en el instante de mirar; el veredicto «falta consolidar» no lo era. **1ª ocurrencia medida** → lección, no CP.

### F5. [CP-013, 4º ciclo] El estado `missed` ya cuenta los turnos perdidos — a medias
**19 filas `missed` en 2 noches sobre 9 jobs**, todas con `claimed_at` = arranque del host (11-11 22:12→23:00 y 12-11 20:52→23:00). **Asimetría medida:** el 13-11 el host estuvo apagado hasta las 17:22, así que también se perdieron los turnos diurnos (informe 09:00, ficha 10:00) — y esos **no** aparecen como `missed`: se re-ejecutaron en la ráfaga de las 17:23–17:26 (el informe de hoy lleva cabecera `2026-11-13 17:23 CET`). La misma causa produce dos registros distintos según la hora. Quien mida turnos perdidos solo con `missed` subestima el doble, y quien mida solo el producto ve un informe con la fecha correcta mirando un estado de hace 8 horas.

### F6. [CP-015, 9ª ocurrencia] Corrida adoptada y matada: artefacto de 0 bytes
07-11: **10:21:56** `Force-killed MCP process 9487 (lancedb) after SIGTERM timeout` → **10:21:58** `Stopped hermes-gateway.service` → **10:23:10** arranque → **10:24:13** ejecución adoptada que muere: artefacto `2026-11-07_10-24-13.md` de **0 bytes**, incidencia `interrupted`, cerrada 1 h 53 min después **sin causa asignada**. El par (0 B + `interrupted`) es una firma barata que hoy nadie usa como criterio.

### F7. [SIN ACCIÓN] Dos corridas manuales de la misma ficha el 12-11
`source=direct` (14:59 y 15:09), ambas `completed` y `delivered` (artefactos de 86.187 B y 86.906 B): dos entregas de la ficha del mismo día, cada una precedida por un fallo de visión (15:03 y 15:10). No se puede determinar desde los artefactos si la segunda sustituyó o duplicó la primera; se anota como observación, sin CP.

### F8. [CP-018, sin cambio] El registro semanal sigue degradado
4 filas nuevas en la ventana sobre 3 jobs distintos; `8bf412ac2ba3` y `bbc1d841e8a7` siguen con **1 firma por fila** (100 % únicas). El fallo de firma no se ha tocado (núcleo de Hermes, RULE-016). Las 19 filas `missed` no generan incidencia: correcto.

### F9. [NUEVO · instrumento] Cinco herramientas del lab fechan con CEST fijo: 1 hora de adelanto desde el 25-10
Al registrar la lección de F4, su `fecha` salió `2026-11-13 18:28 UTC+02:00` mientras `date` daba `2026-11-13 17:28 CET (+0100)`. Causa literal en `tools/registrar_leccion.py:33`:

```python
TZ = timezone(timedelta(hours=2))
```

Zona fija de verano. Desde el cambio de hora del **25-10-2026** toda marca escrita por esa herramienta va **1 h adelantada y etiquetada `UTC+02:00`** cuando el sistema está en CET (`timedatectl`: `Europe/Madrid (CET, +0100)`, reloj sincronizado). Afecta a **5 herramientas**: `registrar_leccion.py:33`, `local_cloud_orchestrator.py:39`, `verificar_hel.py:21`, `pipeline_seleccion_modelo.py:45` (comentario `# CEST`), `descargar_modelos_inactivos.py:32`, más `ventana_perfume.py:205`. **No se ha tocado ninguna** (son herramientas de producción y este ciclo no tiene autorización para modificarlas): queda como recomendación D11. Es el mismo fallo de familia que RULE-012 —una fecha afirmada sin comprobarla contra el reloj— pero automatizado dentro de la herramienta.

---

## 3. Decisiones D0..D11

**D0 — Fuente y alcance.** Sin `*-incidentes.md` nuevos desde el 01-09. Se revisa `cron_incidents` (31 filas), `executions` (1.005 filas, 44 h), artefactos de 7 jobs, journal del gateway, informes locales y `nvidia-smi`. **No se fuerza ninguna promoción por falta de material narrativo.**

**D1 — CP-020 abierto (nuevo expediente).** «El instrumento de visión no cabe en la VRAM, el chequeo se omite y el producto se entrega igual». Cumple la condición de promoción del ciclo: **2+ ocurrencias en contextos distintos** (ficha automática, corridas manuales de la ficha, informe diario) y **6 días consecutivos** de recurrencia medida. 7 campos del `TEMPLATE.md` completos, con **dos condiciones de falsación** (control con VRAM libre; contraejemplo de transparencia en 7 fichas). **No se fusiona** con CP-009 ni CP-010 por los motivos escritos en su §7.

**D2 — CP-017: el umbral de 7 días queda sin respaldo empírico.** El cierre del 02-11 duró 9 días y se rompió. Se anota en el expediente; **no se cambia el procedimiento** en este ciclo (toca `lpa/procedures/cierre-de-incidencia.md`, decisión del usuario). Propuesta para el próximo: sustituir la cifra fija por «N días dentro de la retención real del registro», que hoy es de **~1 día** en `executions` → con retención insuficiente, `resolved` no debería concederse nunca.

**D3 — Lección de proceso: el catch-up no respeta el orden productor → consumidor.** Registrada en el ledger (LEC-20260814-031) y **staged** como parche de la skill `hermes-cron-jobs` (id `9ca06b6e`, pendiente de aprobación: no aplicado). Sin CP (1 ocurrencia). Antídoto propuesto, sin aplicar: el consumidor debe comprobar la mtime/estado del productor antes de certificar su ausencia, o el arranque debe despachar por dependencia y no por hora programada.

**D4 — CP-013: `missed` cierra el borde del rastro, no el de la cadencia.** Se anota la asimetría día/noche. Se añade a la lista de comprobación semanal: **contar `missed` y contar re-ejecuciones tardías por separado**.

**D5 — CP-010: +1 ocurrencia (9ª), familia nueva.** El respaldo de carga sustituye el sustrato del juez y el producto sale sin veredicto comparable. Se anota; **no se toca** `modelos_por_tarea.yaml` ni `llm-router.sh` en este ciclo (afecta a producción del informe diario).

**D6 — CP-015: +1 ocurrencia con prueba física (0 bytes).** Se propone como comprobación del ciclo: **artefacto de 0 B = corrida muerta**, nunca «producto vacío».

**D7 — Ficha 12-11: doble entrega manual.** Solo observación. Si se repite una tercera vez, abre CP (mecanismo: la recuperación manual no comprueba si la ficha del día ya se entregó).

**D8 — CP-018 y CP-016: sin novedad.** La firma con fecha sigue degradando el registro (9ª semana). El vigilante de Telegram suma **0 reinicios** (5ª semana) pero **2 turnos `missed`**; sigue E0 porque no hay prueba de detección con red caída y host encendido.

**D9 — Revisión mensual: no toca.** La mensual se ejecutó el **06-11** (`revision-mensual-2026-11.md`, CP-017/CP-018/CP-019 y procedimiento escrito). Hoy es la semanal del 13-11. **No se promueve nada a `KNOWN.md`/`HYPOTHESIS.md`.**

**D10 — Escrituras del ciclo.** Acta nueva; `CP-020` nuevo; reexámenes en `CP-010`, `CP-013`, `CP-015`, `CP-017` con backup `.bak-20261113`; 4 lecciones en `04-operations/metrics/lecciones_ledger.jsonl` (con su propio backup RULE-008); 1 parche en la skill `hermes-cron-jobs`. **Sin commit. Sin tocar servicios, contenedores ni n8n. Ninguna herramienta de `tools/` modificada.**

**D11 — Recomendación, sin ejecutar: la zona horaria fija (F9).** Las 5 herramientas deben usar la zona del sistema, no `timedelta(hours=2)`:

```python
TZ = datetime.now().astimezone().tzinfo   # sigue a Europe/Madrid, CET/CEST
```

Pedir autorización explícita antes de tocar `verificar_hel.py` (escribe el estado del watchdog HEL) y `local_cloud_orchestrator.py` (enruta llamadas). Mientras no se corrija, **toda marca horaria del ledger de lecciones está 1 h adelantada** y no debe usarse para medir latencias ni para ordenar dentro de la hora.

---

## 4. Estado de la cadena incidente → lección → mejora

- **Visión (`gemma-4-12b-qat`)** → **17 marcas de tiempo en 6 días**, producto entregado sin chequeo → **CP-020 abierto (D1)** → sin mejora: falta el control con VRAM libre. Es el eslabón más roto de la cadena esta semana: **fallo diario, cero consecuencias, cero propietario**.
- **Empleo-pipeline (`bbc1d8`)** → 2 fallos el 11-11 (timeout + `exit 1` con artefacto bueno) → cierre en bloque el 12-11 → **D2**: el criterio de cierre no distingue causas ni mide con retención suficiente.
- **Informe diario** → 4 de 7 informes sin veredicto de calidad; 2 con motor de visión como motor de texto → **D5** (CP-010) → sin cambio de código; el borde «producto verde, calidad no medida» sigue abierto y creció.
- **HEL vs consolidador** → falso fallo de 36 s en el catch-up de hoy → **lección + parche de skill (D3)** → mejora barata pendiente en el lado del consumidor.
- **Turnos perdidos (CP-013)** → 19 `missed` ahora registrados → mejora real del instrumento, pero la mitad diurna sigue invisible → **D4**.
- **Ficha 07-11 (0 bytes)** → corrida adoptada y matada → **D6** (CP-015) → criterio propuesto, no aplicado.
- **Vigilante Telegram (CP-016)** → 0 reinicios en 5 semanas → antídoto sostenido, sin prueba de detección → sin cambio de nivel.

---

## 5. Próxima revisión

**Viernes 2026-11-20, 14:30 CET** (motor `lpa-revision-incidentes-semanal`, id `05de6a93257`). Comprobaciones mínimas:
1. ¿Sigue el fallo de visión? Contar marcas de `gemma-4-12b-qat` en `journalctl` y comprobar si alguna ficha declara el chequeo como ejecutado (§6 de CP-020 → primera falsación parcial).
2. ¿Se repitió la doble entrega manual de la ficha? (F7 → 3ª vez abre CP).
3. `missed` frente a re-ejecuciones tardías, contados por separado (D4).
4. Veredictos de calidad de los 7 informes: ¿cuántos con motor `lfm2.5-vl-3b` y cuántos `ERROR (?)` (D5).
5. Estado de `41a1a4_3c4b8c91fffb`: si sigue `detected`, comprobar si alguien lo cerró y con qué prueba.
6. Retención real de `executions` (D2: sin retención suficiente, ningún `resolved` es defendible).
