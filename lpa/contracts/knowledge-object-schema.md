---
type: lpa
subtype: contract
status: active
tags: [lpa, contract]
created: 2026-07-30
---
# Knowledge Object — Esquema

**Tipo:** Contrato de datos (contract-first)
**Fecha:** 2026-07-31
**Estado:** v1 — Diseño, sin implementar
**Dependencia:** Sustituye el formato actual de DEC/EXP/OBS/PATTERN por entidades con ciclo de vida

---

## Propósito

Cada pieza de conocimiento del laboratorio deja de ser un documento markdown. Se convierte en una **entidad con ciclo de vida**: se crea, se valida, se monitoriza, envejece, se revalida, y eventualmente se retira o se divide.

---

## Esquema base (YAML)

```yaml
id: DEC-003
type: DEC                  # DEC | EXP | OBS | PATTERN | RULE | POLICY
status: activo             # activo | cuestionado | degradado | retirado | dividido | fusionado
version: 3

created: 2026-07-30
last_validated: 2026-08-15
next_review: 2026-11-15    # ~3 meses, ajustable por tipo
expires: 2027-07-30        # fecha máxima, tras la cual se fuerza revisión

confidence: 0.87           # 0.0 - 1.0, calculado por Confidence Decayer
confidence_label: ALTA     # ALTA (>0.8) | MEDIA (0.5-0.8) | BAJA (<0.5)

evidence:
  - EXP-003
  - EXP-007

dependencies:
  - DEC-001

contradicts: []

superseded_by: null

domain: ai-architecture    # proyecto o dominio LPA
scope: todo_joko_lab        # solo_proyecto | proyectos_similares | todo_joko_lab | todo_lpa

monitoring:
  metric: precision         # tokens | latency | precision | coverage
  baseline: 0.82
  current: null
  last_checked: null

history:
  - date: 2026-07-30
    event: created
  - date: 2026-08-15
    event: validated
    result: confirmado
  - date: 2026-09-10
    event: contradicted_by
    ref: DEC-007

body: >
  Granite 4.1 es el modelo preferido para tareas de generación JSON estructurado
  con esquemas complejos (>10 campos), basado en EXP-003 y EXP-007.
```

---

## Tipos de evento en el historial

| Evento | Significado |
|--------|------------|
| `created` | Se creó la entidad |
| `validated` | Superó una revisión |
| `contradicted_by` | Otra entidad la contradice |
| `degraded` | Bajó confianza por debajo del umbral |
| `retired` | Se retiró (E∅), se conserva historial |
| `split_from` / `split_into` | Se dividió en entidades más específicas |
| `merged_from` / `merged_into` | Se fusionó con otra |
| `superseded_by` | Otra entidad la reemplaza |
| `version_bump` | Cambió el cuerpo sin cambiar el ID |

---

## Comparación con el formato actual

| | Actual (markdown libre) | Knowledge Object |
|---|---|---|
| Validación | Manual, sin tracking | `last_validated` + `next_review` |
| Caducidad | No existe | `expires` obligatorio |
| Confianza | Implícita en el texto | `confidence` numérico + label |
| Trazabilidad | Depende de enlaces manuales | `history` con eventos fechados |
| Contradicciones | Detectadas por Debt Detector | `contradicts` explícito |
| Búsqueda | Solo RAG semántico | RAG + filtros por status/confidence/domain |
| Migración | — | Script `migrate_to_ko.py` pendiente |

---

## Migración

Las DEC-001..003 actuales se migrarían con:

```bash
python3 ~/joko-lab/tools/migrate_to_ko.py --source 01-knowledge/decisions/ --target 01-knowledge/objects/
```

El script:
1. Lee cada DEC.md
2. Extrae campos conocidos (id, created, confidence)
3. Genera YAML con valores por defecto para los nuevos campos
4. No borra el .md original (backup)
5. Pide confirmación antes de escribir
