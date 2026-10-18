---
title: "SERIE LINKEDIN — \"LA IA QUE YO USO\""
type: research
---

# SERIE LINKEDIN — "LA IA QUE YO USO"
Guion maestro del proyecto · v3 · 01-sep-2026

## Qué es
Serie de carruseles educativos para LinkedIn (marca empleo IA) con el nombre
"La IA que yo uso". Doble objetivo: repasar conceptos para Joseba y demostrar
trabajo real con IA (no comentar noticias). Diferenciador: datos reales del
lab (hardware A2000 12 GB, Ollama, LM Studio, RAG, mediciones, gate de
veracidad) + honestidad sobre los límites del hardware.

## Reglas de la serie
1. Cadencia: 1 ficha/semana (lunes). Posts espontáneos cuando haya noticia
   grande o medición del lab (0-2/mes, sin calendario).
2. Colchón: mantener SIEMPRE 2 fichas terminadas de adelanto. Nunca publicar
   la última. Si una semana no se produce, el colchón absorbe.
3. Desdoblamiento: cada concepto se explica con ángulos distintos (4 patrones:
   concepto / cómo funciona / por qué importa / dato real del lab). Un ángulo
   = una ficha. Cada ficha debe ser AUTÓNOMA (entendible sin ver las demás).
4. Comparativas como ángulo propio: cuando haya 2+ opciones (herramienta,
   técnica, modelo), la comparativa es una ficha (tabla simple: cuándo cada
   una). Nunca "A es mejor que B" sin contexto de uso.
5. Anti-relleno: si dos fichas comparten el mismo gráfico central o el mismo
   mensaje, fusionar o cambiar el ángulo.
6. Dato real solo donde existe: no forzar medición del lab en cada ficha;
   donde no haya, el ángulo "por qué importa" sostiene la ficha.
7. Estructura por ficha (8-10 slides, patrón maurys): gancho → concepto en una
   frase → cómo funciona (diagrama) → por qué importa → dato real (si aplica)
   → error común/mito → CTA.
8. Sin datos personales: no publicar ubicación de casa, ids internos de BD,
   credenciales ni rutas internas. Genérico y compartible.
9. Verificación SIEMPRE: cada PNG con browser_vision (checklist por slide)
   antes de publicar. NO publicar sin verificación visual real.
10. Todo el trabajo del LAB es fuente de fichas: mediciones, OPs, crons,
    experimentos, fallos y evaluaciones. Incluido lo que NO se pudo
    implementar por hardware — esas fichas ("por qué no lo hicimos / qué
    haría falta") son las más honestas y las que nadie más puede escribir
    con datos propios.
11. Nadie replica el LAB: las fichas salen de trabajo real (logs, mediciones,
    evaluaciones, gate de veracidad), no de teoría. Si una ficha podría
    escribirla cualquiera con una búsqueda en Google, no es una ficha del
    LAB: cámbiala o añádele tu dato real.

## Fábrica de contenido: qué del LAB se convierte en ficha
Fuentes de fichas ya disponibles (no hace falta inventar temas):
- Router local→cloud (pipeline proxy, coste 0 tras 12:00)
- RAG del lab (26 GB → 320 MB, recall, latencias)
- Evaluación de alucinaciones (jueces, verificación de fidelidad)
- Gate de veracidad (cómo evito que el modelo invente)
- MCP servers (lab-db, lancedb, animation-server) y su integración
- Crons de vigilancia (Telegram, YouTube, watchdog de salud)
- Observabilidad del pipeline LLM (TTFB, latencias)
- LM Studio / Ollama / modelos locales (qué cabe en 12 GB y qué no)
- Deploys para clientes (despliegue de IA local)
- TFM / Founderz (lo aprendido en el máster, convertido en ficha)
- Fallos y correcciones (cada pitfall verificado es una ficha "error común")
- Tecnologías evaluadas pero NO implementadas por hardware (Bloque 6)

Regla: cada experimento/medición/fallo nuevo del LAB es una candidata a
ficha. Anotarla en este documento cuando ocurra.

## Pipeline de producción (ya validado en el lab)
- Guion: guion.json (o --demo) → generar_carrusel_linkedin.py
- Plantilla: plantilla-maurys.html (1080×1350, crema #F5EFE6 + negro + naranja)
- Render: Chrome headless con --virtual-time-budget=10000
- Verificar: browser_vision sobre file:// (fondo, título, logo, sin cortes)
- Salida: salidas/<fecha>-<slug>/slide-NN.png + guion.json
- Skill de referencia: linkedin-carrusel-lab

---

## MAPA DE CONTENIDO — 7 BLOQUES

### BLOQUE 0 — FUNDAMENTOS (el vocabulario mínimo)
Objetivo: que el espectador entienda los términos que usa todo el mundo mal.

1. IA / ML / DL
   - F1: Qué es cada uno y la diferencia (analogía: círculos concéntricos)
   - F2: Cómo se relacionan (diagrama: IA ⊃ ML ⊃ DL)
   - F3: Por qué todo el mundo dice "IA" cuando habla de ML (lenguaje vs realidad)
2. Cómo aprende una máquina
   - F4: Qué son los datos de entrenamiento (y por qué "basura entra, basura sale")
   - F5: Qué significa "entrenar": pérdida, gradiente, épocas (concepto)
   - F6: Overfitting vs underfitting: memorizar vs no aprender (analogía exámenes)
3. Qué es un LLM
   - F7: Qué es y qué hace de verdad (predice la siguiente palabra)
   - F8: Qué NO hace (no razona, no entiende — matices importantes)
   - F9: Por qué alucina y cómo se mitiga (concepto + trucos prácticos)
4. Arquitectura
   - F10: Qué es un transformer (la arquitectura de los LLM, concepto)
   - F11: La atención: qué mira el modelo cuando predice (cómo funciona por dentro)
   - F12: Parámetros y pesos: qué se guarda dentro de un modelo
5. Tokens y contexto
   - F13: Qué es un token (cómo se mide "lo que cabe")
   - F14: Qué significa el límite de contexto en la práctica
   - F15: Ventana de contexto vs memoria: por qué el modelo "se olvida"
   - F16: Conocimiento vs razonamiento: lo aprendido vs lo calculado al responder
6. Embeddings
   - F17: Qué es un embedding (palabra → números)
   - F18: Para qué sirve de verdad (búsquedas, similitud, RAG)
7. Sampling y temperatura
   - F19: Temperatura: entre "seguro" y "creativo" (los diales del modelo)
   - F20: Top-p y otros diales que casi nadie toca (y cuándo importan)
8. Entrenamiento vs fine-tuning vs inferencia
   - F21: Las 3 fases con analogía (aprender / especializarse / trabajar)
   - F22: Qué significa fine-tunear hoy (y cuándo NO hace falta — RAG suele bastar)
   - F23: Por qué la inferencia es lo que tú usas cada día (y cuesta dinero/VRAM)
9. La conversación
   - F24: Sistema vs usuario vs asistente: por qué el system prompt cambia tanto
   - F25: Contexto vs instrucción: qué se recuerda y qué se obedece

Subtotal Bloque 0: 25 fichas

### BLOQUE 1 — MODELOS Y NOTICIAS (leer titulares sin humo)
Objetivo: que el espectador sepa evaluar anuncios de modelos por sí mismo.

1. Cómo leer el anuncio de un modelo nuevo
   - F26: Qué mirar primero (tamaño, licencia, VRAM, benchmarks, datos de
     entrenamiento, fecha)
   - F27: Checklist del escéptico (qué preguntar antes de emocionarse)
2. Parámetros vs calidad
   - F28: Por qué "700B" no lo dice todo (parámetros ≠ inteligencia)
   - F29: Lo que de verdad cambia la experiencia (datos, alineación, cuantización)
3. Benchmarks
   - F30: Qué miden (y qué NO miden)
   - F31: Cómo se pueden manipular (contaminación, overfitting a benchmarks —
     conexión con evaluar alucinaciones del lab)
4. Open vs cerrado
   - F32: Licencias: lo que puedes y no puedes hacer con un modelo
   - F33: Por qué importa para empresas y para tu carrera (portabilidad)
5. Familias de modelos
   - F34: Quién es quién: LLaMA, Qwen, Mistral, DeepSeek, GPT, Gemini, Claude
   - F35: Comparativa: modelo gigante vs modelo pequeño (cuándo cada uno)
   - F36: Comparativa: frontier cloud vs local (coste, privacidad, latencia)
6. Multimodal
   - F37: Qué es multimodal (texto + imagen + audio + vídeo)
   - F38: Qué modelos lo hacen y qué cambia en el trabajo diario
7. El ritmo de las noticias
   - F39: Cómo filtrar ruido (qué merece tu atención y qué no — método)
   - F40: Dónde sigo yo las novedades (cron de canales Telegram/YouTube del lab)

Subtotal Bloque 1: 15 fichas

### BLOQUE 2 — IA LOCAL (territorio del lab, mayor valor diferencial)
Objetivo: demostrar que la IA local es viable, con datos reales.

1. Por qué correr modelos en casa
   - F41: Privacidad, coste, latencia, control (4 razones)
   - F42: Cuándo NO conviene (honestidad: cloud gana en algunos casos)
2. GPU y VRAM
   - F43: Qué significa 12 GB y qué cabe en ella (A2000 real)
   - F44: Cómo medir tu VRAM (nvidia-smi) — ficha práctica
3. Cuantización (GGUF)
   - F45: Cómo un modelo de 70B cabe en 12 GB (concepto: precisión vs tamaño)
   - F46: Qué se nota y qué no al cuantizar (dato real del lab si existe)
4. Ollama vs LM Studio
   - F47: Comparativa: cuándo usar cada uno (tabla + casos reales del lab)
   - F48: Arrancar un modelo local en 10 minutos (tutorial práctico)
   - F49: El API server: por qué "abrir LM Studio" no es "tener la API activa"
5. El router local→cloud
   - F50: Mi caso real: coste 0 después de las 12:00 (arquitectura del lab)
   - F51: Por qué un router de modelos es clave para trabajar con IA
6. Herramientas y APIs
   - F52: OpenAI-compatible API: el estándar que lo une todo
   - F53: Function calling / tools: que el modelo pueda "hacer cosas"
   - F54: MCP: el protocolo que conecta modelos con herramientas (concepto)
   - F55: Comparativa: misma tarea en local vs cloud (tiempo, coste, privacidad)
7. Caso real del lab (ficha estrella)
   - F56: Pipeline completo de consulta local con mediciones (end-to-end)

Subtotal Bloque 2: 16 fichas

### BLOQUE 3 — PROMPTING ENGINEERING (bloque propio, muy expandido)
Objetivo: desmontar la magia y dar técnicas que funcionan, con comparativas.

1. Fundamentos
   - F57: Qué es un prompt y por qué a veces importa más que el modelo
   - F58: Estructura de un buen prompt (rol, contexto, tarea, formato, ejemplo)
2. Técnicas básicas
   - F59: Zero-shot: pedir sin ejemplos (cuándo basta)
   - F60: Few-shot: dar ejemplos (cuándo mejora y cuántos)
   - F61: Role prompting: decirle quién es (ventajas y límites)
   - F62: Salida estructurada: pedir JSON, tablas, listas (formato = control)
3. Técnicas avanzadas
   - F63: Chain-of-Thought: "piensa paso a paso" (qué hace y qué NO)
   - F64: Self-consistency: pedir varias respuestas y votar (concepto)
   - F65: ReAct / prompting agéntico: razonar + actuar
   - F66: Structured output: forzar esquema (JSON schema) en la práctica
   - F67: Negative prompting: decir qué NO hacer (límites reales de la técnica)
4. Comparativas de prompting
   - F68: Comparativa: zero-shot vs few-shot vs CoT (cuándo cada uno)
   - F69: Comparativa: prompting vs fine-tuning vs RAG (la gran tabla)
   - F70: Comparativa: prompt largo con contexto vs prompt corto (coste vs precisión)
   - F71: Errores comunes: sin contexto, ambiguos, sobre-pedir (con ejemplos)
5. Prompting en el lab
   - F72: Cómo escribo yo los prompts del lab (patrones que uso a diario)
   - F73: El gate de veracidad: cómo obligo al modelo a no inventar (caso real)

Subtotal Bloque 3: 17 fichas

### BLOQUE 4 — UTILIDADES Y PRÁCTICA (para qué sirve todo esto)
Objetivo: aplicaciones concretas y medibles.

1. RAG
   - F74: Qué es RAG (darle memoria sin reentrenar) — concepto
   - F75: Mi caso real: 26 GB → 320 MB sin tocar una fila (carrusel existente)
   - F76: Cuándo usar RAG y cuándo NO (límites honestos)
   - F77: Comparativa: RAG vs fine-tuning (cuándo cada uno)
   - F78: Búsqueda semántica vs palabras clave: embeddings vs LIKE
2. Agentes
   - F79: Qué son (y qué NO son) hoy
   - F80: Qué pueden hacer ya (automatización con límites claros)
   - F81: Comparativa: agentes vs workflows
   - F82: Agentes + tools: el function calling aplicado
   - F83: Límites honestos: cuándo NO delegar en un agente
3. Automatización con n8n
   - F84: Workflows que combinan IA y acciones (concepto + ejemplo)
   - F85: Mi caso real (un workflow del lab, sin datos internos)
4. IA en el día a día
   - F86: 5 usos reales y medibles (sin humo)
   - F87: Comparativa: flujo manual vs flujo con IA (tiempo y coste)
   - F88: Verificación: cómo comprobar que la IA no alucinó (gate del lab)
5. Cierre
   - F89: Cierre de temporada: qué he aprendido haciendo esta serie

Subtotal Bloque 4: 16 fichas

### BLOQUE 5 — MULTIMODAL Y CREACIÓN (territorio del lab)
Objetivo: mostrar que la IA no es solo texto, con casos reales del lab.

1. Visión
   - F90: Modelos de visión: qué ven y qué NO ven (GLM real del lab)
   - F91: Verificación visual con IA: revisar renders e infografías (uso real)
2. Audio y voz
   - F92: Transcripción y TTS local (Whisper, dictado — lab real)
   - F93: Comparativa: transcribir en local vs cloud (privacidad vs velocidad)
3. Generación de imágenes
   - F94: ComfyUI y generación 100% local (lab real)
   - F95: IA generativa: qué crea y qué alucina visualmente (límites)
4. Ética de la creación
   - F96: ¿Es "tu" trabajo si lo hace la IA? (marca personal, honestidad)
   - F97: Cómo etiquetar contenido generado (transparencia profesional)

Subtotal Bloque 5: 8 fichas

### BLOQUE 6 — LO QUE EL HW NO NOS DEJÓ (y lo que aprendimos)
Objetivo: honestidad técnica. Tecnologías que el LAB evalúa o conoce pero NO
implementa por límites de hardware. Fichas de "qué es / por qué no lo hacemos
/ qué haría falta / qué aprendimos" — nadie más puede escribirlas con datos
propios.

ESTADO REAL VERIFICADO (01-sep-2026, comandos en vivo, no memoria):
- HW: RTX A2000 12 GB (12282 MB; con LM Studio cargado quedan ~2,6 GB),
  CPU i5-9500 6 núcleos, RAM 30 GiB (swap 8 GiB casi lleno en carga).
- FUNCIONA AHORA: Ollama v0.32.13 (API 11434), LM Studio (backend llama.cpp
  en VRAM), ComfyUI instalado en ~/ComfyUI, RAG LanceDB en joko-lab/.lancedb,
  pipeline de evaluación de alucinaciones propio del lab.
- NO INSTALADO (verificado): vLLM, lm-eval-harness, whisper en PATH global.
- Imposible con este HW: pre-training desde cero, 70B+ sin cuantizar
  (fp16 ≈ 140 GB VRAM; Q4 ≈ 40 GB — ni cuantizados caben en 12 GB).

1. Servir modelos grandes a alto rendimiento
   - F98: vLLM y serving de alto rendimiento (qué es; por qué no con 12 GB
     para modelos grandes; qué haría falta — verificado: no instalado)
   - F99: Comparativa: servir con llama.cpp/Ollama vs vLLM (cuándo cada uno;
     el lab sirve con llama.cpp/Ollama hoy)
2. Fine-tuning y entrenamiento
   - F100: Fine-tuning real: qué implica y por qué no es la vía del lab hoy
     (RAG suele bastar; no implementado — conocimiento, no intento)
   - F101: Pre-training desde cero: fuera de alcance HW (imposible con
     A2000 12 GB) — y por qué no lo necesitas (honestidad que casi nadie dice)
3. Modelos que no caben
   - F102: Modelos 70B+ sin cuantizar en local (números reales: fp16 ≈ 140 GB,
     Q4 ≈ 40 GB — imposible en 12 GB; el lab usa 7-14B)
   - F103: Multimodales grandes locales (el lab usa GLM-4.6V flash; los de
     visión pesados no caben cómodos en 12 GB con el LLM cargado)
4. Cargas pesadas
   - F104: Benchmarks pesados (lm-eval-harness: verificado no instalado; el
     lab evalúa alucinaciones con pipeline propio — por qué)
   - F105: Whisper grande en local (CPU vs GPU: el lab transcribe en CPU;
     whisper no está en PATH global — instalación de proyecto)
   - F106: Generación de imágenes con modelos grandes (ComfyUI instalado:
     qué cabe en 12 GB y qué no)
5. Escala
   - F107: RAG a escala masiva (el lab tiene LanceDB funcional ~21K filas;
     millones de documentos: qué limita — RAM 30 GB e índice)
   - F108: Agentes con contexto enorme (VRAM/contexto: dónde está el techo
     con 12 GB)
6. Cierre del bloque
   - F109: Comparativa: lo que sí hacemos vs lo que no pudimos (tabla honesta)
   - F110: "Por qué 12 GB definen mi forma de trabajar" (cierre con datos
     reales: 12282 MB, 6 núcleos, swap al límite en carga — muy diferencial)

Subtotal Bloque 6: 13 fichas

---

## FICHA NUEVA (01-sep-2026, inspirada en reel ai_vatika "Modern Ecosystem Tools")

F111: **"El ecosistema AI que YO uso de verdad"** — mapa del stack real del lab
(no copia del cheat sheet genérico; diferenciador = datos reales).
Bloque: 4 (Utilidades y práctica) / puente de presentación de la serie.
Estado: guion.json creado, render pendiente.

---

## TOTALES
- Bloque 0 (Fundamentos): 25 fichas
- Bloque 1 (Modelos y noticias): 15 fichas
- Bloque 2 (IA local): 16 fichas
- Bloque 3 (Prompting engineering): 17 fichas
- Bloque 4 (Utilidades y práctica): 16 fichas
- Bloque 5 (Multimodal y creación): 8 fichas
- Bloque 6 (Lo que el HW no nos dejó): 13 fichas
- TOTAL SERIE: 110 fichas

A 1 ficha/semana con colchón de 2 → ~2,2 años de contenido programado
(sin contar posts espontáneos, desdobles por feedback ni comparativas nuevas
que surjan de noticias o del trabajo diario del LAB).

## COMIENZO (colchón inicial)
1. F1: "IA / ML / DL — qué es cada uno y la diferencia" (piloto del bloque 0)
2. F2: "Cómo se relacionan IA, ML y DL" (diagrama círculos concéntricos)
3. F3: "Por qué todo el mundo dice IA cuando habla de ML"

Decisión pendiente: arrancar por Bloque 0 (lógico, progresión) o por Bloque 2
(impacto inmediato, diferenciador). Recomendación: Bloque 0 para que la serie
tenga hilo; el Bloque 2 se usa como gancho en el CTA ("pronto: IA local de
verdad, con datos").

## PRÓXIMOS PASOS
- [x] Confirmar Bloque 6 con estado real verificado (01-sep-2026): vLLM y
      lm-eval-harness no instalados; Ollama/LM Studio/ComfyUI/RAG funcionan;
      pre-training y 70B+ sin cuantizar imposibles en 12 GB (datos en bloque)
- [ ] Decidir ficha piloto y montar guion.json + render + verificación
- [ ] Mantener este documento actualizado: tachar fichas publicadas, añadir
      desdobles nuevos que surjan del feedback
- [ ] Revisar al terminar cada bloque: ¿ángulo funciona? ¿se desdobla más?
