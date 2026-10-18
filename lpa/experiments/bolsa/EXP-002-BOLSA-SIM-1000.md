---
title: "Experimento LPA — Bolsa: Simulación real 1.000 € (protocolo DECODE)"
type: lpa
---

# Experimento LPA — Bolsa: Simulación real 1.000 € (protocolo DECODE)

## Metadata

| Campo | Valor |
|-------|-------|
| ID | EXP-002-BOLSA-SIM-1000 |
| Dominio | Bolsa (Experimento 002) |
| Categoría | C (Alta densidad: trading/monitorización) |
| Fecha inicio | 2026-08-05 |
| Fecha fin | (simulación abierta — sin capital real) |
| Estado | En curso (simulación, 0 € reales) |
| Fuente del protocolo | Curso DECODE|CORE (Daniel Sánchez-Crespo), vídeos 0intro+part1-6 |

---

## Propósito

**Simular con datos REALES de cotización (05-ago-2026) la primera operación de 1.000 € según el protocolo del curso DECODE**, para:
1. Verificar que el protocolo es ejecutable con datos reales (no solo teoría).
2. Calcular cuántas acciones enteras entran con 1.000 € en cada candidata "aburrida".
3. Medir el resultado NETO (comisiones + fiscalidad + tipo de cambio), no el bruto — patrón del lab.
4. Decidir si el protocolo merece convertirse en ficha operativa del Experimento 002.

**No es dinero real.** Es una simulación con cotizaciones reales y el protocolo del curso. Cero riesgo.

---

## Datos reales de entrada (05-ago-2026)

- Capital simulado: 1.000,00 EUR
- Tipo de cambio EUR/USD: 1,155 (Yahoo Finance, 05-ago-2026) → 1.000 EUR = 1.155,00 USD
- Cotizaciones (Yahoo Finance, 05-ago-2026, USD/acción):

| Acción | Precio USD | Acciones enteras con 1.155 USD | Invertido USD | Sobra USD |
|---|---|---|---|---|
| V (Visa) | 369,59 | 3 | 1.108,77 | 46,23 |
| GOOGL (Alphabet) | 377,65 | 3 | 1.132,95 | 22,05 |
| NVDA (NVIDIA) | 211,94 | 5 | 1.059,70 | 95,30 |
| MSFT (Microsoft) | 492,81 | 2 | 985,62 | 169,38 |
| AAPL (Apple) | 309,38 | 3 | 928,14 | 226,86 |
| CCL (Carnival) | 29,59 | 39 | 1.154,01 | 0,99 |
| WDC (Western Digital) | 548,56 | 2 | 1.097,12 | 57,88 |

---

## Criterio de selección (del curso, part4)

Acción "aburrida": grande, creciente, retrocesos pequeños. Candidatas del propio curso: V, GOOGL, NVDA, CCL, WDC (+ MSFT/AAPL clásicas).

**Selección simulada: NVDA (5 acciones)** — la clásica del curso, con 5 acciones enteras (el resto deja 2-3, lo que deja más sobrante sin invertir).

---

## Simulación de la operación (NVDA, 5 acciones a 211,94 USD)

| Concepto | Valor |
|---|---|
| Capital inicial | 1.000,00 EUR (1.155,00 USD) |
| Acciones | 5 × NVDA @ 211,94 USD = 1.059,70 USD |
| Sobrante no invertido | 95,30 USD (8,2%) |
| **Escenario +15% (salida positiva del curso)** | 5 × 243,73 USD = 1.218,65 USD = **1.055,11 EUR** (+55,11 EUR = +5,5% en EUR) |
| **Escenario -10% (salida negativa del curso)** | 5 × 190,75 USD = 953,73 USD = **825,74 EUR** (-174,26 EUR = -17,4% en EUR) |

### HALLAZGO REAL (medido, no opinado)

El +15% en USD se convierte en +5,5% en EUR: **el tipo de cambio se come ~2/3 de la ganancia bruta** (porque entras con EUR → compras en USD → vendes en USD → vuelves a EUR). Esto confirma con datos reales la advertencia del curso (part2): el tipo de cambio es "la tangada del siglo" y por eso Dani recomienda cuentas multi-divisa (EUR/GBP/USD) para no pasar por el spread.

### Neto tras comisiones + fiscalidad (modelo del curso, part5)

Con el ejemplo del curso (comisiones ~50 EUR en total) sobre el escenario +15% en USD:
- Bruto en EUR: +55,11 EUR
- Comisiones (compra+venta, estimación curso): ~-50,00 EUR
- Impuestos sobre plusvalía (~19-21% sobre beneficio): la plusvalía quedaría ~+5 EUR → impuesto ~1 EUR
- **Neto estimado: ~+4-5 EUR** (0,4-0,5% del capital) — si el FX no cambia

Conclusión del modelo: con 1.000 EUR y el tipo de cambio actual, una subida del 15% en USD deja ~+5 EUR netos. **El curso asume 10-15% en EUR y ~100 EUR netos; con el FX actual eso solo se consigue con una subida mayor en USD o con cuenta en dólares.** Dato real para el Experimento 002, no promesa del curso.

---

## Guardarraíles mentales (del curso, part4)

| Condición | Umbral | Disparo (mental, no automático) |
|---|---|---|
| Salida positiva | +15% sobre precio de compra (243,73 USD) | Evaluar venta (contexto: ¿sigue subiendo?) |
| Salida negativa | -10% (190,75 USD) | Vender sí o sí (pérdida limitada ~174 EUR máx) |

---

## IE / IMD (métricas LPA)

- Decisiones totales de esta ficha: 5 (simular, seleccionar NVDA, 5 acciones, guardarraíles, registrar neto)
- Decisiones nuevas (sin trazabilidad al core LPA): 0 — todas vienen del protocolo DECODE (material Experimento 002)
- IE = 0% (no emerge concepto nuevo: el protocolo es input del experimento, no del core)
- IMD = 5/5 trazables (100%)

---

## Hallazgos para el lab

1. **El FX domina el resultado en EUR**: un +15% en USD ≈ +5,5% en EUR con FX 1,155. Medir SIEMPRE el retorno en la divisa de entrada.
2. **El sobrante importa**: con 1.000 EUR y NVDA a 211,94 USD, el 8,2% queda sin invertir (acciones indivisibles). Con 1.500-2.000 EUR el sobrante baja en %.
3. **El protocolo del curso es ejecutable** con datos reales: selección → cantidad → orden → guardarraíles → neto. Todo verificable.
4. **Confirmación del patrón lab**: guardarraíles mentales = contrato de decisión previo; neto vs bruto = telemetría real.

---

## Afirmaciones afectadas

| Afirmación | Antes | Después | Justificación |
|---|---|---|---|
| "El protocolo DECODE produce ~100 EUR netos con 1.000 EUR" | (externo, curso) | Cuestionada por simulación | Con FX 1,155 y NVDA, +15% USD ≈ +5 EUR netos. Requiere verificación con operación real o FX distinto |

---

## Siguientes pasos

- [ ] Decidir candidata real si Joseba abre cuenta (1.000 EUR, libre de cargas 12 meses)
- [ ] Recalcular con la cotización del día de la compra real
- [ ] Si se opera real: registrar Excel + PDFs (protocolo part4/5)

---

## Juego autónomo v2 (06-ago-2026)

Autorizado por Joseba ("montar el juego tal cual: diario 22:30, 1.000 €,
aviso Telegram"). El lab juega a la bolsa en SIMULACIÓN con el método de Dani:
razonamiento autónomo OBS→HYP→DEC diario, registro y autocorrección.

### Componentes

- `tools/bolsa_scan.py` — escáner de cotizaciones (API Nasdaq, sin key).
  Primer snapshot real (06-ago-2026): 15 tickers, 4 candidatas L (WDC, MRVL,
  FSLY, MCHP). Fix aplicado: la serie de Nasdaq viene invertida.
- `experiments/bolsa/estado-juego.json` — capital 1.000 € virtuales, reglas,
  posiciones, aprendizajes.
- `experiments/bolsa/ledger-operaciones.jsonl` — historial de operaciones.
- `experiments/bolsa/snapshots/YYYY-MM-DD.json` — snapshots diarios.
- Skill `bolsa-autonoma` — procedimiento de la pasada diaria.
- Cron `bolsa-juego-diario` (b762b14787b5) — lun-vie 22:30, aviso Telegram.

### Reglas operativas (método de Dani)

- Entrar solo en patrón L-swing, a mitad de subida (nunca buy the dip).
- Salida +15% evaluando contexto (noticias); stop -10% sí o sí.
- Evitar NKE, VSCO, MSFT (contraejemplos de Dani).
- Máx 1 operación nueva por pasada; medir en USD (el FX se come el retorno).
- Autocorrección: cada operación cerrada → comparar resultado real vs
  esperado → anotar acierto/error en aprendizajes → ajustar.

### Nota de honestidad

Es una SIMULACIÓN con cotizaciones reales. 0 € reales. El cron decide con los
datos del snapshot; si la fuente falla, no decide.

### Fix 18-sep-2026 — cierre oficial del día (lag del API resuelto)

Problema confirmado 8 veces (04, 08, 09, 14, 15, 16, 17 y 18-sep): a las 22:30
CEST la serie `/historical` de Nasdaq todavía no publica la barra del día, así
que el snapshot registraba el cierre del día ANTERIOR.

Solución aplicada (backup previo: `tools/bolsa_scan.py.bak-20260918`): nueva
función `fetch_live_quote()` que consulta
`https://api.nasdaq.com/api/quote/{ticker}/info?assetclass=stocks` y usa
ÚNICAMENTE el campo `secondaryData` ("Closed at ... 4:00 PM ET") = cierre
oficial del día. No se usa `primaryData` (último precio intradía) para no
violar la regla "scan intradía ≠ cierre".

Efecto: el scan imprime la línea `CIERRE OFICIAL DEL DIA (quote/info, mismo
dia)`, guarda `live_close` / `live_date` por ticker en el snapshot y —segunda
mitad del mismo fix— **recalcula DD%/REC%/patrón con ese cierre**
(`_recalcular_con_cierre`), imprimiendo `METRICAS CON EL CIERRE DEL DIA
(sustituyen a la serie, que va con lag)` y marcando con `*` las candidatas L
medidas con el cierre oficial. La tabla de la serie se conserva, etiquetada
como "con lag", para poder comparar. Verificado en la pasada del 18-sep
(snapshot 22:33:37 y 2ª ejecución 22:37:37): los 14 tickers con dato devuelven
`09/18/2026` y cuadran con la variación diaria (MRVL 244,25 = +1,45% sobre
240,76 → DD -21,36% / REC 18,29% / L-swing*; FSLY 23,86 = -2,89% sobre 24,57 →
DD -20,52% / REC 16,79% / L-swing*). Con esto ya NO hace falta desplazar el
cron a las 23:30 CEST (mejora que estaba pendiente desde el 09-sep) ni
recalcular a mano las métricas del cierre del día.

### Pasadas registradas (últimas)

- 18-sep-2026 (viernes): `no_operar` (27ª del juego). Candidatas L: MRVL
  (REC 18,29%) y FSLY (REC 16,79%) — ninguna pasa el filtro de upside ≥50%,
  ambas pegadas al valle. Guardarraíl geopolítico vigente (Ormuz) + Fed 3,75-4,00%.
  Capital virtual intacto: 1.000 EUR, sin posiciones.
- 21-sep-2026 (lunes): `no_operar` (28ª del juego). Candidatas L con el cierre
  oficial del día: **MRVL** (257,38 = +5,37% sobre el viernes; DD -16,40%, REC
  24,65%, margen al máximo de 3 meses 19,61% — a 0,39 puntos del 20%) y **WDC**
  (448,17; DD -38,83%, REC 8,79% = pegada al valle, sería buy the dip). FSLY
  deja de ser candidata: +14,9% (23,86 → 27,42) por el lanzamiento de su "AI
  firewall" y el scan lo reclasifica a ascendente. Novena confirmación del lag
  del API (la serie a las 22:30 del lunes seguía con el cierre del **viernes
  18-sep**): decisión con `live_close` de los 14 tickers (09/21/2026).
  Guardarraíl geopolítico vigente (dos petroleros alcanzados en Ormuz hoy,
  ataques houthis del 19-sep a Riad/Yanbu), con la primera ventana diplomática
  clara (Pezeshkian + Trump en la Asamblea General de la ONU, 22-29 sep; Brent
  -2,1% a 101,70, mínimo desde el 10-sep). Informe semanal de Dani del lunes NO
  comprobable (CDP 9222/9224 sin sesión de Skool): referencia = lección 5 del
  07-sep. Capital virtual intacto: 1.000 EUR, sin posiciones.

---

## Artefactos

- Análisis del curso: /home/jokoalmi/joko-lab/research/analisis-decode-curso-completo.md
- Análisis individuales: /home/jokoalmi/joko-lab/research/analisis-decode-part*.md
- Transcripts: /tmp/decode_*.vtt

FIN DE LA FICHA
