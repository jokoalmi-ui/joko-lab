---
title: "Análisis — Post DataStreak: MCP vs Agent Skills (17-ago-2026)"
type: research
---

# Análisis — Post DataStreak: MCP vs Agent Skills (17-ago-2026)

**Fuente:** https://www.instagram.com/p/DXyMGkiAQjM/ (DataStreak, 30-abr-2026, imagen única 1440×1440)
**Método:** browser_get_images → descarga → GLM + browser_vision
**VERACIDAD:** [VERIFICADO]

## CONTENIDO (lo que dice)

### "MCP vs. Agent Skills" — 5 dimensiones de comparación

**Subtítulo**: "MCP provides a standard interface and runtime for tools and data. Agent Skills provide the intelligence, logic, and execution."

| Dimensión | MCP | Agent Skills |
|---|---|---|
| **1. Integración** | N agents + M backends (client↔server, iconos de BD) | SKILL.md: "on trigger always loaded", full instructions |
| **2. Arquitectura** | JSON-RPC, MCP server (Python/TS/C#/Java), **proceso separado, runtime propio** | Carpeta `my-skill/` con SKILL.md + scripts/run.sh + references/ + assets/ |
| **3. Invocación** | Schema de params → tool A → tool B (encadenado) | Agente ejecuta `bash run.sh`, `python do.py`, `curl api/` → output |
| **4. Runtime** | Contenedor MCP Server, agente conectado | Skill en el entorno del agente (bash/python/curl/node) — "runs in agent's env" |
| **5. Where it fits** | DB, Queue, Auth, SaaS, Stack (GitHub, Postgres, Stripe, Linear) — "high-frequency, low latency" | Know-how, convenciones, CLI recipes, templates (brand-guide, pdf-extract, doc-format) — "lightweight, no infra" |

**Rule of Thumb**: *Use MCP to connect to tools and data. Use Agent Skills to define how to think and act.*
**Together**: *MCP gives agents capabilities. Skills give agents intelligence.*

## FORMATO (cómo se ve)

- **Estilo**: cuadrado 1440×1440, tabla comparativa de 5 filas × 2 columnas
- **Cada celda**: iconos + texto breve + ejemplo técnico (JSON-RPC, SKILL.md, run.sh)
- **Cierre**: 2 reglas resumen ("Rule of Thumb" + "Together") con iconos

## Aplicación al LAB (contexto: hoy se implementó el primer MCP)

**El lab ES el caso de uso exacto de esta infografía:**
- **Agent Skills = lo que el lab domina**: 40+ skills (least-privilege-lab, instagram-carruseles-analisis, manim-video...) — know-how, convenciones, recipes
- **MCP = lo que el lab acaba de añadir**: Manim MCP (animation-server) — conexión estandarizada a una herramienta (Manim)

**Lectura clave para el lab**: la infografía confirma que la decisión de hoy
fue correcta en el diseño — Manim como MCP (herramienta externa, runtime
propio, proceso separado) y no como skill (que ya existía: manim-video).
La skill enseña CÓMO pensar/crear; el MCP ejecuta la herramienta. Ambos
coexisten: la skill `manim-video` + el MCP `animation-server`.

**Regla de oro aplicada al lab**: "Usa MCP para conectar herramientas y datos; usa Skills para definir cómo pensar y actuar." → El lab debe usar MCPs para exponer herramientas/datos (BD café-ia, perfume-ia, LanceDB; scripts externos) y skills para el know-how interno.

## Veredicto
**APORTA Y VALIDA.** No introduce nada nuevo para implementar, pero:
1. **Valida la arquitectura del lab** (skills + MCP coexistiendo — caso real hoy)
2. **Da un criterio claro para decidir futuro**: MCP = herramientas/datos externos; Skill = know-how interno. El próximo MCP candidato (exponer BD del lab) encaja con esta regla.
3. Formato de tabla comparativa aislable para slides del TFM.

**Nota de proceso**: la cuenta DataStreak publica infografías técnicas de buena calidad; el post original es de abril 2026 pero el tema es atemporal y conecta con el hilo MCP del día.
