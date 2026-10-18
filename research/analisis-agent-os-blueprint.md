---
title: "Análisis — Post Instagram: AI Agent OS Blueprint (tarnannrakhangi)"
type: research
---

# Análisis — Post Instagram: AI Agent OS Blueprint (tarnannrakhangi)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 05-ago-2026 (revisado y corregido el mismo día)
**Fuente:** https://www.instagram.com/p/... — tarnannrakhangi (post enviado por Telegram)
**Imagen:** ~/.hermes/image_cache/img_0d8eeb725ee3.jpg (GLM 4.6V)

---

## Qué propone el post

"Build your own Agentic Operating System" — One dashboard. Shared memory. Five
layers. No coding required.

| Pilar | Qué dice |
|---|---|
| ONE DASHBOARD | Todos los modelos en una pantalla |
| SHARED MEMORY | "Never explain" — memoria compartida |
| SMART ROUTING | Mejor modelo para cada tarea |
| PARALLEL AGENTS | Trabajadores paralelos en cerebro compartido |
| LOOP ENGINE | Bucle de mejora continua |

Stack de 5 capas: FOUNDATION (dashboard) → MEMORY (observar/compartir/testear)
→ ROUTER (cada tarea al mejor modelo) → AGENTS (paralelos) → LOOP ENGINE.

---

## ✅ REVISIÓN REAL (05-ago, verificada en sistema — NO de memoria)

El lab ya cubre 4 de 5 capas + el Loop Engine en F1-F2. Verificación con
comandos de solo lectura:

### Capa por capa (estado real)

| Capa | Estado | Evidencia |
|---|---|---|
| 1. FOUNDATION (dashboard) | 🟡 3 dashboards separados | :5000 (monitor), :5050 (gabinete), :1234 (LM Studio) — NO unificados |
| 2. MEMORY compartida | ✅ COMPLETO | File bus: ~/.hermes/team-context/ (6 dominios: telegram, cli, lab, perfume, biohacking, founderz) + latencia <5s (daemon team-bus-watch) |
| 3. ROUTER | ✅ COMPLETO | AI Router + Decision Engine (tools/consulta-decision.sh + check-router-sync.sh) |
| 4. AGENTS paralelos | ✅ COMPLETO | Delegación (delegate_task) + 6 skills de agentes autónomos (claude-code, codex, hermes-agent, hermes-expert, opencode) |
| 5. LOOP ENGINE | ✅ F1-F2 OPERATIVOS | observer.py produce telemetría real; F3-F4 pendientes |

### LOOP ENGINE — lo que YA funciona (ejecutado hoy)

- `tools/observer.py` → telemetría diaria (04-operations/metrics/telemetria/)
- Ledgers activos: decision-ledger.jsonl (77 KB, 375 decisiones),
  activation-ledger.jsonl, rag-query-ledger.jsonl
- Informe 05-ago: decisiones=375 (horario 85.1%, gpu 11.7%, privacidad 2.9%),
  fallback rate 0.3%, activaciones=13, RAG=15
- `tools/evidence_contract.py` existe (contrato de evidencia)

### GAPS REALES (lo que falta)

1. **F3 Proposer** — propuestas automáticas de ajuste de reglas (NO existe)
2. **F4 Gate activo** — evidence_contract.py existe pero sin puerta de
   aprobación en producción (a medias)
3. **Notificación Telegram** de propuestas del L2 (NO existe)
4. **Dashboard unificado** — 3 pantallas separadas (:5000, :5050, :1234)

### DATO CLAVE de la telemetría (05-ago)

- **9 de 9 RULEs NUNCA activadas** (RULE-001..009)
- **12 KOs nunca recuperados** por RAG (DEC-001, DEC-003, PATTERN-001,
  POLICY-001..003, PRED-001/002, RULE-002/005/007...)

Esto es exactamente el input que el L2 debe procesar: reglas documentadas que
no se activan = candidatas a revisión (no a eliminación a ciegas — principio
de no corregir sin evidencia).

---

## Conclusión

El blueprint del post NO añade nada nuevo conceptualmente — el lab lo supera en
4/5 capas y el Loop Engine en F1-F2. El valor del post fue forzar la revisión
real del estado (que reveló los gaps F3-F4 y el dato de las RULEs inactivas).

Próximos pasos anotados (backlog):
- F3 Proposer + F4 Gate activo + aviso Telegram (completar el L2)
- Evaluar RULEs nunca activadas (solo observación, no eliminar a ciegas)
- Unificar dashboards (opcional, baja prioridad)
