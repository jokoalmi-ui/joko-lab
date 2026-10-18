---
title: "Análisis — Herd: controla todos tus agentes de IA (Migue Baena IA, 22-ago-2026)"
type: research
---

# Análisis — Herd: controla todos tus agentes de IA (Migue Baena IA, 22-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtube.com/shorts/6P6hzRkrspU (Migue Baena IA, 21-08-2026, 42s)
**Método:** subtítulos ES descargados (7.8 KB) + metadatos

## Contenido
- **Herd** (herramienta gratis, open source): controla **varios agentes de IA desde una sola terminal**
- Convierte el caos de varias ventanas en un único espacio de trabajo
- Compatible con agentes de programación populares: **Cloud Code (Codex) y Codex a la vez**
- Permite: ejecutar varios agentes en paralelo · organizar proyectos en espacios de trabajo y pestañas · ver qué agentes están activos / han terminado / esperan respuesta
- Objetivo: no saltar entre 1000 terminales, centralizar todo

**Frase clave**: "En vez de perder el tiempo gestionando ventanas, Herd lo centraliza para que te enfoques en desarrollar mientras tus agentes trabajan."

## 🔴 Para el LAB — VALOR: MEDIO (orquestación de agentes CLI)

| Aspecto | Análisis |
|---|---|
| ¿El lab usa múltiples agentes CLI? | ⚪ Tiene skills de delegación (codex, claude-code, opencode) pero el flujo real es Hermes como orquestador único |
| ¿Herd encaja? | ⚪ Podría si el lab empieza a lanzar varios agentes CLI en paralelo (Codex + OpenCode juntos) |
| Conexión con A2A | El post conecta con la tendencia A2A (agentes colaborando) — Herd es un orquestador de agentes en una terminal |

**Futurible débil**: probar Herd si el lab necesita ejecutar 2+ agentes CLI en paralelo (p.ej. Codex para una tarea + OpenCode para otra). **Señal de activación**: cuando la delegación paralela se vuelva habitual en el lab. Hasta entonces, Hermes ya orquesta (delegate_task batch).

**Conclusión**: herramienta interesante para orquestar agentes CLI, pero el lab ya tiene orquestación con Hermes. Solo sería relevante si se intensifica el uso de CLIs de codificación en paralelo. Sin acción hoy.
