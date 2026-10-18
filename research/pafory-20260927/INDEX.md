---
title: "Evidencia en crudo — investigación Pafory (27-sep-2026)"
type: research
---

# Evidencia en crudo — investigación Pafory (27-sep-2026)

**VERACIDAD:** [VERIFICADO]
**Origen:** copia de `/tmp/pafory/` (directorio temporal, se borra al reiniciar) el 27-sep-2026.
**Informe que interpreta esta evidencia:** `research/pafory-colaboradores-publicidad-20260927.md`
**Carpeta:** `research/pafory-20260927/evidencia/` — 84 ficheros, 2,73 MB.

## Cómo se obtuvo (método)

1. `robots.txt` y `sitemap.xml` de `pafory.com` con UA de navegador → `sitemap-0.xml` (25 URLs).
2. API REST pública de su WordPress (`/wp-json/wp/v2/…`): `pages`, `landingpage`, `influencer` y sondeo
   de otros `rest_base` (`rest_*.json`, 404 = no existe).
3. Sondeo HTTP uno a uno (`probe.py`, `probe2.py`) de slugs de creador candidatos en `/de/` y `/es/`
   para separar páginas activas de inexistentes.
4. Bibliotecas públicas de anuncios: Meta Ad Library (DE y ES), Google Ads Transparency (región ES,
   anunciante YUNIQU GmbH), TikTok Ad Library (control fallido → sin conclusión).
5. `yt-dlp` sobre búsquedas y canales: títulos, descripciones, códigos y métricas de los vídeos de los
   colaboradores.

## Ficheros clave (los que sostienen las afirmaciones del informe)

| Fichero | Qué contiene |
|---|---|
| `probe_out.txt` | Las **10 páginas de creador activas** con su `influencer-promo-code` |
| `lp_list.txt`, `lp_full.json`, `lp.json` | Las **29 landings antiguas** (2024) con estado y fecha |
| `yt_all.txt`, `yt_channels.txt`, `yt_search.txt` | **143 vídeos** sobre Pafory y canales que los publican |
| `yt_views.txt`, `yt_stats.txt` | Vistas/likes/comentarios de los vídeos del calendario 2026 |
| `yt_code_lines.txt`, `yt_codes.txt`, `yt_desc.txt` | Códigos de creador y menciones de pago en descripciones |
| `yuniqu.txt`, `partner_txt.txt`, `partner_es.html` | Programa de embajadores (Paforysta) y programa de socios |
| `infludeals_text.txt`, `infludeals_codes.txt` | Agregador de códigos (usado solo como pista, con reservas) |
| `es_home.txt`, `leni.txt`, `lp_list.txt` | Textos de la web ES, página de una creadora, listado de landings |
| `rest_*.json`, `wp_*.json`, `wp_restbases.txt` | Rutas y respuestas de la REST API del CMS |
| `imgs.txt`, `api_candidates.txt`, `cms_hints.txt` | Rastreo técnico del CMS y de sus assets |
| `tt_fol.txt`, `tt_stats.txt`, `tt.txt`, `ig.html` | TikTok (@pafory) e Instagram: recuentos y volcados |
| `html-crudo-20260927.tar.gz` | Volcados HTML completos (2,4 MB): `pafory.com` ES/DE, páginas de creador, Instagram, `__NEXT_DATA__` |

Los ficheros de 0 bytes son **resultados negativos** (consultas que no devolvieron nada); se conservan a
propósito porque documentan qué NO hay.

## Límites de esta evidencia (no confundir con hallazgos)

- Los **importes de gasto publicitario** no son públicos: no están en la evidencia ni en el informe.
- Los **seguidores** de sus cuentas no son verificables sin sesión: no se afirman.
- **Anuncios de TikTok**: el control de la biblioteca falló ese día; queda sin conclusión.
- Datos de **terceros** (nº de empleados, facturación) proceden de agregadores y **no se han verificado**.
- `server-sitemap.xml` devolvió **error 504**; se trabajó con `sitemap-0.xml`.

## Reutilización

Para volver a comprobar cualquier dato hoy: repetir el paso 2 (REST API) y el paso 4 (bibliotecas de
anuncios). El CMS y las campañas cambian: un dato de esta carpeta vale como «foto del 27-sep-2026»,
no como estado permanente.
