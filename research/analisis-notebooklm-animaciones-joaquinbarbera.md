---
title: "Análisis — ¡Olvida los prompts! NotebookLM como máquina de animaciones (Joaquín Barberá, 15-ago-2026)"
type: research
---

# Análisis — ¡Olvida los prompts! NotebookLM como máquina de animaciones (Joaquín Barberá, 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/q3qcXXsoYno (Joaquín Barberá - IA, ~12 min, es)
**Transcripción:** completa (es)

## Qué muestra
Pipeline completo para crear **animaciones "papercraft" (papel en capas)** — el estilo de vídeo que funciona en YouTube/TikTok/IG:

1. **Gemini Notebook (ex-NotebookLM)** con un "Master Prompt" (lo pega en fuentes + personalización del chat):
   - Propone 10 ideas de vídeos optimizadas para animación papel-en-capas (maximiza ASMR visual + retención)
   - Genera **2 prompts**: uno para el **storyboard** (panel de viñetas) y otro para el **vídeo**
   - Acepta ideas propias del usuario (descripción detallada de colores, texturas, capas)
2. **Generación del storyboard**: en el chat de Gemini Notebook (`crea esta imagen: <prompt>`) o vía **infografía vertical** si la generación de imagen no está disponible en el país
3. **Generación del vídeo con Google Flow (agente + modelo Veo Flash)**:
   - Subir la imagen de referencia (storyboard o infografía) + pegar el prompt de vídeo
   - 50 créditos/día por cuenta Google (~15 créditos por vídeo); 5 cuentas = 250 créditos/día
4. **Música con Flow Music** (gratis, créditos diarios): prompt para instrumental (guitarra acústica, piano, sintetizador ambiental)
5. **Montaje en CapCut** (o cualquier editor): 3+ vídeos + música → exportar

Bonus: muestra la funcionalidad de **Tad.ai** (música + vídeos musicales con sincronización labial).

## Veredicto para el lab
**INTERESANTE PERO CONFLICTO CON EL LOCAL-FIRST — dividido:**

### Lo que encaja
- El **estilo "papel en capas"** es un formato de contenido probado (ASMR visual + retención) — material para el plan de ingresos puente (vídeos cortos en YouTube/TikTok/IG) y para el estilo de contenido del lab
- El patrón **"Master Prompt → ideas → 2 prompts (storyboard + vídeo)"** es aplicable a cualquier LLM, incluido el local
- Es contenido para la marca personal (LinkedIn/IG) — el lab ya tiene `crear_video_explicativo.sh`

### Lo que NO encaja
- **Depende de herramientas cloud**: Gemini Notebook, Google Flow (Veo Flash), Flow Music, CapCut — todo con cuentas Google y créditos diarios (no local-first)
- El lab ya tiene el análisis de NotebookLM (12-ago): el equivalente local y mejor (RAG local, sin límites ni nube)
- La animación "papel en capas" real requeriría herramientas de edición que el lab no tiene instaladas

### Decisión
**Futurible ligero**: el FORMATO "papercraft en capas" se puede replicar con el pipeline local del lab (HTML/CSS → capturas → vídeo con `crear_video_explicativo.sh`), pero NO ahora — es contenido para cuando el plan de ingresos/marca personal se materialice. El patrón de prompts (master prompt → 2 prompts derivados) es una técnica de prompt-engineering ya conocida en el lab.

## Registro
- Guardado: research/analisis-notebooklm-animaciones-joaquinbarbera.md
- Futurible: formato "animación papel en capas" para vídeos de marca personal (replicable localmente, no urgente).
