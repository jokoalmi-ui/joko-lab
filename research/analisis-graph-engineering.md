---
title: "Análisis — Carrusel Instagram: Graph Engineering (techwith.ram)"
type: research
---

# Análisis — Carrusel Instagram: Graph Engineering (techwith.ram)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 05-ago-2026
**Fuente:** https://www.instagram.com/p/DbIlcUzieqr/ — techwith.ram (Data Science | ML | Ramakrushna)
**Método:** carrusel 7 slides — descargadas del CDN + analizadas con GLM
**Lección aplicada:** se obtuvieron TODAS las imágenes del carrusel (no solo el alt)
para identificar las del post (slides 1-2); las 3-7 eran de otros posts del perfil.

---

## El post (slides 1-2 del carrusel)

**Título:** "Graph Engineering: Beyond Single Feedback Loops"
**Caption:** "Un grafo bien diseñado no solo hace tu agente más rápido — lo hace
más fácil de depurar, extender y confiar. Si construyes agentes IA, workflows
o aplicaciones LLM en producción, Graph Engineering es una skill que vale la
pena aprender."

### Slide 1 — Concepto
Graph Engineering = el arte de diseñar flujos de trabajo de agentes IA como
un **grafo** (nodos y aristas), superando los bucles de feedback simples.
Transforma tareas complejas en pasos conectados que operan en orden o paralelo.

### Slide 2 — ¿Qué es Graph Engineering? (los 4 bloques)

| Bloque | Función |
|---|---|
| **Nodo** | Una tarea ejecutada por un agente |
| **Borde** | Dependencia entre tareas |
| **Estado** | Contexto compartido entre nodos |
| **Puerta Humana** | Checkpoint de aprobación (intervención humana) |

**Ejemplo del diagrama:** Investigar → Recopilar datos → Escribir borrador →
Revisar → **aprobación humana** → salida.

**Frase clave:** "Diseñar el grafo correcto hace que los agentes trabajen más
inteligentemente, más rápido y con menos errores."

---

## Conexión directa con Joko Lab (Loop Engineering L2)

**El L2 diseñado el 04-ago es un grafo — y este carrusel lo valida:**

| Concepto del carrusel | Equivalente en el diseño L2 |
|---|---|
| **Nodo** (tarea por agente) | Observer / Evidence / Proposer / Gate |
| **Borde** (dependencia) | El flujo: Observer → Evidence → Proposer → Gate |
| **Estado** (contexto compartido) | decision-ledger.jsonl + file bus (team-context/) |
| **Puerta Humana** (checkpoint) | **JL-012**: el humano decide — el Gate habilita, Joseba aprueba |

**El diseño L2 ya tiene los 4 bloques** — el carrusel confirma que la
arquitectura es la estándar de Graph Engineering 2026.

**Lo que el carrusel añade:** el énfasis en que el grafo hace el agente
"más fácil de depurar, extender y confiar" — los 3 beneficios que el L2 busca.
El ejemplo (Investigar → ... → aprobación humana → salida) es EXACTAMENTE el
flujo del L2 (observar → evidenciar → proponer → humano decide → aplicar).

---

## Nota metodológica (prueba de Instagram superada)

- Carrusel de 7 slides: se descargaron TODAS del CDN (aplicando la lección
  del póster de jugaldb) y se identificaron las 2 del post (1-2)
- Las slides 3-7 eran de otros posts del perfil (Claude+Obsidian, agente
  desde cero, libros, Ollama vs vLLM, AI then/now) — no del carrusel actual
- Lección confirmada: en carruseles, obtener todas las imágenes y filtrar
  por las que tienen el contenido del post (el alt de la primera suele ser
  suficiente pero conviene verificar el número de slides "0X/07")
