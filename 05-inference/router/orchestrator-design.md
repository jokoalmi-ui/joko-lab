---
type: inference
subtype: inference
status: active
tags: [inference]
created: 2026-07-29
---
# Orchestrator design

DISENO DEL ORCHESTRATOR + WORKERS
====================================
Basado en: evaluacion externa (Luis, 2026-07-29)
Estado: DISENO — No implementado

═══════════════════════════════════════════════
1. ARQUITECTURA GENERAL
═══════════════════════════════════════════════

No es un patron aislado. Es la pieza que unifica todo
lo construido hasta ahora. El flujo completo es:

  Usuario
     │
     v
  1. TASK UNDERSTANDING (Fase 1 - Comprension)
     No llama a nadie. Solo responde:
     "Que quiere realmente el usuario?"
     Salida: goal, tipo, complejidad, restricciones, artefacto esperado
     │
     v
  2. PLANNING (Fase 2 - Planificacion)
     Disena el plan de ejecucion sin ejecutar nada:
     "Que componentes necesita?"
     Salida: plan.yaml con steps ordenados
     │
     v
  3. EXECUTION (Fase 3 - Workers)
     Cada worker ejecuta UNA tarea. Escribe en el Blackboard.
     Workers funcionales (no por lenguaje/tema):
     - Context Worker
     - Knowledge Worker
     - Prompt Worker
     - Model Worker
     - Validation Worker
     │
     v
  4. EVALUATION (Fase 4 - Evaluacion)
     El Evaluator-Optimizer evalua TODO, no solo prompts:
     - "Cumple el objetivo?"
     - "Uso bien el conocimiento?"
     - "Violo patrones?"
     - "Aprendimos algo?"
     │
     v
  5. LEARNING (Fase 5 - Capitalizacion)
     Decide si actualizar:
     - Experimentos
     - Decision Memory
     - Pattern Library
     - Model Cards
     - Metricas
     Solo si hay evidencia suficiente.
     │
     v
  Respuesta al usuario

═══════════════════════════════════════════════
2. BLACKBOARD
═══════════════════════════════════════════════

Todos los workers escriben en el MISMO sitio.
No se llaman entre ellos.

  Blackboard = {
    goal:          "lo que quiere el usuario"
    context:       "resultado del Context Builder"
    knowledge:     "resultado del Knowledge Resolver"
    constraints:   "anti-patrones + restricciones"
    prompt:        "prompt actual (iterativo)"
    evaluation:    "resultado del Evaluator"
    confidence:    "nivel de confianza"
    decision:      "que hacer a continuacion"
  }

Cada worker modifica SOLO su seccion.
Eso desacopla completamente el sistema.

═══════════════════════════════════════════════
3. PLAN DE EJECUCION
═══════════════════════════════════════════════

El Orchestrator no decide solo. Usa un Plan:

  plan:
    goal: "Crear un prompt para Gemini"
    steps:
      - context_builder
      - knowledge_resolver
      - prompt_generator
      - evaluator
      - optimizer
      - validator
    model: "Gemini"
    learning: true
    register: true

El Orchestrator INTERPRETA el plan.
Los workers nunca conocen el laboratorio.
Solo ejecutan una tarea.

═══════════════════════════════════════════════
4. WORKERS FUNCIONALES (no por lenguaje)
═══════════════════════════════════════════════

  Worker            | Que hace
  ------------------|------------------------------------------
  Context Worker    | Ejecuta context_builder.py
  Knowledge Worker  | Ejecuta knowledge_resolver.py
  Planning Worker   | Disena el plan de ejecucion
  Prompt Worker     | Genera o compila el prompt
  Execution Worker  | Llama al modelo destino
  Validation Worker | Ejecuta preflight_checklist.py
  Learning Worker   | Decide si registrar conocimiento

═══════════════════════════════════════════════
5. RELACION CON LOS PATRONES EXISTENTES
═══════════════════════════════════════════════

  Pipeline/Chaining  → Fase 3 (Execution)
  Router             → Fase 2 (Planning)
  Evaluator-Optimizer → Fase 4 (Evaluation)
  Orchestrator       → Fase 2-3 (Planning + Execution)

═══════════════════════════════════════════════
6. PRINCIPIOS DE DISENO
═══════════════════════════════════════════════

  - Un worker, una responsabilidad
  - Workers no se conocen entre si (solo Blackboard)
  - El Orchestrador no trabaja (solo coordina)
  - El plan es explicito y trazable
  - Cada ejecucion produce aprendizaje o no se cierra
  - Los errores de diseno deben ser detectables
  - Una mejora solo entra al nucleo si resuelve un
    problema recurrente o aporta beneficio medible

═══════════════════════════════════════════════
7. PENDIENTE PARA IMPLEMENTACION
═══════════════════════════════════════════════

  [ ] Disenar el formato del Blackboard (JSON schema)
  [ ] Disenar el formato del Plan (YAML schema)
  [ ] Implementar Task Understanding (detectar objetivo)
  [ ] Implementar Planning (generar plan a partir de objetivo)
  [ ] Implementar Execution (ejecutar workers contra Blackboard)
  [ ] Implementar Learning (decidir que registrar)
  [ ] Integrar con los 4 patrones existentes

═══════════════════════════════════════════════
FIN DEL DOCUMENTO DE DISENO
═══════════════════════════════════════════════
