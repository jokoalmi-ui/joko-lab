---
type: registro-ficha-diaria
fecha: 2026-11-22
perfume: Encre Noire à L'Extrême
casa: Lalique
carpeta: research/infografias/perfume-del-dia-20261122
---

# Ficha del día · 2026-11-22 (domingo)

## Elección

- **Encre Noire à L'Extrême — Lalique (perfume_id 955 · `uso_diario` 149)**, EDP masculino de 2015,
  amaderada aromática (Nathalie Lorson).
- Clima (pronóstico a un día, `ventana_perfume.py --fecha 2026-11-22 --ventana 08-18`):
  media **11,1 °C**, 9,9–11,9 °C de sensación, amplitud 5,3 (estrecha, sin tramos) ·
  lluvia 0 % · humedad 47 % · banda fresca · dosis 3-4.
- Rotación: 0 usos previos (botella propia; el decant solo desempata).
- Alternativas con números: Encre Noire 2006 4,14/5 · 26.276 votos · Memoir Man 8,0/10 · 1.204 ·
  Laudano Nero 4,06/5 · 3.135.

## Puertas

- `norma_legibilidad.py` → **VEREDICTO NORMA CUMPLE** · 70 nodos · 0 <12 px · 0 bajo 3,0:1 ·
  peor nodo **3,02:1** (SVG CORAZÓN) · avisos 3-4,5:1: 3,82 / 4,00 / 3,81 (tres `[alt-motivo]` a 12 px).
- `qa_maqueta.py` → **VEREDICTO MAQUETA OK**, sin fallos.
- `validar_ficha_preenvio.py --fecha 2026-11-22` → **17/17 · FALTA 0** · altura 1440 · pie 1390 ·
  aire 50 px · veredicto ENVIAR (con avisos A3 ×1,41 · A4 fecha en línea · A5 recorte 660×989, ΔL +10,7).

## Visibilidad del frasco (medida, sin umbrales)

- Fondo contiguo L **75,19** · tapón L **35,0** → **1,81:1** · cuerpo L **186,70** → **4,52:1** ·
  claros 0,0 % · rect 300×450 px en (52, 99).
- Aviso trasladado al usuario: el cuerpo es el mejor medido hasta la fecha (4,52 vs 3,16–3,78 de
  referencia), pero el tapón se funde con el fondo (L 75 frente a 113–116 habituales).
- **Decisión del usuario: se acepta tal cual.** No se genera variante de tono. No se toca el criterio.

## Material

- `ficha_20261122.html` — md5 `c16615e21b236bdebd0b8a79bd9c19bf`
- `perfume_del_dia_v5_encre_noire_extreme.png` — md5 `c0ec8ac89cf7e73bf83da90474eb5a89`
- Render 1080×1440, dos renders idénticos.

## Registro en BD

- `uso_diario` id **149** · fecha 2026-11-22 · `clima_temp` 11,1 · ventana 08-18.
- Ocasión `casa` y ánimo `tranquilo` **asumidos** (domingo, sin dato del usuario).
- Backup previo: `coleccion.db.BACKUP.20261121_ficha22`.
- Marca `[VAL]` en la fila: veredicto **favorable** recibido el 2026-11-22 07:02 CET («están bien»);
  la fila **no se ha reescrito** porque `coleccion.db` es de solo lectura para el asistente.

## Envío

- `enviar-ficha-telegram.sh` → EXIT=0, `sent`. Caption determinista: «Buenos días con alma de vetiver.»
- Entregada en el chat (DM). **No publicada en el canal** `-1003968087263`.

## Horario (cambio del 2026-11-22)

- Desde el 22-11-2026 la entrega diaria se mueve de las **10:00** a las **21:00**, con la ficha del
  día siguiente (cron `8bf412ac2ba3`, `0 21 * * *`). Motivo: es cuando el usuario prepara el día siguiente.
- Esta ficha del 22 fue la última entregada con el horario antiguo (10:36 CET).
