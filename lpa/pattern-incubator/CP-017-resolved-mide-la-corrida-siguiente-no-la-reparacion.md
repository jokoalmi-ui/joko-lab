---
type: candidate_pattern
id: CP-017
status: incubating
created: 2026-10-23
confidence: E0 (3 ocurrencias: 2 cierres sin reparación + 1 historial sobrescrito, en 2 jobs distintos)
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

- [ ] Asciende a KNOWN.md como E1 (falta: medir cierres en 2 ciclos más y decidir la fusión con CP-010)
- [ ] Asciende a procedures/ como procedimiento LPA (el antídoto «`resolved` es hipótesis; exigir mtime del productor + producto posterior + histórico de ocurrencias» **ya se aplica en este ciclo**, ver D1/D4 del acta del 23-10, pero sin documento propio)
- [x] Sigue en incubación
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

