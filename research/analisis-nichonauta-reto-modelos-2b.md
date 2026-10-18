---
title: "Análisis — Nichonauta: Reto Modelos 2B (C_nBDT9cIGM, 20-ago-2026)"
type: research
---

# Análisis — Nichonauta: Reto Modelos 2B (C_nBDT9cIGM, 20-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/C_nBDT9cIGM (Nichonauta, 20-08-2026, 11:18)
**Método:** transcripción ES (yt-dlp auto-subs, VTT limpio + dedup, ~10.3K chars)
**Veredicto:** [VERIFICADO]

## Tesis del vídeo

> "Cambiar de modelo a diario es perder el tiempo. Un modelo es como una secretaria:
> importa lo bien que te comunicas con ella, no solo lo hábil que sea."

**El canal cambia de enfoque unas semanas**: dejar de probar modelos nuevos → usar SOLO
**Gemma 4 2B** y **Qwen 3.5 2B** (a 4 bits) y sacarles el máximo provecho con
entornos (RAG, MCPs, skills, Atomic AI, Hermes Agent).

## Configuración real mostrada (llama.cpp B10453, RTX 3060 12 GB, CUDA 13)

| Modelo | Archivos | VRAM | tok/s (4500-token prompt) |
|---|---|---|---|
| Qwen 3.5 2B (Q4) | GGUF + MTP incluido | 4.0 GB (3.6 con KV cache Q8) | **136** |
| Gemma 4 2B (Q4) | GGUF + mmproj (visión) + MTP | 3.6 GB (menos con KV Q8) | **173** |

- Ventana de contexto: 131K tokens (máx de Gemma; Qwen soporta el doble)
- Razonamiento activo + presupuesto de razonamiento 8192 tokens (anti-bucle)
- Min tokens para imagen: 1024 (recomendación del agente de Qwen)
- **KV cache en Q8**: mantiene ~99% de calidad consumiendo la MITAD de VRAM — pero
  solo tiene sentido cuantizarla en el modelo principal, no en el borrador

## Casos de uso que plantea

Redacción de contenido · búsqueda en internet · **RAG** · generación de código ·
**uso de herramientas dentro de Hermes Agent** · etc.

## 🔴 Conexión con el LAB

| Aspecto | Estado |
|---|---|
| "Optimizar el entorno, no cambiar de modelo" | ✅ **Es EXACTAMENTE la filosofía del lab**: LFM 2.6B adoptado + gate/revisor + skills |
| Modelos 2B para tareas reales | ✅ El lab ya usa LFM 2.6B (55 tok/s) y gpt-oss-20b para batch |
| **Gemma 4 2B: 173 tok/s @ 3.6 GB** | 🟡 Dato a considerar: ~3x más rápido que LFM en llama.cpp — candidato batch si el lab quisiera aún más velocidad |
| KV cache Q8 (99% calidad, mitad VRAM) | 🟡 Técnica aplicable a los GGUF del lab (si LM Studio lo expone) |
| Modelos de 6 meses "no nuevos" | ✅ Valida la regla del lab: no perseguir novedades, consolidar |

## Veredicto

**APORTA (validación fuerte + 2 datos técnicos útiles)** — el vídeo valida al 100% la
dirección del lab (modelos pequeños + entornos + Hermes Agent). Los 2 datos accionables:
(1) Gemma 4 2B = 173 tok/s @ 3.6 GB como posible candidato batch más rápido que LFM;
(2) KV cache Q8 como técnica de ahorro de VRAM. NO requiere acción inmediata: el lab ya
tiene decidida su batería de modelos (gpt-oss para razonamiento, LFM para interactivo).

## Nota honesta

Transcripción auto-subs (puede tener errores de nombres: "Qen" = Qwen, "Gema" = Gemma).
Medidas mostradas en hardware del canal (RTX 3060, llama.cpp directo, Windows) — no
reproducidas en el lab; son referencia de lo que el modelo puede dar, no benchmark propio.
