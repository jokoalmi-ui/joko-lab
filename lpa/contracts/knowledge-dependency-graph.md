---
type: lpa
subtype: contract
status: active
tags: [lpa, contract]
created: 2026-07-30
---
# Knowledge Dependency Graph (KDG)

**Tipo:** Concepto arquitectónico — E0
**Fecha:** 2026-07-31
**Estado:** Diseño, sin implementar
**Problema que resuelve:** Cuando hay cientos de KOs, modificar uno sin saber qué rompe

---

## Problema

Actualmente las dependencias entre conocimiento son implícitas. DEC-003 referencia EXP-004 en su campo `evidence`, pero no hay forma de preguntar:

> "¿Qué pasaría si retiro DEC-001?"

---

## Propuesta

Un grafo dirigido donde los nodos son Knowledge Objects y las aristas son relaciones tipadas:

```
DEC-001 (Qwen descartado)
    │
    ├──[evidence]──→ EXP-001
    ├──[depends_on]─→ POLICY-001 (FATAL)
    │
    └──[impacts]────→ DEC-003 (Gemma creatividad)  ← si Qwen está descartado,
                     → RULE-001 (modelo-creatividad)  Gemma hereda tareas creativas
                     → RULE-004 (bloqueo-qwen)
```

---

## Tipos de aristas

| Tipo | Significado | Ejemplo |
|------|------------|---------|
| `evidence` | EXP valida una DEC | EXP-003 → DEC-003 |
| `depends_on` | DEC requiere otra DEC | KO-041 → DEC-001 |
| `contradicts` | Dos entidades se contradicen | DEC-005 → DEC-002 |
| `supersedes` | Una reemplaza a otra | DEC-007 → DEC-003 |
| `split_from` | Una DEC se dividió | DEC-008a → DEC-003 |
| `merged_from` | Varias se fusionaron | DEC-009 → [DEC-004, DEC-005] |
| `implements` | Un componente implementa una DEC | decision_router.py → DEC-001 |
| `references` | Referencia cruzada sin dependencia fuerte | PATTERN-002 → DEC-003 |

---

## Consultas que habilitaría

```
> python knowledge_graph.py impact DEC-001

Impacto de modificar DEC-001 (Qwen descartado):
  Afecta directamente:  2 KOs
  Afecta indirectamente: 8 KOs
  Componentes que dependen: decision_router.py, activation_engine.py

> python knowledge_graph.py orphans

KOs sin dependencias entrantes: 3
KOs sin dependencias salientes: 7
KOs huérfanos (sin entrada ni salida): 2

> python knowledge_graph.py path DEC-001 DEC-007

Camino más corto: DEC-001 → RULE-004 → DEC-007 (2 saltos)
```

---

## Implementación mínima

Un script `knowledge_graph.py` que:

1. Lee todos los KOs de `01-knowledge/objects/`
2. Construye grafo en memoria (networkx o dict)
3. Exporta a DOT/Graphviz para visualización
4. Responde consultas de impacto, huérfanos, camino más corto

No necesita base de datos. Con < 100 KOs, un grafo en memoria con caché en JSON basta.

---

## Relación con componentes existentes

| Componente | Rol |
|------------|-----|
| Knowledge Objects | Nodos del grafo |
| Debt Detector | Ya detecta huérfanos — alimenta KDG |
| Pruning | KDG informa qué rompería retirar un KO |
| Health Auditor | KDG añade métrica de "cohesión del grafo" |
