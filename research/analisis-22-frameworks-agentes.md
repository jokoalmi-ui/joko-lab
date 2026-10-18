---
title: "Análisis — Reel: 22 AI Agent Frameworks (shiva.bytes, 6s)"
type: research
---

# Análisis — Reel: 22 AI Agent Frameworks (shiva.bytes, 6s)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 09-ago-2026
**Fuente:** https://www.instagram.com/reel/Db0tiQ6lEDU/ — shiva.bytes (Sivasankar Natarajan)
**Método:** Descarga vídeo MP4 (6s) + extracción frames + GLM 4.6V local

---

## Los 22 frameworks

CrewAI, LangGraph, OpenAI Agents SDK, AutoGen, LangChain Agents, Microsoft
ADK, Google ADK, SmolAgents, CamelAI, Agno, LlamaIndex, PydanticAI,
OpenDevin, MetaGPT, ChatDev, SuperAGI, Langroid, Atomic Agents, Mastra,
Haystack Agents, Relevance AI, Zapier AI Actions.

(Columnas del reel: Framework | Integración/Fuente de Datos | Uso)

---

## 🎯 Aplicación al LAB

### El lab NO usa ninguno de estos frameworks (y es correcto)

| Aspecto | Lab |
|---|---|
| **Frameworks de agentes** | ❌ No usa — arquitectura propia (Hermes + scripts + file bus) |
| **Orquestación** | Hermes (orquestador) + scripts gobernados + OpenCode (worker #1) |
| **Por qué es correcto** | El lab es UN agente con pipeline propio; no necesita un framework multi-agente |

### Lo relevante (conecta con el backlog)

1. **LangGraph y CrewAI** — ya aparecen en el backlog como referencia para el
   **ESTUDIO AUTOBOTS** (F3/F4 del L2): "Comparar con: crewAI (crews), LangGraph
   (grafos estado)". Este reel los incluye → confirma que están en el radar.

2. **Agno** — aparece en el backlog como "estudio agentes OSS futuro (Browser
   Use, CrewAI, Agno, LangGraph, Dify)". Aquí se confirma como framework vivo.

3. **OpenAI Agents SDK / AutoGen / Microsoft ADK / Google ADK** — los SDKs de
   los grandes; útiles solo como referencia comparativa (el lab es agnóstico).

4. **Zapier AI Actions** — el único "no-framework" de la lista (automatización
   low-code, tipo n8n que el lab ya tiene).

### Veredicto honesto

**El reel es un inventario de frameworks, no una recomendación.**
Para el lab: NO hay nada accionable nuevo — la decisión de arquitectura propia
se mantiene. Los únicos que conectan con pendientes existentes son LangGraph,
CrewAI y Agno (ya en el backlog como referencias del estudio de agentes).

**Sin backlog nuevo.** El material puede servir para el TFM si se quiere
mostrar el panorama de frameworks y por qué el lab eligió arquitectura propia.

## Nota

Canal shiva.bytes (Sivasankar Natarajan) — el mismo de la infografía
"7 Types of AI Agent Memory" analizada antes (09-ago).
