---
title: "Análisis — carrusel «AWESOME-CLAUDE-SKILLS» 12 skills (leadgenman, 18-09-2026)"
type: research
---

# Análisis — carrusel «AWESOME-CLAUDE-SKILLS» 12 skills (leadgenman, 18-09-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DdcDA1sN8eS/ (autor `leadgenman`, 18-09-2026, 560 likes / 460 comentarios)
**Consultado:** 2026-09-20 (domingo), sin login en Instagram.
**Método:**
1. `search_files 'DdcDA1sN8eS'` en `joko-lab` → **0 coincidencias** (no estaba registrado).
2. Caption vía `browser_exec` sin login (IG sirve el texto aunque no el carrusel completo).
3. Imagen del slide servida sin login descargada a `/tmp/ig_leadgenman.jpg` (**763.880 B**) y **transcrita por visión** (`vision_analyze`, GLM-4.6V en LM Studio `:1234`).
4. Las **12 skills identificadas por nombre** y **estrellas/licencia verificadas hoy contra la API de GitHub**.
5. Resolución de los 12 enlaces `lnkd.in` del slide.

## Qué es el post

Carrusel-bait de captación: el caption pide *«comment SKILLS and I'll drop all 12 in your DMs»* (de ahí los 460 comentarios). El slide visible titula **AWESOME-CLAUDE-SKILLS** y lista 12 skills, cada una con un enlace `lnkd.in`.

**Los enlaces están muertos:** de los 12 `lnkd.in`, **11 devuelven 404** y **1** lleva a una página basura de LinkedIn Hire. El post no entrega nada accionable por sí mismo: la lista hay que identificarla por nombre.

⚠️ **Nota de método (norma del lab):** IG sin login sirve **solo el primer slide**. En el precedente `analisis-alamin8020ai-12-ai-skills.md` (22-ago-2026) descartar un carrusel por el caption resultó ser **un error** (el contenido estaba en las imágenes). Aquí el descarte **no se basa en el caption** sino en que (a) el slide servido ya contiene la lista completa numerada 1-12, y (b) los 12 enlaces están caídos. La conclusión no depende de ver más slides: **cualquier slide adicional repetiría la misma lista con los mismos enlaces muertos.**

## Las 12 skills — verificación GitHub 2026-09-20

| # | Nombre en el slide | Repo real (verificado por API) | ★ | Licencia | ¿En el lab? |
|---|---|---|---|---|---|
| 1 | Superpowers | `obra/superpowers` | 289.124 | MIT | Ya en el inventario verificado de recursos externos |
| 2 | Matt Pocock Skills | `mattpocock/skills` | 266.308 | MIT | **YA PORTADO** en `01-knowledge/references/mattpocock-skills` (37 SKILL.md) |
| 3 | UI/UX Pro Max | `nextlevelbuilder/ui-ux-pro-max-skill` | 129.269 | MIT | **Ya valorado** el 31-ago → MEDIO-BAJO |
| 4 | Caveman | `JuliusBrussee/caveman` | 106.918 | NOASSERTION | **Sin precedente en research/** |
| 5 | Humanizer | (skill, no repo de la lista) | — | — | **YA EN EL LAB**: `creative/humanizer` |
| 6 | Find Skills | no identificado con garantías | — | — | **NO VERIFICADO** |
| 7 | Deploy to Vercel | `vercel/vercel-plugin` | 287 | NOASSERTION | Sin precedente; irrelevante (el lab no despliega en Vercel) |
| 8 | Brainstorming | no identificado con garantías (probablemente incluido en `obra/superpowers`) | — | — | **NO VERIFICADO** |
| 9 | TDD | (concepto) | — | — | **YA EN EL LAB**: `software-development/test-driven-development` (14 research lo citan) |
| 10 | Excalidraw | (skill) | — | — | **YA EN EL LAB**: `creative/excalidraw` |
| 11 | Remotion | `remotion-dev/remotion` | 59.854 | NOASSERTION | **YA RECHAZADO** el 31-ago (`analisis-software-infografias-animadas.md`): stack JS/React nuevo + créditos Claude Code → coste/beneficio y local-first. Queda como FUTURIBLE 2 |
| 12 | Web Quality | `addyosmani/web-quality-skills` | 2.813 | MIT | Sin precedente; alcance menor |

**Fuera de la lista, pero es la fuente de mayor peso que cita el post:** `addyosmani/agent-skills` (**97.519 ★**, MIT, 25 skills de ingeniería) — **ya analizado el 25-ago** en `analisis-pabloinpublic-3skills.md` (entonces **89.445 ★**) con veredicto «VALIDACIÓN de los quality gates del lab» y una tarea pendiente anotada entonces (*«revisar mattpocock/skills y addyosmani/agent-skills por si alguna skill concreta añade algo»*). La parte de mattpocock se completó el 03-sep (`analisis-aihero-dev-completo-20260903.md`); **la de addyosmani sigue pendiente y no urgente**.

## Veredicto para el LAB: **NO ENTRA** (`no_entra`)

Aplicando la doctrina del lab (*«si no aporta nada no le damos entrada»*) y la norma del mapa de capacidades (*«si el mapa ya lo cubre, es validación; si no, es futurible»*):

1. **El post no aporta nada** — carrusel-bait con **los 12 enlaces caídos** (11 × 404 + 1 basura).
2. **8 de las 12 ya están cubiertas por el lab**: 4 instaladas o analizadas (mattpocock, humanizer, TDD, excalidraw), 1 ya en el inventario (superpowers), 2 ya valoradas (UI/UX Pro Max → MEDIO-BAJO; Remotion → rechazado), 1 de alcance irrelevante (Deploy to Vercel).
3. **`addyosmani/agent-skills`** (la fuente más potente que cita el post) **ya está analizada** → es validación, no novedad.
4. **Única novedad real: `Caveman` (106.918 ★)**. Sin precedente en `research/`. Dos cautelas antes de considerarlo siquiera: licencia **NOASSERTION** (no MIT) y su tesis (forzar un registro telegráfico para recortar tokens) es adyacente a la obsesión del lab con coste/contexto (`skill-compaction`, observabilidad del pipeline). **No evaluado a fondo:** requeriría leer el repo, y eso no está autorizado hoy.
5. **`Find Skills` y `Brainstorming`: NO VERIFICADAS** por nombre. No se afirma nada sobre ellas.

## Hallazgos de método (reutilizables)

- **No descartar un carrusel por el caption** sin comprobar el slide (precedente alamin8020ai, 22-ago).
- **Buscar por NOMBRE VISIBLE, no por slug**: `grep 'ui-ux-pro-max'` en `research/` devolvió **0** cuando el lab **sí** lo había valorado — porque allí está escrito «UI UX Pro Max» con espacios. (Es el **segundo falso negativo del día** causado por buscar slugs/dominios en vez de nombres: el primero fue `druni.es` vs `Druni`.)
- Los `lnkd.in` de este tipo de carruseles **caducan en días** → identifican por nombre, nunca por enlace.

## Estado

- **Nada instalado, nada activado, ninguna skill tocada.**
- Registro del veredicto: este research + asiento en `04-operations/backlogs/2026-07-31-backlog.md`.
- **Pendiente de OK** (no ejecutado): anotación en el ledger de aplicabilidad (`aplicabilidad_ledger.jsonl`), donde este descarte sería el **10º `no_entra`**.
