---
title: "EXP-20260804-VIGENCIA-OKF — Índice de vigencia en el retrieval"
type: EXP
---

# EXP-20260804-VIGENCIA-OKF — Índice de vigencia en el retrieval

**Estado:** COMPLETADO (Fase A) — ADOPCIÓN ❌ PENDIENTE
**Fecha:** 2026-08-04
**Relación:** backlog P2 (vigencia en retrieval), OKF, KEL aplicado al retrieval.

## Hipótesis

> H1: La inyección del índice de vigencia (OKF) mejora la selección del
> conocimiento vigente respecto al retrieval anterior (sin índice).

## Método (Fase A — validación del retrieval)

- Misma pregunta, mismo modelo, mismo prompt; ÚNICA variable: con/sin índice.
- Modelo: glm-4.6v-flash (ya cargado; la hipótesis es del retrieval, no del modelo).
- Pipeline: run_eval --use-lab (context_builder real), banco EXP1/EXP3/EXP4.
- EXP4-001 (caso conflictivo): "¿Debe utilizarse Qwen 3.5 para tareas de
  razonamiento?" — regla antigua vs DEC que la bloquea, ambos indexados.

## Resultados

| Corrida | EXP1 | EXP3 | EXP4 | Precisión |
|---|---|---|---|---|
| CON índice (banco original) | OK | OK | OK | 3/3 |
| SIN índice (banco original) | OK | FALLO* | OK | 2/3 |
| SIN índice (keyword "DeepSeek") | OK | OK | OK | 3/3 |

*EXP3 sin índice respondió "deepseek-r1-distill-qwen-14b; max_tokens 2048"
(contenido CORRECTO) pero el banco exigía la frase literal "DeepSeek R1".
Con índice respondió "DeepSeek R1" (nombre canónico del KO) → pasó sin ajustar.

## Interpretación (honesta)

1. El índice NO degrada (3/3 con y sin).
2. El índice aporta robustez: el modelo usa el nombre canónico del KO
   ("DeepSeek R1") en vez del id técnico del RAG. Evita fallos de formato.
3. H1 NO es falsable HOY con aciertos: no existe ningún `superseded_by`
   real en los 17 KOs → no hay conflicto de vigencia verdadero que discrimine.
   Mismo patrón que EXP-MEL-001: el sistema es joven (edad ≤9 días).
4. EXP4 (conflicto simulable Qwen 3.5) se resuelve bien en AMBAS corridas:
   DEC-001/RULE-004 ya estaban bien indexados. El índice no es imprescindible
   para este conflicto concreto.

## Coste

- Índice: ~800 tokens por consulta que active types (modelo/decision/exp/patron).
- Trade-off: robustez + vigencia futura vs +800 tokens fijos.
- El coste real se medirá con usage (run_eval no captura usage: pendiente).

## Estado y puertas

- Implementado: tools/generar_indice_okf.py + bloque [Índice de conocimiento
  (vigencia)] en context_builder.py (backups: .bak-vigencia-20260804).
- ADOPCIÓN ❌ NO abierta (regla: evidencia primero).
- Puerta de adopción: (a) cuando existan superseded reales (KEL operativo),
  re-medir EXP1/EXP3/EXP4 — el índice debería ganar; o (b) decisión de
  robustez (aceptar ~800 tokens por nombre canónico estable y vigencia).
- Fase B (generalización): repetir el mismo banco con granite-4.1-8b cuando
  se cargue. Si ambos modelos muestran la misma mejora, la confianza sube.

## Nota

Primera ejecución práctica del KEL sobre el retrieval: expires/superseded_by/
status dejan de ser metadato pasivo y pasan a influir en el razonamiento.
El cambio es pequeño en código y grande conceptualmente.
