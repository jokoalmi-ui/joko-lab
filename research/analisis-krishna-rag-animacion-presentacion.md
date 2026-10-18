---
title: "Análisis — Reel krishnachaytanyaa: animación RAG (estilo presentación) (17-ago-2026)"
type: research
---

# Análisis — Reel krishnachaytanyaa: animación RAG (estilo presentación) (17-ago-2026)

**Fuente:** https://www.instagram.com/reel/DZU2dPHtcja/ (krishnachaytanyaa, 9.2s, vertical 720×1280)
**Método:** fetch navegador (MP4 298 KB) → scdet 2 frames → GLM + browser_vision. Audio falló (CUDA OOM: GLM ocupa VRAM, whisper sin espacio — esperable en 12 GB)
**VERACIDAD:** [VERIFICADO]
**⚠️ OBJETIVO DEL USUARIO**: copiar el ESTILO como animación de presentación (no el contenido RAG)

## CONTENIDO (lo que dice)

### Diagrama animado de arquitectura RAG (Retrieval-Augmented Generation)

Flujo vertical secuencial: **QUERY → AUGMENT → RETRIEVER → KNOWLEDGE BASE → LLM**

Componentes (cada uno con icono + etiqueta):
1. QUERY — burbuja de mensaje (arriba)
2. AUGMENT — icono cámara
3. RETRIEVER — lupa
4. KNOWLEDGE BASE — icono base de datos
5. LLM — cuadrado con puntos
Conectados por línea punteada vertical que simula el flujo del proceso.

## FORMATO / ESTILO (lo que se quiere COPIAR)

| Elemento | Detalle |
|---|---|
| **Fondo** | Oscuro (negro/azul profundo) con centro más claro para destacar |
| **Colores** | Neutros + acento **cian** para el elemento activo (QUERY) y texto clave; etiquetas en blanco/gris claro |
| **Componentes** | Iconos geométricos simples en cajas (burbuja, lupa, BD, cuadrado) con etiqueta uniforme |
| **Tipografía** | Sans-serif limpia; título grande negrita centrado ("RAG"), subtítulo pequeño ligero |
| **Animación** | **Presentación secuencial**: elementos que aparecen en orden + línea punteada que se anima siguiendo el flujo (QUERY → ... → LLM) |

## APLICACIÓN AL LAB — CÓMO COPIARLO (con stack local)

**Este estilo es 100% replicable con el Manim MCP implementado hoy:**

| Elemento del reel | Equivalente local |
|---|---|
| Fondo oscuro + acento cian | Manim: `config.background_color = "#0d1117"` + color cian `#00E5FF` |
| Iconos geométricos | Manim: `Circle`, `RoundedRectangle`, `Line` con `VGroup` |
| Texto título/etiquetas | Manim: `Text` (fuente sans-serif) |
| **Línea punteada animada** | Manim: `DashedLine` + `Create` (animar el flujo) |
| **Aparición secuencial** | Manim: `FadeIn`/`Create` encadenados con `wait()` |
| Estilo presentación | El patrón del lab `render_paso_pagina.sh` + `crear_video_explicativo.sh` |

**Ventaja del lab**: con el Manim MCP (animation-server) se puede pedir este
estilo por prompt: "genera una animación estilo presentación con fondo oscuro,
elementos que aparecen secuencialmente conectados por línea punteada animada".

## Veredicto
**MUY RELEVANTE para el objetivo del usuario** (copiar como animación de
presentación). El estilo es simple y replicable con las herramientas que el
lab YA tiene (Manim MCP + skills de vídeo). El contenido RAG es tangencial
(el lab ya lo conoce); el valor está en el ESTILO: fondo oscuro, acento cian,
elementos secuenciales, línea de flujo animada. Coincide además con la
directiva de vídeos del lab (estático + aparición progresiva, sin Ken Burns).

**Nota proceso**: audio no transcrito por CUDA OOM (GLM cargado en VRAM);
no bloquea porque el objetivo es el estilo visual. Para transcripciones
futuras con GLM cargado, considerar liberar VRAM primero (lms unload) o
transcribir con CPU (whisper CPU).
