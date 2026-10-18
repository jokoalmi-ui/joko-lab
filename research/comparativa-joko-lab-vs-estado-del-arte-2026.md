---
type: research
subtype: research
status: active
tags: [research]
created: 2026-07-29
---
# Joko Lab vs Estado del Arte — Julio 2026
**VERACIDAD:** [ALCANCE INTERNO]

## Comparativa entre lo más avanzado en IA y nuestro laboratorio

---

## 1. Frameworks de Agentes (Multi-Agent Orchestration)

### 🏆 El panorama en 2026

| Framework | Stars/Adopción | Filosofía | ¿Qué tiene Joko Lab equivalente? |
|---|---|---|---|
| **LangGraph** (LangChain) | 65M+ descargas/mes | Grafos de ejecución, nodos+aristas, estado persistente | 🟡 Equivalente conceptual: n8n + AI Router. Sin estado de grafo nativo. |
| **OpenClaw** | 374K ⭐, adquirido por OpenAI ($1B) | Agentes autónomos local-first, loops→grafos | 🟢 Filosofía alineada: local-first, skills, loops. Precursores del Graph Engineering. |
| **CrewAI** | ~100K ⭐ | Equipos con roles definidos, tareas secuenciales | 🟡 Parecido: multi-modelo con roles (Obrero, Pensador, Director Creativo). |
| **AutoGen (MS)** / AG2 | ~50K ⭐ | Conversación entre agentes, código como acción | 🔴 No hay equivalente directo. Podría integrarse. |
| **Agno** | Emergente | Control total, personalización extrema | 🟢 Similar: Hermes + skills da control total. |

### 🔍 Diagnóstico

**Joko Lab no usa ningún framework de agentes comercial.** Usa **Hermes Agent** (base), **n8n** (workflows), **AI Router** (enrutamiento local/cloud) y **LPA** (memoria/conocimiento). Esto es más ligero que LangGraph pero menos estructurado para grafos complejos.

> **Veredicto:** Joko Lab está alineado conceptualmente pero carece de un framework de grafos de ejecución como LangGraph o OpenClaw. Lo suplimos con n8n + AI Router + skills.

---

## 2. Memoria Persistente para Agentes

### 🏆 El panorama en 2026

| Sistema | Enfoque | Estrellas / Inversión |
|---|---|---|
| **Mem0** | Memoria episódica + semántica. 48K ⭐ | $24M Series A |
| **Zep** | Grafo temporal de conocimiento (Graphiti) | Producción empresarial |
| **Letta** | Memoria virtual tipo OS (evolución de MemGPT) | Liderazgo técnico |
| **LangMem** | SDK de memoria nativo de LangChain | Integración directa con LangGraph |

### 🔍 Diagnóstico

**Joko Lab usa LPA (Living Product Architecture):**
- Clasificación de evidencia E0→E4
- Constitución con normas JL-001 a JL-012
- Skills como memoria procedural
- CHARLA/ para registros de sesión

**Carencias detectadas:**
- No tenemos un sistema de memoria vectorial persistente para el agente (falta integración con BGE-M3 + LanceDB que ya tenemos instalados para RAG)
- LPA es más epistemológico que técnico — no hay consulta programática al historial del agente

> **Veredicto:** LPA es conceptualmente superior a Mem0/Zep en estructura de conocimiento, pero técnicamente inferior. La memoria procedural (skills) es un acierto. Falta integrar la base vectorial que ya tenemos.

---

## 3. Arquitectura Híbrida Local↔Cloud

### 🏆 El panorama en 2026

El estado del arte para 2026 es un **modelo de inferencia por niveles (tiered inference)**:

```
Nivel 1 (Edge/Local):   Modelos 7-14B Q4 → baja latencia, privacidad, coste cero
Nivel 2 (On-prem):      Modelos 30-70B Q4 → capacidad media, coste fijo
Nivel 3 (Cloud):        Modelos frontier → capacidad máxima, coste variable
```

**Principios establecidos:**
- Enrutamiento inteligente basado en capacidad, latencia y coste
- Plano de control compartido + capa de observabilidad unificada
- "Data gravity": datos sensibles no salen del dispositivo

### 🔍 Diagnóstico

**Joko Lab ya implementa esto:**
- ✅ AI Router decide entre local (LM Studio, Ollama) y cloud (DeepSeek)
- ✅ Modelo de decisión por capacidad (Obrero, Pensador, Director Creativo)
- ✅ Privacidad: datos nunca salen del PC para tareas sensibles

**Carencias:**
- ⚠️ No hay observabilidad unificada (métricas de coste, latencia por modelo)
- ⚠️ La decisión local/cloud es manual (no automática por carga)
- ⚠️ Solo un nivel cloud (DeepSeek), sin múltiples proveedores

> **Veredicto:** Arquitectura correcta, implementación básica. De las áreas más maduras del laboratorio. El AI Router es la pieza clave que nos diferencia.

---

## 4. Optimización de Prompts

### 🏆 El panorama en 2026

| Técnica | Descripción |
|---|---|
| **DSPy** | Optimización declarativa automática de prompts. Entrena prompts como si fueran parámetros. |
| **Prompt chaining** | Cadenas de prompts con verificación en cada paso. |
| **Meta-prompting** | Prompts que generan prompts. |
| **Constitutional AI** | Principios éticos integrados en el prompt base. |
| **CI/CD para prompts** | Tests automatizados en pipelines. |

### 🔍 Diagnóstico

**Joko Lab:**
- ✅ Skill `prompt-engineering` con catálogo de 7 modelos probados
- ✅ 35 experimentos documentados con resultados reales
- ✅ Anti-patrones por modelo identificados
- ✅ Conexión con LPA (JL-011, JL-012)

**Carencias:**
- ❌ No tenemos DSPy ni optimización automática de prompts
- ❌ No hay CI/CD para prompts (tests automáticos)
- ⚠️ La skill es manual, no hay pipeline automatizado

> **Veredicto:** Joko Lab está mejor que la mayoría en documentación empírica de prompts, pero muy por detrás en automatización. Donde el mundo usa DSPy, nosotros usamos ensayo-error manual documentado.

---

## 5. Hardware y Modelos

### 🏆 El panorama en 2026

| VRAM | Capacidad | Recomendación industria |
|---|---|---|
| 8 GB | 7B Q4 | Mínimo para entrada |
| **12 GB** | **7-14B Q4** | **Entrada real (A2000, 3060)** |
| 16 GB | 14-20B Q4 | Gama media |
| 24 GB | 30-70B Q4 | Gama alta (3090, 4090, 5090) |
| 48+ GB | 70B+ Q4 / 120B | Profesional (A6000, Apple M3 Ultra) |

**Veredicto industria 2026:** "12GB VRAM is a dead end for 30B+ local LLMs."

### 🔍 Diagnóstico

**Joko Lab (RTX A2000 12GB + i9-9900K):**
- ✅ En el punto dulce para 7-14B (Dolphin, Llama, Qwen3, DeepSeek R1, Gemma 4, GLM, Granite)
- ✅ Catálogo de 7 modelos probados y clasificados por rol
- ⚠️ Limitado a modelos 14B como máximo (los MoE como Granite H Small de 32B no caben)
- ⚠️ PCIe 3.0 limita el ancho de banda GPU (la A2000 es PCIe 4.0 x8 nativa)

> **Veredicto:** Hardware correcto para 2026, pero en el límite inferior. Para modelos de razonamiento profundo (DeepSeek R1 14B, Gemma 4 12B) funciona bien. Para 30B+ necesitaríamos 24GB.

---

## 6. Tabla Resumen: Joko Lab vs Estado del Arte

| Dimensión | Estado del Arte | Joko Lab | Diferencia |
|---|---|---|---|
| **Orquestación multi-agente** | LangGraph, OpenClaw, CrewAI | n8n + AI Router + Hermes | 🟡 Equivalente funcional, menos pulido |
| **Memoria persistente** | Mem0, Zep, Letta | LPA (epistemológico) + SQLite | 🟡 Superior conceptual, inferior técnico |
| **Arquitectura híbrida** | Tiered inference + shared control plane | AI Router (2 niveles, manual) | 🟢 Correcta, falta automatización |
| **Optimización de prompts** | DSPy, CI/CD pipelines | Skill manual + 35 experimentos | 🔴 Manual vs automático |
| **Model testing** | Benchmarks estandarizados (MMLU, etc.) | Pruebas propias con 5 tests × 7 modelos | 🟢 Más realista que benchmarks |
| **Grafos de ejecución** | Graph Engineering, LangGraph | Conceptual, documentado en informe | 🔴 No implementado |
| **Hardware** | 12GB VRAM (entrada) - 48GB (profesional) | RTX A2000 12GB | 🟡 En el límite inferior |
| **Skills / procedural memory** | — (no existe como concepto) | Skills en Hermes Agent + LPA | 🟢 **Ventaja diferencial** |

---

## 7. Conclusiones estratégicas

### 🟢 Dónde estamos por delante

1. **Skills como memoria procedural** — Ningún framework comercial tiene este concepto. Skills + LPA es nuestra ventaja más clara.
2. **Testing empírico de modelos** — 35 experimentos reales con 7 modelos en nuestro hardware. Esto vale más que cualquier benchmark.
3. **Arquitectura híbrida** — Correcta en concepto, con AI Router y separación local/cloud.
4. **Prompt Engineering documentado** — La skill con modelo, patrones y anti-patrones es más valiosa que DSPy sin contexto.

### 🟡 Dónde estamos en línea

1. **Catálogo de modelos** — 7 modelos con roles es un número respetable.
2. **n8n como orquestador** — Puede no ser LangGraph pero cubre el 80% de los casos.
3. **Hardware** — A2000 12GB es lo esperable para un laboratorio personal en 2026.

### 🔴 Dónde estamos detrás

1. **Optimización automática de prompts** — DSPy es el estándar y no lo tenemos.
2. **Memoria vectorial persistente** — Tenemos BGE-M3 + LanceDB instalados pero no integrados con el agente.
3. **Graph Engineering** — Lo hemos teorizado pero no implementado.
4. **Observabilidad** — Sin métricas de coste, latencia, rendimiento por modelo.

### 🎯 Próximos pasos recomendados

Prioridad | Acción | Impacto
---|---|---
1 | Integrar BGE-M3 + LanceDB como memoria vectorial del agente | Cierra la brecha con Mem0/Zep
2 | Implementar un pipeline de test automático de prompts (similar a DSPy) | Automatiza la skill prompt-engineering
3 | Construir el primer grafo de ejecución simple en n8n o script Python | Pasa de teoría a práctica de Graph Engineering
4 | Añadir dashboard de observabilidad (latencia, coste por modelo) | Toma de decisiones basada en datos
5 | Monitorizar ofertas de RTX 3090 usadas (24GB VRAM) | Desbloquea modelos de 30B+
