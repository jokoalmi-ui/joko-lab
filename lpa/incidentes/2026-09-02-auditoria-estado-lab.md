---
type: lpa
subtype: incident
status: closed
tags: [lpa, incident, auditoria]
created: 2026-09-02
---
# INC-006: Auditoría de estado del lab (02-09-2026) — componentes desconectados/desfasados

**ID:** INC-006
**Fecha:** 2026-09-02
**Estado:** CERRADO (hallazgo B pendiente de decisión)
**Origen:** Sesión de mantenimiento 02-09 — el usuario pidió revisar punto por punto TODOS los componentes del lab tras encontrar "demasiados casos" de cosas desconectadas/desfasadas.

---

## Qué se auditó (14 bloques, todo con salida real)

1. Sistema base (fecha/uptime/RAM/swap/GPU/discos/procesos) — SANO
2. Stack Docker (compose ps, daemon, contenedores, puertos) — SANO (4/4 UP, solo loopback)
3. APIs locales (LM Studio/Ollama/monitor/proxy) — SANAS (bug cosmético del monitor)
4. Servicios systemd/user (gateway, proxy, indexer, reranker, monitor, timer) — SANOS
5. Backups (GDrive, logs, retención) — SANOS (bundles OK, retención 3 copias, 41G)
6. Crons Hermes (estado en disco) — SANOS (errores del 31-ago = arranque, pitfall conocido)
7. knowledge_health — ROTO (ver hallazgo 4)
8. Memoria Hermes + errors.log 48h — DIVERGENTE (hallazgos 6 y 8)
9. MCP servers (3) — SANOS (responden; lancedb 22.590 filas)
10. Kanban — SANO (11 tareas done en 2 pilotos; la jerarquía funcionó)
11. detectar-sin-uso — 65 ítems de higiene (skills sin uso, research huérfana, .bak)
12. Docs con estado (SVP) — ROTO (pendientes.txt caducado; ver hallazgo 3)
13. Git hermes-lab — DIVERGENTE (hallazgo 5)
14. Suite de tests — SANO (254 tests; 1 error = runner equivocado, no código)

## Hallazgos y acciones

1. joko-backup.service fallaba desde el 20-08 sin aviso → ARREGLADO el 02-09 (ver D1 de revision-fallos-2026-09-01.md); validación end-to-end con el timer del 03-09 00:26.
2. Doc de revisión afirmó kanban vacío cuando ya se usaba → CORREGIDO (B2) en revision-fallos-2026-09-01.md.
3. pendientes.txt (fuente canónica) caducado (cabecera 06-08; v0.21.0 "sin salir" cuando ya estaba ejecutada) → ACTUALIZADO y commiteado (3a62942).
4. KNOWLEDGE HEALTH 0/100 por bug de clasificación: 24 observaciones de telemetría (OBS-*-decisiones-por-politica) clasificadas como DEC por la subcadena "decision" en _clasificar_por_nombre → FIX en tools/knowledge_health.py (backup .bak-20260902-obscls); health 0→100/100; DEC 29→5 (reales), OBS 51→75. Hallazgo anejo: Evidence Contract 0/23 sobre los KOs reales (todos con reviews=0 y falsacion=0) — PENDIENTE DE DECISIÓN (re-verificar / legacy / deuda conocida).
5. pipeline_proxy.py +2 líneas (cache tokens) sin commitear desde el 01-09 → COMMITEADO (5275227) con recibo RDD; entrará en el bundle 22:35 y push del timer 00:26.
6. Memoria Hermes al 99% (MEMORY/USER) + escritura batch fallida 09:46 (entrada inexistente, carrera entre sesiones) → **RESUELTO 02-09: poda verificada** (MEMORY 91%, USER 94%; datos quitados viven en sus skills: BBK/HAZILAN → ciberseguridad-fp + empleo-emprendimiento-bizkaia; serie LinkedIn → linkedin-carrusel-lab; recursos-gratuitos → skill propia).
7. web.extract_backend vacío → auto-detección ddgs (solo búsqueda); falló en sesión real 11:32 → **RESUELTO 02-09: `hermes config set web.extract_backend exa`** (ring keyless sin API key; backup config.yaml.bak-20260902-webext). Verificado: web_extract extrae example.com y docs.n8n.io/llms.txt sin error. Search sigue con ddgs (per-capability).
8. errors.log con avisos ignorados (sanitizer, curator, extract, Telegram sticky path 12:34) → revisado; sin impacto permanente (la referencia n8n SÍ se guardó pese a los warnings — verificado en disco).
9. Bug cosmético: /api/health del monitor devuelve docstring de psutil como python_version → PENDIENTE (P2).
10. detectar-sin-uso: 20 skills "nunca usadas" (verificar falsos positivos de crons), 33 research sin referencia, 6 .bak huérfanos, tar.gz 29d → PENDIENTE (P2, archivar no borrar).
11. 8 skills de 80-102 KB → PENDIENTE (P2, skill-compaction).
12. Suite de tests sin runner canónico documentado (pytest no instalado; unittest con ~/.venv/hermes-rag) → PENDIENTE (P2).

## Patrón promovido

CP-008 "Estado real ≠ estado documentado" → incubator (8 ocurrencias el mismo día + 4 correcciones previas del backlog).

## Decisiones pendientes

- (A) Evidence Contract 0/23 → **RESUELTO 02-09 (decisión usuario: legacy + fix + nota)**: los 23 KOs existentes se declaran LEGACY (contrato = gate de promoción para KOs NUEVOS; no re-verificación retroactiva — anti-histórico). Deuda conocida desde 31-07 (documentada en el propio contrato) e informativa (no penaliza el health). Fix del verificador: evidence_contract.py crasheaba con tipos fuera del contrato (PRED-001: KeyError 'status'/'actual') → arreglado (backup .bak-20260902-pred); salida con nota legacy y sin crash (EXIT=0, verificado). Contrato actualizado con la decisión (punto 6).
- (B) Podar MEMORY.md/USER.md → **RESUELTO** (ver hallazgo 6).
- (C) Backend de extracción web → **RESUELTO** (ver hallazgo 7: exa keyless).
- (D) P2 higiene → **PARCIALMENTE RESUELTO 02-09**: (1) bug cosmético del monitor FIXED (python_version era `psutil.__doc__...` → `platform.python_version()`; backup app.py.bak-20260902-pyver; servicio reiniciado y verificado en caliente: "3.14.4"); (2) runner de tests documentado/verificado: 259 tests OK con `~/.venv/hermes-rag/bin/python3 -m unittest discover tests` (el python del sistema NO vale: lancedb ausente); (3) research huérfana: 33 archivos archivados en research/.archive-20260902/ (+6 .bak) — detector 67→34, 0 .bak huérfanos; (4) skills nunca usadas: desinstaladas 3 (box, meeting-action-items, weekly-review-planning); 8 conservadas por decisión del usuario (docx, xlsx, pdf, github, email-inbox-triage, document-to-action-items, product-price-monitor, competitor-news-monitor). PENDIENTE para el ciclo LPA: compactar 8 skills gigantes (80-102 KB; piloto propuesto: lm-studio); frontmatter 69% (clasificar qué docs lo requieren o ajustar umbral del watchdog); consolidar 4 skills de clima duplicadas (datos-clima/datos-climaticos/datos-climaticos-historicos/informes-clima) → 1; bug menor del detector detectar-sin-uso.py (lista residuos del usage.json sin cruzar con disco — p.ej. restaurantes-euskadi no existe como skill).
- (E) Antídoto del patrón CP-008: watchdog periódico del estado → **RESUELTO 02-09 (evaluado y ejecutado)**: el watchdog correcto YA existía (lab-health-watchdog.sh, diario 08:30, job 40721dd223cc) pero tenía defectos que lo hacían ruido: falso positivo de git-backup (log con --quiet, 14 días "sin ejecución" cuando el bundle subía), grep de errores contando ruido/protecciones (153 "errores" de los que ~45 eran el curator guard), y NO miraba el score de knowledge_health (el 0/100 pasó sin aviso), ni repo sucio, ni servicios failed. Reparado (backup .bak-20260902-fixes): git-backup verifica el bare local (/mnt/ssd_ia_datos/hermes-lab.git — push secuencial del mismo unit), whitelist de errores reales (BadRequest/Traceback/Streaming failed/Network Retry/memory) con umbral >3, score KH <80 → aviso, check repo hermes-lab sin commitear (excluye .bak), check systemctl is-failed joko-backup.service. Verificado manualmente. Se eliminó además el cron duplicado del ciclo LPA (96e7474e1fe7; se conserva 05de86a93257 con skill lpa — dos sesiones crearon el mismo D0). Pendiente heredado: frontmatter 69% (aviso legítimo del watchdog; higiene documental P2).
