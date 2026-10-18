---
title: "Análisis — Post askgpts: \"Web Scraping Is Dead\" (17-ago-2026)"
type: research
---

# Análisis — Post askgpts: "Web Scraping Is Dead" (17-ago-2026)

**Fuente:** https://www.instagram.com/p/DbbaqhpE7rx/ (askgpts, imagen única 1440×1800)
**Método:** browser_get_images → descarga webp SIN efg (nuevo enfoque anti-pitfall 13 — el CDN lo tolera) → browser_vision
**VERACIDAD:** [VERIFICADO]

## CONTENIDO (lo que dice)

### "WEB SCRAPING IS DEAD — This Open-Source AI Reads Websites Like Humans Do"

Propuesta: en vez de parsear HTML (scraping clásico), la herramienta **ve** la
página renderizada como un humano.

Componentes del pipeline visual (etiquetados en la infografía):
- **Rendered Webpage** — la página renderizada (no el HTML crudo)
- **Screenshot Tiles** — la página troceada en tiles de captura
- **Visual Embeddings** — embeddings de esas capturas
- **Visual Retrieval** — recuperación visual
- **Vision Language Model** — el modelo (tipo GLM-4.6v) interpreta

Demo: navegador mostrando "Avocado Telescope" (página con gráficos + imagen
de satélite) → el modelo la lee visualmente.

## 🎯 APLICACIÓN AL LAB — INTERESANTE (alternativa al scraping clásico)

| Enfoque | Estado en el lab | Valor |
|---|---|---|
| **Scraping clásico** (parsear HTML) | ✅ El lab lo usa (Instagram vía browser, APIs, curl) | Funciona hoy |
| **Scraping visual** (ver la página renderizada) | 🟡 El lab YA tiene las piezas: browser + GLM-4.6v (vision) + embeddings | **Futurible ligero**: pipeline "ver la web" en vez de "parsearla" |

**Matiz importante**: el lab ya hace algo PARECIDO sin nombrarlo — el pipeline
de IG analiza screenshots con GLM vision (browser_vision sobre file://), y
browser_get_images extrae del DOM renderizado. La diferencia es que esta
herramienta **trocea la página en tiles** y hace retrieval visual — útil para
webs dinámicas (JS) donde el HTML no basta.

**Para qué NO sirve en el lab**: el scraping clásico (API de Nasdaq, curl de
JSON) es más rápido y barato para datos estructurados — la visión solo aporta
en webs complejas/renderizadas. Regla: datos estructurados → API/HTML;
webs visuales → visión.

## FORMATO (aislable)

- Infografía: mockup de navegador + pipeline de componentes etiquetados
- Estructura "claim fuerte (Web Scraping Is Dead) + demo visual" — patrón
  de marketing técnico reutilizable

## Veredicto
**INTERESANTE / FUTURIBLE LIGERO.** La propuesta (leer webs con visión en vez
de parsear HTML) es real y el lab tiene las piezas (browser + GLM-4.6v +
embeddings). Pero NO sustituye al scraping clásico para datos estructurados
(Nasdaq, APIs JSON) — es complementario para webs renderizadas con JS. El
claim "Web Scraping Is Dead" es exagerado (marketing): el scraping sigue vivo
para datos estructurados. Futurible ligero con señal: cuando el lab necesite
extraer datos de webs dinámicas donde el HTML no basta.
**Nota proceso**: primer uso del enfoque "URL sin efg" — descarga OK (59 KB)
sin reparos ni chunks; queda como método preferido anti-pitfall 13.
