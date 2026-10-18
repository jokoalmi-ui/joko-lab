---
type: instrument
subtype: instrument
status: index
tags: [instrument, rate-limits, coste, observabilidad]
created: 2026-10-11
---

# Rate Limits v0.1 — Instrumento científico

## Restricción constitucional

Este script **NO modifica absolutamente nada.**

- No toca `pipeline_proxy.py` ni la config de Hermes.
- No bloquea, no limita ni no reintenta llamadas.
- No cambia umbrales ni propone políticas.
- No escribe fuera de su propia carpeta `outputs/`.

Su única misión es **observar, medir y registrar**.

## Propósito real

Cerrar el hueco declarado el 11-oct-2026 (cruce del reel `DeCI09WTN51`, término
«Rate Limits» = único de los 20 sin instrumento). Preguntas que responde:

1. ¿Cuántos frenos reales ha habido y de qué familia (cuota / auth / ritmo / red / cliente)?
2. ¿Cuál es la ráfaga máxima observada (RPM y TPM) y cuándo ocurrió?
3. ¿Los errores generan llamadas duplicadas (bucle de reintentos) y cuánto cuestan?
4. ¿Hay backoff de facto? ¿Cuánto se tarda en volver a llamar tras un fallo?
5. ¿Cuál es el saldo/margen real de la cuenta? (única fuente de cuota medible)

## F0 — descubrimiento de cabeceras (11-oct-2026, medido)

Antes de definir métricas se comprobó **qué emite el proveedor de verdad**:

```
GET  https://api.deepseek.com/user/balance          -> HTTP 200
     {"is_available":true,"balance_infos":[{"currency":"USD",
      "total_balance":"5.39","granted_balance":"0.00","topped_up_balance":"5.39"}]}
POST https://api.deepseek.com/v1/chat/completions   -> HTTP 200
     cabeceras_de_interes = NINGUNA
```

**Resultado: DeepSeek NO envía cabeceras `x-ratelimit-*` ni `retry-after`.**
Cabeceras presentes: `Connection, Content-Length/Transfer-Encoding, Content-Type,
Date, Server, Strict-Transport-Security, Via, X-Amz-Cf-*, X-Cache,
X-Content-Type-Options, access-control-allow-credentials, vary, x-ds-trace-id`.

Consecuencias:
- **La fase «capturar cabeceras de rate limit en el proxy» queda DESCARTADA por
  medición**, no por opinión: no hay nada que capturar.
- El **saldo** (`GET /user/balance`, no consume tokens) es la única fuente real
  de cuota. Es la que se vigila.

## Evidencia acumulada (línea base 11-oct-2026)

Sobre `04-operations/metrics/pipeline_obs.jsonl` (53.299 líneas, 15,8 MB,
2026-08-06 → 2026-10-11):

```
status={'200': 50272, '404': 2920, '400': 64, '0': 25, '401': 13, '402': 5}
frenos_reales=104        ruido /api/show=2923 (sonda de estilo Ollama)
  por_familia={'cliente': 66, 'auth': 9, 'cuota': 5, 'red': 24}
  tokens_gastados_en_fallos=0
ritmo: rpm_max=34 (2026-10-08T21:30)  tpm_max=7.914.755 (2026-08-09T23:22)
rafagas_identicas>=3: n=1 lineas=6
espera_tras_error_s: n=104 min=0.00 p50=3.00 max=27242.0
saldo=5.37 USD (disponible=True)
```

Hallazgos:

- **0 × HTTP 429 en toda la historia.** El ritmo de peticiones nunca ha sido
  frenado por el proveedor. El «rate limit» real del lab NO es de velocidad.
- **5 × HTTP 402 (cuota/saldo), todos el 18-ago-2026 entre 18:47 y 18:55** —
  un único incidente de ~8 min. Ese es el freno duro que sí ocurrió.
- **9 × 401** (auth), **24 × status 0** (red; 21 de ellos `[Errno -3] Temporary
  failure in name resolution`), **66 × 400** (petición inválida).
- **`tokens_gastados_en_fallos = 0`**: las llamadas frenadas no facturan tokens.
  El coste del freno es tiempo perdido y consulta caída, no dinero.
- **Sin backoff explícito**: p50 = 3 s entre error y siguiente llamada; el máximo
  (27.242 s) es el hueco natural entre una incidencia y la sesión siguiente.
- **El ledger NO registra ninguna cabecera de cuota** (`NINGUNO`), coherente con F0.

## Cómo se valida este instrumento (RULE-015)

El medidor debe **redescubrir dos hechos conocidos** o está roto:

1. El incidente `5 × 402` del **18-ago-2026** (18:47–18:55).
2. El pico **TPM = 7.914.755** del **09-ago-2026 23:22**.

**Ningún umbral a priori.** `--min` es un umbral OPCIONAL declarado por el usuario;
por defecto no hay umbral y el instrumento solo informa.

## Uso

```bash
cd /home/jokoalmi/joko-lab/instruments/rate-limits
python3 medir_rate_limits.py                     # informe por stdout
python3 medir_rate_limits.py --json outputs/rate-limits-$(date +%Y%m%d).json
python3 medir_rate_limits.py --saldo --min 2     # + saldo real; aviso si baja de 2 USD
python3 medir_rate_limits.py --watchdog 24       # silencio si no hay frenos en 24 h
```

## Output

- `outputs/rate-limits-YYYYMMDD.json` — informe estructurado (ledger, frenos,
  ritmo, reintentos, cabeceras, watchdog, saldo).
- `outputs/saldo.jsonl` — append: una línea por consulta de saldo
  (`ts`, `is_available`, `currency`, `total_balance`). Traza histórica de cuota.

## Límites honestos

- El ledger **no tiene campo de sesión**: no se puede atribuir un freno a una
  tarea concreta, solo a su instante.
- La firma de ráfaga (`model` + `prompt_tokens` + `completion_tokens`) es
  estricta: un bucle con contexto creciente **no** la activa; el nº de ráfagas
  es una cota inferior, no el total.
- Detectar no es prevenir: este instrumento no evita el 402, lo ve.
- El saldo es el de la cuenta completa, no el de un canal o tarea.

## Roadmap

- v0.2 (si el usuario lo pide): agrupar por rachas (>60 s) y dar RPM/TPM por
  sesión, no solo el máximo global.
- v0.3 (si se autoriza): cron watchdog `no_agent` cada 6 h con `--watchdog 6
  --saldo --min <umbral declarado por el usuario>`, entrega Telegram.
