---
title: "Análisis — Backend → AI Systems Engineering (codewithbrij, 21-ago-2026)"
type: research
---

# Análisis — Backend → AI Systems Engineering (codewithbrij, 21-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcSOy2ODmdo/ (codewithbrij, 20-08-2026)
**Método:** caption íntegro extraído (browser_console) — el contenido está en el texto,
sin necesidad de analizar imágenes

## Tesis del post
"Backend engineering no está muerto: se está convirtiendo en **AI systems engineering**."

- Hace 2 años: APIs, databases, queues, caching, auth, cloud, security, observability
- Ahora, UNA CAPA NUEVA encima: LLM APIs, embeddings, vector databases, RAG,
  context engineering, tool calling, model routing, agents, memory, evals,
  guardrails, human review, agent observability
- **"Llamar a una API de LLM es fácil. Construir un sistema FIABLE alrededor
  del modelo es la parte difícil."**
- Las 8 preguntas del sistema: cómo entra el contexto / cómo se seleccionan las
  tools / cómo se gestiona la memoria / cómo se aplican permisos / cómo se
  evalúan outputs / cómo se trazan fallos / cómo el humano sigue en el bucle /
  cómo se controlan coste y latencia
- Fases: 1. prompt engineering → 2. context engineering → **3. AI systems engineering**

## 🔴 Para el LAB — VALOR: MEDIO-ALTO (validación casi perfecta de la arquitectura)

El lab implementa CASI TODO el checklist del post, con implementación REAL:

| Componente del post | En el lab |
|---|---|
| LLM APIs | ✅ LM Studio :1234 + proxy :9911 |
| Embeddings / vector DB | ✅ bge-m3 + LanceDB (~21.5K filas) |
| RAG | ✅ joko-indexer + reranker :8765 (recall@5 100%) |
| Tool calling | ✅ Hermes tools + skills |
| Model routing | ✅ llm-router.sh (local gpt-oss / cloud según tarea) |
| Agents + memoria | ✅ Hermes + MEMORY.md + MEP-001 |
| Evals | ✅ evaluar_rag.py + batería PRODUCCIÓN (5x5) |
| Guardrails | ✅ gate de veracidad + hardline + tirith (hoy fail-closed) |
| Human review | ✅ confirmación explícita + revisor en sesión |
| Agent observability | ✅ pipeline_proxy :9911 + informe diario + watchdogs |
| Coste/latencia | ✅ regla de costes (12:00 → local 0 €) + telemetría TTFB |
| Permisos | ✅ least-privilege-lab (toolsets mínimos) |

**"The real engineering is the harness around it"** = exactamente la filosofía del
lab: el modelo es 1 componente; el sistema (gate + revisor + telemetría + crons)
es lo que da fiabilidad.

## Futurible
Ninguno nuevo (el lab ya lo tiene). Pero el post es **vocabulario perfecto para
LinkedIn/TFM**: "Phase 3 is AI systems engineering" — el lab ES un ejemplo vivo
de esa fase 3 (harness completo alrededor del modelo).

*Nota: post de texto íntegro — sin análisis de imágenes necesario.*
