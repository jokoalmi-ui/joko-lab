---
title: "Análisis — Póster \"RACI & DACI: Frameworks for Roles, Responsibility & Decision-Making\" (25-ago-2026)"
type: research
---

# Análisis — Póster "RACI & DACI: Frameworks for Roles, Responsibility & Decision-Making" (25-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcfhRx1j5d5/ (askpstudyinaustralia, 25-ago, 9 likes, 0 comentarios — visual de Natan Mohart)
**Método:** pipelina IG → caption mínimo → imagen única (1152×1440) descargada y transcrita con GLM-4.6V local (franja 08-12, 0 €, 2 pasadas)

## Qué propone el póster

Dos frameworks de gestión de roles/responsabilidades y decisiones:

### RACI — Matriz de asignación de responsabilidades
Responde: **"¿Quién es responsable de qué?"**
- **R (Responsible)**: el que ejecuta el trabajo
- **A (Accountable)**: el dueño, responde del resultado
- **C (Consulted)**: el experto, aporta input y feedback
- **I (Informed)**: se le mantiene al tanto del progreso

Cuándo: gestión de proyectos, onboarding, procesos recurrentes, tareas cross-funcionales, eliminar solapamientos.
Buenas prácticas: **solo UN Accountable por tarea** (nunca dos) · varios R OK, varios A no · C/I lean para evitar ruido · actualizar la matriz cuando cambia el equipo · construir el RACI al inicio del proyecto, no al final.

### DACI — Framework de toma de decisiones
Responde: **"¿Quién toma la decisión?"**
- **D (Driver)**: el organizador, mueve el proceso
- **A (Approver)**: el que decide, la llamada final
- **C (Contributor)**: aporta expertise y datos
- **I (Informed)**: notificado cuando se decide

Cuándo: decisiones estratégicas, roadmaps, aprobaciones de presupuesto, hiring, resolución de conflictos.
Buenas prácticas: **solo UN Approver** (aprobar compartido paraliza) · **Driver ≠ Approver** (roles separados) · limitar Contributors a 3-5 · documentar la decisión y su contexto por escrito · plazo claro para decidir.

## 🔴 Aplicación al LAB — VALOR MEDIO-ALTO (metodología, no herramienta)

| Ángulo | Veredicto |
|---|---|
| **RACI → delegación multi-agente** | 🟢 **Aplicable directamente**: el lab ya orquesta subagentes (delegate_task batch, PRD graph delegación). Mapear roles RACI en el pipeline (investigador=R, coordinador=A, revisor=C, usuario=I) formalizaría el patrón que ya se usa de facto |
| **DACI → decisiones del lab** | 🟢 **Encaja con el patrón del lab**: el usuario es SIEMPRE el Approver (A) — regla "veredicto usuario" + gates (f0/f1/f2). Driver = Hermes, Contributors = subagentes/investigación, Informed = Telegram. Formalizar DACI = el usuario A único, Hermes D — nunca Hermes A |
| **"Un solo A / un solo Approver"** | 🟢 Refuerza las reglas existentes del lab: "Confianza: solo datos; veredicto usuario" — el usuario es el único Approver de decisiones grandes |
| **Documentar decisiones por escrito** | 🟢 El lab YA lo hace (backlog + research + DECISIONES) — validación del hábito |
| **Herramienta nueva** | ❌ No instalar nada: es metodología, no software |

**Futurible ligero**: formalizar un "RACI del lab" en una skill/referencia (roles de cada agente del pipeline: investigador/revisor/coordinador; usuario = A único) — ayudaría a explicar el diseño del lab en LinkedIn/TFM y a razonar la delegación. Sin coste, solo documentación.

**Conclusión**: VALOR MEDIO-ALTO como metodología — valida el patrón de gobernanza del lab (usuario = único Approver, Hermes = Driver, subagentes = R/C) y da vocabulario para el TFM/LinkedIn. Sin cambios de stack.
