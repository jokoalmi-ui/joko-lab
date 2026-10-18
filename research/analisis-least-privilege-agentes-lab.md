---
title: "Análisis — Least Privilege para Agentes IA: implementable en el LAB (16-ago-2026)"
type: research
---

# Análisis — Least Privilege para Agentes IA: implementable en el LAB (16-ago-2026)

**Origen:** short IBM "AI Agents Are Becoming the Attack Surface" (C6aZx47q7Zc)
**Investigación:** fuentes externas (Marchward, Security Boulevard/CISO playbook, Baytech IAM 2026)
**VERACIDAD:** [ALCANCE INTERNO]

## El problema (según la investigación)

1. **El fallo real es over-permissioning, no el modelo** — el trigger puede ser una
   prompt injection, pero la explosión la causa el permiso excesivo (caso real:
   agente borró la producción en 9 segundos; la culpa fue del token con permisos
   de cuenta completa, no del modelo).
2. **Prompt y config NO aguantan** — el system prompt es una sugerencia; un
   documento malicioso que el agente lee puede sobreescribirlo. Solo el
   enforcement en el PUNTO DE EJECUCIÓN vale.
3. **Deny-by-default** — el agente empieza con NADA y se le dan las tools
   específicas de su tarea. Una tool que nunca tuvo no puede alcanzarse ni por
   prompt injection ("no hay nada que alcanzar").
4. **OWASP Top 10 LLM** lo nombra "excessive agency" (excessive functionality +
   excessive permissions).
5. **Credenciales nunca expuestas al agente** — se inyectan server-side solo para
   llamadas permitidas (modelo Marchward; el lab ya usa redact_secrets).

## Qué tiene el LAB ya (verificado en config.yaml / disco)

| Mecanismo | Estado | Equivalente a |
|---|---|---|
| `approvals.mode: smart` (fail-closed) | ✅ Activo | Enforcement en punto de ejecución |
| Hardline blocklist (mkfs, rm -rf /... ni con --yolo) | ✅ Activo (2 bloqueos en vivo hoy) | Deny-by-default para destructivos |
| `approvals.cron_mode: deny` | ✅ Activo | Crons no ejecutan destructivos |
| `security.tirith_enabled: true` | ✅ Activo | Anti prompt-injection |
| `security.redact_secrets: true` | ✅ Activo | Credenciales no expuestas al contexto |
| `delegate_task` con `toolsets` por tarea | ✅ Disponible | Allow-list por subagente |
| `enabled_toolsets` en crons | 🟡 6/30 jobs lo usan | Scoping parcial |

## Gaps implementables (lo que el vídeo destapa en el lab)

### 🟡 GAP 1 — ~~24/30 crons sin toolsets~~ → CORREGIDO: solo 5 jobs con agente y TODOS tienen toolsets ✅

⚠️ **Corrección (16-ago, verificación real)**: el análisis inicial marcó 24/30
crons sin `enabled_toolsets` como gap. Al verificar con datos: **los 24 son
`no_agent=True` (scripts puros que ejecutan stdout verbatim, sin LLM ni tools)**
→ no cargan herramientas del agente → NO necesitan scoping. Los **5 jobs con
agente (no_agent=False) TODOS tienen `enabled_toolsets`** ✅ (scan-empleo,
nvidia-suspend, perfumes, bolsa, vigilar-ig). El gap real queda en: **cron
NUEVO con agente → toolsets obligatorio** (regla R2 de la skill
least-privilege-lab).

**Pitfall aprendido:** "sin enabled_toolsets" NO implica riesgo si el job es
no_agent=True — verificar `no_agent` antes de marcar un gap (lección
"verificar > asumir" aplicada en vivo).

### 🟡 GAP 2 — delegate_task sin toolsets mínimos por defecto
La tool acepta `toolsets` por tarea, pero es fácil delegar sin restringir.
**Acción:** regla operativa — SIEMPRE pasar toolsets mínimos al delegar
(terminal+file para código; web para investigación; nunca todo por defecto).

### 🟡 GAP 3 — `inherit_mcp_toolsets: true`
Los subagentes heredan los toolsets MCP del padre. Hoy el lab no usa MCP
activamente (sin MCP servers críticos), pero es un punto de ampliación si se
añaden. **Acción:** documentar; si se añade MCP en el futuro, evaluar false.

### 🟢 GAP 4 — Falta la POLÍTICA (skill/documento)
No existe una skill que diga "qué toolsets para qué tipo de tarea".
**Acción:** crear skill `least-privilege-lab` (o sección en documentacion-joko-lab)
con la tabla de toolsets por tipo de tarea + regla de delegación.

## Veredicto

**El lab ya tiene la capa crítica** (approvals + hardline + cron deny + redact)
— es de los más avanzados para single-user local. Los gaps 1-4 son de
**política y auditoría**, no de infraestructura: se cierran con una skill
(GAP 4), una auditoría de crons (GAP 1) y una regla de uso (GAP 2) — todo
implementable sin tocar el core de Hermes.

**Orden sugerido:** 4 (política) → 1 (auditoría crons) → 2 (regla delegación) → 3 (MCP, solo si aplica).
