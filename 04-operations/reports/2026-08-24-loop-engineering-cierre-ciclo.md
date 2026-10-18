---
title: "Informe — Loop Engineering: cierre del ciclo de observación del piloto"
type: operations
---

# Informe — Loop Engineering: cierre del ciclo de observación del piloto

**Fecha:** 2026-08-24
**Estado:** CICLO CERRADO — veredicto de la pregunta de salida emitido
**Decisiones de referencia:** loop-engineering-diseno.md (04-ago: F1-F2+Baseline aprobado, F3-F6 bloqueados, sin umbrales a priori, piloto 1 semana)
**Predecesor:** 04-operations/reports/2026-08-04-loop-engineering-f1-f2.md

## Fuente

- Ledger: `/mnt/ssd_ia_datos/lab-state/decision-ledger.jsonl`
- Ventana real del piloto: 2026-07-29 → 2026-08-24 (27 días; el corte de 1 semana se amplió a 21 días reales de datos post-corte)

## Resultados reales

- **977 entradas, 0 corruptas** (rango 2026-07-29T13:15 → 2026-08-24T12:30)
- Por regla (histórico): Disponibilidad 495 (50.7%), Horario 426 (43.6%), Gpu 44 (4.5%), Privacidad 12 (1.2%)
- Por provider: deepseek 866 (88.6%), lmstudio 44 (4.5%), gemini 37 (3.8%), ollama 30 (3.1%)
- Por día: estable ~30-35/día desde el 05-ago; picos: 04-ago 163 (anomalía), 05-ago 50, 19-ago 48; 23-24-ago 11/10 (fin de semana/bajo uso)

## Baseline (desde 04-ago, 21 días)

- Media diaria: 37.8 | std: 29.4
- Única anomalía > media+2σ (96.5): **04-ago con 163** — explicada al 100% por el bucle de reintentos del RuntimeAPI 09:12-09:21 (caso E-001: 107 entradas "Horario: 00:00-23:59, ahora 09:1x") + 15:00 (11) + Privacidad (11). Puntual, NO patrón; no se repitió en 20 días posteriores.

## Hallazgo estructural: Disponibilidad domina desde el 08-ago

- Disponibilidad pasó de 1 entrada (01-ago) a 495; 476 son "Gemini no disponible, forzando DeepSeek".
- Inicio: 08-ago 19:00, desde entonces ~30-35/día (cada ciclo de 30 min).
- Interpretación: el DE intenta Gemini en cada ciclo, falla, y cae a deepseek. Resultado neto correcto (deepseek siempre, coherente con DEC-2026-08-04), pero la distribución por regla cambió a mitad del piloto.
- Impacto en Baseline: segmentar en 2 períodos — 04→07-08 (Horario 72.5%) y 08→24-08 (Disponibilidad 62%).

## Pregunta de salida del piloto: ¿el ledger refleja fielmente el comportamiento del sistema?

**Veredicto: PARCIAL — fiel para frecuencia, insuficiente para resultado.**

SÍ refleja fielmente (evidencia):
- Volumen estable y regular (media 37.8/día, std 29.4) con 21 días de datos → Baseline construible.
- 0 líneas corruptas de 977.
- Pico 04-ago íntegramente explicado por E-001, sin repetición.
- La política horario (DEC-2026-08-04: deepseek siempre) se refleja en providers (deepseek 88.6%; gemini residual solo 01-ago + fallos).
- El fallo continuo a Gemini desde 08-08 se registra con precisión (476 entradas, cada 30 min).

NO refleja (limitaciones estructurales, SIN cambio desde 04-ago):
- **Éxito/fallo de la decisión: sigue sin campo de resultado.** La mejora documentada el 04-ago no se implementó. Sin él no se puede medir "reglas que concentran fallos" (requisito de F3).
- Contexto de tarea/cliente/agente: sigue sin registrarse.
- La regla se infiere del prefijo del reason (formato del DE), no de un campo explícito.

## Decisión (según diseño 04-ago)

1. **Ciclo del piloto CERRADO.** El entregable de la Entrega 1 (responder con evidencia qué reglas gobiernan el lab, cuáles concentran fallos, qué es normal vs anómalo) queda respondido parcialmente: distribución real y normalidad SÍ; fallos por regla NO (sin campo de resultado).
2. **F3 (Proposer) SIGUE BLOQUEADO.** Requisito previo: enriquecer el ledger con resultado (éxito/fallo) y contexto. Toca state-manager / apply-decision.sh — requiere confirmación de Joseba y es código del lab.
3. **Baseline formal pendiente de generar como artefacto** (media semanal por regla, desviación, normal/anómalo), segmentado por el cambio del 08-08.
4. **Observación no bloqueante:** el intento continuo a Gemini (08-08 en adelante) es candidato a propuesta L2 cuando exista F3 — posible fuga de latencia/ruido por timeout esperando a Gemini antes de caer a deepseek. No se propone cambio ahora (prohibición del piloto).

## Pendientes derivados

- [ ] Enriquecer ledger con éxito/fallo (+ cliente/tarea) — requisito de F3 (confirmación requerida)
- [ ] Generar artefacto Baseline formal segmentado (04→07-08 / 08→24-08)
- [ ] Vigilar el intento continuo a Gemini (¿política horario debería filtrarlo antes que disponibilidad?)
- [ ] Decidir siguiente ciclo de observación (¿30 días para el baseline largo según diseño?)
