---
title: "Análisis — Post @gbmplus_ (GBM): «Las empresas con mejores rendimientos por año en el S&P 500» (13-oct-2026)"
type: research
---

# Análisis — Post @gbmplus_: líderes anuales del S&P 500

**Fuente:** https://www.instagram.com/p/DecFzQxDlnn/ (shortcode `DecFzQxDlnn`)
**Autor:** @gbmplus_ (GBM — casa de bolsa mexicana) — canal **NO vigilado**
**Fecha del post:** 13-oct-2026 · **Métricas:** 212 me gusta / 0 comentarios (`og:description`)
**Formato:** **UNA sola imagen** (póster-tabla), 1440×1920, 425.459 B, `no video in this post` (yt-dlp) → no es carrusel ni reel
**Método:** navegador → `og:title`/`og:description` → URL del CDN del `<img>` mayor (`naturalWidth`) → `curl` con UA de navegador (sin él, 403) → lectura con **GLM-4.6V-Flash en LM Studio (:1234)**, ctx 16384, 40,9 s
**VERACIDAD:** [VERIFICADO en las filas contrastadas · cifra de 2026 = claim no reproducible]

## CONTENIDO (transcripción literal del póster)

Título: **«Las empresas con mejores rendimientos por año en el S&P 500»**

| Año | Empresa (ticker) | Rendimiento |
|---|---|---|
| 2026* | Sandisk (SNDK) | → 555% |
| 2025 | Western Digital (WDC) | → 283% |
| 2024 | Palantir (PLTR) | → 340% |
| 2023 | NVIDIA (NVDA) | → 239% |
| 2022 | Occidental Petroleum (OXY) | → 119% |
| 2021 | Devon Energy (DVN) | → 194% |
| 2020 | Tesla (TSLA) | → 743% |
| 2019 | AMD (AMD) | → 148% |
| 2018 | AMD (AMD) | → 81% |
| 2017 | NRG Energy (NRG) | → 132% |
| 2016 | NVIDIA (NVDA) | → 224% |

\*2026: acumulado desde el inicio del año hasta septiembre; el resto, año completo.
Pie del póster: **Fuente: S&P Capital IQ**. Sin CTA y sin marca de agua.

## CRUCE CON EL LAB (solo lectura)

- **PIEZA:** `grep -rl 'DecFzQxDlnn' ~/joko-lab` → **0**. También `gbmplus` → 0. La pieza es nueva y el canal no está vigilado.
- **TEMA:** el lab **no** tiene analizado el «líder anual del S&P 500». Sí tiene dominio bolsa propio: `research/analisis-decode-swingtrading.md`, `research/analisis-decode-leccion5-bolsa-20260907.md`, EXP-002 `bolsa-autonoma`. Ninguno contiene esta tabla.

## VERIFICACIÓN (contraste con fuentes, no con memoria)

| Fila del póster | Contraste | Resultado |
|---|---|---|
| 2025 WDC +283% | Schaeffer's 06-ene-2026 «S&P 500's Top Stock of 2025: Western Digital»; Barron's; investing.com (282%) | **Verificado** |
| 2026 SNDK líder | TIKR («el mejor desempeñante en todo el S&P 500 en 2026»); Bloomberg Línea («el mejor desempeño entre las compañías que integran el S&P 500») | **Liderazgo verificado** |
| 2026 +555% (cifra) | 632,96% total return 01-ene→30-sep (Exa); 498,64% (bitfinanzas); 390,66% (Bloomberg, fecha posterior); ~695% (Motley Fool, otro periodo) | **Claim no reproducible**: depende de fecha de corte y de precio vs total return |
| 2020 TSLA +743% | CNBC/FactSet: +743,1% price return 2020 | **Verificado, con matiz**: Tesla **entró en el índice el 21-dic-2020**; el retorno se ganó mayoritariamente fuera del índice |
| 2023 NVDA +239% · 2016 NVDA +224% · 2019 AMD +148% · 2018 AMD ~80% · 2022 OXY ~117% · 2024 PLTR +340% | Tabla histórica Motley Fool (23-nov-2024) y StatMuse | **Coinciden** |
| 2017 NRG +132% | Motley Fool dice **Align Technology +131%** | **Discrepancia entre fuentes** (~1 punto; base precio/total return) |
| 2021 DVN +194% | Motley Fool dice **+179%** | **Diferencia de base** |

## VEREDICTO: **SIN ENTRADA**

Póster divulgativo: un dato (tabla) con fuente citada, **sin técnica, sin método y sin recurso instalable**. No hay nada medible que el lab pueda adoptar. La tabla, además, es correcta en líneas generales pero con las salvedades de base anteriores, así que **no sirve como fuente** (la fuente real sería S&P Capital IQ o un proveedor de datos del propio lab).

**Señal lateral (no urgente):** la rotación WDC (2025) → su escisión **SanDisk** (2026) es un caso de *momentum* de un mismo vector (memoria NAND/almacenamiento para IA) dos años seguidos; encaja como **dataset de referencia** en el dominio bolsa del lab, nunca como estrategia (RULE-013/015: sin recomendación y sin umbrales a priori).

## Estado del lab tras el análisis

- VLM **cargado y descargado**: VRAM 1425 → 9425 → **1402 MiB**; `lms ps` → «No models are currently loaded».
- Nada más tocado: ni el repo, ni cron, ni servicios. Fichero de análisis nuevo (aditivo).
