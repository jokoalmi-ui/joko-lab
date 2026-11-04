# REGISTRO — ficha del día 29-10-2026 (ÔIKB · Santi Burgas)

**Estado: la ficha del día es la variante `_b`. NO se envía al canal** (el usuario validó la imagen recibida en el DM: «Registra como del día pero no envies la ficha ya que me vale la imagen que me has enviado»).

## Registro en BD
- `uso_diario` **id 124** · `perfume_id` 1007 · `fecha` 2026-10-29 · `clima_temp` 15.8 · `clima_desc` «ventana 08-18: 11,1-17,9 C sens, media 15,8; lluvia 0%» · `animo` tranquilo · `ocasion` trabajo.
- `nota_personal` ampliada con: `ficha registrada = variante _b (perfume_del_dia_v5_oikb_b.png, packshot trasero oikb_100_back, frasco bicolor) aprobada por el usuario 29-10; NO enviada al canal (le vale la imagen recibida en el DM) · publicada sigue siendo _a (perfume_del_dia_v5_oikb.png)`.
- Backup previo byte a byte: `coleccion.db.BACKUP.20261029_105806_oikb_b` (md5 `c0df836030c513690f2ea53217d65009`, idéntico al de origen).
- `pragma integrity_check` = `ok` antes y después; filas en `uso_diario` = **122** antes y después (una sola fila tocada, ningún alta).

## Ficheros de la ficha del día
- `perfume_del_dia_v5_oikb_b.png` — 1080×1440, **1.946.417 B**, sha256 `b8c4f4b50e90e83ced2705ba5e2f70f7a9dae3812e7b92b3f8811af1b6047062` (dos pasadas de Chrome con el mismo sha).
- `perfume_del_dia_v5_oikb_b.html` · `santi_oikb_figura_b.png` (packshot **trasero** `oikb_100_back`) · `recorte_bicolor.py` (máscara geométrica) · `build_ficha_b.py` · `vis_b.json`.
- Publicada e intacta: `perfume_del_dia_v5_oikb.png` — 1.970.317 B, sha256 `d369e5dd72ffb2680800d1dcd30dbe15fb968164443e9a24f7cc321fb754c0cb`; `vis.json`.

## Verificación
- `validar_ficha_preenvio.py perfume_del_dia_v5_oikb_b.html` → **17/17, FALTA 0, veredicto ENVIAR (con avisos), EXIT=0**. Avisos **A3, A4 y A5**: los mismos tres que ya daba la ficha publicada; en A5 el filo baja de 5.153 px a 390 px y el delta sube de +69,5 a +87,3.
- `vis_b.json` literal: fondo L **109,57** · «tapón» 75,21 → **1,694:1** · cuerpo 232,00 → **4,188:1** · claros **30,23 %** · rect 47,84,309,450.
- Publicada (`vis.json`): fondo 113,50 · «tapón» 66,78 → 2,049:1 · cuerpo 223,21 → 3,643:1 · claros 9,33 % · rect 48,84,309,450.
- Matiz del «tapón»: en frascos **bicolor** la máscara (L<90) captura **la banda azul**, que va rodeada de blanco y no contra el fondo → 1,694:1 no mide el corcho. Documentado en la skill `perfume-del-dia` (secciones «s silueta geométrica» y «norma de medición»).

## No hecho (a propósito)
- **Ningún envío** a `telegram:-1003968087263` con la variante `_b`.
- **Sin commit** de la variante `_b` ni de `recorte_bicolor.py`/`build_ficha_b.py` (no hay OK).

## Cómo revertir
- BD: restaurar `coleccion.db.BACKUP.20261029_105806_oikb_b`, o quitar el sufijo añadido en `nota_personal`.
- La ficha publicada no se ha tocado: borrar los ficheros `_b` no altera lo ya enviado.
