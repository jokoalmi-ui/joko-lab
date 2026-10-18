---
title: "Informe — Loop Engineering Entrega 1: F1 Observer + F2 Evidence (primera ejecución)"
type: operations
---

# Informe — Loop Engineering Entrega 1: F1 Observer + F2 Evidence (primera ejecución)

**Fecha:** 2026-08-04
**Estado:** IMPLEMENTADO y EJECUTADO contra el ledger real
**Decisiones de referencia:** loop-engineering-diseno.md (04-ago: F1-F2+Baseline aprobado, F3-F6 bloqueados, sin umbrales a priori)

## Herramientas

- `hermes-lab/loop-engineering/observer.py` (F1) — ledger → estadísticas (hechos, no conclusiones)
- `hermes-lab/loop-engineering/evidence.py` (F2) — dashboard (preguntas, no decisiones)
- Fuente: `/mnt/ssd_ia_datos/lab-state/decision-ledger.jsonl` (328 entradas, 0 corruptas, 2026-07-29 → 2026-08-04)

## Resultados reales (primera ejecución)

| Regla | Veces | % del tráfico |
|---|---|---|
| Horario | 272 | 82.9% |
| Gpu | 44 | 13.4% |
| Privacidad | 11 | 3.4% |
| Disponibilidad | 1 | 0.3% |

Por provider: deepseek 236 (72.0%), lmstudio 44 (13.4%), gemini 37 (11.3%), ollama 11 (3.4%).
Por día: 29-jul 25, 30-jul 30, 31-jul 38, 01-ago 33, 02-ago 27, 03-ago 30, **04-ago 145**.

## Hallazgos (preguntas respondidas con datos)

1. **Horario domina el tráfico (82.9%).** Con el umbral del 70% del diseño original a priori, esto habría generado una propuesta automática. HOY es esperado: tras la DEC-2026-08-04 (horario 00:00-23:59 → deepseek siempre), la regla Horario debe decidir ~siempre. Confirma: los umbrales no se fijan sin conocer la política vigente.
2. **Privacidad apareció SOLO hoy (04-ago, 11 decisiones, ollama/llama31-8b-64k).** La regla de privacidad (POLICY-001/002: datos sensibles → local) se está usando activamente desde hoy. Antes no aparecía en el ledger.
3. **Anomalía temporal: 145 decisiones hoy vs ~30/día los días previos (~5x).** El DE corre cada 30 min (~48/día máx). 145 > 48 → algo más escribe en el ledger hoy (posible: reintentos, hook de privacidad, ejecuciones manuales de apply-decision, o el watchdog). A INVESTIGAR (candidato a Baseline/anomalía real).
4. **Limitación descubierta del ledger: NO registra éxito/fallo.** El diseño asumía times_success/times_failed; el ledger real solo tiene timestamp/provider/model/reason/nivel/temperature/max_tokens. F2 lo documenta y NO lo inventa. Si F3 quiere "reglas que concentran fallos", primero hay que enriquecer el ledger.
5. **Todas las reglas declaradas en policies/ aparecen en el ledger** (o policies/ sin reglas con nombre parseable) — no hay reglas muertas detectadas.

## Siguiente paso (según decisión 04-ago)

- Esperar 1 semana de datos con el Observer/Evidence en ejecución (cron diario opcional) para construir el Baseline (media semanal + desviación).
- NO tocar F3 (Proposer) ni umbrales hasta entonces.
- Pendiente menor: investigar el pico del 04-ago (145) y decidir si el ledger debe registrar resultado (éxito/fallo) para que F2 pueda medir calidad, no solo frecuencia.
