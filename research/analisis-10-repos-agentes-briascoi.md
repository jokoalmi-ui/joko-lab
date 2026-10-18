---
title: "Análisis: 10 REPOS para sacar a Claude y ChatGPT del chat (briascoi)"
type: research
---

# Análisis: 10 REPOS para sacar a Claude y ChatGPT del chat (briascoi)
**VERACIDAD:** [VERIFICADO]

- **Fuente**: Instagram @briascoi (Ismael Briasco), post 10-ago-2026
- **URL**: https://www.instagram.com/p/Db3mMfIjWJ2/
- **Tipo**: imagen única (infografía) + caption completo
- **Método**: extracción del DOM (caption + alt de imagen principal) + descarga de la imagen (og:image, 1080x1350 JPEG) + verificación visual con GLM 4.6V local
- **Fecha análisis**: 11-ago-2026

## Qué es

Guía curada de 10 repositorios para llevar a Claude y ChatGPT "del chat al trabajo real":
el modelo responde, el sistema actúa. Organizada en 5 bloques de acción:
RECUERDA, INVESTIGA, OPERA, INTERACTÚA, CONECTA Y PROGRAMA.

## Los 10 repos (verificado en imagen con GLM)

1. **NousResearch/hermes-agent** — memoria, skills y tareas programadas
2. **langchain-ai/open_deep_research** — investigación profunda con fuentes
3. **screenpipe/screenpipe** — memoria local de pantalla y audio
4. **browser-use/browser-use** — navegación y formularios
5. **trycua/cua** — computadoras aisladas para agentes
6. **mobile-next/mobile-mcp** — control de aplicaciones móviles
7. **livekit/agents** — voz, video y telefonía
8. **homeassistant-ai/ha-mcp** — Home Assistant y dispositivos físicos
9. **ComposioHQ/composio** — aplicaciones con autenticación
10. **n8n-io/n8n** — flujos, aprobaciones y registros

El autor añade su siguiente experimento: combinar screenpipe + Open Deep Research + n8n
("memoria de lo que hice, investigación con fuentes y un flujo que sigue trabajando
después del chat"). Aviso de permisos: más herramientas = más permisos; probarlo en un
perfil separado, lectura por defecto y confirmación antes de escribir/comprar/enviar/borrar.

## Mapeo al lab

**VALIDA el stack actual (2/10 ya operativos en el lab):**
- Hermes Agent: es el propio asistente del lab (memoria, skills, cron) — validación total.
- n8n: ya en el stack de automation-stack (flujos, aprobaciones, registros).

**Ya en futuribles del lab:**
- Browser Use: futurible 9 (04-ago, herramientas ecosistema, estudio futuro).

**Futuribles nuevos / interesantes:**
- **screenpipe**: memoria local de pantalla y audio. Encaja con la línea de "memoria"
  del lab (el autor lo usa como "memoria de lo que hice"). Estudiar cuando toque.
- **Open Deep Research**: investigación profunda con fuentes. Relevante para TFM y
  para reducir el coste de contexto (investigar con fuentes estructuradas).
- **trycua/cua**: computadoras aisladas para agentes — aislamiento de permisos, encaja
  con la filosofía de seguridad del lab (perfil separado, lectura por defecto).
- **LiveKit Agents**: voz/video/telefonía para agentes — el lab usa edge-tts (texto a
  voz) pero no un pipeline de voz bidireccional. No urgente.
- **HA-MCP**: Home Assistant + IA — el lab tiene skill openhue pero no Home Assistant.
- **Composio**: apps con autenticación para agentes — no urgente, el lab conecta por API directa.
- **Mobile MCP**: control de apps móviles — no aplica hoy.

## Veredicto

**VALIDA + 1-2 futuribles a futuro.** La guía confirma la dirección del lab (agentes
que actúan fuera del chat, ya con Hermes + n8n). NADA urgente nuevo. El combo
screenpipe + Open Deep Research + n8n del autor es coherente con los intereses del
lab (memoria, investigación con fuentes, automatización) pero no desbloquea ningún
cuello de botella actual. Fuente con componente comercial (vende curso Claude Cowork),
pero el listado de repos es verificable y correcto.

## Mapeo repo por repo al LAB (11-ago-2026, evaluación completa)

**Ya en uso (validación, nada que hacer):**
1. **hermes-agent** → es el propio asistente del lab. Validación total del stack.
2. **n8n** → ya en automation-stack (zona protegida). Validación total.

**Útiles a futuro (ordenados por relevancia para el lab):**
3. **open_deep_research** (langchain-ai) → el MÁS RELEVANTE de los nuevos.
   - Para qué: TFM antes de octubre (investigación con fuentes citadas) y atacar el
     cuello de botella nº1 del lab (coste de contexto, 99.7% prompt): investigar con
     fuentes y devolver síntesis + citas en vez de meter todo el contexto.
   - Cómo encaja: como skill/herramienta de investigación del lab (hoy: web_search +
     RAG local). Integrable con router local/cloud.
   - Prioridad: MEDIA-ALTA cuando toque investigar en serio (TFM).
4. **screenpipe** (screenpipe) → línea "memoria" del lab.
   - Para qué: capturar contexto del trabajo real (pantalla + audio local) como
     complemento a sesion_search de Hermes (que solo ve texto).
   - Riesgos: privacidad (grabar pantalla/audio) y recursos (CPU i5-9500 limitado;
     bucle de captura constante es coste real).
   - Prioridad: BAJA. Interesante conceptualmente, pesado en recursos.
5. **trycua/cua** → aislamiento real de ejecución.
   - Para qué: tareas de alto riesgo (ejecutar código/descargas no confiables) en
     sandbox/VM aislada. El lab ya mitiga con approvals.mode=smart + zonas protegidas;
     cua aportaría aislamiento de sistema real.
   - Prioridad: BAJA. Solo si el lab empieza a ejecutar código externo no confiable.

**No aplican hoy (anotado para no re-evaluar):**
6. **browser-use** → Hermes ya tiene browser tools (mismo dominio). Ya era futurible 9
   (BROWSER USE / CREWAI, 04-ago). Solo si se quiere un agente autónomo dedicado.
7. **mobile-mcp** → el lab interactúa por Telegram/CLI; no controla apps móviles.
   No es el flujo actual.
8. **livekit/agents** → el lab ya tiene dictado por voz (Whisper local, skill
   dictado-voz) y TTS (edge-tts). LiveKit añadiría streaming/teléfono bidireccional;
   no urgente.
9. **ha-mcp** → el lab tiene skill openhue (luces) pero no Home Assistant ni domótica
   montada. No aplica hoy.
10. **composio** → el lab conecta por API directa (Gemini, DeepSeek, LM Studio, n8n).
    Auth gestionada centralizada no es un problema actual.
