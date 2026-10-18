---
title: "Análisis — atareao/graphrag (GraphRAG en Rust: grafo + vectores sobre notas Markdown), 21-sep-2026"
type: research
---

# Análisis — atareao/graphrag (GraphRAG en Rust sobre notas Markdown)

**VERACIDAD:** [VERIFICADO]
**Fuente:** hallazgo colateral del vídeo atareao 833 «Workflows de IA, automatiza tu día con Ollama y Docker» (21-sep-2026, 1.823 s) → repo https://github.com/atareao/graphrag
**Consulta:** 2026-09-21 21:41:16 CEST
**Método:** GitHub API (repo + readme), crates.io API (crate + owners), README íntegro (418 líneas), ficha de la tag del modelo NER en ollama.com, entorno del lab (cargo/rustc/nvim) y corpus real en disco. Sin instalar, sin ejecutar, sin descargar modelos. Nada escrito fuera de este fichero.

## 1. Qué es (según su propio README)

Motor de **búsqueda híbrida sobre notas Markdown**: extrae entidades con un LLM local
(Ollama), construye un grafo de conocimiento en SQLite y responde combinando
**similitud vectorial + expansión por grafo**. **Un solo binario Rust (~6,5 MB)**, sin
Python ni npm, SQLite embebido (bundled). Declara **32 tests (30 sin Ollama)**.

Comandos: `init db|neovim`, `seed`, `build`, `reset`, `search`, `fts` (FTS5), `graph`
(vecinos de un nodo), `path` (camino más corto), `stats`, `completions`, `mcp`.
Config en `~/.config/graphrag/config.toml` (`embed_model = bge-m3:latest`,
`ner_model = gemma4:e2b`, `k`, `depth = 2`, `alpha = 0.7`, `num_threads = 4`).

`build`: pre-scan por **SHA256** → solo ficheros nuevos/modificados → chunking de
Markdown con frontmatter → **NER en lote (1 llamada por fichero)** → N hilos + 1 hilo
escritor (SQLite serializado) → poda de notas borradas → repoblado de FTS5.
`search`: 3 fases — coseno sobre embeddings → rerank por título/tipo → expansión por
CTE recursivo. Trae **servidor MCP por stdio** con 7 tools (`build`, `search`, `fts`,
`graph`, `path`, `stats`, `seed`) y 5 resources (`graphrag://stats|nodes|notes|entities|edges`).

## 2. Discriminantes verificados (2026-09-21 21:41:16 CEST)

- **GitHub `atareao/graphrag`**: **0 ★**, 0 forks, 0 issues, 97 KB, sin descripción ni
  topics. **`created_at` 2026-08-30T16:27:49Z → `pushed_at` 2026-08-30T16:34:09Z**: el
  repo se creó y se subió en **~7 minutos y no se ha vuelto a tocar** (22 días).
  `license: None` → la API **no detecta fichero LICENSE** en el repo, aunque el README
  lleve badge MIT y sección «License: MIT».
- **crates.io `graphrag`**: v0.2.0 publicada el **2026-05-31** (v0.1.1 el 18-mar-2026),
  **77 descargas totales**. `owners: automataIA (carcall)` · `repository:
  github.com/automataIA/graphrag-rs` · descripción «meta-crate that bundles
  graphrag-core and graphrag-cli».
- **`automataIA/graphrag-rs`** (el dueño real del nombre en crates.io): **527 ★**, MIT,
  creado 2025-09-21, `pushed_at` 2026-06-02, «high-performance, state-of-the-art Rust
  implementation of GraphRAG». Su README (38.544 chars) **no menciona MCP, FTS5,
  bge-m3 ni subcomandos al estilo del de atareao** → no hay parentesco de código evidente:
  son **dos implementaciones distintas con el mismo nombre**.
- **Modelo NER**: la tag `gemma4:e2b` **existe** en ollama.com/library/gemma4 (50 tags
  publicadas: e2b, e4b, 12b, 26b, 31b y variantes). La ficha de la tag declara **7,2 GB** (leído de ollama.com/library/gemma4:e2b), NO los 5 GB
  El README de atareao le atribuye **5,1B / ~5 GB** -- un 44% menos -- → cifra del autor, [NO CONTRASTADA].
- **Entorno del lab**: `cargo 1.93.1` y `rustc 1.93.1` **instalados** (compilar sería
  viable). **`nvim` NO está instalado** → el plugin de Neovim no aplica aquí; sí el CLI y el MCP.

## 3. Hallazgo 1 — el `cargo install graphrag` del README NO instala este programa

El README abre con `cargo install graphrag` + badge `shields.io/crates/v/graphrag`, pero
**ese crate es de otro autor** (owners `automataIA/carcall`, repo `automataIA/graphrag-rs`).
Instalar siguiendo su documentación trae **otro proyecto** (el de 527★), no el suyo.
No verificado el motivo (hipótesis no comprobada: el nombre del crate estaba ocupado y
solo publicó el repo; declarado como **inferencia**, no como hecho).

## 4. Hallazgo 2 — el coste sobre el corpus del LAB lo dice su propio README

El README declara **~0,08 ficheros/s** con `gemma4:e2b` y 4 hilos (≈**22 h para 6.254
ficheros** en la primera construcción; después es incremental).

Corpus real medido hoy: **`joko-lab` = 4.475 ficheros `.md` (14 GB)** —
`01-knowledge` 3.089 · `04-operations` 460 · `research` 430. A la tasa declarada:
**~15,5 h de primera construcción** (sin contar el vault de notas), con **1 llamada de NER
por fichero** a un modelo local. La cifra 0,08 fich/s es **del autor**, no medida aquí
([NO CONTRASTADA]); lo medido es el tamaño del corpus.

Y el lab **ya tiene la mitad vectorial**: LanceDB `joko_notes` en
`/home/jokoalmi/joko-lab/.lancedb` → **44.531 filas** (id, path, title, tags, type,
status, text, vector). Lo que graphrag añadiría es el **grafo de entidades**, la
expansión por vecinos, `path` y FTS5.

## 5. 🔴 Conexión con el LAB

| Aspecto | Veredicto |
|---|---|
| GraphRAG como implementación | ⚪ **Ya evaluado y descartado** en el lab: `analisis-atsmatrix-graph-extraction-cost.md` cita 2 análisis previos (graph-engineering 05-ago, agent-graph-engineering 10-ago) y concluye **«NO implementar»**. Esta ficha **no revierte esa decisión** |
| Motivos del descarte | Siguen vigentes: coste de extracción/reindexado y **entity resolution** — `analisis-graph-engineering-20260819.md` (GraphRAG-Bench, arXiv 2506.05690): gana en multi-hop (**53,4% vs 42,9%**) y síntesis corpus-wide, **pierde en lookups simples y alto volumen con coste de índice**; con 85% de precisión por hop, 5 hops = **44% fiable** |
| Búsqueda vectorial del lab | ✅ Ya cubierta: LanceDB 44.531 filas + MCP `lancedb` + `agentic-rag`. El grafo no sustituye esto |
| Formato de entrega | 🟡 **Lo único con valor real**: **un binario Rust único (~6,5 MB) con servidor MCP propio**, pensado para máquinas sin GPU. Encaja con `despliegue-ia-local-clientes` (el lab entrega Python/cgroups). El repo de atareao es demo (0★, 22 días parado); el proyecto vivo del mismo nombre es **`graphrag-rs` (527★, MIT)** |
| Rust en el lab | ✅ `cargo 1.93.1` disponible → compilar/probar sería posible sin instalar toolchain |
| Coste de probarlo | Bajo en dinero (todo local), **alto en tiempo de GPU**: la primera indexación de 4.475 notas a la tasa declarada son ~15 h; la GPU del lab (12 GB) tendría que ceder LM Studio/Ollama durante ese tiempo |

## 6. No verificado / inferido

- **[NO CONTRASTADO]** todas las cifras de rendimiento del README (0,08 fich/s, 22 h,
  ~6,5 MB, 32 tests): son del autor, no reproducidas aquí. No se ha instalado ni ejecutado nada.
- **[NO VERIFICADO]** el tamaño real de `gemma4:e2b` y si el NER produce buenos grafos en
  español (el repo no publica ninguna evaluación de calidad, ni recall/precision).
- **[INFERIDO]** el motivo del `cargo install` apuntando a un crate ajeno.
- **[NO VERIFICADO]** que el binario del repo de atareao compile hoy (no se probó).

## 7. Veredicto

**INFORMATIVO / NO ACCIONABLE AHORA.** El repo de atareao (0★, 7 minutos de vida, 22 días
sin tocar, README con `cargo install` que apunta al crate de otra gente) **no es una
herramienta que el lab deba adoptar**; no cambia los dos motivos por los que el lab ya
descartó GraphRAG (coste de extracción + entity resolution baja a varios hops). Lo
aprovechable es el **patrón de empaquetado** (binario único Rust + MCP por stdio) para
entrega a clientes, y como **referencia viva** el proyecto del mismo nombre con 527★.

**Referencias futuras con señal de activación:**
1. **`automataIA/graphrag-rs`** (527★, MIT, activo hasta jun-2026) — mirar **solo si** el
   lab decide algún día añadir grafo a sus notas. Antes habría que re-medir: coste de
   indexación sobre 44.531 chunks y precisión de extracción en español.
2. **Patrón «binario Rust + MCP por stdio»** — aplicar **cuando** haya que desplegar algo
   en un cliente con hardware mínimo (sin Python, sin GPU).
3. **`gemma4:e2b`** como modelo de extracción de entidades — candidato **si** se retoma
   el eje grafo; requiere medir VRAM real en la A2000 antes de nada.

## 8. Estado del lab

- **Nada tocado**: no se instaló, compiló, descargó ni ejecutó nada. Solo lectura.
- **Este fichero** es la única escritura, autorizada por el usuario («2») el 21-sep-2026.
- No hay backup previo posible (fichero nuevo). No se tocó el backlog (congelado por la
  dieta IG hasta 03/04-oct).
