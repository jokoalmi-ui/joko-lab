---
title: "Auditoría de modelos del LAB — 19-ago-2026 (tras validar gpt-oss-20b)"
type: research
---

# Auditoría de modelos del LAB — 19-ago-2026 (tras validar gpt-oss-20b)
**VERACIDAD:** [ALCANCE INTERNO]

**Motivo:** petición del usuario tras validar gpt-oss-20b (7/7 batería exigente,
15.3 tok/s, +40% vs R1): "Sustituye quedando R1 como alternativa. Revisa que
otros no cumplen o están duplicados que no merecen tener LAB."
**Método:** inventario real en disco (du -sh), estado en LM Studio API,
fichas en 01-knowledge/models/, veredictos documentados en backlog/GUIA.
**Veracidad:** [VERIFICADO] — salidas reales de terminal (disco, API, fichas).

---

## Inventario real (LM Studio, 70 GB total)

| Modelo | Tamaño | Rol documentado | Estado | ¿Merece LAB? |
|---|---|---|---|---|
| gpt-oss-20b (MXFP4) | 12G | Razonamiento batch | NUEVO, 7/7 | ✅ SÍ — SUSTITUYE a R1 |
| DeepSeek-R1-14B | 8.4G | Razonamiento | activo | ✅ SÍ — queda como ALTERNATIVA |
| GLM-4.6V-Flash | 7.5G | Visión | activo | ✅ SÍ — imprescindible |
| gemma-4-12B-it-QAT | 6.7G | Creatividad | activo | ✅ SÍ |
| granite-4.1-8b | 4.8G | RAG/JSON | activo | ✅ SÍ |
| Dolphin3.0-8B | 4.6G | Chat gabinete | activo | ✅ SÍ |
| granite-4.0-h-tiny | 3.8G | Emergencia memoria | activo | ✅ SÍ (rol nicho GUIA) |
| LFM2.5-2.6B | 1.6G | Tool calling | activo | ✅ SÍ (5º cerebro) |
| bge-m3 | 418M | Embeddings | activo | ✅ SÍ |
| **Qwen3.6-35B-A3B** | **21G** | — | **DESCARTADO** | ❌ **NO — borrar** |

## Ollama (Docker, 12 GB)

| Modelo | Tamaño | Para qué se importó | Estado | ¿Merece LAB? |
|---|---|---|---|---|
| deepseek-r1-distill-qwen-14b | 8G | Delegación (delegation.model) | duplicado | ❌ **NO — duplicado del R1 de LM Studio** (delegación local descartada: num_ctx 8192 vs 64K, 5 intentos 4 zombies) |
| llama31-8b-64k | 4G | Delegación | NO cumple | ❌ **NO — veredicto: NO fiable** (4/5 fallos) + ficha retirada → granite |

## Veredicto de auditoría

### Candidatos a BORRAR (33 GB liberables)

1. **Qwen3.6-35B-A3B (21 GB)** — DESCARTADO con prueba real (10-ago):
   2.7-9 tok/s inutilizable, i5-9500 débil para MoE, razona siempre.
   Ocupa 21 GB sin uso. Re-probar solo con i9-9900K o GPU con más banda.
   Fuente: backlog línea 199 + research/veredicto-qwen-35b-a3b-lab.md.
2. **llama31-8b-64k en Ollama (4 GB)** — NO cumple: falló como modelo de
   delegación (4/5 zombies) + la ficha llama-3.1-instruct-8b está RETIRADA
   (superseded_by granite-4.1-8b). El 64K no existe en disco LM Studio.
3. **deepseek-r1-distill-qwen-14b en Ollama (8 GB)** — DUPLICADO: el R1 de
   LM Studio (misma quant Q4_K_M) queda como alternativa. El de Ollama solo
   servía para delegation.model, y la delegación local se descartó.

### Se quedan (37 GB)
gpt-oss (razonamiento), R1 LM Studio (alternativa), GLM (visión),
gemma-12b (creatividad), granite-4.1 (RAG/JSON), Dolphin (chat),
granite-4.0-tiny (emergencia), LFM (tool calling), bge-m3 (embeddings).

### Matices
- nomic-embed-text-v1.5: aparece en la API pero SIN archivo real en disco
  (solo catálogo) — no ocupa, irrelevante.
- qwen-3.5-9b: ficha `descartado` (no está en disco).
- La sustitución de R1→gpt-oss en el router (llm-router.sh batch/batch-json)
  NO se ha hecho aún — requiere ficha + RULE + context_builder + OKF
  (integración completa, regla del lab: OK explícito del usuario).

## Acción recomendada (pendiente de confirmación)
Borrar los 3 candidatos (33 GB) → comando propuesto a la CLI:
- Qwen 35B: `rm -rf "/mnt/ssd_ia_datos/LM STUDIO/lmstudio-community/Qwen3.6-35B-A3B-GGUF"`
- llama31 ollama: `docker exec ollama ollama rm llama31-8b-64k`
- R1 ollama: `docker exec ollama ollama rm deepseek-r1-distill-qwen-14b`
(⚠️ SOLO tras confirmación explícita del usuario + verificar que el R1 de
LM Studio carga OK antes de borrar el de Ollama — no dejar el lab sin R1.)
