---
title: "Análisis — Vídeo: Hermes Agent Quicksilver (0.19/0.20) — Killian Parraga (Expert Brain)"
type: research
---

# Análisis — Vídeo: Hermes Agent Quicksilver (0.19/0.20) — Killian Parraga (Expert Brain)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 06-ago-2026
**Fuente:** https://youtu.be/R_bJga4tzHA
**Tema:** Actualización Quicksilver de Hermes Agent — cambios, instalación, y cómo poner límites de seguridad

---

## ⚠️ AVISO CRÍTICO para el lab

**El vídeo afecta directamente al propio Hermes que ejecuta este análisis.**
Quicksilver (0.19) cambia el modelo de permisos: **un agente de IA ahora aprueba
comandos automáticamente sin pedir verificación al humano** (viene de serie, no
es opcional). El humano puede configurar REGLAS DE DENEGACIÓN que bloquean
acciones concretas aunque dé permiso para todo.

## Las 7 mejoras de Quicksilver

| # | Mejora | Detalle |
|---|---|---|
| 1 | **Permisos con agente validador** | Un LLM analiza cada comando: inofensivo → deja pasar; peligroso → bloquea; dudoso → pregunta al humano. MUCHAS menos preguntas de permisos |
| 2 | **Reglas de denegación (deny rules)** | Bloqueos duros que el agente no puede saltar NI con permiso total. Config: `approvals.deny` en config.yaml |
| 3 | **Más rápido** | Primer token: 4.3s → **0.9s (80% menos)** |
| 4 | **Entrega de mensajes con seguimiento** | Apunta el mensaje antes de enviar y verifica que llegó (ya no "enviar y confiar"). Puede duplicar mensajes en microcortes |
| 5 | **Esfuerzo por tarea** | `/model ones` — subir el nivel de razonamiento puntualmente para una pregunta (plan/max/ultra) sin cambiar de modelo |
| 6 | **Perfiles aislados** | Cada perfil de Hermes tiene info aislada de los demás (antes compartida) |
| 7 | **Partes de trabajo** | Deja constancia de qué ejecutó cada tarea programada y cómo acabó (antes: silencio si fallaba) |

**Extras:** gestor de contraseñas (APIs ya no en texto plano en .env), acceso a
modelos nuevos de Nous (GPT 5.6, Gr 4.5, Fable 5), **reset de sesiones DESACTIVADO
por defecto** (antes auto-reseteo), conversaciones exportables.

## Instalación (lo que muestra el vídeo)

- `hermes --version` → comprobar versión (él tenía 0.17)
- `hermes update` → actualiza (llegó a 0.19.1, mientras grababa salió 0.20)
- Escritorio: botón Update Now en About, o terminal si falla
- Server + escritorio: actualizar AMBOS (client y backend por separado)

## Las 3 reglas de denegación que él puso (ejemplo)

```
1. No borres nada de forma recursiva en la raíz (rm -rf /)
2. No toques la base de datos sin preguntarme
3. No subas nada a la rama principal sin mi visto bueno (git push a main)
```

Config resultante en `~/.hermes/config.yaml` → clave `approvals.deny`:
- bloquea eliminaciones recursivas sobre rutas absolutas del sistema
- bloquea acceso directo a la base de datos
- bloquea git push a main

## 🔗 Aplicación al LAB

| Aspecto | Análisis honesto |
|---|---|
| **¿Está el lab en riesgo?** | 🟡 El lab usa Hermes **0.17.0** (verificado 05-ago, pendientes.txt) con DeepSeek. El cambio de auto-aprobación NO aplica aún: es de Quicksilver (0.19+), y el lab está en 0.17.0 con decisión de esperar a 0.20.1 (DECIDIDO 05-ago). El bug #62723 (migración v30→v32) está CERRADO (15-jul), no es lo que bloquea: es decisión deliberada |
| **Reglas de denegación recomendadas** | 1) rm -rf en rutas absolutas 2) acceso a BD sin preguntar 3) git push a main — EXACTAMENTE las protecciones que el lab ya tiene por convención (JL-014, zona n8n, confirmación explícita). Convertirlas en deny rules formales = refuerzo |
| **Perfiles aislados** | 🟡 El lab tiene 1 perfil (default) — no afecta, pero OJO: las sesiones paralelas (CLI/Telegram) comparten memoria/skills — con perfiles aislados eso cambia si se crean más perfiles |
| **Reset de sesiones desactivado** | ✅ Beneficio: las sesiones ya no se resetean solas (coherente con el multi-sesión del lab) |
| **Partes de trabajo (cron)** | ✅ Mejora directa para los crons del lab (el informe-diario que falla, watchdog) |
| **Gestor de contraseñas** | ✅ Mejora de seguridad (las APIs en texto plano eran un riesgo) |

## Acciones posibles para el lab

1. **Versión YA verificada (05-ago)**: 0.17.0, con decisión de esperar a 0.20.1
   (informe: hermes-lab/informes/2026-08-05-hermes-upgrade-analysis.txt, vigilado por
   cron 517fdc280d6f diario + telegram). Cuando el watchdog avise de 0.20.1 → flujo
   hermes-upgrade-analysis + decisión.
2. **Tras el upgrade a 0.19/0.20+**: considerar añadir deny rules formales en config.yaml
   (las 3 del vídeo + las del lab: no tocar n8n, no borrar backups)
3. **Probar `/model ones`** con DeepSeek para tareas de alto razonamiento
4. **Aprovechar partes de trabajo** para diagnosticar el cron que falla

## Veredicto

Vídeo práctico y honesto (Killian Parraga, agencia Expert Brain). El dato más
importante para el lab es el **cambio de modelo de permisos en Quicksilver**:
el lab está en 0.17.0 con decisión de esperar a 0.20.1 (05-ago, vigilada por
cron diario + telegram), así que el cambio aún no aplica. Tras el upgrade,
configurar deny rules formales para blindar lo que ya protege por convención.

**Nota de revisión (06-ago):** este análisis se corrigió para reflejar la
versión real (0.17.0) y la decisión de esperar a 0.20.1 — la versión original
decía "0.19? — verificar versión" sin contrastar con pendientes.txt.
