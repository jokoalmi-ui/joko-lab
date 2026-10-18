---
title: "Análisis — 7 Chunking Strategies para RAG (The ThinkLab by Saurabh, 20-ago-2026)"
type: research
---

# Análisis — 7 Chunking Strategies para RAG (The ThinkLab by Saurabh, 20-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/reel/Dbr5HjJRY1I/ (The ThinkLab by Saurabh, 06-ago)
**Método:** caption íntegro del snapshot (el vídeo es blob; el caption contiene las 7 estrategias, patrón validado)
**Veredicto:** [VERIFICADO] — cruzado contra la estrategia real de chunking del lab

## ⚠️ VALOR REAL: MEDIO-ALTO (temática central del RAG del lab — evaluación, no acción inmediata)

El post lista 7 estrategias de chunking. El lab YA usa chunking en su RAG
LanceDB (joko_notes, ~19.9K filas, recall@5 100% verificado). El valor real
es AUDITAR qué estrategia usa el lab frente a esta taxonomía y decidir si
alguna mejora el recall. No es accionable sin medir (el lab ya mide).

## Contenido (caption íntegro, resumido)

> "Tu RAG solo es tan bueno como tu estrategia de chunking. Muchos
> desarrolladores optimizan embeddings, prompts y LLMs — pero pasan por alto
> el chunking."

### Las 7 estrategias
| # | Estrategia | Cuándo |
|---|---|---|
| 1 | **Fixed-Size** | Prototipos rápidos y simples |
| 2 | **Recursive** | Default bueno para la mayoría de RAG |
| 3 | **Structure-Based** | Preserva jerarquía del documento (headers/sections) |
| 4 | **Semantic** | Divide por significado, no por tamaño |
| 5 | **Sliding Window** | Mantiene contexto con solapamiento |
| 6 | **Parent-Child** | Retrieval preciso + contexto rico (hijo→padre) |
| 7 | **Agentic/Adaptive** | La IA elige la estrategia por documento |

### Key takeaways
- Mejor chunking → mejor retrieval → respuestas más precisas → menos alucinaciones
- **No hay one-size-fits-all**: depende de los datos y el caso de uso

## 🔴 Conexión con el LAB (auditoría real)

El lab tiene RAG LanceDB (joko_notes) con **recall@5 100% (70 ms)** — ya
verificado. La pregunta honesta: **¿qué estrategia de chunking usa el
indexer del lab?**

| Estrategia del post | Estado en el lab |
|---|---|
| Recursive / por párrafos | ✅ Probablemente la usada por joko-indexer (a verificar en el código del indexer) |
| Parent-Child | 🟡 **Candidata a evaluar**: notas largas de joko-lab (docs de 100+ líneas) podrían beneficiarse (chunk hijo + contexto padre) |
| Semantic | 🟡 Coste de embeddings extra — evaluar solo si recall baja |
| Agentic | ❌ Sobre-ingeniería para el lab (12 GB, local-first) |
| Sliding Window | 🟡 Útil si hay solapamiento perdido entre chunks |

**⚠️ Regla del lab aplicada**: NO cambiar el chunking sin medir antes. El
lab tiene la herramienta para medir (evaluar_rag.py + adversarial). El
paso sería: (1) auditar qué estrategia usa joko-indexer hoy, (2) si no es
Parent-Child, correr una evaluación comparativa, (3) decidir con datos.

## Veredicto honesto

**Valor medio-alto como checklist de auditoría** — no como guía de acción.
El lab ya tiene RAG verificado (recall@5 100%); el chunking actual FUNCIONA
para las notas actuales. El post sugiere una mejora potencial (Parent-Child
para docs largos), pero cambiarla sin medir violaría la regla del lab
("métrica anómala → validar; umbrales nunca a priori"). Futurible menor:
**auditar estrategia de chunking de joko-indexer + prueba comparativa de
Parent-Child** (señal: cuando se indexen docs largos, p.ej. manuales o
TFM).

## Nota honesta

Análisis del caption íntegro (el vídeo es blob; los alts del feed mostraban
"19-ago" pero el post es del 06-ago según el timestamp del caption — los
alts son de otros reels del perfil). El lab puede auditar su chunking real
con una sola consulta al indexer (pendiente de hacer — ver Futurible).
