---
title: "INFORME FINAL — P1: Ahorro de tokens del contexto RAG (crudo vs estructurado)"
type: operations
---

# INFORME FINAL — P1: Ahorro de tokens del contexto RAG (crudo vs estructurado)

**Fecha:** 2026-08-04
**Estado:** COMPLETADO (medición 2-ago; informe final 04-ago)
**Backlog:** P1 (2026-07-31-backlog.md) — "Medir ahorro real de tokens, 4 dimensiones"

---

## 1. Objetivo

Medir el ahorro real de tokens del contexto RAG al pasar de la variante
CRUDA (documento/snippets completos) a la ESTRUCTURADA (ruta + campos clave
+ summary corto), en 4 dimensiones: tokens, latencia, precisión, cobertura.
Hipótesis del KAP (2026-07-31, video PKM): ~55x de ahorro (14,850 → 320 tok).

## 2. Metodología

- Herramienta: `verification/medir_p1.py` (creada 02-ago-2026).
- Banco: 6 items de `verification/bank.yaml` (preguntas con respuesta esperada
  y fuente; evaluación con comparador determinista, sin juicio de LLM).
- Modelo: granite-4.1-8b en LM Studio (`:1234`), temperature=0.
- Variantes:
  - CRUDO: `tools/context_builder.py` (snippets completos).
  - ESTRUCTURADO: `tools/context_builder_estructurado.py` (extracción compacta).
- Estimación de tokens sin LLM: ~4 chars/token (heurística estándar).
  Con LLM: `usage.prompt_tokens` real del endpoint.

## 3. Resultados — DOS NIVELES (no contradictorios, complementarios)

### Nivel A — Contexto RAG realmente recuperado e inyectado (GUIA §6.10)

| Ronda | Variante | tok_ctx (est) | prompt_tok | t_total(s) | precisión | cobertura |
|---|---|---|---|---|---|---|
| 2 (02-ago, tras curar DEC-001/RULE-001) | CRUDO | 303.83 | 527.50 | 21.63 | 5/6 | 6/6 |
| 2 | ESTRUCTURADO | 319.17 | 476.67 | 21.92 | 6/6 | 6/6 |
| 3 (02-ago, bge-reranker-v2-m3 + curación) | CRUDO | 351.00 | 524.50 | 23.21 | 6/6 | 6/6 |
| 3 | ESTRUCTURADO | 339.17 | 503.50 | 21.86 | 6/6 | 6/6 |

Ahorro real en prompt_tokens: **~10%** (527 → 477). El RAG ya filtra por
recuperación: inyecta solo los trozos relevantes, así que la diferencia de
formateo sobre lo ya recuperado es pequeña.

### Nivel B — Documento íntegro vs extracto estructurado (métrica v2, backlog)

| Métrica | Valor |
|---|---|
| Documento crudo ÍNTEGRO | ~19.9k tokens |
| Extracto ESTRUCTURADO | ~323 tokens |
| **Ahorro (consulta 1)** | **98.4%** |
| Ahorro (consulta 2) | 98.0% |

Este es el nivel del KAP (55x): si en lugar de pasar el documento completo se
pasa el extracto estructurado, el ahorro es ~98%. Confirmado el factor ~55-60x
a nivel de documento.

## 4. Conclusiones

1. **La hipótesis del 75% NO se confirma a nivel de contexto RAG** (~10% real),
   pero **el 55x del KAP SÍ se confirma a nivel de documento íntegro** (98.4%).
   Ambas cifras son correctas: el RAG ya filtra; el formateo estructurado
   importa cuando se trabaja con el documento completo.
2. **El valor real está en la curación (OKF), no en el formateo.** Al curar
   DEC-001 y RULE-001 (campos que el reranker usa), ambos KOs subieron a la
   posición 1 y cobertura/precisión pasaron a 6/6. El fallo de fondo del
   reranker (KOs en español hundidos por ms-marco) quedó resuelto con
   `BAAI/bge-reranker-v2-m3` (el nombre sin "-v2-" NO existe, 404).
3. **Adoptado:** `context_builder.py` usa el formateo estructurado desde
   02-ago (backup `context_builder.py.bak-20260802`); consumidores
   (run_eval, joko-context, knowledge_resolver) sin cambios de API.
4. **Cuello de botella real:** search.py (~15s) — mitigado con daemon del
   reranker + lazy import (14.8s → 2.6s, sesión 02-ago) y latencia de
   construcción del contexto ~15s → ~4.3s (GUIA §6.4/§6.11).
5. **Monetización del dato:** 19.9k → 323 tokens por documento es dinero real
   en DeepSeek/Gemini por consulta cuando se procesan docs completos.

## 5. Acciones cerradas con P1

- [x] Herramienta de medición reproducible (medir_p1.py, 4 dimensiones).
- [x] Variante estructurada y adoptada en producción.
- [x] Curación de KOs (DEC-001, RULE-001) + reranker multilingüe.
- [x] Documentación: GUIA §6.10 (detalada) + este informe final.
- [ ] Pendiente de la agenda del 05-ago: test de velocidad Telegram vs CLI
      (10:00) — medición ortogonal (latencia de canal, no tokens).

## 6. Cómo reproducirlo

```bash
cd ~/joko-lab/verification && ~/.venv/hermes-rag/bin/python3 medir_p1.py
cd ~/joko-lab/verification && ~/.venv/hermes-rag/bin/python3 medir_p1.py --no-llm
```

Requiere LM Studio en `:1234` con granite-4.1-8b cargado (o `--model X`).
El script NO modifica nada del lab.
