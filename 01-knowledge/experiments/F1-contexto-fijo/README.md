# F1 — Archivo del experimento: coste del contexto fijo del perfil `default`

**Cerrado:** 2026-09-16 23:25 CEST · **Informe de corte:** `04-operations/reports/2026-09-16-f1-coste-contexto-fijo-corte.md`
**Estado:** cerrado con dato · **Futurible derivado:** F1-bis (medir uso real por toolset)
**Coste:** 0 € (todo local, `gpt-oss-20b` como tokenizador) · **`~/.hermes` modificado:** no

## Resultado en cinco líneas

- Fijo del perfil `default` = **23.292 tok netos** (23.426 brutos − 67 de framing).
- **Tools nativas 10.223 tok (43,9%)** vs system prompt 13.069 tok (56,1%).
- Dentro del system prompt: índice de skills 4.020 tok (17,3% del fijo), SOUL+memorias+perfil 9.049 tok.
- **Los 3 MCP ya van en carga bajo demanda: 619 tok (2,7%)**, no 1.973 (esquemas inline) → −68,6% ya aplicado.
- Conclusión: **la palanca son las tools nativas** (`delegation` sola = 1.050 tok ≈ 26% del índice de skills completo); el índice no se poda (techo ~−10%).

## Material

**Plan y resultados**

- `PLAN-F1.md` — plan del experimento (fases F1.0–F1.5, instrumentos, criterios).
- `RESULTADOS.md` — consolidado de F1.2 + F1.5 + F1.4.
- `mediciones.json`, `fijo_real.json`, `mcp_real.json`, `validacion_instrumento.json`, `ledger_baseline.json` — salidas crudas.
- `prompt_size_telegram.json`, `prompt_size_cli.json` — salida nativa de `hermes prompt-size` (solo métricas: chars/bytes por sección, skills y toolsets).

**Instrumentos (scripts, todos de solo lectura sobre `~/.hermes`; no escriben nada)**

- `recolectar.py` — F1.0: recolecta las piezas del fijo desde disco (`SOUL.md`, memorias, perfil, `config.yaml`, snapshot de skills).
- `validar_instrumento.py` — F1.1: V1 determinismo, V2 linealidad, V3 offset, V4 perfil de contenido, V5 suelo real del ledger.
- `medir_bloques.py` — F1.2: mide el fijo por bloques reconstruidos (cota inferior); `--con-mcp` añade el bloque MCP.
- `medir_fijo_real.py` — F1.5: mide el texto volcado por el instrumento nativo, tokenizado en local.
- `medir_mcp.py` — F1.4: coste real de los MCP desde `cache/mcp_schema_cache.json` + request persistido, sin arrancar servidores.
- `leer_ledger.py` — F1.3: distribución de referencia del ledger del proxy.
- `sanear_y_verificar.py` — saneado de `piezas.json` al archivar + verificación por md5 de esta copia.

**Volcados medidos**

- `fijo/skills_index.txt` — índice de skills renderizado (16.450 B, 163 entradas).
- `fijo/tools.json` — JSON de los esquemas de las 26 tools nativas.
- `fijo/catalogo_real.txt` / `fijo/catalogo_base.txt` — catálogo deferred con los 25 MCP / solo las 4 nativas.
- `fijo/mcp_completos.json` — esquemas completos por servidor MCP.
- `piezas.json` — piezas reconstruidas. **Con dos piezas redactadas** (ver abajo).

## Qué NO está aquí, y por qué

La copia se hizo con criterio de datos personales (el lab se sincroniza a la nube). Excluidos del archivo:

- `fijo/system_prompt.txt` — 53.489 B, md5 `7c8dd4ab4623e1d37c933d8166f6a7fb`
- `fijo/session_prompt.txt` — 51.411 B, md5 `4c49e2d3c2444440a00624bd3e52c14f`
- `piezas.json` (original) — 196.077 B, md5 `17b17a1eb5e1f857525557833ca81cbf`

Los dos primeros son volcados del system prompt que incluyen `MEMORY.md` y `USER.md` literales (no son idénticos entre sí; ninguno contiene al otro). Del tercero se archivó una copia con `B2_memoria` y `B2_user` redactadas — el `_meta.archivado` del fichero declara qué se quitó y el md5 del original.

Regenerables sin arrancar nada:

```bash
~/.hermes/hermes-agent/venv/bin/hermes prompt-size --platform telegram --json   # -> prompt_size_*.json
cd /tmp/f1-contexto && python3 recolectar.py                                    # -> piezas.json
```

## Verificación de esta copia

20 ficheros copiados tal cual: **md5 origen == md5 destino, 20 correctas / 0 desajustes**
(`python3 sanear_y_verificar.py`, 2026-09-16 23:27:48 CEST). Los volcados excluidos quedan identificados por md5 arriba.
