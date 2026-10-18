---
title: "Análisis — Liquid AI QAD (Nichonauta, 23-ago-2026)"
type: research
---

# Análisis — Liquid AI QAD (Nichonauta, 23-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/Ywet5Kh3dZs (Nichonauta, 23-08-2026, 8:59 min, 1.274 views)
**Método:** subtítulos ES descargados (73 KB) → deduplicados (24K→8K chars) → análisis completo

## Qué es QAD (Quantization-Aware Distillation)

Liquid AI publicó puntos de control **QAD** de su serie LFM 2.5: modelos **fine-tuneados específicamente para ser cuantizados a 4 bits** sin perder calidad. La técnica:

```
Modelo maestro (BF16) → destilación con conciencia de cuantización → modelo estudiante Q4
```

- **Recupera ~99% del promedio BF16** (cierra la brecha de calidad que la cuantización normal pierde)
- Pesa **~25% del modelo completo**, mantiene **~97% de la calidad**
- No es una cuantización simple: es un **ajuste adicional** para que el modelo "recuerde" lo que sabía antes de cuantizar
- Mismo enfoque que Google con Gemma

## Datos reales del vídeo (LFM 2.5 1.2B Instruct QAD)

| Métrica | Valor |
|---|---|
| Tamaño | **696 MB** (vs 2.34 GB completo) |
| VRAM | **1.2 GB** |
| Velocidad GPU | **~260 tok/s** |
| Velocidad CPU AMD | 239 tok/s |
| Velocidad móvil NPU | 82 tok/s |
| Contexto | 32.768 |
| Idiomas | 8 (español bien representado) |
| Tool calling | ✅ Sí (llamada a funciones) |
| KV cache | Cuantizable a Q8 (reduce aún más) |

Pruebas del vídeo: 1000 tokens en 3.6s · responde bien en español · extracción de datos con formato específico ✓.

## Mapeo contra el LAB — 🔴 CONEXIÓN DIRECTA

| Aspecto | Estado |
|---|---|
| **LFM 2.5 ya en uso** | ✅ El lab usa **LFM 2.5 2.6B** (validado 7/7 batería, 55 tok/s) — es la MISMA familia |
| **Novedad** | Las versiones QAD (1.2B/2.6B) son NUEVAS — no las tiene el lab |
| **VRAM** | 1.2 GB → **cabe JUNTO a GLM (9.5 GB): 10.7 < 12 GB** — rompe el patrón "un modelo a la vez" |
| **Caso de uso** | Tareas de lenguaje ligeras que hoy usan GLM (9.5 GB) podrían bajar a LFM QAD (1.2 GB) → GLM libre para visión |
| **Coste** | 0 € (local) |

## Veredicto: VALOR MEDIO-ALTO — futurible ACCIONABLE con datos

1. **Es de la familia que el lab YA valida** (LFM 2.5), con la ventaja Q4 sin pérdida → misma calidad, 1/4 del peso.
2. **El dato 1.2 GB VRAM es el más interesante**: permite tener UN SEGUNDO modelo cargado junto a GLM en la A2000 (10.7 < 12 GB) — exactamente lo que el lab no podía con gpt-oss (14.9 GB).
3. **Señal de activación**: si aparece una tarea de lenguaje ligera y frecuente (clasificación, extracción, formateo) que hoy consume GLM, probar LFM 2.5 1.2B QAD (696 MB) o 2.6B QAD.
4. **Sin acción inmediata**: el lab ya tiene LFM 2.6B (55 tok/s) cubriendo ese rol — el QAD es una mejora de eficiencia, no un salto de capacidad.

**Futurible anotado**: probar LFM 2.5 QAD (1.2B o 2.6B) como modelo de lenguaje ligero residente junto a GLM (swap automático de jueces / tareas batch de lenguaje). Señal: tarea recurrente de lenguaje que no necesite GLM.
