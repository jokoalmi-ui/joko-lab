---
title: "Análisis — 4 repos de GitHub para tu agente (chanti.dev, carrusel IG, 29-09-2026)"
type: research
---

# Análisis — 4 repos de GitHub para tu agente (chanti.dev, carrusel IG, 29-09-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/Dd4R1NzjChi/ (chanti.dev — «Chanti | Programación + IA», Madrid; publicado 29-09-2026 a las 19:18:24 CEST; carrusel de 6 láminas; like 3 / comment 8 con el contador desactivado por el autor)
**Método:** copia cruda del propio post (942.562 B) + las 6 láminas descargadas y transcritas una a una con visión local (6/6 OK) + API de GitHub el 29-09-2026 con DOS instrumentos coincidentes (api.github.com a las 19:46:01 y el listado completo de la organización, 88 repos)
**Registro:** asiento 18 del `aplicabilidad_ledger.jsonl` (línea 18, 2026-09-29) — veredicto `no_entra` / motivo `ya_cubierto`

## Qué dice la pieza

Tesis del carrusel: «tu agente de IA escribe código y, al cerrar la sesión, olvida todo»; la solución que propone son 4 repos de GitHub que le dan **memoria, flujo de trabajo y revisión de código**. El pie de foto cierra con un cebo de comentarios («Comenta REPOS y te envío los 4 enlaces»).

Los 4 repos, tal como los presenta cada lámina:

- **Gentle-AI** (lámina 2, «01/04 – Configurador»): «el entorno de ingeniería determinista para el agente que ya usas»; equipa Claude Code, Cursor, OpenCode, Codex, Pi y más; añade memoria persistente, skills y servidores MCP; «un binario dicta el siguiente paso válido, no el modelo»; no instala agentes, adapta los que ya tienes. Instalación propuesta: `brew install gentleman-programming/tap/gentle-ai`.
- **Gentle Shell** (lámina 3, «02/04 – Tu workspace»): agente de programación para desarrollo controlado; Organic Driven Development (ODD), subagentes que mapean/implementan/verifican, evidencia TDD, guardarraíles de revisión y barra de estado. Instalación: `npm i -g gentle-pi` → `gentle-shell`.
- **Engram** (lámina 4, «03/04 – Memoria»): memoria persistente entre sesiones; binario en Go con SQLite + FTS5, sin dependencias; se usa por MCP, API HTTP, CLI y TUI; compatible con Claude Code, OpenCode, Gemini CLI, Codex, Cursor y Windsurf. Instalación: `brew install gentleman-programming/tap/engram`.
- **GGA** (lámina 5, «04/04 – Revisión»): Gentleman Guardian Angel, revisión de código con IA agnóstica de proveedor (Claude, Gemini, Codex, OpenCode, **Ollama** y más), reglas propias desde un fichero tipo `AGENTS.md`, se ejecuta como **hook de pre-commit** sobre los ficheros del commit, núcleo en Bash puro (macOS, Linux, Windows).

## Medición de los 4 repos (API de GitHub, 29-09-2026)

| Repo | ★ | forks | lenguaje | licencia | creado | último push |
|---|---|---|---|---|---|---|
| Gentleman-Programming/gentle-ai | 7.396 | 814 | Go | MIT | 2026-02-27 | 2026-09-29 |
| Gentleman-Programming/engram | 6.933 | 712 | Go | MIT | 2026-02-16 | 2026-09-29 |
| Gentleman-Programming/gentleman-guardian-angel | 1.168 | 162 | Shell | MIT | 2025-12-12 | **2026-07-08** |
| Gentleman-Programming/gentle-shell | 1.137 | 163 | TypeScript | MIT | 2026-05-10 | 2026-09-29 |

Organización `Gentleman-Programming`: 88 repos públicos, 4.096 seguidores, creada el 2022-01-04. **Nota de precisión:** la pieza NO publica ninguna cifra (las láminas no traen números); estas estrellas son medición propia contra la API, no un dato del post.

## Cobertura medida en el lab

| Repo | ¿Hueco en el lab? | Qué lo cubre ya |
|---|---|---|
| Gentle-AI | No | Es el trabajo de Hermes: configurar el agente que ya usas + 213 skills + 4 MCP activos (`animation-server`, `lab-db`, `lancedb`, `codebase-memory`, todos `enabled: true` en `~/.hermes/config.yaml`) |
| Engram | No | `MEMORY.md`/`USER.md` + `~/.hermes/state.db` + MCP `lab-db`/`lancedb` |
| Gentle Shell | No | Delegación propia a OpenCode (`tools/opencode-local.sh`, skill `opencode`) |
| **GGA** | **Parcial** | Solo el gate de recibos (`hooks/pre-commit` + `generar_recibo.sh`) y la skill `requesting-code-review` como proceso, no un revisor IA automático sobre los ficheros del commit |

Datos de cobertura: 4 análisis previos del mismo ecosistema en `research/` (`analisis-agentes-desde-telefono-gentleman.md`, `analisis-gentleman-programming-alucinaciones-review.md`, `analisis-gentleman-programming-ventana-contexto.md`, `analisis-gentlemanprogramming-routing-fusion.md`) sobre 324 `analisis-*` (medido: `research/`, primer nivel, patrón `analisis-*`, cualquier extensión → 324 antes de este fichero y 325 con él; restringido a `.md` son 319) — el asiento 18 se escribió con los 324 previos; **0 instalado** (`command -v gentle`, `gentle-ai`, `gentle-shell`, `engram`, `gga`, `pi` → NO_INSTALADO), 0 menciones en `~/.hermes/config.yaml` y **brew NO instalado** en el host, que es el instalador de dos de las cuatro láminas.

## Veredicto

**`no_entra` / `ya_cubierto`** — la pieza aporta empaquetado, no técnica nueva: tres de los cuatro repos son la versión con marca de lo que el lab ya tiene por su cuenta, y el instalador que propone (brew) no existe en este host.

**Único hueco real — GGA (candidato a evaluar aparte, NO instalado):** revisión de código con IA en un hook de pre-commit, agnóstica de proveedor y que acepta Ollama. Es Bash puro (no necesita brew), así que es instalable sin tocar el gestor de paquetes; en contra: su último push es del 2026-07-08 (dos meses parado) y el lab no tiene hoy ningún revisor automático de ese tipo. Queda como candidato, sin instalar nada y sin registro de pendiente (si se quiere anotar, es una escritura aparte en `04-operations/backlogs/pendientes.md`).

## Transcripción literal de las 6 láminas (evidencia)

Los JPEG de `/tmp/ig_slides_Dd4R1NzjChi/` se retiran al cerrar el triaje, así que el texto extraído se conserva aquí.

**Lámina 1 — portada.** «ECOSISTEMA GENTLEMAN · GITHUB — 4 repos de GitHub que tu agente de IA necesita YA. Memoria, flujo de trabajo y revisión de código para el agente que ya usas. Gentle-AI / Gentle Shell / Engram / GGA. DESLIZA →»

**Lámina 2 — 01/04 CONFIGURADOR · Gentle-AI.** «El entorno de ingeniería determinista para el agente de IA que ya usas. Equipa a Claude Code, Cursor, OpenCode, Codex, Pi y más. Añade memoria persistente, skills y servidores MCP. Un binario dicta el siguiente paso válido, no el modelo. No instala agentes: adapta los que ya tienes. `$ brew install gentleman-programming/tap/gentle-ai`»

**Lámina 3 — 02/04 TU WORKSPACE · Gentle Shell.** «Tu agente de programación para desarrollo controlado en el workspace que tú diriges. Flujo diario con Organic Driven Development (ODD). Subagentes que mapean, implementan y verifican. Evidencia TDD y guardarraíls de revisión. Barra de estado, cambios en vivo y uso del proveedor. `$ npm i -g gentle-pi # el paquete se sigue llamando así` `$ gentle-shell`»

**Lámina 4 — 03/04 MEMORIA · Engram.** «Memoria persistente para agentes de código: tu agente ya no olvida al cerrar la sesión. Guarda decisiones, bugs resueltos y contexto entre sesiones. Binario en Go con SQLite + FTS5, sin dependencias. Se usa por MCP, API HTTP, CLI y TUI. Compatible con Claude Code, OpenCode, Gemini CLI, Codex, Cursor y Windsurf. `$ brew install gentleman-programming/tap/engram`»

**Lámina 5 — 04/04 REVISIÓN · GGA.** «Gentleman Guardian Angel: revisión de código con IA que funciona con cualquier proveedor. Revisa tu código con Claude, Gemini, Codex, OpenCode, Ollama y más. Aplica tus propias reglas desde un archivo como AGENTS.md. Se ejecuta como hook de pre-commit sobre los archivos del commit. Núcleo en Bash puro: funciona en macOS, Linux y Windows.»

**Lámina 6 — CTA.** «ÚLTIMO PASO — ¿Quieres los 4 repos? Te paso los enlaces de Gentle-AI, Gentle Shell, Engram y GGA para que los pruebes con tu agente. Comenta la palabra REPOS y te los envío. Guarda el post. Comenta REPOS.»

## Pie de foto literal

> Tu agente de IA escribe código y, al cerrar la sesión, olvida todo. Estos 4 repos de GitHub le dan memoria, un flujo de trabajo y revisión de código.
>
> Gentle-AI configura el agente que ya usas (Claude Code, Cursor, OpenCode, Codex y más). Gentle Shell es un workspace de desarrollo controlado para Pi. Engram le da memoria persistente entre sesiones. GGA revisa tu código con la IA que elijas.
>
> 🎁 Comenta REPOS y te envío los 4 enlaces. Guarda el post para probarlos en tu próximo proyecto.
>
> ¿Con qué agente de IA programas tú y cuál de los 4 probarías primero?
>
> #aitools #aiagents #agentesdeia #aicoding #aiengineering

## Cifras que NO se re-verifican

- **like 3 / comment 8**: lectura del 29-09-2026 a las 19:39 desde el navegador. El objeto del post trae `like_and_view_counts_disabled: true`, así que una segunda lectura daría otro valor o ninguno.
- **Estrellas y forks de los 4 repos**: medidas el 29-09-2026; son valores vivos y cambian a diario.
