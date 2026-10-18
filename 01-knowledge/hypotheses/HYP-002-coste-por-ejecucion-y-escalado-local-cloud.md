---
type: knowledge
subtype: hypothesis
status: active
tags: [knowledge, hypothesis, coste, router]
created: 2026-09-15
---
# HYP-002: Con coste por ejecucion, la politica de escalado a cloud cambia

**Origen:** OBS-104
**Fecha:** 2026-09-15
**Estado:** propuesta

## Observacion
El router local->cloud no persiste coste ni tokens junto a la decision
(local_cloud_ledger.jsonl: 9 campos, ninguno de coste). El coste solo existe
como texto en consola ("0 USD (local)" / "cloud flash"). Los tokens si se
registran por otra via (pipeline_obs.jsonl) pero sin precio en EUR.

## Hipotesis
Una parte de los escalados a cloud no compensa lo que cuesta: si el coste se
registrara junto a cada decision, aparecerian casos donde el resultado local
(o un reintento local distinto) habria bastado, y la politica de escalado por
franja horaria se ajustaria con datos en vez de por regla fija.

## Prediccion
Si la hipotesis es correcta, al unir tokens (ya registrados) con precio
(EUR/1M) y escribir el coste en el ledger del router:
  - se podra calcular coste medio por tarea y por tipo
  - existira al menos un subconjunto de escalados con coste > 0 cuyo resultado
    local no fue peor
Medible con: coste EUR/dia, % de escalados, % de escalados "no compensados".
Umbral: NO se fija a priori (RULE-015). Primero baseline de 7 dias con el
ledger actual + precio aplicado a los tokens ya registrados; el umbral se fija
despues de ver el baseline.

## Validacion
- [ ] Baseline 7 dias (coste reconstruido desde pipeline_obs.jsonl + precios)
- [ ] EXP-XXX disenado (medir antes/despues de escribir coste en el ledger)
- [ ] EXP-XXX ejecutado
- [ ] Resultado: [confirma | refuta | inconcluso]

## Decision derivada
- DEC-XXX (si confirmada)

## Conexiones
- [[OBS-104]] — origen
