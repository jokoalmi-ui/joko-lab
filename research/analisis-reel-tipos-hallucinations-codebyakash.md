---
title: "Análisis — Reel: Types of Hallucinations in AI (@codeby.akash, 16-ago-2026)"
type: research
---

# Análisis — Reel: Types of Hallucinations in AI (@codeby.akash, 16-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/reel/DcFmIL3Bfk0/ (10s, @codeby.akash)
**Método:** JSON embebido → vídeo completo (393 KB) → 10 frames → GLM-4.6V local (OCR)
**Nota:** canal @codeby.akash YA vigilado (aportó MCP vs RAG 14-ago + reel LLM Hallucinations hoy)

## Contenido del reel
**"🧠 Types of Hallucinations in AI"** — 4 tipos de alucinación (cada uno con icono visual):

1. **Sentence Contradiction** — el modelo se contradice dentro de la misma respuesta
2. **Prompt Contradiction** — la respuesta va contra el prompt/instrucciones del usuario
3. **Factual Contradiction** — información fáctica incorrecta o falsa
4. **Random Hallucinations** — contenido irrelevante, sin sentido o fuera de tema

**Conclusión (en el caption, no en el vídeo):** antes de mejorar un sistema de IA
hay que entender QUÉ tipo de alucinación se tiene. Técnicas de mitigación:
RAG, mejor contexto, datos fiables, **structured outputs**, evaluación y
fact-checking.

## Veredicto para el lab
**COMPLEMENTA el reel anterior del mismo autor + confirmación del enfoque:**
- Es la **taxonomía** de alucinaciones que el reel anterior (LLM Hallucinations)
  no desglosaba: ahora distingue 4 tipos.
- **El lab ya mitiga los 4 tipos**: factual (gates SVP/F4, verify_ko
  evidence→missing), prompt (instrucciones/plantillas), sentence
  (verificación de respuesta), random (structured outputs en el pipeline).
- **Nada nuevo que implementar** — pero la **taxonomía de 4 tipos** es buen
  material didáctico (TFM/LinkedIn) para explicar POR QUÉ el lab verifica
  respuestas: "no toda alucinación es lo mismo".
- Complementa `analisis-reel-llm-hallucinations.md` (mismo autor, misma sesión).

## Registro
- Guardado: research/analisis-reel-tipos-hallucinations-codebyakash.md
- Veredicto: taxonomía de 4 tipos; el lab ya mitiga todos; material didáctico
  TFM/LinkedIn; canal ya vigilado (sin cambio de skill).
