---
title: "Diseno EXP-20260903-001 — Coste real de errores/retrabajo en sesiones (baseline para ROI de metacognicion)"
type: research
---

# Diseno EXP-20260903-001 — Coste real de errores/retrabajo (baseline)

**VERACIDAD:** [ALCANCE INTERNO]
**Fecha:** 03-09-2026
**Origen:** sesion grill-idea + pregunta del usuario sobre ahorro de tokens de una capa metacognitiva avanzada. La ecuacion ROI = (errores evitados x coste medio del error) - (coste de la capa) no se puede resolver: el lab no mide el lado del error.
**Estado:** DISENO — pendiente de aprobacion para ejecutar (7 dias de registro).

## 1. Pregunta

¿Cuanto cuesta HOY (en tokens y tiempo) el retrabajo por errores y decisiones mal calibradas en las sesiones del lab? Con ese dato se decide con numero — no con estimacion — si una capa metacognitiva mas avanzada tiene ROI positivo.

## 2. Hipotesis (falsable, sin umbral a priori — RULE-015)

- H1: el retrabajo por errores/decisiones mal calibradas es material (>5% del gasto semanal). El umbral exacto NO se fija antes: se mide el baseline y se decide despues.
- H0: el retrabajo es marginal (<1%) y los gates actuales (SVP, KVC, PRED, revisar-decisiones, RULEs) ya capturan el beneficio — capa avanzada NO justificada.
- La medicion decide entre H1 y H0. No se decide antes de medir.

## 3. Definicion operativa: que cuenta como error/retrabajo (taxonomia cerrada)

| ID | Tipo | Ejemplo real conocido del lab |
|---|---|---|
| E1 | Re-ejecucion por error de comando/script | bug state.db v0.21.0 (02-03 sep): sesiones de recuperacion + 17 GB limpieza |
| E2 | Correccion de dato inventado (gate veracidad) | respuesta con dato sin fuente → contrastar → rehacer |
| E3 | Iteracion extra por prompt ambiguo (falta fase 0) | tarea lanzada a ciegas → no era lo que se pedia → rehacer |
| E4 | Debug de servicio/infra | OOM ComfyUI, swap 94%, watchdog |
| E5 | Verificacion redundante (no se confio) | re-verificar algo ya verificado por desconfianza/olvido |
| E6 | Reescritura por spec no cumplida | RF no cubierto al primer intento → iterar |
| E7 | Falso negativo/positivo del sistema | subagentes locales con informes pobres (4/5) → repetir con otro modelo |

NO cuenta: trabajo normal de una sola pasada, mejoras voluntarias, mantenimiento planificado.

## 4. Metodo

Fase 1 (BASELINE, 7 dias, herramientas ACTUALES sin capa metacognitiva):
1. Registro PROSPECTIVO (no retrospectivo: el jsonl de sesiones pesa 376 MB y duplica system_prompt — parsearlo entero no es rentable). Cada vez que ocurra un incidente E1-E7 en una sesion, el agente anade UNA linea a un ledger nuevo: `04-operations/metrics/retrabajo_ledger.jsonl` con: fecha, sesion_id, tipo (E1-E7), causa raiz (1 linea), tokens_estimados_correccion, tiempo_min, ejemplo (1 linea).
2. Estimacion de tokens sin LLM: ~4 chars/token (heuristica estandar ya usada en P1); con LLM: usage real si el endpoint lo da.
3. Registro en el momento o al cerrar la sesion — NUNCA de memoria dias despues (gate veracidad).
4. Al final de la semana: script de agregacion (conteo por tipo, suma tokens, % sobre gasto total de la semana si se puede estimar por sesiones; si no, % sobre horas de retrabajo) + informe con los N=7 ejemplos reales como evidencia.

Fase 2 (opcional, SOLO si fase 1 muestra materialidad): repetir 7 dias CON la intervencion candidata (p.ej. grill-idea sistematico en tareas grandes + registro automatico de senales) y comparar. Disenar fase 2 despues de ver los datos de fase 1, no antes.

## 5. Metricas

- Primaria: % retrabajo = tokens_retrabajo_semana / gasto_total_semana (o sustituto medible: horas_retrabajo / horas_sesion).
- Secundarias: distribucion por tipo E1-E7; top-3 causas raiz; coste medio por incidente.
- Calibracion: cuantos incidentes se detectaron por el propio proceso (gates) vs por el usuario (los gates fallados = donde una capa metacognitiva anadiria valor).

## 6. Criterios de calidad

- Cada entrada con ejemplo real de 1 linea (verificable en la sesion).
- Categorias cerradas (E1-E7) — sin categorias inventadas sobre la marcha.
- El registro no cambia el comportamiento: solo observa (regla del MEL-diseno: "registrar, no decidir").
- Coste del propio experimento: minimo (una linea por incidente, ~50-100 tokens) — el experimento NO debe costar mas que lo que mide.

## 7. Decision que alimenta

Con el % real medido: DEC sobre construir (o no) la capa metacognitiva avanzada del lab (diseno 04-ago, congelado). Si el retrabajo es <1%: confirmar el freeze con dato. Si es >5%: el diseno de la capa ligera selectiva (MEL-1 decisiones dudosas, MEL-2 procedimientos — no MEL en todo) pasa a prioridad con ROI calculado.

## 8. Entregables

- 04-operations/metrics/retrabajo_ledger.jsonl (7 dias de datos)
- research/exp-20260903-roi-metacognicion-resultados.md (informe con % real, tabla por tipo, ejemplos, veredicto H1/H0)
- DEC en backlog con backup (RULE-008/009)
