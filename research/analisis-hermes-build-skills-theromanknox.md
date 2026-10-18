---
title: "Análisis — Carrusel theromanknox \"Hermes Agent Build Skills\" (25-ago-2026)"
type: research
---

# Análisis — Carrusel theromanknox "Hermes Agent Build Skills" (25-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/Dcd6C5CiiPS/ (theromanknox / Roman Khaneichuk, 25-ago, 73 likes, 9 comentarios)
**Contexto:** el usuario dice "Este me ha gustado" — carrusel de 5 slides promocionando la comunidad "Build Skills" (skool.com/knox) con ideas de agentes construidos con **Hermes Agent** (el mismo agente que usa el lab).
**Método:** caption (mínimo) + alt de las imágenes del DOM (contienen el texto completo de las diapositivas). Solo 2 de 5 slides accesibles sin login (límite del lab validado con darpan 24-ago). GLM visión no respondió (API local inestable) → se usaron los alt como fuente.

## Contenido (2 slides accesibles, texto real de los alt)

### Slide 2/5 — 🧭 AICodebase Explorer
"Develop an agent that deeply analyzes a GitHub repository rather than just responding to coding queries. Give it a task like 'Handle the authentication logic' and Hermes scans the project, identifies dependencies, reviews history, maps connections, and delivers clear insights."
- Flujo: Query task → Scan project → Read code → Dependencies → Commit history → Map connections → Explain → Refine

### Slide 3/5 — 🧪 Autonomous Testing Agent
"Design an agent that uncovers bugs in a GitHub repository instead of waiting for developers to spot them. Give it a module like 'Check the login function' and Hermes interprets the code, generates tests, runs them, analyzes failures, discovers edge cases, and produces a detailed bug report."
- Flujo: Understand code → dependencies → Module/function → Test generation → Run tests → Analyze failures → Bug report → Additional test cases → Edge case discovery

### Slides 1, 4, 5 — NO accesibles sin login (no inventar)

## 🔴 Aplicación al LAB — VALOR MEDIO (2 ideas útiles + validación)

### ✅ Idea 1: AICodebase Explorer — el lab YA la tiene parcialmente
- El lab tiene: `codebase-inspection` skill (pygount: LOC, lenguajes, ratios), `búsqueda` en joko-lab con search_files, y Hermes con acceso a terminal.
- **Gap**: un agente "explora un repo y responde a tareas concretas tipo 'maneja la autenticación'" — el lab no tiene eso formalizado como skill para repos ajenos (solo para el propio).
- **Aplicable**: cuando el lab necesite analizar un repo externo (p.ej. evaluar una herramienta antes de instalar, como con FreeToken/ComfyUI). Futurible ligero.

### ✅ Idea 2: Autonomous Testing Agent — VALOR MEDIO-ALTO (la más interesante)
- El lab tiene: suite de tests (219 passed + 14 skipped), TDD skill, systematic-debugging.
- **Gap**: "generar tests automáticamente, ejecutarlos, analizar fallos y descubrir edge cases" de forma autónoma — el lab ejecuta tests pero NO genera tests nuevos automáticamente.
- **Conexión directa**: se podría usar en el lab para (a) generar tests de regresión para tools propias (llm_as_judge, verificar_research), (b) descubrir edge cases en scripts de Python.
- **Ya hay base**: el 25-ago se escribió el test unitario de robustez del juez a mano — un "testing agent" automatizaría eso.

### 🟢 Validación del posicionamiento
- El autor vende su comunidad con "ideas de skills para Hermes" — **el lab YA usa Hermes como agente** (el 90% de la audiencia de ese post no sabe qué es Hermes; el lab lo tiene en producción).
- Refuerza: Hermes está ganando visibilidad como agente de código (también visto en el vídeo de Julian Goldie y en OpenRouter con OxAlpha).

## Conclusión
VALOR MEDIO: 2 ideas útiles del carrusel (AICodebase Explorer y Autonomous Testing Agent), 1 futurible ligero anotado (generación automática de tests con Hermes para tools del lab). El resto del carrusel (slides 1/4/5) no accesible sin login — no se inventó. No requiere acción inmediata.

**Nota técnica**: el autor promociona su comunidad (skool.com/knox) — el contenido está diseñado como gancho; las ideas son genéricas pero correctas como patrón.
