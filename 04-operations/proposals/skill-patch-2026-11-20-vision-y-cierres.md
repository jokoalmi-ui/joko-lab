---
title: "Parche de skill STAGED — 2026-11-20 (visión sin traza · cierres por ventana)"
type: knowledge
status: pendiente-de-aprobacion
---

# Parche de skill staged — 2026-11-20

**No aplicado.** Se deja aquí para que el usuario decida. Origen: acta `lpa/incidentes/revision-fallos-2026-11-20.md` (F1, F3, F6) y las 5 lecciones registradas en el ledger el 20-11.

## Patch 1 — skill `perfume-del-dia`

Añadir al bloque de reglas, tras la obligación de declarar la degradación:

> **Visión sin traza = no verificado.** No escribir «verificado por visión», «el VLM leyó» ni equivalentes si no hay una traza del instrumento en ese turno (carga del modelo + respuesta). El journal solo registra los fallos, así que un `vision_analyze` correcto es invisible: si no hay traza, la frase correcta es «no verificado por visión: `vision_analyze` no operativo (<motivo>)». Una afirmación de verificación que el registro no puede contradecir es peor que declarar la omisión.

## Patch 2 — skill `hermes-cron-jobs`

Añadir a la sección de diagnóstico de incidencias:

> **Antes de aceptar un `resolved`:** comprobar (a) la **retención** de `executions.db` (ventana real entre MIN y MAX `started_at`, no el número de filas) y (b) si el cierre coincide con un **cambio de ventana** del job consumidor en vez de con la reparación de la causa. Cerrar 3 filas en el mismo segundo es señal de barrido, no de arreglo.
>
> **Productor/consumidor de artefactos:** si el consumidor busca un nombre derivado de la fecha, verificar que el productor usa **la misma fecha** (día consolidado, no día de ejecución). Un desfase de nombre genera «huecos» que no existen.

## Patch 3 — skill `watchdog-salud-sistema`

> Un vigilante que corre como job del mismo servicio que vigila no puede levantar ese servicio: si el proceso muere, el planificador muere con él. Declarar siempre la **ventana de retención** de sus artefactos; sin ella, «0 reinicios en N semanas» no es una medición.

## Verificación pendiente antes de aplicar
- Comprobar que `perfume-del-dia` no tiene ya una regla equivalente (evitar duplicado).
- Comprobar el nombre exacto de la sección en `hermes-cron-jobs` y `watchdog-salud-sistema` antes del `patch` (old_string único).
