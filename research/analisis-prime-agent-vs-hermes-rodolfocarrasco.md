---
title: "Análisis — Prime Agent vs Hermes Agent (Rodolfo Carrasco, 16-ago-2026)"
type: research
---

# Análisis — Prime Agent vs Hermes Agent (Rodolfo Carrasco, 16-ago-2026)

**Fuente:** https://youtu.be/mQm5s9vgT3Y (Rodolfo Carrasco | IA & Automatizaciones, ~14 min, es)
**Transcripción:** completa (es)
**VERACIDAD:** [VERIFICADO]

## Qué es Prime Agent (datos verificados, no solo lo del vídeo)
- **Repo:** PrimeIntellect-ai/prime-agent — 16.381 ⭐ (16-ago), 1.760 forks, **licencia MIT**, creado 08-may-2026, push activo 15-ago
- **Empresa:** Prime Intellect (SF, fundada 2024, $130M levantados, valoración $1B; inversores Nvidia, Intel; clientes Zapier, RAM, Character)
- **Qué es:** agente de código/investigación open source para tareas largas; vive en terminal (familia Claude Code/Codex)
- **Crecimiento:** anuncio oficial 05-ago-2026, #1 trending GitHub del 06-10-ago, 42 versiones en 7 días

## La arquitectura RLM (lo que lo diferencia REALMENTE)
- **RLM (Recursive Language Model):** contexto como VARIABLE (prompt-as-a-variable) + subagentes recursivos como funciones dentro de un **REPL persistente de Python**
- **Clave:** el contexto NO se llena — los datos viven en variables fuera del modelo; cuando necesita algo, escribe código para leerlo en el momento
- **Analogía del vídeo (buena):** otros agentes memorizan la guía telefónica entera; Prime busca el número cuando lo necesita
- **Refine:** comando que graba correcciones como lecciones permanentes (el agente aprende de cada corrección)
- **Continual Harness:** el agente puede inspeccionar/programar/mejorar SU PROPIO entorno (prompts, skills, memoria como estado CRUD)
- **Claim de la empresa:** 95,5% en ARC-AGI-3 con Opus 5 (vs 95,4% de expertos humanos) — **NO verificado independientemente, es claim de marketing**

## Funciona con
20+ proveedores: Anthropic, OpenAI, xAI, **Ollama (gratis), LM Studio**... (encaja con local-first)

## 🎯 VEREDICTO SINCERO (sin sesgo hacia Hermes)

### Lo que Prime hace GENUINAMENTE bien (y que Hermes no tiene igual)
1. **REPL persistente de Python con variables fuera del modelo** — el contexto nunca se llena; Hermes usa compresión de contexto (0.3/0.15) y skill-compaction porque SÍ se llena. **Este es el punto donde el vídeo tiene razón.**
2. **Refine como comando explícito** — tu corrección queda grabada como lección; Hermes lo hace por memoria/skills pero no como comando directo
3. **Auto-mejora del entorno (Continual Harness)** — el agente se programa a sí mismo; el lab hace algo parecido (skills que se parchean) pero no tan sistematizado

### Lo que Hermes tiene y Prime NO (el vídeo no lo dice)
1. **Multi-plataforma real** — Telegram, WhatsApp, Discord, etc. (Prime es solo CLI)
2. **Crons programados** — vigilancia, informes, watchdog (Prime no tiene scheduler)
3. **RAG integrado** — LanceDB 19.894 filas, recall@5 100% (Prime no trae RAG)
4. **Gate de veracidad** (construido HOY) — etiqueta de certeza + bloqueo de no verificado
5. **233 tests** — el lab se verifica a sí mismo
6. **Memoria persistente + perfiles + file bus** — contexto entre sesiones

### El clickbait "DESTROZA"
- La demo del vídeo (leer 131 facturas → dashboard con alertas) es algo que **Hermes puede hacer con execute_code + pandas** — no demuestra superioridad
- El claim ARC-AGI-3 es de la empresa, con el modelo de pago (Opus 5), no del agente open source
- "Destroza" es marketing de YouTube, no un benchmark comparativo

## 📌 ACCIÓN PARA EL LAB (prioridad: mejorar LAB primero)
- **NO cambiar de agente** — Hermes cubre más (plataformas, crons, RAG, veracidad, tests)
- **SÍ robar la idea del REPL persistente**: evaluar si el lab puede mantener un estado de variables Python entre turnos para tareas largas (evitar re-leer/comprometer contexto). → FUTURIBLE: "estado persistente entre tareas" (inspirado en RLM)
- **SÍ el concepto "buscar cuando necesitas"** — el lab ya lo hace con RAG; confirmación de que el enfoque es correcto
- **Refine → el lab ya lo tiene** (memoria + skills), pero podríamos formalizar un comando equivalente

## Material TFM/LinkedIn
- "Comparativa de arquitecturas de agentes: RLM (contexto como variable) vs contexto completo + compresión"
- El claim ARC-AGI-3 como caso de estudio de claims de marketing vs verificación
