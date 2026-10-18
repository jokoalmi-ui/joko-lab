---
type: knowledge
subtype: observation
status: active
tags: [knowledge, observation, rag, reranker, metrica]
created: 2026-09-15
---
# OBS-105: La metrica del RAG esta saturada y no puede medir el reranker
===============================================

## Datos basicos
  ID: OBS-105
  Fecha: 2026-09-15
  Origen: verificacion directa en la sesion 2026-09-15 (grep completo sin truncar,
          ss, ls de tools/, itinerario-revision-implementacion-20260820.md)

## Observacion

El RAG del lab SI tiene reranker y ademas esta activo, pero su aporte no es
medible con la metrica que hay hoy:

  - tools/reranker_daemon.py (CrossEncoder, modelo por defecto
    BAAI/bge-reranker-v2-m3) sirve POST /rerank en el puerto 8765.
  - Esta ACTIVO: 'LISTEN 127.0.0.1:8765 ... users:(("python3",pid=2526))'
    (comprobado 2026-09-15 18:1x CEST).
  - tools/rag_telemetry.py mide el paso: campo rerank_s junto a embed_s,
    retrieve_s, total_s.
  - 04-operations/reports/2026-08-05-analisis-rag-atareado.txt (l. 31 y 89) ya
    lo describe como pieza del lab: "Embedding + reranker (BGE-M3 cross-encoder)".
  - Existe evaluacion formal del RAG: tools/evaluar_rag.py ->
    recall@5 100% con 8 consultas (12-ago, OP-007), registrado en
    itinerario-revision-implementacion-20260820.md (l. 27); y existe
    tools/evaluar_rag_adversarial.py (18-ago).

El problema de medicion: con recall@5 = 100% sobre 8 consultas la metrica esta
en el techo, asi que no puede distinguir "con reranker" de "sin reranker".
Un instrumento saturado no vale para decidir si se mantiene la pieza
(INSTRUMENTO: validar la metrica antes de confiar en ella).

## Correccion de una afirmacion previa (mismo dia)

A las 18:0x CEST de hoy se afirmo en el analisis del reel DdKHNTOlCSg que
"no hay script de reranker en tools/". Es FALSO. Causa: el grep de
comprobacion se trunco con head y los .py quedaron fuera de la salida, y se
concluyo una ausencia sin ver la lista completa. Corregido en
research/analisis-reel-6-agentic-ai-architectures-20260915.md (seccion
CORRECCION) y en el backlog. Regla que se refuerza: no afirmar una ausencia
a partir de una salida truncada.

## Relacionados
  - HYP-003 (aporte del reranker hoy no medible)
