---
type: candidate_pattern
id: CP-016
status: incubating
created: 2026-10-23
confidence: E0 (4 reinicios nocturnos en 3 noches distintas + 1 fallo de script medido directo)
domain: automatizacion-del-lab / vigilancia
---

# CP-016 · El vigilante que comprueba la red reinicia un servicio sano — y muere al notificarlo

> **Estado:** Incubación (E0→E1)
> **Fecha:** 2026-10-23
> **Origen:** Ciclo semanal LPA, ventana 17→23-10-2026 (acta `incidentes/revision-fallos-2026-10-23.md`, decisión D2). Evidencia recogida en solo lectura: `journalctl --user -u hermes-gateway.service --since "7 days ago"`, `~/.hermes/cron/output/264c02dae003/`, `~/.hermes/cron/executions.db`, y lectura del propio `~/.hermes/scripts/telegram-watchdog.sh`.
> **Nivel de confianza:** E0 (mecanismo leído en el código y **un** fallo medido de punta a punta; los otros 3 reinicios son temporalmente compatibles, no atribuidos con prueba directa)

---

## 1. Qué ocurrió

`telegram-watchdog.sh` (job `264c02dae003`, cada 15 min) hace tres comprobaciones seguidas. La segunda es: `curl getMe` a la API de Telegram; si el código HTTP **no** es 200, ejecuta `systemctl --user restart hermes-gateway.service` y avisa por Telegram.

En el lab hay una **ventana sin red de 00:00 a 07:00**. Dentro de esa ventana `getMe` no devuelve 200: devuelve **`HTTP 000000`** (curl sin resolución DNS), que no es «el gateway está caído», es «no hay red». El vigilante no distingue una cosa de la otra: **reinicia un servicio que estaba funcionando**, y lo hace cada 15 minutos mientras la ventana dure.

El bucle se rompe solo porque el host se apaga a los pocos minutos de medianoche. Cuando el host sigue encendido más rato (noche del 17→18-10), el reinicio **se repite**: `00:06:00 Stopping → 00:09:03 Started` y `00:25:16 Stopping → 00:28:20 Started` — 19 min de diferencia, la cadencia del propio job.

El remate lo pone el `set -e` del script: la notificación del reinicio es otro `curl` **sin `|| true`** (`telegram-watchdog.sh`, 3 apariciones de `sendMessage`, **0** protegidas). Sin red ese `curl` muere con **exit 6** (no resuelve el host) y `set -e` aborta el script **antes** de su `echo "Reiniciado por fallo de API."; exit 0`. Resultado: el job se registra como fallo (`Script exited with code 6`) **precisamente en el escenario que el script existía para manejar**, y el aviso que iba a mandar nunca sale.

## 2. Evidencia que lo respalda

**Reinicios nocturnos del gateway (7 días, `journalctl --user`), literal recortado:**

| noche | `Stopping` | `Started` | ¿host apagado en ese momento? |
|---|---|---|---|
| 17→18-10 | 00:06:00 | 00:09:03 | No (sigue hasta las 00:28) |
| 17→18-10 | 00:25:16 | 00:28:20 | No (se apaga a las 00:28:20+) |
| 21→22-10 | 00:10:47 | 00:13:52 | No (se apaga a las 00:23:51) |
| 22→23-10 | 00:03:56 | 00:07:02 | No (se apaga a las 00:17:37) |

- **4 reinicios en 3 noches distintas, todos entre 00:03 y 00:28.** Ninguno coincide con un arranque del host: los arranques del periodo son `20-10 07:16:21`, `21-10 08:10:05`, `22-10 06:27:11`, `23-10 07:46:22`.
- **Prueba directa del mecanismo (23-10):** `~/.hermes/cron/output/264c02dae003/2026-10-23_00-07-19.md` (248 B) contiene `WARN: API Telegram no responde (HTTP 000000). Reiniciando gateway...` y la fila de `executions` `2c54785d807b419684b34db9cb0b3e84` (job `264c02dae003`) está `failed` con `Script exited with code 6`, de 00:03:42 a 00:07:19.
- **Evidencia de código:** `~/.hermes/scripts/telegram-watchdog.sh` (mtime 25-jul) — paso 2: `if [ "$HTTP_CODE" != "200" ]; then ... systemctl --user restart hermes-gateway.service`; los `curl sendMessage` no llevan `|| true` bajo `set -e`. El mismo defecto de forma aparece en `~/.hermes/scripts/ceder-control.sh` (1 `sendMessage`, 0 protegidos), aunque ahí no hay fallo medido.
- **Estado del servicio:** hoy `systemctl --user is-active` = `active`, `ActiveEnterTimestamp=Fri 2026-10-23 07:46:22 CEST`. No hay ninguna evidencia de que el gateway estuviera caído en ninguno de los 4 reinicios.

## 3. Contradicciones o limitaciones

- **3 de los 4 reinicios son compatibilidad temporal, no atribución.** Solo el del 23-10 tiene fichero de salida que nombra el reinicio. Los del 18-10 y 22-10 no dejan artefacto (los informes de un job de intervalo solo se conservan ~50 ficheros) y el `journalctl` no dice *quién* pidió el `restart`. Que sea el watchdog es la hipótesis con más apoyo (ventana horaria + cadencia + ser el único script del lab que hace `restart` de ese servicio), **no un hecho probado** en esos tres casos.
- **El incidente no lleva 7 semanas contando 7 semanas.** La fila `264c02_761c7f27bcb0` nació el 16-09 y su `last_seen_at` es el 23-10, pero **cuántas veces ocurrió es incontable** con este registro: la fila es única por firma y se sobrescribe (ver **CP-017**). Es el mismo límite que impide medir la recurrencia.
- **La ventana sin red no está documentada en el repo**, solo en la memoria del agente («wifi OFF 00-07»). El `HTTP 000000` a las 00:07 es la única prueba de esta acta de que a esa hora no hay red.
- **No se ha comprobado el efecto del reinicio** sobre sesiones o mensajes en vuelo. El daño medido es «servicio sano reiniciado 4 veces» + «job en rojo»; el daño no medido es el que pudo causar cada reinicio.
- **Frontera con otros patrones:** no es CP-013 (ese es *no correr a su hora*; aquí el job **sí** corre) ni CP-015 (aquí sí hay artefacto y dice lo que pasa: el problema es lo que el script hace con la señal). Su vecino más cercano es **CP-010**: el vigilante usa como señal de «servicio caído» una medida de otra cosa.

## 4. Principio que parece emerger

> Un remedio automático solo debe dispararse por la causa que puede arreglar. Si la señal que lo dispara es **disponibilidad de red** y el remedio es **reiniciar un servicio local**, el remedio no puede funcionar: la red no está bajo su control. En una ventana sin conectividad eso no produce un aviso, produce **un reinicio periódico de algo que funcionaba**.
>
> Corolario del `set -e`: **el camino de emergencia de un script no puede depender del recurso cuya ausencia lo activó**. Si la notificación del remedio usa ese mismo recurso sin proteger el error (`|| true`), el script muere en la notificación y el fallo queda registrado como «el job falló» — que es la conclusión contraria a la verdad.

## 5. ¿En qué otros proyectos podría aplicarse?

- Cualquier watchdog de disponibilidad que use una comprobación externa (API, DNS, ping) para decidir reiniciar un servicio local.
- Hosts domésticos o portátiles con ventanas de desconexión (ahorro, horario, tarifa): el patrón convierte cada ventana en una tormenta de reinicios.
- Kubernetes/health-checks: una `livenessProbe` que mide dependencias externas provoca reinicios en cascada cuando cae el proveedor, no el servicio.
- Cualquier `set -e` con notificación al final: el aviso de fallo es lo primero que se pierde justo cuando más falta hace.

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

Sería **FALSO** si, sobre **10 noches con la ventana sin red y el host encendido**, en **8 o más** el gateway **no** se reinicia (porque el watchdog distingue `000` de «servicio caído», o porque no corre en esa ventana), **y** además el script no sale con código de error en ninguna de esas noches. También lo falsaría que los reinicios observados se debieran a otra causa demostrable (crash real del gateway, `Scheduled restart` de systemd, orden del usuario) en ≥8 de 10, o que el reinicio no tuviera efecto observable (servicio sin sesiones, sin mensajes en vuelo).

## 7. Decisión

- [ ] Asciende a KNOWN.md como E1 (falta: atribución directa de los 4 reinicios, no solo de 1, y un segundo entorno)
- [ ] Asciende a procedures/ como procedimiento LPA (el antídoto —«un watchdog distingue red de servicio, y protege sus notificaciones»— es evidente pero **no se ha aplicado**)
- [x] Sigue en incubación
- [ ] Se descarta
- [ ] Se fusiona con otro patrón (candidato declarado: **CP-010**, por usar una medida de otra cosa como señal de estado)

**Fecha de revisión:** 2026-10-30 (semanal) y 2026-11-02 (mensual).
**Justificación:** el mecanismo está leído en el código y una de sus ocurrencias está medida de punta a punta con artefacto y fila de ejecución; las otras tres son compatibles pero no atribuidas. Supera el umbral de 2 ocurrencias en contextos distintos (3 noches), pero la atribución incompleta obliga a E0.

**Antídoto propuesto (no aplicado, requiere autorización explícita porque toca `~/.hermes/scripts/`):**
1. Distinguir red de servicio: `HTTP 000`/`000000` ⇒ **no** reiniciar; solo reiniciar si el proceso systemd está `inactive`/`failed`.
2. Proteger **todos** los `curl sendMessage` con `|| true` (o `curl ... || echo "sin red"`), y escribir el resultado antes de salir.
3. No programar el watchdog dentro de la ventana sin red, o hacer que en esa ventana salga en verde con `sin_red`.

---

## Reexamen 2026-10-30 (ciclo semanal, ventana 23→30-10)

**Antídoto aplicado y medido.** `~/.hermes/scripts/telegram-watchdog.sh`, 4.178 B, **mtime 2026-10-26 17:45:31** (posterior al `first_seen_at` de la incidencia, condición 1 de CP-017). Quedó así:

- `HTTP_CODE="${HTTP_CODE: -3}"` — normaliza a 3 dígitos, así que `000000` ya no existe.
- `case "$HTTP_CODE" in 000)` → **no reinicia nunca**; dentro de la ventana sin red sale en verde con `sin_red`, fuera de ella avisa y sigue sin reiniciar.
- `notify` protegido: el camino de emergencia ya no depende del recurso cuya ausencia lo activó.

**Medición de la ventana (24→30-10):**
- **0 apariciones de «Reiniciando gateway»** en los artefactos del job (antes: 1 por noche).
- **0 incidencias nuevas** de `264c02dae003`; la fila cerró el 26-10 06:11.
- **2 noches con el host encendido dentro de la ventana sin red** (28-10 00:00→00:20, 29-10 00:00→00:27) sin reinicio. Las otras dos noches el host ya estaba apagado antes de medianoche → **no cuentan como prueba**.

**Estado: E0 → E0 (antídoto verificado).** La falsación pide 10 noches con ventana sin red y host encendido; hay 2. Falta evidencia, no mecanismo.



---

## Actualización 2026-11-06 (ciclo semanal LPA, ventana 30-10 → 06-11)

- **Evidencia a favor:** **0** líneas `Reiniciando gateway` en todos los artefactos de `~/.hermes/cron/output/264c02dae003/` de octubre y noviembre de 2026. En la ventana hubo **8 vidas del gateway** y ninguna fue reiniciada por el vigilante (antes: 4 reinicios en 3 noches).
- **Nivel: sin cambio (sigue E0).** No se ha verificado que el vigilante llegara a **detectar** red caída con el host encendido en la franja 00–07: esa franja se solapa con los apagados nocturnos (10 salidas `exited UNCLEANLY` en 7 días, todas con `suspected_oom=False` y heartbeat ~23:00), así que «no reinició» puede significar «no llegó a comprobar».
- **Pista, no evidencia:** la noche del 01→02-11 el host estuvo encendido hasta las 11:54 (boot `-7`), sin reinicio del vigilante registrado.
- **Falsación:** si en una noche con host encendido y red caída aparece una línea `Reiniciando gateway`, el patrón se reactiva y sube de nivel con esa prueba.
- **Acta:** `incidentes/revision-fallos-2026-11-06.md` (F5, D5). Backup: `.bak-20261106`.
