# REVISIÓN DE FALLOS — 2026-10-30 (ciclo semanal LPA)

> **Fecha real de ejecución:** 2026-10-30 14:36 CET (`date`), host `up 7 hours, 36 minutes` (arrancado 07:00:26).
> **Ventana revisada:** 2026-10-23 14:36 → 2026-10-30 14:36 (7 días).
> **Fuente:** `~/.hermes/cron/executions.db` en **solo lectura** (`sqlite3 -readonly`, `mode=ro`), `~/.hermes/cron/jobs.json`, artefactos en `~/.hermes/cron/output/<job>/`, `journalctl --user`, `journalctl --list-boots`, y los productos del lab en `04-operations/`.
> **Ningún fichero de sistema modificado.** Las únicas escrituras son las de este ciclo en `joko-lab` (esta acta, 1 CP nuevo, 3 reexámenes, 2 lecciones, `pendientes.md`), todas con backup RULE-008 `.bak-20261030`.

---

## 0. Incidentes de la ventana (paso 1)

**No existe ningún `*-incidentes.md` nuevo** en `lpa/incidentes/` desde el acta del 01-09-2026: el registro declarado del lab (formato FALLO/ACIERTO/DUDOSO/HIPOTESIS) **sigue sin escribirse**. Como en las actas del 16-10 y 23-10, la fuente real es la base, los artefactos y el journal. **No se fuerza ninguna promoción por «incidente declarado»**: no lo hay.

**El registro `cron_incidents` tiene 25 filas: 21 `resolved` y 4 `detected`.** Cambio respecto a la semana pasada (20 filas, 0 abiertas):

| id | job | tipo | abierta | cerrada |
|---|---|---|---|---|
| `264c02_761c7f27bcb0` | telegram-watchdog | `script` | 16-09 06:58 | 26-10 06:11:29 |
| `bbc1d8_a5731c9ceec0` | empleo-pipeline | `script` | 24-10 18:02 | 28-10 18:03:05 |
| `67d5fc_74c14f4af0d6` | informe-diario | `script` | 27-10 09:04 | **abierta** |
| `67d5fc_8bfe3bf75670` | informe-diario | `script` | 28-10 09:04 | **abierta** |
| `67d5fc_2b5c43c6a8c3` | informe-diario | `script` | 29-10 09:04 | **abierta** |
| `67d5fc_1e374c70107a` | informe-diario | `script` | 30-10 09:04 | **abierta** |

- **Las 4 abiertas son un solo defecto** contado cuatro veces (D1, CP-018). Es la primera vez desde que este ciclo empezó que el registro declara incidencias abiertas — y son un artefacto de la firma, no cuatro problemas.
- **Ojo con leer «4 abiertas» como «el lab empeoró»:** el defecto es real y lleva 4 días; lo que cambió es que **ahora se ve** (antídoto del 26-10, D6). Antes el mismo fallo se registraba como `ok`.

## 1. Actividad de la ventana (contexto verificado)

- **1.001 ejecuciones** registradas, de `2026-10-29T13:30:25` a `2026-10-30T14:34:08` = **25 h 03 min 43 s** de histórico. El tope de 1.000 filas sigue recortando la semana (D9).
- **999 `completed` · 1 `failed` · 1 `running`** (esta misma ejecución, `05de86a93257`). La única `failed` es el `informe-diario` de hoy: `Script exited with code 3`, de 09:00:07 a 09:04:21.
- **59 jobs definidos: 56 activos, 3 desactivados** (`f268fc0b7552`, `f9615035320a`, `67195e4fd0d5`) frente a 56 la semana pasada. **55 activos en `ok` con `streak` 0**; **1 activo en `error` con `streak` 4** (`67d5fcc5b69e`, `informe-diario`).
- **Artefactos en la ventana:** informe local **7** (24→30-10), `rag-reindex` **7** (24→30), `empleo-pipeline` **6** (24→29; hoy corre a las 18:00), `consolidador-sesiones` **6** (24→29; hoy a las 22:30), `resumen-dia` **7** (noches 23→29), `telemetria` **6**.
- **Descartes del informe:** `informe_descartes.jsonl` 8 líneas de vida, **7 `router_fallo`**, de las cuales **4 caen en la ventana** (27, 28, 29 y 30-10).
- **Arranques del host (7):** 23-10 07:46 → 26-10 11:39 · 26-10 11:40 → 23:46 · 27-10 07:07 → 28-10 00:20 · 28-10 06:55 → 29-10 00:27 · 29-10 08:03 → 23:36 · 30-10 07:00. **Hueco nocturno mayor de la ventana:** 29→30, de 23:36:25 a 07:01:08 = **7 h 24 min 43 s** sin ninguna ejecución (CP-013 en su comportamiento normal: el job no corre porque el host no está).

## 2. Fallos y hallazgos de la ventana

### F1. [NUEVO · CP-018, promovido] El mismo fallo cuenta como 4 incidencias porque la firma incluye la fecha de la ruta

El `informe-diario` falla 4 días seguidos (27→30-10) por la misma causa, y el registro abre **4 filas** con `first_seen_at == last_seen_at`. La única diferencia entre los cuatro errores es el nombre del fichero: `…/reports/20261027-…`, `20261028-…`, `20261029-…`, `20261030-informe-local.txt`.

Mecanismo leído en el código (`~/.hermes/hermes-agent/cron/incidents.py`): `_MAX_SIGNATURE_ERROR_CHARS = 200` (línea 43) y `_error_signature()` (línea 131) firman los **primeros 200 caracteres del error**, normalizando **solo duraciones** (`_DURATION_RE → "#s"`). La fecha de la ruta cae dentro de esos 200 caracteres → firma distinta cada día.

Segundo caso, más limpio: `orquestador-batch` (`380a80273240`) abrió **2 filas el 15-10 con una hora de diferencia** cuyo único cambio era `intento 2/3` → `intento 3/3`. Contraste donde la firma funciona: `empleo-pipeline` falló 4 días con texto estable y mantuvo **una sola fila** con `last_seen_at` avanzando.

**Consecuencia:** el registro ya no puede responder «desde cuándo» ni «cuántas veces», que es lo que existía para conservar. Promovido a **CP-018** en esta misma sesión (D1).

### F2. [ABIERTO · 4 días] El resumen local del informe no existe: `:1234` caído y sin camino alternativo

Los informes del 27, 28, 29 y 30-10 llevan la misma cabecera:

```text
# Gate de veracidad: [SIN RESUMEN — GATE OMITIDO] (GATE_OMITIDO)
# Juez de calidad: CALIDAD: omitido
# Descarte del resumen local: … (motivo: router_fallo)
```

`llm-router.sh` solo conoce `http://localhost:1234` (LM Studio), no tiene ninguna ruta a Ollama (`grep 11434` → 0 resultados en el router). Su arranque bajo demanda —que mide el éxito **en el puerto**, no en el `rc`— falló hoy con salida literal (`~/.hermes/cache/scratch/informe-router-20261030.err`, 672 B):

```text
ERROR: :1234 sigue sin responder 60s despues del arranque bajo demanda
  :1234 caido — arrancando el servidor bajo demanda ('lms server start')...
  salida real de lms server start: Waking up LM Studio service...
Error: Timed out waiting for LM Studio daemon to start.
Error: Failed to start or connect to local LM Studio API server.
```

**La hipótesis del 23-10 («arranque en frío del motor tras el apagado nocturno») no se sostiene tal como se formuló.** Los datos de esta ventana la contradicen por los dos lados: el 27-10 el host arrancó a las **07:07** (dos horas antes del informe) y falló; el 24, 25 y 26-10 el host llevaba **desde el 23-10 07:46** encendido y los informes salieron con resumen real de `gpt-oss` (leído en `20261024` y `20261026`). La variable que separa los días buenos de los malos **no es el tiempo desde el arranque, sino si la app de LM Studio está sirviendo en `:1234`**. Ollama, mientras tanto, está arriba y responde: `docker ps` → `ollama | Up 8 hours`; `curl localhost:11434/api/tags` → **200**.

**No se aplica ningún cambio:** dar al router un camino Ollama o automatizar el arranque del motor toca producción y requiere autorización explícita (D2).

### F3. [CERRADO Y VERIFICADO · CP-017] `empleo-pipeline`: cierre con reparación real

`bbc1d8_a5731c9ceec0` abierta el 24-10 18:02, `last_seen_at` 27-10 18:01, **cerrada el 28-10 18:03:05**. Causa: `invalid_grant: Token has been expired or revoked` (OAuth de Google revocado). Cumple las **tres** condiciones del criterio fijado el 26-10: (1) la credencial se renovó después de `first_seen_at`, (2) hay producto posterior al cierre, (3) la ocurrencia se conservó en la misma fila. **Es el segundo cierre-con-reparación medido** (el primero fue `consolidador-sesiones`, 16-10) y el primer contraejemplo de CP-017 en un job de credenciales.

### F4. [ANTÍDOTO VERIFICADO · CP-016] El vigilante ya no reinicia por falta de red

`~/.hermes/scripts/telegram-watchdog.sh` (4.178 B, **mtime 26-10 17:45:31** — posterior a la incidencia, condición 1 de CP-017) quedó con: normalización a 3 dígitos (`HTTP_CODE="${HTTP_CODE: -3}"`), `000` → **no reinicia nunca**, ventana sin red respetada, y `notify` protegido. Medido en la ventana:

- **0 apariciones de «Reiniciando gateway»** en los artefactos del job del 24 al 30-10 (antes: 1 reinicio por noche).
- **0 incidencias nuevas** de `264c02dae003` (la fila cerró el 26-10 06:11).
- **2 noches con el host encendido dentro de la ventana sin red** (28-10 00:00→00:20 y 29-10 00:00→00:27): sin reinicio. Las otras dos noches el host ya estaba apagado antes de medianoche, así que **no cuentan como prueba**.

Son **2 de las 10 noches** que pide la condición de falsación de CP-016: sigue en E0, pero el antídoto está aplicado y medido (D4).

### F5. [NUEVO · observación, sin causa] Reinicio del gateway el 27-10 22:03 con 18 G de pico de memoria

```text
22:03:52 hermes[…]: WARNING tools.mcp_tool: Force-killed MCP process 4861 (lancedb) after SIGTERM timeout
22:03:54 systemd[…]: hermes-gateway.service: Consumed 51min 29.951s CPU time over 14h 56min 2.114s wall clock time, 18G memory peak, 584.9M memory swap peak.
```

No hay línea de OOM ni `Failed with result` en la ventana consultada: **no se atribuye la causa**. Se registra porque 18 G de pico es el orden de magnitud del episodio ComfyUI/cgroup ya conocido, y porque el `Force-killed` del MCP deja el proceso en un estado que no se ha verificado. Sin acción (D10).

## 3. Decisiones D0..D12

**D0 — [MANTENER] Fuente de la revisión.** No hay `*-incidentes.md` nuevos desde el 01-09-2026. Se revisa sobre `executions.db` (solo lectura), artefactos, `journalctl` y productos. No se fuerza ninguna promoción: nada de lo que sigue procede de un incidente declarado.

**D1 — [PROMOCIÓN · INCUBADORA] CP-018 creado.** «La firma de la incidencia incluye el dato que cambia en cada intento». Evidencia: 6 ocurrencias medidas en 2 jobs (`67d5fc` ×4 por la fecha en la ruta, `380a80` ×2 por el contador de intento) + 2 contrastes en el mismo registro (1 fila con texto estable; 3 filas con causas distintas). E0: un solo motor de incidencias y antídoto sin aplicar. Archivo: `pattern-incubator/CP-018-la-firma-incluye-el-dato-que-cambia-cada-intento.md`. **Criterio de lectura mientras no se repare el núcleo: contar firmas del mismo job+causa, no filas.**

**D2 — [ABIERTO · SIN ACTUAR] El informe diario depende de una app de GUI.** Cuatro días sin resumen (27→30-10), `:1234` caído, `lms server start` falla headless con `Timed out waiting for LM Studio daemon to start`, y el router no tiene camino a Ollama (que está arriba, 200). La hipótesis de «arranque en frío» queda **refinada, no confirmada**: lo que separa los días buenos de los malos es si la app sirve en `:1234`. **No se toca el router ni el arranque del motor:** ambas cosas son producción y requieren autorización explícita. Candidatos para cuando se autorice: (a) camino de respaldo a Ollama en el router cuando `:1234` no responde; (b) unidad de usuario que arranque el servidor al inicio de sesión, medida en el puerto y no en el `rc`. Mientras tanto el producto **no miente**: sale degradado y el job sale en rojo.

**D3 — [CIERRE VERIFICADO] `empleo-pipeline` (`bbc1d8`).** Cerrada el 28-10 18:03 tras renovar la credencial OAuth. Cumple las 3 condiciones del criterio del 26-10 (productor cambiado después de `first_seen_at`, producto posterior al cierre, ocurrencia conservada). Se acepta el cierre como reparación.

**D4 — [ANTÍDOTO VERIFICADO · SIGUE E0] CP-016.** Script corregido el 26-10 17:45 (mtime verificado): `000` no reinicia, ventana sin red respeta, notificación protegida. 0 reinicios y 0 incidencias en 7 días; 2 noches con host encendido dentro de la ventana sin reinicio. Faltan 8 noches del mismo tipo para la falsación → **sigue en incubación**.

**D5 — [CP-017 · TERCER SOBRESCRITO DOCUMENTADO] La fila `264c02_761c7f27bcb0` vuelve a tener otro `closed_at`.** Tres actas, tres lecturas de la **misma fila**: cerrada el 13-10 (acta del 16-10) → cerrada el **23-10 07:46:58** (acta del 23-10) → hoy `closed_at` **26-10 06:11:29**. El historial se pierde en cada reapertura, y con él la respuesta a «cuántas veces ha pasado». Añadido al expediente de CP-017. **Dato nuevo:** el cierre del 26-10 (06:11) precedió **11 horas** a la reparación (17:45); se sostiene hoy por casualidad, no porque el criterio se aplicara entonces.

**D6 — [BORDE CERRADO EN 1 JOB] CP-015.** El falso ok del informe está cerrado por el lado del **productor**: `informe-diario-local.sh` (mtime 26-10 18:09) ahora sale con **código 3** cuando el resumen no está verificado, y el registro lo ve (4 incidencias + 1 ejecución `failed`). El vigía `watchdog-informes-cron.py` **sigue sin leer la cabecera** (mtime 20-09), pero ya no hace falta para este job. Riesgo declarado: **cualquier otro job que degrade su producto sin cambiar el exit code sigue invisible**. CP-015 sigue E0; se lleva a la mensual del 02-11 con este antídoto medido.

**D7 — [CP-009 · MANTENER] Instrumentos que nadie usa.** `retrabajo_ledger.jsonl`: 566 B, mtime **25-09** → **35 días** sin una escritura (plazo de retirada fijado el 26-10: **02-11**). Curador de skills: **pausado** y su ledger `~/.hermes/skills/.curator_ledger.jsonl` no recibe escrituras desde el **21-10** (2.242 líneas, 9 días). No se toca nada: el curador no se reactiva sin autorización. **Añadido:** `registrar_leccion.py` sella las dos lecciones de hoy como `2026-10-30 15:36 UTC+02:00` mientras el host está en **CET (+01:00)** desde el cambio de hora del 25-10 — es el mismo instante, pero la etiqueta de zona está fija en el script. Cosmético hoy; en una auditoría futura que ordene por cadena de texto, dos eventos del mismo minuto quedan desfasados una hora. Se anota, no se corrige.

**D8 — [MANTENER] Skills con `[truncated]`.** 4 ficheros hoy. Sin acción; se vigila que no crezca.

**D9 — [MANTENER] Tope de 1.000 filas en `executions`.** Da 25 h 03 min de histórico: la semana **no se puede reconstruir** desde ahí. La única fuente con alcance semanal es `cron_incidents`, y CP-018 la inutiliza para contar ocurrencias. Es el argumento más fuerte para arreglar la firma.

**D10 — [NUEVO · OBSERVACIÓN] Reinicio del gateway con 18 G de pico (27-10 22:03).** Sin causa atribuida (no hay OOM en el journal consultado). Se anota como observación para el ciclo siguiente; no se actúa.

**D11 — [MANTENER] Sin commit git.** Los cambios de este ciclo quedan en disco con sus `.bak-20261030`.

**D12 — [ABIERTO] Backlog.** Bloque `LPA-REV-20261030` en `04-operations/backlogs/pendientes.md` con los 3 ítems que requieren decisión del usuario: (A) camino de respaldo del router / arranque del motor, (B) normalización de la firma en el núcleo de Hermes (RULE-016), (C) retirada o rescate del `retrabajo_ledger` antes del 02-11.

---

## 4. Estado de la cadena incidente → lección → mejora

| cadena | incidente | lección | mejora aplicada | estado |
|---|---|---|---|---|
| Falso ok del informe (22-10) | CP-015 | LEC-025 | **sí** — exit 3 en el productor (26-10) | borde cerrado en 1 job |
| Vigilante reinicia por falta de red | CP-016 | LEC-023 | **sí** — `000` no reinicia + `notify` protegido (26-10) | 0 reinicios en 7 días |
| `resolved` sin reparación | CP-017 | LEC-024 | **parcial** — criterio de 3 condiciones fijado el 26-10 | 1 cierre verificado (D3) |
| Reintentos que duplican la incidencia | CP-018 (nuevo) | LEC-026 (nueva) | **no** — requiere el núcleo de Hermes | abierto |
| Rutina sin resumen local | F2 | LEC-027 (nueva) | **no** — requiere autorización | abierto, 4 días |
