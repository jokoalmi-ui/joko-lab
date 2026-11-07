---
title: "Análisis — «6 Powerful Ways to Reduce AI Agent Hallucinations» (@theagenticaiengineer, 06-nov-2026)"
type: research
---

# Análisis — «6 Powerful Ways to Reduce AI Agent Hallucinations» (@theagenticaiengineer, 06-nov-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DfbXS3QNvuf/ (`@theagenticaiengineer`)
**Fecha del post:** 06-nov-2026 — literal de `og:description`: «theagenticaiengineer el November 6, 2026». Análisis: 07-nov-2026 (hora exacta en el registro de escritura, tomada con `date`).
**Material:** caption de 1.504 chars leído de `og:description`. **No es vídeo** (`yt-dlp --dump-json`: «There is no video in this post»). **Nº de láminas: no verificado** — el JSON embebido devuelve `carousel_media_count: 20`, cifra del bloque del feed lateral, no del post; con ese dato no se afirma cuántas imágenes tiene.

## Contenido — las 6 técnicas, citadas del propio post

1. «Grounded Knowledge (RAG) – Use trusted, up-to-date data instead of relying only on the LLM’s training knowledge.»
2. «Better Prompts & Constraints – Define clear roles, instructions, context, and boundaries.»
3. «Tool Use & Verification – Connect agents to APIs, databases, and search tools to validate information.»
4. «Self-Reflection & Critique – Let agents review, fact-check, and improve their responses before answering.»
5. «Confidence Checks & Guardrails – Set confidence thresholds and trigger human review when necessary.»
6. «Relevant Memory & Context – Maintain the right conversation history, domain knowledge, and task state.»

Cierre del post (literal): «Key Takeaway: A reliable AI agent needs more than a powerful LLM. It needs the right knowledge, tools, validation, memory, and guardrails.»

No cita ninguna fuente, ni autores, ni medidas. Es una lista de conceptos, sin implementación ni cifras.

## Cruce con el lab — 6 de 6 ya cubiertos

- **1. RAG** → `local-rag` + `agentic-rag`; índice LanceDB `joko_notes` con **61.698 filas** (`/home/jokoalmi/joko-lab/.lancedb`), reindexado por cron activo.
- **2. Prompts y límites** → `prompt-engineering` + el system prompt del lab.
- **3. Tool use y verificación** → `gate-veracidad` + `state-verification-pattern`; regla operativa propia: no se afirma nada sin la salida real del comando.
- **4. Autocrítica** → `tools/juez_alucinaciones.py` (juez) y `tools/evaluar_alucinaciones.py` (evaluador).
- **5. Umbrales y revisión humana** → golden set con categoría `contexto_ausente` (esperado: «NO_SÉ») y `trampa`; avisos del lab con acuse obligatorio (`avisos-con-acuse-lab`).
- **6. Memoria y contexto** → MEP-001 (`~/.hermes/scripts/memoria-episodica.sh`, 3.052 B) + RAG + USER/MEMORY.

Ninguna de las seis técnicas es nueva para el lab. El post funciona como checklist externa y se cierra **6/6**.

## El hueco que sí aparece al cruzar

El instrumento de medición existe y está **frío**:

- `04-operations/metrics/alucinaciones_ledger.jsonl` — **23 filas**, de **2026-08-24** a **2026-09-14**, sobre **5 modelos** distintos (`deepseek/deepseek-r1-distill-qwen-14b`, `gpt-oss-20b` ×2, `qwen3.6-35b-a3b_moe`, `ibm/granite4.2:8b-q4_K_M`).
- `tools/golden_set_alucinaciones.json` — **27 preguntas** en **4 categorías** (`contexto`, `contexto_ausente`, `memoria`, `trampa`).

Es decir: el lab sabe *cómo* medir alucinaciones y tiene el banco montado, pero lleva **54 días sin medir** (última corrida 2026-09-14) — casi ocho semanas. La deuda no es la lista del post; es que la única cifra de alucinación del lab es de mediados de septiembre y de modelos que en parte ya no se usan.

## Qué NO es este documento

- No es contenido validado: una lista de conceptos sin fuente no entra en `KNOWN.md`.
- No es una recomendación de adopción: no hay nada que adoptar, ya está adoptado.
- No es una medición: no se ha ejecutado el golden set en este pase; los números citados son de inventario y de fecha de última corrida, no de tasa de alucinación.

## Límites del método

- El caption es `og:description`, que Instagram trunca a ~1.500 chars: si el post tenía texto más largo, aquí no aparece. Se declara como no verificado, no como completo.
- Las láminas no se han abierto; el veredicto se sostiene en que el caption lista las seis técnicas completas.
- La identidad de la cuenta (`@theagenticaiengineer`) no está verificada fuera de Instagram; no se le atribuye autoridad, solo autoría del post.
