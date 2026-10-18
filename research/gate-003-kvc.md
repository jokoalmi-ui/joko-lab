---
title: "Gate-003 — Knowledge Validation Check (KVC)"
type: research
---

# Gate-003 — Knowledge Validation Check (KVC)
**VERACIDAD:** [ALCANCE INTERNO]

**Clase:** Procedural Gate obligatorio (especificación, NO código)
**Estado:** ESPECIFICADO (06-ago-2026). Pendiente de validación en uso real antes de implementar.
**Dependencias:** responde a Gate-001 (SVP) — todo dato de estado que entre en una DEC debe venir contrastado.

**state_sources (SVP Fase 2):**
- 01-knowledge/objects/ (formato DEC-002.yaml)
- hermes-lab/docs/pendientes.txt
**last_state_check:** 2026-08-06

---

## 1. Qué valida (objetivo)

Que una decisión está **suficientemente sustentada** antes de convertirse en una DEC (Knowledge Object tipo DEC).

No valida si la decisión es correcta. Valida si está justificada: si hay evidencia, si la confianza está declarada, si las fuentes existen. Es el equivalente de Evidence Contract (Gate-002) pero para decisiones, no para reglas.

## 2. Cuándo se ejecuta

- En el paso DEC del flujo OBS→HIP→EXP→DEC→RULE, **antes** de crear o actualizar un KO tipo DEC.
- También en DECs ya existentes cuando se revisan (last_validated / next_review), para detectar DECs que nunca tuvieron sustento suficiente.
- Si la entrada NO es una decisión (es un análisis, una observación, un informe), NO aplica KVC: aplica SVP.

## 3. Entradas que recibe

| Campo | Origen | Requerido |
|---|---|---|
| `decision_origin` | experimento / incidente / análisis / decisión previa | SI |
| `hipótesis` (body) | qué se afirma y qué lo sustenta | SI |
| `evidence[]` | 1+ ítem con origen verificable (no opinión) | SI |
| `confidence` | numérica 0..1 (RULE-006: nunca null) | SI |
| `fuentes` | toda afirmación de estado con su fuente (cross-check SVP) | SI |
| `domain` / `scope` | ámbito de aplicación | SI |
| `contradicts` / `dependencies` | relaciones con otros KOs | cuando aplique |

Alineado con el formato real de DEC-002.yaml (id, type, decision_origin, status, version, created, last_validated, next_review, expires, confidence, confidence_label, label_updated, evidence, dependencies, contradicts, superseded_by, domain, scope, monitoring, history, body).

## 4. Condición PASS/FAIL

**PASS** si TODAS:
1. `decision_origin` definido (no genérico)
2. ≥1 ítem de `evidence` con origen verificable (patrón "fuente verificada", lección 04-ago Renaissance: una respuesta sin fuente y con datos incorrectos fue corregida — la regla del lab es que el dato va con su fuente)
3. `confidence` numérica presente (0..1), no null — **EXCEPCIÓN LEGACY (DEC-004, 06-ago):** si `confidence_origin: legacy` está declarado, el null es un estado VÁLIDO (dato histórico no medido, no reconstruido). El defecto es confidence null SIN declaración de origen, no el null en sí
4. Todo dato de estado dentro de la DEC tiene fuente contrastada (SVP)
5. `body`/hipótesis declara explícitamente qué afirma y qué lo sustenta

**FAIL** si alguna no se cumple → **vuelve a OBS/HIP**: o se recoge más evidencia, o se reformula la hipótesis, o se descarta la decisión. No puede pasar a DEC sin cerrar el fallo.

## 5. Trazabilidad (KVC REPORT)

Al pasar, queda constancia en el propio KO (extendiendo `history`):

```yaml
- date: 2026-08-06
  event: kvc_pass
  note: "evidence=2, confidence=0.7, fuentes=3, decision_origin=experimento"
```

Sin ese registro, la DEC no se considera validada. Misma lógica que SVP REPORT: la evidencia es el bloque escrito, no la palabra "validado".

## 6. Especificación declarativa (referencia, no implementar)

```yaml
Gate-003
Nombre: Knowledge Validation Check (KVC)
Objetivo: validar que una decisión está suficientemente sustentada antes de convertirse en DEC
Entrada:
  - evidencia
  - hipótesis
  - confidence
  - fuentes
  - decision_origin
  - domain/scope
Salida: PASS | FAIL
Acciones:
  PASS -> continúa creación/actualización de DEC
  FAIL -> vuelve a OBS/HIP (recoger evidencia, reformular, o descartar)
Criterios PASS:
  - decision_origin definido
  - >=1 evidencia con origen verificable
  - confidence numérica (no null)
  - fuentes de estado contrastadas (SVP)
  - body con afirmación + sustento
Trazabilidad: history += kvc_pass/kvc_fail con fecha y nota
```

## 7. Contexto (lo que NO define KVC)

- KAP y KEL aparecen en el lab (clasificación en analisis-decode; KEL mencionado en pendientes.txt como destino de señales metacognitivas) pero **no tienen especificación formal localizada**. KVC se define con sus propias entradas; cuando KAP/KEL se especifiquen, se alinearán.
- KVC no sustituye a SVP (Gate-001): SVP valida la revisión de documentos con estado; KVC valida el sustento de decisiones. Complementarios.
