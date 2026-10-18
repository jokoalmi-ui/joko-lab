---
title: "Ecosistema de Gobernanza de Joko Lab — Mapa de referencia"
type: research
---

# Ecosistema de Gobernanza de Joko Lab — Mapa de referencia
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 06-ago-2026
**Propósito:** mapa único del ecosistema de gobernanza (capas, componentes, estado real, rutas). Complementa GUIA-JOKO-LAB.md: esta es la referencia de gobernanza; la GUIA es la referencia del lab completo.
**Regla de mantenimiento:** actualizar en la MISMA sesión en que cambie cualquier estado (mismo patrón que JL-013 para la GUIA).

---

## 1. Vista general (3 capas + transversal)

```
                    RUNTIME
                        │
        ┌───────────────┴───────────────┐
        │                               │
   Conocimiento                     Procedimiento
        │                               │
   KAP → KVC → KEL                  Gates + SVP
        │                               │
        └───────────────┬───────────────┘
                        │
                     Evidencia
                        │
                       EVF
                        │
                     ─────────
                        MEL (transversal, observa todo)
```

| Capa | Responde | Componentes |
|---|---|---|
| 1. Operativo | ¿Cómo aprende el lab? | KAP, KVC, KEL, MEL, KOs, Decision Ledger, Evidence Contract, RAG, Runtime |
| 2. Gobernanza | ¿Se sigue el procedimiento correcto? | Procedural Gates (001-005), SVP, Verifier |
| 3. Científico (EVF) | ¿Las mejoras realmente mejoran el lab? | EVF 5 niveles, Detection Yield, fichas de evolución |
| Transversal | ¿Cómo sé que aprendo correctamente? | MEL (3 niveles), Metacognitive Ledger |

---

## 2. Ciclos de conocimiento (Knowledge Learning Cycles)

| Ciclo | Objeto | Produce | Estado |
|---|---|---|---|
| KAP (Acquisition) | conocimiento nuevo | EXP / DEC / RULE | Operativo (existente) |
| KVC (Validation) | conocimiento existente | validado / rechazado / reabierto | Operativo (existente) + Gate-003 |
| KEL (Evolution) | conocimiento histórico | superseded / retired / merged / split | Operativo (existente) |
| MEL (Meta-Evaluation) | el proceso de aprender | hipótesis / deudas / sesgos / propuestas | Transversal (3 niveles; MEL-3 declarado sin implementar) |

Nomenclatura: se mantienen KAP/KVC/KEL/MEL como nombres propios. "LPA" NO se reutiliza (ya significa Living Product Architect en el lab).

---

## 3. Procedural Gates

| Gate | Disparo | Puerta | Estado | Documento |
|---|---|---|---|---|
| Gate-001 SVP | Documento con estado | SVP REPORT obligatorio | **ADOPTADO** (EXP 10/10, DY=0,10) | research/state-verification-pattern.md |
| Gate-002 Evidence Contract | Se modifica un KO | Evidence contract | EXISTENTE (de facto) | tools/evidence_contract.py |
| Gate-003 KVC | Se crea una DEC | KVC REPORT obligatorio | **ADOPTADO** (EXP 4/4 DECs, DY=0,25) | research/gate-003-kvc.md |
| Gate-004 RULE | Se declara una RULE | EXP validado | EXISTENTE (de facto) | flujo OBS→HIP→EXP→DEC→RULE |
| Gate-005 KCR | Consulta RAG | Conocimiento gobernado priorizado en search_rag | **ADOPTADO** (EXP 6/7→7/7; vigencia por defecto pendiente) | research/gate-005-knowledge-context-resolution.md |

---

## 4. EVF (Evolution Validation Framework)

- Documento: research/evolution-validation-framework.md
- 5 niveles: Gate Tests → Regression (banco) → Behaviour Benchmark → MEL Metrics → Adoption Review
- Métrica transversal: Detection Yield (DY = defectos únicos / revisiones)
- Fichas: 04-operations/metrics/evolution.jsonl
- Ciclo de vida: Diseño → EXP → BENCHMARK PASS → ADOPTADO → RULE
- Primer caso completo: SVP-001 → ADOPTADO (04-operations/reports/2026-08-06-svp-001-evf.md)
- Plantilla de informe final: definida en el EVF

---

## 5. MEL (transversal)

- Diseño: research/metacognitive-layer-diseno.md (sección 3b: MEL como función transversal; sección MEL-Integrity: Epistemic Completeness)
- 3 niveles: MEL-1 operativo (decisión), MEL-2 procedimental (procedimiento), MEL-3 arquitectónico (el LAB, declarado sin implementar)
- Ledger: 04-operations/metrics/mel_ledger.jsonl (aprendizajes sobre el proceso, no decisiones del dominio)
- Entradas: MEL-2026-08-06-001 (incidente 0.19 → SVP), MEL-2026-08-06-002 (EXP KVC → missing_confidence), MEL-2026-08-06-003 (DEC-004 → MEL-Integrity), MEL-2026-08-06-004 (referencia_ko_no_verificada), MEL-2026-08-06-005 (primer corte MEL-3)
- Métrica MEL-Integrity: integridad epistemológica del sistema de conocimiento (confidence presente / legacy / ausente / evaluables %). Aplicado 06-ago: 50% → 100% de DECs evaluables
- MEL-3 (arquitectónico): primer corte real 06-ago (research/mel-3-arquitectonico.md) — 2/5 gates adoptados, tasa instancias 0,53, integridad 100%, KCR sin datos. Sin infraestructura nueva: usa registros existentes
- PIL (Process Integrity Layer): HIPÓTESIS → PIL-001 (EXP), ficha EVF propia (research/process-integrity-layer.md v2). Opción B confirmada: capa transversal de compliance, NO métrica MEL-3 (MEL=QA después del proceso; PIL=compliance durante). Requisito previo CREADO: Operations Ledger (04-operations/metrics/operations_ledger.jsonl, OP-20260806-001 registrada). EXP: 10 operaciones o 1 semana

---

## 5b. Conocimiento gobernado (Knowledge Objects)

| KO | Tipo | Estado | Nota |
|---|---|---|---|
| DEC-001 | DEC | activo | confidence legacy (missing_historical_data) — ver DEC-004 |
| DEC-002 | DEC | activo | confidence legacy (missing_historical_data) — ver DEC-004 |
| DEC-003 | DEC | activo | confidence 0.94 |
| DEC-004 | DEC | activo | Normalización de metadatos históricos (confidence 0.85) — creada 06-ago |
| DEC-GAIPRO-001 | DEC | active | confidence 0.6 |
| RULE-002, RULE-007, POLICY-002 | RULE/POLICY | activo | — |

Regla de gobierno (DEC-004): el conocimiento histórico se conserva como fue creado; sus limitaciones se declaran (legacy), no se rellenan.

---

## 6. Métricas y registros

| Archivo | Qué registra |
|---|---|
| 04-operations/metrics/svp_exp.jsonl | EXP del SVP (10 revisiones, cerrada) |
| 04-operations/metrics/kvc_exp.jsonl | EXP del KVC (4 DECs, cerrada) |
| 04-operations/metrics/evolution.jsonl | Fichas EVF (SVP-001 ADOPTADO, KVC-001 ADOPTADO, KCR-001 EXP) |
| 04-operations/metrics/mel_ledger.jsonl | Aprendizajes metacognitivos (3 entradas, 06-ago) |
| verification/bank.yaml + history.jsonl | Banco de evaluación (regression + behaviour) |
| lab-state/logs/decision.log | Decisiones del runtime |

---

## 7. Architecture Freeze (COMPLETADO 06-ago)

- Regla: no nuevos componentes hasta que al menos DOS evoluciones completen EVF
- Completadas: **2 de 2** (SVP-001 ADOPTADO + KVC-001 ADOPTADO) → **FREEZE SATISFECHO**
- Durante el freeze solo: validar / medir / retirar / simplificar
- **Estado:** el freeze se cumplió. Nuevos componentes pueden diseñarse de nuevo, pero con la disciplina EVF: toda evolución nueva necesita ficha + EXP + informe antes de adoptarse. KCR-001 queda como evolución en curso (diseñada, sin EXP).

---

## 8. Estado de cada evolución (fichas)

| evolution_id | Cambio | Estado | DY | Evidencia |
|---|---|---|---|---|
| SVP-001 | Gate-001 SVP | **ADOPTADO** | 0,10 | svp_exp.jsonl + informe EVF (04-operations/reports/2026-08-06-svp-001-evf.md) |
| KVC-001 | Gate-003 KVC | **ADOPTADO** | 0,25 | kvc_exp.jsonl + informe EVF (04-operations/reports/2026-08-06-kvc-001-evf.md) + DEC-004 |
| KCR-001 | Gate-005 KCR | **ADOPTADO** | 1,0 (bruto; 0,25 limpio) | informe EVF (04-operations/reports/2026-08-06-kcr-001-evf.md) + history.jsonl |

---

## 9. Próximo paso natural (orden sugerido)

1. ✅ RESUELTO (06-ago): defecto missing_confidence en DEC-001/DEC-002 → metadatos legacy + DEC-004 (normalización del histórico). Integridad epistemológica 50% → 100%
2. ✅ HECHO (06-ago): clase de defecto referencia_ko_no_verificada capturada + MEL-3 primer corte + PIL candidata especificada
3. ✅ HECHO (06-ago): KCR-001 ADOPTADO (EXP 7/7; priorización conocimiento gobernado en search_rag). 3 defectos del evaluador corregidos (run_eval truncamiento, comparador subcadena+tildes)
4. PENDIENTE: vigencia por defecto en search.py (expires/superseded como filtro no opcional) — la priorización está, el filtro temporal no
5. ✅ HECHO (06-ago): decisión PIL — OPCIÓN B (capa propia con ficha EVF, no métrica MEL-3). Requisito previo creado: Operations Ledger (04-operations/metrics/operations_ledger.jsonl). PIL-001 en EXP (10 operaciones o 1 semana). Ficha: evolution.jsonl + research/process-integrity-layer.md v2
6. PENDIENTE: EXP PIL-001 — registrar operaciones reales en operations_ledger.jsonl (cada operación con gate: revisión→SVP, DEC→KVC, RAG→KCR, KO→Evidence Contract, RULE→EXP); criterio de éxito: detectar ≥1 bypass/omisión real
7. PENDIENTE: EXP vigencia por defecto en search.py — requiere item de prueba NUEVO en verification/bank.yaml (regla 3 del banco: lo mantiene el responsable a mano, no Hermes)
8. Registro de tiempo de revisión: operativo desde 06-ago (tiempo_s en svp_exp.jsonl se rellena en revisiones futuras)
