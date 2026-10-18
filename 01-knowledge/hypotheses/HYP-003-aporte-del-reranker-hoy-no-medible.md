---
type: knowledge
subtype: hypothesis
status: active
tags: [knowledge, hypothesis, rag, reranker, metrica]
created: 2026-09-15
---
# HYP-003: El reranker aporta, pero la metrica actual no puede verlo

**Origen:** OBS-105
**Fecha:** 2026-09-15
**Estado:** propuesta

## Observacion
El reranker (BAAI/bge-reranker-v2-m3) existe y esta activo en 127.0.0.1:8765,
con telemetria de su tiempo (rerank_s). La unica evaluacion registrada del RAG
es recall@5 100% con 8 consultas (12-ago): metrica saturada, sin capacidad de
discriminar.

## Hipotesis
El reranker mejora el orden de lo recuperado (no el recall, que ya esta al
100%), y el efecto no aparece porque se esta mirando la metrica equivocada.
La mejora, si existe, se vera en el ranking y en la respuesta final (precision
del contexto util, citas correctas), no en "lo encuentro o no lo encuentro".

## Prediccion
Con un banco que discrimine (mas consultas + casos adversariales, ya existe
tools/evaluar_rag_adversarial.py), comparando la MISMA consulta con y sin
reranker y el mismo modelo:
  - el orden de los documentos relevantes cambia (mejor posicion media)
  - y/o la respuesta final mejora en un banco de preguntas con respuesta
    verificable
Medible con: posicion media del documento correcto, precision del contexto
util, acierto en banco adversarial. Umbral: NO a priori (RULE-015); primero
baseline con/sin reranker y despues se decide.

## Validacion
- [ ] Banco ampliado (>8 consultas) + baseline sin reranker
- [ ] EXP-XXX disenado (con/sin reranker, mismo banco y mismo modelo)
- [ ] EXP-XXX ejecutado
- [ ] Resultado: [confirma | refuta | inconcluso]

## Decision derivada
- DEC-XXX (si confirmada: mantener el reranker ya no seria "por diseno", seria por dato)

## Conexiones
- [[OBS-105]] — origen
