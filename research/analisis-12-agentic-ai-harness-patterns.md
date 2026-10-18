---
title: "Análisis — 12 Agentic AI Harness Patterns (mentalhotfix, reel 24s)"
type: research
---

# Análisis — 12 Agentic AI Harness Patterns (mentalhotfix, reel 24s)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 13-ago-2026 (12:00 CEST)
**Fuente:** https://www.instagram.com/p/Db8qga7p8hz/ — mentalhotfix (Prateek Singh)
**Tipo:** Reel 24s — **1er análisis con el pipeline completo del lab**
(audio whisper small + frames inteligentes + GLM, 3-ago-2026)
**Método:** analizar_reel_completo.sh → 12 frames + transcripción (580 chars)

---

## Contenido (del AUDIO — la voz lo dice completo)

> "Here are 12 agentic AI harness patterns you should know if you are building
> AI agents. This blog breaks down the patterns inspired by **Claude Code
> Leak** for building AI agents more reliable in production. You will learn:
> **tiered memory, context compaction, explore-plan-act, selected subagents,
> parallel execution, progressive tool access, risk classification and
> lifecycle hooks**."

### Los 12 patrones (audio + frames)
1. **Persistent Instruction File Pattern** — archivo de instrucciones
   persistente (reglas a nivel de proyecto para estandarizar sesiones; sin él,
   cada agente repite convenciones y comete errores)
2. **Tiered memory** — memoria por niveles
3. **Context compaction** — compactación de contexto
4. **Explore-Plan-Act Loop** — bucle explora-planifica-actúa
5. **Selected subagents** — subagentes seleccionados (ISO)
6. **Parallel execution** — ejecución paralela
7. **Progressive tool access** — acceso progresivo a herramientas
8. **Risk classification** — clasificación de riesgo
9. **Lifecycle hooks** — ganchos de ciclo de vida
10-12. (resto de la lista — el reel corta)

Categorías del carrusel: **Memory & Context**, **Workflow & Orchestration**,
**Tools & Permissions**.

---

## 🎯 Veredicto — RELEVANTE (valida el lab + 2 gaps reales)

| Patrón | Lab | Estado |
|---|---|---|
| Persistent Instruction File | AGENTS.md / GUIA-JOKO-LAB / lab.md | ✅ **SÍ — ya lo hace** (por eso el lab tiene reglas persistentes) |
| Context compaction | Compaction de sesiones Hermes (skill skill-compaction) | ✅ Sí |
| Tiered memory | Memoria de Hermes (memory/user/skills/session) | ✅ Sí |
| Explore-Plan-Act | Plan (skill plan) + OBS→HYP→EXP→DEC | ✅ Sí |
| Selected subagents | `delegate_task` (leaf/orchestrator) | ✅ Sí |
| Parallel execution | delegate_task batch (3 concurrentes) | ✅ Sí |
| **Progressive tool access** | ❌ **GAP** — el lab da TODAS las tools siempre | ⚠️ Futurible |
| **Risk classification** | ❌ **GAP parcial** — confirmación explícita manual, no clasificación automática | ⚠️ Futurible |
| Lifecycle hooks | Crons + watchdogs | ✅ Parcial |

### 🟡 Los 2 gaps honestos
1. **Progressive tool access**: los patrones sugieren dar herramientas GRADUALMENTE
   (empezar con pocas, ampliar según necesidad) — el lab expone todo el toolset
   siempre (los crons ya restringen toolsets, pero la sesión principal no)
2. **Risk classification**: clasificar tareas por riesgo automáticamente (el lab
   pide confirmación manual en acciones peligrosas — el patrón sugiere
   clasificarlas en runtime)

**Nota:** el patrón viene de la CLAUDE CODE LEAK (el código interno filtrado de
Claude Code) — es una fuente de diseño de agentes de producción real.

---

## Conclusión

**VALIDA la arquitectura del lab** (7 de 9 patrones visibles ya implementados)
y revela **2 gaps accionables**: acceso progresivo a herramientas y
clasificación de riesgo en runtime. Ambos son futuribles — no urgentes, pero
interesantes para la madurez del lab. El audio fue CLAVE: los frames solo
mostraban categorías, la voz dio la lista completa de patrones.
