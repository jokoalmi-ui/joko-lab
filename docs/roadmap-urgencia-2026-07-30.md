---
type: docs
subtype: docs
status: active
tags: [docs]
created: 2026-07-30
---
# ROADMAP DE URGENCIA — Joko Lab (2026-07-30)

**Fuentes consolidadas:**
- Guía de prioridades (16 tareas, 2026-07-30)
- Engineering Hardening (4 niveles, 2026-07-29)
- Phase 3 Knowledge Activation (5 sprints, 2026-07-30)
- Input de Luis (Phase 3)

**Principio rector:** no construir sobre cimientos rotos. Primero consolidar lo que existe, luego añadir capacidad nueva.

---

## 🔴 FASE 1 — Apagar fuegos (hoy, ~4h)

Lo que bloquea todo lo demás. Sin esto, cualquier mejora nueva hereda la deuda.

| # | Tarea | Origen | Tiempo | Acción concreta |
|---|-------|--------|:------:|-----------------|
| 1.1 | **Unificar fuente de verdad** | Prio R2 + Hardening N2 | 30 min | Eliminar `ROUTING_TABLE` hardcodeada de decision_router.py. Todo contra RAG. |
| 1.2 | **Formalizar OBS→HYP→EXP→DEC** | Prio R3 | 30 min | Crear `01-knowledge/hypotheses/` con plantilla. Mover observaciones sueltas a OBS-003, OBS-004. |
| 1.3 | **Evaluator contra modelo destino** | Prio R1 + Hardening N1 | 1h | Ejecutar `evaluate_response()` contra el modelo real, no contra rúbrica. Validar que 83% no es cosmético. |
| 1.4 | **Sacar reglas a YAML** | Hardening N2 | 1h | `TASK_KEYWORDS` en task_understanding.py → YAML externo. `ROUTING_CACHE` → alimentado desde RAG. |
| 1.5 | **Prompt Project automático** | Hardening N1 | 1h | Activar Prompt Project al detectar "genera prompt para [modelo]", sin que Hermes lo recuerde. |

**Verificación:** `python3 tools/debt_detector.py --check-dual-sources` debe devolver 0.

---

## 🟠 FASE 2 — Consolidar lo que hay (mañana, ~3h)

Una vez que los cimientos están limpios, eliminar redundancias y unificar.

| # | Tarea | Origen | Tiempo | Acción concreta |
|---|-------|--------|:------:|-----------------|
| 2.1 | **Unificar confidence badge** | Hardening N3 | 30 min | Dos cálculos de confianza distintos → unificar en `confidence.py` con entrada única. |
| 2.2 | **Unificar métricas** | Prio A4 | 1h | 7 archivos de métricas → `04-operations/metrics/store.jsonl`. Una query semanal. |
| 2.3 | **Confidence como campo estándar** | Prio A2 | 1h | Añadir `confidence` a la salida de context_builder, knowledge_resolver y decision_router. |
| 2.4 | **10 problemas de validación** | Prio A3 | 30 min | Ejecutar 10 tareas reales, medir 6 métricas. Línea base objetiva. |

**Verificación:** `python3 -c "from tools.metrics_store import query_last_week; print(query_last_week())"` debe devolver datos unificados.

---

## 🟡 FASE 3 — Activar conocimiento (jueves, ~4h)

El salto que describe Luis. El conocimiento deja de ser pasivo.

| # | Tarea | Origen | Tiempo | Acción concreta |
|---|-------|--------|:------:|-----------------|
| 3.1 | **Crear RULE Store** | Phase 3 Sprint 1 | 2h | `01-knowledge/rules/` con RULE-001 a RULE-004 en YAML. Derivadas de DEC existentes. |
| 3.2 | **Crear POLICY Store** | Phase 3 Sprint 1 | 30 min | `01-knowledge/policies/` con POLICY-001 (FATAL) y POLICY-002 (privacidad). |
| 3.3 | **Ampliar KNOWLEDGE_TYPES** | Phase 3 Sprint 1 | 15 min | Añadir RULE y POLICY a decision_engine.py. |
| 3.4 | **Activation Engine v0** | Phase 3 Sprint 2 | 1h | `tools/activation_engine.py` — busca RULE activas y las inyecta en el Decision Engine. |
| 3.5 | **Integrar en pipeline** | Phase 3 Sprint 2 | 15 min | Insertar Activation Engine entre Knowledge Resolver y Decision Engine. |

**Verificación:**

```bash
python3 tools/activation_engine.py --task-type creatividad
# Debe devolver: RULE-001 activa → Gemma 4, origen DEC-003
```

---

## 🟢 FASE 4 — Cerrar el bucle (viernes-lunes, ~3h)

Capitalización automática. El laboratorio reacciona a cambios.

| # | Tarea | Origen | Tiempo | Acción concreta |
|---|-------|--------|:------:|-----------------|
| 4.1 | **Event Bus** | Phase 3 Sprint 3 | 1.5h | `tools/event_bus.py` + watcher sobre decisions/. Nueva DEC → recalcular RULE. |
| 4.2 | **Trazabilidad por componente** | Hardening N4 | 1h | Cada componente responde: ¿qué sabe, de dónde, qué decide, cómo lo demuestra? |
| 4.3 | **Orchestrator Fase 1-2** | Prio A1 | 30 min | Implementar Task Understanding y Planning del orchestrator-design.md. |

---

## 🔵 FASE 5 — Madurar (próxima semana, ~5h)

El sistema se vuelve autovigilante.

| # | Tarea | Origen | Tiempo | Acción concreta |
|---|-------|--------|:------:|-----------------|
| 5.1 | **Confidence Decay** | Phase 3 Sprint 4 | 2h | `tools/confidence_decayer.py`. RULE con >90 días pierden peso automáticamente. |
| 5.2 | **Debt Detector completo** | Phase 3 Sprint 5 | 1.5h | `tools/debt_detector.py` — huérfanos, conflictos, sin validar, versiones obsoletas. |
| 5.3 | **Evidencia de mejora** | — | 30 min | Comparar línea base (2.4) vs post-activación (3.5). Medir delta de capitalización. |
| 5.4 | **Skill prompt-engineering v1.5** | Prio V1 | 1h | Documentar 5 patrones de agente 100% + 12 OBS + pipeline 49/60. |

---

## VISIÓN DE CONJUNTO

```
HOY (F1)         MAÑANA (F2)       JUEVES (F3)       VIERNES (F4)      SEMANA SIG (F5)
──────────       ───────────       ───────────       ───────────       ──────────────
Apagar fuegos    Consolidar        Activar           Cerrar bucle      Madurar
  🔴🔴🔴🔴🔴       🟠🟠🟠             🟡🟡🟡              🟢🟢🟢             🔵🔵🔵🔵
  ~4h              ~3h               ~4h                ~3h               ~5h
                                                                           │
     │               │                  │                   │               │
     └─── CIMIENTOS ──┘                  │                   │               │
                      └─── PLATAFORMA ───┘                   │               │
                                         └─── ACTIVACIÓN ────┘               │
                                                              └─── MADUREZ ──┘
```

---

## FRONTERA CLARA: qué NO hacer en cada fase

| Fase | NO hacer |
|------|----------|
| F1 | No añadir componentes nuevos. Solo arreglar lo roto. |
| F2 | No diseñar RULE todavía. Consolidar primero. |
| F3 | No implementar eventos ni decay. Solo activación. |
| F4 | No añadir más RULE. Validar las 4 que hay. |
| F5 | No volver a F1. Si algo falla, el Debt Detector lo pilla. |

---

## MÉTRICA DE PROGRESO: capitalización

```
F1 → 2/10 (igual, solo saneamos)
F2 → 2/10 (consolidamos métrica, no cambia)
F3 → 5/10 (RULE activas, auto-aplicación en tareas conocidas)
F4 → 7/10 (eventos, el sistema reacciona a cambios)
F5 → 9/10 (decay + debt detector, autovigilancia)
```

---

## Tiempo total

| Fase | Horas | Acumulado |
|------|:-----:|:---------:|
| 🔴 F1 | 4h | 4h |
| 🟠 F2 | 3h | 7h |
| 🟡 F3 | 4h | 11h |
| 🟢 F4 | 3h | 14h |
| 🔵 F5 | 5h | 19h |

**19 horas totales.** ~4 días de trabajo si se dedican 5h/día.
