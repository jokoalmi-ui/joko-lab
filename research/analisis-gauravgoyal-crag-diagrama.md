---
title: "Análisis — Reel gauravgoyalai: CRAG (Corrective RAG) diagrama completo (17-ago-2026)"
type: research
---

# Análisis — Reel gauravgoyalai: CRAG (Corrective RAG) diagrama completo (17-ago-2026)

**Fuente:** https://www.instagram.com/reel/DcKk7gXxxtf/ (gauravgoyalai, 10.1s, vertical 720×1280)
**Método:** fetch navegador (MP4 348 KB) → scdet 2 frames (misma infografía animada) → GLM + browser_vision
**VERACIDAD:** [VERIFICADO]

## CONTENIDO (lo que dice)

### "CRAG (CORRECTIVE RAG) — Advanced Retrieval with Quality Control"

**1. INDEXING**: Documento (PDF) → parse → Text → Chunks → Embedding Model → Vector Store

**2. RETRIEVAL & EVALUATION (CORE OF CRAG)**: query → embedding → top K candidates → **evaluar calidad de lo recuperado**:
- 🟢 **Good Enough** → usa estos → paso 3
- 🟡 **Need More Info** → recupera más / refina query
- 🔴 **Not Good / Inconsistent** → cambia enfoque y reintenta

**3. AUGMENTED**: top N chunks relevantes + contexto de calidad + query → prompt

**4. GENERATE**: prompt → LLM → respuesta acurada, con auto-check opcional (QA)

Frase clave: "CRAG ensures the system retrieves the right information, fixes
what's missing or wrong, and delivers accurate, trustworthy answers."

## 🎯 APLICACIÓN AL LAB — COMPLEMENTA EL POST DE ANTES + VALIDA EL GATE

Este reel es la **versión diagrama del post gauravgoyalai analizado antes**
(Naive RAG vs Self-RAG vs CRAG — `research/analisis-gauravgoyal-rag-levels.md`).
Ahora tenemos el flujo completo del nivel CRAG.

| Paso CRAG | En el lab (real, verificado) |
|---|---|
| **Indexing** | LanceDB + BGE-M3 (~20K filas, recall@5 100%, 70ms) |
| **Retrieval & EVALUATION** | **El gate de veracidad = el core de CRAG**: evalúa la evidencia y decide VERIFICADO / ALCANCE INTERNO / REVISAR |
| **Good Enough → usar** | Respuesta [VERIFICADO] con fuente |
| **Need More Info → refinar** | El gate re-consulta o re-etiqueta (ALCANCE INTERNO) |
| **Not Good → reintentar** | Fail-closed / re-verificación (gate 5 fases) |
| **Generate con auto-check** | Juez LLM (glm-4.6v-flash, intentos=2) |

**Conclusión del par gauravgoyalai (post + reel):** el lab implementa **los 3
niveles RAG** — Naive (pipeline base), Self-RAG (el modelo se autocritica) y
**CRAG (el gate evalúa y corrige la recuperación)** — sin llamarlos así. La
terminología académica del par valida el diseño del gate de veracidad, que es
exactamente el "Retrieval & Evaluation" del diagrama CRAG.

## FORMATO (aislable)

- Diagrama de flujo con semáforo de evaluación (verde/amarillo/rojo) — patrón
  de control de calidad visual reutilizable para el TFM ("así funciona el
  gate de veracidad")

## Veredicto
**MUY RELEVANTE / VALIDA EL GATE DE VERACIDAD.** El diagrama CRAG es la
formalización académica del gate de veracidad del lab: evalúa la calidad de
lo recuperado (Good Enough / Need More Info / Not Good) y toma acción
correctiva. Par gauravgoyalai completo (post + reel): el lab está en nivel
Naive + Self + CRAG. Material directo para explicar el gate a externos.
**Nota proceso**: reel corto (10.1s, 2 escenas), audio solo música (whisper
inútil — patrón del día), GLM + browser_vision OK con GLM cargado.
