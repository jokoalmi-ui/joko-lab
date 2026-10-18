---
title: "Análisis — RAG Developer Stack cheat sheet (GauravGoyalAI, 21-ago-2026)"
type: research
---

# Análisis — RAG Developer Stack cheat sheet (GauravGoyalAI, 21-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/reel/DcQqD6MRHc7/ (gauravgoyalai, 20-08-2026, 24 likes)
**Método:** caption íntegro extraído (browser_console)

## Contenido
Cheatsheet del stack para RAG en producción ("RAG es más que una vector DB"):

| Capa | Herramientas del post | En el LAB |
|---|---|---|
| Frameworks | LangChain, LlamaIndex, Haystack | ❌ NO — el lab usa joko-indexer + Hermes nativo (a propósito: menos dependencias) |
| Vector Stores | Pinecone, Qdrant, Weaviate, Milvus | ✅ **LanceDB local** (gratis, sin servidor, ~21.5K filas, recall@5 100%) |
| Data Extraction | Crawl4AI, Firecrawl, ScrapeGraphAI | ✅ yt-dlp + urllib + web_extract (patrón validado) |
| Open LLMs | Llama, Mistral, Qwen, DeepSeek | ✅ LFM, gpt-oss, GLM, Gemma (locales) |
| Embeddings | BGE, E5, Cohere, Jina | ✅ **bge-m3** (local) |
| Evaluation | Ragas, DeepEval, TruLens, Giskard | ✅ evaluar_rag.py + adversarial + batería PRODUCCIÓN |

**Takeaway del post**: *"Better data + better retrieval + continuous evaluation = better RAG"* — la MISMA filosofía del lab (evaluación continua, nunca asumir).

## 🔴 Para el LAB — VALOR: MEDIO-ALTO (validación del stack propio)

| Aspecto | Análisis |
|---|---|
| ¿Algo que copiar? | ⚪ Las herramientas de evaluación del post (Ragas/DeepEval) podrían compararse con evaluar_rag.py en un futuro — pero el lab ya mide recall@5 100% + adversarial |
| ¿El lab está al día? | ✅ Sí — cubre TODAS las capas con herramientas locales y gratuitas |
| ¿Futurible? | ⚪ F9 posible: comparar métricas de Ragas/DeepEval vs evaluar_rag.py cuando haya un dataset de evaluación más grande — señal débil |

**Conclusión**: validación externa fuerte del stack RAG del lab. La frase clave coincide con la regla del lab: datos mejores + recuperación mejor + evaluación continua. El lab no usa frameworks pesados (decisión correcta para 12 GB / local-first).
