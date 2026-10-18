---
title: "Análisis — \"Comment RAG to get the complete notes\" (codedsoul_05, 24-ago-2026)"
type: research
---

# Análisis — "Comment RAG to get the complete notes" (codedsoul_05, 24-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcaoisnjY9p/ (codedsoul_05 / Nikhil Solanki, 24-08-2026, 186 likes, 211 comentarios)
**Método:** caption íntegro (og:description) + verificación de imágenes del carrusel (2 imágenes principales 1024×1365, notas manuscritas; resto = posts recomendados)

## El patrón: engagement bait clásico

- **CTA**: "Comment 'RAG' to get the complete notes" — 211 comentarios (la mayoría "RAG", "Rag", 🙌)
- **Contenido real**: notas manuscritas de RAG en carrusel (2 imágenes visibles)
- **El caption NO contiene el conocimiento** — solo el índice del temario:
  LLMs, Transformers, Prompt Engineering, RAG, Document Loading, Embeddings,
  Vector Databases, Retrieval, Reranking, Advanced RAG, Agents, Evaluation,
  Real World Concepts, Interview Q&A

## 🔴 Aplicación al LAB — VALOR BAJO (el temario ya está implementado y superado)

| Tema del carrusel | En el lab |
|---|---|
| LLMs, Transformers | ✅ GLM local, gpt-oss, LFM — en producción |
| Prompt Engineering | ✅ Skill `prompt-engineering` |
| RAG | ✅ **RAG local completo**: LanceDB (21.537 fragmentos) + reranker + evaluar_rag.py |
| Embeddings / Vector DB | ✅ LanceDB + embedding local |
| Retrieval / Reranking | ✅ Reranker :8765 |
| Advanced RAG | ✅ Skill `agentic-rag` (loop iterativo) + 200OK spec 2026 |
| Agents | ✅ Hermes + delegación |
| Evaluation | ✅ `evaluar_rag.py` (recall@5 100%, 73-86 ms) + LLM-as-judge |
| Interview Q&A | ⚪ Material posible para TFM/entrevistas |

## Veredicto: VALOR BAJO (descarta sin extraer imágenes)

1. **Es engagement bait** — el mismo mecanismo que Manus (ivanvibecodes), pero aquí el contenido SÍ existe (notas manuscritas) y está en el carrusel
2. **El temario es introductorio** — "RAG from fundamentals to advanced" para preparar entrevistas; el lab está POR ENCIMA (lo tiene implementado, medido y documentado)
3. **Único valor posible**: las notas manuscritas como material de repaso para el TFM o entrevistas — pero es contenido educativo genérico, no hay nada nuevo
4. **Criterio aplicado** (documentado 23-ago, caso codedsoul): cuando el caption contiene el conocimiento completo, no extraer imágenes; aquí el caption tiene el ÍNDICE completo → el análisis se hace con eso

**Sin futuribles, sin backup de imágenes.** Registrado como otro caso de validación: el contenido educativo que circula sobre RAG está al nivel de lo que el lab ya tiene implementado y superado con medición real (recall 100%, 73-86 ms).
