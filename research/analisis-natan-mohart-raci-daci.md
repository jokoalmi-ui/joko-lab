---
title: "Análisis — \"RACI vs DACI: separar ejecución y decisión\" (natan_mohart, 01-sep-2026)"
type: research
---

# Análisis — "RACI vs DACI: separar ejecución y decisión" (natan_mohart, 01-sep-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcwARHnjHWH/ (@business__infographics / @natan_mohart, carrusel, 5 h)
**Fecha:** 2026-09-01 23:15 CEST

## Contenido — el marco completo (caption íntegro)

**Tesis**: "90% de los equipos no fallan por falta de talento, fallan porque nadie sabe quién es dueño de qué". No es un problema de skills, es un problema de **claridad**. Los equipos mezclan dos cosas: **ejecución** y **toma de decisiones**.

**Los dos frameworks:**

| Marco | Para qué | Roles |
|---|---|---|
| **RACI** | Claridad de EJECUCIÓN | **R**esponsible (hace el trabajo) · **A**ccountable (dueño del resultado) · **C**onsulted (aporta input) · **I**nformed (se mantiene al tanto) |
| **DACI** | Claridad de DECISIÓN | **D**river (impulsa el proceso) · **A**pprover (decisión final) · **C**ontributor (aporta) · **I**nformed (informado) |

**Qué cambió en su equipo**: reuniones más cortas, decisiones más rápidas, accountability obvio, "yo pensaba que esto era tuyo" desapareció.

**Insight clave**: "RACI arregla el caos de ejecución. DACI arregla el caos de decisión. La mayoría de equipos intentan resolver ambos con UN solo framework y se quedan sin ninguno".

**Su práctica**: RACI al inicio de cada proyecto, DACI para cada decisión relevante, **nada de propiedad compartida, nada de aprobación final compartida**.

## 🔴 Aplicación al LAB — VALOR MEDIO (validación del diseño de roles del kanban)

| Ángulo | Veredicto |
|---|---|
| **Separar ejecución y decisión** | 🟢🟢 **Es exactamente la tesis del kanban nativo del lab**: el verifier es independiente del worker (el worker NO se autoaprueba — el hallazgo del vídeo de Gentleman Programming lo confirmó hoy). El lab ya separa "quién hace" (worker) de "quién verifica/decide" (verifier) |
| **RACI del lab (ejecución)** | 🟢 Mapeo real: **Responsible** = worker kanban · **Accountable** = root card / synth (dueño del entregable) · **Consulted** = skills + RAG (aportan contexto) · **Informed** = el usuario (recibe el resumen final) |
| **DACI del lab (decisión)** | 🟢 Mapeo real: **Driver** = Hermes (impulsa el proceso) · **Approver** = verifier + gates fail-closed (decisión final: PASS/FAIL) · **Contributor** = workers · **Informed** = usuario. El **verifier = Approver** es la pieza que el lab ya tiene y la mayoría de frameworks de agentes no |
| **"Un solo framework = ninguno"** | 🟡 Lección útil: el lab usa el kanban para AMBAS cosas (ejecución y decisión) con roles explícitos — no mezcla. El riesgo sería que un agente fuera a la vez worker y approver de su propio trabajo (autoaprobación) |
| **"No shared ownership / no shared final approval"** | 🟢 Coincide con la regla del lab: **nunca el mismo agente que redactó es revisor** (revisor SIEMPRE en sesión, independiente) |

**Conclusión**: VALOR MEDIO — el post es sobre gestión de equipos humanos (no agentes), pero su tesis central **valida el diseño de roles del kanban del lab** (ejecución y decisión separadas, verifier = approver independiente, sin autoaprobación). No aporta nada nuevo que implementar — el lab ya lo ejecuta; es confirmación externa del patrón maker-checker que el lab adoptó (fallo 33% de MAST resuelto).

## Notas de honestidad

- **Carrusel visual no transcrito** (el caption contenía el contenido completo; las slides probablemente repiten el mismo marco con gráficos RACI/DACI — el caption es íntegro y suficiente).
- Autor: **natan_mohart** (perfil de infografías de negocio, @business__infographics) — no es un canal técnico de IA; el valor está en la analogía con agentes, no en el contenido de negocio en sí.
- El comentario del usuario "principalmhood" pide más info de DACI — señal de que el post funciona como contenido, pero no relevante para el lab.
- 2 likes / 14 "me gusta" totales — métricas bajas, irrelevantes para el valor del contenido (el lab no juzga por métricas).
