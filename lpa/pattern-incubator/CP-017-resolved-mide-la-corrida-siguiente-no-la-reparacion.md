---
type: candidate_pattern
id: CP-017
status: promoted
created: 2026-10-23
confidence: E1 (promovido 2026-11-06; era E0 con 3 ocurrencias en 2 jobs distintos)
promoted_to: E1-011
domain: gobernanza-del-conocimiento / observabilidad
---

# CP-017 · El cierre de una incidencia se concede con la corrida siguiente: `resolved` no dice «reparado», y borra la ocurrencia anterior

> **Estado:** Incubación (E0→E1)
> **Fecha:** 2026-10-23
> **Origen:** Ciclo semanal LPA, ventana 17→23-10-2026 (acta `incidentes/revision-fallos-2026-10-23.md`, decisión D3). Medido en solo lectura sobre `~/.hermes/cron/executions.db` (`cron_incidents`) y sobre los artefactos de los dos jobs implicados.
> **Nivel de confianza:** E0 (dos jobs distintos y un caso de historial destruido, pero **un solo registro de incidencias** y un solo motor; no hay aún un caso reparado de verdad que sirva de contraste)

---

## 1. Qué ocurrió

El registro de incidencias del planificador (`cron_incidents`) tiene una sola fila por **firma de error** (`job_id` + `error_sig`). Esa fila acumula: `first_seen_at`, `last_seen_at`, `state`, `closed_at`.

Dos consecuencias medidas esta semana:

1. **El cierre no exige reparación, solo una corrida sana después.** Cuando la siguiente ejecución del job termina bien, la fila pasa a `resolved` y se sella `closed_at` — aunque **nada del productor se haya tocado**.
2. **Al reabrirse, la fila se reutiliza y el cierre anterior se sobrescribe.** No queda histórico: `first_seen_at` sigue siendo el original y `closed_at` pasa a ser el nuevo. Un mismo `id` puede haber cerrado cinco veces y en la base solo consta la última.

## 2. Evidencia que lo respalda

**(1) `rag-reindex-daily` (`da39a2_563646c13b70`): cerrada sin tocar el productor.**
- `first_seen_at` 12-10 08:05:44, `last_seen_at` 16-10 08:05:58, `closed_at` **17-10 08:01:30.814926**, firma `Script timed out after 300s: /home/jokoalmi/.hermes/scripts/rag-reindex.sh`.
- `rag-reindex.sh` **mtime = 15-oct 17:46**, es decir **anterior** a la primera ocurrencia y sin cambios en todo el periodo: nadie reparó nada.
- Las salidas de las corridas siguientes (17 a 23-10, 879-917 B cada una) dicen por qué cerró: `[✓] Sin cambios: 46745 fragmentos ya indexados (sidecar al día)` / `4236 documentos: 0 nuevos, 0 modificados`. La corrida deja de acercarse al límite **porque no tiene trabajo**, no porque el script sea más rápido.
- Historial previo del mismo job: `da39a2_fae825d0fe36` estuvo abierta **33 días** y cerró el 08-10; **4 días después** reapareció con la misma firma. Ese es el patrón oro que hace que un `resolved` no valga como prueba.

**(2) `telegram-watchdog` (`264c02_761c7f27bcb0`): cerrada por el arranque del host.**
- `closed_at` **2026-10-23T07:46:58.401826**, `last_seen_at` 2026-10-23T00:07:19. `uptime -s` = **2026-10-23 07:46:12**: el cierre llega **36 segundos después** de que el host arranque. El script no se ha tocado (mtime 25-jul); lo que «se arregló» fue la vuelta de la red. Ver **CP-016**.

**(3) El historial de la misma fila fue sobrescrito.**
- El acta `revision-fallos-2026-10-16.md` (§0) documenta esta misma fila como **cerrada el 13-10 06:13** tras 27 días abierta, a partir de la lectura de la base de ese día.
- Hoy, la fila `264c02_761c7f27bcb0` —**mismo id**— tiene `closed_at` **2026-10-23T07:46:58**. El cierre del 13-10 ya no existe en la base: se reabrió y se volvió a cerrar encima.
- Consecuencia medida: en el acta del 16-10 esta incidencia contaba como «cerrada dentro de la ventana»; en la de hoy cuenta como «abierta hasta el 23-10». **Las dos lecturas son ciertas y no se pueden reconciliar con la base actual.**

**(4) Contraste (lo que sí es un cierre con reparación):** el `consolidador-sesiones` (`9474f6_807bf8724760`) cerró el 16-10 22:31:24 **después** de que se reescribiera `consolidador_sesiones.py` y se comprimieran los dumps (MAXRSS 11,3 GB → 526 MB), y con **7 noches consecutivas de producto** detrás (`resumen-dia-2026-10-15..21`). Ese cierre sí significa algo. El registro **no distingue** este caso del de `rag-reindex`.

## 3. Contradicciones o limitaciones

- **Un solo registro, un solo motor.** Los dos casos de cierre-sin-reparación son de Hermes cron; no hay evidencia de otros sistemas de incidencias del lab. La generalidad es todavía débil.
- **La semántica puede ser deliberada.** Un `resolved` que signifique «el síntoma ya no se reproduce» es defendible como diseño. El patrón no dice que el diseño esté mal: dice que **el lab lo lee como «reparado»** en sus actas y en `pendientes.md`, y que esa lectura es la que falla.
- **El caso (4) es el contraejemplo vivo** y por eso el patrón se formula con precisión: no es «`resolved` miente siempre», es «`resolved` **no distingue** reparado de no-reproducido, y no hay campo que lo distinga».
- **Frontera con CP-010 (E1-008, en `KNOWN.md`):** comparten familia (una medida que no mide lo que su etiqueta dice). La diferencia es el objeto: CP-010 es «cualquier instrumento no validado»; aquí el objeto es concreto —**la regla de cierre de un registro de incidencias**— y su antídoto también (exigir evidencia de reparación + conservar ocurrencias). Se declara la relación para que la revisión mensual decida si se fusionan.
- **No medido:** cuántas filas de `cron_incidents` han sido reabiertas alguna vez. La base no lo conserva — es exactamente el problema.

## 4. Principio que parece emerger

> **Cerrar no es reparar.** Un registro de incidencias que cierra con «la siguiente corrida salió bien» mide la **no-repetición del síntoma**, no la desaparición de la causa: un job que se salta el trabajo, un host que arranca o una red que vuelve producen el mismo verde que un arreglo real.
>
> Y si al reabrir se reutiliza la fila, el registro **pierde la única prueba de que la causa seguía viva**: la recurrencia. Un registro de incidencias sin ocurrencias conservadas no sirve para decidir si un arreglo funciona, solo para saber qué está rojo ahora.
>
> Formulación operativa: **`resolved` es una hipótesis, no un veredicto.** El veredicto exige nombrar qué cambió en el productor y qué producto existe después. Y toda incidencia que se cierra debería dejar su ocurrencia (fecha) en un histórico append-only, no en el mismo campo que se sobrescribe.

## 5. ¿En qué otros proyectos podría aplicarse?

- Cualquier sistema de alertas con estados tipo `resolved`/`ok`/`closed`: PagerDuty, Sentry, Alertmanager, Uptime Kuma, Zabbix.
- Gestión de incidencias humanas (ITIL, Jira): cerrar un ticket porque el usuario no volvió a llamar.
- Salud y mantenimiento: «la máquina no ha vuelto a dar error» como prueba de que la reparación funcionó.
- Ciencia experimental: dar por bueno un resultado porque no se ha reproducido el fallo (falsación por silencio).

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

Sería **FALSO** si, sobre **10 incidencias cerradas** del lab en **2 ciclos consecutivos**, en **8 o más** el cierre coincidiera con un cambio verificable en el productor (script/config con mtime posterior al `first_seen_at` y producto generado después) **y** el registro conservara el histórico de ocurrencias (reabrir no borra el cierre anterior). También lo falsaría que el lab no usara nunca `resolved` como prueba de reparación: si ninguna decisión (acta, `pendientes.md`, cierre de tarea) se apoyara en el estado `resolved`, el patrón no tendría consecuencia.

## 7. Decisión

- [x] Asciende a KNOWN.md como E1 — **PROMOVIDO el 2026-11-06 como E1-011** (3 ocurrencias en 2 jobs y 4 fechas, con 2 contraejemplos declarados). La fusión con CP-010 se descarta: objetos distintos (regla de cierre vs instrumento cualquiera)
- [ ] Asciende a procedures/ como procedimiento LPA (el antídoto «`resolved` es hipótesis; exigir mtime del productor + producto posterior + histórico de ocurrencias» **ya se aplica en este ciclo**, ver D1/D4 del acta del 23-10, pero sin documento propio)
- [ ] Sigue en incubación *— cerrado el 2026-11-06: asciende a E1-011*
- [ ] Se descarta
- [ ] Se fusiona con otro patrón (candidato declarado: **CP-010**, misma familia de instrumento)

**Fecha de revisión:** 2026-10-30 (semanal) y 2026-11-02 (mensual, donde se decide la fusión con CP-010).
**Justificación:** tres ocurrencias medidas (2 cierres sin reparación en 2 jobs + 1 historial sobrescrito), supera el umbral de 2, pero el registro afectado es uno solo y la semántica podría ser deliberada; se declara E0 y se fija revisión corta.

## 8. Criterio de cierre (fijado el 26-10-2026, decision E)

MARCA: CP-017-CRITERIO-CIERRE-20261026

Un `resolved` solo cuenta como reparacion si se cumplen las **tres** condiciones, cada una con salida literal:

1. **Productor cambiado despues del `first_seen_at`**: `stat -c %Y <script|config>` > `first_seen_at` de la ocurrencia. Sin mtime posterior, el cierre es hipotesis, no veredicto.
2. **Producto generado despues del cierre**: el artefacto que prueba la reparacion tiene mtime posterior al cierre. Un producto anterior al cierre no prueba nada.
3. **Ocurrencia previa conservada**: el cierre se anota como linea nueva (append-only); reabrir NO borra ni sobrescribe la ocurrencia anterior. Si el historico se pierde, el cierre deja de ser verificable.

Si falta cualquiera de las tres, el estado se queda en `open` con nota `resolved-sin-prueba`, y se nombra cual de las tres falta.

_Anotado 2026-10-26 17:46:07 CEST. La seccion 7 (decision) sigue en incubacion: este criterio no asciende el patron, solo define cuando un cierre es valido._

---

## Reexamen 2026-10-30 (ciclo semanal, ventana 23→30-10)

**(1) Segundo cierre CON reparación medido.** `bbc1d8_a5731c9ceec0` (`empleo-pipeline`): abierta 24-10 18:02 por `invalid_grant: Token has been expired or revoked`, `last_seen_at` 27-10 18:01, **cerrada 28-10 18:03:05** tras renovar la credencial OAuth. Cumple las tres condiciones del §8: (1) credencial/config renovada después de `first_seen_at`, (2) producto generado después del cierre, (3) ocurrencia conservada en la misma fila. Es un cierre de **credencial**, dominio que no estaba representado: los dos casos anteriores eran script/timeout.

**(2) Tercer sobrescrito documentado en la misma fila.** `264c02_761c7f27bcb0` — la misma fila que sirve de caso principal del patrón:

| acta | `closed_at` leído ese día |
|---|---|
| 16-10 | 2026-10-13 06:13 |
| 23-10 | 2026-10-23 07:46:58 |
| **30-10** | **2026-10-26 06:11:29** |

Tres lecturas, tres valores, un solo `id`. El historial no se conserva: cada reapertura sustituye el cierre anterior. Es exactamente la condición 3 del §8 incumplida por el registro.

**(3) Dato nuevo que refuerza el patrón: el cierre puede preceder a la reparación.** El cierre del 26-10 (06:11) llegó **11 horas antes** que la reparación real del vigilante (17:45). Hoy el cierre se sostiene *porque la reparación llegó después*, no porque el registro la exigiera. Si no hubiera llegado, la fila habría quedado `resolved` con el defecto intacto — como en los dos casos originales.

**Estado: E0 → E0.** Ya hay 2 cierres con reparación (contraejemplos) y 3 sobrescritos; lo que falta no es evidencia del mecanismo, sino decidir si el criterio del §8 **asciende a procedimiento** en la revisión mensual del 02-11. La fusión con CP-010 sigue sobre la mesa.



---

## Actualización 2026-11-06 (ciclo semanal LPA, ventana 30-10 → 06-11)

- **Reapertura medida:** el cierre aceptado el 28-10 con las 3 condiciones **no se sostuvo**. La misma fila (`bbc1d8_a5731c9ceec0`, job `bbc1d841e8a7`) registra `last_seen_at = 2026-11-01 18:01:55`, cuatro días después del cierre, y un nuevo `closed_at = 2026-11-02 18:02:39`. El `closed_at` anterior quedó sobrescrito.
- **Lectura:** la corrida siguiente como prueba de reparación funciona como *tregua*, no como reparación. El criterio de las 3 condiciones no incluye el tiempo.
- **Propuesta de criterio (no aplicada, decisión del usuario):** cierre válido = **7 días sin recurrencia** o **cambio de causa demostrado**; toda reapertura se registra como fila/nota nueva y no reescribe el `closed_at` anterior.
- **Acta:** `incidentes/revision-fallos-2026-11-06.md` (F3, D3). Backup: `.bak-20261106`.

## 9. Decisión mensual 2026-11-06

MARCA: CP-017-PROMOVIDO-E1-20261106

- **Ascendido a `KNOWN.md` como E1-011** en la revisión mensual del 2026-11-06 (acta `incidentes/revision-mensual-2026-11.md`, §3.3). Criterio: 3 ocurrencias en 2 jobs distintos y 4 fechas + falsación escrita (§5) + 2 contraejemplos declarados. El registro es uno solo (`cron_incidents`) → E1 «patrón observado».
- **Fusión con CP-010 descartada:** objetos distintos (regla de cierre frente a cualquier instrumento). Se mantiene la relación declarada con CP-018 (la firma incluye la fecha, así que la misma causa se cuenta como nueva).
- **Pendiente de decisión del usuario (no se ha escrito nada):** si el criterio del §8 (3 condiciones + **7 días sin recurrencia** + `closed_at` append-only, propuesto tras la reapertura del 01-11) asciende a `procedures/` como procedimiento de cierre. El ascenso a E1 **no** implica escribir el procedimiento.
- Backup: `CP-017-resolved-mide-la-corrida-siguiente-no-la-reparacion.md.bak-20261106`.


## 10. Procedimiento escrito 2026-11-06

MARCA: CP-017-PROCEDIMIENTO-ESCRITO-20261106

- El criterio del §8, ampliado con la permanencia (7 días sin recurrencia o cambio de causa demostrado) y el registro append-only, queda escrito como **`lpa/procedures/cierre-de-incidencia.md`** (v1, 2026-11-06), con estados `open` / `resolved-sin-prueba` / `resolved` / `reabierto`.
- Se escribió a petición del usuario tras la revisión mensual del 2026-11-06. El ascenso a `procedures/` no cambia el nivel de evidencia del patrón (sigue E1-011): documenta el criterio, no lo valida.
- El procedimiento declara explícitamente que la condición de 7 días **no es observable** con las retenciones medidas (`executions` ~1 día, artefactos del vigilante ~21 h), y que en ese caso el cierre no puede ser `resolved`.
- Backup de este fichero: `.bak-20261106-proc`.


## Reexamen 2026-11-13 (ciclo semanal LPA, ventana 06-11 → 13-11)

Acta: `lpa/incidentes/revision-fallos-2026-11-13.md` (F5/D2). Backup: `.bak-20261113`.

**Segundo cierre «verificado» que se rompe, y con la misma forma que el primero.** Cronología medida en `cron_incidents` para el job `bbc1d841e8a7` (`empleo-pipeline-diario`, `0 18 * * *`):

| Evento | Fecha | Fila |
|---|---|---|
| Cierre nº 1 (3 condiciones) | 28-10 | `bbc1d8_a5731c9ceec0` |
| Reapertura | 01-11 18:01 | misma fila, `last_seen` actualizado |
| Cierre nº 2 | 02-11 18:02 | mismo id, `closed_at` **sobrescrito** |
| **Reapertura (2 fallos el mismo día)** | **11-11 18:05:52 y 19:37:18** | `bbc1d8_aba390737219` (`timeout`) + `a5731c9ceec0` (`script`) |
| Cierre nº 3 | 12-11 18:05:17 | **las dos filas a la vez**, mismo `closed_at` |

- **El cierre nº 2 duró 9 días** (02-11 → 11-11) y el nº 1 duró 4 (28-10 → 01-11). El criterio escrito en `procedures/cierre-de-incidencia.md` exige **7 días sin recurrencia**; el nº 2 lo habría cumplido **por dos días** y aun así se rompió. Es la primera medición que muestra que **7 días tampoco basta** como umbral general (RULE-015: el umbral no se fija a priori).
- **Los dos fallos del 11-11 son de naturaleza distinta y se cerraron juntos:** (a) `Script timed out after 300s` a las 18:05:52 (artefacto de 229 B, solo la cabecera); (b) re-ejecución a las 19:37:18 que **produjo un artefacto de 16.044 B** y aun así terminó `exit 1`, con `stderr` que solo contiene un `FutureWarning` de `google-api-core` sobre Python 3.11. Un cierre en bloque de dos causas distintas es exactamente el defecto que este patrón describe: `resolved` mide «hubo una corrida sana después», no «la causa está reparada».
- **Nuevo borde detectado en (b):** un `FutureWarning` en `stderr` no debería producir `exit 1`; o el script traduce un aviso en fallo, o el código de salida viene de otro sitio que el `stderr` no muestra. El artefacto grande y el exit 1 conviven → **el producto existe y el semáforo está rojo**, el caso inverso al falso ok habitual y también engañoso (un rojo que no señala nada).
- **Nivel sin cambio (E1-011):** el patrón está confirmado, no ampliado. Afecta al procedimiento, no al nivel: el umbral de 7 días queda **sin respaldo empírico** y debe reformularse como «N días observados con retención suficiente», no como una cifra fija.

---

## Reexamen 2026-11-20 (semanal, ventana 13→20-11)

- **Tercer mecanismo de cierre falso, distinto de los dos anteriores: cerrar por salida de ventana.** El hueco del **12-11** (45 sesiones en `state.db`, sin `sesiones-delta-20261112.jsonl`) produjo **3 alertas** (`41a1a4_3c4b8c91fffb` 13-11 17:23; `41a1a4_6472980b291b` 13-11 22:35; `41a1a4_2288feb11262` 14-11 22:35) y las 3 se cerraron **a la vez** el **15-11 22:35:02.515752**. El hueco no se reparó: **salió de la ventana de 3 días** que mira `registrar_hel_diario.py` (`objetivo = [hoy-2, hoy-1, hoy]`). El job salió `ok` porque dejó de mirar, no porque el dato estuviera.
- **Causa raíz localizada en código (verificada):** el consumidor busca el fichero **nombrado por el día consolidado** (`registrar_hel_diario.py:160-165`, `sesiones-delta-<dd>.jsonl`) y el productor escribe el delta **nombrado por el día en que corre** (`consolidador_sesiones.py:121`, `sesiones-delta-{hoy}`). Un día rellenado hacia atrás **nunca tendrá delta con su propio nombre** → la alerta es segura. Prueba de que la consolidación sí se hizo: `resumen-dia-2026-11-12.md` existe (mtime 13-11 22:30:50) con «Sesiones del dia 2026-11-12: 45».
- **Precisión del recuento:** de las 3 alertas, **1 fue verdadera** (13-11 17:23: el resumen aún no existía, se creó a las 22:30) y **2 fueron falsas** (13-11 22:35 y 14-11 22:35: el resumen llevaba 4 minutos escrito). Es **una causa con alertas repetidas**, no dos ocurrencias en contextos distintos.
- **Cierre nº 3 roto:** el cierre del 12-11 18:05 duró **7 días exactos** y el pipeline de empleo volvió a fallar el **19-11 18:05** (`invalid_grant` de Gmail, ver acta 2026-11-20, F2) **sin abrir fila en `cron_incidents`**. Segunda medición que invalida la cifra fija de 7 días como umbral general.
- **Regla operativa que se añade a la revisión:** ante cualquier cierre, comprobar si coincide con **un cambio de causa** o con **un cambio de ventana/retención**. En esta ventana, 3 de 3 cierres coinciden con lo segundo.
- **Nivel:** sin cambio (E1-011). El patrón se confirma por tercera vía; lo que falta sigue siendo un criterio de cierre con respaldo empírico, no una cifra a priori (RULE-015).
