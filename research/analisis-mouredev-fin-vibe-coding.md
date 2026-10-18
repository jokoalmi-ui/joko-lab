---
title: "Análisis — El fin del VIBE CODING (MoureDev, 21-ago-2026)"
type: research
---

# Análisis — El fin del VIBE CODING (MoureDev, 21-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/jresR0hZ_Hs (MoureDev / Brais Moure, 20-08-2026, 13:23)
**Método:** transcripción ES completa (yt-dlp auto-subs, 43.5K chars)

## Tesis del vídeo
- **Vibe coding** = programar por "vibras": describir en lenguaje natural, aceptar lo que
  la IA genera sin leerlo en profundidad, pedir en bucle si falla → el código deja de ser
  algo que entiendes y pasa a ser "magia invocada". Engancha (dopamina, elimina pensar,
  funciona para prototipos) pero el fallo llega cuando el proyecto crece (contexto limitado,
  nadie al volante).
- **3 facturas del vibe coding**:
  1. **Dinero/tokens**: regenera-regenera-regenera = la forma MÁS cara de usar IA
     ("$50 en resolver lo que otro resuelve por 50 céntimos = problema de empleabilidad")
  2. **Deuda técnica invisible**: código no leído = funciona hoy, nadie verificó seguridad/
     escalabilidad/errores; los intereses cobran en producción, los viernes.
  3. **Estancamiento personal**: mientras haces vibe coding no aprendes — delegas las
     decisiones de arquitectura, que son la parte más valiosa de la profesión.
- **Flujo profesional en 4 pasos** (el corazón del vídeo):
  1. **Especificar** antes de generar — spec-driven development, el doc es el CONTRATO
     con el agente ("hazme una app de hábitos" → 4 bloques: qué hace, funcionalidades v1,
     qué NO tiene todavía, datos y tecnologías)
  2. **Diseñar** la arquitectura con la IA como CONSULTORA (pide 2 opciones con pros/contras;
     elegir = criterio humano)
  3. **Dirigir** generando por piezas con contexto (pieza a pieza, leer entero, preguntar,
     ajustar, commit y git, siguiente)
  4. **Revisar** con criterio: 3 preguntas por bloque (¿dato inesperado? ¿compromete
     seguridad? ¿podría explicarlo a otra persona?) + truco: **sesión limpia de IA auditando
     a otra IA y un humano decidiendo al final**
- **Cuándo SÍ está bien el vibe coding**: prototipos desechables, scripts usar-y-tirar,
  explorar librerías. Línea roja: usuarios reales, datos reales, mantenimiento, dinero →
  ingeniería de software.
- **Frase del vídeo**: "El problema nunca fue hacer vibe coding, el problema es no saber
  hacer otra cosa."
- **Cierre**: "Generar código sin más ya no vale nada. El mercado paga por dirigir el
  proceso: especificar, diseñar, revisar y responsabilizarte del resultado."

## 🔴 Opinión del lab (ver análisis de la sesión) — veredicto: MEDIO-ALTO, alineado al 100%

El lab YA implementa esta filosofía en producción:
- Skills con procedimientos explícitos = especificar
- Gate de veracidad + revisor + verificar_research.py = revisar con criterio
- "IA audita a IA + humano decide" = EXACTO el patrón del lab (gate + revisor + humano)
- Regla de costes (después de 12:00 → local 0 €) = contra la "factura 1" de Moure
- Spike/experimentos desechables = vibe coding legítimo acotado

Matiz honesto: el vídeo tiene un titular provocador ("fin del vibe coding") pero la tesis
real es matizada — el vibe coding MUERE como metodología de producción, no como herramienta
de prototipado. La línea roja ("usuarios reales → ingeniería") es la regla correcta.

Conexión directa con el TFM/empleo del usuario: "¿sabes usar IA con criterio y sin
arruinarte en tokens?" es EXACTAMENTE la habilidad que el lab entrena y que el mercado paga.

---

**Seguimiento del mismo canal (continuación):** `analisis-mouredev-sdd-vibe-coding.md` —
MoureDev, «El fin del Vibe Coding: crea software robusto» (live 02-sep-2026): curso completo
paso a paso de **Spec Driven Development (SDD)** con un proyecto Python real. Conecta con
`analisis-spec-driven-vs-vibe-coding.md`.
