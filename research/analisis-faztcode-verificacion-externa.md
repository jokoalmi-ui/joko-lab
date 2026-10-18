---
title: "Análisis — Verificación externa: \"¿Los MCP están muriendo?\" (Fazt Code, ampliado 24-ago-2026)"
type: research
---

# Análisis — Verificación externa: "¿Los MCP están muriendo?" (Fazt Code, ampliado 24-ago-2026)
**VERACIDAD:** [VERIFICADO]

**Fuente original:** https://youtu.be/eWY6bHtid1o (Fazt Code, 16-03-2026, 16:29 min)
**Análisis previo:** `analisis-faztcode-mcp-vs-skills.md` (22-ago, [VERIFICADO] — resumen del contenido)
**Este documento:** verificación del CLAIM del vídeo contra webs especializadas (petición del usuario 24-ago: "investiga en todas las webs especializadas y si tiene razón de ser")

## El claim del vídeo a verificar

El titular es provocador: **"¿Los MCP están muriendo?"** — porque Skills + herramientas pueden hacer tareas similares. El contenido real del vídeo es más matizado: skills = documentos ligeros que no cargan contexto; MCP = protocolo de conexión con servicios; "no es un reemplazo, es otra forma de comunicación".

## Verificación en webs especializadas (evidencia externa)

### 1. Fuente oficial del estándar — Agent Skills (agentskills.io) ✅ CONFIRMA el vídeo

La documentación oficial del estándar de Agent Skills describe EXACTAMENTE lo que Fazt dice:
- Skill = carpeta con `SKILL.md` (metadata + instrucciones) + scripts/references/assets opcionales
- **Progressive disclosure en 3 etapas**: al arrancar el agente solo carga nombre+descripción; cuando una tarea coincide, lee el SKILL.md completo; ejecuta el código solo si hace falta
- **"Full instructions load only when a task calls for them... small context footprint"** → esto es literalmente lo que Fazt explica ("no se carga en el contexto, simplemente se ejecuta el script")
- Soporte multi-cliente: GitHub Copilot, OpenHands, Emdash, Firebender... (skills portables entre agentes)

### 2. "MCP Isn't Dead. But It's Not the Default Answer Anymore." (Medium, Micheal Lanham, 2026) ⚠️ MATIZA el titular

- **"MCP no está muerto"** — pero dejó de ser la respuesta por defecto
- El fix no es reemplazarlo: **progressive disclosure + deduplicación de schemas + tool search** en vez de volcar todas las tools al contexto
- "La mayoría de implementaciones aún meten todas las definiciones de tools en el contexto y rezan"

### 3. "MCP Isn't Dead. It's Becoming Infrastructure" (LinkedIn, Eddie Shochat) 🎯 LA CLAVE

- **"MCP no está muriendo. Está siendo degradado de capa de hype a capa de infraestructura"**
- Mismo patrón histórico: REST/HTTP también fue "hype" antes de ser invisible

### 4. "MCP Isn't Dead. It Just Needs the Right Engine" (CData blog)

- Confirma que **Anthropic publicó un blog** identificando 2 desafíos reales de MCP a escala: **usa demasiados tokens y llena rápido el contexto**
- (Ese es el mismo problema que la spec MCP 2026-07-28 resolvió con stateless + cacheable — ver `analisis-200ok-mcp-2026.md`)

### 5. "MCP Tool Design: Why Your AI Agent Is Failing" (DEV Community, AWS Heroes)

- **"MCP isn't dead; it's being used poorly"** — cada nombre/descripción/schema de tool consume tokens en cada request (context window bloat)
- La evidencia de cómo usarlo bien "es ahora abrumadora"

### 6. LinkedIn (rchaganti) — la frase que resume el consenso

> "Anthropic built Skills after MCP, and Skills' progressive disclosure design directly addresses MCP's biggest practical weakness (context window bloat). **The two standards don't compete.**"

## Veredicto final: ¿TIENE RAZÓN DE SER?

| Afirmación del vídeo | Veredicto externo | Fuente |
|---|---|---|
| "Los MCP están muriendo" (titular) | ❌ **HIPÉRBOLE** — nadie en la industria dice que mueran; dicen que pasan a ser infraestructura | LinkedIn Shochat, Medium Lanham, CData |
| "Skills son documentos ligeros que no cargan contexto" | ✅ **EXACTO** — progressive disclosure confirmado en la spec oficial | agentskills.io |
| "MCP no es un reemplazo, es otra forma de comunicación" | ✅ **CORRECTO** — "The two standards don't compete" | LinkedIn rchaganti |
| "Hay un debate MCP vs Skills" | ⚠️ **EL DEBATE EXISTE pero es falso** — es complementariedad, no competencia | Consenso general |

**Conclusión**: el vídeo de Fazt Code **tiene razón de ser** en el contenido (la explicación de skills/MCP es correcta y confirmada por la spec oficial) pero **el titular es clickbait** — "¿están muriendo?" es la hipérbole que atrae clics; la industria unánimemente dice que MCP no muere, se convierte en infraestructura (igual que pasó con HTTP).

## Aplicación al LAB (refuerza el diseño existente)

- El lab ya hace lo correcto: **skills para procedimientos** (SKILL.md + scripts que no cargan contexto) + **MCPs para datos/servicios** (lab-db, lancedb, animation-server)
- El patrón "progressive disclosure" = exactamente cómo funcionan las skills de Hermes (solo nombre+descripción se cargan siempre)
- El problema que todos señalan (context window bloat de MCP) NO aplica al lab: los 3 MCPs son stdio locales con tools concretas, no cientos de tools remotas
- **Sin futuribles nuevos** — validación externa de una decisión ya tomada

**Material LinkedIn/TFM**: el consenso de la industria ("MCP es infraestructura, Skills es conocimiento, no compiten") es un argumento excelente para explicar por qué el lab usa ambos.
