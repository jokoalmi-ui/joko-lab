---
title: "Análisis — Carrusel n8nstack: Deep Research y Research Loop (16-ago-2026)"
type: research
---

# Análisis — Carrusel n8nstack: Deep Research y Research Loop (16-ago-2026)

**Fuente:** https://www.instagram.com/p/DcH2aihE4ob/ (n8nstack | AI Automation, 16-ago-2026)
**Método:** browser_get_images (URLs completas) → descarga 2 slides 1440×1920 → GLM + browser_vision
**VERACIDAD:** [VERIFICADO]

## CONTENIDO (lo que dice)

### Slide 1 — "THE 5 PARTS BEHIND DEEP RESEARCH"
*A smart agent needs more than just a search.*

Diagrama: círculo central "RESEARCH AGENT" conectado a 5 partes:

| Parte | Función |
|---|---|
| 1. **PLANNER** | Desglosa la pregunta principal en subtareas claras y accionables |
| 2. **SEARCH TOOLS** | Busca en web, bases de datos y documentos las mejores fuentes |
| 3. **MEMORY** | Almacena contexto, fuentes y hallazgos — el agente no pierde el hilo |
| 4. **VERIFIER** | Comprueba hechos, evalúa fiabilidad — toda afirmación respaldada por fuentes reales |
| 5. **WRITER** | Convierte los insights validados en un informe final claro, estructurado y citado |

Mensajes: "Cuando estas 5 partes trabajan juntas obtienes insights más profundos,
no solo más datos" · "Better research. Better answers. Better decisions."

### Slide 2 — "DON'T SEARCH ONCE. LOOP."
*The agent keeps learning, finding gaps, and going deeper.*

Bucle de investigación iterativo (6 pasos):
1. **UNDERSTAND THE QUESTION** — analizar la pregunta y lo ya conocido
2. **CREATE RESEARCH QUERIES** — desglosar en consultas dirigidas (todos los ángulos)
3. **SEARCH MULTIPLE SOURCES** — fuentes diversas y fiables
4. **EXTRACT USEFUL INFORMATION** — leer, resumir, extraer insights
5. **IDENTIFY KNOWLEDGE GAPS** — comparar hallazgos, descubrir lo que falta
6. **SEARCH AGAIN** — refinar consultas y profundizar hasta cerrar brechas

Mensajes: "Iterate. Refine. Validate. That's how you go deep, not wide." ·
"More sources. Better insights. Stronger answers." · "Repeat until the answer is complete."

## FORMATO (cómo se ve)

- **Estilo**: póster vertical 4:5 (1440×1920), fondo oscuro con acentos vivos
- **Marca**: "n8n • AI AUTOMATION" arriba a la izquierda (badge), @n8nstack abajo
- **Slide 1**: diagrama radial (agente central + 5 nodos con icono y descripción)
- **Slide 2**: diagrama circular de bucle (6 pasos con flechas) centrado en "RESEARCH LOOP"
- **Iconos**: cada parte/paso con icono simple (lista, globo, base de datos, escudo, documento, lupa...)
- **Cierre**: 3 checkmarks ("More sources / Better insights / Stronger answers")

## Aplicación al LAB

| Concepto | Aplicación | Valor |
|---|---|---|
| **Deep Research = 5 partes (Planner/Search/Memory/Verifier/Writer)** | El lab tiene TODAS: enrutador (planner), RAG LanceDB (search/memory), gate de veracidad (verifier), skills (writer) | ✅ **VALIDA el diseño del lab** — es la misma arquitectura |
| **Research Loop iterativo (don't search once)** | El lab tiene el concepto: loop drift RAG (Q&A sintéticos) y el patrón RLM de Prime Agent (contexto como variable) | ✅ **Confirma la dirección** — el loop es el siguiente paso natural |
| **Verifier como parte del agente** | El gate de veracidad del lab (5 fases, 156 análisis) ES el verifier | ✅ VALIDA |
| **Formato visual** | Diagramas radiales/circulares de conceptos → reutilizables para slides del TFM | 🟡 Aislable |

## Veredicto
**APORTA/VALIDA.** El carrusel describe la arquitectura de deep research que el
lab ya implementa por piezas (planner=RAG+enrutador, verifier=gate de
veracidad, writer=skills de redacción, memory=LanceDB). La novedad conceptual
es el **"don't search once, loop"** — el loop iterativo de búsqueda hasta
cerrar brechas, que está en línea con el futurible de loop drift RAG ya
anotado. Nada que implementar nuevo hoy; refuerza la hoja de ruta.

**Nota de proceso:** el caption del JSON era null y el alt del feed describía
posts previos del canal — el tema real salió de las slides descargadas
(regla: frames/imágenes reales mandan, no alt/caption).
