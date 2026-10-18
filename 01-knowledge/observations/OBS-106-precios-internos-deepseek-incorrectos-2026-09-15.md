---
type: knowledge
subtype: observation
status: active
tags: [knowledge, observation, coste, precios, deepseek, verificacion]
created: 2026-09-15
---
# OBS-106: La tabla de precios de DeepSeek usada en los informes internos es incorrecta
===============================================

## Datos basicos
  ID: OBS-106
  Fecha: 2026-09-15
  Origen: F0 del EXP-20260915-006 (sesion 2026-09-15), al intentar reconstruir
          el coste por ejecucion desde pipeline_obs.jsonl

## Observacion

El lab tiene dos juegos de precios de DeepSeek V4 Flash que no coinciden, y el que
usan los informes de monitorizacion es el erroneo:

  A) Export oficial de facturacion de la plataforma (fuente primaria):
     cache hit 0,0028 / cache miss 0,14 / output 0,28 USD por 1M tokens
  B) Tabla "Precios oficiales directos (verificados 19-ago-2026)" que aparece identica
     en 04-operations/metrics/precios-ia/2026-08-19.md, 2026-08-24.md, 2026-09-07.md
     y 2026-09-14.md: cache hit 0,007 / miss 0,22 / output 0,66 USD por 1M tokens

No es un factor uniforme (1,57x / 2,36x / 2,50x), por lo que no se explica por franja peak.

## Evidencia literal

1) Identidad contable en el export oficial, DOS periodos independientes:
   suma(price x amount) = suma(cost) al sexto decimal
   - 2026-06-27_2026-07-27: 14,406802 = 14,406802 USD
   - 2026-07-12_2026-08-10: 35,900597 = 35,900597 USD
   El campo `price` por tipo de token es identico en ambos periodos (tarifa estable).

2) Refutacion de B por minimo teorico, con las cantidades reales del ledger 07->10 ago
   (prompt 1.150.153.104 tokens, output 3.589.854):
   minimo con B (100% del prompt como cache hit) = 8,0511 + 2,3693 = 10,4204 USD
   facturado real de esos 4 dias = 5,9132 USD
   -> el minimo con B ya supera la factura: B es imposible para estas cantidades.

3) Con A, la factura se reproduce con un ratio de cache hit implicito de 98,93%
   (banda 98,93%-99,53% segun cobertura de tokens), plausible frente al 96,09% medido
   en septiembre (unico periodo con el campo instrumentado).

## Alcance

- Afecta a cualquier calculo de coste que use la tabla B: el prompt se sobreestima ~1,6x
  y el output ~2,4x. Las cifras de "gasto real" de los monitores (14,41 y 35,90 USD) vienen
  del CSV oficial y NO estan afectadas.
- La tabla B se copia sin revisar desde el 19-ago en los cuatro monitores (seccion fija).

## Que NO dice

- No dice de donde salio la tabla B (pudo ser un precio de otro modelo, de OpenRouter u otra
  cuenta). No confirmado.
- No valida la cobertura del proxy (cuanto trafico ve). Eso es F2 del EXP-20260915-006 y
  requiere el export oficial de septiembre.
- No descarta que el proveedor cambie de tarifa en el futuro: la validez de A es jun-ago-2026.

## Acciones derivadas

- Fichero de referencia creado: `04-operations/metrics/precios-ia/precios-vigentes-2026-09-15.md`
- F0 del `EXP-20260915-006` cerrado (precio fijado). F2 (cobertura) sigue pendiente del export de septiembre.
- Registro: OP-20260915-003.
