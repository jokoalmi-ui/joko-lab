---
title: "Análisis — Póster: 9 MCP Projects for AI Engineers (Brij Kishore Pandey)"
type: research
---

# Análisis — Póster: 9 MCP Projects for AI Engineers (Brij Kishore Pandey)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 06-ago-2026
**Fuente:** https://www.instagram.com/p/DbvKeEDCPTn/ — codewithbrij (Brij Kishore Pandey)
**Método:** Descarga imagen única (1611×1536) + análisis GLM 4.6V local
**Imagen:** /tmp/brij_post.jpg (temporal)

---

## Los 9 proyectos MCP

| # | Proyecto | Stack |
|---|---|---|
| 1 | **Multi-Agent Deep Researcher** | Web Search Agent + Analyst + Writer; Linkup |
| 2 | **Synthetic Data Generator (MCP Server)** | Cursor IDE + SDV (Synthetic Data Vault) |
| 3 | **MCP Client 100% local y privado** | LlamaIndex + Ollama + DeepSeek-R1 |
| 4 | **Agentic RAG con MCP** | Cursor + Qdrant + Bright |
| 5 | **RAG sobre docs complejos reales** | Cursor + EYELEVEL |
| 6 | **Financial Analyst con MCP** | CrewAI + Cursor + DeepSeek |
| 7 | **Voice Agent con Qwen3** | AssemblyAI (STT) + Claude (LLM) |
| 8 | **Unified MCP Server con MindsDB** | MySQL + MindsDB + Claude |
| 9 | **Memoria integrada Cursor + Claude Desktop** | Cursor IDE + Zep + Graphiti |

## 🔗 Relevancia para el LAB

**MCP (Model Context Protocol)** es el estándar que conecta agentes a herramientas.
El lab ya usa herramientas de Hermes (terminal, file, web) — MCP es una vía
alternativa/complementaria para exponer capacidades.

**Los más interesantes para el lab:**

| Proyecto | Por qué |
|---|---|
| #3 MCP Client local (Ollama + LlamaIndex) | Coincide con el stack local del lab (LM Studio/Ollama) |
| #4 Agentic RAG con Qdrant | El lab tiene RAG propio — Qdrant es alternativa a LanceDB |
| #9 Memoria integrada (Zep + Graphiti) | **Conecta con el gap de Prospective Memory** (memoria de agentes) |
| #1 Multi-Agent Researcher | El lab delega investigación — patrón similar |
| #7 Voice Agent | El lab ya tiene dictado por voz (Whisper local) |

**No prioritarios:** #2 (SDV datos sintéticos), #6 (financiero), #8 (MindsDB/MySQL).

## Veredicto

Póster de referencia: 9 proyectos MCP con stack variado. Para el lab: **los
proyectos #3 (MCP local), #4 (agentic RAG) y #9 (memoria persistente)** son los
más alineados con la arquitectura actual. El #9 refuerza la idea de formalizar
la memoria de agente (file bus → Zep/Graphiti como estudio).

Anotado en backlog como **PROYECTOS FUTUROS** (grupo) para estudio individual.
