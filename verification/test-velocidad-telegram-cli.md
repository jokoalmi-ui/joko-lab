---
title: "PROTOCOLO — Test de velocidad Telegram vs CLI"
type: verification
---

# PROTOCOLO — Test de velocidad Telegram vs CLI

**Fecha del test:** 2026-08-05 10:00 (hora España)
**Objetivo:** verificar si Telegram responde más rápido que el CLI (percepción del 03-ago).
**Tipo:** medición de latencia de canal percibida (no benchmark de inferencia pura).

---

## Condiciones de validez (obligatorias)

1. **Mismo modelo en ambos canales.** Verificar justo antes:
   ```bash
   grep -A3 "^model:" ~/.hermes/config.yaml
   bash ~/joko-lab/tools/consulta-decision.sh "codigo"
   ```
   Esperado tras DEC-2026-08-04: provider=deepseek, model=deepseek-v4-flash,
   política horario 00:00-23:59. Si el config dice otra cosa (p.ej. cambio
   manual a PRO), anotarlo y NO comparar contra una medición con otro modelo.

2. **Contexto comparable.** El CLI debe usar UNA SESIÓN NUEVA (no la sesión
   de trabajo larga). El gateway de Telegram inicia conversación nueva por
   defecto: equivalente.

3. **Sin carga extra en la GPU/red** durante el test (sin indexador RAG, sin
   descargas).

## Pregunta idéntica (3 repeticiones por canal)

```
Responde en una sola línea: ¿qué modelo estás usando ahora mismo y qué hora es en España?
```

Corta, sin herramientas, sin RAG: mide el canal, no la recuperación.

## Procedimiento

### A. Telegram (desde el móvil)
1. Abrir el bot y enviar la pregunta.
2. Cronometrar desde el envío hasta que la respuesta llega COMPLETA.
3. Repetir 3 veces con 15s de separación. Anotar t1, t2, t3.

### B. CLI (en el PC, sesión nueva)
1. Abrir una terminal y ejecutar (sesión nueva, contexto mínimo):
   ```bash
   time hermes chat -q "Responde en una sola línea: ¿qué modelo estás usando ahora mismo y qué hora es en España?"
   ```
2. El `time` da el tiempo real total (incluye arranque del proceso ~1-2s).
3. Repetir 3 veces con 15s de separación. Anotar t1, t2, t3.

## Registro de resultados

Guardar el informe en:
`04-operations/reports/2026-08-05-test-velocidad-telegram-cli.md`

Formato mínimo:

| Canal | t1 (s) | t2 (s) | t3 (s) | media |
|---|---|---|---|---|
| Telegram | | | | |
| CLI | | | | |

Campos extra obligatorios: modelo verificado (config + DE), fecha/hora,
cualquier incidencia (gateway reiniciado, cola de API, red).

## Interpretación honesta (reglas del lab)

- La diferencia NO es el canal por sí mismo: es (a) tamaño de contexto de la
  sesión, (b) modelo/proveedor activo, (c) latencia de red. Si el CLI se mide
  con sesión nueva y mismo modelo, la diferencia esperada es pequeña.
- El "typing..." de Telegram y la entrega inmediata al servidor alteran la
  percepción. El dato objetivo es el cronómetro.
- Si la diferencia > 2s a favor de Telegram con condiciones válidas, investigar
  el gateway (polling vs webhook) antes de concluir.
