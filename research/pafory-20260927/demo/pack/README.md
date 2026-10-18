# Pack de colaboradoras — Casa Aurora (EJEMPLO)

Entrega de ejemplo del servicio de gestión de colaboradoras para una tienda de perfume
y decants. **Casa Aurora no existe**: la clienta, las creadoras, los productos, los precios
y todas las cifras son inventados y van marcados como EJEMPLO dentro de cada pieza.

## Qué hay (10 piezas, PNG a tamaño de publicación + HTML editable)

| # | archivo | formato | para qué sirve |
|---|---------|---------|----------------|
| 1 | 00_portada.png | 1080×1527 | portada e índice de lo que se entrega |
| 2 | 01_pagina_creadora.png | 1080×1920 | página de la creadora: enlace, cupón, condiciones, su selección |
| 3 | 02_sistema_atribucion.png | 1080×1350 | cómo se atribuye una venta y qué no se puede medir |
| 4 | 03_anuncio_a.png | 1080×1350 | anuncio 4:5 · variante producto |
| 5 | 04_anuncio_b.png | 1080×1350 | anuncio 4:5 · variante selección |
| 6 | 05_anuncio_c.png | 1080×1350 | anuncio 4:5 · variante prueba social |
| 7 | 06_story_9x16.png | 1080×1920 | story vertical con zonas seguras y guion |
| 8 | 07_brief_campana.png | 1080×1527 | brief: objetivo, mensajes, límites y calendario |
| 9 | 08_informe_mensual.png | 1080×1920 | informe del mes por creadora, con lectura y recomendación |
| 10 | 09_panel_seguimiento.png | 1080×1350 | panel por creadora + coste y retorno |

## Cómo se regenera

```bash
cd pack
python3 gen.py          # las 10 piezas: HTML → PNG + comprobaciones
python3 qa.py           # QA medible: brillo, tinta, huecos, contraste WCAG
python3 dbg.py <pieza>  # mapa de alturas de una pieza concreta
```

No hay dependencias de red: tipografía Inter del sistema, gráficos e ilustraciones en
SVG inline, render con `google-chrome --headless`. Dos ejecuciones dan el mismo PNG.

## Qué se comprueba solo (si algo falla, el script sale con error)

- Las 10 piezas del índice existen, en orden y con la altura esperada.
- Ninguna pieza se desborda ni queda cortada (mide lienzo, scroll y último bloque).
- El PNG mide exactamente 1080 × altura esperada.
- No queda ningún marcador de plantilla sin sustituir en el HTML.
- 15 comprobaciones de coherencia de cifras: sumas por creadora, ingresos = pedidos ×
  ticket, comisión = 10 %, semanas = pedidos, cupón vs enlace, comparativa con septiembre,
  clics y pedidos por pieza, y que cada cupón anuncie el descuento que aplica.
- Contraste WCAG AA de toda la paleta de texto (mínimo 4,5:1) en `qa.py`.

## Datos del caso (todos simulados)

- 3 creadoras, 111 pedidos atribuidos, 5.128,20 € y 512,82 € de comisión en octubre.
- Ticket medio 46,20 € · honorarios de gestión 120 €/mes · retorno 8,1× sobre el coste.
- Ana Ortiz: 962 clics, 58 pedidos, 2.679,60 € de ingresos, 4 piezas publicadas.
- Cupones ANA12 / MARIA10 / JULIA10 con el descuento que anuncia cada uno.

## Ficheros internos

- `out/chk_*.html` son copias de cada pieza con el script de medición: no se entregan.
- `dbg.py` y `qa.py` son herramientas de control, no parte del pack.
