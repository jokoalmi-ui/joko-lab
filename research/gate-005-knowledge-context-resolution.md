---
title: "Gate-005 — Knowledge Context Resolution (KCR)"
type: research
---

# Gate-005 — Knowledge Context Resolution (KCR)
**VERACIDAD:** [ALCANCE INTERNO]

**Clase:** Procedural Gate obligatorio (especificación, NO código)
**Estado:** DISEÑADO (06-ago-2026). Sin implementar. Adaptará search.py / context_builder / knowledge_resolver cuando el diseño se estabilice.
**Origen:** Caso 1 del informe SVP (documento antiguo recuperado antes que el vigente; la vigencia existe pero no participa en retrieval).

**state_sources (SVP Fase 2):**
- verification/bank.yaml
- GUIA-JOKO-LAB.md (sección 6.9, patrón OKF)
- tools/search.py
**last_state_check:** 2026-08-06

---

## 1. Qué resuelve (objetivo)

Decidir, para cada consulta RAG, si existe conocimiento gobernado (KO) relevante y construir el contexto aplicando su estado de vigencia. Deja de ser un "search" y pasa a ser una **resolución del conocimiento**: el estado no es un filtro opcional, es parte del contrato de la consulta.

Fallo que previene (verificado en el lab, GUIA 6.9): el fallo más caro de un RAG no genera error — la respuesta "suena completa" pero le falta un hecho, o el doc viejo gana al vigente por volumen de trozos (EXP1-001/EXP3-001).

## 2. Estado actual del lab (verificado 06-ago, no inventado)

| Pieza | Existe | Alcance actual |
|---|---|---|
| Índice OKF | SI — tools/generar_indice_okf.py → verification/indice.md | decisions_rules_policies_only; se concatena al system prompt como índice, NO filtra retrieval |
| Filtro status en search.py | SI — filtro_status opcional (P3, 05-ago) | SOLO si el revisor lo pide (--status); no participa por defecto |
| Filtro expires | NO | No existe en search.py; el campo existe en los KOs pero no participa |
| knowledge_resolver | Existe como consumidor (GUIA: run_eval, joko-context lo usan) | No resuelve vigencia |

## 3. Flujo del Gate-005 (diseño)

```
Query
   │
   ▼
¿Existe KO gobernado relevante?
   │
   ├── NO
   │      ▼
   │   Retrieval normal (sin gate)
   │
   └── SI
          │
          ▼
   Resolver vigencia:
   - Eliminar superseded
   - Eliminar expires (fecha > hoy)
   - Priorizar active
   - Aplicar índice OKF (scope del KO)
          │
          ▼
   Construir contexto (con estado resuelto)
          │
          ▼
   LLM
```

## 4. Condiciones del gate (PASS/FAIL del contexto)

El contexto construido por el gate debe cumplir:

1. **Todo KO superseded** excluido (o marcado explícitamente como histórico si es imprescindible)
2. **Todo KO con expires < hoy** excluido del contexto activo
3. **KOs active priorizados** sobre cualquier fragmento RAG no gobernado con el que compitan
4. **Índice OKF aplicado**: si la query toca dominio cubierto por un KO, el body del KO (curado, con keywords) participa por defecto — no solo si el RAG lo recupera
5. Si el gate no puede resolver vigencia (p. ej. falta de fecha en un KO): el KO se incluye con marca `estado: no_resuelto` y el LLM lo recibe explícitamente como incierto — nunca como vigente

## 5. Entradas / Salidas

**Entradas:**
- Query del usuario
- Fragmentos RAG recuperados (top-k)
- Índice OKF (verification/indice.md)
- Estado de los KOs: status, expires, superseded_by (desde objects/)

**Salidas:**
- Contexto resuelto (KOs activos + fragmentos no gobernados, con marca de vigencia)
- Nota de gate: qué se excluyó y por qué (trazabilidad, mismo patrón que SVP REPORT / KVC REPORT)

## 6. Implementación prevista (solo cuando el diseño esté estable)

| Componente | Cambio previsto |
|---|---|
| search.py | filtro status/expires por defecto (no opcional) para KOs; expires como columna utilizable |
| context_builder.py | llamar al gate antes de inyectar contexto |
| knowledge_resolver | resolver vigencia (eliminar superseded/expires, priorizar active) |
| generar_indice_okf.py | regenerar índice al cambiar KOs (ya existe el mecanismo) |

Nada de esto se implementa ahora. Primero se estabiliza el diseño y se valida con el banco de evaluación existente (verification/, banco 6 items).

## 7. Relación con los otros gates

- **Gate-001 SVP** valida la revisión de DOCUMENTOS con estado (no cubre consultas — limitación declarada).
- **Gate-005 KCR** cubre el caso que SVP no cubre: las CONSULTAS que ignoran vigencia.
- Complementarios: SVP evita aprobar documentos sin contrastar; KCR evita recuperar datos muertos.
- Alimenta MEL: métrica de contexto excluido por vigencia (KOs superseded/expires filtrados por consulta).

## 8. Validación prevista (EXP del gate)

- Banco de evaluación existente (verification/, 6 items) como baseline
- Añadir items: (a) consulta que debe recuperar KO vigente vs fragmento viejo, (b) consulta a KO superseded que debe quedar excluido, (c) consulta con expires vencido
- Criterio: cobertura 6/6 + nuevos items, sin regresión de latencia > umbral medido
- Tras validación → decidir promoción (OBS→HIP→EXP→DEC→RULE)

## Nota

Este diseño no implementa nada. Cuando se apruebe su estabilidad, los componentes (search.py, context_builder, knowledge_resolver) se adaptarán siguiendo esta especificación, con backup previo (RULE-008) y verificación con el banco existente.
