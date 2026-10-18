---
title: "Ficha de oferta — servicio de colaboradores para tiendas de perfume en España (27-sep-2026)"
type: research
---

# Ficha de oferta — «sistema de colaboradores» para tiendas de perfume ES

**VERACIDAD:** [ALCANCE INTERNO]
**Método:** sondeo propio de solo lectura el 27-09-2026 (`/tmp/pafory-es/probe_es.py`, `probe2_es.py`):
home con UA de navegador + `robots.txt` + **todos los sitemaps** de cada tienda, buscando páginas
de colaboradores/afiliados/embajadores/influencers/creadores/programas/cupones. Copia de la
evidencia en `evidencia_es/`. Datos de negocio (facturación, seguidores) **no verificados**.
**Origen del enfoque:** la investigación de Pafory (27-09) demostró que el valor de una red de
creadoras está en la capa de operaciones: código + UTM + página por creadora + informe.

## 1. Qué se vende (entregables, no «marketing»)

| Entregable | Qué incluye | Plazo |
|---|---|---|
| Página de creadora | 1 pieza (formato 1080×1350) con su código, su enlace con `creator=` + UTMs y su selección | 2 días |
| Pack de anuncios | 3 variantes del mismo producto con gancho distinto (regalo / descubrimiento / prueba social) | 3 días |
| Tubería de atribución | Alta del código en la tienda, enlaces con UTMs normalizados, hoja de seguimiento por creadora | 4 días |
| Informe por creadora | Clics, pedidos, ingresos, comisión, coste por pedido + lectura de qué funcionó | mensual |

Base técnica: el pipeline del lab (HTML→PNG determinista) genera la página y los anuncios en horas,
y el panel sale de los parámetros `creator=` y UTM. Ejemplo real y funcional: `demo/` (5 piezas).

## 2. El hueco, medido

Sondeo de 7 tiendas ES de perfume/decants; se leyeron **todos** sus sitemaps (147 a 3.161 URLs cada una):

| Tienda | URLs en sitemap | Página de colaboradores/afiliados/cupones |
|---|---|---|
| decants.es | 147 | **0** |
| oasisparadise.es | 536 | **0** |
| decantsperfumespain.com | 7 | **0** |
| ponsaparfums.com | 53 | **0** |
| nadiaperfumeria.com | 3.161 | **0** |
| sillagebarcelona.com | 206 | **0** |
| arabicparfums.es | 0 (sitemap vacío) | no verificable por esta vía (su home menciona «club», «programa») |
| anyaperfumes.es | sitemap → 404 | no verificable por esta vía |

Lectura: **ninguna** de las que publican sitemap tiene programa de colaboradoras, ni página de
afiliados, ni cupones indexados. Todas están en redes (Instagram/TikTok enlazados desde su propia
web) y varias hacen contenido. Es decir: **hacen cosas con creadoras o quieren hacerlas, pero sin
sistema**. Eso es exactamente lo que se vende.
Matiz honesto: el sondeo mira páginas publicadas; pueden colaborar por DM y no tenerlo publicado.
Eso no invalida la oferta, la explica: no hay forma de saber qué venta vino de quién.

## 3. A quién (5 objetivos, por orden de ataque)

1. **decants.es** — tienda de decants en España. Redes: `instagram.com/@decant.studio`, `tiktok.com/@decantsstudio`.
   Encaje: los decants viven del descubrimiento, y ya invierten en redes. Sin programa publicado.
   Ángulo: «tus decants los recomienda gente; hoy no sabes cuál te trae clientes».
2. **oasisparadise.es** — perfumería de nicho + decants. Redes: Instagram `oasis_a_touch_of_paradise`.
   536 URLs (catálogo serio). Encaje: catálogo amplio que se explica mejor con creadoras que con anuncios.
3. **decantsperfumespain.com** — tienda pequeña (7 URLs), envío gratis desde 50 €. Encaje: **piloto
   barato**: poco catálogo, decisión rápida, ideal para la primera pieza de portafolio.
4. **ponsaparfums.com** — perfumería de autor en Sant Joan Despí (Barcelona), marca propia + talleres.
   Redes: Instagram y TikTok `@ponsabarcelona`. Encaje: marca con producto propio que necesita darse a
   conocer; su producto se cuenta muy bien en vídeo.
5. **nadiaperfumeria.com** — perfumería de nicho en Madrid (dos tiendas: Velázquez 46 y Diego de León 35).
   3.161 URLs. Encaje: la más grande de la lista → ciclo de venta más largo, pero presupuesto real.

Secundarios (si fallan los cinco): `sillagebarcelona.com` (tienda + editorial propio, ya hace contenido),
`anyaperfumes.es` (perfumería indie en Zaragoza, vegana), `arabicparfums.es` (perfumes árabes, 1,29 MB
de home y redes activas en IG/TikTok).

**Descartados y por qué:** `marvimundo.com` y `perfumerias.com` (cadenas con >90 tiendas: no compran
a un autónomo); `notino.es` (multinacional); `esenzzia.es` (perfumes de imitación: no encaja con la
marca personal que está construyendo); `aineaperfums.com` (es un laboratorio B2B, no una tienda).

## 4. Precio y plazos

- **Piloto**: 1 cliente, 2 semanas, **150-250 €** → página de creadora + 3 anuncios + tubería de
  atribución + primer informe con datos reales. Es un trabajo pequeño y cerrado: sirve para tener
  una referencia con nombre y apellidos.
- **Recurrente**: informe mensual por creadora (o tarifa plana por la red), 40-80 €/mes para redes
  de 1-5 creadoras.
- **Regla propia (27-09)**: cobrar cero no valida nada. Si se regala, que sea **una** pieza a un
  cliente concreto y a cambio de poder citarlo como referencia.
- **Alcance explícito**: no se gestionan las creadoras por él (eso es relación personal de la tienda),
  ni se compra publicidad, ni se prometen ventas. Se monta y se mide el sistema.

## 5. Cómo se mide el resultado

- Código por creadora + enlace con `creator=` y UTMs (`utm_medium=influencer`, `utm_campaign=fecha_formato`).
- Métricas del informe: visitas con su enlace, clics únicos (CTR), pedidos atribuidos, ingresos,
  comisión, coste por pedido.
- Criterio de éxito del piloto, fijado ANTES: que la tienda pueda responder «quién me trajo ventas
  este mes» con una lista, no con una intuición.

## 6. Primer contacto (borrador, 4 líneas)

> Hola: soy Joseba, de Bilbao. Vi que en [tienda] trabajáis con gente que recomienda vuestros
> perfumes, pero no tenéis código ni enlace propio para cada persona: eso significa que no podéis
> saber qué venta vino de quién. Monto ese sistema en 2 semanas: página para cada creadora con su
> código, enlaces medibles y un informe mensual. Te enseño un ejemplo hecho (no una propuesta de
> PowerPoint). ¿Te lo paso?

## 7. Lo que NO está verificado (no usar como argumento)

- **Seguidores** de las tiendas y de sus redes: no verificables sin sesión. Solo consta que **enlazan**
  esas cuentas desde su web.
- **Facturación, plantilla, presupuesto de marketing**: nada verificado.
- **Si ya colaboran** con creadoras de forma informal (DM, producto gratis): no se puede saber desde
  fuera; el borrador asume que **no hay sistema**, que es lo comprobado.
- `arabicparfums.es` (su home menciona «club»/«programa») y `anyaperfumes.es` (sin sitemap): **pendiente
  de una segunda comprobación manual** antes de usarlos como objetivo.

## 8. Fuentes y evidencia

- Sondeo de home + robots + sitemaps de cada tienda, 27-09-2026: `/tmp/pafory-es/probe_es.py`,
  `probe2_es.py`, `resumen.json`, `sitemaps_resumen.json`, `urls_<tienda>.txt`, `<tienda>.txt`
  (texto plano de cada home) → copiado a `evidencia_es/`.
- Datos de negocio de cada tienda: los que publica su propia web (dirección, redes, política de envío).
- Enfoque y cifras del sector: `research/pafory-colaboradores-publicidad-20260927.md`.
