---
title: "Análisis — MCPs más usados en 2026 + MCPs a medida (17-ago-2026)"
type: research
---

# Análisis — MCPs más usados en 2026 + MCPs a medida (17-ago-2026)

**Fuente:** web_search (3+ fuentes: Totalum, Shareuhack, MCPBundles, Awesome-MCP, K2View)
**VERACIDAD:** [ALCANCE INTERNO]
detalles de cada server según snippets (no extract completo — backend solo-búsqueda)

## 1. Los MCPs más usados en 2026 (consenso entre fuentes)

| # | MCP | Qué hace | Por qué importa |
|---|---|---|---|
| 1 | **Context7** (Upstash) | Docs actualizadas de librerías (React, Next.js...) inyectadas en el contexto — "no API alucinadas" | **El más popular del ecosistema** según Shareuhack (mayo 2026) |
| 2 | **Playwright MCP** | Automatización de navegador | **"El más usado de la comunidad"** (Totalum) — browser testing |
| 3 | **GitHub MCP** | Repos, PRs, CI/CD | Esencial para dev |
| 4 | **Filesystem MCP** | Acceso a archivos locales con scope | Seguridad: solo ve lo que el usuario permite |
| 5 | **MindsDB** | Agregador: 1 endpoint → 200+ fuentes (Postgres, Snowflake, Salesforce, Slack...) | No cablear un server por fuente |
| 6 | **Slack MCP** | Historial, búsqueda, contexto de hilos, mensajes | Respeta permisos del workspace |
| 7 | **Salesforce MCP** | Datos CRM inyectados en flujos LLM | Marketing/ventas |
| 8 | **Knowledge management MCPs** | Triage de comunicación (categoría que crece rápido en 2026) | "Ahorra más tiempo que casi cualquier otro uso" (MCPBundles) |

**Top-5 recomendado por Totalum**: Context7 + GitHub + Playwright + Filesystem + 1 de app-building.

## 2. ¿Los MCPs se pueden crear a medida? — **SÍ, y es el caso de uso central**

**Respuesta corta: SÍ, crear MCPs a medida es una práctica estándar y documentada.**

- **FastMCP (Python)** es la librería que impulsa ~70% de los MCPs (danilchenko.dev, 2026)
- Tutoriales oficiales/actualizados (2026): desde "hello world" de 9 líneas hasta
  servidores con Docker, auth y hardening de seguridad
- Un MCP custom expone **tools, resources y prompts** de tu propio código/datos
- **Prueba real en el lab HOY**: el Manim MCP (animation-server) es un MCP a
  medida — escribimos el servidor, corregimos bugs, lo conectamos a Hermes y
  lo usamos en producción. **El lab ya tiene la capacidad demostrada.**

## 3. Relevancia para el LAB

| MCP | Aplicación al lab | Valor |
|---|---|---|
| **Context7** | Docs actualizadas de librerías — útil para el desarrollo del lab | 🟡 Futurible (el lab usa docs locales/skills; poco beneficio hoy) |
| **Playwright** | El lab ya tiene browser (Hermes); un MCP Playwright sería redundante | ❌ Ya cubierto |
| **GitHub MCP** | El lab tiene `gh` CLI + skills GitHub | ❌ Ya cubierto |
| **Filesystem** | Hermes ya tiene file tools con scope | ❌ Ya cubierto |
| **MindsDB** | Acceso unificado a BD — el lab tiene SQLite/LanceDB por proyecto | 🟡 Posible futuro (unificar café-ia, perfume-ia, coleccion.db) |
| **MCP a medida (FastMCP)** | **YA DEMOSTRADO hoy** (Manim MCP) — el lab puede crear servidores MCP propios para sus BD, scripts y herramientas | ✅ **Capacidad instalada** |

## Veredicto honesto
**Ninguno de los MCPs "top" del ecosistema es imprescindible para el lab**
(la mayoría cubre capacidades que Hermes ya tiene nativas: browser, filesystem,
GitHub, Slack...). El valor real para el lab está en la **capacidad de crear
MCPs a medida** (ya demostrada con Manim): exponer las BD propias (café-ia,
perfume-ia, LanceDB) o scripts como servidores MCP estandarizados. El candidato
más interesante de los externos sería MindsDB (unificar acceso a datos) — pero
solo si el lab crece en número de BD. La lección del día: **el ecosistema MCP
valida la dirección del lab (conectar herramientas propias de forma
estandarizada), no requiere adoptar los servers populares por defecto.**
