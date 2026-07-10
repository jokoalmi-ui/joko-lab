# Decisión Técnica: Arquitectura Agéntica Jerárquica (Director Cloud → Ejecutor Local)

**Fecha**: 2026-07-10
**Estado**: Aceptada
**Área**: Arquitectura de IA y Enrutamiento

## Contexto
El laboratorio contaba con una arquitectura híbrida donde los modelos Cloud (Gemini/DeepSeek) y Local (Ollama) se alternaban según la hora. Aunque eficiente en costes, desaprovechaba la sinergia entre el razonamiento estratégico de la nube y la capacidad de ejecución local de bajo coste.

## Problema
- El modelo Cloud gastaba tokens y tiempo en tareas puramente mecánicas (búsquedas, lectura de logs, listados).
- No existía una jerarquía de roles (Arquitecto vs. Ingeniero de Ejecución).

## Decisión
Implementar un modelo de gobierno agéntico basado en el patrón **Orchestrator-Worker**:
1. **Cloud Director (Arquitecto Técnico):** Se ejecuta en el bloque principal (`model:`). Es responsable de comprender, planificar, priorizar, delegar y revisar. Configurado para *DeepSeek* (noche) o *Gemini* (día).
2. **Local Worker (Ingeniero de Ejecución):** Se ejecuta en el bloque de delegación (`delegation:`). Es responsable de ejecutar trabajo operativo (búsquedas, lecturas, generación de archivos). Configurado fijo 24/7 en *Ollama* (qwen2.5:7b o llama31).
3. **Mecanismo de Delegación:** El Director Cloud utilizará obligatoriamente la herramienta `delegate_task` de Hermes para asignar trabajo al Worker Local, sin intervenir directamente en las tareas mecánicas.

## Motivos
- Minimiza el uso de herramientas pesadas por parte del modelo cloud, ahorrando latencia y costes.
- Maximiza el uso del hardware local (NVIDIA RTX A2000) para procesamiento de texto repetitivo.
- Aísla la toma de decisiones estratégicas de la ejecución operativa.
- Mantiene intacta la regla de seguridad `approvals.mode: manual`.

## Consecuencias
- Las tareas requerirán la autorización del usuario tanto para lanzar el subagente como para que el subagente ejecute comandos (doble factor de seguridad).
- Aumenta la madurez de la métrica de **Autonomía** del laboratorio.

## Referencias
- `HERMES.md` (Principios de delegación y arquitectura híbrida).
- Documentación de Hermes Agent sobre `delegate_task` y subagentes.