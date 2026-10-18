---
title: "Análisis de video — hdeleon.net \"Después de ver esto, usarás la IA de otra forma\""
type: operations
---

# Análisis de video — hdeleon.net "Después de ver esto, usarás la IA de otra forma"

Fecha: 2026-08-07
Fuente: https://youtu.be/1w6SxWR-wdA (9:38, canal hdeleon.net)
Tipo: análisis de referencia (solo archivo, sin backlog ni eventos)

## Qué muestra

Combinar agentes de IA (indeterministas) con herramientas deterministas para
ahorrar tokens, tiempo y dar mejor contexto al modelo. Ejemplo práctico:
generar clases C# a partir de un XSD de facturación electrónica (CFDI México)
usando el comando XSCGen en lugar de dejar que el agente lea el XSD de 5MB y
escriba las clases él mismo. Resultado mostrado: ~500.000 líneas de código
generadas por la herramienta sin pasar por el modelo.

## Puntos técnicos centrales

1. No hacer que el agente haga trabajo determinista (cobertura, complejidad
   ciclomática, mutación): ejecutar herramientas deterministas que ya lo hacen.
   Cita tweet de Uncle Bob: "todo lo que pueda ser determinista, con herramienta
   determinista. No intentes que los agentes sigan un proceso determinista".
2. No dar cadenas largas de instrucciones: el agente pierde el hilo. En su
   lugar, máquina de estados finita ejecutable que dirija sus acciones.
3. El conocimiento del dominio es lo que dice qué herramienta determinista
   existe. El ahorro viene de saber que la herramienta existe, no de que el
   LLM razone mejor.

## Validez

Principio correcto y no novedoso: patrón "herramienta determinista + LLM como
orquestador". La demostración es honesta en lo esencial: el código generado no
pasa por tokens, y el tiempo real lo consume el comando (archivo de 5MB), no
el modelo.

Limitaciones del video: presentación clickbait (promoción de cursos, "modelo
pedorrón"), sin cifras de ahorro de tokens (no cuantifica), sin comparación
rigurosa con el enfoque todo-LLM. El ahorro es evidente por lógica, no medido.

## Utilidad en el LAB

Confirmación, no novedad. El lab ya aplica el patrón en varios sitios
(documentado en skill local-rag):

- reranker daemon: modelo pesado cargado UNA vez, servido por HTTP (no por
  llamada).
- lmstudio_embeddings.py: embeddings vía API en vez de cargar BGE-M3 a mano.
- indexer.py v2 incremental por hash: re-embebe solo lo que cambió.
- activation_engine.py: enrutado por reglas deterministas antes del LLM.
- crons no_agent: scripts puros sin LLM (telemetría, backups, consolidación).

El conocimiento del dominio ya existe: KOs, skills y preflight checklist hacen
que el LLM use herramientas existentes en vez de reinventar procesos.

La parte que NO aplica tal cual: el ejemplo concreto (C#/.NET + XSD México) no
es el stack del lab. Equivalente en el lab: no pedir al LLM que re-embeba o
lea 5MB; ejecutar indexer.py / search.py.

## Punto potencialmente nuevo

La máquina de estados finita ejecutable para dirigir agentes, en lugar de
cadenas de instrucciones. El lab tiene piezas parecidas (gates de commit,
flujos por fases con puertas, Agentic RAG Loop PLAN-RETRIEVE-EVALUATE-
REFORMULATE-SYNTHESIZE documentado como pendiente en local-rag), pero no una
FSM explícita y ejecutable que dirija las acciones de un agente. Único punto
candidato a estudio como posible pendiente del lab.
