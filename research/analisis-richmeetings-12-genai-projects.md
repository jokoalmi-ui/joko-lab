---
title: "Análisis — Carrusel richmeetings.ai: 12 GenAI Projects (17-ago-2026)"
type: research
---

# Análisis — Carrusel richmeetings.ai: 12 GenAI Projects (17-ago-2026)

**Fuente:** https://www.instagram.com/p/DcD_-5GkxQ6/ (richmeetings.ai, img_index=1)
**Método:** browser_get_images → descarga 2 slides (1440×1799) → GLM + browser_vision
**VERACIDAD:** [VERIFICADO]
**⚠️ CARRUSEL INCOMPLETO**: el post tiene 4 slides (indicador "1/4" y "2/4"); solo se descargaron 2 (img_index=1). Faltan 09-12.

## CONTENIDO (lo que dice)

### "12 GenAI PROJECTS Every Student & Professional Should Build" — BUILD PORTFOLIO-WORTHY AI PROJECTS

Metodología por proyecto: descripción + BEST AI (herramientas) + PRD PROMPT (prompt para generar el PRD completo).

| # | Proyecto | Qué hace | BEST AI |
|---|---|---|---|
| 01 | **AI Resume Builder** | CV para ATS, carta presentación, perfil LinkedIn | ChatGPT, Claude |
| 02 | **AI Portfolio Website** | Web personal con IA, sin código | ChatGPT, LavaLabs |
| 03 | **AI Study Assistant** | Notas → resúmenes, flashcards, quizzes, planes | Gemini, ChatGPT |
| 04 | **AI Research Assistant** | PDFs/artículos → resúmenes instantáneos | NotionLM, ChatGPT |
| 05 | **AI Meeting Assistant** | Graba, transcribe, resume reuniones con action items | ChatGPT, Claude |
| 06 | **AI Content Studio** | Blogs, posts sociales, scripts YouTube, LinkedIn | ChatGPT, Claude |
| 07 | **AI Data Dashboard** | Conecta datos, analiza, visualiza insights interactivos | Claude, ChatGPT |
| 08 | **AI Customer Support Bot** | Chatbot 24/7 con escalado a humano | ChatGPT, Gemini |

(09-12 en slides 3-4 no descargadas)

## FORMATO (cómo se ve)

- **Estilo**: carrusel vertical 1440×1799, 4 proyectos por slide
- **Cada proyecto**: icono circular numerado + descripción + BEST AI + PRD PROMPT en caja
- **Barras inferiores**: "SAVE THIS POST FOR LATER", "SMART PROMPTS • REAL RESULTS", "SWIPE LEFT FOR MORE"
- **Indicador de página**: 1/4, 2/4...

## Aplicación al LAB

| Proyecto | Relevancia LAB | Valor |
|---|---|---|
| **AI Meeting Assistant (05)** | **⚠️ CERCANO**: el lab ya transcribe (whisper local) y resume (vídeos, reuniones). La pieza que falta: action items + calendario | 🟡 **Ya casi lo tienes** — unificar transcripción+resumen+action items |
| **AI Research Assistant (04)** | **⚠️ CERCANO**: el lab ya resume PDFs (RAG LanceDB, ocr-and-documents) | 🟡 Ya cubierto por RAG local |
| **AI Content Studio (06)** | **⚠️ CERCANO**: el lab ya genera contenido (skills infografia-html, carruseles, vídeos) | 🟡 Ya cubierto |
| **AI Data Dashboard (07)** | Cercano: el lab tiene dashboards (LM Studio monitor, informes) | 🟡 Parcialmente cubierto |
| **AI Resume Builder (01)** | Relevante para empleo (LinkedIn, CV) | 🟢 Futurible útil — pero hay que verificar herramientas (ATS local vs SaaS) |
| **Metodología PRD PROMPT** | Interesante: prompt para generar PRDs completos | 🟡 Formato aislable |

## Veredicto
**INTERESANTE pero en su mayoría ya cubierto por el lab.** De los 8 proyectos
visibles, 4-5 son cosas que el lab YA hace (transcripción, RAG, contenido,
dashboards) con stack local. El patrón útil: **metodología PRD PROMPT** (pedir
a la IA el PRD completo antes de construir — evita construir a ciegas) — es un
patrón que el lab podría aplicar a sus futuribles. AI Resume Builder es el más
nuevo y relevante para el objetivo de empleo (pero verificar local-first:
ATS con datos locales vs SaaS).

⚠️ El post promociona herramientas cloud (ChatGPT, Claude, Gemini, LavaLabs,
NotionLM) — choca con el enfoque local-first del lab; los proyectos valen
como ideas, no como stack.
