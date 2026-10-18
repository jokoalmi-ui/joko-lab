---
type: lpa
subtype: contract
status: active
tags: [lpa, contract]
created: 2026-07-30
---
# De prompt monolítico a Orchestrator + Workers

**Tipo:** Nota arquitectónica
**Fecha:** 2026-07-31
**Estado:** Observación — dirección futura, no implementar aún

---

## Diagnóstico

El prompt v5 tiene 10 pasos, 3 reglas obligatorias, y ~2500 palabras. Está cerca del límite práctico donde cada nueva regla aporta menos valor marginal y aumenta el riesgo de que el modelo:

- Olvide pasos intermedios (pérdida de contexto en modelos largos)
- Contamine pasos posteriores con sesgos de pasos anteriores
- Produzca respuestas de calidad decreciente en los últimos pasos

---

## Principio

> Cuando un prompt supera su complejidad óptima, no se mejora añadiendo reglas. Se mejora dividiéndolo en workers especializados.

---

## Dirección propuesta (no implementar aún)

```
Prompt Director (ligero: ~300 palabras)
    │
    ├── Worker 1: Crítica adversarial (PASO 1, 1b, 5)
    ├── Worker 2: Goodhart + Deuda técnica (PASO 3, 4)
    ├── Worker 3: Falsación (PASO 6)
    ├── Worker 4: Decision Engine (PASO 2, 8, 9)
    │
    └── Síntesis (PASO 10: Metaevaluación)
```

Cada worker:
- Recibe solo el contexto que necesita (análisis de Hermes + su paso específico)
- No sabe que existen otros workers
- Devuelve resultado estructurado

El Director:
- Orquesta la ejecución en paralelo donde sea posible
- Consolida resultados sin reinterpretar
- Aplica la metaevaluación sobre el proceso completo

---

## Cuándo implementar

- Cuando v5 muestre degradación en los últimos pasos (observable en 3-5 ejecuciones reales)
- Cuando aparezca la necesidad de un paso 11 (señal de que el monolito ya no escala)
- Cuando la latencia de v5 completa sea un problema (>60s)

No antes. v5 está recién diseñado y no se ha probado en producción.

---

## Relación con patrones existentes

| Patrón | Relación |
|--------|----------|
| CP-001 (colaboración multi-modelo) | Orchestrator + Workers es literalmente CP-001 aplicado a prompts |
| delegate_task | Implementación natural: cada worker = un delegate_task |
| CP-002 (pensar antes de codificar) | El Director piensa (orquesta), los workers ejecutan |
