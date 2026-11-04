# REVISIÓN DE FALLOS — 2026-10-23 (ciclo semanal LPA)

> **Fecha real de ejecución:** 2026-10-23 14:36 CEST (`date`), host `up 6 hours, 50 minutes` (arrancado 07:46:12).
> **Ventana revisada:** 2026-10-17 00:00 → 2026-10-23 14:36 (7 días).
> **Fuente:** `~/.hermes/cron/executions.db` en **solo lectura** (`sqlite3 -readonly`, `mode=ro`), `~/.hermes/cron/jobs.json`, artefactos en `~/.hermes/cron/output/<job>/`, `journalctl --user -u hermes-gateway.service`, y los productos del lab en `04-operations/`.
> **Ningún fichero de sistema modificado.** Las únicas escrituras son las de este ciclo en `joko-lab` (acta, 2 CP nuevos, 5 reexámenes, ledger de lecciones, `pendientes.md`), todas con backup RULE-008 `.bak-20261023`.

---

## 0. Incidentes de la ventana (paso 1)

**El registro `cron_incidents` tiene 20 filas, 20 `resolved`, 0 abiertas.** Tres cierres caen en la ventana:

| id | job | tipo | abierta desde | cerrada |
|---|---|---|---|---|
| `da39a2_563646c13b70` | rag-reindex-daily | `timeout` | 12-10 08:05 | **17-10 08:01:30** |
| `8bf412_369f79e3c051` | ficha-perfume-diaria | `unknown` | 20-10 07:12 (**única vez**) | **20-10 08:01:59** |
| `264c02_761c7f27bcb0` | telegram-watchdog | `script` | 16-09 06:58 | **23-10 07:46:58** |

- **No hay ningún `*-incidentes.md` nuevo** en `lpa/incidentes/` desde `revision-fallos-2026-10-16.md`. El registro declarado del lab (formato FALLO/ACIERTO/DUDOSO/HIPOTESIS) sigue sin escribirse: **la fuente real de esta revisión es la base y los artefactos**, como en D0 del 16-10.
- **Ojo con leer «0 abiertas» como «todo bien»**: dos de los tres cierres no son reparaciones (D3). El registro cierra con la corrida siguiente.

## 1. Actividad de la ventana (contexto verificado)

- **1.001 ejecuciones** registradas, de `2026-10-22T13:25:42.513056` a `2026-10-23T14:30:54.157162` = **25 h 05 min 12 s** de histórico (el tope de 1.000 filas sigue recortando la semana, D10 del 16-10 se mantiene).
- **999 `completed` · 1 `failed` · 1 `running`** (esta misma ejecución).
- **56 jobs definidos: 52 activos, 4 desactivados** (`f268fc0b7552`, `f9615035320a`, `319ddf42aaf2`, `9ee28ab8519e`). **Los 52 activos con `last_status` = `ok` y `failure_streak` = 0.** Es la primera vez desde que empezó este ciclo que el `streak` no señala nada: el job que el 16-10 llevaba 15 fallos seguidos está en 0.
- **77 ficheros de salida** conservados en la ventana en los directorios de job inspeccionados: `67d5fcc5b69e` informe **7** (17→23-10), `9474f6f3d224` consolidador **6** (17→22-10), `da39a2148b34` reindex **7**, `8bf412ac2ba3` ficha-perfume **7**, `264c02dae003` watchdog **50** (su tope de retención: no permite contar sus corridas de la semana).
- **Producción real de productos:** `resumen-dia-2026-10-15..21` (7 ficheros, 314 B cada uno, 16→22-10), informes locales `20261017..20261023`, `telemetria/2026-10-17..23`, y 7 salidas de `rag-reindex` (17→23-10).

## 2. Fallos y hallazgos de la ventana

### F1. [NUEVO · CP-016, 1ª medición] El vigilante reinicia el gateway sano cuando no hay red — 4 veces en 3 noches — y muere al notificarlo

`telegram-watchdog.sh` (job `264c02dae003`, cada 15 min) reinicia `hermes-gateway.service` cuando el `getMe` de Telegram **no da 200**. En la ventana sin red (00:00-07:00) la respuesta es `HTTP 000000`, que no significa «gateway caído» sino «no hay red»: **el remedio se dispara por una causa que no puede arreglar**.

Reinicios nocturnos del gateway en 7 días (`journalctl --user`), ninguno coincide con un arranque del host:

- `17→18-10` `00:06:00 Stopping` → `00:09:03 Started` · y otra vez `00:25:16` → `00:28:20`
- `21→22-10` `00:10:47` → `00:13:52`
- `22→23-10` `00:03:56` → `00:07:02`

**4 reinicios en 3 noches distintas, todos entre 00:03 y 00:28.** La prueba directa del mecanismo está en la noche del 23-10: `~/.hermes/cron/output/264c02dae003/2026-10-23_00-07-19.md` contiene `WARN: API Telegram no responde (HTTP 000000). Reiniciando gateway...`, y la fila de `executions` `2c54785d807b419684b34db9cb0b3e84` está **`failed` con `Script exited with code 6`** (00:03:42 → 00:07:19).

El `exit 6` es el segundo defecto: el `curl sendMessage` de la notificación va **sin `|| true`** bajo `set -e`, así que sin red el script muere **antes** de su salida normal. El fallo queda registrado como «el job falló» cuando lo que ocurrió es «no había red y reinicié un servicio sano». Mismo defecto de forma en `ceder-control.sh` (1 `sendMessage`, 0 protegidos).

Hoy el servicio está `active` desde 07:46:22 y **no hay ninguna evidencia de que el gateway estuviera caído** en ninguno de los 4 reinicios.

### F2. [NUEVO · CP-017] Dos cierres que no son reparaciones, y un historial sobrescrito

- **`rag-reindex-daily`** cerró el **17-10 08:01:30** sin que nadie tocara nada: `rag-reindex.sh` tiene **mtime 15-oct 17:46**, anterior a la primera ocurrencia. Cerró porque la corrida dejó de acercarse al límite de 300 s: `[✓] Sin cambios: 46745 fragmentos ya indexados` / `4236 documentos: 0 nuevos, 0 modificados`. **No hubo trabajo, no hubo arreglo.**
- **`telegram-watchdog`** cerró a las **07:46:58**, **36 segundos después** de que el host arrancara (`uptime -s` = 07:46:12). Script sin tocar (mtime 25-jul). Lo que «se arregló» fue la vuelta de la red.
- **Historial destruido:** el acta del 16-10 documenta esta **misma fila** (`264c02_761c7f27bcb0`) como cerrada el **13-10 06:13** tras 27 días abierta. Hoy la fila, mismo `id`, tiene `closed_at` **23-10 07:46:58**. El cierre del 13-10 ya no existe: se reabrió y se escribió encima. **Las dos lecturas son ciertas y ya no se pueden reconciliar con la base.**
- **Contraejemplo que sí vale:** `9474f6_807bf8724760` (consolidador) cerró el 16-10 22:31:24 **después** de reescribir el script y comprimir los dumps, y con 7 noches de producto detrás. El registro **no distingue** ese cierre del de `rag-reindex`.

### F3. [NUEVO · borde falso-ok de CP-015] El informe diario salió mudo 3 de 7 días y el semáforo se quedó en verde

`67d5fcc5b69e` terminó `ok` con `failure_streak` 0 **los 7 días**. Pero el producto de **20, 21 y 23-10** dice en su propia cabecera:

```
# Gate de veracidad: [SIN RESUMEN — GATE OMITIDO] (GATE_OMITIDO)
# Juez de calidad: CALIDAD: omitido
# Descarte del resumen local: ... (motivo: router_fallo)
## Resumen (gpt-oss local)
(resumen local no disponible)
```

y `04-operations/metrics/informe_descartes.jsonl` tiene **3 filas `router_fallo, chars 0`** (20, 21, 23-10; la cuarta fila es `descarte_heuristica` del 15-10). El 22-10 salió completo: `CALIDAD: PASA (4.33)`.

**El producto declara su degradación y el único que podía leerla no la mira**: el vigía busca fichero ausente o exit distinto de 0, no `GATE_OMITIDO`. **3 de 7 días (43 %)** con el informe sin resumen ejecutivo. Ningún ciclo anterior lo había reportado — es un fallo de este informe, no solo del job.

Estado de los motores ahora mismo: Ollama `HTTP 200`, LM Studio `HTTP 000` (API apagada, normal). **No se afirma la causa del `router_fallo`**: no hay log del router en la ventana que lo explique, y el fallo no coincide con una hora fija de arranque (20-10 arrancó 07:12, 21-10 08:10, 23-10 07:46; el 22-10, que salió bien, arrancó a las 06:27). Queda como hipótesis a falsar (D5), no como diagnóstico.

### F4. [RECURRENCIA, 4º ciclo · CP-009] `retrabajo_ledger.jsonl`: 28 días congelado, y el curador sigue «PAUSED» con el ledger creciendo

- `retrabajo_ledger.jsonl`: **566 B, mtime 25-09** → **28 días** sin asiento (21 el 09-10, 21 el 16-10).
- `hermes curator status`: **PAUSED**, `runs` 13, última ejecución hace **29 días**, último informe `20260923-170843`. Pero `~/.hermes/skills/.curator_ledger.jsonl` tiene **2242 filas** (eran 2203) con **39 nuevas en la ventana** (17:9, 18:5, 19:15, 21:10), todas `patch`, última `2026-10-21T12:35:57Z`. **6º ciclo** con el estado del CLI contradiciendo al ledger: el que escribe es el agente en sesión.
- `[truncated]`: **4 ficheros**, sin cambios desde que se midió (`render-html-a-imagen/SKILL.md`, `validacion-instrumentos-medicion/SKILL.md` + `.bak`, `perfume-ia/references/capa-lpa-recomendacion.md`).
- **La parte buena, y es nueva:** el mecanismo del `failure_streak` que este patrón usaba como prueba **ha desaparecido** esta semana (52 jobs en 0). Lo arregló tener consumidor, que es exactamente lo que predice el patrón.

### F5. [NUEVO · CP-013, 3ª noche medida] Récord de ventana muerta: 7 h 30 min 49 s, con ráfaga de 12 jobs en 483 ms

- Última ejecución antes del apagón: `2026-10-23T00:16:06.020075`. Primera después: `2026-10-23T07:46:55.217831`. **Ventana muerta = 7 h 30 min 49 s** (récord; la anterior 6 h 18 min 49 s).
- La primera ejecución sale **43 s** después del arranque del host (`uptime -s` 07:46:12).
- **Ráfaga de recuperación:** 12 jobs entre `07:46:55.217831` y `07:46:55.701131` = **483 ms**, los 12 `completed`, **0 `unknown`**.

### F6. [CIERRE VERIFICADO · D5 del 16-10] El `consolidador-sesiones` aguantó: 7 de 7 noches

`resumen-dia-2026-10-15..21` en `04-operations/metrics/sesiones/`, 7 ficheros de 314 B, generados 16→22-10, contenido `OK: 25 sesiones de 2026-10-21 | export del dia 42.6 MB`. `9474f6f3d224` con `failure_streak` 0 y próxima corrida 23-10 22:30. **El criterio de cierre de D5 se cumple; la incidencia se da por buena.**

### F7. [NUEVO · CP-012, 5ª ocurrencia] El `unknown` se resolvió en el mismo segundo en que apareció el producto

`8bf412_369f79e3c051` (`unknown`, 20-10 07:12:51, una sola vez) cerró a las **08:01:59**, y el artefacto `~/.hermes/cron/output/8bf412ac2ba3/2026-10-20_08-01-59.md` (**79.753 B**) tiene **ese mismo timestamp**: los side effects sí corrieron. `last_status` `ok`, `streak` 0. El `closed_at` sirve como pista para localizar el artefacto que resuelve el `unknown`.

## 3. Aciertos de la ventana

1. **El `failure_streak` en cero por primera vez** (52/52 jobs `ok`): el consolidador cerrado con reparación real, el informe con producto los 7 días y el reindex corriendo puntual (21-10 algo tarde, 08:11:34).
2. **7 noches consecutivas con `resumen-dia`** (15→21-10): el fallo que el 16-10 era una incidencia abierta ya no se reproduce.
3. **Cero ejecuciones `unknown`** en 1.001 ejecuciones. La única `failed` dejó artefacto.
4. **La recuperación tras el apagón sigue siendo sub-segundo** (483 ms, 12 jobs) y sin pérdidas.
5. **Los productos de esta semana existen todos** salvo el resumen ejecutivo del informe (F3), que es el hallazgo importante.

## 4. Patrones (paso 3)

| Patrón | Estado | Qué pasa esta ventana |
|---|---|---|
| **CP-016** (nuevo) El vigilante que mide red reinicia un servicio sano — y muere al notificarlo | **Promovido hoy a incubación** | 4 reinicios en 3 noches + 1 fallo `exit 6` medido de punta a punta; mecanismo leído en el código |
| **CP-017** (nuevo) El cierre se concede con la corrida siguiente: `resolved` no dice reparado, y borra la ocurrencia | **Promovido hoy a incubación** | 2 cierres sin reparación (2 jobs) + 1 historial sobrescrito (13-10 → 23-10 en la misma fila) |
| **CP-012** el `unknown` se resuelve en el artefacto | Incubación, E0 | 5ª ocurrencia (ficha-perfume); sin cambio de nivel |
| **CP-013** los jobs no corren a su hora en la ventana de apagado | Incubación, E0 | 3ª noche medida, récord 7 h 30 min; sin cambio de nivel |
| **CP-014** el fallo en cadena se registra en el consumidor | Incubación, E0 | **0 ocurrencias**; el caso de esta semana es el reverso (fallo declarado en el productor) → evidencia de frontera, no ocurrencia |
| **CP-015** la corrida que muere sin artefacto no deja señal | Incubación, E0 | 0 `failed` sin artefacto, pero **3 falsos ok** (F3). 4ª cara del borde: al límite — el 30-10 se decide ascenso o descarte |
| **CP-009** el instrumento sin forzado se degrada | E1 | 4º ciclo: `retrabajo_ledger` 28 días, curador «PAUSED» con ledger activo; **pero** el `streak` que usaba como prueba desapareció. Sin cambio de nivel |
| **CP-010** el instrumento no validado miente | E1-008 en `KNOWN.md` | **6º ciclo**: `curator status` contra `.curator_ledger.jsonl`. Sin cambio de nivel |

**Descartados esta ventana: ninguno.** No hay patrón con ocurrencias que no encaje en los existentes.

## 5. Lecciones registradas (paso 4, dominio `proceso`)

| id | Título | Ref |
|---|---|---|
| **LEC-20260814-023** | Un watchdog que mide red no debe reiniciar un servicio local, y su notificación no puede depender del recurso que falta | CP-016 |
| **LEC-20260814-024** | Una incidencia cerrada no está reparada: verificar mtime del productor y producto posterior antes de creerse el `resolved` | CP-017 |
| **LEC-20260814-025** | Un producto que declara su degradación en la cabecera no es un `ok`: el vigía debe leer la cabecera, no solo el exit code | CP-015 borde |

Ledger: `04-operations/metrics/lecciones_ledger.jsonl` **22 → 25 filas**. **3ª vez consecutiva** que el disparador de facto de este instrumento es este ciclo (D7 del 16-10 se mantiene).

## 6. Cadena incidente → lección → mejora

| Incidente | Lección | Mejora | Estado de la mejora |
|---|---|---|---|
| `264c02_761c7f27bcb0` (4 reinicios + `exit 6`) | LEC-023 | CP-016 + antídoto en 3 pasos (`000` ≠ caído, `\|\| true` en sendMessage, no correr en la ventana sin red) | **Propuesta, NO aplicada** — toca `~/.hermes/scripts/telegram-watchdog.sh`, requiere autorización |
| `da39a2_563646c13b70` + `264c02_…` (cierres sin reparación) | LEC-024 | CP-017 + criterio de cierre obligatorio en las actas (mtime del productor + producto posterior + ocurrencia previa) | **Aplicado ya en esta acta** (F2, F6) |
| `67d5fcc5b69e` 20/21/23-10 (informe mudo con semáforo verde) | LEC-025 | Ampliar el vigía de informes para leer la cabecera declarativa (`GATE_OMITIDO`) | **Propuesta, NO aplicada** — toca `~/.hermes/scripts/watchdog-informes-cron.py`, requiere autorización |
| `9474f6_807bf8724760` (OOM consolidador) | LEC-018 (16-10) | Compresión + reescritura del script | **Cerrada y verificada**: 7/7 noches |

## DECISIONES (2026-10-23)

- **D0 [MANTENER]** Fuente real = `executions.db` (solo lectura) + artefactos en disco + `journalctl --user`. El registro declarado `*-incidentes.md` lleva **50 días** sin una sola escritura (último 16-10) y no se usa como fuente. Confirmado que **no hay incidente nuevo** en ese formato: no se fuerza ninguna lectura de FALLO/ACIERTO/DUDOSO/HIPOTESIS que no exista.
- **D1 [CERRADO Y VERIFICADO]** D5 del 16-10 (`consolidador-sesiones`): criterio cumplido — producto del 16/17/18/19/20/21 en disco, `failure_streak` 0, próxima corrida programada. Sin acción pendiente.
- **D2 [NUEVO · PROMOVIDO]** **CP-016** a `lpa/pattern-incubator/` con los 7 campos y falsación («10 noches con ventana sin red y host encendido: si en ≥8 no se reinicia, es falso»). E0: 1 ocurrencia medida de punta a punta, 3 compatibles. Revisión **30-10** y **02-11**. El **antídoto no se aplica**: toca un script de `~/.hermes/scripts/` → **requiere autorización explícita del usuario**.
- **D3 [NUEVO · PROMOVIDO]** **CP-017** a incubación con falsación («10 incidencias cerradas en 2 ciclos: si en ≥8 el cierre coincide con cambio verificable del productor y se conserva el histórico, es falso»). E0: 3 ocurrencias, un solo registro. Relación declarada con **CP-010** (misma familia de instrumento); la mensual del **02-11** decide si se fusionan.
- **D4 [NUEVO · CRITERIO DE CIERRE]** A partir de hoy, una incidencia **no se da por reparada** en esta acta sin: (1) mtime del productor posterior al `first_seen_at`, (2) producto generado después del cierre, (3) aviso de si la fila ya cerró antes. Aplicado a F2 y F6. Consecuencia inmediata: `rag-reindex` queda como **«no reproducido desde 17-10», no como «reparado»**, y su límite de 300 s sigue vivo (ver D5).
- **D5 [ABIERTO, fecha tope 30-10]** `rag-reindex-daily`: el `timeout` de 300 s **no está arreglado**, solo no se toca porque no hay nada que indexar. Condición de disparo real: el primer día con >1 documento nuevo. Hipótesis a falsar: *el script no escala con el número de documentos nuevos*. **No se toca el script sin autorización.**
- **D6 [ABIERTO, fecha tope 30-10]** Informe diario mudo 3/7 días (`router_fallo`, `chars 0`). **Hipótesis, no diagnóstico**: el resumen local falla por arranque en frío del motor tras el apagado nocturno (20-10 arranque 07:12, 21-10 08:10, 23-10 07:46 → fallan; 22-10 arranque 06:27 → funciona). Falsación: si un día con el motor caliente a las 09:00 también falla, o si un día con arranque tardío funciona, la hipótesis cae. **Falta el log del router**: sin él no se afirma nada. Añadir la lectura de `GATE_OMITIDO` al vigía → **requiere autorización** (LEC-025).
- **D7 [MANTENER, 4º ciclo · decisión del usuario]** `retrabajo_ledger.jsonl`: **28 días** congelado. Tres opciones, ninguna ejecutada: (a) disparador automático, (b) declararlo no-instrumento y retirarlo, (c) fecha tope. **Fecha tope propuesta: 30-10.** Si el 30-10 no hay decisión, este acta propone **(b)**: un ledger que solo se mueve cuando un humano se acuerda no es un instrumento.
- **D8 [MANTENER, 6º ciclo]** El curador sigue `PAUSED` (29 días) con 39 filas nuevas en su ledger. **No se reactiva** sin decisión explícita. **Nuevo matiz aplicado**: a partir de hoy, la medida del curador se toma **del ledger**, no de `hermes curator status` (el CLI mide otra cosa).
- **D9 [MANTENER, 4º ciclo]** `[truncated]` en 4 ficheros de skills: declarado, no resuelto (no rompe ejecución).
- **D10 [MANTENER, 4º ciclo]** El tope de 1.000 filas de `executions` deja **25 h 05 min** de histórico: no se cuenta «la semana» ahí.
- **D11 [NUEVO]** CP-015 queda **al límite**: 4 caras medidas (F3 es la cuarta) y ninguna aplicación del antídoto. Si el **30-10** vuelve a aparecer un falso ok, la mensual del **02-11** decide **ascenso a E1 o descarte**, sin otra prórroga.
- **D12 [MANTENER]** No se hace `git add`/`commit` de los hallazgos (D12 del 02-10 y del 16-10).
- **D13 [NUEVO · EJECUTADO]** Puntos abiertos volcados a `pendientes.md` como bloque `LPA-REV-20261023` con fecha tope **30-10** (CP-016 antídoto · CP-017 criterio · `rag-reindex` límite 300 s · informe mudo + `GATE_OMITIDO` · `retrabajo_ledger` con 3 opciones). Medición de la escritura (RULE-008, en §8): `04-operations/backlogs/pendientes.md` **335.326 → 340.878 B** (1.448 → 1.457 líneas, aporta 5.552 B), backup `.bak-20261023` md5 `de453c87…` == estado previo, los primeros 335.326 B del fichero final idénticos byte a byte, 1 marcador `LPA-REV-20261023`.

## 7. Próxima revisión

- **Semanal: 2026-10-30.** Agenda obligatoria: ¿se aplicó el antídoto de CP-016? ¿apareció otro falso ok (→ CP-015 se decide)? ¿volvió el `router_fallo`? ¿se movió `retrabajo_ledger`?
- **Mensual: 2026-11-02** (1ª del mes): revisar incubator → ascender o descartar CP-012/013/014/015/016/017; decidir fusión CP-017 ↔ CP-010. Sin ascensos automáticos.

## 8. Integridad y backups (RULE-008)

Backups `.bak-20261023` creados **antes** de tocar cada fichero existente:

| Fichero | Bytes backup | Bytes después |
|---|---|---|
| `lpa/pattern-incubator/CP-009-…md` | 16.437 | 18.243 |
| `lpa/pattern-incubator/CP-012-…md` | 11.434 | 12.871 |
| `lpa/pattern-incubator/CP-013-…md` | 10.584 | 11.690 |
| `lpa/pattern-incubator/CP-014-…md` | 7.936 | 8.988 |
| `lpa/pattern-incubator/CP-015-…md` | 7.863 | 9.523 |
| `04-operations/metrics/lecciones_ledger.jsonl` | 21.708 (22 filas) | 25 filas (+3) |
| `04-operations/backlogs/pendientes.md` | 335.326 (1.448 líneas) | 340.878 (+5.552 B, 1.457 líneas; los primeros 335.326 B idénticos byte a byte; md5 backup `de453c87…`, md5 final `78456cf7…`, 1 marcador `LPA-REV-20261023`) |

Ficheros **nuevos** (sin backup, no existían): `CP-016-…md` (9.039 B), `CP-017-…md` (8.422 B), esta acta.

## Anexo · literal vs resumen

- **Literal citado sin alterar:** los `Stopping`/`Started` de `journalctl`; `WARN: API Telegram no responde (HTTP 000000). Reiniciando gateway...`; `Script exited with code 6`; `Restart-safe cron worker exited with status 1 after adopting this execution, without writing a durable terminal state; whether side effects ran is unknown.`; las 3 líneas de cabecera del informe del 20-10 (`GATE_OMITIDO`, `CALIDAD: omitido`, `(resumen local no disponible)`); `[✓] Sin cambios: 46745 fragmentos ya indexados`.
- **Resumen (no literal):** la atribución de los reinicios del 18-10 y 22-10 al watchdog — es inferencia temporal (ventana 00:0x + cadencia 15 min + ser el único script que hace ese `restart`), **no** prueba directa; solo el del 23-10 tiene artefacto. Se declara así en CP-016 §3.
- **No aparece en las salidas:** el log del router que explique `router_fallo`; el número de veces que la fila `264c02_761c7f27bcb0` ha sido reabierta (la base no lo conserva); el motivo de los 4 jobs desactivados.
