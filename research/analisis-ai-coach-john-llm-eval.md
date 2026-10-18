---
title: "Análisis — LLM Evaluation Metrics (ai_coach_john, 20-ago-2026)"
type: research
---

# Análisis — LLM Evaluation Metrics (ai_coach_john, 20-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcffhS7k-Fj/ (AI Coach | John Gabriel, 19-ago, carrusel)
**Método:** caption íntegro del snapshot (accesibility tree) — patrón validado 17-ago; 15 slides no descargadas (el caption contiene el texto completo del carrusel)
**Veredicto:** [VERIFICADO]

## Idea central (textual)

> "A high evaluation score doesn't mean your LLM is good. It might just mean you're measuring the wrong thing."

**Nunca preguntes "¿cuál es la mejor métrica?" — pregunta "¿qué fallo estoy intentando detectar?"**

## Las 6 métricas (con qué fallo se conecta cada una)

| Métrica | Qué mide | Para qué sirve | No sirve para |
|---|---|---|---|
| **Faithfulness** | ¿Cada claim está respaldado por el contexto recuperado? | **RAG — detecta alucinaciones** | — |
| **Answer Relevancy** | ¿Respondió la pregunta del usuario? | Ser correcto no basta, debe ser relevante | — |
| **Context Precision** | ¿El retriever trajo docs útiles o ruido? | Diagnostica el pipeline de recuperación | — |
| **BLEU** | Solapamiento exacto de palabras | Traducción automática | Asistentes open-ended (una paráfrasis correcta puntúa mal) |
| **ROUGE** | Cuánto contenido importante se preservó | Resumen (summarization) | Evaluar respuestas RAG |
| **Perplexity** | Fluidez | — | Corrección factual (tonterías fluidas con excelente perplexity) |

## La regla de oro (métrica ↔ fallo)

| Fallo a detectar | Métrica |
|---|---|
| Alucinaciones | Faithfulness |
| Mala recuperación | Context Precision |
| Malos resúmenes | ROUGE |
| Traducción | BLEU |
| Fluidez | Perplexity |

> "The best AI engineers don't optimize for higher scores. They optimize for better user outcomes. Because the wrong metric gives you confidence... not correctness."

## 🔴 Conexión con el LAB

| Aspecto del lab | Veredicto |
|---|---|
| **Gate de veracidad** | ✅ VALIDA al 100% — es Faithfulness aplicado manualmente (¿cada claim tiene fuente?) |
| **RAG evals** (recall@5 100%) | ✅ El lab ya usa **Context Precision** implícito (¿el retriever trae lo útil?) |
| **Batería de modelos 7/7** | ⚠️ La lección aplica: 7/7 en batería ≠ bueno en producción → por eso el lab exige batería de PRODUCCIÓN (5 tareas reales, 19-ago) |
| **Métricas del lab** | ✅ El lab NO optimiza BLEU/ROUGE — evalúa tareas reales con veredicto ciego (juicio del usuario) |
| Evaluador regex de T5 | 🟡 Pitfall conocido 19-ago: evaluadores por keyword dan falsos negativos → evaluar por significado, no substring (es literalmente "the wrong metric gives you confidence, not correctness") |

## Veredicto

**APORTA (validación + refuerzo)** — el carrusel valida la filosofía de evaluación del lab con una regla memorable ("métrica ↔ fallo") que se puede citar en el LinkedIn Lab y en la documentación de evaluación. Nada nuevo que implementar: el lab ya evalúa por fallo real (gate = Faithfulness, recall = Context Precision, batería producción = user outcomes).

## Nota honesta

Análisis basado en el caption íntegro del snapshot (15 slides no descargadas — el caption contiene el contenido completo del carrusel en formato lista; las slides eran capturas de Twitter con el mismo texto). Fuente: texto literal del post verificado en el DOM.
