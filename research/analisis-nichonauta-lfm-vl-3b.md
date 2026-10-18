---
title: "Análisis — Liquid AI LFM 2.5 VL 3B, visión eficiente (Nichonauta, 21-ago-2026)"
type: research
---

# Análisis — Liquid AI LFM 2.5 VL 3B, visión eficiente (Nichonauta, 21-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/msa_tCqhJUw (Nichonauta, 14-08-2026, 8:55)
**Método:** transcripción ES completa (yt-dlp auto-subs, 24.3K chars, dedup parcial)

## El modelo (verificado en el vídeo)
**LFM 2.5 VL 3B** (Liquid AI) — modelo de VISIÓN de pesos abiertos, 16 idiomas (incl. español):
- **3B parámetros** (pequeño, eficiente) · Q4 = **1.67 GB**
- GGUF disponible → LM Studio, Ollama, llama.cpp
- **Requiere el encoder de visión (mmproj)** aparte — sin él no sirve para imágenes
- Ventana de contexto: **32,768**
- Parámetros recomendados: temp 0.22 · top_k 50 · repeat penalty 1.0
- **Sin cadena de razonamiento** (responde directo, rápido)
- Habilidades estrella:
  1. **Posicionamiento + detección de objetos por consulta en lenguaje natural** — no solo
     "qué hay", sino "DÓNDE está" (verificado: localiza personajes, cables, colores con precisión)
  2. **OCR de página completa** con anotaciones de diseño
  3. Rápido en GPU y **sin GPU** (poca VRAM/RAM)
- Fallos honestos del vídeo: contar líneas (dijo 3, eran 2) y puntos de luz (dijo 12, ~10)
- Herramientas/funciones: MALO (no es su objetivo, poca ventana de contexto)

## 🔴 Para el LAB — VEREDICTO: MEDIO-ALTO (candidato real a visión ligera)

| Aspecto | Veredicto |
|---|---|
| Peso (1.67 GB Q4) vs GLM (7.41 GiB) | ✅ **~4.4× más ligero** — podría convivir con gpt-oss en 12 GB |
| Visión local (reemplazo/complemento GLM) | 🟡 Candidato para tareas de visión simples (verificar frascos, OCR capturas, monitor) |
| OCR de página completa | 🟡 Sustituiría al tesseract NO instalado (capturas de sueño, docs) |
| Posicionamiento de objetos | 🟡 Útil para el monitor LM Studio / análisis de capturas |
| GLM sigue siendo mejor en visión compleja | ✅ Para razonamiento visual profundo mantener GLM |
| Herramientas: malo | ✅ No usar para tool calling |

## Futurible nuevo (F8)
> **Probar LFM 2.5 VL 3B (Q4, 1.67 GB) como modelo de VISIÓN LIGERO del lab** — señal:
> cuando se necesite visión que conviva con gpt-oss (12 GB) o para OCR/posicionamiento sin
> pagar los 7.4 GiB de GLM. No sustituye a GLM en razonamiento visual, pero amplía el
> portfolio de modelos locales (misma familia que LFM 2.5 2.6B ya validado 7/7).

*Nota: coherente con la serie Nichonauta (modelos pequeños + eficiencia). El lab ya usa
LFM 2.5 2.6B (texto, validado); este es su hermano de visión.*
