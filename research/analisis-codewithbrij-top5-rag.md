---
title: "Análisis — Top 5 RAG Architectures 2026 (codewithbrij, 20-ago-2026)"
type: research
---

# Análisis — Top 5 RAG Architectures 2026 (codewithbrij, 20-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/codewithbrij/p/DcNJAfgDq07/ (19-ago, Brij Kishore Pandey)
**Método:** alts oficiales IG del DOM (2 slides visibles sin login) + cruce con research/
**Veredicto:** [VERIFICADO]

## Contenido (transcripción de los alts del DOM real)

### Slide 1 — "GENAI ARCHITECTURE GUIDE 2026: Top 5 RAG Architectures"

1. **HYBRID RAG** — Dense Results + Sparse Results → **Reciprocal Rank Fusion** (fusión por ranking)
2. **GRAPH RAG** — Chunks → LLM → Knowledge Graph Extractor (nodos, aristas, relaciones) → query al grafo
3. **AGENTIC RAG** — Query → Planner → Search/WebSearch → Reasoner → Agent
4. **CORRECTIVE RAG (CRAG)** — Query → Retriever → Retrieved Docs → Evaluator → "agente repite hasta confiar" → Rewrite/Fallback → Final Answer
5. **MULTIMODAL RAG** — Unified Vector Indexing → Retrieval → Multimodal LLM → Answer

### Slide 2 — Comparativa Classic vs Graph vs Agentic (post 13-ago del mismo autor)

| | Classic RAG | Graph RAG | Agentic RAG |
|---|---|---|---|
| Acción | Retrieve | Connect | Reason |
| Carácter | Rápido, simple | Rico en entidades | Adaptativo |
| Salto | Single-hop | Multi-source | Self-correcting |
| Flujo | Embed→VectorDB→Top-K→LLM | Entity extraction→Knowledge Graph→LLM | Reasoning Agent→Web Search→LLM→Self-Eval |

## 🔴 Conexión con el LAB — estado a 19-nov-2026 (revalidado)

| Arquitectura | Estado en el lab (19-nov-2026) | Evidencia en disco |
|---|---|---|
| **Hybrid RAG (RRF)** | ✅ **IMPLEMENTADO** (en ago era solo futurible) | `tools/search.py`: `_calcular_rrf(fts_ids, vec_ids, K=60)`, líneas 280-336 |
| Graph RAG | ⚪ No — el grafo del lab son skills, no un knowledge graph de entidades | `codebase-memory` indexa código, no documentos |
| **Agentic RAG** | ✅ **IMPLEMENTADO** (en ago era ⚪) | `tools/agentic_loop.py` (evaluación determinista del loop) + `tools/medir_agentic.py` |
| CRAG (correctivo) | 🟡 **PARCIAL — hueco real** | `tools/evaluar_rag_adversarial.py` (10-nov) hace el *grading* de documentos; **falta** reescritura de query y fallback automático |
| Multimodal RAG | ⚪ No — LanceDB es texto; la visión (GLM) es on-demand, fuera del índice | — |

**Lectura:** de las cinco arquitecturas, el lab ya ejecuta dos (híbrida+RRF y agéntica) y tiene media tercera. Lo que queda por construir, si se quiere completar el eje, es **CRAG completo** (evaluator → rewrite/fallback), no volver a discutir híbrida.

## Veredicto

- El carrusel **valida el camino del lab**: RAG clásico sólido (LanceDB 19.894 filas, recall@5 100%) + el siguiente paso natural es **Hybrid RAG con RRF** (ya anotado)
- CRAG valida conceptualmente el **gate de veracidad** (evaluar → corregir → repetir) — el lab lo hace manual, no automático
- No hay nada que implementar NUEVO hoy: es confirmación de la dirección

## Revalidación 19-nov-2026 — repost del mismo temario

- **Fuente nueva:** https://www.instagram.com/p/Df7HNY0Neof/ — `julianvelez1997`, 19-nov-2026, con etiqueta «Pb @codewithbrij». Es **re-publicación del mismo contenido** de `DcNJAfgDq07` (19-ago-2026): Hybrid, GraphRAG, Agentic, Corrective y Multimodal. Sin material nuevo.
- **Método:** caption íntegro por `og:description` (verificado). El JSON embebido dio `carousel_media_count = 7`, pero sus `accessibility_caption` eran de posts ajenos del feed («Video by WEB DESIGN», «Photo by Sangram Singh Yadav») → **nº de láminas: no verificado**; no se usó ese bloque ni se descargaron imágenes.
- **Corrección al análisis original:** la fila «Agentic RAG ⚪ No» y la fila «Hybrid 🔵 futurible» quedaron obsoletas; ambas están implementadas (ver tabla de arriba).
- **Hueco vigente:** CRAG sin reescritura de query ni fallback automático.

## Nota honesta

Solo 2 slides visibles sin login (limitación conocida de IG); el contenido viene de los alts oficiales del DOM (fiables como resumen, no al 100% para diagramas). El gráfico comparativo Classic/Graph/Agentic corresponde a un post del 13-ago del mismo autor (pitfall conocido: el alt puede ser de otro post del feed) pero es coherente con el tema.
