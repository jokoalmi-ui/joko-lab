---
type: registro-ficha-diaria
fecha: 2026-10-31
perfume: Pegasus
casa: Parfums de Marly
carpeta: research/infografias/perfume-del-dia-20261031
---

# Ficha del día · 2026-10-31 (sábado)

## Elección

- **Pegasus — Parfums de Marly (id 1058)**, EDP masculino de 2011.
- Motivo: ventana 08-18 con sensación media **15,0 °C** (banda templada) y amplitud **7,0 °C**
  (media) → perfil medio, sin extremos. `rango_termico` lo sitúa en **banda medio, índice +0,03**
  (índice **0,00**, banda `medio`, el más cercano a 0 de los candidatos con decant). Última aparición en `uso_diario`:
  **2026-08-05** → 87 días antes de hoy (≥60, puede volver).
- Disponibilidad: `perfumes.posee='decant'` y **1 decant disponible** (desempate, no filtro).

## Instrumento de clima (tools/ventana_perfume.py --ventana 08-18)

- Ventana 08-18: sensación **10,4–17,4 °C**, media **15,0**.
- Día: mín 10,9 / máx 18,2 °C · amplitud sensación **7,0 °C (media)**.
- Lluvia 0 % · humedad media 72,3 %.
- Tramos emitidos por el script: mañana (08-12) 13,1 °C → 3-4 sprays; tarde (13-18) 16,7 °C → 3 sprays.
- Dosis en la ficha: **3** a las 08:00 · **3** si se repite de tarde.

## Datos de la ficha

- Pirámide: **oficial de parfums-de-marly.com** (consultada 31-10-2026) — salida anís, bergamota,
  almendra; corazón jazmín, lavanda, almendra amarga; fondo vainilla, ámbar, sándalo.
- Rating: Fragrantica ES 4,07/5 · 6.812 votos · 39 reseñas.
- Precio: **290,00 € / 125 ml · 232,00 € / 100 ml** (parfums-de-marly.com, consultado 31-10-2026).
- Alternativas con fuente y números: Armaf Craze (Parfumo 7,6/10 · 565 votos), Maison Alhambra
  Perseus (90 % de notas en común), Dior Hypnotic Poison (Fragrantica 4,08/5 · 30.857 votos).
- Cita de comunidad: peterMartinez, Fragrantica ES, 25-dic-2025.

## Material

- Packshot: Shopify oficial de la casa (`PEGASUS-PERFUME-125-PACK1-1X1_CENTERED_*.png`), 1080×1080,
  con canal alfa real → alfa de origen respetado; recorte a figura 249×450.
- Fondo: FLUX.2 [klein] 4B, 20 pasos, seed 42, 1024², vía `tools/gen_fondo_klein.py` (GPU, ComfyUI).
- QR: apunta a la ficha de Fragrantica de Pegasus.

## Puerta preenvío

`validar_ficha_preenvio.py` → **17/17, FALTA 0**, 3 avisos informativos (A3 ampliación ×1,41 ·
A4 precio con fecha · A5 recorte sin halo). E1 altura real 1440 px (fuentes `loaded`, img 3/3),
E2 pie bottom 1388 → aire 52 px.

## Visibilidad del frasco (`vis.json`)

- Rect del frasco: x 78-327 · y 84-534 (249×450 px del PNG).
- Fondo contiguo: **L 153,1**.
- Tapón: L 70,0 → **3,32:1**.
- Cuerpo: L 238,2 → **2,46:1**.
- Píxeles claros dentro del rect: **23,1 %** (informativo, sin umbral).
- Referencias: 17-oct tapón 3,92 · cuerpo 3,16 · fondo 116,8; 18-oct tapón 2,07 · cuerpo 3,78 · fondo 113,7.
  El cuerpo queda por debajo de ambas (frasco plateado claro sobre fondo klein claro); se subió de
  2,19 a 2,46:1 reajustando solo la sombra del frasco (la primera medición de hoy fue 2,19).

## Envío

- Canal Telegram `-1003968087263`: **enviado** (wrapper `enviar-ficha-telegram.sh canal`, EXIT=0, "sent").
- Caption: solo el saludo del script (`Buenos días. El perfume no cambia el día: cambia cómo lo vives.`).

## Registro en BD

- `uso_diario` id **126** · perfume_id 1058 · fecha 2026-10-31 · clima_temp **15,0** ·
  clima_desc `ventana 08-18: 10,4-17,4 C sens, media 15,0; dia 10,9-18,2 C; lluvia 0%` ·
  animo `tranquilo` (asumido) · ocasion `trabajo` · nota con `[VAL: sin respuesta aun | ventana 08-18]`.
- Backup previo: `coleccion.db.BACKUP.20261031_pegasus`.
- Corrección de dato: `perfumes.concentracion` de 1058 estaba vacío → **EDP** (dato oficial).
