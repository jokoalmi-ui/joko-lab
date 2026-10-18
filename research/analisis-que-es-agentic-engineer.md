---
title: "Análisis — Qué es Agentic Engineer (lidr.co, Álvaro Moya)"
type: research
---

# Análisis — Qué es Agentic Engineer (lidr.co, Álvaro Moya)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 13-ago-2026 (15:43 CEST)
**Fuente:** https://www.lidr.co/blog/que-es-agentic-engineer/
**Autor:** Álvaro Moya — lidr.co (escuela AI-Powered Careers, máster AI4Devs)
**Tipo:** artículo educativo/marketing (blog de escuela, con UTM de Google Ads)

---

## Contenido resumido

### Definición
El **Agentic Engineer** es el developer que diseña, coordina y supervisa
sistemas donde múltiples agentes de IA trabajan de forma autónoma. No escribe
cada línea de código — diseña la arquitectura del sistema multiagente, define
cómo interactúan los agentes y establece los criterios de validación.

**Karpathy:** "en los flujos agénticos el developer ya no escribe código
directamente la mayor parte del tiempo. Orquesta los agentes que lo escriben."

### Diferencia con AI Engineer (importante)
- **AI Engineer**: construye productos con IA (chatbots, pipelines RAG, sistemas
  de recomendación)
- **Agentic Engineer**: coordina agentes de IA (diseña el sistema donde esos
  agentes ejecutan de forma fiable)
- **Complementarios, no sinónimos**

### Día a día (6 tareas)
1. **Diseñar la arquitectura multiagente** — qué agentes, cómo se comunican,
   qué estado comparten, qué restricciones. Si el sistema falla, sabe en qué
   agente está el problema
2. **Escribir la spec** que los agentes van a ejecutar (Spec-Driven)
3. **Configurar el contexto** de cada agente (CLAUDE.md con convenciones, stack,
   lo prohibido)
4. **Establecer guardrails** — qué hace cada agente autónomo vs qué requiere
   aprobación humana
5. **Revisar outputs al nivel de criterios** — "¿cumplió la spec?", no "¿está
   bien escrito cada bloque?"
6. **Medir y mejorar el sistema** — logs de decisiones, costes en tokens,
   latencia, calidad

### Las 4 skills
1. **Spec-Driven Development** — contratos en Markdown ejecutables
2. **Context Engineering** — qué entra en el contexto de cada agente, cómo se
   actualiza, qué se descarta
3. **Diseño de sistemas multiagente** — módulos, contratos entre agentes,
   restricciones de coordinación
4. **Validación y observabilidad** — comprobar automáticamente que cada agente
   hizo bien su tarea (antes de ejecutar, no después)

### En equipo
"Sin specs compartidas, sin contexto común, sin criterios de validación
acordados. El resultado no es adopción. Es variabilidad. Y la variabilidad se
paga en PRs impredecibles y pérdida de confianza."
Caso Bdeo: de adopción de copilots a agentes especializados + MCP servers +
frameworks multiagente.

---

## 🎯 Veredicto — DESCRIBE EXACTAMENTE AL USUARIO (el lab ES esto)

| Skill del artículo | El usuario/lab | Estado |
|---|---|---|
| **Spec-Driven Development** | LPA + Spec-Driven (skill plan, verificaciones) | ✅ **NÚCLEO del método** |
| **Context Engineering** | Contextos por tarea, GUIA-JOKO-LAB, AGENTS.md, compression | ✅ **Implementado** (aún más: compactación de skills, context pruning hoy) |
| **Diseño de sistemas multiagente** | Hermes orquestador + skills + delegate_task + OpenCode worker | ✅ **Implementado** |
| **Validación y observabilidad** | Tests 205 OK, ledgers, evaluar_rag, métricas | ✅ **Implementado** |

### Día a día — el lab ya lo hace todo:
| Tarea del artículo | Lab |
|---|---|
| Arquitectura multiagente | Hermes + skills + subagentes |
| Escribir specs | LPA, Spec-Driven, TDD |
| Configurar contexto | AGENTS.md, GUIA, contextos |
| Guardrails | Confirmación explícita (acciones destructivas) |
| Revisar por criterios | SVP, KVC, KCR, gates |
| Medir y mejorar | Ledgers, OPs, métricas de coste |

### 📌 Relevancia para el usuario
1. **VALIDACIÓN de identidad**: "Agentic Engineer" es el nombre del perfil que el
   lab ya implementa. Útil para LinkedIn (búsqueda de empleo) y para explicar
   qué hace.
2. **Conexión con lo de hoy**: el "Context Engineering" del artículo = el
   Context Pruning que implementamos hace 2 horas. Validación cruzada.
3. **Material de FORMATO para LinkedIn Lab**: estructura concepto → por qué →
   día a día → 4 skills → caso real → gancho. El mismo patrón del carrusel de
   Maurys Álvarez.

### ⚠️ Nota honesta
- El artículo es de una escuela que vende un máster (AI4Devs) — hay CTA de
  inscripción por todas partes. El contenido técnico es correcto pero el
  objetivo es captación de alumnos.
- No aporta NADA técnico nuevo al lab (todo lo que describe ya está
  implementado) — pero SÍ aporta **vocabulario para hablar del perfil** y
  validación del modelo operativo.

---

## Conclusión

**VALIDA la identidad del lab**: el "Agentic Engineer" del artículo es
exactamente lo que el usuario ya es/hace con Hermes + skills + subagentes.
Aporta: (1) vocabulario profesional para LinkedIn/empleo, (2) referencia de
formato para el LinkedIn Lab, (3) validación cruzada del Context Engineering
(lo que implementamos hoy). No aporta novedad técnica.
