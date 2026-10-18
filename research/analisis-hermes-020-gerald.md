---
title: "Análisis — Hermes 0.20 \"Gerald\" (vídeo YT Kilian Párraga, 12-ago-2026)"
type: research
---

# Análisis — Hermes 0.20 "Gerald" (vídeo YT Kilian Párraga, 12-ago-2026)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 12-ago-2026 (08:10 CEST)
**Fuente:** https://youtu.be/5UQSHScCv00 — Kilian Párraga (agencia Expert Brain)
**Tema:** Review de Hermes 0.20 (release "Gerald", llegó la semana pasada)
**Relevancia:** 🔴 CRÍTICA — el lab usa Hermes 0.17.0 y la memoria dice
"NO upgrade (esperar 0.20.1; A2A solo 0.20.0+)".

---

## Las novedades de 0.20 (en orden de importancia del vídeo)

### 1. Modo voz "Hey Hermes" (EMES)
- Activación por voz como Alexa/Siri: "Oye Hermes" → escucha → pide tareas
- Latencia mínima, habla "limpio" (sin leer markdown), se puede interrumpir/parar con "stop"
- Proveedor configurable (viene Nous Research por defecto, se puede cambiar)
- ⚠️ **Pitfall del vídeo:** el comando por defecto "Ermes" (acento inglés) falla
  con hablantes de español → cambiarlo a "Oye Hermes" + motor de español
- Voz multicanal: WhatsApp, Line, Telegram (mensaje de voz → respuesta de voz)

### 2. A2A — agentes que hablan entre sí (la 2ª más importante)
- Desde 0.17/0.19 se pueden crear múltiples agentes (cada uno con capacidades
  y memoria distintas)
- **NUEVO en 0.20:** los agentes se comunican entre sí (A2A) — un agente
  director orquesta a otros (ej: frontend + backend + seguridad para programar)
- **⚠️ CONFIRMA lo que la memoria del lab ya sabía: A2A solo 0.20.0+**

### 3. Investigación con fuentes verificadas (anti-alucinación)
- **Problema anterior:** en investigaciones largas los agentes tendían a
  INVENTAR (alucinar) con demasiado contexto
- **Fix en 0.20:** cada afirmación va ANCLADA a una fuente real comprobada;
  cada cita se contrasta con el texto real de la página; los enlaces apuntan a
  la evidencia concreta (no a la home)
- **"Nada de citas inventadas, no alucinaciones"**

### 4. Mejoras técnicas
- **6x más interacciones de herramientas:** límite 90 → 500 pasos por tarea
  (tareas mucho más largas)
- **Arranque en frío: 14s → 1.8s**
- **Artifacts versionados:** todo lo generado se guarda versionado con preview
  en vivo (repescable para iterar)
- **Quick Entry:** comando desde cualquier ventana para hablar con Hermes
- **¡Comando:** para usuarios técnicos — escribir el comando exacto de terminal
  sin interacción con la IA (ahorra tokens)
- **Redirección en caliente:** corregir a mitad de turno sin parar (le escribes
  y continúa corrigiendo)
- **`hermes import agent`:** importar configuración de Claude Code / Codex
  (claude.md / AGENTS.md) para no empezar de cero
- **Voz multicanal** (WhatsApp/Line/Telegram)

### Datos de la release
- 647+ contribuyentes · 770 correcciones
- Llegó la semana pasada (≈ 05-ago-2026)

### Opinión del autor (honesta)
- Modo voz: **"espectacular pero no para todo"** — cuándo usarlo y cuándo
  seguir escribiendo (lo muestra en directo)
- Requiere actualizar primero el servidor (VPS) y luego el escritorio

---

## 🎯 Aplicación al LAB — DECISIÓN DE UPGRADE

### El contexto de la memoria del lab
"Hermes v0.17.0; NO upgrade (esperar 0.20.1; A2A solo 0.20.0+)"

### Qué aporta este vídeo a la decisión

**A FAVOR de actualizar (a 0.20.x):**
1. **A2A** — el lab tiene delegación con subagentes (delegate_task) pero A2A
   sería comunicación formal entre agentes con memoria distinta — directamente
   útil para el lab (sesión CLI + Telegram ya colaboran vía file bus; A2A
   formalizaría eso)
2. **Fuentes verificadas anti-alucinación** — el lab analiza contenido (web,
   carruseles) y el RAG busca fuentes; la ancla a fuente real es una mejora
   directa de calidad
3. **500 pasos por tarea** (vs 90) — tareas largas (los análisis de carruseles,
   refactors masivos) dejarían de cortarse
4. **Arranque 14s → 1.8s** — relevante para el gateway que reinicia
5. **Redirección en caliente** — el usuario corrige a mitad de turno (patrón
   real: "no, así no" → ahora se aplicaría sin reiniciar la tarea)

**EN CONTRA (prudencia del lab):**
1. **0.20.0 es reciente** (semana pasada) — la memoria ya decidió esperar a
   0.20.1 (el .1 suele traer fixes de los bugs del .0)
2. **El lab está en producción** (crons, gateway, 27 jobs, skills) — un upgrade
   rompe cosas (lecciones del pasado: config.yaml, skills, rutas)
3. **El vídeo muestra bugs** (comando de voz no funcionaba con acento español —
   aunque es configurable)
4. **Coste de migración:** hay que verificar compatibilidad de skills,
   config.yaml, crons antes de actualizar

### Veredicto honesto
**El vídeo REFUERZA el plan de la memoria (esperar a 0.20.1), no lo cambia:**
- Las 3 novedades grandes (voz, A2A, fuentes) son atractivas, pero el lab no
  las necesita URGENTEMENTE (la voz no es prioridad; A2A ya tiene equivalente
  parcial con delegate_task + file bus; las fuentes verificadas son mejora,
  no necesidad)
- Esperar a 0.20.1 = los bugs del .0 se arreglan (como el del comando de voz)
- **Futurible:** actualizar a 0.20.1 cuando salga, con el proceso de
  verificación completo (backup config.yaml + skills + prueba de crons)

### Futuribles
1. 🟢 **Upgrade Hermes a 0.20.1 cuando salga** (mantener el plan de la memoria):
   verificar compatibilidad de skills/config/crons antes; el vídeo confirma
   que vale la pena (A2A + fuentes + 500 pasos + arranque 1.8s).
2. 🟡 **A2A para el lab:** cuando esté en 0.20.x, evaluar si formaliza la
   colaboración sesión CLI ↔ Telegram (hoy vía file bus).

## Conclusión
Review completa de Hermes 0.20 (Gerald). REFUERZA la decisión de esperar a
0.20.1 (bugs del .0 visibles en el vídeo) pero confirma que el upgrade merece
la pena cuando salga: A2A + fuentes verificadas + 500 pasos + arranque 1.8s +
redirección en caliente. Anotado como futurible con el plan de verificación.

## Nota técnica
- Transcripción en español obtenida (el script falló la primera vez con el
  python del sistema — usar SIEMPRE ~/.hermes/.venv/bin/python3)
- El vídeo es de la comunidad Hermes (Kilian Párraga) — fuente terciaria,
  contrastar con la release oficial antes de actualizar
