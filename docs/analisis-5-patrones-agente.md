---
type: docs
subtype: docs
status: active
tags: [docs]
created: 2026-07-29
---
# Analisis 5 patrones agente

ANALISIS: 5 PATRONES DE AGENTE vs JOKO LAB
=============================================
Fuente: Captura de pantalla (LM Studio / Hermes Agent)
        Infografia "5 Agent Patterns" by Keta Saperi
Fecha analisis: 2026-07-29

═══════════════════════════════════════════
CUADRO COMPARATIVO
═══════════════════════════════════════════

| # | Patron | Descripcion | En Joko Lab | Estado | Implementacion |
|---|--------|------------|-------------|--------|---------------|
| 01 | PROMPT CHAIN | Paso de salida como entrada al siguiente paso | ✅ Pipeline | IMPLEMENTADO | Context Builder → Knowledge Resolver → Decision Router |
| 02 | ROUTING | Redirigir input al modelo/especialista adecuado | ✅ Router | IMPLEMENTADO | decision_router.py + detect_type() |
| 03 | PARALLELIZATION | Dividir tarea en subtareas paralelas | ❌ No existe | PENDIENTE | No hay workers paralelos. Todo es secuencial |
| 04 | ORCHESTRATOR-WORKERS | Orquestador asigna tareas a workers | ⚠️ Disenado | DISENADO | orchestrator-design.md (Fase 1-2 implementadas, Fase 3 pendiente) |
| 05 | EVALUATOR-OPTIMIZER | Evaluar salida y refinar iterativamente | ✅ v2 | IMPLEMENTADO | evaluator_optimizer.py con GATE fail-closed |

═══════════════════════════════════════════
ANALISIS
═══════════════════════════════════════════

1. DE 4 A 5 PATRONES

   El video de BettaTech (analizado hoy temprano) describia 4 patrones.
   Esta infografia anyade un QUINTO: PARALLELIZATION.

   El patron 3 (Parallelization) NO existe en Joko Lab. Todo el
   procesamiento es secuencial: Context Builder → Knowledge Resolver →
   Decision Router → Evaluator-Optimizer.

   La infografia describe Parallelization como: "Break task into
   subtasks and run them parallel. Best for speed and handling
   independent tasks." Esto es exactamente lo que nos falta para
   acelerar el pipeline.

2. LOS QUE YA TENEMOS

   01 PROMPT CHAIN: ✅ Implementado. Nuestro pipeline encadena
      componentes con salidas claras.

   02 ROUTING: ✅ Implementado. decision_router.py detecta tipo de
      tarea y recomienda modelo. Pero la seleccion sigue siendo
      manual (no automatica).

   04 ORCHESTRATOR-WORKERS: ⚠️ Diseno completado en orchestrator-design.md.
      Fase 1 (Task Understanding) y Fase 2 (Planning) implementadas.
      Falta Fase 3 (Execution con Blackboard y workers reales).

   05 EVALUATOR-OPTIMIZER: ✅ Implementado. v2 con GATE fail-closed,
      rubrica YAML, verificacion semantica.

3. EL QUE FALTA

   03 PARALLELIZATION: ❌ NO implementado. Seria util para:
      - Ejecutar Context Builder y Decision Router en paralelo
      - Comparar 2-3 modelos simultaneamente (benchmark)
      - Procesar multiples documentos RAG a la vez

4. LO QUE DICE LA INFOGRAFIA SOBRE COMBINAR PATRONES

   "The single pattern or combine them based on your needs"

   Joko Lab YA combina 3 patrones (Chain + Router + Evaluator).
   Anadir Parallelization permitiria:
   - Acelerar el pipeline (tareas independientes en paralelo)
   - Comparar modelos simultaneamente (benchmark paralelo)
   - Procesar busquedas RAG en paralelo

5. PATRON 03 COMO PROXIMO PASO

   La infografia sugiere que Parallelization es mejor para "speed
   and handling independent tasks". Esto encaja con:
   - Test 4 de validacion (velocidad de respuesta): el pipeline
     tarda ~25s en arrancar por cargar BGE-M3. Con paralelismo,
     podriamos precargar modelos mientras el usuario escribe.
   - Orchestrator Fase 3: los workers deberian ejecutarse en paralelo,
     no secuencialmente.

═══════════════════════════════════════════
FIN
═══════════════════════════════════════════
