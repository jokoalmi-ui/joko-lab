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

---

## Parche estructural v2: validación pre-aplicación en apply-decision.sh (2026-07-15 23:34)

### Problema adicional detectado tras el fix inicial

Aunque `state-manager.py` ya leía y transmitía la key correctamente, el
script `apply-decision.sh` aplicaba ciegamente cualquier decisión del
Runtime sin verificar que el proveedor elegido realmente respondiera.
Esto permitía dos modos de fallo:

1. **Key ausente/vacía**: si `deepseek.key` faltaba en SECRETS_DIR,
   el DE podía decidir DeepSeek igual y `apply-decision.sh` lo escribía
   en `config.yaml` — la siguiente sesión de Hermes arrancaba muerta.
2. **Modelo inexistente**: si el DE decidía un modelo que no existe en
   la API (p.ej. `gemini-3.1-flash`), `apply-decision.sh` lo escribía
   igual en `config.yaml`.

### Fix aplicado

Fichero: `decision-engine/apply-decision.sh` (63 → 230 líneas)

Insertada una fase de validación pre-aplicación entre la obtención de la
decisión y la escritura en `config.yaml`:

```
Runtime.resolve() → deepseek/deepseek-v4-flash
                           ↓
              ┌─ VALIDACIÓN PRE-APLICACIÓN ─┐
              │  • deepseek.key existe?      │ ← bloquea si no
              │  • deepseek.key vacío?       │ ← bloquea si sí
              │  • GET /models con auth      │ ← bloquea si 000/401
              │  • modelo en lista?          │ ← bloquea si no está
              │  (gemini: mismo patrón       │
              │   con endpoint por-modelo)   │
              │  (ollama/lmstudio: solo      │
              │   comprobar HTTP != 000)     │
              └──────────────────────────────┘
                     ↓ OK               ↓ FALLA
              hermes config set      log + exit 1
              ✓ config.yaml         → config.yaml intacto
              → siguiente ciclo     (cron reintenta en 30 min)
```

### Detalles técnicos

- **deepseek**: `GET https://api.deepseek.com/models` con
  `Authorization: Bearer $key` (array de args, sin eval).
  Valida HTTP 000 (caído), 401 (key inválida) y parsea JSON
  confirmando que `model.id` está en la lista.
- **gemini**: `GET /v1beta/models/$MODEL?key=$KEY`. Endpoint
  por-modelo: 200 = existe, 404 = no existe, 401/403 = key inválida.
- **ollama/lmstudio**: `GET /api/tags` o `/v0/models`, timeout 5s.
  Solo comprueba HTTP 000 (proceso caído). No valida modelo
  específico por diferencias de naming con el DE.
- **Proveedores cloud (deepseek, gemini)**: se considera bloqueante
  que el archivo `.key` no exista o esté vacío. No hay tier gratuito
  sin auth en ninguno de los dos.
- **Arrays curl**: se usa `curl_args=(-s --max-time "$timeout")` y
  `curl_args+=(-H "Authorization: Bearer $key")`, expandido como
  `curl "${curl_args[@]}" ...` — idéntico al patrón de
  `check_cloud()` en `state-manager.py`. Sin `eval`.

### Pruebas realizadas

1. **Camino de fallo**: renombrado `deepseek.key` → `apply-decision.sh`
   bloquea con `❌ VALIDACIÓN FALLÓ: deepseek requiere key pero no existe`.
   `config.yaml` no se modifica. `exit 1`.
2. **Camino de éxito**: restaurado `deepseek.key` → `apply-decision.sh`
   ejecuta `GET /models`, confirma modelo en lista, aplica cambio.
   `config.yaml` actualizado. `exit 0`.
3. **Verificación ad-hoc**: 11/11 tests internos (sintaxis, funciones,
   orden de operaciones, parseo de modelos mock).
4. **Histórico**: el patrón `Cambiando: / →` (OLD_PROVIDER vacío) es
   preexistente desde el 13 de julio — no fue introducido por este parche.

### Lección operativa

Ahora hay DOS puntos donde un proveedor cloud puede ser bloqueado:
`state-manager.py` (disponibilidad en `state.json`) y
`apply-decision.sh` (validación pre-aplicación). Si uno falla,
el otro actúa como respaldo. El cron reintenta cada 30 min.
