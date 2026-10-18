---
title: "Análisis: \"Complete Generative AI Roadmap\" (ai_vatika) — base roadmap LinkedIn"
type: operations
---

# Análisis: "Complete Generative AI Roadmap" (ai_vatika) — base roadmap LinkedIn
**VERACIDAD:** [VERIFICADO]

**Fuente**: https://www.instagram.com/reel/Dcw9EHKSk8r/ · @ai_vatika · 02-sep-2026
**Formato**: imagen única tipo cheat sheet (grid 4×5, 19 cajas numeradas) — el caption
dice "single cheat sheet" (confirmado: 1 imagen real, las demás del DOM eran del grid)
**Estado**: [VERIFICADO] imagen real + caption · GLM visión + análisis visual
**Uso**: base estructural para roadmap de publicaciones LinkedIn del usuario

## Qué es

"The Complete Generative AI Roadmap — 19 KEY TOPICS TO MASTER GENERATIVE AI":
grid 4×5 de cajas numeradas 1-19, fondo oscuro, cada caja con tema + sub-puntos
(icono, título, lista de conceptos). Cuenta-IA genérica ("Contenido generado con
IA"), 26 likes, sin profundidad en cada tema (es índice, no explicación).

### Los 19 temas
1 GenAI Fundamentals · 2 AI vs ML vs DL · 3 Modelos Generativos · 4 LLM Fundamentals
· 5 Tokens & Tokenization · 6 Embeddings · 7 Transformers & Attention · 8 Prompt
Engineering · 9 Parámetros & Decoding · 10 RAG Fundamentals · 11 RAG Pipeline ·
12 Técnicas Avanzadas · 13 Fine-tuning & PEFT · 14 Function Calling · 15 Agentes &
Workflows · 16 Multimodal · 17 Evaluación & Guardrails · 18 Seguridad GenAI ·
19 Aplicaciones reales

## Juicio de DISEÑO (separar estructura de estilo)

**El ESTILO es anti-patrón del lab** (mismo caso DcxT4UIB-_C documentado 02-sep):
cajas numeradas con texto denso = cheat sheet genérico de cuenta-IA. NO replicar
el estilo visual en piezas del lab (regla INFOGRAFÍAS: mínimo arte SDXL +
tipografía sobre arte; nunca degradar).

**La ESTRUCTURA SÍ vale** como columna vertebral editorial: orden pedagógico
correcto (fundamentos → arquitectura → técnicas → producción → aplicaciones).
Es un buen índice de qué temas cubre el terreno GenAI.

## Cruce con capacidades reales del lab (333 research)

| Tema roadmap | Research lab | Experiencia demostrable |
|---|---|---|
| RAG (10-12) | 25 | ✅✅ híbrido vectorial+FTS RRF, recall@5 100%, reranker, adversarial |
| Agentes (15) | 44 | ✅✅ kanban jerárquico, delegación, MCP, subagentes |
| Evaluación (17) | 2 + gate | ✅✅ gate veracidad, batería 5x5, juicio ciego, adversarial |
| Fine-tuning/PEFT (13) | 6 | ✅ conceptos + reel 5 técnicas (02-sep) |
| Multimodal (16) | 2 | ✅ CLIP, visión GLM local, pipeline reels |
| Prompt (8) | 4 | ✅ skills prompt engineering |
| Seguridad (18) | 1 | 🟡 tirith, adversarial — parcial |
| Embeddings (6) | 0 directos | 🟡 BGE-M3 en uso, sin research dedicado |
| Transformers/Modelos/Tokens (3-5,7) | — | ⚪ teoría genérica |
| Aplicaciones reales (19) | — | ⚪ caso-dependente |

**Insight**: no publicar 19 temas genéricos — publicar los ~6-8 con evidencia
real propia (RAG, agentes, evaluación) con sello "esto lo construí y lo mido".
El resto = relleno que cualquier cuenta-IA hace igual.

## Propuesta de roadmap editorial (3 fases)

- **Fase A — terreno propio (experiencia demostrable)**: RAG híbrido + recall
  medido + gate de veracidad + agentes verificados → 6-8 posts con datos reales.
- **Fase B — conceptos con ángulo propio**: fine-tuning GPU doméstica, embeddings
  con caso BGE-M3, evaluación adversarial, "tu RAG es Self-RAG sin llamarlo así".
- **Fase C — relleno opcional**: solo si falta cadencia y no hay material A/B.

## Notas
- Post visto en feed previamente (02-sep, durante análisis reel shiva.bytes) —
  ahora compartido explícitamente por el usuario como candidato a roadmap.
- PENDIENTE (si el usuario lo pide): desarrollar el roadmap editorial completo
  (Fase A: qué post concreto + qué dato real como gancho + orden).
