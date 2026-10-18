---
title: "Análisis — Kimi Cat 3: ¿es posible correr un modelo de 2.78B en CPU? (vídeo YT)"
type: research
---

# Análisis — Kimi Cat 3: ¿es posible correr un modelo de 2.78B en CPU? (vídeo YT)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 11-ago-2026
**Fuente:** https://youtu.be/1o_JvhCk-gw — vídeo de divulgación técnica (transcripción completa)
**Tema:** Moonshot subió Kimi Cat 3 (27-jul): 2.78 billones de parámetros, MoE,
1M contexto, multimodal, MXFP4 nativo. Alguien lo corrió en CPU con 8.24 GB RAM.

---

## El contenido

### La noticia
- **Kimi Cat 3** (Moonshot, 27-jul-2026): modelo open source más grande hasta
  la fecha. 2.78B parámetros (billones), 1M tokens contexto, multimodal nativo.
- Nivel frontera: #1 Front End Code Arena, #2 Balce AI, #3 Artificial Analysis
  (tras Claude y GPT-5.6), más barato que ambos.
- Alguien lo corrió en una sola máquina (9h después), otro en 29 GB RAM (1 día),
  y un investigador en Karachi lo bajó a **8.24 GB** — CPU, 0 GPUs, 6 archivos C
  compilados en un binario de 176 KB.

### Arquitectura (por qué es posible aritméticamente)
- **MoE**: 93 capas, 896 expertos, 16 activos por token → **3.7% activo**
  (104M activos de 2.78B). El 96% está "dormido" en cada instante.
- **Matizoro clave**: el enrutador decide qué expertos usar MIENTRAS computa la
  capa — no se sabe con antelación. Los 896 deben ser accesibles rápido. La
  dispersión sola no regala nada.

### Las 4 reducciones de ingeniería
1. **MXFP4** (0.53 bytes/peso): 4 bits indexan tabla de 16 valores + exponente
   de 8 bits por grupo de 32. 1.44 TB = 93% del checkpoint. El motor NUNCA
   descomprime (un experto 17.5 MB → 132 MB en FP32; descomprimir todos serían
   194 GB/token).
2. **Kimi Delta Attention** (69 capas): memoria de tamaño FIJO por cabeza —
   NO crece con la longitud del contexto (10 tokens o 1M = igual).
3. **Multi-Latent Attention** (24 capas globales): proyectan a un latente de
   576 dims → 53x menos memoria, salida matemáticamente idéntica. Contexto a
   ~2.37 MB/posición.
4. **Swap a disco**: el tronco (113 GB, sin cuantizar, sin dispersión) NO se
   sostiene entero — N capas en RAM + ranura rotatoria que lee del disco.

### LA TRAMPA (demostrada al final)
- No elimina trabajo: **lo mueve al disco**.
- Preset pequeño: 3 GB tronco en RAM (3% aciertos), 105 GB leídos de disco
  POR CADA TOKEN, a 5.4-6.1 GB/s sostenido → **32.69 s/token** (8 tokens en
  261.5s).
- Una respuesta de 500 palabras (~650 tokens) ≈ **6 horas**.

---

## 🎯 Aplicación al LAB — VEREDICTO

### ¿Es posible en el lab? NO vale la pena (datos)
| Requisito | Kimi Cat 3 CPU | Lab (A2000+i5-9500) |
|---|---|---|
| RAM | 8-29 GB solo modelo | 30 GB total |
| Disco NVMe | 5.4-6.1 GB/s sostenido | ~2-3 GB/s (mitad) |
| Velocidad | 32.69 s/token (ya inutilizable) | **60+ s/token** (peor) |
| Respuesta 500 palabras | 6 horas | 12+ horas |

Incluso replicando la hazaña exacta, sería 100x más lento que R1-14B local
(11 tok/s) y miles de veces más lento que DeepSeek cloud.

### Lo que SÍ aporta (conocimiento)
1. **Confirma el límite del MoE en hardware modesto** (validado con Qwen 35B:
   los expertos dormidos no regalan velocidad; el enrutador necesita acceso
   rápido a todos).
2. **MXFP4 nativo** (cuantizado desde entrenamiento) = el futuro de la
   cuantización; si llega a modelos pequeños, R1-14B en 4 bits nativo sería
   más rápido.
3. **Delta Attention / MLA**: si llama.cpp/LM Studio los incorporan, el
   contexto largo dejaría de comer memoria (relevante para el RAG local).
4. **Swap a disco**: ya lo usamos (offload Qwen a CPU); el vídeo confirma el
   límite — solo demo, no uso real.

## Conclusión
Kimi Cat 3 en CPU es una hazaña de ingeniería impresionante ("se puede"),
pero NO es una herramienta usable (32-60+ s/token). El lab ya tiene lo mejor
para su hardware: R1-14B + router + paralelismo. Futurible: vigilar MXFP4 +
Delta Attention en llama.cpp/LM Studio para modelos pequeños.

## Futuribles anotados
- Vigilar MXFP4 nativo en GGUF de modelos pequeños
- Vigilar Delta Attention / MLA en llama.cpp/LM Studio (contexto largo sin
  comer memoria — relevante para RAG)
