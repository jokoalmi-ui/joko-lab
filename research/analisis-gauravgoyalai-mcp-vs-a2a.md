---
title: "Análisis — MCP vs A2A (GauravGoyalAI, 22-ago-2026)"
type: research
---

# Análisis — MCP vs A2A (GauravGoyalAI, 22-ago-2026)

**VERACIDAD:** [VERIFICADO]
**Última actualización:** 13-nov-2026 (dato «A2A no activo» marcado caducado + matiz MCP-Tasks vs A2A; ver secciones finales)

**Fuente:** https://www.instagram.com/reel/DcUybP0TCw2/ (gauravgoyalai, 21-08-2026, 13 likes)
**Método:** caption íntegro extraído (browser_console)

## Contenido: MCP vs A2A

**Dos tipos de conectividad para agentes de IA:**
- 🔵 **MCP = Agent → Tools**: conecta agentes con herramientas, APIs, BBDD, archivos y datos externos
- 🔴 **A2A = Agent → Agent**: permite que agentes se comuniquen, deleguen tareas y colaboren

**Truco de memoria**: MCP da capacidades · A2A permite colaboración.
**Idea clave**: el poder real viene de usar AMBOS juntos en un sistema agéntico.

## 🔴 Para el LAB — VALOR: MEDIO-ALTO (aclara la distinción + valida el roadmap)

| Protocolo | En el lab |
|---|---|
| **MCP (Agent → Tools)** | ✅ Plenamente usado: lab-db (solo lectura), lancedb (RAG), animation-server (Manim) — 3 MCPs en producción |
| **A2A (Agent → Agent)** | ⚪ **NO activo** *(DATO CADUCADO el 13-nov-2026: A2A está activado y sirviendo — ver §Actualización 13-nov-2026)* — pero está en el roadmap: (1) Hermes 0.20+ soporta A2A (análisis "Gerald" 12-ago, backlog línea 242), (2) checklist upgrade 0.21 lo tiene como "NO activar sin confirmación" |

**Conexión real con el lab**:
1. El lab ya domina la mitad izquierda (MCP) — los 3 MCPs son la "capa de capacidades"
2. La mitad derecha (A2A) es el **siguiente paso natural**: formalizar la colaboración CLI ↔ Telegram (el flujo cross-session-awareness ya hace una versión manual de "agentes que se comunican" vía shared-events)
3. El upgrade a Hermes 0.21 (~23-ago) es el punto donde A2A se podrá activar — con confirmación explícita

**Futurible (ya existente, reforzado)**: A2A para formalizar la colaboración CLI↔Telegram tras el upgrade 0.21 — el post confirma que MCP+A2A juntos = el estándar del "sistema agéntico completo", y el lab está a medio camino (MCP ✅, A2A pendiente).

## Conclusión
Validación clara y concisa de la distinción. El lab tiene MCP ✅ y A2A en el roadmap post-upgrade. Sin acción nueva — el plan ya existe (checklist 0.21).

---

## Actualización 13-nov-2026 — el dato «A2A NO activo» está caducado

**Verificado en el host** (`date` 13-nov-2026 17:44): `platforms.a2a.enabled: true` en `~/.hermes/config.yaml:634-637` (puerto 9900, plugin `platforms/a2a` en `plugins.enabled`); `ss -ltnp` → `LISTEN 127.0.0.1:9900` con pid 2607 (`hermes`); `GET /.well-known/agent-card.json` → **HTTP 200, 7.866 B**, `name: hermes-milinux`, `protocolBinding: JSONRPC`, `protocolVersion: 1.0`, `streaming: true`.

Hermes ya **sirve** A2A inbound desde este host. Lo que falta no es el protocolo: es un peer con quien hablarlo. Se marca el dato antiguo en la tabla; no se borra (RULE-023).

## Matiz nuevo: MCP con extensión Tasks no es lo mismo que A2A

Fuente: https://www.instagram.com/p/DfphO_3EZMf/ — Damien Benveniste, 12-nov-2026 17:47 (26 likes, 0 comentarios). Caption íntegro leído por `og:title` y `og:description`; imagen única tipo infografía leída solo en el recorte 640×639 del `og:image`, porque el HTML no expone las URLs del CDN sin login. Enlace del post verificado: doc de Microsoft **prerelease** — canales MCP/A2A solo en entornos early-release, Entra ID por usuario, app registration obligatoria, facturación por Copilot Credits.

- **MCP = operación con nombre.** El cliente descubre nombre, descripción y esquema de entrada, y llama con argumentos; el resultado vuelve como *tool result*. Un tool puede ejecutar un agente entero.
- **MCP + extensión Tasks.** Ese mismo tool puede devolver un **task ID** y el cliente sondea hasta tener el resultado, siempre que ambos lados lo soporten. Por eso la **duración no distingue** los dos protocolos.
- **A2A = conversación con estado.** El **Agent Card** anuncia skills e interacciones soportadas; el llamante manda la petición con adjuntos y el remoto decide sus pasos: puede devolver mensaje directo o **tarea trackeada** (con preguntas de vuelta) y cerrar con un **artifact**, documento u objeto de datos. Los task IDs permiten seguir el trabajo entre intercambios.
- **Criterio de elección.** Si el host ya llama tools MCP, exponer al especialista por esa misma interfaz basta. A2A cuando el llamante necesita modelo compartido de conversación, estados de tarea y artifacts. El especialista puede usar MCP internamente.
- **Para el lab.** Refuerza el criterio de `graph-lab`: una llamada de herramienta no lleva estado de tarea; si el subagente tiene que preguntar, esperar y devolver un entregable, el patrón correcto es el de tarea con identificador, no el de tool call.
- **Lo que NO es.** Medición. Es divulgación de una función en preview de una plataforma cloud de pago, fuera del eje local-first. Cero cifras propias.

**VERIFICACIÓN:** config y puerto leídos en el host; Agent Card descargada (200, 7.866 B); doc de Microsoft extraída; caption por doble vía. No se obtuvo la infografía a resolución completa.
