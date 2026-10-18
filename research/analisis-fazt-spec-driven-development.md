---
title: "Análisis — \"Spec Driven Development: El flujo real para crear apps con IA\" (Fazt Code, 27-ago-2026)"
type: research
---

# Análisis — "Spec Driven Development: El flujo real para crear apps con IA" (Fazt Code, 27-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/_jJJDQOXSxM (Fazt Code, 27-ago, 40.681 views, 31:53)
**Método:** pipelina YT → metadatos + descripción íntegra con timeline 00:00-31:00 (32 puntos). Subs es-orig NO descargables (yt-dlp sin JS runtime — mismo fallo que atareao 827; refuerza el futurible Invidious del 25-ago).

## Contenido (timeline completo)

**Tesis**: el ciclo de desarrollo NO ha cambiado (planificación → diseño → implementación → testing → despliegue); la IA lo acelera y automatiza, pero no lo elimina. Diferencia clave:

| | Vibe coding | Spec-Driven Development |
|---|---|---|
| Para quién | No técnicos | Desarrolladores |
| Proceso | "Escribe la idea y dale al botón" | Planificación primero |
| Specs | — | **Cubren 70-80% del proyecto** |
| Modelo | Importa | **Casi no importa** (planificación > modelo) |
| Testing | — | Adversarial con IA |

**Puntos clave del timeline:**
- **08:00-12:30 — Specs**: generar especificaciones y arquitectura ANTES de programar; la planificación es más importante que el modelo
- **15:30-17:00 — Agentes**: implementa con Claude Code; "casi no importa el modelo"; agentes trabajando en paralelo
- **18:00-20:00 — Testing adversarial** con IA; NO es fan del TDD puro con IA (ventajas y limitaciones)
- **20:00-22:00 — Despliegue**: CLIs + skills, automatización
- **26:30 — Loop Engineering**: desarrollo iterativo con agentes
- **29:00 — Flujo recomendado**: Spec-Driven en proyectos reales, varios proyectos en paralelo

## 🔴 Aplicación al LAB — VALOR MEDIO-ALTO

| Ángulo | Veredicto |
|---|---|
| **Specs antes de código** | 🟢 **VALIDACIÓN DIRECTA del PRD Graph delegación multi-agente (18-ago)**: el PRD del lab ya especifica nodos, contratos de edges, política de modelos y gates ANTES de tocar código — exactamente el patrón Spec-Driven. Fazt confirma: sin specs, el agente vaga |
| **Planificación > modelo** | 🟢 Coincide con el fallo del 25-ago (fusión 2/5): el problema no era el modelo local, era la falta de verificación. Fazt: "casi no importa el modelo" |
| **Testing adversarial** | 🟢 El lab YA lo hace: suite 219+14, verificar_research.py, LLM-as-judge (PASA/REVISA/FALLA/DISCREPANCIA) |
| **Loop Engineering (26:30)** | 🟢 Mismo concepto que codewithbrij "The Loop Governs" (18-ago): el lab implementa hasta Loop (gate, estado persistente) |
| **Agentes en paralelo** | 🟡 Refuerza el PRD graph (investigador+redactor+revisor paralelos) — pendiente de aprobación F0 |
| **CLIs + skills para despliegue** | 🟢 El lab ya automatiza con CLIs (joko-git-recibos, create-mcp-lab.sh, deployment script) |
| **Despliegue VPS (patrocinio Hostinger)** | ⚪ Patrocinado — el lab ya decidió NO contratar VPS (25-ago, el PC local cubre) |

**Conclusión**: VALOR MEDIO-ALTO — valida el patrón Spec-Driven que el lab ya sigue (PRD graph, gates, planificación antes de código) y da material para el TFM (capítulo "desarrollo de software con agentes"). Sin futuribles nuevos — refuerza la aprobación pendiente del PRD graph (F0).

## Anexo — Matices de la transcripción real (youtube_transcript_api, 31-ago)

Tras el fix del PO Token (skill video-transcription), la transcripción completa
(40.419 chars) confirma el análisis y añade:

1. **"El modelo casi no importa" — CON DATOS**: "los modelos del top 10 cada vez se parecen más... la brecha se está cerrando... la diferencia va a ser en precio" — valida la política de costes del lab (no pagar por el modelo más caro cuando el local/barato da lo mismo).
2. **Testing adversarial — ejemplo real**: la reescritura de **Bun en Rust** usó "un agente de Claude escribiendo + dos agentes de GPT revisando, bucle de ~11 días, 1 millón de líneas" — EXACTAMENTE el patrón del PRD graph (escritor + 2 revisores paralelos). Confirma la estructura del graph.
3. **TDD — por qué NO es fan (matiz)**: "si la IA escribe el código y también el código del testing, ¿qué evita que la IA modifique el mismo código del testing?" — argumento nuevo que justifica el enfoque del lab (testing adversarial externo, no TDD auto-generado).
4. **Grill Me / Matt Pocock**: "el skill más instalado, llegando al millón de descargas semanal" — el lab ya lo tiene como futurible (podcast 17-ago, integrar en F3 del PRD). Confirmado por Fazt.
5. **Loop Engineering — límite honesto**: "solo para proyectos muy puntuales (web scraping)... para sistemas con módulos, roles, nube — usar spec-driven" — matiza el "Loop Governs": el loop automático NO reemplaza la planificación para sistemas grandes.
6. **Despliegue = CLIs + skills**: "la infraestructura se puede generar con código y la IA puede generar código → la IA genera la infraestructura... pero necesitas entender la arquitectura para saber si es lo que quieres pagar" — valida que el lab deba entender su stack antes de automatizar despliegues.
