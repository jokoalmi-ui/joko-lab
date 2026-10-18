---
title: "Investigación — Colaboradores de Pafory y publicidad en redes sociales (27-sep-2026)"
type: research
---

# Investigación — Colaboradores de Pafory y publicidad en redes sociales

**VERACIDAD:** [ALCANCE INTERNO]
**Consultado:** 2026-09-27 (todos los datos se comprobaron el mismo día)
**Encargo (Joseba):** «investigación sobre colaboradores de Pafory y publicidad en redes sociales»,
cruzando perfumería + informática/marketing.

**Fuentes primarias usadas:**
- Web de Pafory (DE/ES) y su CMS: `pafory.com/es/partner-program`, `pafory.com/brand-ambassador`,
  `pafory.com/es/`, `pafory.com/blog-2/`, API REST pública `/wp-json/wp/v2/` (WordPress).
- Bibliotecas públicas de anuncios: Meta Ad Library (país DE y ES), Google Ads Transparency
  (región ES, dominio pafory.com), TikTok Ad Library (no fiable hoy, ver §6).
- Vídeos/descripciones de los propios colaboradores (YouTube y TikTok) vía `yt-dlp`.
- Agregadores de códigos (infludeals) — usados solo como pista, con reservas (§7).

---

## Resumen ejecutivo

1. **Pafory = YUNIQU GmbH (Stuttgart)**, suscripción de perfume: 1 fragancia nueva al mes de 8 ml,
   +600 perfumes de nicho y lujo, 19 €/mes (primer mes 9,50 €), envío gratis, 4,6★ con 1.800+ reseñas.
   Tienda y páginas de creador **localizadas al español**.
2. **No tiene un solo programa de colaboradores: tiene cuatro vías solapadas** (afiliados Awin,
   embajadores «Paforysta», página+código por creador, y un anuncio de reclutamiento de creadores).
3. **Los colaboradores son mayoritariamente micro/nano creadores alemanes de belleza**, con un
   subgrupo muy concreto: **reseñadores profesionales de calendarios de adviento**, que el mismo mes
   reseñan Rituals, Sephora, Lookfantastic y Pafory.
4. **Su propia publicidad es poca y muy concentrada**: ~25 anuncios de Meta activos en Alemania
   (casi todos empujando el calendario de adviento y varias creatividades idénticas creadas el 25-sep)
   y **0 anuncios de Meta en España**; en Google sí hay anuncios visibles en ES bajo el anunciante
   **YUNIQU GmbH**.
5. **Lo aprovechable es la capa de operaciones**, no el contenido: código de creador + UTMs
   normalizados + landing por creador + variantes de anuncio + informes. Es exactamente lo que el
   pipeline de Joko Lab ya hace (HTML→PNG determinista).
6. **Hueco medible:** Pafory traduce su web y sus páginas de creador al español y tiene el programa de
   afiliados en español, pero **no compra Meta en España** y su red de creadores ES es mínima
   (4 nombres encontrados). Ese es el espacio real para servicios de marketing/automatización.

---

## 1. Qué es Pafory (dato de su web)

- Empresa: **YUNIQU GmbH** (el anunciante verificado de Google es «YUNIQU GmbH», HQ Alemania;
  el portal de empleo es `pafory.jobs.personio.de`, Personio, sede Stuttgart).
- Modelo: suscripción mensual de perfume («Parfüm Abo») — **1 fragancia nueva al mes**, formato 8 ml,
  **+600 fragancias** de marcas de nicho y lujo, «solo originales, sin dupes»,
  «colaboramos con marcas líderes del segmento nicho y de lujo».
- Precio (ES): **19,00 €/mes, primer mes 9,50 €**, envío gratis, estuche de viaje gratis como gancho.
- Prueba social que exhiben: **4,6★ · 1.800+ reseñas**.
- Producto estrella de temporada: **calendario de adviento 99 €** — 24 fragancias de 2 ml (24 marcas),
  revista de 100 páginas con tiras olfativas, 6 vales de 50 €, valor declarado >500 €.
- Su web es **WordPress** con REST API pública (`/wp-json/wp/v2/`): se pueden enumerar sus páginas
  (incluidas las de creador) sin scraping sucio.

## 2. Cómo consiguen colaboradores — cuatro vías

### 2.1 Programa de afiliados (Awin) — `pafory.com/es/partner-program`
- Comisión: **22 € / 7%**, «nuevo miembro – compra única», **cookie 30 días**.
- Plataforma: **Awin**; programa **PAFORY DE, ID 21284**.
- Hay versión de la página **en español** → reclutan afiliados hispanohablantes.

### 2.2 Paforysta (Brand Ambassador) — `pafory.com/brand-ambassador`
- «**Verdiene bis zu 10 € Provision pro Verkauf**» (hasta 10 € por venta).
- «**Jeden Monat erhältst Du eine Box zum Testen**» (box mensual gratis para testar).
- Promete «Auftritt in unserem Blog» y —textual— **«mehr Sichtbarkeit über unsere Marketingkanäle»**
  (más visibilidad en sus canales de marketing) para los que rinden.
- Dicen expresamente que **no hace falta ser influencer** y que revisan todas las candidaturas.

### 2.3 Página propia por creador + código personal
- Cada colaborador tiene una **landing propia dentro de pafory.com** con su nombre, su código y una
  **selección curada de fragancias** («Duftauswahl»).
- Las páginas existen en **DE y ES** (verificado página por página).
- Patrón del código: **nombre + descuento** (`LENI55` = 55%, `SWANA60` = 60%, `KATHRIN10` = 10 €).

### 2.4 Anuncio pagado para reclutar creadores (Meta, desde 4-ago-2026)
- Creatividad de la página Pafory dirigida a creadores: buscan **nano y micro creators**,
  ofrecen entrar en su **Creator Pool**, **acuerdos de afiliación** y piden enviar
  Reel / TikTok / Story como candidatura.
- Es decir: no esperan a que lleguen; **pagan publicidad para captar creadores**.

## 3. Colaboradores reales (listados con evidencia)

### 3.1 Páginas de creador activas hoy (10, en DE y en ES)
Extraídas de su propio CMS (campo `influencer-promo-code`, estado «aktiv»):

| Creador | Código |
|---|---|
| Leni's Scents | `LENI55` |
| Max Aoud | `MAXAOUD55` |
| Meloshmusc | `MELO55` |
| Lubella | `LUBELLA55` |
| Yvonne | `YVONNE55` |
| Tamara | `TAMARA55` |
| Miriam | `MIRIAM55` |
| Frühstück in der Parfümerie (Swana) | `SWANA60` |
| Nico | `NICO55` |
| Erika | `ERIKA55` |

### 3.2 Catálogo antiguo (29 landings, mayoría de 2024)
Perfume of Max, Jasmin, Xenia, Thomas (*selectthescent*), Buon Profumo, Angelina, Davisa,
Mina (*minambery*), Luigi, Hanan, Peter (*olfactory-ambition*), Swana, Franka, Jamina, Juse Beauty,
NIIA, *Addictedtomakeup*, Max Aoud, Delara (*insporia*), Niklas Steenfatt, *Swana*, y páginas de
campaña (*Dupes & Fakes*, *Taboola 1*, *Neues Parfum jeden Monat*).
**Ojo:** son de 2024; no mezclar con las 10 activas.

### 3.3 Colaboradores en YouTube (143 vídeos indexados sobre Pafory)
Nº de vídeos por canal: PAFORY (canal propio, 24) · Schikitas Place (14) · Claudis Welt (14) ·
Franka's Favorites (12) · Frühstück in der Parfümerie (10) · Greyteful Quadra (8, francés) ·
The Tays (6) · Jennys Highlights (6) · jaykup makeup (4) · echtKATHRIN (3) · Rosa87lie (3) ·
Fraganceando (3, español) · Parfum met Katja (2, neerlandés) · Kai Porten (2) · Max Aoud (2) ·
y one-offs (My Scent Bouquet EN, Olivia et ses parfums FR, Estelle Parler Parfums FR,
Esther In Wonderland, Dianina XL, Schnäppchengestöber…).

### 3.4 Códigos cazados en los propios vídeos/descripciones
`KATHRIN10` · `CLAUDI10` · `FRANKA10` · `Angelina10` · `LENI55` · `SCHIKITA60` /
`Schikitasplace10` · `SSIKI55` · `FRAGANCEANDO` (55% en el primer mes).

### 3.5 Colaboradores en español (los relevantes para el hueco ES)
- **Fraganceando** (YouTube ES): «55% en el primer mes de suscripción a Pafory: FRAGANCEANDO».
- **Ssiki VaneSsiki (Vanesa Sánchez)**: «PERSEUS PARFUMS DE MARLY, LO PRUEBO CON PAFORY.
  SSIKI55 PARA UN 55% DESCUENTO…».
- **Anto Parfums**: «🚨 CALENDARIO DE ADVIENTO DE PAFORY 🚨 ¿Merece la pena?».
- **Los perfumes de Silvia**: «Colaboración @pafory 💕 PRIMERAS IMPRESIONES…».

### 3.6 Colaboradores B2B (marcas)
- El calendario se vende como «**24 marcas detrás de 24 puertas**».
- En sus selecciones curadas aparecen **Ojar, Memoize London, Les Soeurs de Noé, Olfactive Studio**;
  en sus anuncios, **Maison Micallef**.

### 3.7 ¿Hay dinero o solo producto?
- Hay vídeos que declaran «**bezahlte Kooperation mit Pafory**» (colaboración pagada) y
  agradecimientos por «**patrocinar** este vídeo».
- **No hay cifras públicas** de cuánto pagan por campaña.

## 4. Publicidad en redes — medido el 27-sep-2026

### 4.1 Meta (Facebook/Instagram)
- **Alemania:** ~**25 anuncios activos**. La mayoría son de la **página «Pafory»** empujando el
  **calendario de adviento** (99 €). Detalle fino: una **ola de ~13 creatividades prácticamente
  idénticas creadas el 25-sep** (mismo texto/imagen repetido) → están haciendo test de variantes.
  Además: 1 anuncio de **reclutamiento de creadores** (activo desde 4-ago-2026) y
  **1 anuncio de creador**: «**angelina.patchouli con Pafory**» (21-sep-2026) con su código
  (es decir, usan *partnership ads*, anuncios con la cuenta del creador).
- **España: 0 anuncios.** Control ejecutado con la palabra «perfume» en ES (≈9.000 resultados) para
  descartar falso negativo: la búsqueda funciona, simplemente Pafory no pauta en ES.

### 4.2 Google
- **Anunciante verificado: YUNIQU GmbH** (HQ Alemania), **14 anuncios** visibles con región España.
- Para el dominio `pafory.com` en ES aparecen **17 anuncios** (incluye **terceros que pujan por su
  marca**).
- **Relación Pafory ↔ YUNIQU**: aparece YUNIQU como anunciante del dominio de Pafory y la dirección
  de la empresa coincide con la sede alemana; **no se ha encontrado documento societario que lo
  declare formalmente** → se afirma solo como «anunciante del dominio», no como «propietaria».

### 4.3 TikTok
- **No verificable hoy.** La biblioteca pública de anuncios de TikTok devolvió **0 resultados incluso
  con un control conocido** («glossybox») → el instrumento no era fiable en el momento de la consulta.
  No se emite ninguna conclusión sobre anuncios de TikTok de Pafory.

### 4.4 Orgánico propio
- **TikTok @pafory**: **466 vídeos** indexados; los **últimos 15** (19-ago a 25-sep-2026) tienen entre
  **345 y 3.818 visualizaciones**. Alcance propio pequeño: su estrategia no es su cuenta, son los
  creadores.
- Instagram: existe cuenta oficial, pero **el contador de seguidores no es verificable sin sesión**.

### 4.5 Lo que sí mueve la aguja: el alcance de los creadores (calendario 2026)
- Claudis Welt: **18.259 vistas · 602 likes · 165 comentarios** (15-sep-2026).
- Schikitas Place: **10.411 vistas · 404 likes** (15-sep-2026).
- Franka's Favorites: **7.235 vistas · 230 likes · 105 comentarios** (15-sep-2026).
- Frühstück in der Parfümerie: **2.686 vistas** (25-sep-2026).
- Contexto: **los mismos canales** reseñan el mismo mes **Rituals (51 mil), Sephora (35 mil),
  Lookfantastic (18 mil)**. Son reseñadores profesionales de calendarios: la marca compite por su
  hueco en su parrilla, no por un favor.

### 4.6 Arquitectura de trazabilidad (lo más reutilizable)
Link real de un creador:

```
pafory.com/advent-calendars?creator=Claudi10
  &utm_source=claudiswelt
  &utm_medium=influencer
  &utm_campaign=09-26_cold_ac-advent26
  &utm_content=story
```

Lectura: **parámetro propio `creator=`** + UTM con convención
`mes-año_{cold|retargeting}_ac-{campaña}` + formato en `utm_content` (`story`, etc.).
Es un sistema pensado para **atribuir ventas anuncio a anuncio y creador a creador**.

### 4.7 Herramientas que usan
- **Awin** (con enlaces acortados `tidd.ly`) para el affiliate.
- **bit.ly** para enlaces de campaña.
- **Landing propia por creador** dentro de su WordPress.
- **Personio** para el ATS de empleo.

### 4.8 Empleo: están profesionalizando esta función
- **5 vacantes** en Stuttgart, **4 de marketing**, incluida «**Influencer und Creator Management**»
  (jornada completa/parcial) y una **beca del mismo campo**
  (`pafory.jobs.personio.de`).

## 5. Lectura para Joseba (perfumería + informática/marketing)

- **El oficio está en la capa de operaciones**, no en el contenido: dar de alta creadores, generar su
  **página + código**, normalizar **UTMs**, sacar **variantes de anuncio**, medir por creador y emitir
  **informes**. Todo eso es determinista y automatizable.
- **Encaje directo con lo ya construido:** el pipeline HTML→PNG de Joko Lab (ficha del perfume del día)
  puede producir *página de creador + pack de anuncios + panel de resultados* en horas. Es el mismo
  problema técnico que ya está resuelto en el lab.
- **Hueco ES medible:** la marca localiza su web, sus landings de creador y su programa de afiliados al
  español, **pero no compra Meta en España** y su red de creadores ES son 4 nombres. O no tienen la
  operación ES montada o es mínima: eso es exactamente lo que se puede vender como servicio.
- **Ruta realista sin audiencia propia:** no ser creador (eso exige público), sino ofrecer el
  *sistema* (páginas por creador + códigos + UTMs + panel) a una marca/tienda de perfume o decant
  española. Es una extensión natural del «candidato 1» (fichas/catálogo) ya propuesto.
- **Aprendizaje transferible:** la convención de campaña y el binomio `creator=` + UTM son el estándar
  de facto del sector; documentarlo sirve para cualquier marca D2C, no solo perfume.

## 6. Lo que NO se ha podido verificar (no se afirma)

- **Anuncios de TikTok de Pafory** (instrumento no fiable en la consulta; control fallido).
- **Cuánto gasta** Pafory al mes en publicidad (las bibliotecas no publican importes en estos casos).
- **Número de seguidores** de sus cuentas (Instagram exige sesión; TikTok no lo expone de forma fiable
  por esta vía).
- **Cuánto dinero paga** a cada creador (hay indicios de pago, no cifras).
- **Si las 29 landings antiguas siguen operativas** (existen como páginas; su uso actual no se puede
  comprobar desde fuera).
- **Nº de empleados / facturación**: los datos que circulan son de agregadores (p. ej. «19 empleados»),
  **no verificados**.
- **Relación societaria formal Pafory↔YUNIQU** (solo consta que YUNIQU es el anunciante del dominio).

## 7. Detalles que no cuadran (para no citarlos mal)

- La página de embajadores promete aparición en un blog llamado «**Beauty Unboxed**», que es el nombre
  del blog de **GLOSSYBOX**. O reutilizaron plantilla o es un error de contenido. No hay blog propio
  con ese nombre.
- **infludeals.net** (agregador de códigos) lista `SCHIKITA60` dentro de una ficha de **joyería**, con
  texto autogenerado. Los agregadores de cupones mezclan datos: usarlos solo como pista.
- `server-sitemap.xml` de su web devolvía **error 504** en la consulta (no bloqueante: se usó
  `sitemap-0.xml`).

## 8. Método (reproducible)

1. `robots.txt` + `sitemap.xml` → `sitemap-0.xml` (25 URLs) → secciones
   `inspiration/blog`, `inspiration/influencer`, `inspiration/playlist` y `influencer-overview`.
2. Su **REST API de WordPress** (`/wp-json/wp/v2/{pages,landingpage,influencer}`) → listados de
   páginas y **códigos de creador** (10 activos) y **29 landings antiguas**.
3. **Comprobación HTTP una a una** de las landings candidatas en `/de/` y `/es/` (códigos 200).
4. **Bibliotecas de anuncios**: Meta Ad Library (DE y ES, con **control** en ES), Google Ads
   Transparency (región ES + ficha de anunciante), TikTok Ad Library (falló el control).
5. **Vídeos de los colaboradores** con `yt-dlp`: canal, título, código, menciones de pago, métricas
   (vistas/likes/comentarios) y **URLs de seguimiento** con `creator=` y UTMs.
6. Evidencia en crudo recopilada en `/tmp/pafory/` (temporal): `robots.txt`, `sitemap-0.xml`,
   `probe_out.txt` (10 landings + códigos), `lp_list.txt` (29 antiguas), `yuniqu.txt` (texto del
   programa de embajadores), `yt_all.txt` (143 vídeos), `yt_views.txt` (métricas), `infludeals_text.txt`.

## 9. Próximos pasos propuestos (a decidir por Joseba)

1. **Guardar la evidencia en el lab** (copiar los .txt de `/tmp/pafory/` a
   `research/pafory-20260927/`), porque `/tmp` se borra al reiniciar.
2. **Ficha de una página** del hueco ES: qué se vendería, a quién (3-5 tiendas/marcas ES concretas),
   precio y qué se entrega en una semana.
3. **Prueba de concepto interna:** generar con el pipeline actual una *landing de creador + código +
   pack de anuncios* de ejemplo (sin tocar nada de terceros) para tener una demo enseñable.
