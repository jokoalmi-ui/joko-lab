# F1 — Coste en tokens del contexto fijo (perfil default)

- Instrumento A (bloques): `usage.prompt_tokens` de LM Studio · `openai/gpt-oss-20b` · `127.0.0.1:1234/v1`
- Instrumento B (nativo): `hermes prompt-size --platform telegram --json` (offline, sin llamadas al modelo)
- Piezas recolectadas: 2026-09-16T23:00:47+02:00 · offset framing: 71 tok (A) / 67 tok (B, texto vacio)
- Etiqueta de validez: **fraccion por bloque valida; el total es cota inferior del prompt cloud**
- Instrumento F1.1: VALIDADO (V1 varianza 0 · V2 +520/+520 dev 0,00% · V3 offset 71 · V4 informativo · V5 suelo real 1.009 tok)

## Bloque A — reconstruccion por ficheros (F1.2)

| bloque | chars | tokens netos | % del fijo | chars/token |
|---|---|---|---|---|
| B1_soul | 20235 | 5131 | 27.9% | 3.94 |
| B2_memorias | 4342 | 1459 | 7.9% | 2.98 |
| B3_skills (indice reconstruido, 205 SKILL.md) | 47437 | 11793 | 64.1% | 4.02 |
| B5_mcp | no_calculable en esta via | — | — | — |

Total reconstruido: **18.383 tok netos** (acumulado 18.386, Δ 3 tok = 0,016% → aditivo).
B3 reconstruido SOBRECUENTA: el snapshot real de runtime tiene **165 skills**, no 205.

## Bloque B — medicion NATIVA (F1.5, la que vale)

| pieza | chars | tokens |
|---|---|---|
| system_prompt completo | 52.534 | 13.136 → 13.069 neto |
| tools (26 esquemas) | 43.288 | 10.290 → 10.223 neto |
| **FIJO TOTAL (sin MCP arrancados)** | 95.822 | **23.292 tok netos** |
| — indice de skills | 16.450 B | 4.020 (17,3% del fijo) |
| — SOUL+guia+memoria+perfil | — | 9.049 |

Reparto: tools **43,9%** · system **56,1%** (del que skills 31%).
El indice real es PLANO: 163 entradas, 83,9 B/linea, max 99 B. Las descripciones ya cumplen tope 60 chars.
La palanca del indice tiene techo ~2.300 tok (-10%); quitar descripciones de categoria solo -2,4%.

## F1.4 — MCP (CERRADO, 2026-09-16 23:20)

Fuentes reales, sin arrancar ningun servidor:
- `~/.hermes/cache/mcp_schema_cache.json` → 25 tools MCP en 3 servidores (animation-server 6, lab-db 13, lancedb 6), 8.653 B
- `~/.hermes/sessions/request_dump_20260914_172635_d00cc0_...json` → request HTTP real (14-sep 22:33): system 55.157 chars, 20 tools (37.389 chars), tool_search con catalogo completo (2.697 chars, 25 lineas `mcp__`)
- config: `tools.tool_search = {enabled: auto, threshold_pct: 10, search_default_limit: 5, max_search_limit: 20}`

| pieza | chars | tokens |
|---|---|---|
| catalogo real (25 MCP + 4 nativas) | 2.697 | 793 |
| catalogo base (solo 4 nativas) | 454 | 174 |
| **coste MCP hoy (diferencia)** | 2.242 | **619** |
| 25 esquemas MCP COMPLETOS (contraste) | 6.900 | 1.973 |
| FIJO real de la sesion del 14-sep (system+tools) | 92.546 | 22.800 |

**Hallazgo:** los 3 MCP YA estan en carga bajo demanda. El catalogo no vive en el system prompt
sino en la **descripcion de la tool `tool_search`** (por eso `system_prompts` tiene 0 filas con `mcp__`).
Ahorro ya aplicado: 619 tok en lugar de 1.973 → **-1.354 tok (-68,6%)**.
Cambiar al modo `summary`/`names` ahorraria ~500 tok mas (-2% del fijo): no compensa.

## Reparto final del fijo (perfil default, 23.292 tok)

- tools nativas: **10.223 tok (43,9%)** ← palanca mayor; `delegation` sola = 1.050 tok
- system prompt sin skills: 9.049 tok (38,8%)
- indice de skills: 4.020 tok (17,3%) ← techo de poda ~2.300 tok
- MCP: 619 tok (2,7%) ← ya optimizado

> Sin recomendacion de poda a priori: umbral se fija DESPUES del baseline (RULE-015).
> No se ha escrito nada en `~/.hermes` ni en el lab. Todo en `/tmp/f1-contexto/`.
