# Investigación semanal de modelos locales — 2026-09-21

Cron `investigacion-modelos-locales-semanal` (v2). Hardware objetivo: **RTX A2000 12 GB VRAM**, contexto de referencia 8K.
Regla v2: este informe **no re-lista** candidatos ya registrados. Memoria = `candidatos-modelos-locales.json`.

## PASO 0 — memoria consultada (antes de cualquier veredicto)

- `04-operations/metrics/modelos-locales/candidatos-modelos-locales.json` — 25 entradas antes de esta pasada (EN_USO / PENDIENTE / OBSERVAR / DESCARTADO).
- `01-knowledge/modelos_por_tarea.yaml` — roles asignados (veracidad_critica, vision, redaccion, grounding, razonamiento, tool_calling, json, chat_rapido, ligero_masivo).
- `04-operations/metrics/alucinaciones_ledger.jsonl` — mediciones reales del lab.
- Búsqueda de cada nombre nuevo en `01-knowledge/experiments/` y `01-knowledge/objects/`: `(?i)(minicpm|needle|edge0|neohorse|bonsai|xing4|ternary|empero)` → **0 coincidencias en 01-knowledge** (ninguno de los nombres de esta semana tiene EXP ni RULE).
- Evidencia previa del lab ya existente y aplicada (JL-006):
  - `research/analisis-nichonauta-bonsai2-27b-2026-09-19.md`
  - `research/analisis-nichonauta-neohorse-1-4b-2026-09-19.md`
- `date` → 2026-09-21 14:04 CEST. Backup previo a escribir: `candidatos-modelos-locales.json.bak-2026-09-21`.

## Novedades reales de la semana (7 días)

| Candidato | GGUF | VRAM (8K) | tok/s A2000 | Veredicto |
|---|---|---|---|---|
| **MiniCPM5-2B** (OpenBMB, 07-sep, Apache 2.0) | Q4_K_M 1,6 GB (Ollama oficial) | ~2,5-3 GB (estimación propia) | no publicado | **PROBAR** |
| **Maple-Preview-20B-A1B** (DeepGrove, MIT) | TQ1_0/TQ2_0 4,64-5,91 GiB | 7,3 GB medidos por terceros (16 GB, fork) | no publicado | **OBSERVAR** |
| **Ternary-Bonsai-2-27B** (Prism ML, 17-sep) | PQ2_0 5,9 GB (+0,63 GB visión) | cabe en 12 GB | no publicado en A2000; 42 tok/s medidos en RTX 3060 12 GB | **OBSERVAR** |
| **NeoHorse-1-9B** (TokenRhythm, 05-sep, Apache 2.0) | Q4_K_M 5,63 GB (oficial) | ~6,5-7 GB | no publicado | **OBSERVAR** |

Diálogo de decisiones:

- **MiniCPM5-2B → PROBAR.** Es la única novedad con evidencia externa independiente (Artificial Analysis Intelligence Index v4.2: 15 según eWeek, 23 según tuit de OpenBMB → **discrepancia sin resolver**), GGUF oficial y soporte en Ollama/LM Studio/llama.cpp sin fork. Motivo de cola: el rol `tool_calling` del lab (`lfm2.5-2.6b`, EN_USO) **no tiene medición propia en el ledger**; este es el tramo 2B con mejor respaldo. Probar con `tools/evaluar_json_tool_calling.py` + banco de validación del juez, no con benchmarks de razonamiento. Cifras del vendor (media 53,9 en 34 pruebas, BFCL v4 66,6, SWE-bench Verified 46,4, τ²-Bench Telecom 97,1) = auto-reportadas.
- **Maple-Preview-20B-A1B → OBSERVAR.** Publicado el 05-ago (fuera de la ventana de 2 semanas); entra por **cambio material**: llama.cpp v0.4.1 (14-sep) añade la arquitectura `maple` (implementación **CPU** en mainline). El formato ternario `tq2_0` del fork `stamsam/llama.cpp` (rama `prism`) **no es interoperable con mainline** y los kernels CUDA viven en el fork → no carga en LM Studio/Ollama. Mediciones de terceros con ese fork: 7,3 GB de VRAM a 8K con 4 slots y 361,8 tok/s tg128 en una GPU de 16 GB (Windows + CUDA). Model card: puede rendir por debajo en benchmarks agénticos.
- **Ternary-Bonsai-2-27B → OBSERVAR, sin acción.** El lab ya lo analizó el 19-sep: cabe y funciona (42 tok/s, ~40 min por tarea de landing en una RTX 3060 12 GB), pero requiere fork de llama.cpp, NO es compatible con Ollama y el propio autor del test real rechaza el «98,2%» del vendor. No sustituye a `gpt-oss-20b` ni a `qwen3.6-35b-a3b`.
- **NeoHorse-1-9B → OBSERVAR, sin cola.** GGUF oficial con Q4_K_M 5,63 GB y carga vía LM Studio (`lms get tokenrhythm/neohorse-1-9b-gguf`). Las cifras del vendor (macro 69,04 vs 65,60 de Qwen3.5-9B; BFCL v4 67,43 frente a 52,06 de granite-4.2-8B) **no tienen reproducción de terceros** y el hermano NeoHorse-1-4B, con la misma receta, fue desmentido en prueba real (lab, 19-sep). No entra en cola.

## Descartes de esta pasada (registrados para no volver a listarlos)

| Candidato | Motivo |
|---|---|
| **Xing4.0-29B-A4B** (China Telecom) | GGUF IQ4_NL 20,1 GB en 3 shards (la card dice ~18 GB); repack Q4_K_M 17,6 GB. No cabe. |
| **Qwen3.8-35B-A3B-Distill-GGUF** (empero-ai) | Cuantización mínima IQ2_M 12,558 GB (orientada a 16 GB); Q6_K 29,2 GB. No cabe. |
| **Needle / Cactus (familia)** | Sin GGUF: binario `.cact` de 14 MB y motor propio; objetivo microcontrolador. No carga en LM Studio/Ollama. |
| **Edge0-35B-A3B-preview** | Requiere framework propio (backend MLX = Apple) y streaming de expertos desde SSD; el lab ya descartó `kimi-cat3` por disco lento. |
| **Muse-Glimmer-30B** (Meta, Apache 2.0) | 4-bit 17 GB, 2-bit 12-14 GB. No cabe en 12 GB. |

## Sin verificar / pendiente de contraste

- Infra: el weekly del 21-sep menciona un motor de aceleración para Qwen3.8 («Splash Engine») publicado por LM Studio. **No verificado** fuera de esa fuente ni en el changelog de LM Studio. Relevante solo si se retoma el pendiente `Qwen3.8-27B-GSQ-RCO`.
- `Tencent Hy 4 (hy_v4)` aparece como arquitectura preview añadida en llama.cpp (04-14 sep) **sin datos de tamaño publicados en esta pasada** → no se registra (no se inventan tamaños).

## Pendientes heredados

- **PENDIENTE: 2** + 1 nuevo (`MiniCPM5-2B`) → el más viejo sigue siendo `Ministral-3-14B-Instruct` (primera aparición 24-ago-2026, **28 días**, 4 semanas sin ejecutar).
- Segundo pendiente: `Qwen3.8-27B-GSQ-RCO` (07-sep, 2 semanas sin ejecutar).
- OBSERVAR heredados sin cambio: `Mellum2-12B-A2.5B` (24-ago), `Ornith-1.5-9B` (07-sep), `LFM2.5-8B-A1B` (07-sep).

## Estado del registro

- `candidatos-modelos-locales.json`: 25 → **34 entradas** (9 nuevas), `actualizado: 2026-09-21`. Ninguna entrada borrada (verificado por diff contra el backup).
- Backup: `candidatos-modelos-locales.json.bak-2026-09-21`.

**No se ha descargado ni cargado ningún modelo. Nada se descarga ni se prueba sin OK explícito del usuario.**
