# Lista definitiva de borrado de modelos — LM Studio (01-oct-2026)

Fuente de tamaños: `lms ls` (no `du`). Estado medido el **01-oct-2026 20:16 CEST**: `lms ps` → "No models are currently loaded."
Store actual: **14 modelos / 104,22 GB** (`lms ls`). Raíz de modelos: `/mnt/ssd_ia_datos/LM STUDIO/<publisher>/<repo>/`.
Disco del store (`df -h /mnt/ssd_ia_datos`, `/dev/sdb1`, mismo SSD que los datos de n8n; medido el 02-oct-2026 09:19 CEST): 440 G totales · 335 G usados · **83 G libres (81 % de uso)** → el borrado dejaría ~111 G libres.

## LISTA DEFINITIVA — borrar 2 modelos (28,38 GB, 27,2 % del store)

| # | id exacto en LM Studio | Tamaño | Carpeta en disco | Por qué se borra | Qué se pierde |
|---|---|---|---|---|---|
| 1 | `qwen3.6-35b-a3b-mtp` | 22,66 GB | `/mnt/ssd_ia_datos/LM STUDIO/unsloth/Qwen3.6-35B-A3B-MTP-GGUF` | 0 consumidores en código (solo 2 scripts de MEDICIÓN). Duplica a `qwen3.6-35b-a3b_moe` (mismo 35B, otra cuantización) que sí tiene evidencia. 8,3 vs 7,0 tok/s = diferencia irrelevante. | Nada único: 7/7 en la batería v2 y sin rol en el router. |
| 2 | `qwen3.5-9b-the-defiant-fable-uncensored-heretic-neo-imatrix-max-mtp` | 5,72 GB | `/mnt/ssd_ia_datos/LM STUDIO/DavidAU/Qwen3.5-9B-The-Defiant-Fable-Uncensored-Heretic-NEO-IMATRIX-MAX-MTP-GGUF` | 0 consumidores, 0 rol, 0 evidencia propia. Fine-tune de comunidad de la línea Qwen 3.5 (ya descartada por DEC-001). | Nada: 7/7 en la batería v2, sin rol. |

Resultado: **12 modelos / 75,84 GB** (se liberan 28,38 GB).

## NO borrar (y por qué)

| id | Tamaño | Motivo para conservarlo |
|---|---|---|
| `qwen3.6-35b-a3b_moe` | 21,17 GB | **Único 0,0 % / 81 respuestas del ledger** = la evidencia de `veracidad_critica`. 6 documentos del lab lo citan. Si se borra, `veracidad_critica` tendría que caer a `openai/gpt-oss-20b` (4,5–9,1 % con T=0,2) → **degrada la tarea de hechos del lab**. |
| `granite-4.0-h-tiny` | 4,00 GB | Las guías del lab le dan rol de nicho: 3,72 GiB, "útil cuando la tarjeta está muy ocupada". En la v3 del router es **alternativo 2 de `razonamiento`**. Solo liberaría 4 GB a cambio de tocar 3 documentos. |
| `glm-4.6v-flash` | 7,95 GB | ~25 scripts + `config.yaml`. Norma de visión (RULE-014). **Intocable.** |
| `google/gemma-4-12b-qat` | 7,15 GB | Principal de `redaccion_datos`; alternativo 1 de `vision`. |
| `openai/gpt-oss-20b` | 12,11 GB | Principal de `razonamiento` + `fallback` + alternativo en 6 buckets + `config.yaml`. **Intocable.** |
| `granite-4.1-8b` | 5,09 GB | 10 consumidores en código; alternativo en 6 buckets. |
| `dolphin3.0-llama3.1-8b-cyber-lora-test-v0.2` | 4,92 GB | Principal de `codigo` (B1 en 6,3 s vs 23,6 s de gpt-oss). |
| `deepseek/deepseek-r1-distill-qwen-14b` | 8,99 GB | Principal de `grounding`. |
| `lfm2.5-vl-3b` | 2,26 GB | VLM ligero (vistazos rápidos); alternativo 2 de `vision`. |
| `lfm2.5-2.6b` | 1,67 GB | 1 consumidor real (`context_builder`); alternativo de `interactivo`. |
| `text-embedding-bge-m3` (437 MB) / `text-embedding-nomic-embed-text-v1.5` (84 MB) | 0,5 GB | RAG del lab. **Intocables.** |

## Cómo borrar

**Verificado el 02-oct-2026 (09:20 CEST) con `lms --help`: NO existe subcomando de borrado** (los subcomandos son `chat/get/load/unload/ls/ps/import/server/log/link/runtime/clone/push/dev/login/logout/whoami`). El borrado es **manual en la GUI de LM Studio**:

1. Comprobar antes: `lms ps` debe decir "No models are currently loaded." (verificado 01-oct-2026 20:16 CEST).
2. LM Studio → pestaña **My Models** → buscar cada nombre exacto → **Delete**.
3. Después: `lms ls` debe decir **"You have 12 models, taking up 75.84 GB of disk space."**

Tamaños reales en disco (`du`, 02-oct-2026): `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` = 22.663.387.424 B · `Qwen3.5-9B-The-Defiant-Fable-Uncnr-Heretic-NEO-MAX-MTP-IQ3_M.gguf` = 5.722.667.232 B.

## Efectos colaterales en el lab (a aplicar DESPUÉS de borrar)

- `01-knowledge/modelos_por_tarea.yaml`: quitar de `modelos_instalados` las líneas 144-145 y de `sin_asignar` las líneas 195-197. **NO tocar** los bloques `mediciones_bateria_*`: son medidas reales de esos modelos, histórico válido.
- 2 scripts quedan apuntando a un modelo ausente (si se re-ejecutan, fallarán):
  `research/infografias/serie-ia-agentes/leccion-0-b-que-puedes-pedirle/diag-lms.py:6` y `medicion-tamano.py:24`.
- `02-infrastructure/inicio/estado-inicial.json:37` es un snapshot histórico: dejar como está.

## Fase 2 (solo si hace falta espacio) — NO recomendada hoy

Borrar además `_moe` + `granite-4.0-h-tiny` = 25,17 GB más → store 50,67 GB (51,4 % menos).
Condiciones: (a) reasignar `veracidad_critica` a `openai/gpt-oss-20b` en el YAML (1 línea) y aceptar más alucinación en hechos; (b) actualizar `GUIA-JOKO-LAB.md`, `GUIA-APRENDIZAJE-JOKO-LAB.md` y `research/auditoria-modelos-19ago.md`.
