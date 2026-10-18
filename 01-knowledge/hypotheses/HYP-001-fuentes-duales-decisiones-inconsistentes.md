---
type: knowledge
subtype: hypothesis
status: active
tags: [knowledge, hypothesis]
created: 2026-07-30
---
# HYP-001: Fuentes duales causan decisiones inconsistentes

**Origen:** OBS-001
**Fecha:** 2026-07-30
**Estado:** confirmada

## Observación
El decision_router.py consultaba dos fuentes distintas para decidir
qué modelo recomendar: una tabla hardcodeada (6 entradas) y consultas
al RAG. Si se creaba DEC-004, la tabla hardcodeada no la detectaba.

## Hipótesis
Si las fuentes divergen, el router tomará decisiones inconsistentes
— la tabla hardcodeada dará una respuesta, el RAG dará otra distinta.
El usuario no sabrá cuál es la autoritativa.

## Predicción
Al eliminar la tabla hardcodeada y dejar solo RAG como fuente única:
- Nuevas DEC serán detectadas automáticamente
- No habrá divergencia posible
- La confianza será coherente con el origen de datos

## Validación
- [x] F1.1 ejecutado: capability_map eliminado de decision_router.py
- [x] _query_rag_routing() ahora consulta solo RAG
- [x] Sintaxis verificada (ast.parse OK)
- [ ] Pendiente: verificar con RAG funcional (test end-to-end)

## Decisión derivada
- DEC-XXX (pendiente — formalizar que RAG es fuente única de decisión de modelo)

## Conexiones

- [[OBS-001]] — OBS-001: router con dos fuentes de verdad (origen)
- [[DEC-002]] — DEC-002: decisión sobre el router
