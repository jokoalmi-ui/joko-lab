# Análisis — post @growthrockstar: «86 skills de Claude» (Dd1jGUxlMF5)

**VERACIDAD:** [ALCANCE INTERNO]
**Fecha del análisis:** 2026-10-12 09:01 CEST (medida con `date`)
**Fuente:** https://www.instagram.com/p/Dd1jGUxlMF5/ — cuenta **@growthrockstar** («GR | Crecimiento para negocios»)
**Fecha del post:** 2026-09-28T15:51:36Z = epoch `1790610696` = **28-sep-2026 17:51 CEST** (`date -d @1790610696`)
**Interacciones (og:description):** **668 likes · 1.860 comentarios**
**Formato:** carrusel de **9 slides** (9 medios únicos detectados en el JSON embebido; 9/9 descargados HTTP 200)
**Método:** caption por `og:description`; texto de cada slide por VLM local `glm-4.6v-flash` (temp 0, transcripción literal); las URLs leídas por VLM se **verificaron una a una con la GitHub API** (una URL leída no es un dato).

## Qué es

Un post-cebo: «Comentá "86" y te mandamos los enlaces de los 86 skills de Claude, listas para usar».
**El valor no está detrás del comentario: los enlaces ya están impresos en las slides.** El comentario solo alimenta el alcance (1.860 comentarios para un post de 668 likes).

Los 86 salen de 6 «equipos»: marketing (45) + redes sociales (17) + diseño (3) + legal (9) + financiero (8) + documentos (4) = **86** (aritmética comprobada).

## Los 8 recursos, verificados por API (12-oct-2026)

| # | Qué dice el post | URL impresa en la slide | Repo REAL verificado (`api.github.com`) | ★ 12-oct | Estado |
|---|---|---|---|---|---|
| 1 | Marketing, 45 skills | `coreyhaines31/marketingskills` | `coreyhaines31/marketingskills` | **54.268** | MIT · hoy `skills/` tiene **50** carpetas (el post dice 45) |
| 2 | Redes sociales, 17 skills | `charlie947/social-media-skills` | `charlie947/social-media-skills` | **4.000** | `skills/` = **17** ✓ cuadra |
| 3 | Diseño | `Leonlnx/taste-skill` | **`Leonxlnx/taste-skill`** | **94.846** | la grafía impresa da 404; el repo real es con «xlnx» |
| 4 | Diseño (frontend) | `anthropics/skills-frontend-design` | **404** → el recurso real es la skill `frontend-design` dentro de `anthropics/skills` | **180.584** (repo) | repo YA en el inventario del lab |
| 5 | Diseño (UI/UX) | `nextlevelbuilder/ui-ux-pro-max-skill` | `nextlevelbuilder/ui-ux-pro-max-skill` | **134.932** | MIT · **ya valorado en el lab el 31-ago → MEDIO-BAJO** |
| 6 | Legal, 9 skills | `anthropics/clause-for-legal` | **`anthropics/claude-for-legal`** | **9.643** | la grafía impresa da 404; repo real: 14 áreas legales |
| 7 | Financiero, 8 skills | `anthropics/financial-services` | `anthropics/financial-services` | **39.436** | 3 grupos de plugins (agent / partner-built / vertical) |
| 8 | Documentos, 4 skills (Word/PDF/PPT/Excel) | `anthropics/skills` | `anthropics/skills` | **180.584** | `skills/` = 19, incluye `docx`, `pdf`, `pptx`, `xlsx` **✓ cuadra** |

**Dos de las URLs impresas no existen** (`skills-frontend-design`, `clause-for-legal`): el VLM las leyó literalmente, la API devolvió 404 y el repositorio real se localizó por búsqueda + descripción coincidente. Lección: **toda URL leída por VLM se cierra con `curl api.github.com`** antes de darla por buena.

## Veredicto

**ANALIZADO — novedad parcial.** De los 8 recursos:
- **3 ya conocidos por el lab**: `anthropics/skills` (inventario 04-sep), `ui-ux-pro-max-skill` (valorado 31-ago → MEDIO-BAJO), y la vía «.pptx solo si hay que entregar a terceros» ya decidida en `analisis-mcp-presentaciones-animaciones.md`.
- **5 sin precedente** en `research/` + backlog (búsqueda por nombre visible ✅ + slug ❌): **marketingskills** (★54,3k, MIT), **social-media-skills** (★4,0k, 17 skills), **taste-skill** (★94,8k), **claude-for-legal** (★9,6k) y **financial-services** (★39,4k).
- **Cifras del post: cuadran en el total (86) pero no una a una** — marketingskills declara 45 y hoy tiene 50 carpetas; legal «9 skills» no se corresponde con la estructura actual (14 plugins legales). Es un post de hace 2 semanas y los repos crecen rápido.

## Lo que NO es
- NO es contenido propio del autor: es un **directorio con enlaces** a repos de terceros (uno de ellos, `charlie947/social-media-skills`, con ~350k seguidores/100M vistas atribuidos sin verificar).
- NO es «86 skills listas para usar» en el lab: son colecciones para Claude Code / plugins de Cowork (varias dependen de Gemini o de la nube), no todo es portable ni local-first.
- NO aporta técnica nueva: no hay método, ni medición, ni código; aporta **catálogo**.

## Encaje real con el lab
- **`social-media-skills`** (17: `hook-generator`, `content-matrix`, `niche-research`, `gemini-carousel`, `gemini-infographic`, `graphic-designer`…) es lo más cercano a la serie LinkedIn/IG del lab, pero su parte «carousel/infographic» es **Gemini (nube)** → el lab ya cubre eso en local con `linkedin-carrusel-lab` + `infografia-html`.
- **`marketingskills`** (50: ads, copy, SEO, analytics, CRO) es el hueco de contenido que el lab NO tiene (marca de empleo), y es MIT.
- **`taste-skill`** (★94,8k, «que tu IA no genere slop genérico») toca el eje de diseño de las infografías HTML del lab.
- Legal/financiero (plugins oficiales Anthropic para Cowork) = bajo encaje (el lab toca finanzas personales, no workflows legales).

## Estado del lab devuelto
VLM `glm-4.6v-flash` usado para las slides y **descargado al terminar** (`lms unload glm-4.6v-flash`). `nvidia-smi` POST: **3.565 / 12.282 MiB, 3 %**. LM Studio `:1234` sin modelos cargados. Nada más tocado (n8n y `/mnt/ssd_ia_datos` intactos).
