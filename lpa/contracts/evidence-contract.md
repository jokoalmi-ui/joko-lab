---
type: lpa
subtype: contract
status: active
tags: [lpa, contract]
created: 2026-07-30
---
# Evidence Contract — Requisitos mínimos para DEC

**Tipo:** POLICY (contrato verificable)
**Fecha:** 2026-07-31
**Estado:** Implementado v1 — 2026-07-31 (verificador: `tools/evidence_contract.py`, integrado en `tools/knowledge_health.py`)
**Problema que resuelve:** Actualmente el paso de EXP → DEC depende del juicio, no de un umbral verificable

---

## Principio

> Una DEC no se promociona porque "parece correcta". Se promociona porque cumple un umbral de evidencia definido de antemano.

---

## Contrato

```yaml
evidence_contract:
  minimum_experiments: 2          # al menos 2 EXPs independientes
  minimum_independent_review: 1   # al menos 1 crítica adversarial externa
  minimum_contradictory_tests: 1  # al menos 1 intento de falsación fallido
  minimum_confidence: 0.80        # confidence >= 0.80 antes de promocionar
  minimum_domains: 1              # opcional: 2+ dominios para PATTERN
  max_age_without_review: 180     # días máximos sin revalidación
```

---

## Aplicación

Antes de que una EXP se convierta en DEC, el Decision Engine verifica:

```python
def can_promote_to_dec(knowledge_object):
    c = knowledge_object.evidence_contract
    return (
        len(knowledge_object.evidence) >= c["minimum_experiments"]
        and knowledge_object.independent_reviews >= c["minimum_independent_review"]
        and knowledge_object.falsification_attempts >= c["minimum_contradictory_tests"]
        and (knowledge_object.confidence or 0) >= c["minimum_confidence"]
    )
```

Si no cumple → se rechaza la promoción con un mensaje explícito:
```
DEC-004 rechazada: falta 1 revisión independiente y 1 test de falsación.
```

### Implementación real (v1)

El verificador vive en `tools/evidence_contract.py` (solo lectura, sin LLM):

```bash
python3 ~/joko-lab/tools/evidence_contract.py            # verifica todos los KOs
python3 ~/joko-lab/tools/evidence_contract.py DEC-001    # verifica uno
python3 ~/joko-lab/tools/evidence_contract.py --json     # salida JSON para pipelines
```

Reglas de la implementación:
1. **Solo lectura**: no modifica ningún KO.
2. **Tolerancia de campos**: acepta aliases inglés/español (`evidence`/`evidencia`, `confidence`/`confianza`, etc.). Campo ausente = 0 + nota, nunca asume cumplimiento.
3. **Dependencias ≠ evidencia**: una dependencia transitiva (RULE→DEC) se informa como nota, pero NO cuenta como experimento para el contrato.
4. **Integración**: `tools/knowledge_health.py` ejecuta `verify_all()` en cada auditoría y reporta `Cumplen contrato: X/Y` (dimensión informativa, no penaliza el Health Score).
5. **Estado actual (2026-07-31)**: 0/9 KOs cumplen el contrato completo. DEC-003 es el más cercano (2 evidencias + 0.94 confianza; le faltan revisión independiente y falsación). Esto es deuda real señalada, no un fallo del verificador.
6. **Decisión 02-09-2026 (auditoría INC-006/CP-008)**: los KOs existentes se declaran LEGACY — este contrato es gate de PROMOCIÓN EXP→DEC para KOs NUEVOS; no se re-verifican retroactivamente (rellenar reviews/falsación en 23 fichas viejas sería reconstruir el pasado — anti-histórico, pitfall SVP). El informe lo declara en su salida ("0/N informativo, no penaliza el Health Score"). Fix del verificador: ya no crashea con tipos fuera del contrato (PRED) — backup `tools/evidence_contract.py.bak-20260902-pred`. Promociones futuras: EXP → cumplir contrato → DEC, sin excepción.

---

## Niveles de exigencia por tipo

| Tipo | Experiments | Review | Falsación | Confidence |
|------|------------|--------|-----------|------------|
| DEC | 2 | 1 | 1 | 0.80 |
| RULE | 2 | 1 | 1 | 0.85 |
| POLICY | 1 | 2 | 1 | 0.90 |
| PATTERN | 3 | 1 | 2 | 0.70 |

Las POLICYs requieren más revisión independiente (2) porque afectan a todo el lab.
Los PATTERNs requieren más falsación (2) porque son hipótesis, no decisiones.

---

## Integración con KVC

```
EXP (E3)
    ↓
¿Cumple Evidence Contract?
    ↓
   Sí → DEC
   No → "Falta: 1 revisión independiente" → vuelve a EXP
```

Esto convierte el paso EXP→DEC de "juicio" a "contrato verificable". El modelo o el operador pueden opinar, pero el contrato decide.

---

## Relación con componentes existentes

| Componente | Rol |
|------------|-----|
| Decision Engine | Verifica el contrato antes de promocionar |
| Knowledge Health Auditor | Reporta DECs que no cumplirían el contrato hoy |
| KVC (CP-003) | La fase de falsación alimenta `falsification_attempts` |
| v5 (Fase B) | La crítica adversarial cuenta como `independent_review` |
