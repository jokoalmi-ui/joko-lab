# EXP-20260916-007 — F2 par T2: sesión directa (A) vs swarm (B)

- **Tarea T2** (idéntica en ambos modos): MTP (multi-token prediction) en llama.cpp y en LM Studio: en qué versión/fecha se introdujo, flags exactos de activación, requisitos de versión del motor y límites conocidos, con fuentes oficiales y cita literal.
- **Mismo modelo en ambos modos**: `deepseek-v4-flash` (cloud). Tarifa oficial de referencia (peak/off-peak).
- **Fecha**: 2026-09-16. A: sesión directa (4 turnos). B: swarm `exp007-f2-t2`, ventana 15:39:41 → 16:01:17.

## Tabla comparativa (3 métricas del contrato)

| métrica | A — sesión directa | B — swarm | ratio B/A |
|---|---|---|---|
| llamadas al modelo | 22 | 183 | ×8,3 |
| prompt tokens | 1.825.839 | 13.204.353 | ×7,2 |
| completion tokens | 27.153 | 135.389 | ×5,0 |
| **coste (USD, cota superior en B)** | **0,03634** | **0,191971** | **×5,28** |
| ttfb_total | 20,3 s | 164,7 s | ×8,1 |
| total_ms_total | 148,3 s | 807,4 s | ×5,4 |
| **tasa_pass (claims reales)** | **4/4 = 100 %** | **8/8 = 100 %** (v3) | **iguales** |
| control negativo (cita inventada) | no encontrada ✔ | no encontrada ✔ | — |
| fuentes sin desglose de caché | 0 | 4 (cota superior) | — |
| extensión del entregable | 11 líneas / 4 claims | **290 líneas / 20.563 B** + 31 ficheros de evidencia + manifiesto sha256 32/32 | — |

## Lectura (sin fijar umbral: eso es F3)

1. **La calidad verificable no mejora**: en ambos modos, todo claim comprobable pasa; **0 alucinaciones detectadas** en los dos. La tasa_pass es equivalente.
2. **El coste sube ×5,3 y la latencia ×5,4–8,1** con el mismo modelo. La latencia de B está inflada por el dispatcher de 60 s y por tres saltos secuenciales (worker → verifier → synthesizer).
3. **B entrega más cobertura y más auditoría**, no más veracidad: identificó el build `b9180`, aclaró el nombre del flag, corrigió una atribución de versión y aportó un **manifiesto sha256 de 31 ficheros verificable** (32/32 OK). Eso es volumen y trazabilidad, no exactitud adicional.
4. **Limitación del instrumento de calidad**: mide *verificable y citable*, no *profundidad ni cobertura*. Comparar 4 claims contra 8 claims favorece artificialmente al que cita menos. Para F3 hay que igualar el número de claims por celda (o normalizar por claim).
5. **Limitación del instrumento de coste**: la ventana incluye mi propio tráfico (≈4 turnos) y 4 líneas sin desglose de caché → el coste de B es **cota superior**, nunca 0.

## Estado de los 3 claims bloqueados — RESUELTO

- Se etiquetaron `ANTIBOT_NO_VERIFICABLE_POR_CURL` (403 de `api.github.com` sin token, `remaining=0`).
- El reintento programado despertó a las **16:36:39** (56 s antes del reset) y volvió a dar 403×3 → después, ya con el cupo restablecido, los tres quedaron **verificados en vivo**.
- La **re-medición con el instrumento v3, ya con el cupo restablecido, los verificó en vivo: HTTP 200 + cita literal exacta** → **B(T2) cerrado con 8/8 claims reales PASS (100 %)**.
- El artefacto era del instrumento (rate limit), nunca un fallo del informe: el hecho central (fecha de merge `2026-05-16T12:06:24Z`) ya había pasado como claim 1.

## Nota de instrumento (v2 → v3)

La tasa de esta celda pasó de **5/8** a **8/8** al corregir el medidor (ver `f2-instrumento-correccion-v3.md`): el v2 borraba tramos de las fuentes de código al tratar los `<`/`>` de C++ como etiquetas HTML, generando falsos negativos concentrados en los informes del swarm (más largos y con más código citado). El sesgo del instrumento **penalizaba a B**.
