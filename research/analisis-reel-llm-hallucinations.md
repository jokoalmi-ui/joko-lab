---
title: "Análisis — Reel LLM Hallucinations (codeby.akash, 16-ago-2026)"
type: research
---

# Análisis — Reel LLM Hallucinations (codeby.akash, 16-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/reel/DcFlppwhpGJ/ (10s, @codeby.akash)
**Método:** JSON embebido → vídeo completo (403 KB) → 10 frames → GLM-4.6V local (2 tandas)

## Contenido del reel
Vídeo estático (todos los frames idénticos, sin animación real) sobre **alucinaciones de LLM**:

- **Título:** "LLM HALLUCINATIONS — How & Why LLMs Can Generate Incorrect Information" (con ejemplo)
- **Explicación paso a paso:**
  1. Entrada del usuario: "The sky is"
  2. Datos de entrenamiento: el modelo se entrena con grandes volúmenes de texto ("El cielo es azul", "el cielo está claro"...)
  3. Modelo LLM (red neuronal)
  4. Probabilidades de la siguiente palabra: "blue" 80%, "clear" 15%, "open" 5% (más/menos probable)
  5A. Respuesta factual: ✓ "The sky is blue"
  5B. Respuesta alucinada: ! "The sky is flat"
- **Sección "el cerebro":** los LLM no saben hechos, predicen patrones → alucinación
- **Conclusiones (Key Takeaways):** 1) Los LLM predicen, no saben; 2) Basado en patrones de entrenamiento; 3) Las probabilidades importan; 4) Verificar información crítica
- @codeby.akash al final

## Veredicto para el lab
**DIDÁCTICO BÁSICO, SIN APORTE NUEVO:**
- Explica el mecanismo de las alucinaciones (predicción de patrones, no conocimiento) — nivel divulgativo correcto y visualmente claro
- **El lab ya lo tiene implementado y más avanzado**: el pipeline de verificación (gates SVP/F4, verify_ko con evidence→missing, RAG con recall@5 100%) es exactamente la "verificación de información crítica" que el reel recomienda como takeaway #4
- **NO accionable** — no hay herramienta nueva, técnica nueva ni dato nuevo

**Único valor posible:** el formato visual (diagrama de flujo con probabilidades) es buen material didáctico para explicar alucinaciones en el TFM/LinkedIn — mismo estilo texto+gráficos del lab. La explicación "80% blue / 15% clear / 5% open" es la mejor analogía visual de por qué un LLM alucina.

## Registro
- Guardado: research/analisis-reel-llm-hallucinations.md
- Veredicto: didáctico básico; el lab ya supera el consejo (verificación de información crítica implementada); material de referencia TFM/LinkedIn.
