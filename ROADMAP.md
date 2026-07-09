# ROADMAP de Joko Lab

"No quiero un chatbot. Quiero un compañero que entienda mi laboratorio y evolucione conmigo."

Hoja de ruta del laboratorio personal de IA y automatización.
Cada hito representa una mejora concreta, ordenada por prioridad.

## Visión

Construir un laboratorio de IA personal, local y mantenible,
gestionado principalmente por Hermes Agent, donde toda la
infraestructura pueda comprenderse, documentarse y evolucionar
de forma segura.

---

## Fase 1: Consolidar lo que tenemos

Objetivo: que lo existente esté documentado, estable y comprobado.

| # | Tarea | Prioridad | Estado |
|---|---|---|---|
| 1.1 | Poblar skills especializadas: `docker-admin`, `n8n-admin`, `ai-router`, `hermes-expert`, `betterbird`, `perfumes` | Alta | ✔ Hecho (hermes-expert) |
| 1.2 | Desarrollar `hermes.md` con el contenido del esquema actual | Alta | Pendiente |
| 1.3 | Decidir qué hacer con `scripts/`, `backups/` y `test/` (poblar o limpiar) | Media | Pendiente |
|1.4 | Unificar `hermes-notes.md` y `hermes-internals.md` en un solo documento | Media | ✔ Hecho (archivados como obsoletos) |
| 1.5 | Unificar la filosofía de trabajo (actualmente duplicada entre SKILL.md y system prompt) | Media | Pendiente |
| 1.6 | Primera batería de pruebas de humo: verificar que cada servicio responde | Alta | Pendiente |

---

## Fase 2: Automatización local

Objetivo: que el laboratorio haga cosas útiles sin depender de la nube.

| # | Tarea | Prioridad | Estado |
|---|---|---|---|
| 2.1 | Workflow en n8n que consuma Ollama para tareas de texto locales | Alta | Pendiente |
| 2.2 | Workflow en n8n que procese PDFs con Stirling-PDF + Ollama | Alta | Pendiente |
| 2.3 | Workflow en n8n que envíe notificaciones (WhatsApp, email) | Alta | Pendiente |
| 2.4 | Script de respaldo automático del stack Docker y datos críticos | Media | Pendiente |
| 2.5 | Script de limpieza de logs y temporales del laboratorio | Baja | Pendiente |

---

## Fase 3: Agente más capaz

Objetivo: que Hermes resuelva más tareas sin intervención manual.

| # | Tarea | Prioridad | Estado |
|---|---|---|---|
| 3.1 | Skill `docker-admin` completa: diagnósticos, logs, inspección de contenedores | Alta | Pendiente |
| 3.2 | Skill `n8n-admin` completa: estado, logs, workflows colgados | Alta | Pendiente |
| 3.3 | Skill `ai-router` funcional: elegir modelo según tarea (local vs online) | Media | Pendiente |
| 3.4 | Integración de Hermes con Ollama como proveedor interno | Media | Pendiente |
| 3.5 | Capacidad de Hermes para llamar a n8n webhooks desde terminal | Baja | Pendiente |

---

## Fase 4: Monitorización y control

Objetivo: saber en todo momento qué pasa en el laboratorio.

| # | Tarea | Prioridad | Estado |
|---|---|---|---|
| 4.1 | Dashboard del monitor LM Studio: estable y funcional | Media | Pendiente |
| 4.2 | Añadir estado del stack Docker al monitor | Media | Pendiente |
| 4.3 | Añadir estado de n8n (workflows activos/fallidos) al monitor | Baja | Pendiente |
| 4.4 | Alertas simples cuando un servicio caiga | Baja | Pendiente |

---

## Fase 5: Expansión controlada

Objetivo: añadir nuevas capacidades solo cuando lo existente esté sólido.

| # | Tarea | Prioridad | Estado |
|---|---|---|---|
| 5.1 | Integrar Betterbird como skill para gestión de correo local | Media | Pendiente |
| 5.2 | Explorar si hace falta un buscador semántico local (alternativa a mem0) | Baja | Pendiente |
| 5.3 | Evaluar si integrar algo de la suite de Home Assistant o similar | Baja | Pendiente |
| 5.4 | Skill perfumes: base de datos local de la colección | Baja | Pendiente |

---

## Criterios de prioridad

| Prioridad | Cuándo aplica |
|---|---|
| **Alta** | Desbloquea otras tareas, estabiliza el laboratorio o cubre un riesgo |
| **Media** | Mejora significativa pero no urgente |
| **Baja** | Deseable, no bloquea nada |

## Principios para decidir qué hacer después

1. **Consolidar antes de expandir.** No pasar a la Fase 2 si la Fase 1 no está completa.
2. **Una cosa a la vez.** No empezar varias tareas de alta prioridad simultáneamente.
3. **Documentar cada paso.** Cada tarea completada debe dejar rastro en `decisiones.md` o en el documento correspondiente.
4. **Revisar el roadmap periódicamente.** El orden puede cambiar según necesidades reales.

---

*Última actualización: 2026-07-03*
