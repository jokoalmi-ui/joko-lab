---
title: "Análisis — Carrusel RAG completo (Ketan Sagare, 10 slides)"
type: research
---

# Análisis — Carrusel RAG completo (Ketan Sagare, 10 slides)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 10-ago-2026
**Fuente:** https://www.instagram.com/p/Db2CMH5Ar3J/ — ds_ai_ketan (Ketan Sagare)
**Método:** Descarga 10 imágenes (webp) + GLM 4.6V local

---

## Contenido (10 slides educativas de RAG)

1. **Fundamentos de RAG** — 3 pasos: Recuperar → Aumentar → Generar. Ventajas: conocimiento actualizado, reduce alucinaciones, datos privados seguros.
2. **Arquitectura RAG** — pipelines Offline (parseo→chunking→embedding→vector DB) y Online (recuperar→rerank→LLM).
3. **Document Ingestion** — convertir documentos brutos en contenido limpio y buscable.
4. **Chunking** — dividir en piezas significativas: tamaño fijo, recursiva (por encabezados), semántica.
5. **Embeddings** — texto → vectores numéricos que capturan significado.
6. **Vector Database** — búsqueda por similitud, ANN, HNSW, filtrado de metadatos, Top-K. Herramientas: Pinecone, Milvus, Weaviate, Qdrant, Chroma.
7. **Estrategias de Recuperación** — Densa (semántica), Esparse (BM25), Híbrida (RRF), Filtrado por metadatos.
8. **Reranking y Transformación de Consultas** — Cross-Encoder, BGE Reranker; Rewriting, Expansión, Multi-query, HyDE.
9. **Evaluación de RAG** — Recall@K, Precision@K, MRR (recuperación); Fiabilidad, Relevancia, Correctitud, Completitud (generación).
10. **Best Practices y Retos** — chunking inteligente, embeddings de calidad, híbrido+reranking, filtrado.

---

## 🎯 Aplicación al LAB — VALIDACIÓN COMPLETA (el lab ES un RAG maduro)

| Slide del carrusel | Implementación en el lab |
|---|---|
| 1. Fundamentos (R→A→G) | ✅ search.py (_busqueda_hibrida) + context_builder |
| 2. Arquitectura (offline/online) | ✅ indexer.py (offline) + pipeline_proxy (online) |
| 3. Ingestión de documentos | ✅ indexer (markdown/yaml + hash incremental) |
| 4. Chunking | ✅ load_notes_con_hash + fragmentos por archivo |
| 5. Embeddings | ✅ **BGE-M3** (multilingüe, mejor que los del carrusel) |
| 6. Vector DB | ✅ **LanceDB** (FTS+vectorial, híbrido nativo) |
| 7. Estrategias de recuperación | ✅ **Híbrida (FTS + vectorial + RRF)** — exactamente el patrón del carrusel |
| 8. Reranking | ✅ **Reranker CPU (daemon)** + BGE-Reranker |
| 9. Evaluación | 🟡 Parcial — run_10_tests + suite, pero sin métricas RAG formales (Recall@K, MRR) |
| 10. Best practices | ✅ Híbrido + rerank + filtros |

**El lab implementa 9/10 slides de forma superior** (BGE-M3, LanceDB, RRF, reranker dedicado). El único gap: **evaluación formal del RAG** (métricas de recuperación).

## Veredicto honesto

**El carrusel es el manual del RAG que el lab YA tiene implementado y superior.** Cero acciones nuevas.

**El único matiz (gap de evaluación):** el lab mide pipeline (TTFB, tokens) pero NO mide calidad de recuperación formalmente (Recall@K, Precision@K, MRR). No es urgente, pero si algún día se quiere optimizar el RAG con datos, esas métricas serían la base.

**Opción futura (ya anotada como PROYECTOS FUTUROS del MCP):** el punto 9 conecta con el backlog — "Agentic RAG Qdrant" del análisis de 9 MCP projects. No implementar ahora.

## Conclusión

Validación total: el RAG del lab es un RAG de nivel 2026 completo (híbrido + rerank + filtros). Sin backlog nuevo. Material útil para TFM (el lab como caso de estudio de RAG).

## Nota

Canal ds_ai_ketan (Ketan Sagare) — cuenta educativa de IA/ML. Carrusel de 10 slides muy bien estructurado como curso de RAG.
