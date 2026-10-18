# EXP-20260916-007 — F2 celda B(T2): MTP en llama.cpp y LM Studio (modo supervisado / swarm)

- **Fecha**: 2026-09-16, ventana **15:39:41 → 16:01:17 CEST** (cierre del sintetizador 16:01:17).
- **Tenant**: `exp007-f2-t2`. Root `t_1f24382f` · worker `t_93752865` (investigador-mtp) · verifier `t_a48a64df` (**PASS**) · synthesizer `t_c6eabd9c`.
- **Objetivo**: idéntico al de la celda A(T2) (fecha de introducción, flags exactos, requisitos de motor, límites; fuentes oficiales con cita literal).

## Coste y latencia (medidor `/tmp/exp007_coste.py`, tarifa oficial)

| métrica | valor |
|---|---|
| llamadas en la ventana | **183** |
| prompt tokens | 13.204.353 (hit 12.720.512 / miss 483.841) |
| completion tokens | 135.389 |
| **coste** | **0,191971 USD** |
| ttfb_total | 164,7 s |
| total_ms_total | 807,4 s |
| franja | 183/183 off-peak |
| líneas sin desglose de caché | 4 → coste declarado como **cota superior** |
| status ≠ 200 | 3 |

**Ruido declarado**: la ventana incluye el tráfico de mi propia sesión (≈4 turnos del asistente). No se puede separar con el esquema real del ledger (no hay `task_id`); el delta es de orden de magnitud muy superior a mi tráfico.

## Calidad (medidor `/tmp/exp007_calidad.py`, criterio objetivo)

- Claims externos verificados **en vivo**: **8 PASS** de 8 reales = **100 %** (tras corregir el instrumento a v3; el v2 marcaba 5/8 por falsos negativos, ver `f2-instrumento-correccion-v3.md`). Los 3 de `api.github.com` pasaron al restablecerse el cupo de la API.
- **3 claims bloqueados por el instrumento**: `ANTIBOT_NO_VERIFICABLE_POR_CURL` (HTTP **403**) sobre `api.github.com`. **Diagnóstico**: `GET /rate_limit` → `limit=60, remaining=0, reset 16:37:35` → es **rate limit del medidor** (API sin token), **no un fallo del informe**. Reintento a las 16:36:39 (aún dentro del bloqueo) → 403×3; verificados en vivo tras el reset.
- **0 claims con contenido no encontrado** en las URLs vivas.
- **Control negativo** (cita inventada sobre el changelog de LM Studio): **correctamente no encontrada** → el instrumento discrimina.
- Dos de los tres bloqueados (hash del merge y frase del body del PR) **sí constan en el crudo archivado** `evidence/gh_pr22673.json` del propio entregable.

## Integridad del entregable (verificación independiente)

- `sha256sum -c manifest-sha256.txt` tras reconstruir la disposición (`evidencia/evidence/…`): **32/32 OK, 0 FAILED** (31 ficheros de evidencia + el documento de síntesis).
- Hashes del worker recomputados y **coincidentes byte a byte**: informe `f281df11…`, tarball `00fe3728…`.
- La **última línea del manifiesto** es el sha256 real de la síntesis (`0524625e…`); el `77d88bff…` que figura en el cuerpo del texto es de una versión previa (el propio texto lo advierte y remite al manifiesto).
- Cita clave contrastada contra el crudo: `common_speculative.cpp:37` = `{"draft-mtp",     COMMON_SPECULATIVE_TYPE_DRAFT_MTP},`.

## Aportaciones que la celda A(T2) no tenía

1. **Primer build con MTP identificado: `b9180`**, cerrado con método reproducible (el listado de releases está topado en 1000 resultados, pero `/tags` paginado + `compare b9180...<merge>` → `status=identical`).
2. **Nombre del flag aclarado**: `draft-mtp` desde el commit del merge; los textos con `--spec-type mtp` son previos al merge.
3. **Corrección de atribución**: el `llama.cpp 2.22.1 runtime` pertenece a la página de **0.4.17**, no a 0.4.14. El MTP de 0.4.14 **no declara** versión de motor.
4. **Negativo reproducible**: `grep -c -i 'MTP'` = **0** en la doc oficial de speculative decoding (re-verificado por mí: HTTP 200, 159.047 bytes, 0 ocurrencias).
5. Cobertura de las páginas 0.4.15–0.4.24 (MTP solo en 0.4.14 y 0.4.22).

## Defectos que el propio swarm declara (no invalidan hechos)

- El informe del worker listaba 16 hashes: 3 ficheros no viajaban en el tarball y 18 de los 31 no tenían hash → el manifiesto del sintetizador lo cierra.
- Desviación de 1-2 líneas en dos rangos citados (`arg.cpp:3080`, `speculative.cpp:37`); el contenido citado es correcto.
