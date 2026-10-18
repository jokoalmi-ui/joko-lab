---
title: "Análisis — Reel: How do we evaluate RAG pipelines with LLMs? (@gauravgoyalai, 16-ago-2026)"
type: research
---

# Análisis — Reel: How do we evaluate RAG pipelines with LLMs? (@gauravgoyalai, 16-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/reel/DcFQudFz7BR/ (10s, @gauravgoyalai)
**Método:** JSON embebido → vídeo completo (443 KB) → 10 frames → GLM-4.6V local (OCR)
**Nota:** el caption del JSON era de otro post (Claude Certifications, carrusel del mismo autor);
el vídeo real del reel es sobre evaluación de pipelines RAG.

## Contenido del reel
Título: **"HOW DO WE EVALUATE RAG PIPELINES WITH LLMs?"**
Subtítulo: "A reliable RAG system needs more than a good LLM. We need to evaluate
retrieval, context, generation, and tool usage."

1. **OBSERVABILITY & EVALS**: trackear el pipeline completo
   (User Query → Retrieval → Context → LLM → Answer → Tools); monitorizar cada
   paso para identificar dónde se rompe la calidad.
2. **WHAT ARE EVALS?**: Evals = tests sistemáticos de calidad RAG:
   - ANSWER RELEVANCE: ¿la respuesta aborda la pregunta?
   - GROUNDEDNESS / FAITHFULNESS: ¿la respuesta está respaldada por el contexto recuperado?
   - RETRIEVAL QUALITY: ¿el sistema recuperó la información correcta?
   - TOOL-CALL / SEQUENCE QUALITY: ¿el agente usó las herramientas correctas en el orden correcto?
3. **WHO DOES THE EVALUATION?**: combinación de:
   - HUMAN EVALUATION: expertos revisan ejemplos representativos
   - LLM-AS-A-JUDGE: un LLM puntúa outputs contra criterios definidos
   - AUTOMATED METRICS: métricas medibles de retrieval y generación
   - ⭐ Best practice → combinar múltiples métodos de evaluación
4. **WHAT SHOULD WE MEASURE?**: RAG Quality = Retrieval + Generation + System Behavior
   - Retrieval: Relevance, Recall, Ranking
   - Context: Relevance, Completeness, Noise
   - Generation: Correctness, Relevance, Groundedness
   - Tools: correct tool, correct sequence
   - System: Latency, Errors, Cost, Stability
5. **KEY TAKEAWAY** (checklist):
   - No preguntar solo "¿es buena la respuesta final?"
   - ¿Recuperamos la info correcta? ¿Usamos el contexto correcto?
   - ¿Generó el LLM una respuesta grounded? ¿Usó las herramientas correctamente?
- **Conclusión**: RELIABLE RAG = OBSERVABLE + EVALUATED + CONTINUOUSLY IMPROVED
- Footer: "Evaluate continuously. Improve consistently."

## Veredicto para el lab
**CONFIRMA el enfoque del lab + aporta 1 matiz útil:**
- **El lab YA hace esto** (y en parte mejor): observabilidad (métricas pipeline
  LLM), evaluaciones (evaluar_rag.py con recall@5 100% en 70 ms, gates SVP/F4),
  métricas de RAG (LanceDB híbrido BGE-M3), monitorización de coste/latencia.
- **Novedad/refuerzo del reel**: la **tabla por capas** (Retrieval / Context /
  Generation / Tools / System) como checklist estructurado — útil para el TFM y
  para ampliar el `evaluar_rag.py` con métricas de Context (noise/completeness)
  y de System (latencia/errores) si algún día hacen falta.
- El concepto **LLM-as-a-judge** ya se usa en el lab (verificación de respuestas
  con R1/GLM en el pipeline).
- Material didáctico: buen diagrama para LinkedIn/TFM sobre RAG.

## Registro
- Guardado: research/analisis-reel-rag-evals-gauravgoyalai.md
- Veredicto: confirma el enfoque del lab (observabilidad + evals + mejora continua);
  aporta checklist por capas como referencia; nada nuevo que implementar ya.
