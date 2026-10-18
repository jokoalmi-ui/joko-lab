---
title: "Análisis — RAG Pipeline Observability Architecture"
type: research
---

# Análisis — RAG Pipeline Observability Architecture
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 04-ago-2026
**Fuente:** Post de code_hive.dev en redes sociales (infografía recibida por Telegram)
**Imagen:** `~/.hermes/image_cache/img_bf7cb89bdc66.jpg`

---

## Lo que muestra la infografía

Pipeline RAG end-to-end con observabilidad en CADA paso:

```
query → embedding → vector DB → re-rank → prompt → LLM → evaluación
   └───────└──────└───────└──────└──────└──────└──
   Cada paso emite: traces + logs + metrics → OTLP exporter
```

**Tesis del post:** "Un sistema RAG de producción necesita más que respuestas
precisas — necesita observabilidad" (ver qué pasa en cada paso, no solo el
resultado final).

---

## Los 3 pilares de cada paso

| Señal | Qué responde | Ejemplo en RAG |
|---|---|---|
| **Trace** | ¿Quién llamó a quién? (cadena) | query → embedding → rerank → LLM |
| **Log** | ¿Qué pasó exactamente? | "recuperó 10, re-rankeó a 3" |
| **Metric** | ¿Cuánto tardó / costó? | latencia embedding, tokens prompt |

**Exportación:** OpenTelemetry (OTLP) — estándar de facto, vendor-neutral.

**Punto clave:** la EVALUACIÓN es parte del pipeline (no post-mortem).

---

## Conexión con Joko Lab (estado real 04-ago)

| Paso del pipeline | Equivalente en el lab | ¿Observable hoy? |
|---|---|---|
| Query | context_builder | ⚠️ Parcial |
| Embedding | BGE-M3 (LM Studio API) | ❌ No medido |
| Vector DB | LanceDB | ❌ No medido |
| Re-rank | joko-reranker (daemon :8765) | ✅ Health endpoint + tiempo medido (0.91s CPU) |
| Prompt | context_builder_estructurado | ⚠️ Logs manuales |
| LLM | DeepSeek cloud / LM Studio | ⚠️ Parcial |
| Evaluación | evidence_contract.py | ✅ Existe (0/9 KOs cumplen) |

**Veredicto:** el lab tiene casi todos los pasos, pero la observabilidad NO está
unificada (no hay trazas OTLP ni métricas consolidadas). Es exactamente el hueco
del backlog F4 (observabilidad) — implementado parcialmente el 29-jul (monitor
LM Studio :5000) pero sin cubrir el pipeline RAG completo.

---

## Acciones sugeridas (para el futuro, backlog F4)

1. **Medir cada paso del RAG** (latencia embedding, búsqueda, rerank, prompt)
   — ya tenemos datos sueltos (reranker 0.91s, búsqueda 11.6s) pero no
   consolidados por consulta.
2. **Registro por consulta:** cada búsqueda RAG emite un log JSON con
   (query, top_k recuperados, scores, tiempo por paso, tokens).
3. **Métricas agregadas:** tiempo medio de búsqueda, tokens promedio por
   consulta (relacionado con P1: ahorro 98.4% ya medido).
4. **Evaluación integrada:** usar evidence_contract como paso del pipeline,
   no como auditoría externa.

**Relación con P1 (tokens):** la medición del 03-ago (crudo 19.9k → estructurado
323 tokens, ahorro 98.4%) ES una métrica de observabilidad del paso "prompt".
Ampliar ese patrón a los demás pasos = F4 completo.

---

## Nota

Infografía de divulgación técnica (code_hive.dev). Conceptualmente correcta y
útil como referencia visual del objetivo F4. No requiere implementación
inmediata — queda como guía para cuando se retome observabilidad del RAG.
