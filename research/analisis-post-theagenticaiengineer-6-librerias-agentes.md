---
title: "Análisis — Post: 6 most used AI agent libraries (TheAgenticAIEngineer, 01-nov-2026)"
type: research
---

# Análisis — Post: «6 Most Used AI Agent Libraries» (TheAgenticAIEngineer)

**VERACIDAD:** [VERIFICADO]
**Fecha del análisis:** 01-11-2026
**Fuente:** https://www.instagram.com/p/DfNj9uyhDDd/ — `theagenticaiengineer`, publicado 1-nov-2026
**Método:** `yt-dlp --dump-json` (descartó vídeo) + `og:title`/`og:description` (doble vía) + descarga de la imagen (curl con UA, 307.691 B) + lectura con `google/gemma-4-12b-qat` (ctx 8192, carga 6,45 s) vía LM Studio headless `:99`
**Veredicto:** **SIN ENTRADA EN EL LAB** — material ya cubierto, sin datos medidos ni recurso nuevo

---

## Qué es

Infografía estática (imagen única, **1184×1568**, `JPEG` 307.691 B) con una rejilla 2×3 de tarjetas. No es vídeo: `yt-dlp` devuelve `ERROR: [Instagram] DfNj9uyhDDd: There is no video in this post`.

- **Título en la imagen:** `AI AGENTS — 6 MOST USED LIBRARIES` · `@TheAgenticAIEngineer`
- **Likes/comentarios:** `no aparece en la salida` (el `og:description` de este post no los incluye)
- **Nº de slides:** no hay indicador de carrusel ni JSON con `carousel_media`; se trata como imagen única. Si hubiera más, `no aparece en la salida`.

## Transcripción literal del póster

```
AI AGENTS
6 MOST USED LIBRARIES
@TheAgenticAIEngineer

1  LangChain
   Build LLM apps with chains, tools, memory and integrations.
   - Connect LLMs with tools, APIs and external data.
   - Build chains and agents.
   - Memory for conversation history.
   - Integrations with vector DBs, databases and other services.
   - Easy to build RAG applications.
   - Large community and ecosystem.

2  LangGraph
   Build stateful, multi-step agents with graph workflows.
   - Create agent workflows using graphs.
   - Manage state, memory and checkpoints.
   - Support for multi-agent systems.
   - Handle complex, conditional flows.
   - Built on top of LangChain.
   - Ideal for production-grade agent workflows.

3  CrewAI
   Create and manage collaborative multi-agent teams easily.
   - Build role-based agents (e.g., researcher, analyst, writer).
   - Execute complex tasks with agent teams.
   - Simple and easy-to-use API.
   - Built-in support for tools and memory.
   - Great for real-world multi-agent use cases.
   - Active development and growing community.

4  AutoGen
   Enable AI agents to converse, collaborate and automate tasks.
   - Build conversational multi-agent systems.
   - Agents can chat, plan and solve tasks together.
   - Support for human-in-the-loop.
   - Integrate tools, code execution and APIs.
   - Useful for research, data analysis and automation.
   - Developed by Microsoft, production-ready and widely used.

5  LlamaIndex
   Connect LLMs with your data for RAG, search and retrieval.
   - Easy data loading from multiple sources (PDF, websites, DBs, etc.).
   - Create indexes for efficient retrieval.
   - Support for different vector stores.
   - Built-in query engines and RAG pipelines.
   - Integrate with LangChain and other frameworks.
   - Great for document Q&A and enterprise knowledge search.

6  Semantic Kernel
   Build enterprise-ready AI apps with plugins, memory and planning.
   - Connect LLMs with tools and plugins (Function calling).
   - Built-in support for memory and skills.
   - Plan and execute complex tasks with step-by-step reasoning.
   - Works with multiple LLMs (OpenAI, Azure OpenAI, etc.).
   - Strong support for C#, Python and Java.
   - Ideal for enterprise and production use cases.

These libraries help you build smarter, more capable and autonomous AI agents.
```

## Cruce con el lab

| Término | Ficheros que lo mencionan en `joko-lab` |
|---|---|
| LangChain | 290 |
| AutoGen | 293 |
| LangGraph | 236 |
| CrewAI | 193 |
| LlamaIndex | 183 |
| Semantic Kernel | 108 |

- **Ya analizado con más alcance:** `research/analisis-22-frameworks-agentes.md` (09-ago-2026, `[VERIFICADO]`, reel de `shiva.bytes`) — 22 frameworks, 5 de estos 6 incluidos (falta Semantic Kernel), y con una conclusión que este post no tiene: **el lab no usa ninguno y es correcto**, porque Hermes + skills + delegación cubre el caso sin esas dependencias.
- **El canal ya aparecía** en el lab (backlog), no es fuente nueva.

## Claims no verificados

- **«6 most used»** — el ranking no cita fuente, método ni fecha de medición. Es un claim, no un dato.
- **«Enterprise» / «production-grade»** — adjetivos en AutoGen y Semantic Kernel; ninguna característica medible detrás.
- **Tres de los seis no son independientes:** el propio póster dice que LangGraph va «built on top of LangChain» y que LlamaIndex «integrate[s] with LangChain and other frameworks». Presentarlos como seis opciones paralelas induce a error en la elección.

## Lo aprovechable (editorial, no técnico)

- Ángulo para la serie LinkedIn de IA/agentes: **el orden de aprendizaje que propone el post (empezar por LangChain) es el más caro para un agente simple**. El gancho contrario — «los frameworks se cambian, el criterio no» — es defendible con la evidencia del lab (22 frameworks inventariados, ninguno adoptado).
- Nada de esto requiere escribir en el lab ni cambiar nada: es material de post, no de arquitectura.

## Estado del lab tras el análisis

LM Studio headless en `:99`, `:1234` en `200`, gemma cargado 6,45 s para leer el póster y **descargado** después; GPU **106 MiB**, cero modelos en VRAM.
