# EXP-20260916-007 — Corrección del instrumento de calidad (v2 → v3)

- **Fecha**: 2026-09-16. **Motivo**: un claim de B(T3) daba `URL_OK_CITA_NO_ENCONTRADA` pese a estar literalmente en la fuente.
- **Aplica a**: TODAS las celdas de calidad de F2 (A y B, tareas T1, T2 y T3).

## El defecto

`norm()` (y `norm_agresiva()`) aplicaban `re.sub(r"<[^>]+>", " ", s)` para limpiar etiquetas HTML de las páginas web.

Ese patrón es **correcto para HTML** y **destructivo para fuentes de código**: en un `arg.cpp` de C++ hay `<` y `>` por todas partes (plantillas, comparadores, `#include <...>`), y el patrón interpreta cada `<` como apertura de etiqueta y **borra todo el texto hasta el siguiente `>`**, que puede estar cientos de líneas después. El texto desaparece antes de buscar la cita.

## Evidencia (no inferencia)

- La cita `keep the dense FFN weights of the first N layers in the CPU` está **literalmente** en `common/arg.cpp` del commit `dfe45163e1c98491bbd7ccab4339422ea3f80100`: comprobado con `grep -n "dense FFN"` y con Python sobre el fichero descargado (`cita in texto` → `True`).
- El cuerpo que el propio medidor descarga (220.178 B) es el fichero correcto (`#include "arg.h"`, con `dense`, `ffn`, `n-cpu-ffn` presentes), pero en el texto **normalizado** la cita no aparece.
- Con la pasada sobre texto crudo → PASS.

## Corrección aplicada (v3)

Tercera pasada de búsqueda sobre **texto crudo** (`norm_crudo`: NFKD + unescape + colapso de espacios + minúsculas, **sin** strip de pseudo-tags), manteniendo las dos pasadas anteriores. La vía queda etiquetada en el detalle (`via: crudo`), así que el cambio es auditable en cada claim.

## Efecto medido (re-medición de todas las celdas)

| celda | v2 | v3 | delta |
|---|---|---|---|
| A-T1 | 7/9 | 7/9 | 0 |
| A-T1 (claim corregido) | 1/1 | 1/1 | 0 |
| A-T2 | 4/5 | 4/5 | 0 |
| A-T3 | 8/10 | **9/10** | +1 |
| **B-T2** | 5/9 | **8/9** | **+3** |
| B-T3 | 11/12 | **12/12** | +1 |

- Los denominadores incluyen el **control negativo** (cita inventada), que correctamente **no** se encuentra.
- **El sesgo del v2 no era aleatorio: penalizaba a B.** Los informes del swarm son más largos y citan mucho más código C++ directo, así que acumulaban más falsos negativos. Con el instrumento corregido, **B no es peor que A en calidad verificada en ninguna celda**.
- **Conclusión de método (RULE-015)**: el instrumento estaba mal calibrado y producía un resultado que parecía confirmar la hipótesis por la vía equivocada. Validar la métrica **antes** de confiar en su cifra evitó firmar un veredicto con un artefacto propio.

## Pendiente de honestidad

Los tres claims de `api.github.com` bloqueados por *rate limit* (403, `remaining=0`, reset 16:37:35) se etiquetaron `ANTIBOT_NO_VERIFICABLE_POR_CURL` y **no contaron como PASS ni como fallo** hasta resolverse. El reintento programado despertó a las **16:36:39** (56 s antes del reset) y aún dio 403×3; la re-medición posterior al reset los verificó **en vivo** (HTTP 200 + cita) → **B(T2) 8/8 = 100 %**. El propio informe de B(T3) documenta la misma limitación desde esta IP.
