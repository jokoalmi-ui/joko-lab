---
type: registro-ficha-diaria
fecha: 2026-11-21
perfume: Ambre Tabac
casa: Daniel Josier
carpeta: research/infografias/perfume-del-dia-20261121
---

# Ficha del día · 2026-11-21 (sábado)

## Elección

- **Ambre Tabac — Daniel Josier (perfume_id 919 · `uso_diario` 148)**, EDP masculino de 2014, oriental amaderado.
- Clima (pronóstico a un día, `ventana_perfume.py --fecha 2026-11-21`): media **13,6 °C**,
  12,7–14,4 °C de sensación, amplitud 3,9 (sin tramos) · **lluvia 83 %** · banda fresca.
- Rotación: 0 usos previos en `uso_diario`.
- Comunidad: Fragrantica **4,57/5 · 866 votos** (consultado 20-11-2026).
- Precio: **90,00 € / 100 ml** (danieljosier.com, consultado 20-11-2026).

## Variante designada como ficha del día (decisión 2026-11-21)

- Se publica/entrega la variante **`_d60v`**, no la `_d60`.
- Motivo: el usuario pidió «reducir texto sin tocar tamaños» y «reducir un poco el velo blanco
  alrededor del texto».

### Cambios respecto a `_d60`

| Elemento | Antes | Después |
|---|---|---|
| Velo global (blanco sobre el arte) | 18 / 26 / 40 % | **13 / 19 / 28 %** |
| Halo de la letra (text-shadow) | 70–75 % | **45–48 %** |
| Inspiración | incluía ADN (Ambre Narguilé / Oajan / Angels' Share) y puesto 152 Parfumo | recortado a la idea + notas |
| Comunidad | cerraba con la frase del «sultán multimillonario» | recortada |
| Pie (clima) | «…banda fresca · ámbar y tabaco para un sábado de agua» | «…banda fresca» |

Los **tamaños de letra no se han tocado** (16 reglas a ≤12,5 px siguen intactas).

### Medición

- `norma_legibilidad.py` → **VEREDICTO NORMA CUMPLE** · 70 nodos · R1 0 · R2 0 · avisos 3-4,5:1 **ninguno**.
- Contraste medio de los 70 nodos: **7,777 → 7,779**; mínimo **3,02:1** en ambos (SVG CORAZÓN, nodo
  que el método no mide con halo). Caída mayor: **−0,44** en la cita.
- Lectura del dato: al bajar el velo **el contraste no baja** porque lo sostiene el halo, no el velo.
  Si se quiere el fondo aún más oscuro, hay que tocar tinta o cuerpo de letra: el suelo es 3,0 y ya
  estamos en 3,02.
- `validar_ficha_preenvio.py` → **17/17 · FALTA 0** · avisos A3 (×1,41), A4 (precio con fecha 21-11-2026),
  A5 (recorte filo 787 px, delta L +27,7, visibles 66,3 %) · E1 altura 1440 px · E2 pie bottom 1390 →
  **aire 50 px** (antes 41). Veredicto **ENVIAR (con avisos)**.

## Material

- `ficha_20261121_d60v.html` — md5 `1220dff86b81d8faaac9bd0772d9b551`
- `perfume_del_dia_v5_ambre_tabac_d60v.png` — md5 `a0d978be30ae11e1e6ee1cc896b41a26`
- Render: `google-chrome --headless=new --force-device-scale-factor=1 --window-size=1080,1440`.
- Descartadas y conservadas: `_d60` (original envío), `_d68`, `_d80`, y la clara sin palanca.
- El generador (`build_ficha.py`) y la plantilla compartida **no se han modificado**: la variante se
  construyó sobre el HTML final.

## Registro en BD

- `uso_diario` id **148** · fecha 2026-11-21 · `clima_temp` 13,6 · ventana 08-18.
- Marca de valoración: **`[VAL: sin respuesta aun]` — ABIERTA**. No se cierra sin veredicto del usuario
  (`cerrar_ficha_dia.py` no se ha ejecutado).
- Backup previo: `coleccion.db.BACKUP.20261120_ficha_20261121`.

## Envío

- Entregada en el chat (DM) como PNG + HTML. **No publicada en el canal** `-1003968087263`:
  falta autorización explícita.

## Cierre (veredicto del usuario)

- **2026-11-22 07:02 CET** — el usuario da por buena la ficha: «están bien».
- Marca `[VAL: sin respuesta aun]` de `uso_diario` **148**: veredicto **favorable**, recibido.
  La fila **no se ha reescrito**: `coleccion.db` es de solo lectura para el asistente; la marca
  se actualiza desde el propio flujo o con autorización explícita.
- Ficha cerrada en su variante `_d60v`. No se reescribe.

