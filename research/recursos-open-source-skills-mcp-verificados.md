# Recursos Open-Source Skills + MCP para el lab — verificado 04-sep-2026
**VERACIDAD:** [ALCANCE INTERNO]

**Estado de verificación:** cada repo comprobado con la GitHub API (04-sep-2026: stars, updated_at, licencia).
**Método:** búsqueda web → candidatos → verificación determinista `curl api.github.com/repos/...` → solo lo OK entra.
**Lección del día:** 3 subagentes locales (r1-14b) reportaron 19 repos — TODOS fabricados (HTTP 404). La verificación con API es obligatoria; lo de abajo está verificado repo a repo.

## A. Repos oficiales / núcleo (verificados 04-sep)

| Repo | ⭐ | Licencia | Para qué |
|---|---|---|---|
| github.com/anthropics/skills | 173,8K | (multi) | Repo público oficial de Agent Skills de Anthropic: skills ejemplo, template, spec del formato. Fuente canónica del estándar SKILL.md |
| github.com/obra/superpowers | 281,5K | MIT | Framework agéntico de desarrollo (skills de proceso: brainstorm, plan, TDD, debug, review, verify). Portable a Cursor/Codex/Copilot |
| github.com/modelcontextprotocol/servers | 90K | — | Servidores MCP de referencia (archivados varios, verificar cada uno) |
| github.com/modelcontextprotocol/python-sdk | 24,2K | MIT | SDK oficial Python para construir servidores/clientes MCP |
| github.com/modelcontextprotocol/typescript-sdk | 13,3K | — | SDK oficial TypeScript para MCP |
| github.com/modelcontextprotocol/modelcontextprotocol | 9,1K | — | Especificación y documentación del protocolo MCP |

## B. Colecciones curadas de skills (verificadas 04-sep)

| Repo | ⭐ | Licencia | Para qué |
|---|---|---|---|
| github.com/composiohq/awesome-claude-skills | 74,4K | — | Lista curada enorme de skills Claude |
| github.com/punkpeye/awesome-mcp-servers | 94K | MIT | Colección de servidores MCP (más actualizada que el repo oficial archivado) |
| github.com/travisvn/awesome-claude-skills | 15K | — | Lista curada de skills + recursos para Claude Code |
| github.com/jeffallan/claude-skills | 11,3K | MIT | 67 skills especializadas full-stack (React, Python, DevOps, 30+ frameworks) |
| github.com/BehiSecc/awesome-claude-skills | 10,1K | — | Lista curada de skills Claude (organizada por categorías) |
| github.com/kepano/obsidian-skills | 47,8K | MIT | Skills para Obsidian (CLI, Markdown, Bases, JSON Canvas) — MUY relevante: el lab usa Obsidian |
| github.com/wondelai/skills | 2,1K | MIT | 50 skills negocio/marketing/UX/coding de libros bestseller (Norman, Cialdini, Ries, Hormozi) |
| github.com/gooseworks-ai/goose-skills | 1,2K | MIT | 125 skills growth/GTM (ads, contenido, lead gen, SEO, scraping) |

## C. Nichos valiosos (verificados, estrellas menores pero útiles)

| Repo | ⭐ | Licencia | Para qué |
|---|---|---|---|
| github.com/daxaur/openpaw | 167 | MIT | 38 skills asistente personal (git, Telegram, Discord, Obsidian, daily briefing) — patrón parecido al lab |
| github.com/guia-matthieu/clawfu-skills | 149 | MIT | 172 skills marketing expert (Dunford, Schwartz, Ogilvy, Cialdini) como MCP server |
| github.com/jonathimer/devmarketing-skills | 86 | MIT | 33 skills dev-marketing (HN, tutorials, SEO devtools) |
| github.com/pjt222/agent-almanac | 32 | MIT | 317 skills + 65 agentes referencia (directorio navegable) |
| github.com/obviousworks/Claude-AI-skills-collection-2026 | 52 | — | 94 skills, enlaces verificados contra GitHub API (jul-2026) |

## D. Documentación oficial / educación (verificadas con HTTP real 04-sep)

| Recurso | URL (verificada) | Qué es |
|---|---|---|
| Anthropic — Complete Guide to Building Skills for Claude | docs.claude.com/en/docs/agents-and-tools/agent-skills/overview (302 → platform.claude.com/docs/... 200 OK) | Guía oficial de 32 páginas (ene-2026) |
| Estándar abierto Agent Skills | agentskills.io (308 redirect activo) | Spec del formato SKILL.md abierto (~40 clientes adoptantes) |
| MCP documentación oficial | modelcontextprotocol.io (308 → /docs/2026-07-28/getting-started/intro, 200 OK) | Spec + guías MCP |
| Spec SKILL.md en anthropics/skills | github.com/anthropics/skills (spec/ + template/) | Fuente canónica del formato |

## F. Repos del experimento controlado de delegación (verificados 2× 04-sep)

6 repos reportados por el subagente gpt-oss-20b (deleg_ee0b8567, api_calls=15) y re-verificados 1 a 1 con la GitHub API desde la sesión (04-sep). Contrasta con la sección E: mismos criterios de tarea, modelo distinto → 6/6 reales vs 19/19 fabricados. Enfoque: skills específicas para **Hermes Agent** (el lab usa Hermes — más relevantes que las colecciones genéricas de la sección B).

| Repo | ⭐ | Licencia | Para qué |
|---|---|---|---|
| github.com/ZeroPointRepo/awesome-hermes-skills | 503 | MIT | Directorio comunitario 350+ skills, memory providers y tools para Hermes, Claude Code, OpenClaw, Cursor |
| github.com/tlehman/litprog-skill | 259 | — | Skill de programación literaria para Claude Code, OpenCode y Hermes: convierte codebases a docs `.lit.md` |
| github.com/itgoyo/hermes-skills | 54 | — | 310+ workflows reutilizables (coding, marketing, finanzas, MLOps) |
| github.com/moonlight-lupin/agent-skills | 47 | MIT | Colección de skills para Hermes Agent (research, creative, productivity, devops) |
| github.com/RobinBeraud/hermes-skills | 9 | — | Skills comunitarias SEO, WordPress y marketing |
| github.com/BBridgeers/hermes-skills | 0 | — | 372 skills exportadas de una deployment Hermes en producción (research, devops, AI-engineering) |

**Nota de curado:** ZeroPointRepo/awesome-hermes-skills y BBridgeers/hermes-skills son los más interesantes para auditar (directorio de 350+ y export real de producción); itgoyo 310+ y moonlight-lupin también. BBridgeers con 0⭐ pero updated 26-ago-2026 — un export de producción puede valer más que su popularidad sugiere; verificar contenido antes de portar nada.

## E. Lo que NO pasó la verificación (NO usar)
- 19 repos reportados por subagentes: TODOS HTTP 404 (agente-hq/skills, chain-protocol/skills, creative-agents/skills, langcat/skills, langchain-ai/skills, lm-sds/skills, mixtral-ai/skills, monday-cw/skills, octoai/awesome-cc-skills, photonic/skills, prefecthq/skills, radiant-ai/skills, superpowers/skills, mcp-docs/tutorial, mcp-js/sdk, mcp-python/sdk, mcp-scan/scanner, mcp-tools/registry, mcp-workflows-playwright/automation) — fabricados por alucinación.
- URLs educativas inventadas o rotas: arxiv.org (sin paper concreto), deepseek.com/docs, openai.blogs, youtube.com/AI-Education, medium.com/AI-Research.

## Relevancia para el lab (orden de interés)
1. **F — ZeroPointRepo/awesome-hermes-skills** (503⭐) y **BBridgeers/hermes-skills** (372 skills de producción) — repos específicos de Hermes Agent: el recurso más directamente accionable del inventario. Auditar qué skills portar/adaptar a las 40+ del lab.
2. **kepano/obsidian-skills** (47,8K ⭐) — el lab usa Obsidian: revisar si sus skills se pueden portar/adaptar.
3. **anthropics/skills** spec + **obra/superpowers** — patrones de autoría de skills para comparar con las 40+ del lab.
4. **modelcontextprotocol/python-sdk** + spec — si el lab construye más servidores MCP propios (hoy 3: lab-db, lancedb, animation-server).
5. **wondelai/skills** (2,1K, libros de negocio) + **clawfu-skills** (172 marketing) — ideas para futuras skills de contenido LinkedIn.
6. **punkpeye/awesome-mcp-servers** (94K) — catálogo para cuando se evalúe un MCP nuevo.
7. **tlehman/litprog-skill** (259⭐) — patrón interesante para documentar codebases del lab (concepto literate programming aplicado a skills).
