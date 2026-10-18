---
title: "Mapa de Capacidades del LAB — Joko Lab (24-ago-2026)"
type: research
---

# Mapa de Capacidades del LAB — Joko Lab (24-ago-2026)
**VERACIDAD:** [ALCANCE INTERNO]

**Propósito**: plano central de TODO lo que el lab puede hacer hoy. Consultar antes de valorar cualquier "novedad" externa: si el mapa ya lo cubre, es validación; si no, es futurible.

## ⚡ Números del sistema (verificados 24-ago; re-verificados 17-sep-2026 19:53)

| Recurso | Cantidad |
|---|---|
| Skills Hermes | **203** (SKILL.md en disco; 28 categorías según 24-ago) |
| Research documentados | **358** |
| Tools Python (joko-lab/tools) | **96** .py + **22** .sh |
| Crons (crontab) | **10** + **43** crons Hermes (**41** activos) |
| MCPs activos | **3** (animation-server, lab-db, lancedb) · sin cambio |
| RAG LanceDB | **43.951 fragmentos** · 4,9 GB · recall@5 = 100% |
| Docker stack | **4/4 Up** (n8n, ollama, pdf-cleaner, stirling-pdf) · sin cambio |
| Modelos locales | **14** en la API de LM Studio (:1234) · lista del 24-ago: GLM-4.6V visión, gpt-oss-20b, LFM ×2, deepseek-r1-14b, gemma-4-12b, granite ×2, embeddings ×2 |

Cifras del 24-ago, para comparar: skills 164 · research 317 · tools 80 · crons 33 Hermes · RAG 21.975 · modelos 10.
Medido con salidas reales: `find | wc -l` (skills), `crontab -l` + `jobs.json`, `docker compose ps`, `/api/v0/models`, MCP `info_rag`, `du -sh`.

---

## 🏗️ DOMINIO 1 — INFRAESTRUCTURA LOCAL (0 €/mes)

| Capacidad | Herramienta real | Estado |
|---|---|---|
| LLM razonamiento | gpt-oss-20b (LM Studio) | ✅ Producción |
| LLM visión | GLM-4.6V-flash | ✅ Producción (swap validado) |
| Modelos alternativos | LFM 2.6B/3B, deepseek-r1-14b, gemma-4-12b, granite | ✅ Disponibles |
| Imágenes IA | ComfyUI + SDXL (GPU A2000) | ✅ Validado (~30s) |
| OCR/PDF | Stirling-PDF + pdf-cleaner (Docker) | ✅ Producción |
| Monitor GPU/RAM | lmstudio_real_monitor (Flask :5000) | ✅ |
| Felicitaciones/tarjetas | ComfyUI fondo + HTML + Chrome render + GLM verificación | ✅ Pipeline validado 24-ago |

## 🔍 DOMINIO 2 — DATOS PÚBLICOS SIN PAGAR APIs (el "Agent-Reach" del lab)

| Plataforma | Herramienta | Coste |
|---|---|---|
| YouTube | yt-dlp (subtítulos ES/EN, dedup) | 0 € |
| Instagram | browser + pipelina (cookies, img_index) | 0 € |
| X/Twitter | skill xurl (CLI oficial) | 0 € |
| GitHub | gh CLI + skills github-* | 0 € |
| Web general | web_search + browser | 0 € |
| **LinkedIn** | ⚠️ Solo manual | — (futurible: Agent-Reach, con riesgo ToS) |

**Pipelinas validadas**: YouTube ×9+ · IG ×6+ · carruseles (extraer TODAS las imágenes o caption completo) · subtítulos (ES 429 → EN fallback).

## 🧠 DOMINIO 3 — RAG Y CONOCIMIENTO

| Capacidad | Herramienta | Dato real |
|---|---|---|
| Índice vectorial | LanceDB `joko_notes` | 21.975 fragmentos |
| Búsqueda híbrida | FTS + vectorial (RRF) | ✅ |
| Reranking | reranker daemon :8765 (CPU) | ✅ 0 VRAM |
| Evaluación | `evaluar_rag.py` | **recall@5 = 100%** (73-86 ms) |
| Adversarial | `evaluar_rag_adversarial.py` | 0/6 + 0/4 + 0/3 ✅ |
| Multimodal | CLIP ViT-B/32 (tabla joko_images) | ✅ |
| Query+Summary | joko_summaries + joko_queries | ✅ (20-ago) |
| Contexto | context_builder + knowledge_resolver | TTL 300s |
| Compactación | optimize() + cleanup | 26 GB → 320 MB (98.8%) |
| MCP acceso | `lancedb` MCP (buscar_rag, info_rag) | ✅ |

## 💰 DOMINIO 4 — AHORRO DE COSTES (palanca #1)

| Técnica | Implementación | Dato real |
|---|---|---|
| Routing cloud/local | `llvm-router.sh` | gpt-oss local tras 12:00 (0 €) |
| Context pruning | Cron pruning 0.4 | **-32,1%** (314K → 213K tok/consulta) |
| Cache | context_builder TTL 300s + sidecars | ✅ |
| LLM-as-judge | `llm_as_judge.py --juez` | etiqueta CALIDAD |
| Evaluación modelos | Batería 5x5 real + juicio ciego CLI | ✅ |
| Modelo correcto/tarea | gpt-oss razonamiento · deepseek-r1 grounding · GLM visión | ✅ |

## 🤖 DOMINIO 5 — AUTOMATIZACIÓN

| Capacidad | Implementación |
|---|---|
| Crons Hermes | 33 (cron.json): recordatorios, watchdogs, telemetría, precios, scans |
| Crons sistema | 9 (crontab) |
| MCPs | animation-server (manim), lab-db (SQLite), lancedb (RAG) |
| n8n Docker | Envío WhatsApp (ENVIO WHATSAPP) — zona protegida |
| Notificaciones | Telegram (canal -1003968087263) |
| Watchdogs | GPU suspend/resume, salud sistema, telemetría 22:00 |

## 🏠 DOMINIO 6 — SISTEMAS PERSONALES

| Sistema | BD | Estado |
|---|---|---|
| perfume-ia | coleccion.db + futuribles.db | 352+ perfumes, uso diario, ficha v4 |
| café-ia | cafes.db | Catálogo cafés especialidad |
| finanzas | Baskepensiones 14.097 € | Seguimiento |
| biohacking | ~/proyectos/biohacking-cerebral | Pruebas + protocolos |
| bolsa (Skool) | Experimento 002 | MRVL 27-ago |
| Obsidian | /mnt/ssd_ia_datos/obsidian-vault | Unificado PC+móvil |

## 💼 DOMINIO 7 — EMPLEO Y NEGOCIO

| Recurso | Estado |
|---|---|
| Skill recursos-gratuitos-desempleados v2.0 | 22 recursos verificados (5 categorías) |
| LinkedIn Lab | Marca personal (contenido educativo IA) |
| TFM | En marcha (antes de octubre) |
| HAZILAN+ | 21/09 |
| BBK Bootcamps | Ciberseguridad 05/10-04/02/27 |
| Especialidad n8n Founderz | Señal: al empezar → buscador de precios + checklist 45 capítulos |

## 🚀 FUTURIBLES ANOTADOS (con señales, NO hacer sin señal)

| Futurible | Señal |
|---|---|
| Buscador de precios perfumes (Python+n8n) | Al empezar especialidad n8n |
| ~~Skill create-mcp-lab.sh~~ ✅ IMPLEMENTADO 25-ago (tools/create-mcp-lab.sh, validado punta a punta) | — |
| Mini-auditoría IA PYMES | Cuando tú decidas (tras TFM) |
| Rank & rent PYMES | Tras TFM/empleo |
| Marketplace skills | LinkedIn Lab con audiencia |
| Metadata filtering RAG | Indexar docs versionados o caso real |
| MCP n8n→Hermes | Crear workflows n8n con frecuencia |
| F6 Qwen 27B | GPU 24 GB |
| LFM QAD residente | Tarea recurrente ligera |
| Checklist n8n 45 capítulos | Especialidad n8n |
| Agent-Reach (LinkedIn/IG) | Necesidad estable + aceptar riesgo ToS |
| **Panel único del LAB** — HTML/SVG con la vista gráfica del sistema, regenerado sin tokens y con botones que ENCOLAN en kanban (no ejecutan) | **TFM en marcha** (el mapa entero es su caso de estudio) o levantar el Architecture Freeze. Origen: panel de control descrito por Marcos Emowe (`ejDH5-Q9bu4`). Precedentes en el lab: `lmstudio_real_monitor` (Flask :5000, una sola pieza), `tfm/slides/03-mapa-lab.html` (SVG estático, 0 script), `tools/mapa_conocimiento.py` |
| **Insights de Instagram via API oficial** (cuenta profesional + app Meta + token): medir alcance/interaccion, ordenar los DMs, publicar con aprobacion. Origen: post `DeSAWqzjCdI` (ia.university, 09-oct-2026; 3 puertas + 4 flujos) | **Señal:** querer MEDIR el rendimiento de IG (alcance/interaccion) en vez de solo listar publicaciones, y aceptar que los DMs de terceros pasen por un MCP remoto (nube). Hoy la vigilancia navega SIN sesion -> 0 metricas |

## 🔑 CÓMO USAR ESTE MAPA

1. **Llega una "novedad"** → consultar el dominio correspondiente → si ya está → **es validación** (no acción)
2. **Toca algo nuevo** → comprobar si existe skill/tool/research → si no → **futurible con señal**
3. **TFM/LinkedIn** → el mapa entero es el caso de estudio del lab
4. **Regla anti-duplicado**: buscar en research/ (317) ANTES de analizar algo ya cubierto

## Estado del mapa

- Verificado: 24-ago-2026 (salidas reales del sistema)
- Actualizar: cuando cambie un número (skills/research/RAG) o se añada un dominio
- Re-verificado: 17-sep-2026 19:53:15 CEST — 203 skills (eran 164) · 358 research (317) · 96 tools .py (80) · 43 crons Hermes/41 activos (33) · RAG 43.951 fragmentos (21.975: más que duplicado) · 14 modelos en API (10). MCPs 3 y Docker 4/4 sin cambio.
- Futurible añadido 17-sep-2026: **Panel único del LAB**, señal = TFM o levantar el freeze. No se implementa sin señal.
- Nota: el nombre del fichero conserva la fecha `20260824` aunque el contenido esté re-verificado (renombrar exige `mv`, fuera de esta escritura).
- Registro de escritura: 6.238 B antes (md5 `b7e66c7cadce69048d3301d646631b94`) · este bloque se añadió después de una copia `.bak-20260917-futurible-panel`. Esta línea no puede contener el tamaño del fichero que la contiene: la cifra posterior se mide tras pasar el validador y va al backlog del 17-sep.
