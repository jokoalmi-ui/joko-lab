# EXP-20260916-007 — F2 par T3: sesión directa (A) vs swarm (B)

- **Tarea T3** (idéntica en ambos modos): servir un MoE de 22,6 GB (Qwen3.6-35B-A3B Q4_K_M) en una GPU de 12 GB por offload de capas, con fuentes oficiales y cita literal.
- **Mismo modelo en ambos modos**: `deepseek-v4-flash` (cloud), tarifa oficial peak/off-peak.
- **Fecha**: 2026-09-16. A: 16:10:44 → 16:12:37 (1,88 min). B: swarm `exp007-f2-t3`, 16:13 → 16:31 (18 min).

## Tabla comparativa (3 métricas del contrato)

| métrica | A — sesión directa | B — swarm | ratio B/A |
|---|---|---|---|
| llamadas al modelo | 6 | 135 | ×22,5 |
| prompt tokens | 440.074 | 9.559.678 | ×21,7 |
| completion tokens | 8.642 | 161.943 | ×18,7 |
| **coste (USD)** | **0,012867** | **0,214731** (cota superior) | **×16,7** |
| ttfb_total | 5,7 s | 16.934,2 s | ×2.978 |
| total_ms_total | 46,2 s | 899,0 s | ×19,5 |
| reloj (min) | 1,88 | 18,0 | ×9,6 |
| **tasa_pass (claims reales)** | **9/9 = 100 %** | **12/12 = 100 %** | iguales |
| control negativo (cita inventada) | no encontrado ✔ | no encontrado ✔ | — |
| líneas sin desglose de caché | 0 | 4 (cota superior) | — |
| extensión del entregable | 53 líneas / 1 informe | **253 líneas** + informe de worker 20.787 B + verificación 12.518 B + manifiesto de evidencia | — |
| correcciones propias aplicadas | 1 (claim 3, construcción de cita) | 2 obligatorias del gate + 5 residuales declarados | — |

## Lectura (sin fijar umbral: eso es F3)

1. **La calidad verificable vuelve a no separar los modos**: 100 % de claims reales en ambos, **0 alucinaciones**.
2. **El coste sube ×16,7 y la latencia ×9,6–19,5** con el mismo modelo. El ttfb_total de B (×2.978) no es comparable: incluye la espera del dispatcher de 60 s y tres saltos secuenciales.
3. **B aportó verificación de tercer orden**: no solo comprobó sus claims, sino que **detectó y corrigió dos errores de su propio informe** (una afirmación falsa sobre el gist y una equivalencia imprecisa sobre LM Studio) y **contradijo la guía de HuggingFace con el código** en la dirección de conteo de `--n-cpu-moe`. A(T3) aceptó la advertencia de la guía sin contrastarla con el código: ahí B fue **materialmente mejor**, no solo más caro.
4. **La ventaja de B en T3 es la auditoría, no la veracidad**: 12 claims citados y verificados frente a 9, un gate que re-verifica en vivo al commit exacto, y una lista explícita de lo que **no** se pudo verificar.
5. **Limitación del instrumento de calidad**: mide *verificable y citable*, no *profundidad*. El número de claims por celda no está normalizado (12 vs 9). Para F3 hay que leer la tasa, no el volumen.
6. **Limitación del instrumento de coste**: la ventana de B incluye mi propio tráfico de sesión → cota superior.

## Nota de instrumento (aplicada a TODAS las celdas)

El medidor v2 producía **falsos negativos** en fuentes de código (ver `f2-instrumento-correccion-v3.md`). Tras corregirlo y re-medir: A-T3 8/10 → **9/10**, B-T3 11/12 → **12/12**, B-T2 5/9 → **8/9**. Los claims que parecían fallar estaban literalmente en la fuente.
