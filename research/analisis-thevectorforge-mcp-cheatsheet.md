---
title: "Análisis — Cheat sheet MCP (TheVectorForge / Backend and AI, 01-sep-2026)"
type: research
---

# Análisis — Cheat sheet MCP (TheVectorForge / Backend and AI, 01-sep-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcqxZHLiELD/ (@thevectorforge, carrusel 8 slides, 38 likes · 43 comments, 2 días). Transcripción completa con GLM local (8/8 slides).

## Contenido (carrusel completo)

1. **WHAT IS MCP?** — "el USB-C para aplicaciones AI": estándar abierto que permite a apps AI conectarse de forma segura a datos, herramientas y servicios externos. Diagrama: AI app → MCP → (datos, archivos, APIs, tools, cloud). Key takeaway: exponer capacidades vía MCP en vez de integraciones personalizadas.
2. **WHY DO WE NEED MCP?** — el problema N×M: cada app construye su integración custom (duplicación, difícil de mantener, se rompe con cambios, caro). The MCP way: build once, expose via MCP, use everywhere.
3. **MCP ARCHITECTURE** — User → AI Host/App → MCP Client → MCP Server → (Tools, Resources, Prompts) → sistemas externos. **El modelo exacto que usa el lab.**
4. **MCP PRIMITIVES** — **Tools = Do** (acciones, `send_email(to, body)`) · **Resources = Read** (contexto, `file:///docs/Architecture.md`) · **Prompts = Guide** (plantillas reutilizables, `incident_report`). Con ejemplos de definición Python.
5. **HOW AN MCP TOOL CALL WORKS** — flujo de 5 pasos con ejemplo real: crear ticket Jira (`create_ticket` → Jira REST API → "Ticket PRJ-5678 creado"). MODEL decide, CLIENT conecta, SERVER ejecuta.
6. **BUILD A SIMPLE MCP SERVER** — ejemplo Python: definir server + tool (`@mcp.tool()`), añadir resource, añadir prompt, SDKs (Python, JS/TS).
7. **MCP TRANSPORTS** — **STDIO (local)**: client inicia el server como proceso hijo, JSON-RPC, mejor para dev local · **Streamable HTTP (remoto)**: HTTPS, mejor para cloud/producción. Tabla comparativa.
8. **MCP CHEAT SHEET** — resumen: primitivas, dónde brilla (agentes, dev productivity, cloud, search), checklist del servidor, **la fórmula: `MCP Client + MCP Server + Tools/Resources/Prompts = Connected AI`**.

## 🔴 Aplicación al LAB — VALOR MEDIO-ALTO (validación + 1 idea concreta)

| Ángulo | Veredicto |
|---|---|
| **La arquitectura del carrusel = la del lab** | 🟢🟢 El lab YA tiene implementado el modelo exacto: Hermes (AI Host con cliente MCP integrado) + 3 servidores MCP activos (animation-server, lab-db, lancedb) verificados. La slide 3 es un diagrama de lo que el lab ya corre |
| **Tools/Resources/Prompts** | 🟢🟢 Los 3 MCPs del lab exponen exactamente eso (lab-db: tools de búsqueda + resources + prompts; lancedb: buscar_rag/info_rag) — validación directa de que el lab usa las primitivas correctas |
| **Transports: STDIO vs Streamable HTTP** | 🟢 **Idea para verificar**: el carrusel distingue local (proceso hijo, JSON-RPC) vs remoto (HTTPS). ¿Cómo están conectados los MCPs del lab? Si todos son STDIO local — bien para el lab (local-first). Si alguno podría ser remoto — no aplica (el lab es local por diseño). |
| **Ejemplo servidor Python (slide 6)** | 🟡 GLM transcribió `FastAPMServer` — probablemente es **FastMCP** (el nombre real del SDK). ⚠️ Ojo con la fidelidad de GLM en código: contrastar antes de usar. El lab ya tiene `create-mcp-lab.sh` (skill integracion-mcp-lab) |
| **"Build once, expose via MCP, use everywhere"** | 🟢 Es exactamente el motivo de los 3 MCPs del lab: mismos datos (perfumes, cafés, RAG) accesibles desde cualquier herramienta (Hermes, n8n, scripts) |
| **La fórmula final** | 🟢 Validación del enfoque: MCP como capa de integración universal en el lab |

**Conclusión**: validación fuerte del diseño MCP del lab (que ya implementa la arquitectura "correcta" del carrusel). 1 acción opcional: revisar cómo están conectados los 3 MCPs (STDIO vs HTTP) para confirmar que usan el transporte adecuado al caso local. El carrusel es material educativo sólido — no hay nada nuevo que implementar.

**Nota honesta**: perfil con "Contenido generado con IA" (como todos los reels recientes de este estilo) — contenido educativo genérico pero bien estructurado; el lab ya está 1 paso por delante (tiene los MCPs corriendo, no solo el diagrama).
