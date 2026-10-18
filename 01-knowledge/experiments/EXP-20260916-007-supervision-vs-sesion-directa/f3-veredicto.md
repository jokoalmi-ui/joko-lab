# EXP-20260916-007 — F3 VEREDICTO

**Experimento**: «Supervisión multiagente (swarm) vs sesión directa» — ¿mejora la calidad verificada lo suficiente para justificar su coste?
**Hipótesis H-EXP-007**: el modo supervisado **no mejora la calidad verificada** y **sube coste y latencia**.
**Diseño**: 3 tareas idénticas (T1 precios oficiales, T2 MTP en llama.cpp/LM Studio, T3 MoE 22,6 GB en 12 GB de VRAM), cada una ejecutada en modo A (sesión directa) y modo B (swarm worker→verifier→synthesizer), mismo modelo (`deepseek-v4-flash`, tarifa oficial peak/off-peak).
**Fecha**: 2026-09-16. **Veredicto**: **H-EXP-007 CONFIRMADA (3/3 tareas)**, con dos matices que el instrumento no captura.

## Las 3 métricas por celda (datos medidos)

| tarea | modo | llamadas | prompt tokens | coste USD | total_ms | reloj | calidad (claims reales) | control negativo |
|---|---|---|---|---|---|---|---|---|
| **T1** precios | A | 4 | 329.484 | 0,007316 | 35,2 s | 0,8 min | **8/8 = 100 %** | ✔ no encontrada |
| | B | 33 | 1.339.710 | 0,030860 | 135,3 s | 3,9 min | **3/3 = 100 %** | ✔ no encontrada |
| **T2** MTP | A | 22 | 1.825.839 | 0,036340 | 148,3 s | — | **4/4 = 100 %** | ✔ no encontrada |
| | B | 183 | 13.204.353 | 0,191971 | 807,4 s | 21,6 min | **8/8 = 100 %** | ✔ no encontrada |
| **T3** MoE | A | 6 | 440.074 | 0,012867 | 46,2 s | 1,9 min | **9/9 = 100 %** | ✔ no encontrada |
| | B | 135 | 9.559.678 | 0,214731 | 899,0 s | 18,0 min | **12/12 = 100 %** | ✔ no encontrada |

## Ratios B/A (sobrecoste del modo supervisado)

| tarea | llamadas | coste | latencia (total_ms) | calidad |
|---|---|---|---|---|
| T1 | ×8,3 | **×4,22** | ×3,8 | iguales (100 %) |
| T2 | ×8,3 | **×5,28** | ×5,4 | iguales (100 %) |
| T3 | ×22,5 | **×16,7** | ×19,5 | iguales (100 %) |

**El sobrecoste crece con la profundidad documental de la tarea**: ×4,2 en la consulta factual corta → ×16,7 en la investigación larga con evidencia externa.

## Lo que sostiene la hipótesis

1. **La calidad verificable no mejora en ninguna de las 3 tareas**: 100 % de claims reales PASS en ambos modos, **0 alucinaciones** en las 6 celdas. Con el instrumento corregido, **B no es peor que A en ninguna celda, pero tampoco mejor**.
2. **El coste sube ×4,2 a ×16,7** con el mismo modelo y la misma pregunta.
3. **La latencia sube ×3,8 a ×19,5** (y el ttfb ×8 a ×2.978 por el dispatcher de 60 s y los tres saltos secuenciales).

## Los dos matices (no los captura el instrumento)

1. **B sí aporta verificación de tercer orden.** En T3 detectó y corrigió **dos errores de su propio informe** y **contradijo la guía de HuggingFace con el código** (dirección de conteo de `--n-cpu-moe`: la guía dice «desde las más altas», el código y el ejemplo de la propia guía dicen «las primeras N»). A(T3) se quedó con la advertencia de la guía sin contrastarla. En T2 corrigió una atribución de versión y el nombre de un flag. **El instrumento mide tasa de veracidad, no capacidad de detección**: un informe sin errores propios y sin errores ajenos detectados puntúa igual que uno sin errores propios pero que además tumba una fuente.
2. **La latencia de B no compite con el tiempo del usuario** si se lanza en segundo plano: el swarm de T3 trabajó 18 min **mientras yo ejecutaba la prueba empírica** en la misma máquina. El coste real de B es **monetario y de céntimos** (0,031–0,215 USD), no de atención.

## Umbral de uso (fijado DESPUÉS del baseline, RULE-015)

- **Consultas factuales simples (T1)**: **NO** usar swarm. ×4,2 de coste por menos cobertura (3 claims frente a 8) y sin valor de auditoría.
- **Investigación documental con muchas fuentes externas (T2/T3)**: swarm **solo** si se quiere explícitamente la capa de auditoría — gate de verificación con re-fetch al commit exacto, manifiesto de evidencia y lista declarada de lo **no** verificado. Sobrecoste absoluto: **0,02–0,20 USD por tarea**.
- **Regla práctica**: usar swarm cuando un error no detectado cueste **más de ~10× el coste de la consulta directa** (≈ 0,1–0,4 USD) o cuando la decisión sea difícil de revertir. Para todo lo demás, sesión directa.
- **Lanzarlo siempre en background** para no consumir tiempo de sesión.

## Hallazgos colaterales de F2

1. **Artefacto del instrumento (v2 → v3)** — el medidor de calidad borraba tramos de las fuentes de código al tratar los `<`/`>` de C++ como etiquetas HTML. Generaba falsos negativos **sesgados contra B** (informes más largos, más código citado): B-T2 5/8 → **8/8**, A-T3 8/10 → **9/10**, B-T3 11/12 → **12/12**. Sin validar la métrica, el veredicto se habría firmado con un artefacto propio. Ver `f2-instrumento-correccion-v3.md`.
2. **Prueba empírica del MoE de 22,6 GB** (`f2-A-T3-empirico.md`): con `-ngl 99 -ncmoe 24` el modelo **arranca** en 12 GB (VRAM pico 11.068 MiB) a **1,44 tok/s** (×3,9 sobre CPU puro, 0,37 tok/s); con `-ncmoe 20` **no arranca** (`cudaMalloc` OOM pidiendo 11.303 MiB en un buffer). **Conclusión: el offload sirve para arrancar, no para trabajar.** Y el bloque MTP del GGUF (504,4 MB) no cuesta VRAM si no se usa speculative decoding.
3. **Los claims bloqueados por `api.github.com`** (403, rate limit 60/h sin token) se resolvieron **verificados en vivo** (HTTP 200 + cita literal) tras el reset del cupo. El reintento programado despertó a las 16:36:39 (56 s antes del reset) y aún dio 403×3; la re-medición posterior los pasó.

## Límites declarados de este veredicto

- **Modelo único**: todo medido con `deepseek-v4-flash` cloud. No se probó otro modelo ni modelo local.
- **Coste como cota superior** en B: la ventana del medidor incluye mi propio tráfico de sesión y hay 4 líneas sin desglose de caché contadas como *miss*.
- **Instrumento de calidad** = «citable y verificable con `curl`», **no** profundidad, cobertura ni utilidad. El número de claims por celda no está normalizado (8 vs 3 en T1).
- **3 tareas, 1 ejecución por celda**: sin repeticiones, no hay intervalo de confianza. Los ratios son de una sola muestra.
- **Contaminación temporal**: los pares T2 y T3 se solaparon con trabajo mío en paralelo (incluida la prueba empírica del MoE).

## Cierre

- F0 cerrado (contrato antes de medir) · F1 PASA · **F2 cerrado: pares T1, T2 y T3 completos** · **F3 emitido**.
- Evidencia: `f2-A-T1.md`, `f2-par-T1.md`, `f2-A-T2.md`, `f2-B-T2.md`, `f2-par-T2.md`, `f2-A-T3.md`, `f2-B-T3.md`, `f2-par-T3.md`, `f2-A-T3-empirico.md`, `f2-instrumento-correccion-v3.md`.
- JSON de medición (crudo): `/tmp/exp007/{coste,calidad,claims}-*.json` y `/tmp/exp007/v3/`.
