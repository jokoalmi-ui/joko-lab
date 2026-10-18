---
title: "Análisis — Tutorial llama.cpp: Configurar Modelos de IA con Máximo RENDIMIENTO (Nichonauta, video YT 13-ago-2026)"
type: research
---

# Análisis — Tutorial llama.cpp: Configurar Modelos de IA con Máximo RENDIMIENTO (Nichonauta, video YT 13-ago-2026)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 2026-08-13 08:59 CEST (verificada con `date`)
**Fuente:** https://youtu.be/FMuUEe-QWXg — Nichonauta
**Título:** "Configurar Modelos de IA con Máximo RENDIMIENTO 🐑 Tutorial en llama.cpp"
**Estado:** ✅ ANALIZADO CON TRANSCRIPCIÓN (la transcripción estaba bloqueada por rate-limit de YouTube el 12-ago; 24h después se obtuvo completa, 26.393 chars, español)
**Duración:** 24:47

---

## Qué dice el vídeo (solo lo que aparece en la transcripción)

**Tesis:** LM Studio (y otros frontends) usan llama.cpp por debajo, pero una
versión desactualizada y más simple. Ejecutar llama.cpp directamente da el
potencial completo: actualizado, personalizable, y permite pasar de ~3
tokens/s a >40 tokens/s solo configurando bien. El tutorial no es sobre Gemma
4: es sobre CÓMO ELEGIR y CONFIGURAR un modelo para un hardware concreto.

### 1. Elegir el binario según hardware
- CPU-only → versión CPU; GPU AMD → Vulkan o ROCm; GPU NVIDIA → versión CUDA.
- El autor usa RTX 3060 12GB + RX 6600 8GB + 64GB RAM; descarga CUDA 13.3.
- Estructura de carpetas: `bin/` (ejecutables), `GGUF/` (modelos), `ZIP/`
  (binarios originales por si acaso).

### 2. Elegir el modelo (regla de dedo)
- Modelos recomendados para hardware de hogar: **Gemma y Qwen** (siguen
  funcionando bien a tamaño reducido).
- Estimación de peso: parámetros × 2 ≈ GB a 16 bits → a 8 bits = mitad → a 4
  bits = cuarta parte. Ejemplo del vídeo: Qwen 3.5 9B → 18 GB (16b) / 9 GB
  (8b) / 4.5 GB (4b). Gemma 4 12B → 24 GB (16b) / 12 GB (8b) / 6 GB (4b).
- Regla: **el más grande que quepa al menos a 4 bits**. Menos de 4 bits ya
  pierde bastante calidad. Ejemplo: para 12 GB VRAM, Qwen 3.5 9B Q4 (4.5 GB)
  o Gemma 4 12B Q4 — comparados por benchmark están a la par (la KV cache del
  Qwen 3.5 9B pide más, así que ambos son válidos).
- El 9B a 4 bits puede ser mejor elección que el 4B a 8 bits ("el más grande
  que podamos cargar cuando menos a 4 bits").

### 3. Gemma 4 + QAT (clave de calidad)
- Los modelos Gemma 4 tienen variantes **QAT** (quantization-aware training):
  entrenados para ser cuantizados a 4 bits manteniendo inteligencia
  equivalente al original, pesando una cuarta parte.
- En Hugging Face, la versión GGUF cuantizada suele ser de **unsloth**
  (cuantización dinámica: casi todo a 4 bits, con partes a 8/16 bits para
  mantener calidad — p.ej. IQ4_XS). Gemma 4 12B QAT GGUF: 6.72 GB en HF,
  6.3 GB descargado.
- Con QAT + cuantización dinámica: ~99.9% de la calidad original pesando una
  cuarta parte.

### 4. Los tres archivos del modelo (Gemma 4 12B)
1. **Modelo GGUF** QAT a 4 bits (unsloth, ~6.3 GB).
2. **mmproj** (proyector de visión): 175 MB BF16 — da visión (imagen, audio,
   video) con muy poco peso comparado con otros modelos.
3. **MTP (multi-token prediction) / speculative decoding**: modelo borrador
   que predice los siguientes tokens; el modelo grande solo verifica y
   corrige. Gana 50-300% de velocidad (el autor reporta hasta 300% con 254 MB
   adicionales). En Q4 le da MÁS velocidad real que sin cuantizar (pesa una
   cuarta parte). En Qwen, el MTP va DENTRO del archivo del modelo; en Gemma
   es archivo aparte.
- Total de los 3 archivos: 6.65 GB → cabe en una GPU de 12 GB con ventana de
  contexto de 262.144 tokens.

### 5. El comando de ejecución (llama-server) — parámetros mencionados
El autor muestra el .bat con el comando, pero NO lo pega (caracteres no
permitidos en descripciones de YT; sugiere captura de pantalla + LLM con
visión para transcribirlo). De la transcripción se identifican estos
parámetros (solo los que aparecen nombrados o descritos):
- **`llama-server`** (el ejecutable) con el modelo GGUF, el mmproj y el
  modelo borrador MTP.
- **Parámetro numérico a tunear (no nombrado en la transcripción; el autor
  probó valores 1-4 y en su caso 4 dio más velocidad)**: "tenemos que ir
  probando con el valor de 1 2 3 4 hasta donde veamos que en vez de seguir
  mejorando la velocidad empieza a empeorar".
- **100% de capas en GPU**: no quiere que llama.cpp divida el modelo
  automáticamente entre dispositivos (equivalente a `-ngl` alto).
- **Cache de contexto en RAM**: los contextos/conversaciones ya procesados se
  cachean temporalmente en RAM para copiar/pegar en vez de reprocesar.
- **Cadena de razonamiento activada** (thinking del modelo).
- **Ventana de contexto 131.072 tokens** (el modelo soporta hasta 262.144).
- **Parámetros de sampleo recomendados por Google** para Gemma 4 (no
  detallados en la transcripción).
- **Una única respuesta en simultáneo** (slots paralelos = 1): si llega otra
  solicitud, espera a que termine la primera.
- **Logs de llama.cpp en línea de comandos** y **alias del modelo**.

### 6. Turbo Quant / KV cache cuantizada (segunda parte del comando)
- Añade líneas para **cuantizar la KV cache** (la memoria de la ventana de
  contexto) del modelo Y del borrador MTP a **8 bits (Q8)** → requiere la
  mitad de memoria → permite **duplicar la ventana de contexto a 262.144**
  (el máximo del modelo).
- llama.cpp incluye **rotación de atención estilo Turbo Quant** (paper de
  Google): mitad de memoria manteniendo ~99% de calidad.
- Resultado medido: modelo 9.8 GB sin cuantizar KV → 10.9 GB con KV Q8 +
  ventana completa en una GPU de 12 GB. Deja ~1 GB libre, que el autor
  recomienda porque al generar tokens/ver imágenes puede requerir picos de
  memoria.

### 7. Resultados y uso
- Velocidad: hasta **110 tokens/s generando código** con MTP activo.
- Uso: chat en `localhost:8080` (URL del servidor), visión de imágenes, y
  cualquier cliente/agente: ChatGPT Desktop con modelos locales, OpenCode,
  PAgent, AnythingLLM, agentes estilo Hermes Agent, o código propio.

---

## 🎯 Aplicación al LAB

**Hardware del lab:** RTX A2000 12GB (misma VRAM que la RTX 3060 12GB del
vídeo) + LM Studio como motor de inferencia local (que envuelve llama.cpp).
Los aprendizajes se dividen en dos capas:

### A. Selección de modelo (aplicable directamente hoy)
- La regla "parámetros × 2 a 16b → /4 a 4b" y "el más grande que quepa al
  menos a 4 bits" es el criterio correcto para el A2000 de 12 GB. Gemma y
  Qwen siguen siendo las familias adecuadas para hardware de hogar.
- **Gemma 4 12B QAT** es el caso estrella del vídeo: 6.3 GB Q4 + 175 MB
  mmproj + MTP = 6.65 GB, con visión barata y KV cache ligera. Encaja en la
  A2000 igual que en la 3060. Es candidato a evaluar como modelo de
  inferencia del lab si LM Studio lo carga (GGUF QAT de unsloth es estándar).
- Qwen 3.5 9B Q4 (4.5 GB) como alternativa con KV cache más exigente.

### B. Flags de rendimiento (según cómo se ejecute)
- **Si el lab usa LM Studio:** LM Studio expone en su UI varios de estos
  controles (capas en GPU, tamaño de contexto, cuantización de KV cache en
  versiones recientes). **Verificar qué expone la versión instalada antes de
  asumir** — no está confirmado que LM Studio del lab exponga MTP/draft model
  ni rotación de atención Turbo.
- **Si el lab usa llama.cpp CLI directo** (opción para máximo rendimiento,
  como propone el vídeo): aplicar `-ngl` completo, cache de contexto en RAM,
  `-c` según modelo, KV cache Q8 + rotación de atención Turbo para doblar el
  contexto, y MTP si el modelo tiene variante (Gemma 4: archivo aparte;
  Qwen: incluido).
- Regla del **~1 GB libre** en la A2000 (12 GB): no llenar la VRAM al 100%.
- El **MTP/speculative decoding** es la palanca de velocidad más grande del
  vídeo (hasta 3x). El lab ya optimiza con paralelismo + router; un draft
  model bien elegido es ortogonal y compatible.

### Veredicto honesto
- Alta relevancia: valida el criterio de selección de modelo del lab y abre
  una vía de rendimiento (MTP + KV Q8 + Turbo attention) que el lab puede
  aplicar si LM Studio lo expone o si se usa llama.cpp directo.
- No hay acción inmediata obligatoria: el lab ya tiene inferencia operativa;
  esto es una optimización a evaluar, no un fix.

### Futurible
🟢 **Evaluar Gemma 4 12B QAT (GGUF unsloth) + mmproj en LM Studio del lab**
(A2000 12GB): 6.3 GB Q4 con calidad ~original por QAT, visión de 175 MB y KV
cache ligera — encaja en la VRAM actual. Incluye probar si la versión de LM
Studio expone KV cache Q8 y draft model (MTP); si no, evaluar llama.cpp CLI
directo como backend de máximo rendimiento.

## Nota técnica
- Transcripción obtenida 13-ago 08:59 CEST (24h después del bloqueo 429 del
  12-ago) — la IP ya no estaba rate-limited. `--language es` funcionó a la
  primera.
- Fechas/horas verificadas con `date` (Europe/Madrid): 2026-08-13 08:59 CEST.
