---
title: "Análisis: QM — agent harness open-source de Y Combinator (dailydoseofds_)"
type: research
---

# Análisis: QM — agent harness open-source de YC (dailydoseofds_)
**VERACIDAD:** [VERIFICADO]

**Fuente**: https://www.instagram.com/dailydoseofds_/p/DdDnvobD4Gp/ · @dailydoseofds_ · 08-sep-2026
**Formato**: post con caption extenso (30 likes, 0 comments) — contenido real en el texto
**Estado**: [VERIFICADO] caption literal + repo GitHub real + web oficial + README
**Fecha análisis**: 09-sep-2026 (21:40 CEST)

## Claim del post (caption, resumen literal)

Y Combinator open-sourceó el agent harness que corre internamente: **QM** (quartermaster). Contexto del post:
- YC empezó con un agent loop pequeño en Ruby (datos internos), luego añadió crons y webhooks.
- Después **aprovisionó 50+ agentes Hermes** como asistentes personales individuales. Gestionar una flota de ese tamaño se volvió un trabajo en sí.
- QM es lo que construyeron en su lugar; corre en YC en accounting, legal, events e engineering. MIT, open source.

5 ideas que lo diferencian (según el post):
1. **Scope** = unidad de aislamiento, igual para una persona que para un canal de Slack: memoria propia, archivos, credenciales, permisos, jobs programados y sandbox.
2. **Sandbox durable**: las herramientas instaladas en una sesión siguen en la siguiente (la mayoría de entornos de ejecución se descartan tras cada run).
3. **Core pequeño**: identidad, policy, scheduler y agent loop; Postgres guarda sesiones, memoria y cola. Todo lo demás son plugins sobre su HTTP API.
4. **Harness swappable**: Claude Code, Codex, OpenCode y Pi pueden conducir el mismo core → sin vendor lock.
5. **Seguridad en 3 niveles**: Strict (aprueba cada tool call), Dangerous (no pausa nada), Auto (clasificador sobre datos externos con *provenance labelling* antes de llegar al modelo) → respuesta concreta a prompt injection.

## Verificación externa (09-sep-2026)

- Repo real: **github.com/yc-software/qm** — «Multiplayer agent harness for work», **14,549 ⭐ / 1,767 forks**, MIT, creado 2026-07-29, rama main activa.
- Web oficial: **qm.ycombinator.com** (jul-2026) — confirma la historia: probaron varios harnesses, «the launch of OpenClaw pushed us in a new direction», luego 50+ Hermes agents, y construyeron QM por gestión de flota: «as flexible as Hermes, but with the simplicity of our original system», self-hosted.
- README confirma: scopes personales/compartidos (memoria, archivos, keychain, permisos, crons, web apps, sandbox durable), Slack + web, admin control, skills scope-owned compartibles por grant con import desde git, background work (crons/watches/webhooks), arquitectura Postgres + core headless (API/identity/policy/scheduler) + agent loop (Pi/OpenCode/Claude Code) + per-scope sandbox.
- El core expone `execute` como una de sus herramientas: ejecuta comandos en el sandbox aislado del scope (su «ordenador durable»).
- Fecha del post (08-sep) coherente con repo creado 29-jul y web jul-2026 → no es noticia del día, pero es real y reciente.

## Valor para el lab

**Valor de ejecución BAJO-MEDIO (09-sep)**: el lab es 1 persona/1 host — QM (Postgres multiusuario, Slack, flota) NO aplica como despliegue. No instalar.

**Valor de VALIDACIÓN ALTO (09-sep)**: YC probó 50+ agentes Hermes reales y su conclusión es que Hermes escala (lo usaron como estándar de comparación: «as flexible as Hermes»). Confirma la elección de stack del lab (Hermes + skills + crons + MCP). Los scopes aislados con memoria/credenciales/permisos propios, skills compartibles y sandbox durable son exactamente el modelo conceptual que el lab ya usa (profiles, skills, rutas protegidas).

**NUEVO menor (patrón de seguridad por procedencia)**: el nivel «Auto» — clasificador que examina el *origen* de los datos externos antes de que lleguen al modelo — es la pieza genuinamente nueva frente a la defensa actual del lab (tirith fail-closed, gate-veracidad, RULE-013). Idea a revisar a la vuelta: ¿screening de procedencia de tool results como capa anti-prompt-injection?

## Nota de contexto
- dailydoseofds_ = canal de referencia del usuario (TG IA + IG vigilado).
- Detectado por cron IG 09-09 (20 posts 08-sep), analizado a petición del usuario antes del viaje a Gijón (LAB apagado 10-13 sep).
- Post hermano del mismo barrido descartado: mentalhotfix «agentes en CI/CD testing UI desde .MD sin Selenium» = vídeo especulativo (9 likes, 1 comment, sin repo/demo) → NO registrado.
- Pendiente de decisión a la vuelta: si revisar el patrón de seguridad por procedencia de QM como mejora del lab (issue abierto en backlog).
