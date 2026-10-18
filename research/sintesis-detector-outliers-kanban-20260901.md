---
title: "Detección de vídeos outlier en YouTube — Síntesis final del swarm"
type: research
---

# Detección de vídeos outlier en YouTube — Síntesis final del swarm
**VERACIDAD:** [VERIFICADO]

Synthesizer: t_0c8723e8 | Swarm root: t_cee1e159 | Fecha: 2026-09-01
Workers: t_04bc1953 (investigador-outliers, 9 búsquedas) + t_e08aff37 (investigador-alternativas, 10 búsquedas)
Verificador: t_e8d85479 — gate PASS (2 informes leídos, 15 URLs HTTP 200, empírico reproducido)

## Resumen ejecutivo

Detectar "vídeos outlier" (canal pequeño, muchas visitas) es viable con datos 100% públicos, sin API key y sin gastar cuota de Google. El lab ya tiene casi todo montado: el feed RSS que usa el monitor incluye las visitas por vídeo; solo falta el número de suscriptores del canal, que se obtiene gratis desde el HTML de la página del canal o con una llamada de 1 unidad a la API oficial.

Hallazgo clave (dato corregido por el verificador): el RSS de YouTube **sí** trae las visitas por vídeo (`<media:statistics views="N"/>`), verificado empíricamente hoy sobre el feed de Nichonauta (160, 2032, 3992, 6158, 6015, 7640...). El RSS **no** trae suscriptores. Esto hace que el MVP sea más barato de lo que parecía: las visitas salen gratis del feed ya existente.

## 1) Herramientas open source y servicios

### Open source (código disponible)

| Herramienta | Qué aporta | Cómo obtiene datos | Notas |
|---|---|---|---|
| **YT-Outlier-Finder** (github.com/benjamin-henley/YT-Outlier-Finder) | El único proyecto open source que implementa exactamente esto: detección de outliers con Isolation Forest (scikit-learn), ratio visitas/suscriptores, foco en canales <100k, export CSV | YouTube Data API | Repo con LICENSE, verificado hoy |
| **yt-dlp** (CLI, ya instalado en el lab) | Metadata sin descargar: `view_count`, `channel_follower_count`, `channel_id` | Scraping | Validado empíricamente en el lab: sobre v88cvk6fBYU devolvió 160\|20800\|UCz6Mu2Iv4-gitXurg9amisw |
| **YouTube Data API v3** | La única fuente canónica: `channels.list` y `videos.list` devuelven statistics exactos | API oficial | Gratis hasta 10.000 unidades/día; `channels.list` = 1 unidad, `search.list` = 100 |
| **Invidious** (docs.invidious.io/api) | API propia: `/api/v1/videos/:id` con `viewCount`, `/api/v1/channels/:id` con suscriptores | Scraping, sin API oficial | Autoalojable en Docker; **instancias públicas NO fiables (3/3 fallaron hoy: disabled/403/401)** |
| **Piped** (github.com/TeamPiped/Piped) | Frontend alternativo con API JSON por instancia | NewPipeExtractor | Docs inestables (en IPFS) |
| **NewPipeExtractor** (librería Java) | Librería de extracción, la base de Piped | Scraping | Integrable en herramientas propias |
| **LibreTube** (github.com/libre-tube/LibreTube) | Cliente Android que consume Invidious/Piped | vía Invidious/Piped | Útil como app, no como backend |
| **TubeArchivist** (github.com/tubearchivist/tubearchivist) | Servidor self-hosted que archiva vídeos y metadata | API oficial/scraping | Pesado para un monitor; es archivador, no detector |

### Servicios (referencia de metodología, no open source)

- **Apify "YouTube Outlier Finder"**: documenta la metodología canónica: `outlierScore = views ÷ baseline`, donde baseline = **mediana** de las visitas de los uploads recientes **excluyendo el vídeo candidato**; triple gate (piso de visitas + múltiplo outlier + tope de tamaño de canal). Definición de outlier: 5x, 20x, incluso 100x las visitas típicas del canal.
- **Viddar**: usa explícitamente el View-to-sub ratio (VSR) como métrica.
- **OverseerOS**: estudio con datos reales de benchmarks views-to-subscriber por tamaño de canal (ver sección 2).
- **Social Blade**: tracking de canales, sin API pública fiable.
- **vidIQ Outliers / YouTool Outlier Finder / Outlyr / Viewstats**: detectores comerciales del mismo concepto (referencia de mercado).
- **n8n workflow público** "Detect viral YouTube videos with AI analysis": calcula un "Algorithmic Lift Score" (visitas relativas a la base de suscriptores). Directamente aplicable al lab, que ya usa n8n.

## 2) Cómo calcular el ratio con datos públicos

### Dos métricas distintas (no mezclarlas)

**A) Ratio visitas/suscriptores del canal (salud del canal)** — NO sirve para detectar vídeos outlier.
`(media de visitas de los últimos 10-15 vídeos ÷ suscriptores) × 100`
Sirve para detectar compra de subs o audiencia fantasma. (Fuente: SoInfluential.)

**B) Outlier score por vídeo (lo que busca el lab)**
`outlierScore = visitas del vídeo ÷ baseline del canal`
donde baseline = mediana de visitas de los uploads recientes (10-15 últimos) **excluyendo el vídeo candidato**. (Fuente: Apify.)
Alternativa usada por YT-Outlier-Finder: `viral coefficient = views ÷ subscribers` del canal por vídeo.

### Datos públicos disponibles (todos verificados hoy)

| Dato | Fuente pública | Verificación |
|---|---|---|
| Visitas por vídeo | **Feed RSS** `youtube.com/feeds/videos.xml?channel_id=...` → `<media:statistics views="N"/>` | ✅ SÍ, sin API key ni cuota |
| Suscriptores del canal | HTML de la página del canal (`ytInitialData`, `subscriberCount`; método `externalId` ya usado en el lab) | ✅ método ya validado en la skill vigilancia-canales-youtube |
| Suscriptores + visitas exactas | YouTube Data API `channels.list(part=statistics)` | ✅ 1 unidad de cuota por llamada |
| Suscriptores + visitas | Invidious self-hosted `/api/v1/channels/:id` | ⚠️ docs OK, instancias públicas no fiables |
| Visitas + suscriptores en una llamada | yt-dlp `--skip-download --print "%(view_count)s\|%(channel_follower_count)s"` | ✅ validado en el lab (160\|20800) |

### Benchmarks reales para fijar umbrales (no inventados)

**Estudio OverseerOS — 2.996 vídeos breakout, 463 canales** (verificado hoy):
- 1.364 breakouts vinieron de canales <100k subs; 191 de canales <1.000 subs.
- 89,7% de los breakouts de canales sub-100k tenían MÁS visitas que suscriptores (97,4% en sub-1k).
- Mediana sub-100k: 4,95x visitas ÷ suscriptores; sub-1k: 10,95x.
- Mediana del outlier score: sub-100k = 12,89x; 1k-99,9k = 13,30x; 100k-999,9k = 21,50x; 1M+ = 20,47x. 52,9% (sub-1k) y 63,9% (1k-99,9k) superaron 10x su baseline.

**Benchmarks ratio visitas/suscriptores por franja (SoInfluential)**:
| Franja | Sano | Cautela | Bandera roja |
|---|---|---|---|
| Nano 1k-10k | 15-40%+ | 8-15% | <5% |
| Micro 10k-100k | 10-25% | 5-10% | <4% |
| Mid 100k-1M | 5-20% | 3-5% | <3% |
| Macro 1M-10M | 3-12% | 1,5-3% | <1,5% |
| Mega 10M+ | 1-8% | 0,5-1% | <0,5% |

### Limitaciones a documentar
- `subscriberCount` de la API oficial se redondea a 3 cifras significativas → distorsiona el ratio en canales muy pequeños.
- Las visitas crecen con el tiempo: conviene fijar una ventana (p. ej. ratio a las 24-72 h de publicación) o marcar el ratio con timestamp.
- Un solo vídeo outlier puede ser un pico de recomendación pasajero; los benchmarks por tamaño de canal dan contexto para elegir umbral.
- Regla comunitaria de 48h (un canal sano atrae el 15-40% de sus suscriptores en las primeras 48h) — no es cifra oficial de YouTube.

## 3) Recomendación de implementación mínima viable (local-first)

**Arquitectura: ampliar `monitor_yt.py` existente sin tocar su patrón watchdog. Cero API key, cero cuota, coste 0 €.**

```
cron diario (patrón watchdog existente)
  └─ monitor_yt.py (ya existe: RSS detecta vídeo NUEVO)
        └─ parsear <media:statistics views="N"/> del MISMO feed (gratis, verificado)
        └─ suscriptores del canal: HTML de la página (1 vez/día, método externalId ya dominado)
              └─ baseline = mediana de visitas de los últimos 10-15 vídeos, excluyendo el candidato
              └─ outlierScore = views_video ÷ baseline
              └─ métrica secundaria: views_video ÷ suscriptores_canal
              └─ si cumple umbrales → registro en state JSON + aviso Telegram (solo si hay outlier)
```

### Pasos concretos
1. **Capa de datos (ya existente)**: el RSS detecta vídeo nuevo; ahora también da las visitas parseando `media:statistics`.
2. **Añadir suscriptores (1 vez/día por canal, sin API key)**: fetch del HTML del canal con curl + User-Agent Chrome (método ya usado en el lab para `externalId`), extraer `subscriberCount` de `ytInitialData`. Alternativa: yt-dlp `--print channel_follower_count` (validado). Si algún día se quisiera API oficial: 1 llamada `channels.list` por canal = 1 unidad (100 canales = 1% de la cuota diaria).
3. **Cálculo del outlier score** (semana o mes rodante): baseline mediano por canal excluyendo el candidato (método Apify) + viral coefficient views÷subs.
4. **Umbrales iniciales a calibrar** (regla INSTRUMENTO del lab: umbrales NO a priori — arrancar con estos, ajustar con datos reales):
   - Canal con suscriptores < 100.000 (configurable) Y
   - `outlierScore ≥ 10x` (dato: mediana de breakouts sub-100k = 12,89x; 52,9-63,9% superan 10x) Y/O
   - `views_video > suscriptores_canal` (89,7% de los breakouts sub-100k cumplen esto)
   - Piso absoluto de visitas (p. ej. ≥ 1.000) para filtrar ruido.
5. **Estado y aviso**: state JSON en `~/.hermes/state/` (mismo patrón que `monitor_yt_state.json`); cron watchdog diario con silencio si no hay outliers y Telegram solo cuando aparece uno (mismo wrapper `~/.hermes/scripts/`).
6. **Futurible (fase 2, solo si hace falta)**: Isolation Forest de scikit-learn sobre el vector [views, ratio, baseline, edad del vídeo...] como YT-Outlier-Finder, cuando haya histórico propio; Invidious self-hosted en Docker si el scraping directo se vuelve frágil.

### Dónde se notará el beneficio
El monitor deja de ser "qué publicaron mis canales" y pasa a ser "qué vídeo de un canal pequeño de IA está explotando AHORA en mi nicho", sin gastar ni una unidad de cuota de Google ni una API key. Con el RSS ya en producción, el coste incremental es mínimo: parsear un atributo y una llamada diaria por canal para los suscriptores.

### Qué NO es esta solución
- No detecta tendencias globales de YouTube (funciona por lista de canales/nicho vigilados).
- No rastrea todos los canales del mundo.
- No es un sustituto de SocialBlade ni de herramientas comerciales de analítica.
- Los umbrales iniciales son orientativos; necesitan calibración con los datos reales del lab.

## Decisión del sintetizador (discrepancia resuelta)
t_04bc1953 afirmó que el RSS "NO incluye viewCount ni subscriberCount (solo título/fecha/thumbnail)" — incorrecto en las visitas. El verificador reprodujo que el RSS sí trae `media:statistics views="N"` (correcto en que no trae suscriptores). t_e08aff37 tiene el dato correcto. Consecuencia: el MVP de t_04bc1953 (yt-dlp para todo) sigue siendo válido pero no es mínimo; la vía verdaderamente mínima usa las visitas del RSS ya existente y solo añade la llamada de suscriptores.

## Fuentes verificadas (15 URLs HTTP 200 por el verificador)

1. https://developers.google.com/youtube/v3/docs/channels — YouTube Data API v3, recurso Channels (statistics; redondeo a 3 cifras significativas)
2. https://developers.google.com/youtube/v3/docs/channels/list — coste de cuota 1 unidad
3. https://developers.google.com/youtube/v3/getting-started — cuota 10.000 unidades/día, 100 search.list/día
4. https://github.com/yt-dlp/yt-dlp — yt-dlp (view_count, channel_follower_count)
5. https://github.com/benjamin-henley/YT-Outlier-Finder — Isolation Forest + ratio visitas/suscriptores + canales <100k + CSV
6. https://apify.com/datascoutlab/youtube-outlier-finder — metodología outlierScore = views ÷ baseline (mediana, excluyendo candidato), triple gate
7. https://docs.invidious.io/api/ — API de Invidious (GET /api/v1/videos/:id → viewCount; /api/v1/channels/:id → suscriptores)
8. https://github.com/iv-org/invidious — Invidious (frontend alternativo, no usa API oficial)
9. https://github.com/TeamPiped/Piped — Piped (frontend open source con API JSON)
10. https://docs.piped.video/docs/api-documentation/ — Documentación API de Piped
11. https://github.com/TeamNewPipe/NewPipeExtractor — NewPipeExtractor (librería de extracción)
12. https://github.com/tubearchivist/tubearchivist — TubeArchivist (servidor self-hosted)
13. https://www.overseeros.com/blog/can-small-youtube-channels-go-viral — estudio 2.996 vídeos / 463 canales (mediana 12,89x sub-100k; 89,7% con views > subs)
14. https://soinfluential.com/blog/youtube-views-to-subscriber-ratio-2026/ — fórmula del ratio y benchmarks por franja + regla 48h
15. https://viddar.io/en/blog/view-to-subscriber-ratio-youtube — Viddar: View-to-sub ratio (VSR)
16. https://n8n.io/workflows/8368-detect-viral-youtube-videos-with-ai-analysis-and-email-reports/ — workflow n8n "Algorithmic Lift Score"
17. https://www.youtube.com/feeds/videos.xml?channel_id=UCz6Mu2Iv4-gitXurg9amisw — feed RSS real con `<media:statistics views="N"/>` (verificación empírica)
18. https://dev.to/siyabuilt/youtubes-api-quota-is-10000-unitsday-heres-how-i-track-100k-videos-without-hitting-it-5d8h — contexto de cuota en producción
19. https://sumguy.com/invidious-piped-redlib-nitter-2026/ — estado 2026 de los frontends privados de YouTube
20. https://vidiq.com/features/outliers/ — vidIQ Outliers (referencia comercial)
21. https://www.youtool.io/tools/outlier-finder — YouTool Outlier Finder (referencia comercial)
22. https://tryoutlyr.io/ — Outlyr (referencia comercial)
