---
title: "Análisis — Carrusel thepracticai: \"Build your own MCP server\" (18-ago-2026)"
type: research
---

# Análisis — Carrusel thepracticai: "Build your own MCP server" (18-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DblDC8WErcm/ (thepracticai — canal de IA práctica, 2 slides, 1440×1798)
**Método:** browser_console (ig_cache_key) → fetch navegador (2 slides, 101-140 KB) → GLM-4.6v-flash vía analizar_carrusel_rapido.py (512px, 36s total). ⚠️ Llama-server huérfano (6h, 8.1 GB) bloqueaba GLM → kill (patrón autorizado skill lm-studio) → recarga GLM 19s.
**Veracidad:** [VERIFICADO] — contenido extraído de la imagen real, no de memoria.

## Slide 1 — Arquitectura: "Build your own MCP server"

- **MCP Host** (aplicaciones cliente): Claude · Cursor · YourApp
- Cada host tiene un **MCP Client** que se conecta a **múltiples instancias de MCP Server**
- Cada MCP Server se conecta a: **APIs privadas · base de datos · APIs web públicas**
- La arquitectura permite REUTILIZAR el servidor MCP en múltiples hosts (una vez construido, sirve a todas las apps)

## Slide 2 — El problema que resuelve MCP

- Los modelos IA están **entrenados hasta una fecha y CONGELADOS**: saben generalidades pero nada del usuario
- Limitaciones concretas (del diagrama):
  - ❌ No saben "¿qué tareas están pendientes hoy?" (datos del usuario)
  - ❌ No acceden a sistemas externos ("ver la BD de staging de Postgres")
  - ❌ No ejecutan acciones ("crear un ticket en Jira")
- **Sin MCP**: la app IA interactúa DIRECTAMENTE con cada servicio (acoplamiento)
- **Con MCP**: la app usa un SERVIDOR que media las conexiones (desacoplamiento + reutilización)

## 🎯 CONEXIÓN DIRECTA CON EL LAB — VALIDACIÓN EXTERNA DEL MANIM MCP

| Elemento del carrusel | En el lab (implementado 17-ago) |
|---|---|
| MCP Host = Claude/Cursor/YourApp | Hermes (CLI + Telegram) |
| MCP Client | `animation-server` registrado en config.yaml (enabled: true) |
| MCP Server | `~/manim-mcp/server/animation_mcp.py` (FastMCP, 2 tools) |
| API privada / BD | Manim (generación de vídeos animados local) |
| Servidor reutilizado en múltiples hosts | ✅ Verificado: la CLI y Telegram (sesiones nuevas) usan el mismo servidor |

**El lab ya es exactamente la arquitectura de la slide 1**: un host (Hermes) con un MCP server propio (Manim). El carrusel valida el camino y sugiere el siguiente paso natural: **exponer las BD propias (café-ia, perfume-ia, LanceDB) como MCP servers** — el futurible ya registrado en backlog.

## ✅ IMPLEMENTADO 20-ago-2026 (verificado con salida real)

El futurible "exponer BD propias como MCP" está COMPLETO:
- **lab-db** (18-ago): SQLite perfume-ia (coleccion.db) + café-ia (cafes.db), 5 tools, SOLO lectura.
- **lancedb** (20-ago): RAG joko_notes (21.247 filas), 2 tools (`buscar_rag`, `info_rag`), SOLO lectura, device=cpu (no roba VRAM a LM Studio). Servidor `~/mcp-lancedb/server/lancedb_mcp.py`, venv `~/.venv/hermes-rag` (fastmcp+mcp añadidos, torch/lancedb ya estaban). Verificado: `hermes mcp test lancedb` ✓ + consulta real OK (seguimiento-prueba1, prueba1-cafeina-14h, horario-diario).
- Queda como extensión futura: joko_images (CLIP) — requiere otro modelo de embeddings, solo si el usuario la pide.

## ⚠️ Nota de proceso (día de aprendizaje)

- GLM-4.6v-flash NO cargaba (400 "exited before becoming healthy") → **llama-server huérfano de 6h con 8.1 GB bloqueaba la VRAM** (patrón documentado en skill lm-studio: matar PID + recargar; autorizado previamente por el usuario)
- Tras kill: VRAM 0.9/12 GB → `lms load glm-4.6v-flash` → 19s, 7.41 GiB → análisis OK
- El analizador con `--max_tokens 400` truncaba el detalle de slide_01 → re-análisis con 1200

## 📌 Valor para el lab

1. **Material LinkedIn**: "Así se ve un MCP por dentro" — el lab tiene una implementación real que contar (Manim MCP)
2. **Validación del roadmap**: el carrusel confirma el patrón host→client→server→APIs que el lab ya usa
3. **Futurible reforzado**: exponer BD propias como MCP (café-ia, perfume-ia, LanceDB) — siguiente MCP del lab
