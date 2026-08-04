# DEC-2026-08-04 — Modelo cloud permanente: deepseek-v4-flash

**Fecha:** 2026-08-04
**Estado:** activa
**Ámbito:** Enrutamiento cloud (Decision Engine / Hermes)

## Decisión

El modelo cloud de Hermes es SIEMPRE deepseek-v4-flash. Se elimina la
franja horaria de Gemini (03:00-12:00) y la selección de modelo principal
por VRAM (gpu.yaml). El cambio a deepseek-v4-pro es manual, por decisión
del usuario según la tarea del momento (`/model deepseek-v4-pro`).

## Motivo

1. Coste mínimo: deepseek-v4-flash cubre el uso cloud habitual; la franja
   fija de Gemini era coste sin consumo (0 sesiones gemini desde 13-jul-2026).
2. Desincronización real detectada 04-ago: el DE decidía gemini por la
   mañana pero las sesiones usaban deepseek (Hermes fija el modelo al
   iniciar sesión, no cambia en caliente).
3. La VRAM local ya no debe secuestrar el modelo principal: cuando la GPU
   está ocupada (RAG, LM Studio), Hermes sigue en cloud.

## Qué cambió

- `policies/horario.yaml` v2: regla única 00:00-23:59 → deepseek; fallback deepseek.
- `policies/gpu.yaml` v2: reglas vacías (la VRAM ya no decide el modelo principal).
- El uso local (delegación, LM Studio, Ollama) se mantiene intacto por sus
  vías propias — objetivo: máximo aprovechamiento del lab, mínimo coste.
- Salvaguardas intactas: privacidad (datos sensibles → local) y
  disponibilidad (fallback si cloud cae).

## Consecuencias

- config.yaml de Hermes: deepseek-v4-flash estable (salvo `/model` manual).
- apply-decision.sh (cada 30 min) ya no produce cambios de proveedor:
  validará deepseek y no tocará el config.
- El usuario decide cuándo subir a PRO según la tarea.

## Validación (04-ago, salida real)

- apply-decision.sh → "✓ Set model.provider = deepseek / default = deepseek-v4-flash / base_url = https://api.deepseek.com/v1"
- grep config.yaml → provider deepseek, default deepseek-v4-flash, base_url correcto
- consulta-decision.sh → "provider=deepseek | model=deepseek-v4-flash — Política: horario.yaml — Horario: 00:00-23:59, ahora 09:12"

## Qué me haría cambiar de opinión

- Que una tarea requiera Gemini de forma recurrente (evidencia de uso > 0).
- Que deepseek-v4-flash se quede corto en calidad/precio frente a otra opción.

## Confianza

Alta (validación real post-cambio).
