---
title: "Análisis — \"Git Worktrees: varios agentes de IA en paralelo sin pelearse\" (Fazt Code, 25-ago-2026)"
type: research
---

# Análisis — "Git Worktrees: varios agentes de IA en paralelo sin pelearse" (Fazt Code, 25-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.youtube.com/watch?v=BlZiq68cgIw (Fazt Code, 25-08-2026, 25:03 min, 879 views)
**Método:** subtítulos ES (294 KB, dedup 32.5K chars) — sponsor Hostinger descartado

## El concepto: Git Worktrees

**Worktree** = copia del proyecto gestionada por Git, con su propio branch, commits y working tree independiente. Los agentes de IA escriben en paralelo SIN pisarse los archivos (a diferencia de branches en un solo working tree, donde todos modifican los mismos archivos físicos).

**Comandos clave** (los demuestra manualmente para entender qué hace la IA por debajo):
```bash
git worktree add ../proyecto-api        # crear copia (crea branch asociado)
git worktree list                        # listar
git worktree remove API                  # quitar carpeta (rama queda)
git branch -d API                        # borrar rama
git worktree prune                       # limpiar worktrees huérfanos
git worktree add ../proyecto-ui          # segunda copia → 2 agentes en paralelo
git merge                                # fusionar al final
```

**Regla de orden**: crear worktrees AL MISMO NIVEL del proyecto (`../nombre-proyecto-api`) para que el agente no los interprete como parte del código original.

**Por qué ahora**: antes el paralelismo se hacía por GitHub (cada uno en su máquina); ahora los agentes trabajan en la MISMA máquina → necesitas dividir el proyecto físicamente.

## 🔴 Aplicación al LAB — VALOR MEDIO (con matiz honesto)

| Aspecto | En el lab | Veredicto |
|---|---|---|
| **Paralelismo de agentes** | ✅ `delegate_task` (batch hasta 3) + skills claude-code/codex/opencode | Ya existe, pero los subagentes trabajan en contextos aislados (no comparten archivos) |
| **Worktrees para código real** | ⚠️ Solo aplicaría en proyectos de código donde varios agentes escriban archivos del MISMO repo | El lab no tiene ese patrón hoy (los análisis son investigación, no código multi-agente) |
| **COMPARAR 2 agentes en la misma tarea** | 🟡 **La parte más interesante**: 2 worktrees con la misma feature, cada uno con un agente/modelo distinto, decidir cuál es mejor | Conecta con LLM-as-judge + juicio ciego CLI del lab |
| **AGENTS.md por worktree** | 🟡 Cada worktree puede tener su propio AGENTS.md (reglas distintas por versión) | Patrón aplicable si el lab separa contextos por tarea |
| **Cuándo NO usar** (exploratorio, tarea que abarca todo) | ✅ El lab lo sabe: la mayoría de tareas son exploratorias | La regla de Fazt coincide con el uso real del lab |

## Veredicto: VALOR MEDIO — NO implementar ahora, 1 idea anotable

1. **Los worktrees NO aplican hoy al lab**: la mayoría de tareas son investigativas (exploratorias → Fazt dice NO usar worktrees) o de sistemas (no comparten repo de código multi-agente)
2. **La idea valiosa**: el patrón de **comparar 2 agentes en worktrees paralelos** (misma feature, 2 modelos, elegir el mejor) — pero el lab ya tiene ese patrón con su batería 5x5 + juicio ciego + LLM-as-judge, solo que no con worktrees
3. **El matiz de Fazt "cuándo no" valida el enfoque del lab**: el lab NO fragmenta código exploratorio — correcto
4. **Futurible menor**: si algún día el lab desarrolla un proyecto de código donde 2+ agentes escriban en el mismo repo (p.ej. el SaaS futura), los worktrees serían LA herramienta. Señal: cuando haya un proyecto de código multi-agente real.

**Sin acción inmediata.** El vídeo es buen material conceptual para cuando llegue el proyecto de código grande (SaaS), y refuerza que el lab ya tiene el patrón de comparación de agentes con sus propias herramientas.
