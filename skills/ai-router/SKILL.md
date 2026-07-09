---
name: ai-router
description: Enrutamiento inteligente entre modelos de IA locales y externos según la tarea.
version: 0.3.0
author: JokoAlmi
license: MIT

metadata:
  hermes:
    tags:
      - ia
      - ollama
      - deepseek
      - gemini
      - lm-studio
      - enrutamiento
      - modelo-ligero
---

# ai-router

Skill especializada en decidir qué modelo de IA usar según la tarea.

**Etapa actual:** 3 — Actuar

## Criterios de enrutamiento

| Si la tarea... | Entonces usar... | Motivo |
|---|---|---|
| Contiene información privada | Ollama (local) | Los datos nunca salen del equipo |
| Necesita razonamiento complejo | DeepSeek (v4-flash) | Mayor capacidad de razonamiento |
| Contiene imágenes o PDFs grandes | Gemini | Soporte multimodal nativo |
| Hay poca memoria disponible (VRAM < 4 GB libre) | Modelo ligero local | Evita out-of-memory y swapping |
| Es una consulta rápida y simple | Modelo ligero local | Menor latencia, sin coste |

## Proveedores gestionados

- **Ollama** — `localhost:11434` — modelos locales, GPU acelerada
- **DeepSeek** — API externa (v4-flash) — razonamiento avanzado
- **Gemini** — API externa — multimodal (imágenes, PDFs, audio)
- **LM Studio** — `localhost:1234` (opcional) — modelos locales adicionales
- **Modelo ligero** — Ollama con modelo pequeño (ej: llama3.2:1b, phi4-mini)

Para comandos y órdenes, consultar `COMMANDS.md`.
Para riesgos y protecciones, consultar `SAFETY.md`.
Para conocimiento detallado, consultar `KNOWLEDGE.md`.
