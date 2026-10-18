---
type: docs
subtype: docs
status: active
tags: [docs]
created: 2026-07-29
---
# Pendientes 2026 07 29

PENDIENTES JOKO LAB — 29 julio 2026 (noche)
=============================================

═══════════════════════════════════════════
🔴 CRITICO — Capitalizacion (el 0% duele)
═══════════════════════════════════════════

1. Integrar Decision Engine en el pipeline real
   Que: El motor existe pero no se ejecuta automaticamente en cada
        consulta. Hay que engancharlo al flujo principal.
   Por que: Es la pieza que convierte "saber" en "actuar".
   Tiempo: 30 min
   Archivo: decision_engine.py → entry point del pipeline

2. Auto-disparar el pipeline completo al detectar keywords
   Que: Cuando el usuario escribe "modelo", "prompt", "workflow",
        el sistema debe ejecutar el pipeline sin que Hermes lo pida.
   Por que: Elimina "Hermes recuerda..." para siempre.
   Tiempo: 1h
   Archivo: skill joko-context o wrapper pre-consulta

3. Eliminar las ultimas 3 reglas hardcodeadas
   Que: Mover a YAML: umbral 80% del Evaluator, TTL=1h del cache,
        threshold cos=0.1 del confidence badge.
   Por que: Toda constante debe tener origen documentado.
   Tiempo: 30 min
   Archivos: evaluator_rubric.yaml, context_builder.py, confidence.py

═══════════════════════════════════════════
🟡 ALTO — Calidad de decisiones
═══════════════════════════════════════════

4. Goodhart en Evaluator-Optimizer
   Que: El evaluator mide "parecido a rubrica", no "mejora real".
        Anyadir check semantico de preservacion de significado.
   Por que: Prueba 3 paso de 1/6 a 3/6 pero sigue siendo baja.
   Tiempo: 2h
   Archivos: evaluator_optimizer.py, _check_semantics()

5. Recalcular confidence con pesos
   Que: Evidencia 40% + actualidad 30% + consenso 20% + conflictos 10%.
        No solo "numero de fuentes encontradas".
   Por que: El badge actual sigue siendo debil aunque ya no miente.
   Tiempo: 1h
   Archivo: confidence.py

6. Unificar las dos fuentes del router definitivamente
   Que: El capability_map en decision_router.py es una cache, no fuente.
        Debe regenerarse desde RAG en cada sesion, no persistir.
   Por que: Si creamos DEC-004, el capability_map no la ve.
   Tiempo: 30 min
   Archivo: decision_router.py

7. Prompt Project: auto-activar + auto-guardar
   Que: Cuando se genera un prompt para un modelo cloud, crear
        automaticamente spec.yaml en 05-inference/compiler/projects/
   Por que: Prueba 6 paso de 3/6 a 6/6 con Decision Engine.
        Pero aun no guarda el spec.
   Tiempo: 1h
   Archivos: decision_engine.py, 05-inference/compiler/

═══════════════════════════════════════════
🟢 MEDIO — Robustez y metricas
═══════════════════════════════════════════

8. Banco de regresion con las 11 pruebas
   Que: Convertir las 11 pruebas en tests automatizados que se
        ejecuten tras cada cambio.
   Por que: Saber si una mejora rompe otra parte del lab.
   Tiempo: 1h
   Archivos: 04-operations/tests/regression/

9. Re-indexar observaciones en el RAG
   Que: Las 12 OBS no estan en el indice de busqueda semantica.
   Por que: El autoanalisis no encontro sus propias observaciones.
   Tiempo: 5 min
   Comando: python3 tools/indexer.py —force

10. Knowledge Graph (version inicial)
    Que: Crear un indice de relaciones entre entidades:
         modelo → experimento → decision → patron → anti-patron.
    Por que: Permitir consultas como "dame todo sobre Granite 4.1".
    Tiempo: 2h (diseno) + 1h (implementacion)
    Archivos: 01-knowledge/graph/

═══════════════════════════════════════════
⚪ BAJO — Mejora continua
═══════════════════════════════════════════

11. Sustitucion de Gemma 4 (cuando haya candidato)
    Que: Ejecutar plan de migracion del Test 3 de EXP-20260729-004.
    Tiempo: 2h 15m
    Estado: Bloqueado (sin candidato)

12. Integrar nuevo proveedor cloud
    Que: Implementar diseno del Test 2.
    Tiempo: 2h
    Estado: Bloqueado (sin proveedor concreto)

13. Ejecutar W1-W5 benchmark n8n
    Que: El benchmark esta disenyado pero no ejecutado.
    Tiempo: 1h

14. Granite 4.1 a temp=0.5 (tercera condicion para E3)
    Tiempo: 15 min

15. Qwen 3.5 a temp=0.5 (tercera condicion para E3)
    Tiempo: 15 min

16. GLM a max_tokens=8192 para extraccion de texto
    Tiempo: 10 min

═══════════════════════════════════════════
RESUMEN
═══════════════════════════════════════════

🔴 CRITICO:   3 tareas — 2 horas
🟡 ALTO:      4 tareas — 4.5 horas
🟢 MEDIO:     3 tareas — 3 horas
⚪ BAJO:      6 tareas — 6 horas

TOTAL: 16 tareas — 15.5 horas

Proxima sesion recomendada: 🔴 1→2→3 → 🟡 4→5→6→7
═══════════════════════════════════════════
