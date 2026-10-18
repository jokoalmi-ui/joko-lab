---
title: "Precios vigentes — DeepSeek V4 (fijados 2026-09-15)"
type: operations
---

# Precios vigentes DeepSeek V4 — fijados 2026-09-15

Cierra F0 del `EXP-20260915-006`. Sustituye, para el cálculo de coste del lab, a la tabla
"Precios oficiales directos (verificados 19-ago-2026)" que arrastran los monitores
`2026-08-19.md`, `2026-08-24.md`, `2026-09-07.md` y `2026-09-14.md` — esa tabla es INCORRECTA (ver abajo).

## Tabla válida (USD por 1M tokens, precio unitario por tipo de token)

| Modelo | cache hit | cache miss | output |
|---|---|---|---|
| deepseek-v4-flash | 0,0028 | 0,14 | 0,28 |
| deepseek-v4-pro | 0,003625 | 0,435 | 0,87 |

## Prueba (fuente primaria: export oficial de facturación de la propia plataforma)

El export detalla `price` + `amount` por tipo de token y el `cost` facturado por día.
`price × amount` reproduce el coste facturado **exactamente**, en dos periodos independientes:

| Periodo | Σ(price × amount) | Σ(cost) facturado | Diferencia |
|---|---|---|---|
| 2026-06-27 → 2026-07-27 | 14,406802 USD | 14,406802 USD | 0,000000 |
| 2026-07-12 → 2026-08-10 | 35,900597 USD | 35,900597 USD | 0,000000 |

Ficheros: `USAGE/extraido/amount-*.csv` y `cost-*.csv` (columnas `model`, `type`, `price`, `amount`, `cost`, `currency`).
El precio unitario aparece **idéntico en ambos periodos** → tarifa estable en jun-ago-2026.

## Refutación de la tabla errónea (0,22 / 0,66 / 0,007)

La tabla de los monitores dice para v4-flash off-peak: miss **0,22**, output **0,66**, cache hit **0,007**.
Con las cantidades REALES del ledger en 07→10 ago (prompt 1.150.153.104 tokens, output 3.589.854):

- Coste **mínimo teórico** con esos precios (suponiendo el 100% del prompt como cache hit):
  `1.150.153.104 × 0,007/1M + 3.589.854 × 0,66/1M` = 8,0511 + 2,3693 = **10,4204 USD**
- Facturado real de esos mismos 4 días: **5,9132 USD**

→ El mínimo con esos precios ya SUPERA la factura. Son **imposibles** para estas cantidades: no es un error de ratio de cache, es el precio lo que está mal. Descartada también la explicación "franja peak ×2" (0,14×2 = 0,28 ≠ 0,22, y los tres factores no son uniformes: 1,57x / 2,36x / 2,5x).

## Validación por inversión (ratio de cache implícito)

Con la tabla válida, el coste reconstruido de 07→10 ago cuadra con la factura si el ratio de cache hit fue:

- cobertura de tokens ×1,00 → **98,93%**
- ×1,05 → 99,11% · ×1,10 → 99,27% · ×1,19 → 99,53%

Rango plausible (septiembre mide 96,09% con cache ya instrumentado). **No es prueba directa** — en agosto el campo no existía — pero sí descarta errores de orden de magnitud y confirma que el método (tokens del ledger × precio unitario oficial) es el correcto.

## Consecuencia operativa

- Cualquier informe de coste que use 0,22/0,66/0,007 sobreestima el gasto del prompt ~1,6x y el output ~2,4x.
- Desglose del coste del lab (con tabla válida): el prompt cacheado es baratísimo (0,0028/M); el gasto se decide en el **ratio de cache** y en el **output**.
- Registrado: OBS-106 · OP-20260915-003.
