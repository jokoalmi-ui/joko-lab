---
type: lpa
subtype: procedure
status: active
tags: [lpa, procedure]
created: 2026-07-30
---
# Knowledge Pruning — Procedimiento (v2)

**Tipo:** Procedimiento LPA — Fase 0 (concepto)
**Fecha:** 2026-07-31 (v2: operaciones expandidas + Knowledge Health Index)
**Estado:** E0 — Observación, sin implementar
**Dependencias:** Knowledge Health Auditor (implementado), Knowledge Object (diseñado)

---

## Problema que resuelve

El laboratorio acumula conocimiento. Sin poda, se degrada por acumulación, obsolescencia y contradicciones no resueltas.

---

## Principio

> Un sistema que solo aprende a incorporar conocimiento pero no aprende a retirarlo termina degradándose por acumulación.

---

## Knowledge Health Index (KHI)

Métrica global de 0-100 calculada por `knowledge_health.py`:

```
KHI = 100 - (expiradas×5 + sin_validar×3 + sin_revisión×2 + confianza_baja×3 + sin_evidencia×4 + sin_expiración×1 + contradicciones×5)
```

| Rango | Estado | Acción |
|-------|--------|--------|
| 90-100 | Sano | Pruning ligero (trimestral) |
| 70-89 | Atención | Pruning medio (mensual) |
| 50-69 | Degradado | Pruning profundo (quincenal) |
| <50 | Crítico | Intervención humana prioritaria |

---

## Operaciones de Pruning

### VALIDAR
Confirmar que una DEC/EXP sigue siendo correcta con la evidencia actual.
- Disparador: `next_review` vencido
- Acción: ejecutar paso de falsación de KVC v5, actualizar `last_validated`

### DEGRADAR
Reducir confianza sin retirar.
- Disparador: evidencia contradictoria parcial
- Acción: `confidence -= 0.2`, `status = cuestionado`

### RETIRAR
Mover a E∅ (revocado).
- Disparador: refutación completa, condición desaparecida, o sustitución
- Acción: `status = retirado`, conservar historial, no eliminar

### DIVIDIR
Una DEC era demasiado general y ahora se sabe que depende del contexto.
- Ejemplo: "Granite para JSON" → "Granite para JSON < 10 campos" + "DeepSeek para JSON > 10 campos"
- Acción: `status = dividido`, crear dos nuevas entidades con `split_from`

### FUSIONAR
Dos DECs dicen lo mismo con distinto vocabulario.
- Acción: `status = fusionado`, crear entidad consolidada con `merged_from: [DEC-X, DEC-Y]`

### VERSIONAR
El cuerpo cambia pero la identidad permanece.
- Disparador: refinamiento sin cambio de conclusión
- Acción: `version += 1`, evento `version_bump` en historial

### ARCHIVAR
Conocimiento históricamente relevante pero sin impacto operativo actual.
- Disparador: scope reducido a cero (ej: modelo que ya no se usa)
- Acción: mover a `archive/`, no retirar (conserva valor documental)

---

## Progresión de implementación (5 fases)

| Fase | Qué | Riesgo | Estado |
|------|-----|--------|--------|
| 1 | **Knowledge Health Auditor** — solo lectura, detecta problemas | Nulo | ✅ Implementado (`tools/knowledge_health.py`) |
| 2 | **Knowledge Object** — DEC/EXP/OBS con metadatos de ciclo de vida | Bajo (solo esquema) | 🔄 Diseñado (`contracts/knowledge-object-schema.md`) |
| 3 | **Revalidación asistida** — el sistema propone qué revisar, el humano decide | Bajo | ❌ |
| 4 | **Pruning semiautomático** — marca candidatos a retirar/degradar/dividir, no ejecuta | Medio | ❌ |
| 5 | **Pruning automático** — solo para reglas conservadoras (confidence > 0.9, 3+ validaciones, sin contradicciones) | Alto | ❌ |

**No saltar fases.** Cada fase debe funcionar varias semanas antes de pasar a la siguiente.
