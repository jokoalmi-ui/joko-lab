---
title: "Análisis — Spec-Driven Development (lidr.co, Álvaro Moya)"
type: research
---

# Análisis — Spec-Driven Development (lidr.co, Álvaro Moya)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 13-ago-2026 (15:50 CEST)
**Fuente:** https://www.lidr.co/blog/spec-driven-development/ (08-06-2026)
**Autor:** Álvaro Moya — LIDR (máster AI4Devs)

---

## Contenido resumido

### Definición
**Spec-Driven Development (SDD)** = metodología guiada por especificaciones
claras y formales que actúan como fuente de verdad para diseñar, implementar y
validar el sistema. La especificación precede y guía al código.

**Punto clave:** "la spec se convierte en el artefacto que el agente ejecuta.
Si la spec está clara, el agente ejecuta. Si no, improvisa."

### El dato METR (julio 2025)
Ensayo controlado aleatorizado: developers experimentados predijeron +24% de
velocidad con IA; el resultado medido fue **19% MÁS LENTOS**. Y seguían
convencidos de haber ido más rápido. "Sin método, la IA añade fricción
invisible. La spec te hace predecible. Predecibilidad gana a velocidad."

### 2 niveles de spec (deben convivir)
| Tipo | Qué define | Quién |
|---|---|---|
| **Spec de sistema** | Arquitectura, convenciones globales, modelo de datos, patrones | Tech Lead/CTO |
| **Spec de feature** | Un cambio concreto: qué, criterios de aceptación, restricciones, tareas | Developer |

### Elementos de una spec de feature (Markdown)
Objetivo, Capacidades, **Criterios de aceptación** (Given/When/Then),
Restricciones, Decisiones técnicas, Casos de error, Tareas.

### El ciclo OpenSpec (6 pasos)
1. **User Story** — requisito en lenguaje de negocio
2. **Refined User Story** — el agente enriquece/clarifica y detecta ambigüedades
3. **Proposal Artifacts (la spec)** — criterios de aceptación, arquitectura, plan
4. **Apply** — el agente genera rama, tests, documentación, código, testing report
5. **Revisión humana + PR** — revisar que cumple la spec (no cada línea)
6. **Verify + Archive** — verificación final y cierre

### Herramientas SDD
OpenSpec (LIDR), BMAD-Method, GitHub Spec Kit, Kiro (AWS), Claude Code +
CLAUDE.md, Cursor + .cursorrules.

### Errores comunes
- Spec ambigua ("la ambigüedad no desaparece: se delega")
- Sobre-especificar (quita margen al agente)
- Confundir SDD con waterfall (la spec evoluciona)
- No versionar las specs (si no está en git, no es fuente de verdad)
- Escribirla en solitario

### Dato: Qodo State of AI Code Quality 2025
El **65% de developers** reporta que la IA pierde el contexto relevante en
tareas críticas. "Es un fallo del input."

---

## 🎯 Veredicto — ESTO ES EXACTAMENTE LO QUE EL LAB YA HACE (LPA)

| Concepto del artículo | El lab | Estado |
|---|---|---|
| Spec de sistema | GUIA-JOKO-LAB + AGENTS.md + skills | ✅ **Implementado** |
| Spec de feature | Plantillas LPA + SVP + plan (skill plan) | ✅ **Implementado** |
| Criterios de aceptación | KVC/KCR, gates de evidencia TD-001 | ✅ |
| Revisión por criterios (no líneas) | SVP, state-verification-pattern | ✅ |
| Spec versionada en git | GUIA versionada (v1.3.x), backups | ✅ |
| Ciclo User Story → Archive | OBS→HYP→EXP→DEC + OPs | ✅ |

### 📌 Lo que APORTA (novedad real)
1. **Dato METR validado**: el estudio de que la IA sin método hace +19% LENTO
   — **justificación objetiva de por qué el lab es LPA/Spec-Driven** (material
   para LinkedIn/TFM)
2. **El concepto "la ambigüedad no desaparece: se delega"** — frase potente
   para explicar por qué se escribe la spec antes
3. **OpenSpec como referencia** si algún día se formaliza el flujo en CLI
   (hoy el lab usa plan + TDD, que cubre lo mismo)

### ⚠️ Honesto
- Blog de escuela (vende máster AI4Devs)
- El lab ya tiene TODO esto implementado de forma nativa (LPA + SVP + plan +
  TDD) — el artículo valida el método, no aporta nada que falte

**Conclusión: VALIDACIÓN de la metodología LPA del lab con evidencia externa
(METR, Qodo). Material para LinkedIn/TFM. Sin futuribles técnicos.**
