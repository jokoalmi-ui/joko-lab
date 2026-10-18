---
type: EXP
subtype: experiment
status: active
tags: [knowledge, experiment]
created: 2026-07-29
---
# Validacion 10 problemas

EXPERIMENTO DE VALIDACION: 10 PROBLEMAS REALES
=================================================
Objetivo: Medir si el pipeline del laboratorio mejora las respuestas
          comparado con ejecutar solo el LLM sin contexto.
Metricas: 6 binarias por problema (Si/No)
Fecha prevista: 30 julio 2026

═══════════════════════════════════════════
METRICAS (una por problema)
═══════════════════════════════════════════

M1. ¿Uso Context Builder?           (debio consultar RAG)
M2. ¿Uso Knowledge Resolver?        (debio sintetizar fuentes)
M3. ¿Recupero conocimiento relevante? (la info era pertinente)
M4. ¿La recomendacion coincidio con decisiones del lab? (DEC-00X)
M5. ¿La respuesta mejoro frente a ejecutar solo el LLM? (mas precisa/util)
M6. ¿Se genero conocimiento nuevo reutilizable? (OBS/HYP/EXP/DEC nuevo)

═══════════════════════════════════════
LOS 10 PROBLEMAS
═══════════════════════════════════════

PROBLEMA 1 — Seleccion de modelo (decision)
────────────────────────────────────────────
Prompt: "Necesito generar un prompt creativo para un relato
         literario. Que modelo uso y con que parametros?"

Tipo esperado: decision
Pipeline esperado: Context Builder → Knowledge Resolver → Decision Router
Conocimiento relevante: DEC-003 (Gemma 4 creatividad), ficha Gemma 4,
                        anti-patron "max_tokens < 400 con Gemma 4"
Metodo: Comparar respuesta sin pipeline (LLM solo) vs con pipeline

PROBLEMA 2 — Busqueda de conocimiento (busqueda)
────────────────────────────────────────────
Prompt: "Por que se descarto Qwen 3.5? Busca la decision y el
         experimento que lo respalda."

Tipo esperado: busqueda
Pipeline esperado: Context Builder → Knowledge Resolver
Conocimiento relevante: DEC-001, EXP-20260726-001 (tests 11-15),
                        ficha Qwen 3.5, anti-patron FATAL
Metodo: Verificar si encuentra DEC-001 y EXP-20260726-001

PROBLEMA 3 — Mejora de prompt (optimizacion)
────────────────────────────────────────────
Prompt: "Dime algo sobre IA"

Tipo esperado: prompt
Pipeline esperado: Context Builder → Decision Router →
                   Evaluator-Optimizer (con GATE)
Conocimiento relevante: Ninguno (el prompt es demasiado generico)
Metodo: Ejecutar E-O, ver si el GATE rechaza la mejora como cosmetica
        o si realmente produce una respuesta mejor

PROBLEMA 4 — Anti-patron (validacion de reglas)
────────────────────────────────────────────
Prompt: "Usando GLM 4.6V, haz lo siguiente: 1) analiza esta imagen,
         2) dime que colores predominan, 3) evalua la composicion,
         4) sugiere mejoras, 5) compara con la regla de los tercios"

Tipo esperado: analisis
Pipeline esperado: Context Builder → Knowledge Resolver
Conocimiento relevante: Anti-patron FATAL "multi-instruccion a GLM",
                        patron "atomic-prompt-glm"
Metodo: Verificar si el pipeline DETECTA que este prompt viola un
        anti-patron FATAL antes de ejecutarlo

PROBLEMA 5 — Benchmark (analisis comparativo)
────────────────────────────────────────────
Prompt: "Compara Granite 4.1 con DeepSeek R1 para generacion de
         codigo Python. Dame datos concretos de los experimentos."

Tipo esperado: analisis
Pipeline esperado: Context Builder → Knowledge Resolver
Conocimiento relevante: EXP-20260726-001, EXP-20260728-002,
                        fichas de ambos modelos, velocidades
Metodo: Verificar si la respuesta incluye datos reales de los
        experimentos (tiempos, tokens, puntuaciones)

PROBLEMA 6 — Prompt para modelo cloud (compilador)
────────────────────────────────────────────
Prompt: "Genera un prompt optimizado para Gemini 2.5 Pro que pida
         disenar una arquitectura RAG con BGE-M3 + LanceDB + Obsidian"

Tipo esperado: prompt
Pipeline esperado: Context Builder → Knowledge Resolver →
                   Decision Router → Evaluator-Optimizer
Conocimiento relevante: skill prompt-engineering (perfiles cloud),
                        prompt-gemini.md (Prompt Project existente)
Metodo: Verificar si el pipeline consulta el perfil de Gemini
        (directo, tecnico, tablas) y genera un prompt adaptado

PROBLEMA 7 — Consulta inter-sesion (memoria transversal)
────────────────────────────────────────────
Prompt: "Que decidimos sobre el umbral de confianza para E3 en la
         auditoria de Claude? Busca en las sesiones de julio."

Tipo esperado: busqueda
Pipeline esperado: Context Builder (busca en 209 sesiones)
Conocimiento relevante: Sesion del 28 julio, anti-patterns/catalogo.md
                        (umbral E3: 3+ condiciones distintas)
Metodo: Verificar si el RAG encuentra la sesion correcta entre las
        209 sesiones indexadas

PROBLEMA 8 — Tarea sin conocimiento previo (fallback)
────────────────────────────────────────────
Prompt: "Cual es la capital de Mongolia?"

Tipo esperado: respuesta (conocimiento general)
Pipeline esperado: Context Builder (sin resultados) → LLM directo
Conocimiento relevante: Ninguno (no esta en el laboratorio)
Metodo: Verificar que el pipeline NO inventa contexto inexistente.
        La confianza deberia ser BAJA (sin fuentes del lab)

PROBLEMA 9 — Nueva decision (generacion de conocimiento)
────────────────────────────────────────────
Prompt: "He probado Qwen 3.5 con temperature=0.2 y max_tokens=4096
         y sigue dando content vacio. Deberiamos actualizar DEC-001?"

Tipo esperado: decision
Pipeline esperado: Context Builder → Knowledge Resolver →
                   Decision Router → Evidence Collector
Conocimiento relevante: DEC-001, OBS-001 (nueva), anti-patron FATAL
Metodo: Verificar si el Evidence Collector sugiere crear OBS o HYP
        (no DEC directamente) y si el Decision Router sugiere NO usar Qwen 3.5

PROBLEMA 10 — Pipeline completo (estres)
────────────────────────────────────────────
Prompt: "Quiero crear un benchmark para evaluar modelos locales
         en generacion de workflows n8n. Antes de disenar nada,
         busca experimentos similares, decisiones relacionadas,
         patrones y anti-patrones. Luego propon el benchmark."

Tipo esperado: analisis + diseno
Pipeline esperado: Task Understanding → Planning →
                   Context Builder → Knowledge Resolver →
                   Decision Router → Evidence Collector
Conocimiento relevante: EXP-20260726-001 (plantilla benchmark),
                        anti-patrones, fichas de modelo,
                        Test 1 de EXP-20260729-004
Metodo: Este es el test mas completo. Debe ejecutar practicamente
        todo el pipeline. Verificar que el plan generado por
        Planning Engine coincide con los pasos ejecutados.

═══════════════════════════════════════════
HOJA DE RESULTADOS (para rellenar)
═══════════════════════════════════════════

| # | Tipo | M1 | M2 | M3 | M4 | M5 | M6 | Total |
|---|---|---|---|---|---|---|---|---|
| 1 | Decision |   |   |   |   |   |   | /6 |
| 2 | Busqueda |   |   |   |   |   |   | /6 |
| 3 | Prompt |   |   |   |   |   |   | /6 |
| 4 | Anti-patron |   |   |   |   |   |   | /6 |
| 5 | Analisis |   |   |   |   |   |   | /6 |
| 6 | Compilador |   |   |   |   |   |   | /6 |
| 7 | Inter-sesion |   |   |   |   |   |   | /6 |
| 8 | Fallback |   |   |   |   |   |   | /6 |
| 9 | Nueva decision |   |   |   |   |   |   | /6 |
| 10 | Pipeline completo |   |   |   |   |   |   | /6 |
| **TOTAL** | | | | | | | | **/60** |

═══════════════════════════════════════════
INTERPRETACION
═══════════════════════════════════════════

  >= 50/60 → El pipeline funciona. El laboratorio mejora sistematicamente.
  30-49/60 → Funciona parcialmente. Algunos componentes necesitan ajuste.
  < 30/60  → El pipeline no anade valor significativo. Redisenar.

═══════════════════════════════════════════
