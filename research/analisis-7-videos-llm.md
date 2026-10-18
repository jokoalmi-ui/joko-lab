---
title: "Análisis — Post Instagram: 7 vídeos para entender LLMs (jugaldb)"
type: research
---

# Análisis — Post Instagram: 7 vídeos para entender LLMs (jugaldb)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 05-ago-2026
**Fuente:** https://www.instagram.com/p/DbLjBHHsCFx/ — jugaldb (verificado)
**Nota:** El caption dice "Comment LLM y te mando los links" (trampa de DM).
Los enlaces están DENTRO de la imagen del póster — extraídos con GLM (visión
local) + verificación con YouTube oEmbed.

---

## Los 7 vídeos (extraídos de la imagen)

| # | Título | ID YouTube | Verificado |
|---|---|---|---|
| 1 | How Large Language Models Work | `5sLYAQS9sWQ` | ✅ |
| 2 | Large Language Models explained briefly | `LPZh9BOjkQs` | ✅ |
| 3 | [1hr Talk] Intro to Large Language Models (Karpathy) | `zjkBMFhNj_g` | ✅ |
| 4 | LLM Explained / What is LLM | `67_aMPDk2zw` | ✅ |
| 5 | Everything About LLMs | `osKyyVJ3PRM` | ❌ ID no verificado |
| 6 | How LLMs Works? - Overview | `K45s2PgywvI` | ✅ |
| 7 | 20 AI Concepts Explained in 40 Minutes | `OYvlznJ4IZQ` | ✅ |

**Nota del #5:** el ID leído por GLM (`osKyyVJ3PRM`) no existe en YouTube —
probablemente un carácter mal leído por OCR. 5 intentos de relectura fallaron.
El vídeo "Everything About LLMs" existe (es una encuesta sobre ventanas de
contexto, parámetros y tradeoffs) pero el ID exacto requiere ver el póster
a ojo. Los otros 6 están confirmados funcionando.

---

## Método usado (el reto del usuario)

1. Navegador a Instagram → aceptar cookies → leer el post (caption + alt)
2. El alt de la imagen revelaba IDs parciales (zjkBMFhNj_, aMPDk2zw, K45s2Pgywv)
3. **Descargar la imagen del póster** (2700×3375, 1.2 MB) desde cdninstagram
4. **GLM 4.6V (visión local)** leyó la imagen → extrajo títulos + IDs
5. **Verificación con YouTube oEmbed** (público, sin login) → 6/7 confirmados

**Lección:** Instagram público + visión local + verificación externa =
extracción de enlaces funcional. La limitación: OCR de IDs pequeños en
imágenes densas puede fallar (1/7 aquí).

---

## Aplicación al lab

- El #3 (Karpathy Intro to LLMs) es el clásico imprescindible — si se quiere
  material de estudio del máster, es el primero.
- El método (descargar imagen IG → GLM → verificar) es reutilizable para
  extraer información de infografías/pósters de Instagram.
- Posible mejora: skill "extraer-enlaces-de-posters" (pip install yt-dlp para
  resolución de IDs ambiguos).

## Nota

Post con estrategia de engagement (DM a cambio de comment). El contenido real
(los 7 vídeos) es una buena lista de fundamentos de LLMs — útil como material
de estudio (máster FOUNDERZ) y para el lab.
