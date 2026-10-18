# EXP-20260916-007 — F2 par T1: sesión directa (A) vs swarm (B)

- **Tarea T1** (idéntica en ambos modos): precios y límites oficiales vigentes de la API DeepSeek.
- **Mismo modelo** (`deepseek-v4-flash` cloud en el ledger; hoy servido por V4.1-Flash). Tarifa oficial 2026-09-16.
- **Fecha**: 2026-09-16. A: 16:09:30 → 16:10:16. B: tenant `exp007-f1` (gate F1), 15:31 → 15:34:54.

## Tabla comparativa

| métrica | A — sesión directa | B — swarm (F1) | ratio B/A |
|---|---|---|---|
| llamadas al modelo | 4 | 33 | ×8,3 |
| prompt tokens | 329.484 | 1.339.710 | ×4,1 |
| **coste (USD)** | **0,007316** | **0,03086** | **×4,22** |
| ttfb_total | 3,6 s | 24,6 s | ×6,8 |
| total_ms_total | 35,2 s | 135,3 s | ×3,8 |
| reloj (min) | 0,77 | 3,9 | ×5,1 |
| **tasa_pass (claims reales)** | **8/8 = 100 %** | **3/3 = 100 %** | iguales |
| control negativo | no encontrado ✔ | no encontrado ✔ | — |
| líneas sin desglose de caché | 0 | 4 (cota superior) | — |
| claims verificados entregados | **8** | 3 | — |

## Lectura (sin fijar umbral: eso es F3)

1. **Otra vez: la calidad verificable no separa los modos** → 100 % en ambos, **0 alucinaciones** en los dos.
2. **B cuesta ×4,2 y tarda ×3,8-6,8** para la misma tarea.
3. **A entregó más claims verificados (8 vs 3)** en esta tarea: la ventaja de B **no es cobertura aquí**, es el reparto de trabajo.
4. **La celda A encontró el mismo hallazgo material** que el swarm (el cambio de modelo a `deepseek-flash`/V4.1-Flash y la tabla vigente) y además detectó y **corrigió su propio error de cita** dentro de la celda.
5. Recordatorio de limitación ya anotada en el par T2: el instrumento mide *verificable y citable*, no *profundidad*; y el número de claims por celda no está normalizado.
