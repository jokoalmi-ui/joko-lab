<!-- metadatos pre-OKF (conformidad OKF v0.2, 25-sep-2026; frontmatter retirado): type: knowledge · subtype: experiment · status: index · tags: [knowledge, experiment] · created: 2026-07-28 -->
# Experimentos — Joko Lab
# Formato: | EXP ID | Fecha | Tipo | Modelos | Tests | Estado |

| EXP ID | Fecha | Tipo | Modelos | Tests | Estado |
|---|---|---|---|---|---|
| EXP-20260726-001 | 2026-07-26 | Benchmark | 7 modelos | 5 tests c/u | COMPLETADO |
| EXP-20260728-002 | 2026-07-28 | Ciclo manual | Granite 4.1 8B | 5 tests | COMPLETADO |
| EXP-20260728-003 | 2026-07-28 | Embeddings | nomic vs BGE-M3 | 10 queries | COMPLETADO |
| EXP-20260915-006 | 2026-09-15 | Coste | deepseek-v4-flash/pro (reconstruccion) | 5 dias solape + 7 dias baseline | F1 HECHO (NO VALIDADO) |
| EXP-20260916-007 | 2026-09-16 | Multiagente | deepseek-v4-flash (perfil default) | 3 tareas x 2 modos (intercalado) | **F3 EMITIDO: H CONFIRMADA (3/3)** — calidad 100% en ambos modos; coste x4,2 / x5,3 / x16,7 |
| EXP-20261009-008 | 2026-10-09 | Rendimiento (MoE, offload) | qwen3.6-35b-a3b MXFP4 (18,9 GiB) | 11 celdas (E1/E2 x 0/256/512/1024 + control `-ngl 0`), 2 rondas intercaladas | **F3 EMITIDO: H CONFIRMADA** — `--moe-cache-mib 512` sube 5,55→8,54 tok/s (E1) y 7,54→11,88 (E2); C=2048 OOM; ganancia NO depende de la clase de entrada (P2 falsada) |
