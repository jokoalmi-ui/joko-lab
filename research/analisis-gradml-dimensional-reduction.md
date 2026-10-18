---
title: "Análisis — Reel graduate_ml: Dimensional Reduction Algorithms (17-ago-2026)"
type: research
---

# Análisis — Reel graduate_ml: Dimensional Reduction Algorithms (17-ago-2026)

**Fuente:** https://www.instagram.com/reel/Da5hOE9zS_s/ (graduate_ml, 7s, vertical 720×1280)
**Método:** fetch navegador (MP4 353 KB) → scdet 2 frames → GLM + browser_vision. Audio inútil ("Okay" — whisper CPU con fix del día, 4 chars)
**VERACIDAD:** [VERIFICADO]

## CONTENIDO (lo que dice)

### "Dimensional Reduction Algorithms" — 5 algoritmos de reducción de dimensionalidad

| Algoritmo | Subtítulo (uso) | Fórmula | Visual |
|---|---|---|---|
| **PCA** | variance / preprocessing | Z = XV, Σx = λr | 2D + embed (rojo) |
| **t-SNE** | cluster visualization | min KL(P||Q) | 2D + embed (naranja) |
| **UMAP** | scalable manifold viz | min C(Z|F|W) | 2D + embed (turquesa) |
| **Isomap** | nonlinear manifold unfolding | Z = MDS(D_G) | 2D + embed (morado) |
| **LLE** | local neighborhood preservation | min Σ‖x_i - ΣW_ij·y_j‖² | 2D + embed (verde) |

Formato: tarjetas con nombre + subtítulo (cuándo usarlo) + fórmula + gráfico 2D de embeddings.

## FORMATO (cómo se ve — reel de 7s)

- **Estilo**: tarjetas verticales, cada una con color de fondo distinto por algoritmo
- **Cada tarjeta**: nombre grande + subtítulo (uso) + fórmula + mini-gráfico 2D
- **Fondo**: oscuro con tarjetas de colores
- **Ritmo**: probablemente 1 tarjeta por beat (7s / 5 algoritmos ≈ 1.4s por tarjeta)

## Aplicación al LAB

| Concepto | Aplicación | Valor |
|---|---|---|
| **Reducción de dimensionalidad** | El lab NO la usa hoy (RAG con BGE-M3 embeddings, sin necesidad de reducir) | 🟡 Didáctico |
| **Formato tarjetas por algoritmo** | Reutilizable para slides del TFM (comparativas de técnicas) | ✅ Recurso de formato |
| **Estilo: color por concepto + fórmula + visual** | Patrón visual aislable para infografías propias | ✅ Formato |
| **Contenido ML clásico** | Material educativo posible para LinkedIn Lab | 🟡 Contenido marca empleo |

## Veredicto
**NADA ACCIONABLE / VALIDA.** Reel didáctico de ML clásico (5 algoritmos de
dimensionalidad) que el lab no usa actualmente — el valor está en el FORMATO
(tarjetas con color por concepto + subtítulo de uso + fórmula + visual),
aislable para slides propias o infografías. Consistente con la tendencia del
día: el usuario está coleccionando FORMATOS de infografía/animación para sus
presentaciones (reel Krishna de estilo animado + este de tarjetas de color).
**Nota proceso**: el fix de transcripción inteligente de hoy funcionó de nuevo
en CPU (audio "Okay" — inútil, pero sin CUDA OOM); contenido real en frames
(regla confirmada: frames mandan).
