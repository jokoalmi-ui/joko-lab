---
title: "Análisis: \"Your RAG is not broken\" — Vectorless RAG (shiva.bytes)"
type: research
---

# Análisis: "Your RAG is not broken" — Vectorless RAG (shiva.bytes)
**VERACIDAD:** [VERIFICADO]

**Fuente**: https://www.instagram.com/reel/DcyTFq2jP0t/ · @shiva.bytes · 02-sep-2026
**Formato**: reel divulgativo (caption completo = argumento íntegro; sin transcripción de audio — no necesaria para el veredicto)
**Estado**: [VERIFICADO] caption literal · **Veredicto: VALIDACIÓN (el lab ya lo tiene)**

## Argumento del reel (caption literal)

- "Your RAG is not broken. It is looking in the wrong way 👀"
- Traditional RAG persigue texto "similar" (vectorial). **Vectorless RAG** encuentra
  la sección exacta donde vive la respuesta (keyword/FTS exacto).
- Ejemplo: manual de compliance de 400 páginas — uno hojea la superficie, el
  otro va directo a la cláusula correcta.
- Traditional RAG brilla con datos desestructurados/messy. Vectorless gana en
  contratos, manuales, API docs, codebases.
- **"La mayoría de sistemas reales necesitan AMBOS, enrutados por forma del
  documento y tipo de pregunta"** ← la tesis clave.

## Veredicto para el lab (filtro de valor, regla 20-ago)

**VALIDACIÓN, no acción.** El lab YA implementa el híbrido que el reel describe:

```
search.py L182: hybrid_rank (columna adicional)
search.py L215: RRF (Reciprocal Rank Fusion) sobre scores
search.py L269: fallback FTS si vectorial falla ("[hybrid] FTS fallo, usando solo vectorial")
```

Es decir: el lab combina búsqueda vectorial (LanceDB) + FTS keyword exacto
con fusión RRF — exactamente el "ambos, enrutados" del reel. El reel valida
la arquitectura del lab desde un caso real (manuales, docs, codebases).

Investigaciones previas del lab que ya cubrían el terreno: reranking
(thepracticai), RAG completo (ketan), top-5 RAG (codewithbrij), datasciencebrain.

## Valor como CONTENIDO (señal real, 02-sep)

El **gancho del reel es excelente para LinkedIn**: "Your RAG is not broken.
It is looking in the wrong way" — titular de negación + reframe, patrón que
funciona. El ejemplo del manual de 400 páginas (superficie vs cláusula
exacta) es una analogía visual potente para explicar híbrido vectorial+FTS.

Ángulo para contenido propio: el lab puede contar su caso REAL (recall@5
100%, híbrido LanceDB+FTS con RRF) como ejemplo práctico de "cuándo la
búsqueda exacta gana a la vectorial" — contenido con credibilidad porque es
experiencia propia, no teoría.

## Notas
- shiva.bytes = canal ya analizado (prompt/prefix tuning, 22 frameworks agentes).
- El post siguiente del feed (ai_vatika "Complete Generative AI Roadmap") NO
  forma parte de este reel — es otro post de otra cuenta.
