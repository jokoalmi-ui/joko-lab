---
title: "Análisis — 12 AI Skills carrusel (alamin.8020ai, 22-ago-2026)"
type: research
---

# Análisis — 12 AI Skills carrusel (alamin.8020ai, 22-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcQYcOdEaR3/ (alamin.8020ai, 20-08-2026, 157 likes / 53 comentarios)
**Método:** caption + **TODAS las 12 imágenes del carrusel extraídas** (navegación img_index 3-13, texto de cada slide vía alt del DOM)

## ⚠️ CORRECCIÓN AL ANÁLISIS INICIAL
El primer análisis lo descartó como "engagement bait sin contenido" basándome SOLO en el caption. **El usuario tenía razón**: el carrusel contiene las 12 skills detalladas con herramientas y recursos de aprendizaje. El bait (Comment LIST) es solo la capa de engagement; el contenido real está en las imágenes.

## LAS 12 SKILLS (contenido real del carrusel)

| # | Skill | Qué es | Herramientas | Recursos |
|---|---|---|---|---|
| 1 | **Prompt Engineering** | Convertir respuestas genéricas de IA en insights estratégicos | ChatGPT, Gemini, Claude, Perplexity | DeepLearning.AI, Anthropic Docs |
| 2 | **Workflow Automation** | Sistemas donde la IA ejecuta flujos conectando tools/datos/acciones | Zapier, Make, Bardeen | Zapier University, N8N, Make Academy |
| 3 | **AI Agents** | Sistemas autónomos que planifican, razonan y ejecutan tareas multi-paso | CrewAI, AutoGen | LangChain Docs, AutoGen Cookbook, LangGraph |
| 4 | **RAG** | IA que trabaja sobre tus datos y razona desde conocimiento real | LlamaIndex, LangChain, Vectara, Haystack | LlamaIndex Docs, Haystack Tutorials, Vectara Academy |
| 5 | **Multimodal AI** | Modelos que entienden texto, imágenes, código, audio como un stream conectado | ChatGPT, Gemini, Claude, Grok | OpenAI Guides, Google AI Studio, Anthropic |
| 6 | **Fine-Tuning & AI Assistants** | Expertos de IA especializados en tu dominio | OpenAI, Hugging Face | HF Hub, Cohere Academy, NVIDIA AI Foundations |
| 7 | **Voice AI & Avatars** | Ideas → voz y presencia de vídeo realista a escala | ElevenLabs, HeyGen, Synthesia, VAPI | ElevenLabs KB, HeyGen Academy |
| 8 | **AI Stacking** | Ecosistema donde múltiples herramientas IA trabajan como equipo coordinado | Notion, ClickUp, Asana, Zapier | Notion Academy, ClickUp University |
| 9 | **AI Video Content Generation** | Creación de vídeo IA: estrategia → contenido listo para publicar | Runway, Veed, Opus, OpenAI Sora | Runway Learn, VEED Academy |
| 10 | **AI-Powered SaaS Development** | Productos donde la IA es parte de la lógica de negocio desde el día 1 | Bubble, Lovable, Cursor, Windsurf | Bubble Academy, Lovable Docs, Cursor Guides |
| 11 | **LLM Management** | Monitorizar precisión, coste, latencia y fiabilidad de los LLM | PromptLayer, Helicone, TruLens, Phoenix | Helicone Docs, TruLens Guides, PromptLayer Docs |
| 12 | **Staying Updated** | Hábito de seguir avances, tools y cambios de la industria | The Verge, TechCrunch, VentureBeat, MIT Tech Review | — |

## 🔴 Para el LAB — VALOR REVISADO: MEDIO-ALTO (el lab cubre 11/12)

| Skill | En el lab | Detalle |
|---|---|---|
| 1. Prompt Engineering | ✅ | skill prompt-engineering propia |
| 2. Workflow Automation | ✅ | 33 crons + n8n + MCPs |
| 3. AI Agents | ✅ | Hermes (el agente más completo de la lista) |
| 4. RAG | ✅ | LanceDB + bge-m3 + joko-indexer (MEJOR que las tools listadas para el caso local) |
| 5. Multimodal | ✅ | GLM visión + LFM VL + audio |
| 6. Fine-Tuning | ⚪ | Futurible ya anotado (LoRA de LFM si hace falta) |
| 7. Voice AI | ✅ | edge-tts (voz local en fichas) |
| 8. AI Stacking | ✅ | Hermes + MCPs + crons = ecosistema coordinado |
| 9. Video Content | ✅ | gen_video_corto.sh + Manim + ficha animada |
| 10. SaaS Dev | ⚪ | No aplica hoy (no se construye producto SaaS) |
| 11. **LLM Management** | ✅ | **Observabilidad proxy :9911 + llm_as_judge + telemetría — EXACTAMENTE esto** |
| 12. Staying Updated | ✅ | Crons de vigilancia IG/YT + watchdogs |

**Hallazgo importante**: la skill #11 (LLM Management con PromptLayer/Helicone/TruLens) es **exactamente lo que el lab ya hace** con el proxy :9911 + llm_as_judge — validación directa.

**Conclusión corregida**: no era "bait vacío" — el contenido real del carrusel es una lista sólida de skills de IA, y el lab cubre 11/12 (solo falta #10 SaaS, que no aplica). Sin futuribles nuevos, pero el análisis queda corregido con el contenido real de las 12 imágenes.
