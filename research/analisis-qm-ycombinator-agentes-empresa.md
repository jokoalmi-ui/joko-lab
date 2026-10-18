---
title: "Análisis — ¿Adiós a los Agentes IA Individuales? Y Combinator libera QM (Alejandro Pardo, 16-ago-2026)"
type: research
---

# Análisis — ¿Adiós a los Agentes IA Individuales? Y Combinator libera QM (Alejandro Pardo, 16-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/7hT1sF5dcb0 (Alejandro Pardo | IA Automatización, ~15 min, es)
**Transcripción:** completa (es)

## Qué es QM (Quarter Master)
- Y Combinator construyó 50+ **Hermes agents** para empleados individuales y la gestión se volvió un caos → construyeron **QM** ("quarter master" = la persona que coordina el orden en un barco).
- **Open source** (lanzado 31-jul-2026, **13.200 ⭐ en 13 días**). Para organizar y gestionar agentes de IA a escala en empresas.
- Idea: fusionar la simplicidad (su agente Ruby original) con la flexibilidad/potencia (50 Hermes agents).

## Conceptos clave
1. **Arnés (harness)**: capa que convierte un LLM en "trabajador" (bucle pensar→ejecutar→resultado). Ejemplos: Claude Code, Codex, OpenCode, **Hermes**, OpenClaw. Los de programación (Codex/Claude Code) vs genéricos (Hermes/OpenClaw).
2. **Scope**: = "oficina"/espacio de trabajo. Cada scope tiene SU memoria, archivos, permisos, keys y sandbox. El arnés entra/sale del scope. **El scope define DÓNDE puede trabajar; el arnés define CÓMO trabaja.** Permite cambiar de arnés sin perder nada (memoria externa en Postgres).

## Arquitectura
- **Entradas**: Slack (empresa) + interfaz web (chat) + panel administrador (usuarios, permisos, modelos).
- **Core headless** (backend): API → **orquestador** (código, no IA: identifica usuario → scope → permisos) → capa de seguridad (deniega/requiere aprobación humana) → **scheduler** (crons) → **Postgres** (estado: trabajadores, scopes, sesiones — memoria EXTERNA distinta de la del agente) → **arnés router** (elige arnés según tarea: Codex para programación, Claude Code para marketing...).
- **Sandbox por scope**: entorno aislado (Linux, Node, Git, herramientas) con sus credenciales (CRM, GitHub, correo) y durable (terminal persistente).
- **Sistemas externos**: correo, CRM, ERP, Drive vía herramientas/CLI/APIs.
- **Instalación**: Docker + Git + Node 24+; build imagen base; `qm` dev instance (no producción); túnel SSH → panel admin → configurar modelo (OpenAI/Anthropic/OpenRouter — NO OAuth con planes Codex/GPT) → conectar arnés. Producción: fly.io / AWS (soporte oficial), no Docker dev.

## Funcionalidades de governance (por scope)
- **Autonomía**: auto / aprobación humana / estricto-peligroso.
- Reglas de comandos permitidos/prohibidos en el sandbox.
- System prompt ("soul"), red/network, quién puede usar Slack, qué modelos/proveedores.
- Sesiones (registro de cada conversación), auditoría (acciones administrativas y accesos sensibles), archivos, skills, memoria, métricas, crons, integraciones, usuarios.

## Veredicto para el lab
**VALIDA la arquitectura del lab + NO accionable ahora:**
- **Lo que ya hace el lab sin QM**: el concepto de **scope** ≈ lo que el lab hace con perfiles + file bus + skills por proyecto (memoria, archivos, reglas). Hermes ya tiene: agentes, skills, crons, integraciones, memoria persistente, sesiones.
- **Lo que el lab NO tiene (y no necesita)**: sandbox aislado por proyecto, permisos multi-usuario, auditoría administrativa, router entre arneses múltiples. QM resuelve el problema de DECENAS de trabajadores/equipos — Joseba es 1 persona (Joko Lab), el overhead no compensa.
- **Confirmación externa valiosa**: YC eligió **Hermes agents como uno de los arneses** que integran → validación de terceros del stack del lab.
- **Útil como material didáctico** (TFM/LinkedIn): "cómo se orquesta una flota de agentes en empresa" — el concepto scope/arnés es visual y se explica bien.

## Registro
- Guardado: research/analisis-qm-ycombinator-agentes-empresa.md
- Veredicto: valida arquitectura lab; no accionable (multi-usuario, 1 persona); material TFM/LinkedIn; QM usa Hermes = validación externa.
