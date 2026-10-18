---
title: "Análisis — Nichonauta: Comparativa Speculative Decoding (KC-Dx9hj-e0, 20-ago-2026)"
type: research
---

# Análisis — Nichonauta: Comparativa Speculative Decoding (KC-Dx9hj-e0, 20-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/KC-Dx9hj-e0 (Nichonauta, 19-08-2026, 10:13)
**Método:** transcripción ES (yt-dlp auto-subs, VTT limpio + dedup, ~9.5K chars)
**Veredicto:** [VERIFICADO]

## Qué es speculative decoding (recordatorio del vídeo)

Contar con un **modelo borrador** que predice los siguientes tokens y el **modelo grande
solo valida/corrige**. Transparente para el usuario, sin pérdida de calidad.

## La comparativa REAL (Qwen 3.5 9B, 4 bits, RTX 3060 12 GB)

| Método | tok/s | Notas |
|---|---|---|
| **Sin borrador (base)** | **49.45** | 9.1 GB VRAM |
| **MTP incluido** | **67** | +36% casi gratis (~20 tok/s más), no aumenta mucho VRAM |
| **Qwen 0.8B como borrador** | **18-19** ⚠️ PEOR | Responde muy distinto al 9B → casi todo rechazado; más VRAM por cargar el borrador |
| **The Flash como borrador** | ~50-55 (picos 140+ al inicio) | Inconsistente: arranca rápido y cae; requiere bajar contexto (no cabe, 10 GB); peor que MTP |
| **N-gram (solo contexto)** | **200-260 en contextos SIMILARES** | Casi gratis (0 VRAM extra); SOLO funciona al repetir/modificar código o texto similar ya presente en contexto |

## Conclusiones del canal

1. **MTP = la mejora más rentable**: +36% gratis, sin archivo extra (viene dentro del GGUF en Qwen 3.5)
2. **Un borrador que responde distinto al grande = pierdes velocidad** (0.8B era inútil)
3. **The Flash**: inconsistente en este hardware — no lo recomienda para este modelo
4. **N-gram brilla en uso agéntico/iterativo**: al modificar código ya escrito en contexto (200-260 tok/s)
5. **Combinar MTP + n-gram** puede funcionar: MTP para contextos nuevos, n-gram para similares — "hay que probarlo en usos reales"

## 🔴 Conexión con el LAB (complementa el análisis ngram-mtp del 19-ago)

| Aspecto | Veredicto |
|---|---|
| **Futurible flags n-gram en llama-server** (anotado 19-ago) | 🔵 **REFORZADO con números reales**: n-gram = 200-260 tok/s SOLO en tareas iterativas con contexto similar (código, JSON repetitivo). Señal clara: batch diario que modifica/reutiliza plantillas |
| **MTP en Qwen 3.5** | 🟡 El lab usa LM Studio (MTP no expuesto como flag fácil). Si se probara llama.cpp directo, MTP da +36% gratis |
| **Borrador "0.8B inútil"** | ✅ Lección para el lab: NO mezclar modelos de familias distintas como draft (LFM como borrador de gpt-oss no serviría) |
| "Probar en usos reales" | ✅ Metodología del lab: batería de PRODUCCIÓN (5 tareas reales), no benchmarks sintéticos |

## Veredicto

**APORTA (refuerza futurible existente con datos reales)** — no es futurible NUEVO:
el n-gram/MTP ya estaba anotado el 19-ago (backup 20a). Lo que añade este vídeo:
(1) números reales de la comparativa (MTP +36%, n-gram 200-260 solo en contexto similar,
borrador 0.8B contraproducente); (2) la señal de activación del futurible n-gram se
concreta: **tareas batch iterativas con plantillas repetidas** (ej. informe diario, JSON
de evaluación, infografías re-renderizadas). Sigue SIN acción inmediata: LM Studio no
expone n-gram/MTP como flags simples y el lab no tiene la tarea batch 30-60 min diaria
que justificaría el cambio a llama.cpp directo.

## Nota honesta

Transcripción auto-subs (nombres: "Qen" = Qwen, "The Flash" = DeepSeek Flash? — el canal
no lo aclara, solo muestra la descarga de "The Flash" como borrador). Medidas en hardware
del canal (RTX 3060, llama.cpp, Windows) — referencia, no benchmark propio. El vídeo
prueba 1 modelo (Qwen 3.5 9B) — los resultados pueden no generalizar a otros tamaños.
