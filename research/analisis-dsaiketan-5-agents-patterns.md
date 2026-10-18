---
title: "Análisis — \"5 AI Agents Patterns\" (ds_ai_ketan, 22-ago-2026)"
type: research
---

# Análisis — "5 AI Agents Patterns" (ds_ai_ketan, 22-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/reel/DcSYH9yy4Db/ (ds_ai_ketan, reel visual 5s)
**Método:** audio transcrito (solo "Follow the moon" — reel visual sin narración) + 5 frames extraídos y analizados con GLM local (visión)

## Contenido: "5 AGENT PATTERNS — Every production AI system in 2026 uses at least one"

| # | Patrón | Descripción | Diagrama |
|---|---|---|---|
| 1 | **Prompt Chaining** | Rompe la tarea grande en pasos, valida entre cada paso. Mejor para flujos descomponibles limpiamente | INPUT → STEP 1 (LLM) → VALIDATE → STEP 2 (LLM) → … → OUTPUT |
| 2 | **Routing** | Un clasificador envía cada consulta al especialista. Mejor para muchos tipos de entrada con puerta frontal clara | USER QUERY → ROUTER → SPECIALIST A/B/C → RESPONSE |
| 3 | **Parallelization** | Múltiples llamadas LLM a la vez, luego merge. Mejor para velocidad, votación o cubrir perspectivas | INPUT → LLM CALL 1..N → MERGE/AGGREGATE → OUTPUT |
| 4 | **Orchestrator-Workers** | Un LLM gestor decide subtareas en tiempo real y delega. Mejor para problemas abiertos con pasos impredecibles | ORCHESTRATOR → WORKER 1,2,3 → RESULTS/ARTIFACTS |
| 5 | **Evaluator-Optimizer** | Un generador redacta, un evaluador critica, bucle hasta que esté bien. Mejor para calidad alta con criterios claros | GENERATOR → EVALUATOR → ¿SÍ? OUTPUT / NO → REFINAMIENTO |

## 🔴 Para el LAB — VALOR: MEDIO-ALTO (validación del diseño existente)

**El lab YA implementa estos patrones de forma natural:**
- **Routing (patrón 2)**: `llm-router.sh` (enruta por coste/hora: cloud antes de 12:00, gpt-oss local después) + ai-router
- **Evaluator-Optimizer (patrón 5)**: `verificar_research.py --juez` (LLM-as-Judge: VERACIDAD gate + CALIDAD juez local GLM/gpt-oss) + revisor en sesión — **es el patrón 5 en producción**
- **Prompt Chaining (patrón 1)**: skills con pasos validados (checklist 17/17 de la ficha, flujos de análisis IG)
- **Orchestrator-Workers (patrón 4)**: Hermes con skills + gate (aunque el lab NO usa delegación local — decisión F4)
- **Parallelization (patrón 3)**: el que menos usa el lab (podría aplicarse a la batería de evaluación de modelos — 5x5 en paralelo sería más rápido)

**Futurible débil**: Parallelization en la batería de evaluación de modelos (evaluar 5 prompts × 5 modelos en paralelo en vez de secuencial) — señal: cuando la batería tarde demasiado.

**Conclusión**: los 5 patrones canónicos de producción están prácticamente todos en el lab (2, 5, 1, 4) — validación externa más del diseño. Nada aplicado al lab (solo documentado).
