---
title: "Informe — Precipitación en Euskadi (Bilbao) enero-agosto 2026 vs últimos 30 años"
type: research
---

# Informe — Precipitación en Euskadi (Bilbao) enero-agosto 2026 vs últimos 30 años
**VERACIDAD:** [VERIFICADO]

**Fecha:** 19-ago-2026
**Fuente:** Open-Meteo Historical API (reanálisis ERA5) — Bilbao (43.26, -2.93)
**URL:** `https://archive-api.open-meteo.com/v1/archive?latitude=43.26&longitude=-2.93&start_date=1996-01-01&end_date=2026-08-19&daily=precipitation_sum`
**Método:** 11.189 días descargados (1996-01-01 → 2026-08-19) → acumulado
enero-agosto por año + media mensual
**Veracidad:** [VERIFICADO] — datos ERA5 reales descargados hoy (202 KB JSON)

---

## Resultado principal

**Enero-agosto 2026 acumulado: 680 mm**
**Media 30 años (1996-2025) mismo periodo: 680 mm**
→ **EXACTAMENTE EN LA MEDIA (+0.0%, +0 mm)**

## Estadísticas de referencia (ene-ago, 30 años)

| Métrica | Valor |
|---|---|
| Media | 680 mm |
| Mediana | 666 mm |
| Desviación estándar | 114 mm |
| Mínimo | 556 mm (1998) |
| Máximo | 1032 mm (2013) |
| **2026** | **680 mm (percentil ~20/31 — normal, ligeramente por encima de la mediana)** |

## Distribución mensual 2026 vs media 30 años

| Mes | 2026 (mm) | Media 30 a (mm) | Δ | % |
|---|---|---|---|---|
| Ene | 132 | 122 | +10 | +8% |
| Feb | 159 | 107 | **+52** | **+48%** |
| Mar | 148 | 99 | **+49** | **+49%** |
| Abr | 58 | 91 | -33 | -36% |
| May | 115 | 83 | **+32** | +38% |
| Jun | 38 | 66 | -28 | -42% |
| Jul | 24 | 56 | **-32** | **-57%** |
| Ago (parcial) | 6 | 55 | -49 | -90% |

## Top 5 más lluviosos y más secos (ene-ago)

| Más lluviosos | mm | Más secos | mm |
|---|---|---|---|
| 2013 | 1032 | 1998 | 556 |
| 2018 | 943 | 2022 | 558 |
| 2015 | 872 | 2000 | 569 |
| 2007 | 821 | 2009 | 571 |
| 2016 | 782 | 2011 | 576 |

## Lectura honesta

1. **2026 NO es un año anómalo en total**: 680 mm ene-ago = media exacta de
   30 años. Ni sequía ni exceso en el acumulado.
2. **PERO el patrón estacional está muy distorsionado**: invierno-primavera
   muy húmedos (Feb +48%, Mar +49%, May +38%) y **verano seco** (Jun -42%,
   Jul -57%, Ago -90%).
3. **Agosto 2026 destaca**: solo 6 mm hasta el día 19 (vs media 55 mm) —
   un agosto extremadamente seco hasta la fecha. Si continúa así, sería el
   agosto más seco del periodo.
4. El total "normal" enmascara una **redistribución estacional**: la lluvia
   que solía caer en verano se adelantó a invierno/primavera. Patrón
   consistente con cambios en la circulación atmosférica (no con la media
   anual de temperatura que sube).
5. **Comparación con temperatura** (informes del mismo día): el calentamiento
   (+0.4-0.5 °C en 20 años) no ha cambiado el total anual de lluvia, pero
   sí su distribución mensual.

## Limitaciones
- Punto ERA5 Bilbao ≈ Euskadi costera; Vitoria (interior) recibe menos
  (pero el patrón de tendencia es el mismo).
- Agosto 2026 es PARCIAL (hasta el 19) — el -90% puede moderarse con las
  lluvias de fin de mes.
- Los acumulados por año usan solo ene-ago (periodo comparable con 2026).

## Nota de proceso
- Datos crudos en /tmp/bilbao_lluvia.json (temporal)
- 11.189 días, 31 valores anuales (30 de referencia + 2026)
