---
title: "Análisis — Context Engineering (lidr.co, Álvaro Moya)"
type: research
---

# Análisis — Context Engineering (lidr.co, Álvaro Moya)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 13-ago-2026 (15:55 CEST)
**Fuente:** https://www.lidr.co/blog/context-engineering/
**Autor:** Álvaro Moya — LIDR (máster AI4Devs)

---

## Contenido resumido

### Definición
**Context Engineering** = la disciplina de diseñar y gestionar TODA la
información que un sistema de IA recibe antes de generar una respuesta. No es
solo el prompt: instrucciones del sistema, memoria del proyecto, documentos
relevantes, herramientas disponibles y estado de la sesión.

**Karpathy + Tobi Lütke (CEO Shopify) lo hicieron viral:** "los modelos
predicen el siguiente token basándose exclusivamente en lo que tienen en su
ventana de contexto. Si tienen un prompt suelto, improvisarán. Si tienen el
contexto completo — especificaciones, flujo de trabajo, historial — ejecutarán."

### Context vs Prompt Engineering
| Dimensión | Prompt Eng | Context Eng |
|---|---|---|
| Alcance | Una instrucción | Todo el ecosistema |
| Naturaleza | Estático | Dinámico (se gestiona durante la sesión) |
| Escalabilidad | Tareas simples | Tareas complejas/sistemas reales |
| Dónde vive | Chat/código | Config, repos, herramientas |
| Quién | Cualquiera | El responsable del contexto |

**Analogía:** "un copiloto sin contexto es como un junior sin onboarding. Uno
bien configurado es un senior que ya pasó el onboarding."

### Las 3 capas (independientes, versionables)
1. **Especificaciones técnicas** — stack, arquitectura, modelo de datos,
   patrones, convenciones (naming, git, tests, errores, logging). La capa más
   estable. Vive en ficheros .mdc referenciados desde un archivo base.
2. **Flujo de trabajo** — cómo trabaja el equipo desde la petición hasta
   producción: qué proceso, quién interviene, qué entregable, qué define
   "excelente" para cada entregable. "Un agente que no sabe que antes del
   código va una spec no va a pedirla."
3. **Contexto compartido y actualizado** — consistencia (mismas reglas),
   coherencia (refleja cómo se trabaja REALMENTE), independencia del prompt,
   independencia del seniority (junior con contexto correcto > senior sin él).

### DORA 2025 (Google, ~5.000 profesionales, septiembre 2025)
Dato citado sobre el impacto del contexto en el rendimiento de equipos.

### Errores comunes
(sección parcial — el artículo los lista, con el patrón de los otros artículos:
prompt suelto, contexto desactualizado, contexto individual no compartido)

---

## 🎯 Veredicto — EL LAB ES UN CASO DE ESTUDIO DE CONTEXT ENGINEERING

| Capa del artículo | El lab | Estado |
|---|---|---|
| **1. Especificaciones técnicas** | GUIA-JOKO-LAB, AGENTS.md, skills con stack | ✅ **Implementado** |
| **2. Flujo de trabajo** | LPA (OBS→HYP→EXP→DEC), SVP, plan, TDD | ✅ **Implementado** |
| **3. Contexto compartido** | File bus (lab.md, cli.md), skills versionadas, memoria Hermes | ✅ **Implementado** |

### 📌 Conexión directa con HOY
El artículo valida EXACTAMENTE lo que hicimos hace 3 horas:
- **Context Pruning** (threshold 0.4) = gestionar el "estado de la sesión"
- **Compactación de skills** = curar y descartar contexto
- **`enabled_toolsets` en crons** = "herramientas disponibles" del contexto
- **Hermes memory + profile** = "instrucciones del sistema y memoria del
  proyecto"

**El lab NO solo aplica Context Engineering — lo MIDE** (coste por contexto,
compactación, OPs). Eso va más allá del artículo.

### 🟡 Única idea potencialmente nueva
El artículo menciona **ficheros .mdc referenciados desde un archivo base**
(estilo Cursor) para las especificaciones técnicas. El lab usa GUIA + skills,
que cumplen el mismo papel — pero la estructura de "ficheros de estándares
independientes + archivo base que los referencia" podría formalizar mejor la
GUIA si crece. Futurible menor.

### ⚠️ Honesto
- Blog de escuela (vende máster)
- El artículo cita DORA pero no da el dato concreto en el texto visible
- El lab está POR DELANTE del artículo (mide + versiona + comparte)

**Conclusión: VALIDACIÓN del lab como sistema de Context Engineering completo
+ conexión directa con el Context Pruning implementado hoy. Único futurible
menor: estructura .mdc/archivo-base para la GUIA.**
