---
title: "Medición Agentic RAG Loop — clásico vs agentic (2026-08-07)"
type: operations
---

# Medición Agentic RAG Loop — clásico vs agentic (2026-08-07)

Fecha: 2026-08-07 10:51 (ejecución manual de tools/medir_agentic.py)
Banco: verification/bank.yaml (7 items) | top_k=5 | agentic máx 3 iteraciones

## Resultado

- Cobertura clásica (1 búsqueda): 5/7
- Cobertura agentic (loop): 6/7
- Items que el agentic resuelve y el clásico NO: 1 (EXP4-001)
- Items sin mejora: 6 (V001-V004, EXP3-001)
- Items incompletos en ambos: 1 (EXP1-001, ver hallazgo abajo)
- Tiempo: clásico 122.31s | agentic 139.7s (+14%)
- Única reformulación disparada: EXP4-001 (2 búsquedas, 36.44s)

## Interpretación

El loop aporta EXACTAMENTE en el caso de conflicto/vigencia para el que fue
diseñado: EXP4-001 ("¿Debe utilizarse Qwen 3.5 para tareas de razonamiento?",
espera "no", prohíbe "sí"). El clásico fallaba; con una segunda búsqueda
reformulada el agentic recupera lo correcto y aprueba.

En consultas simples (V001-V004 keywords, EXP3-001 composición) no hay mejora:
el clásico ya las resuelve. Confirma la regla de activación del diseño: el loop
solo tiene sentido para el subconjunto de consultas con señal de conflicto.

## Hallazgo: falso negativo del EVALUATE con prohibidos

EXP1-001 sale "AMBOS incompletos" con faltantes=[] (todas las keywords
esperadas presentes en lo recuperado) pero cobertura_ok=False. Por
construcción de `completitud_parcial` (comparador.py), eso solo ocurre cuando
el texto recuperado contiene la keyword PROHIBIDA. Es decir: cualquier
documento del lab que mencione "Qwen 3.5" (p.ej. un experimento de descarte)
hace fallar la cobertura aunque el LLM respondería correctamente.

Consecuencia: el evaluador de cobertura sobre texto BRUTO de recuperación es
demasiado estricto con `prohibido`. El criterio fue diseñado para evaluar
RESPUESTAS del LLM, no contextos. Para la medición del retrieval, un
`prohibido` presente en el contexto NO implica respuesta incorrecta — puede
ser justo la evidencia que permite responder "no".

No corregido en esta fase (decisión consciente): modificar comparador.py
afectaría a run_eval.py y al banco. Se documenta como limitación conocida del
EVALUATE Fase 1. Si se quiere medir el retrieval con prohibidos, el evaluador
debería comprobar prohibidos SOLO en la síntesis final (respuesta), no en el
contexto.

## Decisión Fase 4 (umbrales con datos)

- Activar el loop (cuando se apruebe la activación) SOLO para consultas con
  señal de conflicto/vigencia: detect_type ampliado (comparativa, contradicción,
  vigencia, "debe usarse", "descartado", presencia de superseded).
- NO activar para consultas simples (keywords/1 fuente): el clásico las
  resuelve sin coste extra (medido: 0 mejora en 6/7).
- Coste aceptable: +14% tiempo en el peor caso del banco, y la reformulación
  solo se dispara cuando hay señal.

## Estado

- Fase 1 ✅ agentic_loop.py (verificada EXP3-001 y banco completo)
- Fase 2 ✅ skill agentic-rag (USO MANUAL)
- Fase 3 ✅ medir_agentic.py EJECUTADA (este informe + history-agentic.jsonl)
- Fase 4 ✅ umbrales decididos con datos (arriba)
- Fase 0 ⏳ activación en producción NO aprobada — decisión del usuario.
  El loop sigue INACTIVO: nada lo invoca automáticamente.
