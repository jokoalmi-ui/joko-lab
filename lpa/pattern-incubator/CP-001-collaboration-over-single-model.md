---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-07-25
---
# Colaboración especializada sobre modelo único

> **Estado:** Incubación (E0→E1)
> **Fecha:** 2026-07-25
> **Origen:** Análisis de Graph Engineering (informe externo) + 5 instancias previas en Joko Lab
> **Nivel de confianza:** Alto

---

## 1. Qué ocurrió

Al analizar el informe sobre Graph Engineering (julio 2026), emergió que la industria está redescubriendo un patrón que Joko Lab ya practicaba: **la inteligencia útil no viene de un modelo más potente, sino de la colaboración entre especialistas**.

El informe plantea Graph Engineering como "la última evolución del Prompt Engineering", pero al examinar críticamente el concepto, se observa que lo valioso no es el grafo ni la herramienta — es el principio subyacente: sistemas con nodos especializados, handoffs definidos y verificación externa superan a sistemas monolíticos.

En Joko Lab, este patrón ya se había observado empíricamente en múltiples contextos antes de encontrar una fuente externa que lo nombrara.

---

## 2. Evidencia que lo respalda

El patrón aparece en **al menos 5 contextos independientes** dentro de Joko Lab, más 1 fuente externa:

| # | Contexto | Descripción | Rol del patrón |
|---|----------|-------------|----------------|
| 1 | **Pipeline GLM→Gemma→Hermes→ChatGPT→Hermes** | Cadena de modelos especializados para extracción de principios visuales: GLM detecta (visión), Gemma analiza (parámetros), Hermes razona, ChatGPT critica, Hermes consolida | Cada modelo hace lo que mejor sabe |
| 2 | **KAP con revisión adversarial (M-001)** | Pipeline de asimilación de conocimiento con fase adversarial externa (ChatGPT/Claude) que critica la extracción inicial | Verificador separado del extractor |
| 3 | **delegate_task** | Hermes delega subtareas a subagentes especializados en lugar de hacerlo todo en un solo contexto | Especialización > monolítico |
| 4 | **Founderz (Claude como guionista + otro como generador)** | Dos modelos con roles distintos colaboran en la misma tarea | Roles complementarios |
| 5 | **LPA + Skills Hermes** | División entre conocimiento LPA (procedimientos portátiles) y runtime Hermes (skills adaptadoras) | Separación conocimiento/ejecución |
| 6 | **Informe Graph Engineering (fuente externa)** | La industria reconoce que un solo modelo con un loop no es suficiente; se necesita un sistema de nodos especializados | Confirmación externa del patrón |

**Total:** 6 instancias, 5 dominios distintos (visión, conocimiento, ejecución, educación, metodología), 1 fuente externa.

---

## 3. Contradicciones o limitaciones

1. **No todas las tareas necesitan colaboración.** Para tareas simples (responder un dato, ejecutar un comando), un solo modelo es más eficiente. Añadir capas de especialización añade latencia y complejidad.
2. **Coste de coordinación.** Cuantos más especialistas, más overhead de comunicación y más riesgo de pérdida de contexto entre handoffs.
3. **No hemos probado el límite inferior.** ¿A partir de qué complejidad mínima merece la pena la especialización? No lo sabemos.
4. **Dependencia de modelos comerciales.** En los casos 2 y 4 dependemos de ChatGPT/Claude como crítico externo. Si esos modelos dejan de estar disponibles, el patrón se debilita.
5. **Solo un dominio negativo testeado.** No hemos encontrado un contraejemplo claro donde un modelo único supere sistemáticamente a la colaboración especializada. Eso no significa que no exista.

---

## 4. Principio que parece emerger

> **La inteligencia útil de un sistema de IA no depende del modelo más potente, sino de la calidad de la colaboración entre especialistas.**

### Corolarios operativos:

- Un pipeline de modelos modestos con roles complementarios supera a un modelo enorme sin colaboración externa.
- El crítico debe ser independiente del generador (verificación externa).
- La especialización por rol (visión, razonamiento, crítica, consolidación) es más importante que la capacidad bruta del modelo individual.
- El coste de coordinación debe ser menor que el beneficio de la especialización.

---

## 5. ¿En qué otros proyectos podría aplicarse?

| Proyecto/Dominio | Aplicación potencial |
|------------------|---------------------|
| **Compan-IA** (proyecto futuro) | Pipeline Whisper→Ollama→Piper TTS: tres especialistas que colaboran |
| **n8n workflows** | Cada nodo como especialista, con verificación externa en workflows críticos |
| **LPA experiments** | Diseñar experimentos donde la hipótesis se pruebe con colaboración multi-modelo vs modelo único |
| **Cualquier proyecto de automatización local** | Separar captura, análisis, decisión y ejecución en componentes independientes |

---

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

**Condición de falsación:**

> Que un solo modelo abierto (ej: llama-4, qwen-4) ejecute una tarea compleja de Joko Lab en un solo prompt con = o mejor calidad que el pipeline multi-modelo actual, midiendo:
> - Calidad del resultado (evaluación humana ciega)
> - Tiempo de ejecución
> - Coste computacional

**Criterio concreto:** Si en una tarea del laboratorio (ej: extracción de principios de un vídeo, análisis de un diseño visual, asimilación de un recurso externo), un solo modelo iguala o supera al pipeline multi-modelo en los 3 ejes (calidad, tiempo, coste) durante 3 pruebas consecutivas, el patrón se debilita significativamente.

---

## 7. Decisión

*[Se rellena en la revisión periódica, no al crear el documento.]*

- [ ] Asciende a KNOWN.md como E1
- [ ] Asciende a procedures/ como procedimiento LPA
- [ ] Sigue en incubación (falta evidencia)
- [ ] Se descarta (no sobrevive a otro dominio / fue falseado)
- [ ] Se fusiona con otro patrón

**Fecha de revisión:** 2026-08-01 (próxima revisión semanal)
**Justificación:** [Pendiente]
