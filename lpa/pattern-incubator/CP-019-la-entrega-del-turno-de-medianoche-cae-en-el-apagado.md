---
type: candidate_pattern
id: CP-019
status: incubating
created: 2026-11-06
confidence: E0 (9 fallos de entrega medidos en un job + 3 jobs más con el mismo síntoma; causa raíz no asignada)
domain: observabilidad / fiabilidad-de-entrega
---

# CP-019 · La entrega del turno de medianoche cae en la ventana de apagado: 9 noches de avisos perdidos o en cola

> **Estado:** Incubación (E0)
> **Fecha:** 2026-11-06
> **Origen:** Revisión del acta `lpa/incidentes/revision-fallos-2026-11-06.md`. El acta lo registró como caso aislado («`7b5207` worker `-15` a las 00:00:43 del 03-11, sin estado terminal»). Medido hoy en solo lectura sobre `~/.hermes/logs/agent.log*` y `~/.hermes/logs/errors.log*`.
> **Nivel de confianza:** E0. La recurrencia está medida; la causa (apagado del host, parada del gateway o red ausente) no está asignada.

---

## 1. Qué ocurrió

El job `7b52075a99e5` (**watchdog-salud-sistema**, cron `0 */4 * * *`, 6 turnos al día) ha fallado la entrega del turno de **medianoche** en 9 noches distintas de un total de ~21 turnos de 00:00 en la ventana de 3 semanas:

| Fecha | Hora | Firma del error |
|---|---|---|
| 2026-10-17 | 06:59:25 | `ConnectError: [Errno -3] Temporary failure in name resolution` |
| 2026-10-20 | 07:12:51 | `send_path_degraded`, falling back to standalone |
| 2026-10-22 | 00:01:13 | `Timed out` |
| 2026-10-23 | 00:01:26 | `Timed out` |
| 2026-10-26 | 00:01:10 | `timed out after 30s (telegram-send)` |
| 2026-10-28 | 00:01:21 | `Timed out` |
| 2026-10-29 | 00:00:29 | `send_path_degraded` |
| 2026-11-01 | 00:01:18 | `ConnectError: All connection attempts failed` |
| 2026-11-05 | 00:00:42 | `send_path_degraded` (2 líneas) |

Además, el mismo síntoma aparece en otros tres jobs:

- `8bf412ac2ba3` (ficha-perfume-diaria) — 20-10 07:12:52, `send_path_degraded`
- `404f3a96481c` (coste-ahorro-diario) — 20-10 07:12:55, `send_path_degraded`
- `174499853a8b` (rag-reindex-catchup) — 01-11 00:07:51, `send_path_degraded`

**Cuatro firmas distintas para el mismo defecto** (`ConnectError` DNS, `ConnectError` sin resolución, `Timed out`, `send_path_degraded`). Bajo el criterio de CP-018, cada una cuenta como incidencia nueva y no acumula historia: por eso el patrón no había emergido del registro de incidencias.

## 2. Lo que sí se pierde

En 4 de esas noches el mensaje **no se entregó en vivo** y quedó en cola:

```
2026-10-20 07:12:51  queued for redelivery
2026-10-29 00:00:44  queued for redelivery
2026-11-01 00:08:00  queued for redelivery
2026-11-05 00:01:02  queued for redelivery
```

No está medido si la reentrega llegó a producirse. Es un aviso de salud del sistema: si se pierde, el fallo que debía avisar queda invisible.

## 3. Hipótesis abiertas (ninguna asignada)

1. El turno de 00:00 coincide con el apagado o suspensión del host, y el gateway recibe `SIGTERM` a mitad de la entrega.
2. La red está caída en esa franja (el registro del 17-10 muestra fallo de DNS, no de Telegram).
3. `send_path_degraded` es una degradación previa (adaptador vivo pero no confirmado) que se convierte en pérdida cuando no hay nadie que reconecte.

Dato que apoya la 1 y no la confirma: en la misma ventana hay **10 salidas `UNCLEANLY`** con `suspected_oom=False` y heartbeat ~23:00.

## 4. Hallazgo de instrumento asociado

La tabla `executions` de `~/.hermes/cron/executions.db` retenía, a fecha de hoy, **1.000 filas con rango `2026-11-05T15:00:10` → `2026-11-06T16:38:21`**: aproximadamente **un día** de histórico. Consecuencias:

- La fila del `7b5207` del 03-11 que cita el acta **ya no existe**: no se puede verificar ni desmentir.
- Cualquier revisión semanal que se apoye en esa tabla mide como máximo el último día, y lo hace sin avisar.
- `cron_incidents` (28 filas) sí conserva histórico; `executions` no.

## 5. Antídoto propuesto (no aplicado)

- Medir la entrega por el **artefacto entregado** y no por el status del job (RULE-021): contar `Sending media group` / `queued for redelivery` por turno.
- Declarar el límite de retención de `executions` en el procedimiento de revisión, o subir la retención si el coste es aceptable.
- No cambiar el cron del watchdog sin medir antes qué turnos son alcanzables: mover la hora sin datos solo traslada el fallo.

## 6. Relación con otros CP

- **CP-018** (la firma incluye el dato que cambia): misma mecánica, cuatro firmas para un defecto.
- **CP-015** (la corrida que muere sin artefacto no deja señal): el turno que no entrega no deja rastro en `executions` porque la fila desaparece por retención.
- **CP-010** (instrumento no validado miente): retención no declarada.
