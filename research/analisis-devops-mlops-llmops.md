---
title: "Análisis — Carrusel: DevOps vs MLOps vs LLMOps (mentalhotfix, 9 slides)"
type: research
---

# Análisis — Carrusel: DevOps vs MLOps vs LLMOps (mentalhotfix, 9 slides)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 09-ago-2026
**Fuente:** https://www.instagram.com/p/Db0P2W3iTth/ — @mentalhotfix (Prateek Singh)
**Método:** Descarga carrusel (9 slides) + GLM 4.6V local

---

## Qué es

Comparativa de los 3 pipelines de entrega en IA:

| | DevOps | MLOps | LLMOps |
|---|---|---|---|
| **Opera** | Software | Modelos | Apps LLM |
| **Pipeline** | Plan→Code→Build/Test→Release→Deploy→Monitor | Datos→Prep→Train→Eval→Register→Deploy→Monitor | Foundation Model→Prompt/Context→RAG/Tools→Eval→Guards→Deploy→Feedback |
| **Foco** | Entregar software fiable | Ejecutar ciclo de vida del modelo | Ejecutar apps LLM fiables |
| **Riesgos** | Bugs, fallos de despliegue | Data drift, modelos degradados | Alucinaciones, contexto, seguridad |

**Mensaje central:** "MODEL WORKING ≠ APP WORKING" (que el modelo funcione no implica que la app funcione).

**Modelo mental final:** Código + Modelos + Contexto = Producto IA
- DevOps = entrega de software
- MLOps = entrega de modelos
- **LLMOps = entrega de la EXPERIENCIA de IA**

---

## 🎯 Aplicación al LAB

### El lab YA tiene los 3 pipelines (sin etiquetarlos así)

| Pipeline | Lab |
|---|---|
| **DevOps** | Docker (n8n, ollama...), systemd (indexer, reranker), crons, backups |
| **MLOps** | LM Studio (modelos), evaluación RAG, revalidar_kos, telemetría observer |
| **LLMOps** | Hermes, pipeline_proxy, RAG (BGE-M3+LanceDB), evidencia (TD-001), Eval (evaluator_optimizer) |

### Lo ÚNICO que aporta (conceptualmente)

**1. "MODEL WORKING ≠ APP WORKING"** — la lección clave:
- El lab ya la aplica: el evaluator_optimizer y el Evidence Contract (TD-001) verifican
  que la APP (el pipeline completo) funciona, no solo que el modelo responde.
- VALIDA la decisión del lab de no quedarse en "el modelo carga bien".

**2. El pipeline LLMOps explícito (slide 5):**
`Modelo → Prompt/Contexto → RAG/Herramientas → Evaluar → Frenos → Desplegar → Feedback`
- El lab cubre todas las etapas: RAG (search), Evaluar (evaluator_optimizer,
  evidence_contract), Frenos (evidencia/gate), Feedback (observer, ledgers).
- CONFIRMA que la arquitectura del lab es un LLMOps completo, no solo RAG.

**3. El modelo mental "Código + Modelos + Contexto = Producto IA"** — útil para:
- El TFM/Founderz (explicar el stack en una frase)
- La presentación de la plantilla cuaderno block

### Veredicto honesto

**El carrusel VALIDA la arquitectura del lab** (es un stack LLMOps completo),
pero **no aporta nada accionable nuevo** — el lab ya tiene las 7 etapas del
pipeline LLMOps y ya aplica "MODEL WORKING ≠ APP WORKING" con su gate de
evidencia. Sin backlog nuevo.

**Único valor extra:** material conceptual para el TFM (la frase "MODEL
WORKING ≠ APP WORKING" y el modelo mental Código+Modelos+Contexto son
excelentes para explicar por qué el lab tiene gate de evidencia).

## Nota

Canal @mentalhotfix (Prateek Singh) — contenido educativo de ingeniería IA.
