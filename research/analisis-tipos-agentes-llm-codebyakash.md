---
title: "Análisis — Tipos de LLM Agents (codeby.akash, 16-ago-2026)"
type: research
---

# Análisis — Tipos de LLM Agents (codeby.akash, 16-ago-2026)

**Fuente:** https://www.instagram.com/reel/DcGgRUOhHIR/ (codeby.akash, 10s, infografía animada)
**Transcripción audio:** solo "¡Suscríbete!" (reel sin voz explicativa — contenido 100% visual)
**Frames:** 3 (scdet) analizados con GLM-4.6V-Flash
**VERACIDAD:** [VERIFICADO]

## Qué es (resumen)

Infografía animada que clasifica los 6 tipos de agentes LLM según cómo
piensan, actúan y colaboran. Es contenido educativo de divulgación IA
(patrón típico del canal codeby.akash).

## Los 6 tipos de agentes (contenido del reel, transcrito por GLM)

| # | Tipo | Cómo funciona | Ejemplo |
|---|---|---|---|
| 1 | **Reactive Agent** | Responde al input actual: Prompt → Event Trigger → Quick Response → Single Action (Input → Response) | Responder una pregunta simple |
| 2 | **Planning Agent** | Divide metas en pasos: Goal → Plan → Tasks → Milestone (Goal → Plan → Execute) | Planificar un informe de investigación |
| 3 | **Tool-Using Agent** | Usa herramientas externas: Reason → Choose Tool → Act (Web Search, API, DB, Calculator, Code, File System) | Buscar, calcular y resumir |
| 4 | **Memory-Enabled Agent** | Recuerda interacciones pasadas: New Input → Retrieve from Memory → Context-Aware Response (Input → Recall → Reason → Respond) | Continuar una conversación |
| 5 | **Evaluator Agent** | Evalúa outputs y da feedback: Model Output → Evaluate → Feedback & Critique → Improve | Revisar y mejorar respuestas |
| 6 | **Multi-Agent System** | Varios agentes colaboran: Coordinator, Research, Analysis, Writer → Final Result (Collaborate → Share → Solve → Deliver) | Investigar, analizar y escribir un informe |

Mensaje de cierre: "LLM agents come in different types, each designed for
unique tasks. Choose the right agent, or combine them, to build powerful AI
solutions!"

## Estilo visual (para posible replicación)

- 6 secciones con código de color: azul, morado, naranja, teal, verde, rojo.
- Layout radial: icono central (cerebro/robot) con flechas a cada tipo.
- Títulos en negrita grande, cajas de ejemplo con fondo de color, iconos simples.
- Formato: infografía animada 720×1280 (vertical, reel).

## Relevancia para el LAB

| Punto | Aplicación |
|---|---|
| ⭐ **Taxonomía de agentes** | Marco útil para documentar/diseñar los agentes del lab (Hermes, subagentes, crons): clasificar qué tipo es cada uno |
| **Multi-Agent System** | Valida el patrón de delegación del lab (delegate_task, subagentes) — es el tipo 6 en producción |
| **Memory-Enabled** | Corresponde al RAG/persistencia del lab (LanceDB, skills, memoria) |
| **Tool-Using** | Es Hermes con sus toolsets (terminal, web, browser) — validación externa del diseño |
| **Contenido educativo** | Material potencial para LinkedIn Lab (carrusel sobre tipos de agentes) — el lab tiene pipeline de carruseles |

## Veredicto

**Útil como marco conceptual, no como acción inmediata.** El reel no aporta
nada nuevo que el lab no tenga ya implementado (sus agentes combinan los
tipos 3, 4 y 6), pero la taxonomía es clara y didáctica — sirve como
referencia para documentar la arquitectura de agentes del lab y como
material educativo para la marca personal (LinkedIn).

## Futuribles (registrar)

1. **Documentar los agentes del lab con esta taxonomía** (Hermes = Tool-Using +
   Memory + Multi-Agent; subagentes = Multi-Agent) — en GUIA-JOKO-LAB o research
2. **Carrusel LinkedIn "6 tipos de agentes LLM"** con el pipeline del lab
   (plantilla maurys) — contenido educativo para marca personal
