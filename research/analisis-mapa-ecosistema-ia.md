---
title: "Análisis — Mapa del ecosistema IA (marketingwithgaurav)"
type: research
---

# Análisis — Mapa del ecosistema IA (marketingwithgaurav)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 06-ago-2026
**Fuente:** https://www.instagram.com/p/DblEQFUNEPs/ — marketingwithgaurav (Gaurav Sharma)
**Método:** Descarga imagen (1440×1920) + análisis GLM 4.6V local

---

## Qué es

**Mapa visual del ecosistema de herramientas de IA** ("AI Map") — guía categorizada
de las herramientas clave para desarrolladores/builders. No es comparativa con
métricas: es organización lógica por categoría con iconos y colores.

## Las 11 categorías con herramientas (transcripción GLM)

| # | Categoría | Herramientas |
|---|---|---|
| 1 | **LLM** | ChatGPT, Claude, Gemini, Grok, DeepSeek |
| 2 | **Agentic AI** | LangGraph, CrewAI, AutoGen, OpenAI Agents SDK, Agno |
| 3 | **RAG** | LangChain, LlamaIndex, Haystack, RagFlow, GraphRAG |
| 4 | **Embeddings** | OpenAI, Voyage AI, Cohere, Jina AI, BAAI BGE |
| 5 | **MCP** | Anthropic MCP, OpenAI MCP, Cloudflare MCP, Composio MCP, Zapier MCP |
| 6 | **AI Security** | Lakera, Protect AI, HiddenLayer, Promptfoo, Robust Intelligence |
| 7 | **Observability** | LangSmith, Langfuse, Helicone, Arize AI, Weights & Biases |
| 8 | **Memory** | Mem0, Zep, Letta, LangMem, Cognee |
| 9 | **AI Agents** | (categoría cortada en el análisis — ver nota) |
| 10 | **Automation** | n8n, Zapier, Make, Pipedream, Activepieces |
| 11 | **Vector DB** | Pinecone, Weaviate, Qdrant, Milvus, Chroma |

## 🔗 Aplicación al LAB (lo importante)

| Categoría | El lab usa | Estado |
|---|---|---|
| **LLM** | DeepSeek (cloud) + Dolphin 8B + GLM (local) | ✅ 3 de las 5 (ChatGPT/Claude/Gemini no — por local-first) |
| **Agentic AI** | Hermes (delegación) — LangGraph/CrewAI anotados como estudio | 🟡 Hermes es el framework, no LangGraph |
| **RAG** | LanceDB + BGE-M3 + reranker (stack PROPIO, no LangChain) | ✅ Diferente pero equivalente |
| **Embeddings** | **BAAI BGE** (el mapa lo lista!) | ✅ **Validación externa de la elección** |
| **MCP** | Interés anotado (MCP de modelos) | 🟡 Pendiente de evaluar |
| **AI Security** | Promptfoo podría interesar (evaluación de prompts) | 🟡 Candidato |
| **Observability** | Langfuse/LangSmith | 🟡 El lab tiene F4 propio (telemetría) — Langfuse sería alternativa |
| **Memory** | Mem0/Zep | 🟡 El lab tiene memoria propia (file bus, ledger, RAG) |
| **Automation** | **n8n** (el mapa lo lista!) | ✅ **Validación externa** |
| **Vector DB** | LanceDB | ✅ Alternativa válida a las 5 listadas (LanceDB no está en el mapa) |

### 🎯 Los 3 datos que valen la pena

1. **BAAI BGE está en el mapa de embeddings** — el lab usa BGE-M3: elección validada externamente
2. **n8n está en el mapa de automatización** — el lab ya lo usa: validado
3. **LanceDB no aparece** (el mapa lista Pinecone/Weaviate/Qdrant/Milvus/Chroma) — pero LanceDB es una alternativa sólida para local (el mapa es orientado a cloud/SaaS)

### 🟡 Candidatos nuevos que el mapa sugiere

- **Promptfoo** (AI Security) → evaluación/adversario de prompts — conecta con el verifier
- **Langfuse** (Observability) → alternativa al F4 propio
- **Mem0/Zep** (Memory) → comparar con el file bus del lab

## Veredicto

Mapa útil como **inventario del ecosistema** (11 categorías × 5 herramientas).
Para el lab: **valida 2 decisiones** (BGE-M3, n8n) y sugiere 3 candidatos a
estudio (Promptfoo, Langfuse, Mem0/Zep). El stack del lab está bien posicionado:
usa alternativas locales propias donde el mapa lista opciones cloud.

**Nota:** la categoría 9 "AI Agents" quedó cortada en la transcripción (GLM la
dio parcial). El resto está completo.
