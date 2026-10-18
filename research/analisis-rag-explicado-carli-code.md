---
title: "Análisis — RAG explicado (carli.code, 15-ago-2026)"
type: research
---

# Análisis — RAG explicado (carli.code, 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcCox1AjQz-/ (carrusel 10 slides)
**Autor:** carli.code
**Método:** 10/10 slides descargadas del CDN + GLM-4.6V-Flash local (2 pasadas;
slides 1, 5-9 requirieron re-análisis individual con prompt firme anti-reasoning)

---

## Contenido del carrusel (RAG explicado en español, formato didáctico)

| Slide | Contenido |
|---|---|
| 1 | ¿Qué es RAG y por qué todo el mundo lo usa? (primero fácil, después técnico) |
| 2 | Analogía estudiante: **examen a libro cerrado** = LLM sin RAG (responde solo con lo memorizado, info desactualizada) |
| 3 | **Examen a libro abierto** = RAG (busca en la biblioteca información actualizada antes de responder) |
| 4 | Definición técnica: busca info relevante en fuentes externas → la añade al contexto del modelo |
| 5 | ¿Por qué existe RAG? 3 problemas del LLM: conocimiento congelado en entrenamiento, no conoce datos privados, alucina cuando no sabe. **RAG resuelve los 3 sin reentrenar** |
| 6 | Componentes clave: **embeddings** (texto → vectores numéricos) + **vector database** (almacena y busca los similares) — Pinecone, Weaviate, pgvector |
| 7 | (pipeline diagrama — no extraído con claridad) |
| 8 | **RAG vs fine-tuning**: FT cambia comportamiento/estilo reentrenando; RAG da info actualizada sin tocar pesos. No excluyentes; RAG más rápido de implementar y mantener |
| 9 | Errores comunes: mala calidad de chunking, embeddings poco relevantes, demasiado contexto irrelevante |
| 10 | **RAG no aumenta la inteligencia del modelo, lo hace mejor informado** (libro abierto + lupa + check) |

---

## Veredicto

### ✅ VALIDA el lab — el carrusel describe EXACTAMENTE el RAG del lab

| Idea del carrusel | Implementación REAL en el lab |
|---|---|
| Embeddings (texto → vectores) | **BGE-M3** (multilingüe, mejor que BGE-small del carrusel) |
| Vector database | **LanceDB** híbrido (FTS + IVF_HNSW + RRF) — 19.894 filas, recall@5 100% |
| RAG sin tocar pesos | El lab NO fine-tunea (decisión 05-ago, confirmada 3×) — exactamente esta filosofía |
| Chunking | Indexer con chunks + estructura (markdown-aware) |
| "RAG = mejor informado, no más inteligente" | **La razón del diseño del lab** (conocimiento en RAG, razonamiento en modelo) |
| Errores comunes (chunking malo, contexto irrelevante) | Ya medidos/controlados (evaluar_rag.py, telemetría F4) |

### 📌 Lo destacable

1. **La analogía del examen a libro cerrado/abierto** (slides 2-3) es la MEJOR
   forma de explicar RAG a no técnicos — **material directo para LinkedIn/TFM**
   con el estilo recién decidido (texto + gráficos bonitos + español)
2. **Slide 10** ("RAG no aumenta la inteligencia, te hace mejor informado") =
   frase clave para explicar por qué el lab separa conocimiento (RAG) de
   razonamiento (modelo) — exactamente la arquitectura del lab
3. Sin gaps técnicos nuevos — el lab implementa el carrusel de forma superior

### 🚫 Nada accionable nuevo

- No hay técnica que el lab no tenga
- El valor es 100% **formativo/explicativo** (referencia de cómo explicar RAG
  a principiantes)

---

## Registro

- Guardado: research/analisis-rag-explicado-carli-code.md
- Veredicto: **VALIDA + material didáctico para LinkedIn/TFM**
- Nota técnica: slides 1, 5-9 requirieron re-análisis individual (GLM entra en
  modo razonamiento en lotes; prompt firme "NO razones" + thumbnail 512 lo
  resuelve)
