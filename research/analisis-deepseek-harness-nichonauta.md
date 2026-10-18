---
title: "Análisis — DeepSeek Harness (Nichonauta, 15-ago-2026)"
type: research
---

# Análisis — DeepSeek Harness (Nichonauta, 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/Fx8b5u0J5Wo (9 min, Nichonauta — canal de referencia #1)
**Transcripción:** completa (es, 239 líneas)
**Fecha:** 2026-08-15 10:06 CEST (verificado con date)

---

## Qué es DeepSeek Harness

**Harness agéntico de código abierto (licencia MIT) lanzado por DeepSeek** —
"principalmente pensado para desarrollo de software, pero usable para
cualquier cosa con un modelo de lenguaje y herramientas para uso agéntico".

### Características (transcripción literal)

1. **Código abierto (MIT)** — DeepSeek lo lanzó "hace unas horas" del vídeo
2. **Conexión flexible:** no solo la API oficial de DeepSeek — compatible con
   cualquier API OpenAI-compatible (DeepSeek, Google, Anthropic, OpenAI, y
   **modelos locales** — el siguiente vídeo de Nichonauta lo probará local)
3. **Instalación:** `npx` (Node.js) — la 1ª instalación tarda (compila cosas)
4. **UI web en localhost** (diferente de los harness CLI típicos) — interfaz
   tipo chat de DeepSeek pero orientada a uso agéntico
5. **Modos:** estándar, **código**, mínimo, creador (estilo OpenCode, P/agent)
6. **Espacios de trabajo/proyectos:** seleccionas una carpeta y trabaja ahí
7. **Funciones:** cadena de razonamiento visible, trayectoria técnica (turnos,
   llamadas, duración), compactar, exportar logs ZIP, feedback, meta,
   permisos, modo plan, cambiar modelo
8. **Proveedores:** muchos predefinidos + **proveedor personalizado** (archivo
   de configuración accesible)
9. **Plugins:** instalar/activar/desactivar + **presets de agentes** (crear nuevos)
10. **Visión:** permite adjuntar imagen pero NO funciona con los modelos de
    DeepSeek (no son VLM nativos; "es gracioso" — lo permite pero falla)
11. **Idiomas:** solo chino e inglés (de momento)
12. **Presets por modelo:** distintos presets según el LLM (funciona mejor o
    peor según el modelo)

---

## Veredicto para el lab

### ✅ VALIDA el concepto de harness (3ª validación esta semana)

| Fuente | Idea |
|---|---|
| maurys (37 agentes, 15-ago) | "Hermes = capa de acción" |
| deadlockdreams (Agent Harness = OS del LLM, 15-ago) | LLM=CPU, Context=RAM, Harness=OS |
| **DeepSeek Harness (hoy)** | **DeepSeek mismo lanza un harness agéntico open source** |

**Conclusión:** el concepto "harness agéntico alrededor del LLM" es el patrón
dominante de la industria — y **el lab ya tiene el suyo** (Hermes +
router + skills + LM Studio local + workers OpenCode/Aider).

### 🚫 NO accionable ahora (por qué no cambiar de harness)

1. **El lab ya tiene harness** — Hermes orquesta, el router decide local/cloud,
   los workers (OpenCode/Aider) delegan. Cambiar a DeepSeek Harness sería
   reemplazar lo que ya funciona por algo recién salido (preview)
2. **UI web + Node.js** — el lab es CLI-first + scripts; no necesita otra UI
3. **DeepSeek lo orienta a su API cloud** (aunque sea conectable a local) —
   el lab es local-first
4. **Idiomas solo chino/inglés** — el lab trabaja en español

### ⭐ LO INTERESANTE (a seguir)

1. **El siguiente vídeo de Nichonauta** ("probar DeepSeek Harness con modelo
   local") — ese SÍ puede aportar: cómo conectar un harness a LM Studio
   local es el terreno del lab. **Pendiente de revisar cuando salga.**
2. **Confirma el patrón de validación:** cada día más actores (incluido
   DeepSeek) implementan la arquitectura que el lab ya tiene — material
   perfecto para TFM/LinkedIn ("lo que las grandes empresas lanzan, nosotros
   ya lo usamos en local")
3. **La UI web como patrón** — no es accionable ahora, pero es un dato:
   los harness convergen hacia UI web + presets por modelo

### 📌 Nota honesta

- El vídeo es una **primera impresión** (Nichonauta lo probó 30 min tras el
  lanzamiento; "a pesar de ser preview, me parece interesante") — no es un
  benchmark ni una comparación seria con Claude Code/OpenCode
- El detalle de la visión (permite adjuntar pero falla) es una curiosidad de
  producto, no un fallo del lab

---

## Registro

- Guardado: research/analisis-deepseek-harness-nichonauta.md
- Veredicto: **VALIDA el patrón harness (3ª validación) — NO accionable
  (el lab ya tiene su harness); a seguir: el vídeo de Nichonauta probándolo
  con modelo local**
- Relacionado: research/analisis-37-agentes-maurys.md, analisis-3-posts-vigilante-ig.md
