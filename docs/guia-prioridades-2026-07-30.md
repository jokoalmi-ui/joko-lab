---
type: docs
subtype: docs
status: active
tags: [docs]
created: 2026-07-29
---
# Guia prioridades 2026 07 30

GUIA DE IMPLEMENTACION — JOKO LAB (30 julio 2026+)
=======================================================
Basado en: autoevaluacion del laboratorio + auditoria E-O + 5 tests + plan prioridades
Estado actual del lab: pipeline de 6 etapas (Context Builder → Knowledge Resolver →
  Decision Router → Evidence Collector → Evaluator-Optimizer v2 → Respuesta)

═══════════════════════════════════════════════
🔴 ROJO — Bloquea el resto (hacer YA)
═══════════════════════════════════════════════

R1. Evaluacion contra modelo destino (1h)
    Que: Ejecutar el prompt original y el mejorado contra el modelo
         destino y comparar respuestas reales.
    Por que: Sin esto, el E-O mide sintaxis, no eficacia. Decir que
             un prompt mejoro de 16% a 83% es mentira si la respuesta
             del modelo no cambio.
    Como: La funcion evaluate_response() ya existe en evaluator_optimizer.py.
          Solo falta probarla en un ciclo real y validar que funciona.
    Archivos: evaluator_optimizer.py

R2. Eliminar las dos fuentes de verdad (30 min)
    Que: decision_router.py tiene una tabla hardcodeada + consulta RAG.
         Unificar en una sola: leer decisiones desde RAG siempre.
    Por que: Dos fuentes divergen. Si creamos DEC-004 manana, la tabla
             hardcodeada no la detecta. Deuda tecnica que crece.
    Como: Sustituir ROUTING_TABLE por consulta via _integrate_lab_knowledge()
          o _run_context_builder() en cada llamada.
    Archivos: decision_router.py

R3. OBS → HYP → EXP → DEC (30 min)
    Que: Formalizar el flujo metodologico. No saltar de observacion a
         decision. Introducir niveles intermedios.
    Por que: Las 6 debilidades de la autoevaluacion no son DEC-00X.
             Son OBS-00X hasta que se validen.
    Como: Crear carpetas 01-knowledge/observations/ y 01-knowledge/hypotheses/
          con plantillas minimas (ID, fecha, descripcion, evidencia, estado).
    Archivos: 01-knowledge/observations/, 01-knowledge/hypotheses/

═══════════════════════════════════════════════
🟡 AMARILLO — Importante (cuando R1-R3 esten)
═══════════════════════════════════════════════

A1. Orchestrator + Workers (Implementacion) (2-3h)
    Que: Implementar Fase 1 (Task Understanding) y Fase 2 (Planning)
         del diseno en orchestrator-design.md.
    Por que: El pipeline hoy es lineal. Un orchestrator con Blackboard
             permitiria workers independientes y paralelos.
    Como: Seguir el diseno ya documentado en 05-inference/router/.
    Archivos: task_understanding.py, planning_engine.py, orchestrator.py

A2. Confidence Engine (diseno + prototipo) (1-2h)
    Que: Cada componente devuelve resultado + confianza + evidencia + supuestos.
    Por que: El siguiente componente debe saber cuanto fiarse del anterior.
             Sin esto, un error en Context Builder se propaga silenciosamente.
    Como: Anyadir campo "confidence" a la salida de context_builder,
          knowledge_resolver y decision_router.
    Archivos: context_builder.py, knowledge_resolver.py, decision_router.py

A3. 10 problemas de validacion (Experimento) (1h)
    Que: Ejecutar 10 tareas reales contra el laboratorio y medir 6 metricas.
    Por que: Necesitamos una linea base objetiva. Sin esto, cada mejora
             se evalua subjetivamente ("creo que va mejor").
    Como: Definir 10 prompts, ejecutar con y sin el pipeline, comparar.
    Metricas: Uso Context Builder? Uso Knowledge Resolver? Conocimiento
              relevante? Coincide con decisiones? Mejora vs LLM solo?
              Genero conocimiento nuevo?

A4. Unificar metricas historicas (1h)
    Que: Todas las herramientas guardan resultados en formatos distintos.
         Crear un repositorio unificado en 04-operations/metrics/.
    Por que: Hoy no se puede responder "ha mejorado el lab esta semana?"
             sin mirar 7 archivos distintos.
    Como: Crear metrics_store.py con append_jsonl() y query_last_week().
    Archivos: 04-operations/metrics/store.jsonl

═══════════════════════════════════════════════
🟢 VERDE — Conveniente (mejora calidad de vida)
═══════════════════════════════════════════════

V1. Capitalizacion automatica (diseno) (1h)
    Que: Disenar el mecanismo para que decisiones y patrones se apliquen
         automaticamente sin intervencion manual.
    Por que: Es el gap mas grande del laboratorio (1→3 en la autoevaluacion).
    Como: Disenar un auto_apply() en decision_router.py que, si confianza > 90%,
          ejecute la recomendacion sin preguntar. Pero solo despues de que
          Evidence Collector confirme que hay evidencia suficiente.

V2. Caché RAG inteligente (30 min)
    Que: Caché semantica, no por hash exacto. Usar embeddings para detectar
         queries similares y devolver resultados cacheados.
    Por que: Cambiar "razonamiento" por "razonar" invalida el cache actual.
    Como: Anyadir similitud coseno con queries previas cacheadas.

V3. Probar GLM a 8192 tokens (10 min)
    Que: Usar GLM con max_tokens=8192 para extraer texto de imagenes.
    Por que: Hoy use 2048 y se corto la transcripcion.
    Como: Repetir la prueba de la infografia con max_tokens=8192.

V4. Granite 4.1 a temp=0.5 (15 min)
    Que: Tercera condicion para alcanzar E3 en la ficha de Granite.
    Por que: Solo tenemos E2 (0.3 y 0.7). Falta 0.5 para E3.
    Como: Ejecutar T1-T5 con temp=0.5 y comparar.

V5. Integrar nuevo proveedor cloud (2h)
    Que: Implementar el diseno del Test 2 en 05-inference/executors/cloud/.
    Por que: Ya esta disenado, solo falta implementar.

V6. Sustitucion de Gemma 4 (2h 15m)
    Que: Ejecutar el plan de migracion del Test 3 si hay un modelo sustituto.
    Por que: 15 archivos afectados, DEC-003 obsoleta.

═══════════════════════════════════════════════
RESUMEN
═══════════════════════════════════════════════

Total: 16 tareas
  🔴 ROJO (hacer YA):     3 tareas — ~2 horas
  🟡 AMARILLO (pronto):    4 tareas — ~5-7 horas
  🟢 VERDE (cuando toque): 6 tareas — ~5-6 horas

Orden recomendado: R1→R2→R3 (manana temprano) → A1→A2→A3 (manana tarde)
                   → V1→V2→V3→V4→A4→V5→V6 (resto de la semana)

═══════════════════════════════════════════════
