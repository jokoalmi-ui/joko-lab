---
type: lpa
subtype: procedure
status: active
tags: [lpa, procedure, incidentes, cierre]
created: 2026-11-06
source: CP-017 (E1-011)
---

# Cierre de incidencia — Procedimiento de verificación (v1)

MARCA: LPA-PROC-CIERRE-v1-20261106

**Tipo:** Procedimiento LPA — operación de validación
**Fecha:** 2026-11-06
**Origen:** CP-017 «`resolved` mide la corrida siguiente, no la reparación» (ascendido a E1-011 el 2026-11-06)
**Estado:** activo

---

## Problema que resuelve

Una incidencia se marca `resolved` cuando deja de verse. Dejar de verse no es estar reparada.

Casos medidos que sostienen el procedimiento:

- **`bbc1d8_a5731c9ceec0`** (job `bbc1d841e8a7`): cerrada el 28-10 tras renovar la credencial OAuth, cumpliendo las tres condiciones de entonces. El 01-11 18:01:55 volvió a registrarse y el `closed_at` fue sobrescrito por `2026-11-02 18:02:39`. El cierre no se sostuvo cuatro días.
- **`264c02_761c7f27bcb0`**: una sola fila con tres `closed_at` distintos leídos en tres actas (13-10, 23-10, 26-10). El historial no se conserva.
- El cierre del 26-10 (06:11) llegó **11 horas antes** de la reparación real del vigilante (17:45). Se sostuvo porque la reparación llegó después, no porque el registro la exigiera.

---

## Regla

Un cierre solo es válido si se cumplen las **tres condiciones de prueba** y, además, **una de las dos condiciones de permanencia**.

### Condiciones de prueba (las tres, con salida literal)

1. **Productor cambiado después del `first_seen_at`**
   `stat -c %Y <script|config>` > `first_seen_at` de la ocurrencia.
   Sin mtime posterior, el cierre es hipótesis, no veredicto.

2. **Producto generado después del cierre**
   El artefacto que prueba la reparación tiene mtime posterior al `closed_at`.
   Un producto anterior al cierre no prueba nada.

3. **Ocurrencia previa conservada**
   El cierre se anota como línea nueva (append-only). Reabrir **no** borra ni sobrescribe la ocurrencia anterior.
   Si el histórico se pierde, el cierre deja de ser verificable.

### Condiciones de permanencia (una de las dos)

4. **7 días sin recurrencia** contados desde el cierre, con la ventana observable en el instrumento.
5. **Cambio de causa demostrado**: la causa que produjo la ocurrencia ya no existe (credencial renovada, servicio retirado, código eliminado), con evidencia de ese cambio, no solo ausencia de síntoma.

---

## Estados

| Estado | Significado |
|---|---|
| `open` | abierta, sin prueba de reparación |
| `resolved-sin-prueba` | alguien la cerró y falta al menos una condición; se nombra cuál |
| `resolved` | las 3 condiciones de prueba + una de permanencia, con salida literal |
| `reabierto` | la recurrencia llegó dentro de la ventana; se anota línea nueva, no se reescribe |

---

## Procedimiento

1. **Leer la ocurrencia completa** (solo lectura):
   `sqlite3 ~/.hermes/cron/executions.db "select id, job_id, state, first_seen_at, last_seen_at, closed_at from cron_incidents where id='<id>';"`
   Anotar las tres fechas tal como están.

2. **Verificar condición 1** — mtime del productor contra `first_seen_at`.
   Si el fichero que falló no tiene mtime posterior, parar aquí: no hay reparación, hay silencio.

3. **Verificar condición 2** — mtime del producto (informe, acta, log de la corrida) contra `closed_at`.
   Si no hay producto posterior, el cierre es hipótesis.

4. **Verificar condición 3** — ¿la ocurrencia anterior sigue en el registro?
   Si el `closed_at` cambió respecto a lo leído en un acta anterior, la condición 3 está rota: el cierre no es verificable aunque el síntoma haya desaparecido.

5. **Verificar permanencia** — 7 días sin recurrencia con ventana observable, o cambio de causa documentado.

6. **Escribir el veredicto** con la salida literal de los pasos 1-5 y el estado resultante. Si falta algo: `resolved-sin-prueba` + qué falta.

---

## Qué NO es prueba de reparación

- La corrida siguiente terminó bien.
- El `status` del job en el scheduler.
- `EXIT=0` de un wrapper.
- Ausencia de la palabra «error» en los logs, sin ventana declarada.
- Un cierre escrito a mano sin mtime ni producto posterior.
- Que el síntoma no aparezca en una tabla cuya retención es más corta que la ventana que se quiere afirmar.

---

## Límites de instrumento (declararlos en cada cierre)

- `cron_incidents` es **un solo registro**: sirve para contar ocurrencias, no para reconstruir historia.
- `executions` retuvo ~1 día en la medición del 06-11 (1.001 filas, 05-11 16:15 → 06-11 17:55).
- Los artefactos del vigilante cubren ~21 h.

Con esas retenciones, **la condición 4 (7 días) no es observable**. Cuando eso ocurre, el cierre no puede ser `resolved`: se queda en `resolved-sin-prueba` con el hueco nombrado, o en `open`. Afirmar siete días limpios sobre una ventana de un día es un falso ok.

---

## Relación con otras reglas

- **RULE-021** (el ok se acredita en el artefacto): este procedimiento es su aplicación al cierre de incidencias.
- **RULE-015** (control negativo antes de confiar en una métrica): antes de usar una tabla para afirmar permanencia, medir cuánto retiene.
- **CP-018** (la firma incluye el dato que cambia en cada intento): una reapertura con fecha distinta cuenta como ocurrencia nueva; no invalida el procedimiento, lo alimenta.
- **CP-010** (instrumento no validado miente): un `resolved` sin prueba es el instrumento mintiendo.

---

## Revisión

Se revisa en cada ciclo mensual LPA. Si en tres cierres consecutivos el criterio no cambia ningún veredicto, el procedimiento se simplifica; si un cierre válido vuelve a abrirse dentro de los 7 días, se revisa la condición de permanencia.
