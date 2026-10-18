---
title: "Análisis — BEYOND THE WHILE LOOP: Agent Graph Engineering (Rubix Script, 10 slides)"
type: research
---

# Análisis — BEYOND THE WHILE LOOP: Agent Graph Engineering (Rubix Script, 10 slides)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 10-ago-2026
**Fuente:** https://www.instagram.com/p/Db2GFnUlbel/ — rubix_codes
**Método:** Descarga 10 imágenes (HEIC→JPG) + GLM 4.6V local

---

## Contenido (Agent Graph Engineering — grafos de agentes)

1. **Beyond the while loop** — "A loop is one path. A graph is every path you meant to allow." Nodes, edges, shared state y concurrencia.
2. *(estado compartido / node design)*
3. *(edges y transiciones)*
4. *(definición de nodos)*
5. **Routing es solo una función** — el ruteo como función pura que decide el siguiente nodo.
6. **Ciclos en grafos de agentes** — un grafo NO es un DAG; los loops son conexiones hacia atrás con condiciones de salida ("React as a graph").
7. **Paralelismo fan-out/fan-in** — agentes secuenciales demoran ~6x; un grafo que fana a N ramas paralelas y mergea con un reducer reduce la latencia.
8. **Checkpoints para agentes long-running** — pausar, fork, aprobación humana, resume-after-crash, time-travel.
9. **Multi-agent es una forma, no una vibra** — elegir la topología (estructura), no solo "añadir agentes".
10. **Diseñar el grafo antes de promptear** — estado tipado, reducers, router, ciclo checkpointado, ramificación paralela. Comentar "GRAPH" → starter.

---

## 🎯 Aplicación al LAB

| Concepto | Lab | Estado |
|---|---|---|
| **Loop = un camino, grafo = todos los caminos** | Agentic RAG Loop (un loop) | 🟡 El lab tiene 1 loop principal |
| **Routing como función pura** | decision_engine.evaluate() + router local/cloud | ✅ Ya es una función pura |
| **Ciclos con condiciones de salida** | Agentic RAG Loop tiene límites de iteración | ✅ |
| **Fan-out/fan-in paralelo** | No hay (secuencial) | 🟢 Futurible (p.ej. analizar N imágenes en paralelo) |
| **Checkpoints human-in-the-loop** | F4 Gate (humano decide) | ✅ El lab ya tiene gate humano |
| **Multi-agent = topología** | Un agente + OpenCode worker | 🟡 Coherente: el lab ya decidió NO multi-agente |
| **Estado tipado + reducers** | scripts con estado YAML/JSON | 🟡 Sin framework |

### Veredicto honesto

**Este carrusel explica el porqué de las decisiones del lab** — valida la
arquitectura actual (1 agente + workers, gate humano, router como función pura).
Los conceptos son de diseño de grafos de agentes (estilo LangGraph), que el lab
ya cubre conceptualmente SIN framework (decisiones 22 frameworks + Agentic
Handbook).

**Las 2 ideas nuevas accionables (futuribles):**
1. **Fan-out/fan-in paralelo** — el lab procesa imágenes/carruseles secuencialmente
   (GLM una a una, ~2 min/imagen). Con paralelismo (3 ramas) tardaría ~3x menos.
2. **Checkpoints/time-travel** — el lab tiene backups y snapshots, pero no
   "pausar/reanudar" un agente en medio de una ejecución larga.

## Conclusión

Material de diseño de agentes (rubix_codes, estilo arquitectura de grafos).
Para el lab: **valida las decisiones existentes** (router función pura, gate
humano, no-multi-agente) + 2 futuribles menores (paralelismo fan-out para el
análisis de imágenes, checkpoints formales). NADA urgente.

## Nota

Las slides 8-9 usaron reasoning (GLM) pero el contenido es claro: checkpoints
para agentes long-running y "multi-agent es una forma, no una vibra" (topología
> cantidad de agentes).
