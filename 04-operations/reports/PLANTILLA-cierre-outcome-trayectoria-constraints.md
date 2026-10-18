# PLANTILLA — Cierre de evaluación con la terna `outcome` + `trayectoria` + `constraints`

**Origen:** ítem **(B)** de `04-operations/backlogs/pendientes.md` (línea 626; encolado el 04-oct-2026).
**Versión:** v1.0 — 2026-10-11 CEST.
**Probada en un cierre real:** `04-operations/reports/2026-10-11-cierre-terna-tool-calling-qwen2.5-7b.md`.

**Regla dura:** todo cierre de evaluación o EXP declara los TRES bloques. Lo que no se midió se
declara `NO MEDIDO` + motivo. Nunca se rellena de memoria ni se deja en blanco.

---

## 1. Cuándo aplica

- Al cerrar cualquier evaluación o experimento del lab.
- El veredicto se emite **sobre la terna**, no solo sobre el resultado final.
- Alimenta el cierre con 2 campos nuevos para `04-operations/metrics/aplicabilidad_ledger.jsonl`
  (`trayectoria`, `constraints`) **o** con un anexo por EXP si el registro no es una pieza de vigilancia.

## 2. Bloque 1 — OUTCOME (¿qué salió?)

Obligatorio:
- Instrumento: ruta + tamaño + versión/comentario de versión.
- Set de casos: ruta + **hash** (sha256 o md5) → sin hash, el número no es reproducible.
- Modelo + backend + los parámetros que afectan a la comparabilidad (contexto, temperatura, seed, modo de razonamiento).
- Cifra: `pasan/total` y, por cada fallo, el **motivo literal** que emite el corrector.
- Distinguir **fallo de formato** de **fallo de contenido** cuando el caso lo permita.

## 3. Bloque 2 — TRAYECTORIA (¿cómo llegó al resultado?)

Por caso, mínimo obligatorio:
- `pasos` / nº de tool calls.
- `herramientas` (nombres elegidos).
- `argumentos` (los emitidos, no los esperados).
- `reintentos` y errores intermedios.
- `razonamiento` (chars de thinking, si el modelo lo emite).

Preguntas que el eje debe poder responder:
- ¿El acierto salió por el camino previsto o por otro?
- ¿El corrector comprueba **lo que el modelo hizo** o solo la primera llamada?
- ¿Hay llamadas/argumentos que el outcome da por buenos y no se comprueban?

## 4. Bloque 3 — CONSTRAINTS (¿dentro de qué límites?)

- **Latencia:** por caso + agregado. Separar el arranque en frío (1.ª llamada) del estado caliente; si no, la media miente.
- **Coste:** € reales. Si todo es local, el coste marginal es energía, no dinero.
- **Recursos:** VRAM, potencia/energía (y CPU/RAM si aplica).
- **Presupuesto:** contexto (`num_ctx`), tokens, nº máximo de pasos.
- **Seguridad/privilegios:** qué tocó el instrumento y qué NO tocó.
- **Límites de la medición:** qué NO cubre el número. Obligatorio (RULE-015: validar la métrica antes de fiarse).

## 5. Veredicto

Se escribe sobre la terna. Un outcome alto con trayectoria fuera de lo previsto, o con constraints
`NO MEDIDO`, se declara tal cual: el número no se maquilla.

## 6. Anexo para el ledger (si el cierre lo alimenta)

Los 2 campos nuevos, dentro de la misma línea JSON:

```json
"trayectoria": {"pasos": 0, "herramientas": [], "argumentos": [], "reintentos": 0},
"constraints": {"latencia_s": 0.0, "coste_eur": 0.0, "vram_mib": 0, "potencia_w": 0.0,
                "energia_wh": 0.0, "contexto_tokens": 0, "límites_de_medicion": "..."}
```
