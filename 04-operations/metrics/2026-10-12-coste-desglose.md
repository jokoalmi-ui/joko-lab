# Coste real del lab — desglose por tipo, techo y contraste con el saldo

**Medición**: 2026-10-12, 15:07–15:19 CEST (hora medida con `date`).
**Instrumentos** (solo lectura, no modificados): `tools/desglose_coste.py`, `tools/coste_ahorro.py`, `tools/coste_historial.jsonl`, `GET https://api.deepseek.com/user/balance`.
**Datos**: `04-operations/metrics/pipeline_obs.jsonl` (54.494 líneas, 1 corrupta; campos `prompt_cache_hit/miss_tokens` solo desde 2026-09-01T17:38:15) + `coste_historial.jsonl` + CSVs de `USAGE/extraido/`.

## 0. Titular: el saldo se agota en ~22 h, no en 1,8 días

- Saldo real leído en crudo (`/user/balance`, HTTP 200, `is_available: true`): **2,47 USD**, `currency: USD`, `granted_balance: 0.00`, `topped_up_balance: 2.47`.
- **Ritmo real medido por saldo: 2,696 USD/día** (caída de 1,86 USD en 16,56 h entre dos lecturas independientes).
- **→ quedan ~0,92 días ≈ 22 h** desde las 15:19; se agota en torno al mediodía del martes 13.
- El ledger del lab estima 1,3862 USD/día (7 d) → 1,78 días. **El ledger subestima ×1,84** (ver §5).

Lecturas del saldo (todas con `currency: USD`):

- 2026-10-11 22:45:35 (cron) → **4,33**
- 2026-10-11 22:45:51 (cron) → **4,33**
- 2026-10-12 07:00:45 (cron) → **3,95**
- 2026-10-12 15:12 (manual) → **2,51**
- 2026-10-12 15:18:55 (manual, crudo) → **2,47**

## 1. Gasto estimado por el ledger

- **7 d** (2026-10-05T15:19:15 → 2026-10-12T15:19:15): 5.817 consultas · **9,7031 USD** · **1,3862 USD/día** · 0,0017 USD/consulta.
- **30 d** (2026-09-12T15:19:26 → 2026-10-12T15:19:26): 24.602 consultas · **42,3780 USD** · **1,4126 USD/día** · 0,0017 USD/consulta.
- Dispersión diaria 7 d: 0,13 (05-oct, parcial) → 1,87 (08-oct). 11-oct: 1,6991. 12-oct (hasta 15:19): 1,0132.
- Hora más cara de la semana: **08:00 (1,8925 USD = 19,5 % del gasto)**; le siguen 07:00 (1,6102 = 16,6 %) y 23:00 (0,9278 = 9,6 %).
- Franjas 30 d: 08-12 **PICO** = 28,5 % del gasto; 12-24 valle = 59,9 %; 06-08 valle = 11,6 %; 00-03 = 0,0 %.

## 2. Desglose por tipo (7 d; base «valle-equivalente» 8,7612 USD)

- **Salida** 3,7081 USD (**42,3 %** de la base)
- **Miss** 3,9583 USD (**45,2 %**)
- **Hit** 1,0948 USD (**12,5 %**)
- **Recargo de pico** 0,9436 USD (9,7 % del total de 9,7031)

30 d (base 37,9418): salida 16,8212 (44,3 %) · miss 16,3700 (43,1 %) · hit 4,7506 (12,5 %) · recargo de pico 4,4379 (10,5 %).

## 3. Salida y prefijo (por qué cuesta lo que cuesta)

- Salida 7 d: 6,18 M tokens, coste 4,1613 USD (42,9 %). Media 1.062 tok/consulta; p50 640 · p90 2.498 · p95 3.401 · **máx 25.718**.
- **El 10 % de consultas más largas = 39,4 % del coste de salida.**
- Prefijo: prompt medio **67.258** tokens (p50 74.651, máx 128.948); **hit 93,3 %** → ~4.536 tokens nuevos por consulta; el miss es el **44,4 %** del coste con solo el 6,7 % de los tokens de entrada.

## 4. Palancas y techo (7 d)

- A1 salida −30 % = **1,11 USD** (cap en p90 = 0,66)
- A2 miss −30 % = **1,19 USD**
- A4 mover todo el pico a valle = **0,94 USD** (parcialmente evitable: es la franja real de trabajo)
- Suma simple de A1+A2+A4 = 3,24 USD → **infla** (ver §5). **Techo apilado = 2,6819 USD/ventana = 0,3831 USD/día.**
- Con el techo, a ritmo del ledger: 1,81 → 2,50 días. **A ritmo real (2,696 USD/día): 22 h → 26 h.** El recorte técnico cambia poco: lo que corta el servicio es el saldo.

## 5. Lo que NO cuadra (abierto, no se toca el instrumento)

- **La tarifa es correcta**: verificada hoy contra `api-docs.deepseek.com/quick_start/pricing` → hit 0,003 / miss 0,15 / out 0,60 USD por 1 M en valle; **pico ×2** en 01:00–04:00 y 06:00–10:00 UTC de lunes a viernes. `deepseek-v4-flash` es nombre heredado servido por DeepSeek-V4.1-Flash y facturado a precio Flash.
- **Pero el saldo cae ×1,84 más rápido que la estimación del ledger**, y el patrón se repite en dos ventanas independientes:
  - W1 (11-oct 22:45:35 → 12-oct 07:00:45): saldo −0,38 USD vs ledger 0,2213 → **×1,72**
  - W2 (12-oct 07:00:45 → 15:12:30): saldo −1,44 USD vs ledger 0,7909 → **×1,82**
  - Global (16,56 h): saldo −1,86 USD vs ledger 1,0122 → **×1,84**
- Los datos de tokens de la ventana están **completos** (479/479 líneas con `usage`, 1 sin él = 0,2 %) y todas las llamadas son `deepseek-v4-flash`/`deepseek`. No es tráfico perdido del ledger.
- Hipótesis **sin resolver** (ninguna descartada):
  - **H1**: la API factura tokens que `usage` no reporta como salida — V4.1-Flash va en modo pensamiento por defecto y `hermes-lab/observability/pipeline_proxy.py` guarda solo 4 campos de `usage` (`prompt_tokens`, `completion_tokens`, `prompt_cache_hit_tokens`, `prompt_cache_miss_tokens`).
  - **H2**: facturación efectiva a tarifa de pico en más franjas de las asumidas (la realidad medida ≈ 90 % del hipotético «todo a pico»).
  - **H3**: consumo con la misma clave fuera del proxy.
- **Prueba decisiva pendiente**: re-exportar de la consola los CSV de uso (`amount` y `cost`) de un día reciente y cruzar tokens × coste del mismo día. Requiere **login del usuario**; el último export acaba el 10-ago.

## 6. Factura real exportada (referencia)

- `USAGE/extraido/cost-2026-06-27_2026-07-27.csv`: flash 6,8163 + pro 7,5905 = **14,4068 USD**
- `USAGE/extraido/cost-2026-07-12_2026-08-10.csv`: flash 24,2120 + pro 11,6886 = **35,9006 USD**
- Total exportado **50,31 USD** (jul–ago, `wallet_type: Paid`). No cubre septiembre–octubre.
- El export de `amount` de ese periodo trae **un solo total de tokens por día** (sin desglose hit/miss), así que no permite separar el efecto del caché: sirve para totales, no para validar la tarifa por tramos.

## 7. Acciones

1. **Recargar saldo** — es lo único que evita el corte a ~22 h.
2. **No programar trabajo cloud en 08-12 h L-V** (30 % del gasto; 08:00 sola = 19,5 %), y preferir 00-07 h (a cero hoy) para lotes.
3. Re-exportar los CSV de uso para cerrar la causa del ×1,84.
4. **No modificar** `tools/desglose_coste.py` hasta validar (RULE-015); el techo doble-contado está propuesto en `04-operations/backlogs/pendientes.md`.

## Reproducir

```bash
cd /home/jokoalmi/joko-lab
/usr/bin/python3 tools/desglose_coste.py --dias 7
/usr/bin/python3 tools/desglose_coste.py --dias 30
# saldo real (solo lectura; la clave se lee de ~/.hermes/.env y no se imprime):
#   GET https://api.deepseek.com/user/balance  con Authorization: Bearer $DEEPSEEK_API_KEY
```

Estimación con la tarifa oficial aplicada al ledger, **no la factura**. El contraste con el saldo real indica que la estimación es ~1,8× baja.
