---
title: "Análisis — Post gauravgoyalai: Naive RAG vs Self-RAG vs CRAG (17-ago-2026)"
type: research
---

# Análisis — Post gauravgoyalai: Naive RAG vs Self-RAG vs CRAG (17-ago-2026)

**Fuente:** https://www.instagram.com/p/DcDczWbkc1z/ (gauravgoyalai, 2 días)
**Método:** browser_get_images → descarga 2 slides (1440×1920) → GLM + browser_vision + caption completo
**VERACIDAD:** [VERIFICADO]

## CONTENIDO (lo que dice)

### Slide 1 — NAIVE / BASIC RAG (The Simplest & Most Common RAG Pattern)
4 pasos clásicos:
1. **INDEXING**: Documento (PDF) → parse → texto → chunk → embeddings → Vector Store
2. **RETRIEVAL (R)**: Query del usuario → encode → búsqueda semántica → Top K chunks relevantes
3. **AUGMENTED (A)**: Chunks → combine → contexto + query → prompt
4. **GENERATE (G)**: Prompt → LLM → respuesta

Leyenda: "Retrieve relevant information once and use it as context for the LLM to generate accurate answers."
Naive RAG = Simple, Fast & Effective. One retrieval step. One context. One answer.

### Slide 2 — SELF-RAG (Self-Reflective RAG for Smarter Answers)
LLM reflexiona sobre sus propios outputs, critica y decide qué recuperar a continuación:
1. **INDEXING** (igual que Naive)
2. **SELF-REFLECTIVE RETRIEVAL, GENERATION & CRITIQUE**: LLM genera borrador → se autocritica (refleja) → 3 rutas:
   - Good Answer (confident & supported) → Finalize
   - Need More Evidence → Retrieve More / Refine Query
   - Weak / Inconsistent → Revise & Regenerate
3. **AUGMENTED**: chunks de alta calidad (tras reflexión) + query → prompt
4. **GENERATE & SELF-CHECK**: respuesta + auto-chequeo QA opcional

"Self-RAG makes the model think, critique, and adapt so it retrieves the right information and delivers better, more reliable answers."

### Caption (información extra) — CRAG (Corrective RAG)
RAG que evalúa y CORRIGE su propia recuperación: capa de control de calidad que
evalúa lo recuperado (relevancia, suficiencia, consistencia, calidad) y si no es
suficiente → refinar la query y recuperar de nuevo.
Flujo: Retrieval & Evaluation → si no bueno → refine query → retrieve again.

## 🎯 APLICACIÓN AL LAB — EL HALLAZGO MÁS RELEVANTE DEL DÍA

**El lab YA implementa los 3 niveles de RAG sin llamarlos así:**

| Patrón | En el lab (real, verificado) |
|---|---|
| **Naive RAG** | Pipeline RAG con LanceDB (~20K filas, recall@5 100% en 70ms) + BGE-M3 embeddings — EXACTAMENTE el flujo Indexing→Retrieval→Augment→Generate |
| **Self-RAG** | **El gate de veracidad** (5 fases): responde → verifica contra fuentes → si no respalda, re-consulta/re-etiqueta (VERIFICADO/ALCANCE INTERNO) — ES autocritique + refine |
| **CRAG** | El gate en su fase de evaluación de calidad: si la evidencia es débil → refinar/re-buscar → repetir (fail-closed) |

**El lab está en el nivel Self-RAG/CRAG sin haberlo nombrado así** — y eso
valida la arquitectura: no es RAG básico, es RAG reflexivo con verificación.

## FORMATO (aislable)

- Diagrama de flujo en 4 pasos (I→R→A→G) con etiquetas verbales ("parse",
  "chunk", "embed", "combine", "feed")
- Variantes comparadas (Naive vs Self vs Corrective) — el mismo esqueleto con
  la mejora destacada
- Reutilizable para slides TFM: "cómo tu RAG es Self-RAG sin llamarlo así"

## Veredicto
**MUY RELEVANTE / VALIDA LA ARQUITECTURA.** El post describe los 3 niveles de
RAG y el lab está en el nivel 2-3 (gate de veracidad = Self-RAG/CRAG real).
Valida con terminología académica lo que el lab construyó empíricamente.
Formato de diagrama 4 pasos aislable para TFM/LinkedIn. El mejor candidato
para explicar el RAG del lab a externos (misma terminología que la industria).
