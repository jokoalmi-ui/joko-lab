---
title: "Análisis — 8 Skills imprescindibles para AI Agents (David Ondrej, 16-ago-2026)"
type: research
---

# Análisis — 8 Skills imprescindibles para AI Agents (David Ondrej, 16-ago-2026)

**Fuente:** https://youtu.be/clrUbBtD2j4 (David Ondrej, ~13 min, EN)
**Transcripción:** completa (en)
**VERACIDAD:** [VERIFICADO]

## Contexto
David Ondrej (3 años, 2000+ h con agentes) abrió su repo personal de agent skills
(github.com/davidandr/skills, 42 skills). Se hizo viral: medio millón de vistas en
Twitter, avalado por Morgan Linton (cofundador de Hermes Agent), CTO de Boldmetrics
("posiblemente el mejor repo de agent skills"), CTO de OpenSea.

## Las 8 skills (resumen honesto)

### 1. ⭐ GLOBAL AGENT GUARDRAILS (la nº1, la más importante)
- **Problema:** en Yolo mode (autonomía sin aprobar cada comando) hay riesgo real
  (borrados de producción, etc.). El system prompt NO basta para frenar.
- **Solución:** hooks de PRE-tool-call (scripts shell) que **bloquean
  programáticamente** patrones peligrosos ANTES de ejecutarlos: `rm -rf /`,
  borrar home completo, fork bombs, pipe de internet a shell, reescribir git
  history remoto, borrar ramas/tags remotas, romper permisos del sistema,
  destruir reflog, CLI de GitHub peligrosa.
- **Matiz clave:** NO es "ponerlo en el prompt y esperar" — es un hook que corre
  antes de cada tool call. Permite `rm -rf node_modules` (legítimo) pero bloquea
  `rm -rf /`.

### 2. ⭐ GIT WORKTREE (aislar agentes paralelos)
- **Problema:** con >5 agentes en el mismo repo se pelean por los mismos archivos.
- **Solución:** cada agente trabaja en un worktree = copia del repo en otra
  carpeta con su propia rama Git. Aislamiento total, más velocidad.
- Skill corta: detectar ubicación, crear/quitar worktrees, marcar completado,
  copiar .env, automatizar setup.

### 3. VPS SERVER MANAGEMENT
- Aislar agentes en VPSs (un Hermes en cada VPS: tareas, OpenClaw, etc.).
- Un agente gestiona todos los VPS por SSH/Tailscale: recuperar agente caído,
  actualizar modelos.
- ⚠️ **Patrocinado por Hostinger** (código David = -10%) — contenido promocional.

### 4. GOAL LOOP (arquitectura de prompts /goal)
- Un /goal solo funciona con **end condition verificable**: números claros,
  criterio de parada ("hasta encontrar 100 CMOs con 3 formas de contacto").
- La skill convierte instrucciones vagas en goal loops optimizados (contrato de
  5 partes, mythology.md, fuentes públicas).

### 5. ⭐ SETUP HELP (formato "paso actual + pasos restantes")
- Para tareas donde TÚ debes estar involucrado (setup de DB, deploy, formularios).
- **El valor:** el agente da contexto del paso ACTUAL + lista de pasos RESTANTES
  en cada respuesta → no pierde el hilo cuando preguntas más a fondo.
- Aplicable a cualquier setup complejo (impuestos, deploy, DNS...).

### 6. ⭐ DECISIONS (revisar decisiones, no código)
- Inspirado en Victor Talan: tras un cambio GRANDE (docenas de archivos, miles
  de líneas), no revises el código (imposible a escala): pregunta al modelo
  "¿qué decisiones importantes tomaste de las que NO estás seguro?".
- Versión de David: "solo lista decisiones dudosas, no las obvias; sé conciso".
- **Bonus:** NEXT DECISION — presenta las decisiones UNA a una con top-4 opciones
  y su recomendación para que el humano decida con contexto.

### 7. ANTI-SLEEP
- Evita que el PC duerma mientras corren agentes (caffeinate en macOS, script
  shell con verificación). Uso: lanzar tarea larga e ir al gimnasio.

### 8. DEEP API (⚠️ promocional, no accesible aún)
- API key única para scraping + deep research + web search + email para agentes.
- **NO liberada al público** (solo aplicación: deepapi.co). Benchmark propio
  contra Perplexity/ChatGPT. Contenido promocional del producto de David.

## 🎯 APLICACIÓN AL LAB (prioridad: mejorar LAB primero)

| Skill | Aplicable al lab | Acción |
|---|---|---|
| **1. Global guardrails** | ✅ **MUCHO** | El lab tiene reglas de seguridad en system prompt pero NO hooks programáticos. Un hook pre-tool-call bloqueando `rm -rf /`, `sudo`, git history remoto, etc. = capa real de seguridad. **GAP real.** |
| **2. Git worktree** | ✅ **MUCHO** | **Resuelve el problema REAL del lab**: el subagente hermano (CLI) colisiona con la sesión TG en el backlog. Un worktree por sesión/agente = aislamiento. **Acción concreta.** |
| **4. Goal loop** | ✅ Sí | El lab ya tiene end conditions en crons/experimentos; formalizar el patrón /goal con condiciones verificables. |
| **5. Setup help** | ✅ Sí | Formato "paso actual + restantes" = útil para guías de instalación del lab (ya se hace parcialmente). |
| **6. Decisions** | ✅ **SÍ** | **Complemento directo del gate de veracidad para CÓDIGO**: tras un refactor grande, revisar decisiones del agente, no 2000 líneas. Encaja con SVP. |
| 3. VPS | ⚠️ Local-first | No prioritario (el lab es local; VPS contradice privacidad local). Futurible si se necesita mover agentes a la nube. |
| 7. Anti-sleep | 🟡 Menor | El PC es el servidor del lab; útil si se lanzan tareas largas nocturnas (aunque hay cero crons 00:00-07:00 por diseño). |
| 8. Deep API | ❌ No | Promocional, no público, cloud (contradice local-first). Ignorar. |

## Veredicto
Vídeo de **alta relevancia**: valida el sistema de skills del lab (42 skills de
David = el mismo formato skill.md de Hermes) y aporta **2 gaps reales del lab**:
(1) guardrails programáticos (hooks pre-tool-call) y (2) worktrees para aislar
agentes paralelos. La skill "decisions" es un complemento natural del gate de
veracidad para código.

## Futuribles anotados
1. 🟢 **Hooks de guardrails programáticos** (skill 1): hook pre-tool-call que
   bloquee patrones peligrosos (rm -rf /, sudo sin autorización, git history
   remoto) — capa real más allá del system prompt.
2. 🟢 **Git worktrees para sesiones paralelas** (skill 2): resolver la colisión
   subagente-CLI vs sesión TG en el backlog (aislar por worktree).
3. 🟡 **Skill "decisions" del lab**: tras refactors grandes, pedir al agente las
   decisiones dudosas (complementa gate-veracidad + SVP).

## Nota honesta
- 2 de las 8 skills son promocionales (Hostinger VPS + Deep API, su producto).
- El claim de avales es real (Morgan Linton = cofundador de Hermes, sí respondió
  en Twitter) pero es autopromoción legítima de su repo.
- Los guardrails por hook son la idea MÁS transferible al lab.
