---
title: "Análisis — \"Hermes Agent Skills That Make It 10x More Powerful\" (AI LABS, 30-ago-2026)"
type: research
---

# Análisis — "Hermes Agent Skills That Make It 10x More Powerful" (AI LABS, 30-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.youtube.com/watch?v=WJgxX0Eib6k — canal **AI LABS** (`@AILABS-393`, id `UCelfWQr9sXVMTvBzviPGlFw`), subido **30-08-2026**, **11 m 54 s** (714 s), 127.382 vistas / 2.130 likes / 30 comentarios (yt-dlp, 29-09-2026 19:50:55 CEST). **Contenido patrocinado** (Plural.sh) + CTA a comunidad propia (ailabspro.io).
**Método:** pista de subtítulos **original** `en-orig` (42.285 B crudos → **14.121 chars** tras limpiar VTT karaoke y deduplicar por n-gramas); lectura **íntegra** de los 8 capítulos. Cifras de repos medidas con **dos instrumentos independientes** (API de GitHub 29-09-2026 19:53:20 CEST; HTML de GitHub + shields.io 29-09-2026 19:54:02 CEST) y leídas del volcado en fichero. Anti-duplicado: **0 coincidencias previas** por id de vídeo y 0 por canal.

## Veredicto: ENTRA — por los criterios (b) y (c) del ledger, no por (a)

El criterio del propio `04-operations/metrics/aplicabilidad_ledger.jsonl` es: entra **solo** si aporta (a) cifra medida con fuente, (b) técnica implementable en el stack real (Ollama / LM Studio / n8n / Qdrant-LanceDB / MCP) o (c) idea de experimento concreta. Este vídeo **no trae ninguna cifra verificable** (las suyas son *claims* de los autores), pero trae **dos técnicas implementables y un experimento medible**. De los 6 elementos de la lista: 2 ya estaban cubiertos, 1 es duplicado y 1 es publicidad.

## Elemento por elemento

**1) Planning with Files — `OthmanAdi/planning-with-files` — YA EN EL LAB**
27.180★ (API; HTML 27k), MIT, Shell, 26,9 MB, push 27-09-2026, 8 issues abiertas. «Persistent file-based planning… session recovery after /clear and compaction, per-turn re-injection against context rot, deterministic completion gate».
- Ya auditado el **04-09-2026** (recomendado en el audit de `awesome-hermes-skills`, recogido en `04-operations/backlogs/pendientes.md`) y **ya clonado** en `01-knowledge/references/planning-with-files/` → **679 ficheros** medidos hoy (el doc de la auditoría estructural contaba 185 con otro criterio; discrepancia anotada, no resuelta).
- Novedad menor: el índice del hub local ya ofrece una **versión en español** del mismo autor (`planning-with-files-es`).
- Aportación al lab: **ninguna nueva** (ya está en casa).

**2) Delegate Skills — `amElnagdy/delegate-skills` — DUPLICADO**
2.257★ (2.3k), MIT, JavaScript, push 20-09-2026, 25 issues abiertas. «Delegate a coding task to a separate coding agent CLI, **review the diff, land the commit yourself** — one per implementer».
- Es exactamente lo que el lab ya hace: `delegacion-subagentes` (delegación con salida cruda verificada) + `tools/opencode-local.sh` + el gate de recibos `joko-lab/hooks/pre-commit`, que obliga a **revisar el diff antes de commitear** (`joko-git-recibos`).
- Aportación: **0**.

**3) RTK — `rtk-ai/rtk` — CANDIDATO NUEVO (el de mayor tamaño)**
**82.005★** (API exacta; HTML `aria-label="82005 users starred this repository"`), Apache-2.0, Rust, 11,1 MB, push **29-09-2026 13:37Z**, **1.540 issues abiertas**. «CLI proxy that reduces LLM token consumption by 60-90% on common dev commands. Single Rust binary, zero dependencies».
- **0 referencias textuales previas en el lab.** Aviso de método: un `grep` amplio de `\bRTK\b` devolvía **38 ficheros**, pero eran **frames PNG** de un vídeo (falsos positivos); el grep de texto da 0.
- Encaje: ataca un dolor **medido** del lab — el coste de contexto por salidas de comandos largas (la anomalía recurrente «1 lines output» obliga ya a volcar a `/tmp` y leer el fichero; `agregacion-corpus-grande` resuelve el corpus grande, no la terminal).
- Caveats: el 60-90 % es **claim del propio repo**, no medición del lab → validar antes de confiar (RULE-015); 1.540 issues abiertas en un repo de 8 meses; es un *proxy* interpuesto en la ejecución de comandos (afecta al entorno del agente) ⇒ instalar = OK explícito + prueba acotada.

**4) Plural — PATROCINIO.** Infra/workbenches Kubernetes para el workspace del agente. El lab es local-first sobre Docker Compose: **no aplica**, nada que evaluar.

**5) Mantis — `google/mantis` — CANDIDATO NUEVO**
1.731★ (1.7k), Apache-2.0, Python, 1,8 MB, push 28-09-2026, **solo 2 issues abiertas**. «A modular, stack-agnostic toolkit for AI coding agents to autonomously find, reproduce, and patch vulnerabilities».
- La atribución del vídeo («de Google») es **correcta**: la organización del repo es `google`.
- **0 referencias previas en el lab** (el único hit del grep era un falso positivo de otro patrón). En el índice del hub **no aparece** `google/mantis`: el único «mantis» del catálogo es «MantisBT Manager» (gestor de incidencias, sin relación).
- Doble encaje: (a) auditoría de seguridad del código propio (`joko-lab/tools/`, `hooks/`), (b) material real para la unidad de **ciberseguridad del FP** (`ciberseguridad-fp`). Complementa a `requesting-code-review` (calidad) y al gate de recibos: Mantis busca/reproduce/parchea vulnerabilidades, no revisa estilo.

**6) Agent Reach — `Panniantong/Agent-Reach` — YA CERRADO**
86.160★ (86k), MIT, Python, push 15-09-2026, 166 issues abiertas. Lee/busca Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu con «cero cuotas de API».
- **Ya triado por el lab**: `research/analisis-miguebaena-agent-reach.md` → **«VALOR MEDIO — NO instalar»**. Esas vías ya están cubiertas por `reddit-reading`, `rss-feeds`, `blocked-page-recovery` (403/429/paywall) y `youtube-content` / `video-transcription`.

**Extra (capítulo 7) — Skill Retrieval — `moonlight-lupin/agent-skills` → `plugins/skill-retrieval` — CANDIDATO NUEVO, y es un PLUGIN de Hermes**
83★ (83 exactas), MIT, Python, push 29-09-2026 05:17Z. Contenido del subdirectorio: `plugin.yaml` 472 B, `__init__.py` 16.850 B, `SKILL.md` 8.252 B, `LICENSE`, `README.md`, `scripts/`, `tests/`.
- El repo se describe como «A collection of AI agent skills and plugins **for Hermes Agent**»: es el único de los 6 específico de Hermes y el único que **modifica el arranque de la sesión** (no es una skill más).
- Ataca un problema que el lab **tiene medido**: hoy hay **213 ficheros `SKILL.md`** instalados en `~/.hermes/skills/` (46 de ellos en `.archive/`), más 204 en `~/.hermes/profiles/` → el índice de skills viaja en cada turno. El vídeo cita la afirmación del autor: **11.000 → 2.300 tokens** por turno (ahorro >9.000). Es *claim*, no medición.
- Contexto local: ya existe `skill-compaction`, que reduce el **contenido** de las skills — enfoque distinto. Este plugin propone **recuperación selectiva** por turno. En el índice del hub **no aparece** (sí otra pieza de nombre parecido, `skill-retrieval-gate`, de otro autor, que decide si ejecutar `memory_search` antes de seguir una skill).
- Caveats: 83★ = madurez baja (1 issue abierta); sería el **primer plugin** del lab (`~/.hermes/plugins/` está **vacío**, verificado hoy); y toca la inyección de skills ⇒ un fallo ahí afecta a **todas** las sesiones, así que solo cabe experimento aislado y reversible.

## Cifras medidas (ninguna copiada del vídeo)

- **Estrellas** (coinciden los dos instrumentos): planning-with-files **27.180** · delegate-skills **2.257** · RTK **82.005** · mantis **1.731** · Agent-Reach **86.160** · agent-skills **83**.
- **Licencias / lenguaje / push**: MIT Shell (27-09) · MIT JS (20-09) · Apache-2.0 Rust (29-09 13:37Z) · Apache-2.0 Python (28-09) · MIT Python (15-09) · MIT Python (29-09 05:17Z). Ninguno archivado.
- **Vídeo**: `WJgxX0Eib6k`, AI LABS, 714 s, upload 2026-08-30, 127.382 / 2.130 / 30 (29-09-2026 19:50:55 CEST).
- **Corrección de método (propia)**: el primer intento del segundo instrumento devolvió `NO_LEIDO` en los 6 repos y el volcado del segundo intento **se dio por bueno sin leerlo** (la salida de terminal volvió recortada). Se releyó `/tmp/yt_stars3.txt` **antes** de publicar. Regla vigente y reforzada: nunca citar cifras desde una salida de terminal recortada («1 lines output») — volcar a fichero y leerlo.

## Veracidad del contenido (gate)

- **Correcto**: `google/mantis` es de la organización `google`; los 6 repos existen y sus cifras cuadran; el vídeo atribuye los ahorros a los autores («they claim»), no como hechos.
- **No verificable / claim**: «60-90 % menos tokens» (RTK) y «11.000 → 2.300 tokens» (skill retrieval) son cifras de los propios repos.
- **No se detecta nada burdamente falso** → no procede anotación contra el canal. Aviso: pieza **patrocinada** con CTA propio.

## Propuesta (nada ejecutado; instalar software nuevo requiere OK explícito)

1. **RTK**: prueba acotada con dos instrumentos (tokens de la salida de un comando del lab antes/después), sin tocar servicios ni n8n.
2. **Skill Retrieval (plugin)**: experimento con métrica propia (tamaño del bloque de skills por turno, antes/después) y vuelta atrás preparada.
3. **Mantis**: evaluar solo si se decide auditar seguridad del código propio; material aprovechable para el FP de ciberseguridad.
4. **Canal AI LABS**: no está en la vigilancia de YouTube del lab (el cron lista 7 canales). Decidir si se añade: cubre Hermes, pero es contenido patrocinado.

## Referencias internas

- `joko-lab/hooks/pre-commit` (3.393 B, gate determinista de recibos) — por qué Delegate Skills no aporta nada nuevo.
- Skills propias: `delegacion-subagentes`, `skill-compaction`, `reddit-reading`, `blocked-page-recovery`, `requesting-code-review`, `ciberseguridad-fp`.
- `tools/opencode-local.sh`; `01-knowledge/references/planning-with-files/` (679 ficheros).
- `research/analisis-miguebaena-agent-reach.md` (veredicto previo de Agent Reach).
- `~/.hermes/skills/.hub/index-cache/` (índice del hub: 88.124 items de skills.sh + clawhub).
- `04-operations/metrics/aplicabilidad_ledger.jsonl` (asiento `yt WJgxX0Eib6k`).
