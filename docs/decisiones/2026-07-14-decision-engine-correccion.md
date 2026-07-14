# Corrección: decision_engine.py SÍ está activo

**Fecha**: 2026-07-14
**Estado**: Aceptada
**Corrige a**: 2026-07-14-decision-engine-state-manager.md

## Qué estaba mal
La decisión anterior afirmaba que decision_engine.py estaba "escrito pero
no conectado" y que "no modifica config.yaml". Ambas afirmaciones eran
incorrectas, basadas en una búsqueda con grep demasiado literal (buscaba
el texto "decide()" y no encontró apply-decision.sh, que lo invoca vía
`python3 decision_engine.py --json` sin usar esa cadena exacta).

## Estado real, verificado con `crontab -l` y lectura de apply-decision.sh
- router-cron.sh fue retirado del crontab (sustituido en el commit a07ee66).
- decision_engine.py se ejecuta cada 30 min + 03:00 + 12:00 vía
  apply-decision.sh, que SÍ ejecuta `hermes config set model.provider`
  y `hermes config set model.default` -- modifica config.yaml en producción.
- Corregidos los tres fallbacks a "qwen2.5:7b" (evaluar_privacidad y
  evaluar_costes) por "llama31-8b-64k", ya descargado y verificado con
  Hermes previamente. Se descartó "gemma3:12b" por no estar descargado
  en Ollama (confirmado con `docker exec ollama ollama list`).

## Lección
Antes de documentar que algo "no está conectado", verificar con crontab -l
y grep de nombre de archivo (no de función), no solo grep de texto literal.
Antes de fijar un modelo en un fallback automático, confirmar con
`ollama list` que está realmente descargado, no asumirlo de sesiones previas.
