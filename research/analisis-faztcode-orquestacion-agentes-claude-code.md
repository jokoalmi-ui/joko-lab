---
title: "Análisis: Orquestación de agentes SIN Herder ni Orca (solo Claude Code) (Fazt Code)"
type: research
---

# Análisis: Orquestación de agentes SIN Herder ni Orca (Fazt Code)
**VERACIDAD:** [VERIFICADO]

**Fuente**: https://youtu.be/-e64NFNmfwo · Fazt Code (@FaztCode) · 05-sep-2026
**Vídeo**: 12:53 min · 7.088 views · Transcripción real (subs es-orig, dedup → 16.264 chars, análisis completo)
**ID**: -e64NFNmfwo · **Estado**: [VERIFICADO] con transcripción íntegra

## ⚠️ Nota de veracidad

Vídeo con **sponsor de Hostinger (~2 min iniciales — descartado como
contenido)**. La demo central es auténtica (la ejecuta en vivo con Claude
Code). Sin afirmaciones factuales falsas burdas → no activa RULE-017.

## Qué muestra el vídeo

Demo de la función de Claude Code de **enviar mensajes entre sesiones/terminales**
(sustituto de Herder/Orca para casos simples):

1. Sesión "planner" (modelo caro, esfuerzo alto) genera `plan.md` con tareas
   marcadas por dificultad (baja/media/alta)
2. Renombra sesiones (`/rename`): planner, developer 1, developer 2
3. Planner **delega por dificultad**: tareas baja/media → dev1 (Sonnet, rápido),
   alta → dev2 (Opus, más lento pero mejor código)
4. Cada sesión recibe el mensaje con su resumen de tareas y avanza en paralelo
   (mismo proyecto, carpetas distintas)
5. También sirve entre **proyectos distintos** (una sesión pide a otra que
   implemente una feature en su CLI — caso real del autor con sus herramientas
   propias)

## Advertencias del propio autor

- No es para todos: **cansa saltar entre sesiones** y tener en mente qué avanza
- No aporta en un solo proyecto ni en vibe coding (pedir y ver)
- Requiere planificar primero (él dedica 30-60 min al plan antes de delegar)
- El valor real aparece con suscripciones caras (Claude $100-$200) o con
  agentes multi-modelo (OpenCode/Command Code: DeepSeek, GLM, etc. en un solo
  agente)

## Filtro de valor para el lab (regla 20-ago)

**VALIDACIÓN, no novedad.** El lab ya orquesta agentes con `delegate_task`
(subagentes con verificación integrada — exactamente lo que a Fazt le falta:
él admite que revisar N sesiones "es cansado y no es perfecto"). El patrón
"plan grande → delegar por dificultad" valida la metodología del lab
(plan → delegación), y el mensaje de modelos mixtos baratos (DeepSeek/GLM)
es lo que el lab ya aplica con combined-mode/ai-router.

Sin futuribles nuevos: no introduce técnica que el lab no tenga; Claude Code
con mensajes entre sesiones es inferior a `delegate_task` del lab (sin
verificación ni orquestación central).

Conecta con: skills `delegacion-subagentes`, `graph-lab`, `claude-code`
(orquestación del lab), `plan` (patrón plan grande → delegar).
