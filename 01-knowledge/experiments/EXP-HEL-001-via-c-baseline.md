---
title: "EXP-HEL-001 — Estudio observacional de activación del razonamiento (vía C, baseline)"
type: EXP
---

# EXP-HEL-001 — Activación del razonamiento antes de responder (baseline vía C)

**Estado:** EN EJECUCIÓN — Fase 1 observacional iniciada 07-ago-2026 (confirmación de Joseba). Corte previsto: 14-ago-2026. Modo de registro: a posteriori por sesión (declaración del agente + verificación con SVP Procedure Check). Ledger `respuestas_hel.jsonl` creado; EXP registrada en `evolution.jsonl` (EXP-HEL-001-VIA-C). **ACTUALIZACIÓN 10-ago: backfill de los días 08-09 (15 entradas de preguntas de estado reales, selección manual desde sesiones) + instrumentación automática (tools/registrar_hel_diario.py + cron 22:35, no_agent). Ledger: 23 entradas (07:6, 08:4, 09:13). VERIFICACIÓN POSTERIOR COMPLETADA 10-ago → 21/23 activación verificada (91%), 2/23 de memoria (9%): "cuanto queda para dejar bien el lab?" y "Qu más queda??" — la PRIMERA respuesta fue de memoria (las tool calls posteriores eran de la siguiente tarea). ANÁLISIS DE SESGO (47 preguntas de estado en sesiones 08-09): 89% con herramientas, 11% de memoria; el registro manual captura preferentemente casos con actividad (sesgo de selección leve), pero el 9-11% de respuestas de memoria ES detectable → el baseline SÍ discrimina.**
**Tipo:** EXP-HEL-001 (primer experimento de H-HEL-001; vía C decidida por Joseba el 07-ago-2026).
**Método:** Observacional en fase 1 (solo lectura, sin cambios de comportamiento); comparación con intervención en fase 2 (solo si la fase 1 lo justifica).

## Hipótesis

> **H-HEL-001 (formulación canónica):** La DECISIÓN de activar deliberadamente una fase previa de construcción de contexto y razonamiento, cuando la naturaleza de la pregunta lo requiere, reduce los errores de primera respuesta respecto a responder directamente desde la memoria paramétrica.

Independiente del mecanismo (leer el LAB, RAG, herramientas, subagente, generar alternativas). Referencias: lpa/HYPOTHESIS.md (H-HEL-001), research/reasoning-gate-diseno.md (RULE-PROC-001..005, Evidence Arbitration Layer), lpa/patterns-observed.md (E0 07-ago).

## Método

Fuentes:
- `04-operations/metrics/operations_ledger.jsonl` — ya existe (creado por PIL-001, 06-ago; 11 operaciones). Sirve de denominador de operaciones reales. NO se modifica su formato.
- `04-operations/metrics/sesiones/sesiones-YYYYMMDD.jsonl` — registro automático de sesiones (ya existente).
- `04-operations/metrics/respuestas_hel.jsonl` — ledger NUEVO propuesto (requiere confirmación de Joseba para crearlo). Instrumentación defensiva (try/except), como los ledgers del OBSERVER. NO tocar `mel_ledger.jsonl` (Architecture Freeze).
- Verifier: SVP Procedure Check (research/reasoning-gate-diseno.md sección 5) como verificador externo de la activación (declarada vs verificada).

Variables por respuesta de estado registrada:
- `tipo_pregunta`: factual | estado | estratégica | diseño (la clasificación que RULE-PROC-005/State Question Detector propone).
- `activacion_declarada`: sí/no (auto-reporte del agente al responder).
- `activacion_verificada`: sí/no + evidencia (comando lanzado, archivo abierto, fuente citada en la respuesta). La declarada sin verificación NO cuenta como activación (lección KVC-001; patrón SVP-A/SVP-B).
- `resultado`: correcto | incorrecto | desconocido (verificación posterior, no auto-judicio).
- `coste_tokens`, `latencia` (aproximados, del registro de sesión).

Ejecución — EXECUTION PATH (6 campos mínimos, decisión 07-ago: instrumentar lo mínimo):
- `execution_path`: lista de etapas reales recorridas (memoria | clasificación | rag | rule | fuente | verificación | modelo) — el grafo ejecutado, no la intención.
- `memory_used`: sí/no (¿se respondió desde memoria sin contraste?).
- `rag_used`: sí/no (¿se consultó el RAG?).
- `rules_used`: lista de RULEs que participaron en la respuesta.
- `external_sources`: lista de fuentes externas consultadas.
- `verification_done`: sí/no (¿se ejecutó verificación con evidencia?).

NOTA limitación: las entradas 1-6 (07-ago) se registraron antes de definir el path; NO se reconstruyen (Historical Integrity). Las entradas nuevas lo llevan.

PENDIENTE (D, retrasado por decisión de Joseba 07-ago): documentar la lección del instrumento (observer) como patrón del lab SOLO tras validar que el fix A explica la anomalía con datos de varios días.

Métricas derivadas:
- MOR (Memory Override Rate) = overrides / consultas de estado.
- MTE (Memory Trust Error) = errores_por_memoria / respuestas_desde_memoria.
- Ratio activación verificada/declarada (mide Goodhart: cuánto de lo declarado se sostiene con evidencia).
- % veces que la respuesta final no coincide con la primera hipótesis (solo medible en fase de intervención).

Regla: NO se fija ningún umbral a priori. Los umbrales se derivan de la distribución tras ≥1 semana de datos (patrón Observation Before Automation).

## Protocolo Fase 1 (baseline)

1. Registrar respuestas de estado reales tal como ocurren hoy, SIN introducir activación deliberada. El objetivo es medir el comportamiento actual: cuántas respuestas se emiten desde memoria, cuántas activan contraste de forma natural, cuántas fallan y cuánto cuestan.
2. Duración mínima: 7 días de operación real (puerta de evidencia del lab).
3. Prohibido proponer o aplicar cambios de comportamiento durante el piloto (patrón 16: fase observacional separada de la propositiva). Las anomalías se registran como hipótesis a falsar, no como justificación para tocar el sistema.
4. El registro de respuestas puede ser a posteriori por sesión (las sesiones ya se guardan automáticamente); la verificación (declarada vs verificada) la hace el Verifier con el SVP Procedure Check.

## Criterios de éxito (NO binarios)

- ÉXITO: patrón estable — la activación verificada correlaciona con menos errores de primera respuesta Y MOR/MTE discriminan, con coste justificado por la distribución real.
- NEUTRO: sin patrón consistente en el baseline (ni a favor ni en contra).
- NEGATIVO: las métricas no discriminan, o el coste (tokens/latencia) supera el beneficio medido → H-HEL-001 se rechaza o se reformula según EVF.

## Qué falsearía la hipótesis

Que la activación deliberada no reduzca la tasa de errores de primera respuesta respecto al baseline, o que el coste medido supere el beneficio medido con la distribución real.

## Siguientes pasos

1. Crear `04-operations/metrics/respuestas_hel.jsonl` (ledger nuevo, defensivo; sin tocar mel_ledger). HECHO (07-ago).
2. Definir el punto de registro (al emitir una respuesta de estado, el agente declara; el Verifier contrasta). HECHO: modo a posteriori por sesión.
3. Registrar esta EXP en `04-operations/metrics/evolution.jsonl`. HECHO (EXP-HEL-001-VIA-C, 07-ago).
4. Fijar fecha de inicio del baseline. HECHO: inicio 07-ago, corte previsto 14-ago.
5. Tras el análisis del baseline: decidir intervención (activación deliberada) o descarte, con informe en `04-operations/reports/`. PENDIENTE.

## 📊 ESTADO 11-ago (verificado, pre-corte 14-ago)

**Datos al 11-ago (4 días: 07-10):**
- Total preguntas de estado: **47** (07:6, 08:4, 09:13, 10:24 — el día 10 con instrumentación automática)
- Con activación verificada (tools): **43 (91%)**
- De memoria (sin tools): **4 (9%)** — 2 del backfill + 2 del día 10
- Resultado: 47 correcto (100%)
- **El baseline DISCRIMINA** (9% de memoria detectable) → la fase 2 tendrá contraste real

**Pendiente para el corte (14-ago):** esperar días 11-13 (cron 22:35 captura automática)
y hacer el análisis final completo (medias, tendencia, comparación fase 2).
