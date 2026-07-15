# Bug DeepSeek Disponibilidad — 73 ciclos forzando Gemini (2026-07-14/15)

## Causa raíz

Dos partes que actuaron en conjunto:

1. **`api_key` nunca transmitida a `check_cloud()` para DeepSeek**. La
   función `check_cloud("deepseek", url)` en `state-manager/state-manager.py`
   se llamaba sin `api_key`, a diferencia de la llamada equivalente de Gemini
   que sí la recibía vía `read_secret("gemini.key")`. La API de DeepSeek
   devolvía error/denegación, y el estado se registraba como "no disponible".
2. **`deepseek.key` nunca existió en `SECRETS_DIR`**
   (`/mnt/ssd_ia_datos/lab-state/secrets/`). Aunque la primera parte se
   corrigiera, no había clave que leer.

## Impacto verificable

- **Inicio**: 2026-07-14T12:55:16 (primer `"forzando Gemini"` en JSON)
- **Fin**: 2026-07-15T22:37:56 (último `"forzando Gemini"` antes del fix)
- **Ciclos afectados**: 73 entradas con `"DeepSeek no disponible, forzando Gemini"`
  en `decision.log`
- **Coste**: forzó Gemini de forma continua durante ~30h, coincidiendo con
  el anuncio de peak-pricing de DeepSeek (posible sobrecoste evitable)

## Fix aplicado

- Añadida línea `deepseek_key = read_secret("deepseek.key")` en
  `_collect_fast()` de `state-manager/state-manager.py`
- Pasada como `api_key=deepseek_key` a `check_cloud("deepseek", ...)`
- Creado `deepseek.key` en `SECRETS_DIR` con la API key real
- Verificación manual contra `https://api.deepseek.com/v1/models` —
  respuesta 200 con 2 modelos listados
- Ejecutado `systemctl --user restart lab-state-manager.service` para
  que el cambio surta efecto en el proceso persistente (`--watch`)

## Lección operativa crítica

`state-manager.py` corre como servicio systemd persistente
(`lab-state-manager.service`, modo `--watch`). Editar el `.py` NO es
suficiente — hay que reiniciar el servicio para que el cambio cargue
en memoria.

## Verificación

1. `systemctl --user status lab-state-manager.service` — activo, PID
   reiniciado a las 22:39:43
2. `decision.log` muestra la primera decisión con `"provider": "deepseek"`
   a las 2026-07-15T22:41:02 (3 minutos tras el reinicio)

## Estado actual

Verificado 1 ciclo post-fix. Pendiente de confirmar estabilidad en 3+
ciclos adicionales antes de cerrar como definitivo.
