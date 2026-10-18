---
title: "Análisis — \"9 Pillars of Production AI\" (codewithbrij, IG + ad X)"
type: research
---

# Análisis — "9 Pillars of Production AI" (codewithbrij, IG + ad X)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 14-ago-2026
**Fuente:** https://www.instagram.com/p/DcBPtJ5G8G8/ (codewithbrij, verificado,
2h) + captura del usuario del mismo contenido publicado como PUBLICIDAD en X
(lidr_ai, 18:15).
**Autor:** Brij Kishore Pandey (codewithbrij) — cuenta verificada, India.
**Tesis:** "Your AI vocabulary from 2024 won't survive 2026. RAG and prompt
engineering? Table stakes now. The real production playbook has 9 new pillars."

---

## 1. Los 9 pilares (texto real del post)

| # | Pilar | Claim |
|---|---|---|
| 1 | **Loop Engineering** | "design the cycle, not the prompt. The verifier is the bottleneck." |
| 2 | **Graph Engineering** | "parallel agent networks. DAGs, not chains." |
| 3 | **Spec-Driven Dev** | "specs as executable contracts. Agents implement." |
| 4 | **Context Engineering** | "architect everything the model sees. Systems, not word-smithing." |
| 5 | **Memory Engineering** | "persist, compress, forget. Memory is architecture now." |
| 6 | **MCP** | "the USB-C of AI. Build once, plug anywhere." |
| 7 | **Eval-Driven Dev** | "no evals, no ship. Evals live in CI/CD." |
| 8 | **Agent Awareness** | "agents that know their limits and when to escalate." |
| 9 | **Agent Identity & Security** | "least privilege, audit trails, injection defense." |

**Cierre:** "models are commoditizing. The system is the differentiator."

## 2. Mapeo con el LAB (qué ya tiene cada pilar)

| Pilar | Estado en el lab | Evidencia |
|---|---|---|
| Loop Engineering | ✅ Implementado | SVP (State Verification Pattern) + gates de verificación + OBS→HYP→EXP→DEC; el "verifier is the bottleneck" = la obsesión del lab por verificar con salida real |
| Graph Engineering | 🟡 Parcial | Delegación de subagentes (max 3 concurrentes); NO hay DAGs tipados (typed edges, depends_on) — pipelines secuenciales/paralelos simples |
| Spec-Driven Dev | ✅ Implementado | refactor-seguro (tests + complejidad + comportamiento preservado), diseño de experimentos con C1/C2/C3 implementados con tests |
| Context Engineering | ✅✅ PIONERO | context pruning, token budgeting (400/300/600), skills compactadas (lm-studio 86K→12K), cross-session-awareness, file bus |
| Memory Engineering | ✅ Implementado | memoria persistente + skill compaction + session_search + backups (joko-lab.BACKUP.*) |
| MCP | ✅ Implementado | ~/.lmstudio/mcp.json + skills con MCP (filesystem, etc.) |
| Eval-Driven Dev | ✅ Implementado | suite 205 OK + complejidad CRAP + verificación de código (/tmp/hermes-verify) + KCR (el evaluador se evalúa) |
| Agent Awareness | 🟡 Parcial | Subagentes con límites (max_spawn_depth, leaf/orchestrator) y conocimiento de límites; escalado a usuario manual |
| Agent Identity & Security | 🟡 Parcial | Ledgers (operations_ledger, activación, RAG), SVP anti-fabricación, regla "no inventar datos"; sin auditoría formal de identidad de agentes |

## 3. Veredicto

**VALIDA FUERTEMENTE la arquitectura del lab — 5/9 pilares ya implementados,
2/9 parciales, 0 ausentes.** El lab NO es "2024 vocabulary": ya vive en el
paradigma "the system is the differentiator" — Context Engineering y Memory
Engineering (los 2 pilares más avanzados según el post) son exactamente la
obsesión de las últimas semanas (reducir contexto = coste, compactar skills).

**Post de marketing?** Sí — es contenido de autoridad para vender cursos/notas
(codewithbrij vende formación), y circula como PUBLICIDAD en X. Pero el mapa
conceptual es correcto y sirve como validación externa.

## 4. Aprovechable para el lab (acciones)

1. **Graph Engineering (futurible real):** el único pilar donde el lab está
   parcial. Los "typed edges" (DEPENDS_ON, SUPERSEDES) ya existen como concepto
   en el lab (KO superadas/superseded) — un pipeline DAG explícito para tareas
   paralelas del lab (análisis múltiples) sería la evolución natural. NO
   implementar ahora (sin backlog urgente); queda como plantilla.
2. **Agent Awareness (refuerzo barato):** formalizar el "cuándo escalar al
   usuario" — el lab ya lo hace (confirmaciones explícitas antes de acciones
   destructivas) — documentarlo como patrón explícito en una skill.
3. **Agent Identity & Security (futurible):** "audit trails" — el lab ya tiene
   ledgers; ampliar con identidad de agente (qué sesión/subagente escribió)
   encaja con la brecha de OPs detectada (los refactors de Telegram ahora
   tienen OP). Sin urgencia.
4. **Validación para LinkedIn Lab/TFM:** los 9 pilares son un marco excelente
   para contenido educativo (carrusel "cómo el lab implementa los 9 pilares")
   — dato real del lab como diferencial.
