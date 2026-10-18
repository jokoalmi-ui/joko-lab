---
title: "Análisis — MinAgent (Nichonauta): agente CLI mínimo para modelos locales (25-sep-2026)"
type: research
fecha: 2026-09-26
---

# Análisis — MinAgent (Nichonauta): agente CLI mínimo para modelos locales (25-sep-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/APszMDLxf-o — **[Nichonauta] «MinAgent 🤖 El Mejor Agente IA Gratis 🚀 Guía de INSTALACIÓN y Uso»**, publicado **25-sep-2026**, **445 s (7:25)**, **2.717 vistas / 76 likes** (leídos con `yt-dlp` el 26-sep-2026). Transcripción ES auto-generada, **8.396 B**. Repositorio verificado el mismo día con la API de GitHub y el README. **No estaba analizado antes**: `APszMDLxf-o` y «MinAgent» daban 0 coincidencias en `~/joko-lab`.

## Qué es

- `github.com/Nichonauta/MinAgent` — agente CLI de código **para el directorio desde el que se arranca**. **MIT**, **Node.js ≥22**, **cero dependencias** de paquete o runtime. Creado **2026-09-24T23:08:17Z** (un día antes del vídeo): **10 ★, 5 forks, 1 contribuidor** (10 contribuciones). Lenguajes del repo: Batchfile, JavaScript, PowerShell → **lanzadores de Windows**.
- Habla con cualquier endpoint compatible con **OpenAI Chat Completions** con streaming SSE: llama.cpp, LM Studio, Ollama, Anthropic, Gemini, OpenAI. Tool calling obligatorio para operar ficheros; multimodal solo si se usan imágenes.
- Configuración por `.env` en su directorio (el entorno del sistema tiene prioridad). Variables: `OPENAI_BASE_URL`, `OPENAI_API_KEY` (opcional), `OPENAI_MODEL` (obligatoria), `OPENAI_INPUT=text,image`, `OPENAI_CONTEXT_WINDOW` (**por defecto 262144**), `OPENAI_SHOW_REASONING=on|off`, `WORKSPACE_LIST_LIMIT` (**0 = desactivado**, N por carpeta, **−1 = todo**), `TERMINAL_MODE=off`, `SKILLS_ENABLED=off`, `MCP_ENABLED=off`.
- Herramientas: inventario/listado del workspace, lectura y edición de ficheros, terminal opcional. `@` autocompleta ficheros con un índice local acotado a 10.000 entradas.
- Comandos: `/init` (genera `agents.md` con el resumen del proyecto), `@agents.md` (editar el comportamiento), `/context` (**desglose de tokens por ítem**), compactación manual, **Esc** corta la generación.
- Lo que se ve en el vídeo: gemma-4-E4B QAT GGUF sobre llama.cpp (**6,1 GB de VRAM**), sin MCP, sin skills y con la terminal apagada; base **<1.000 tokens** y **1.850 tokens** solo por el `agents.md`.

## 🔴 Mapeo contra el lab

| Pregunta | Respuesta |
|---|---|
| ¿Sustituye o complementa a Hermes? | **No como herramienta**: Hermes ya hace todo lo que se ve (skills, MCP, terminal, edición, imagen, cualquier API compatible) y además memoria, cron, subagentes y RAG. MinAgent no tiene nada de eso. |
| ¿Es interesante con modelos pequeños? | **Es el único hueco funcional real**: su sobrecoste de contexto es <1.000 tokens, frente al system prompt + skills + anclas de Hermes, que sobre un 2-4B pesa. |
| ¿Aporta algo en seguridad? | **Sí, de diseño**: por defecto trabaja solo en el directorio de arranque, solo lee fuera si le pasas la ruta exacta y la terminal viene apagada → vale como **caja** para revisar código de terceros (línea de `least-privilege-lab`). |
| ¿Aporta para clientes? | Potencial: **MIT + Node sin dependencias** es mucho más fácil de entregar que Hermes con perfiles/skills/RAG (`despliegue-ia-local-clientes`). |
| ¿Y el desglose de tokens de `/context`? | **La pregunta es la correcta, pero el lab no parte de cero (corregido el 26-09)**: `hermes prompt-size` mide **offline** el contexto FIJO por bloque (system prompt, índice de skills, memorias, perfil y tools) y el experimento **F1 (cerrado el 16-sep)** lo tokenizó: **23.292 tok netos**, con `tools` ≈ 43,9% e índice de skills ≈ 17% — el fijo no se ha movido en 10 días (53.492 B hoy frente a 53.489 B en F1). La escala la da el agregado del pipeline (`04-operations/metrics/pipeline_obs.jsonl`). **Lo que no había —y sigue faltando— es el desglose del contexto DINÁMICO**, que es ≈85% del prompt real (p50 154.309 tok frente a 23.292 de fijo): diseñado como **F2** el 26-09 en `01-knowledge/experiments/F2-contexto-dinamico/PLAN-F2.md`. |
| Coste de propiedad | Alto para lo que da: repo de un día, un autor, sin pruebas ni benchmarks, y hay que mantener Node 22 + `.env` propios. |
| Riesgo de trazabilidad | MinAgent **no registra nada**. El valor del lab es la trazabilidad (RULE, backlog, ledgers); un segundo agente que no deja rastro rompe eso. |

## Veredicto: **VALOR BAJO como herramienta — MEDIO-BAJO como idea**

1. **CONFIRMA (no es nuevo):** (a) la ventana de contexto hay que fijarla explícitamente — su `.env` lleva `OPENAI_CONTEXT_WINDOW=262144` por defecto, el mismo error que el lab documentó con `num_ctx` en Ollama; (b) herramientas apagadas por defecto (`SKILLS_ENABLED`, `MCP_ENABLED`, `TERMINAL_MODE`) = privilegio mínimo; (c) higiene de contexto por rareza (`WORKSPACE_LIST_LIMIT` 0/N/−1) y compactación manual = `skill-compaction`; (d) prompts cortos para modelos pequeños, criterio ya usado con gpt-oss-20b y gemma.
2. **NO ES NUEVO (corregido el 26-09):** el desglose del contexto **fijo** ya existe en el lab (`hermes prompt-size`, verificado byte a byte; experimento F1 cerrado el 16-sep). Lo que falta es el desglose del **dinámico** (≈85% del prompt real), que es lo que recoge F2 — diseñado, no ejecutado.
3. **NO aporta:** nada nuevo en agentes, herramientas ni multi-proveedor; no reemplaza a Hermes ni a `opencode`.
4. **Riesgo de fuente:** es una demo del propio autor, sin comparación medida con ningún otro agente. Las cifras de VRAM (6,1 GB) salen de su equipo, no de una prueba del lab.

**Sin acción:** no se instala nada. Decisión de la pregunta del usuario («¿Hermes y MinAgent a la vez?») **respondida el 26-09: complementariedad sí, en paralelo no** — los huecos que MinAgent cubriría ya están cubiertos (`delegate_task` para contexto aislado, `opencode` como segundo CLI); papeles válidos: caja para código de terceros, modelos muy pequeños y puente a clientes; y dos agentes sobre los mismos ficheros son dos fuentes de verdad (Hermes deja rastro, MinAgent no).

## Futuribles

- **Fuerte (señal real, no urgente) — reencuadrado el 26-09:** medir el contexto de una sesión de Hermes **por bloque**, pero el **FIJO ya está medido** (F1: 23.292 tok netos; tools 43,9%, índice de skills 17%, MCP 619 tok = 2,7% → los MCP no son palanca). El futurible vivo es el **DINÁMICO** (≈85% del prompt real): **F2**, diseñado el 26-09 en `01-knowledge/experiments/F2-contexto-dinamico/`.
- **Débil:** MinAgent como jaula (solo directorio de arranque, terminal off) para revisar repos de terceros.

## No verificado

- El nombre comercial «MinAgent» frente a otros proyectos homónimos de GitHub: se ha localizado por el usuario del canal (`Nichonauta/MinAgent`), no por un enlace en la descripción del vídeo (la descripción no trae el repo).
- Que la versión del vídeo coincida con el `main` del repo de hoy: no se ha clonado ni ejecutado.

*Nota honesta: transcripción auto-generada con deformaciones («Gema 4 E4B» = Gemma 4 E4B; «M Studio» = LM Studio). Los datos del repo son literal del README y de la API de GitHub leídos hoy; el resto del análisis es el mapeo contra el estado real del lab.*

- **Cifras (revisión 26-09, 4 afirmaciones corregidas):** 6220 B / md5 `86be475b7ecdf44cfd0b6171202e37ac` / 53 líneas → **7661 B** / **55 líneas** (esta línea aporta 369 B; 0 líneas eliminadas; md5 del cuerpo sin esta línea `0c45384ad482ba9719b9aea0c78a8c4b`; validador [VERIFICADO]; backup `analisis-nichonauta-minagent-20260926.md.bak-20260926-correccion`).
