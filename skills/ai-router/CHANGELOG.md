# ai-router — Changelog

## 2026-07-07 — v0.4.0

- Avanzada a etapa 3 (Actuar):
  - Creado script `ai-router.py` con enrutamiento automático
  - Detecta: privacidad, razonamiento, visión, consulta simple
  - Rama simple: ✅ consulta a Ollama funcional
  - Rama visión: ✅ consulta a LM Studio funcional
  - Rama diagnóstico: ✅ muestra VRAM, RAM, modelos disponibles
  - Detecta VRAM baja y modelos no cargados
  - Actualizados ROADMAP, COMMANDS.md

- Avanzada a etapa 2 (Diagnosticar):
  - Testeados 3 modelos de Ollama: qwen2.5:7b (15.87s), llama3.1:8b (18.32s), llama31-8b-64k (1.92s)
  - Confirmado llama31-8b-64k como modelo local más rápido para consultas simples
  - Comparativa razonamiento complejo: DeepSeek gana vs local (5.23s, respuesta incorrecta)
  - Verificados modelos de LM Studio: 6 modelos VLM disponibles
  - Cargado y testeado google/gemma-4-e4b: 0.25-0.58s texto, visión funcional
  - Árbol de decisión actualizado con LM Studio como alternativa local a Gemini
  - Umbrales de VRAM ajustados según hardware real (10.9 GB libres)

## 2026-07-07 — v0.2.0

- Poblada skill completa en etapa 1 (Comprender):
  - **SKILL.md:** criterios de enrutamiento reales (privacidad → Ollama, razonamiento → DeepSeek, multimodal → Gemini, recursos → ligero)
  - **README.md:** descripción detallada, dependencias actualizadas con Gemini y VRAM
  - **KNOWLEDGE.md:** árbol de decisión completo, umbrales de VRAM, tareas típicas por proveedor
  - **COMMANDS.md:** comandos de diagnóstico y enrutamiento manual
  - **SAFETY.md:** reglas de seguridad extendidas con Gemini, VRAM y modelo ligero
  - **ROADMAP.md:** tareas actualizadas para etapas 2, 3 y 4
  - **CHANGELOG.md:** este archivo

## 2026-07-05 — v0.1.0

- Creación de la skill en etapa 1 (Comprender)
- Archivos creados: SKILL.md, README.md, KNOWLEDGE.md, COMMANDS.md, SAFETY.md, ROADMAP.md, CHANGELOG.md
