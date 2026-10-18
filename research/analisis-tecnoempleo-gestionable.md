---
title: "Análisis — ¿Es Tecnoempleo.com gestionable desde el LAB? (25-ago-2026)"
type: research
---

# Análisis — ¿Es Tecnoempleo.com gestionable desde el LAB? (25-ago-2026)
**VERACIDAD:** [VERIFICADO]

**Pregunta:** ¿Tecnoempleo.com es gestionable desde LAB? (conecta con cron `scan-empleo` pausado y meta empleo: LinkedIn Lab, TFM, HAZILAN+ 21/09, BBK 05/10)
**Método:** verificación técnica en vivo (curl, robots.txt, RSS) — lección Wallapop aplicada: NO prometer sin verificar.

## ✅ VEREDICTO: SÍ — VÍA RSS (verificado con salida real)

### Evidencia en vivo (25-ago 16:35)

1. **robots.txt** → HTTP 200, 953 bytes. Permite scraping genérico (`User-agent: *`), solo bloquea áreas internas (imágenes, políticas, ajax, matomo) y **bots de Anthropic/Claude** (`Disallow: /` para AnthropicBot, Claude, ClaudeBot, anthropic-ai). Nada que impida un cron del lab.

2. **RSS de ofertas** → HTTP 200 · **294.578 bytes · 80 ofertas** · actualizado hoy 12:51 UTC:
   - `https://www.tecnoempleo.com/alertas-empleo-rss.php`
   - Formato RSS 2.0 estándar, `pubDate` por oferta (80 únicos).
   - Datos por oferta: **título, empresa, provincia, descripción (primeros ~200 chars), link directo**.

3. **Ejemplos reales de hoy** (25-ago):
   - Android SDK Developer — Arelance (híbrido)
   - Coordinador/a equipo Data & BI — LÃBERIT (híbrido)
   - Auditor/a técnico de seguridad y procesos — LÃBERIT (ENS/RGPD)
   - 4G/5G Core Network DB Operator — T-Systems
   - Full Stack Developer Java/Python-Angular — T-Systems
   - Administrador/a SIEM SPLUNK — T-Systems (SOAR/Python)
   - T&T Project Manager — Grupo Digital
   - Senior Staff Communications Systems Eng — Michael Page (DSP/MATLAB/C)

4. **Sin Cloudflare**: las peticiones curl simples responden 200 (no hay "Just a moment" ni cf-browser).

### Limitaciones verificadas

- ❌ **Filtro por URL NO existe**: `?q=java`, `?palabra=python` → 301 al RSS base (siempre las mismas 80 ofertas). **El filtrado debe hacerse LOCAL** con Python (título/descripción/empresa) — exactamente lo que hace el lab.
- ⚠️ **Página individual de oferta → HTTP 410 Gone con curl** (incluso con User-Agent de navegador completo): el detalle completo de cada oferta NO es scrapeable sin sesión/JS. Pero el RSS ya trae título + empresa + provincia + descripción + link — suficiente para **alertas de calidad**.
- ⚠️ 80 ofertas por fetch — probablemente las más recientes (snapshot).

## 🔴 Aplicación al LAB — VIABLE PARA EL CRON scan-empleo

| Capacidad | Estado |
|---|---|
| **Fuente de ofertas TI real** | ✅ RSS 80 ofertas/día, actualizado (hoy 12:51) |
| **Filtrado por perfil** | ✅ Local con Python: "IA", "Data", "seguridad", "Python", provincia, empresa |
| **Alertas Telegram** | ✅ Vía cron Hermes (como PRECIOS-IA lun09/10 TG) |
| **Dedupe entre días** | ✅ BD SQLite o lista de links vistos (patrón vigilar-canales-ig) |
| **Sin login** | ✅ RSS público sin sesión |

**Señal de activación**: cuando el usuario quiera reactivar `scan-empleo` (pausado OFF). El RSS de Tecnoempleo sería la fuente ① (oferta TI España real); se puede combinar con otras fuentes.

**Coste**: 0 € — el cron solo hace curl + parse + filtro Python local (sin LLM o con gpt-oss para resumen si se quiere).

## Conclusión
**SÍ es gestionable desde el LAB** — vía RSS (verificado: 200, 80 ofertas, datos completos de cabecera). El detalle de la oferta individual no es scrapeable (410), pero para el objetivo (alertas de ofertas que encajan con el perfil → Telegram) el RSS es suficiente. La lección de Wallapop aplica solo al detalle: verificado antes de prometer.
