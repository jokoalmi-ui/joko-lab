---
title: "Process Integrity Layer (PIL) — especificación v2 (Opción B confirmada)"
type: research
---

# Process Integrity Layer (PIL) — especificación v2 (Opción B confirmada)
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 06-ago-2026
**Estado:** HIPÓTESIS ARQUITECTÓNICA → PIL-001 (EXP) con ficha EVF propia. NO es LPA ni gate: capa transversal de cumplimiento.
**Decisión (06-ago, responsable):** PIL se formaliza como capa propia con ficha EVF (Opción B), NO como métrica MEL-3. Razón arquitectónica: separación de responsabilidades — PIL responde una pregunta distinta de las que responde cualquier ciclo existente.

**state_sources (SVP Fase 2, añadido 06-ago tras hallazgo OP-...011):**
- research/ecosistema-gobernanza.md
- 04-operations/metrics/operations_ledger.jsonl
- 04-operations/metrics/evolution.jsonl (ficha PIL-001)
**last_state_check:** 2026-08-06

---

## 1. Qué responde (única)

> **¿Se ha ejecutado correctamente el procedimiento obligatorio?**

- ¿Se ejecutó Gate-003?
- ¿Se ejecutó SVP?
- ¿Se consultó la fuente obligatoria?
- ¿Hubo bypass?
- ¿Hubo exención?
- ¿Qué porcentaje de operaciones siguieron el procedimiento?

No evalúa conocimiento (KAP), decisiones (KVC), ciclo de vida (KEL) ni calidad epistemológica (MEL). Evalúa **disciplina procedimental**.

## 2. Por qué NO es MEL

| Dimensión | MEL | PIL |
|---|---|---|
| Pregunta | ¿estamos bien calibrados? ¿qué componente aporta valor? | ¿se ejecutó el gate obligatorio? |
| Cuándo | DESPUÉS del proceso (análisis longitudinal) | DURANTE el proceso (compliance) |
| Disciplina | QA (calidad del producto) | Compliance (cumplimiento del proceso) |

Si se mezclan, MEL se convierte en cajón de sastre. El diseño del lab ha evitado eso hasta ahora.

## 3. Posición arquitectónica (capa transversal)

```
              PIL
               │
               ▼
KAP → KVC → KEL → MEL
```

PIL supervisa todas. No sustituye ninguna. No es un LPA (no procesa conocimiento): es una capa de cumplimiento.

## 4. REQUISITO PREVIO — Operations Ledger (el denominador)

Sin el número total de operaciones susceptibles de gate, PIL solo puede decir "he visto 7 gates" pero nunca "de 10 operaciones, 9 ejecutaron todos los gates (90%)".

Esquema del registro (04-operations/metrics/operations_ledger.jsonl):

```json
{"operation_id": "OP-20260806-001", "ts": "2026-08-06T13:30:00+02:00",
 "operation_type": "revision_documental|creacion_dec|consulta_rag|modificacion_ko|...",
 "required_gates": ["SVP", "KVC", ...],
 "executed_gates": ["SVP"],
 "bypass": false,
 "exemption": null,
 "result": "PASS|FAIL|COMPLETED|..."}
```

- `required_gates` = qué gates deberían haberse ejecutado para ese tipo de operación (mapa fijo: revisión documental → SVP; creación DEC → KVC; consulta RAG → KCR; modificación KO → Evidence Contract; declaración RULE → EXP; **modificación código pipeline → VERIFIER + SVP-diff, añadido 06-ago tras hallazgo OP-...010**)
- `executed_gates` = qué gates se ejecutaron realmente
- `bypass` = saltó un gate obligatorio (con justificación en `exemption`)
- `exemption` = tipo de exención (p. ej. legacy) o null
- El ledger NO se llena solo: cada operación registra su entrada al ejecutarse (mismo patrón que svp_exp.jsonl: registro por operación, no agregado)

**Gap actual:** no existe este registro hoy. Solo existen los de las operaciones REVISADAS (svp_exp, kvc_exp). El primer paso de la EXP PIL-001 es crear el Operations Ledger y empezar a registrar operaciones reales.

## 5. Métricas PIL (con denominador disponible)

| Métrica | Definición | Objetivo |
|---|---|---|
| Tasa de ejecución de gates | executed_gates / required_gates por operación | 100% |
| Cobertura de procedimiento | operaciones con todos los gates ejecutados / operaciones totales | 100% |
| Bypass registrados | operaciones con bypass=true | registrar |
| Omisiones no registradas | operaciones sin gate NI justificación | 0 |
| Exenciones usadas | % de operaciones con exemption | registrar |

## 6. Ciclo de vida (mismo rigor que el resto)

```
OBS (incidente 0.19: fallo de procedimiento)
 ↓
HIP (PIL como capa de compliance)  ← ESTAMOS AQUÍ
 ↓
EXP (PIL-001: crear Operations Ledger + medir N operaciones)
 ↓
EVF (informe + DY)
 ↓
BENCHMARK PASS
 ↓
ADOPTADO
 ↓
RULE (si procede)
```

Ni siquiera la arquitectura queda exenta del mismo proceso de validación que se exige al conocimiento. PIL-001 queda registrada en evolution.jsonl como EXP.

## 7. Criterio de éxito de la EXP PIL-001

- El Operations Ledger existe y registra operaciones reales (volumen definido: 10 operaciones o 1 semana)
- Se detecta al menos un bypass u omisión real (Condición B de utilidad)
- Sin ello, PIL no demuestra valor y no se promueve

## 8. Gate de código (VERIFIER + SVP-diff) — definido 06-ago tras hallazgo OP-...010

El hallazgo de la EXP: los fixes de run_eval/comparador/context_builder se hicieron con backup pero SIN gate obligatorio (el mapa no cubría "modificación de código del pipeline"). Definición del gate para esa clase de operación:

| Requisito | Qué exige | Ejemplo aplicado 06-ago |
|---|---|---|
| **Backup previo** | copia .bak-YYYYMMDD del archivo antes de tocar (RULE-008) | run_eval.py.bak-20260806, comparador.py.bak-20260806, context_builder.py.bak-20260806 |
| **Verifier** | script ad-hoc bajo /tmp con prefijo hermes-verify- que comprueba el comportamiento cambiado | /tmp/hermes-verify-kcr-run-eval.py (6/6), /tmp/hermes-verify-comparador-fix.py (7/7) |
| **SVP-diff** | revisar el diff contra el estado (¿toca conocimiento gobernado? ¿declara fuentes? ¿deja marcadores?) | los 3 fixes documentados con causa raíz en mel_ledger |

Regla: toda modificación de código del pipeline (tools/, verification/) registra su operación en el Operations Ledger con required_gates=["VERIFIER","SVP-diff"] ANTES de declararse completada. Sin verifier, la operación no existe (mismo patrón que SVP REPORT).
