---
title: "Análisis — Gemma 4 26B A4B con llama.cpp en GPU pequeña (Nichonauta)"
type: research
---

# Análisis — Gemma 4 26B A4B con llama.cpp en GPU pequeña (Nichonauta)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 10-ago-2026
**Fuente:** https://www.youtube.com/watch?v=Rq-b5umGldY — Nichonauta (26 min)
**Tema:** Cómo cargar y afinar un modelo GRANDE (26B) en una GPU pequeña (RTX 3060 12 GB)

---

## Qué muestra el vídeo

Gemma 4 26B A4B (mezcla de expertos, solo 4B activos por token) cabe en 12 GB
con llama.cpp usando técnicas específicas:

### Setup (3 archivos)
1. Modelo GGUF **dynamic Q4_XL** (solo existe en 4 bits — Q5-Q8 no aportan calidad)
2. **mmproj** (encoder de visión) en BF16
3. **MTP** (multi-token prediction — modelo borrador) en Q4

### Técnica clave: `--cmoe` / `--nmoe`
- `--cmoe` = TODAS las capas de expertos a CPU/RAM (solo los expertos; el resto del modelo sigue en GPU)
- `--nmoe N` = N capas de expertos a CPU (N=31 = lo mismo que cmoe; bajar N = más expertos en GPU)
- Ajuste fino: bajar N hasta dejar **~1 GB libre** de VRAM (margen de seguridad)

### Optimizaciones de velocidad
1. **Speculative decoding con MTP** — el modelo borrador predice 1-4 tokens; el grande acepta/rechaza. Valor óptimo probado: **3** (el 4 fue inestable)
2. **KV cache en Q8** (`--cache-type-k/v q8_0`) — mitad de VRAM de contexto, ~sin pérdida de calidad (rotación de atención tipo Turbo Quant de Google)
3. Resultado final: **~40-43 tok/s** sostenidos tras +3000 tokens

### Resultados medidos
| Config | Velocidad |
|---|---|
| Sin MTP (solo cmoe) | 23 tok/s |
| Con MTP=1 | 26-27 tok/s |
| Con MTP=2 | 28-30 tok/s |
| Con MTP=3 | ~30 tok/s (óptimo) |
| Con MTP=4 | inestable (peor) |
| nmoe 19 + KV Q8 | **40-43 tok/s** |

### Nota del autor
- Los valores (MTP=3, nmoe=19) son ESPECÍFICOS de su hardware — hay que probar
- Qwen 3.6 35B A3B es el siguiente candidato (más inteligente, 3B activos, también con MTP) — próximo vídeo
- **LM Studio/Ollama NO dan este control** — llama.cpp es necesario para cmoe/nmoe

---

## 🎯 Aplicación al LAB

### El lab tiene la misma GPU (RTX A2000 12 GB)

| Aspecto | Lab hoy | Con esta técnica |
|---|---|---|
| Modelo principal local | R1-14B (11 tok/s) | **Gemma 26B A4B (~40 tok/s)** — 4x más rápido |
| Control de carga | LM Studio (sin cmoe/nmoe) | llama.cpp (control total) |
| Modelo cargado ahora | R1 (8.5 GB) | Gemma 26B cabría con cmoe |

### Veredicto honesto

**Esto es MUY relevante para el lab** — cambia la ecuación del router local/cloud:

1. **R1-14B → 11 tok/s** (medido 09-ago). **Gemma 26B A4B → 40+ tok/s** con mejor calidad. **4x de ganancia** con el mismo hardware.

2. **El trade-off de VRAM:** el lab usa LM Studio (7.4 GB GLM + 8.5 GB R1 no caben juntos). Con llama.cpp + Gemma 26B, se libera todo ese espacio → **podría caber Gemma 26B + GLM 4.6V para visión**.

3. **Para el router local/cloud:** un modelo local de 40 tok/s con calidad 26B (calidad que en el 90% de tareas "reemplaza a modelos frontera" según el autor) haría que MÁS tareas batch sean viables en local — y las interactivas también.

### ⚠️ PERO — 3 salvedades

| Salvedad | Detalle |
|---|---|
| **LM Studio vs llama.cpp** | El lab usa LM Studio (skill lm-studio, arranque autónomo autorizado). Cambiar a llama.cpp = nuevo runtime, nueva configuración. Decisión no trivial. |
| **Descarga** | Gemma 26B A4B ≈ 14.3 GB (sin MTP) — ocupa disco, hay que descargarlo |
| **Ajuste** | Los valores (MTP=3, nmoe=19) hay que probarlos en la A2000 — no son copia-pega |

### Recomendación

**NO cambiar ahora** (el lab está estable, R1 validado para batch). **PERO anotarlo como experimento prioritario** — la ganancia de 4x velocidad + mejor calidad justifica una prueba real cuando el lab quiera subir de nivel en local.

## Referencia técnica rápida (para el experimento futuro)

```bash
# llama.cpp server con Gemma 26B A4B en 12 GB
llama-server -m gemma-4-26b-a4b-it-Q4_XL.gguf \
  --mmproj gemma-4-26b-a4b-mmproj-f16.gguf \
  --mtp gemma-4-26b-a4b-mtp-Q4.gguf \
  -ngl 999 --nmoe 19 \
  --cache-type-k q8_0 --cache-type-v q8_0 \
  -c 131072
```
