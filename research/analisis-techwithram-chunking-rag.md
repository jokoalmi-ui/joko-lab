---
title: "Análisis — \"8 Chunking Strategies To Improve RAG Performance\" (techwith.ram, 28-ago-2026)"
type: research
---

# Análisis — "8 Chunking Strategies To Improve RAG Performance" (techwith.ram, 28-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DclSiz0ia0a/ (techwith.ram, 28-ago, 941 likes, 28 comentarios)
**Método:** pipelina IG → caption íntegro + 2 slides transcritas con GLM local (glm-4.6v-flash, 0€, max_tokens 4000 — regla validada). Nota: la slide 2 enumera 8 estrategias con nombres ligeramente distintos a la portada (Fixed-size, Sliding Window, Semantic, Document Structure, Hybrid, Token-based, Custom, Contextual Relevance) — misma familia.

## Contenido (transcripción GLM)

**Problema (caption):** el chunking puede romper tu RAG:
- Chunks muy pequeños → pierdes contexto
- Muy grandes → retrieval ruidoso
- Límites incorrectos → la info correcta nunca se recupera junta

**Las 8 estrategias (slide 2, con descripción):**

| # | Estrategia | Qué es | Cuándo usarla |
|---|---|---|---|
| 1 | **Fixed-size** | Dividir en trozos iguales (256-512 tokens) | Baseline rápido, varios tipos de doc |
| 2 | **Sliding Window** | Trozos fijos CON solapamiento definido | Preservar contexto entre límites (narrativa, docs técnicos) |
| 3 | **Semantic** | Agrupar por similitud semántica (embeddings/clustering) | Coherencia temática (papers, artículos) |
| 4 | **Document Structure** | Dividir por estructura (headers, párrafos, secciones) | Docs con estructura clara |
| 5 | **Hybrid** | Combinar varias (fixed + semantic) | Docs complejos, ningún método solo sirve |
| 6 | **Token-based + sentence boundaries** | Por tokens respetando límites de frase | Noticias, contenido usuario |
| 7 | **Custom-defined** | Reglas a medida (keywords, entidades de dominio) | Legal, médico |
| 8 | **Contextual Relevance** | ML clasifica relevancia por query (BERT) | IA conversacional, búsqueda personalizada |

## 🔴 Aplicación al LAB — VALOR MEDIO (validación + 2 insights)

| Ángulo | Veredicto |
|---|---|
| **Estrategia actual del lab** | 🟢 El lab usa **RecursiveCharacterTextSplitter (1000 chars, overlap 150)** = estrategia 2 (Sliding Window/Recursive) — YA implementa solapamiento para no perder contexto en los límites. Validado en disco: indexer.py línea 142-143 |
| **Semantic chunking** | 🟡 Futurible ligero: agrupar por similitud en vez de tamaño fijo — pero el lab YA tiene recall@5 100% y el corpus es markdown estructurado (cabeceras/secciones) → la ganancia sería marginal; señalar como referencia si el recall baja |
| **Hybrid chunking** | 🟡 El lab ya es híbrido de facto: RRF (FTS+vectorial) + Query/Summary indexing + reranker — el "hybrid" del post es de CHUNKING, no de retrieval; matiz conceptual |
| **Contextual Relevance (8)** | ⚪ El lab ya lo cubre con el reranker (bge-reranker-v2-m3 en CPU, daemon) — el post lo llama "chunking" pero es re-ranking |
| **Material BBK/TFM** | 🟢 Las 8 estrategias con la tabla = material excelente para entrevistas (BBK) y para el TFM (capítulo RAG: "qué chunking usa el lab y por qué") |

**Comentario relevante del post**: un usuario (ernestosalem) señala que el post "misses hybrid rag" — el lab YA lo tiene (RRF hybrid, validado). Coincidencia con el análisis.

**Conclusión**: VALOR MEDIO — valida la elección de chunking del lab (Recursive+overlap = la estrategia 2 recomendada para docs técnicos), da vocabulario académico para TFM/BBK y apunta 2 futuribles ligeros (semantic chunking y hybrid si el recall bajara — hoy no hace falta, recall@5 100%). Sin cambios.
