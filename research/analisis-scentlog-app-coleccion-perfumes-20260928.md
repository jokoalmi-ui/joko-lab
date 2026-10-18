---
title: "Análisis — ScentLog: aplicación de gestión de colección de perfumes (revisada y descartada, 28-sep-2026)"
type: research
---

# Análisis — ScentLog (aplicación de colección de perfumes)

**VERACIDAD:** [ALCANCE INTERNO]
**Consultado:** 2026-09-28 (07:16 CEST; fecha verificada con `date`)
**Origen:** el usuario pegó `https://www.scentlog.io/landing` la noche del 27-sep-2026.
**Encargo (Joseba):** opción «1» = comparar sus funciones contra `coleccion.db`, **solo lectura**.
**Veredicto:** **REVISADA Y DESCARTADA** como producto a adoptar. Motivo, palabras del usuario:
_«La visión de esa app es desde el vista empresarial, llevado todo a costos. De momento no quiero
llevarlo por ahí.»_ Se conserva como **referencia del nicho** y como **lista de contraste** con el
sistema propio.

---

## 1. Qué es

- Web app para gestionar una colección de perfumes: colección, muestras/decants, diario de uso,
  capas (_layering_), lista de deseos, estadísticas y asistente de IA. Gratis, acceso con cuenta de
  Google, sin tarjeta.
- Declara explícitamente que **no es un catálogo público de perfumes ni de precios**: el contenido
  lo aporta cada usuario.
- Titular: **SecureFrame Consulting, S.L.** (España), contacto `info@scentlog.io`. Privacidad y
  términos fechados **2026-05-29** → proyecto de unos cuatro meses.
- Stack declarado en su propia política: **Vercel** (alojamiento), **Supabase** (BD y autenticación,
  RLS), **Google OAuth**, **Anthropic** (asistente) y **Google Analytics 4**.
- `robots.txt`: bloquea crawlers de entrenamiento (GPTBot, ClaudeBot, Google-Extended, DeepSeekBot)
  y permite buscadores.

## 2. Fuentes primarias usadas

- `https://www.scentlog.io/landing`
- `https://www.scentlog.io/about`, `/privacy`, `/faq`, `/terms`
- `https://www.scentlog.io/robots.txt` y `/sitemap.xml` (el mapa de rutas del sitemap equivale al
  mapa de funciones del producto)
- Búsquedas: `"ScentLog" app colección perfumes diario olfativo` y `scentlog.io`

## 3. Medición propia — contraste con la base del lab (solo lectura)

BD: `/home/jokoalmi/perfume-ia/data/coleccion.db`, abierta con `?mode=ro`. Cifras medidas:

- 10 tablas · **328 perfumes** · **213 decants** (192 disponibles / 21 agotados) · 153 casas ·
  **1363** vínculos perfume–nota.
- **Diario `uso_diario`: 86 registros** del 2026-06-30 al 2026-09-27, sobre **49 perfumes**
  distintos (reparto mensual 1 / 35 / 23 / 27).
- `clima_temp` y `clima_desc` presentes en **86/86** registros → el diario con clima **ya existe**
  en el lab (corrección de una afirmación previa errónea del asistente).
- Inventario `posee`: botella 296 · decant 23 · agotado 7 · ambos 2.
- Relleno de campos clave en `perfumes`: `familia_id` 156/328 · `sensaciones` 320/328 ·
  `edad_recomendada` 320/328 · `estacionalidad` 152/328 · `longevidad_horas` 162/328 ·
  `estela` 162/328 · `genero` 164/328 · `concentracion` 180/328 · `año` 216/328 ·
  **`rating` 5/328** · **`foto_path` 5/328** · **`estado_botella` 8/328** · **`recompra` 8/328** ·
  **`precio` 1/328** · **`fecha_compra` 0/328** · `lote` 0/328.
- Otras: `reformulaciones` **0 filas** (tabla preparada y sin uso) · decants con temporada
  clasificada 213/213 (otoño 60 · primavera 51 · otoño-invierno 45 · verano 30 · invierno 16 ·
  mixtos 11) · `volumen_ml` en decants **0/213**.
- `futuribles.db` (BD aparte): 18 marcas · 5 perfumes · 3 precios.

## 4. Función por función

**Cubierto igual o mejor en el lab**: colección; decants con temporada y familia; notas
normalizadas; diario de uso **con clima**, ánimo y ocasión; lista de deseos (en `futuribles.db`);
asistente sobre la colección (motor propio del lab).

**Huecos reales medidos**: (1) nivel de frasco (`estado_botella` 8/328); (2) valoración propia
(`rating` 5/328); (3) combinaciones/capas, que no tienen tabla.

**Descartado a propósito por el usuario**: coste por frasco, coste por uso y valor económico de la
colección. No es un hueco a cubrir: es un enfoque rechazado.

## 5. Referencia del nicho

Menciones halladas al buscar el nicho (no auditadas una por una): **Fragrance - Scent Collector**
(App Store), **ScentAtlas** (GitHub, tema hijo de WordPress) y **ScentVerdict** (GitHub).

## 6. No verificado / límites

- **La empresa NO quedó verificada por fuente externa.** Una búsqueda del dominio no devolvió
  ninguna mención a `scentlog.io` (los cinco resultados apuntaban a otros proyectos del nicho) y
  una segunda búsqueda falló por error del backend. → La titularidad consta **solo según su propia
  web**.
- No se ha creado cuenta, no se han tocado rutas privadas y no se ha usado el asistente de la
  aplicación. Solo páginas públicas y `robots.txt`.
- Sin precedente en el lab: `(?i)scentlog` sobre `~/joko-lab`, `/home/jokoalmi` y las skills → 0.

## 7. Qué NO es y qué no autoriza este documento

- **No** es una adopción de producto ni una recomendación de migrar nada.
- **No** autoriza a escribir en la BD ni a tocar `aplicabilidad_ledger.jsonl` (registro
  independiente, con su propio OK).
- Cierra la línea: no volver a proponer esta aplicación salvo cambio de criterio del usuario.
