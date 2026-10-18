---
title: "Análisis — Truco \"se calle\" Claude Opus 5 (prompteados, 15-ago-2026)"
type: research
---

# Análisis — Truco "se calle" Claude Opus 5 (prompteados, 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcA5MeICKhY/ (carrusel 4 slides)
**Autor:** prompteados
**Método:** 4/4 slides CDN + GLM-4.6V-Flash local (slide 3 vía reasoning_content)

---

## Contenido

| Slide | Contenido |
|---|---|
| 1 | Truco viral: decirle "se calle" a Claude Opus 5 mejora resultados (usuarios afirman ~10x) — estrategia de memoria forzada |
| 2 | Interacción con Claude + reemplazo por Opus 5 (memoria administrada; ejemplos: opinión, calculadora, microondas) |
| 3 | El prompt real del truco: "CALLATE. SOLO CALLATE. NO TE PEDI TUS PENSAMIENTOS, HAZ LA TAREA..." (instrucciones firmes de silencio) |
| 4 | CTA: curso gratis de IA (1-3 septiembre, 20:00h España) — marketing |

---

## Veredicto

### 🚫 NO accionable para el lab — meme de prompt engineering

- Es un **truco anecdótico y viral** (prompt agresivo de "cállate") para Claude Opus 5
- El lab usa **DeepSeek/Hermes**, no Claude Opus 5 → el truco no aplica directamente
- El principio de fondo (instrucciones firmes → menos divagación) **ya está documentado**
  en el lab: skill `prompt-engineering` + sysmsg del router ("NO razones en voz alta,
  da la respuesta directa") + el pitfall real de GLM (razona en voz alta si no se le
  pide lo contrario)

### ⚠️ Única observación (curiosidad, no acción)

- El patrón "pide firmeza para que el modelo no divague" es EXACTAMENTE el problema
  que el lab ya resolvió con GLM (que responde en `reasoning_content` cuando el
  prompt no es directo). La lección del carrusel = confirmación informal de que el
  prompt firme importa — pero el lab ya lo aplica.

### 📌 Nota

- Slide 4 = marketing puro (curso gratis) — mismo patrón de monetización
  detectado en maurys (repo premium) y briascoi (curso): los canales IG
  divulgativos acaban en CTA de venta.

---

## Registro

- Guardado: research/analisis-se-calle-claude-prompteados.md
- Veredicto: **NO accionable — meme; valida informalmente el prompt firme del lab**
