# Decisión Técnica: Decision Engine y State Manager (arquitectura v3)

**Fecha**: 2026-07-14
**Estado**: Aceptada (parcialmente activa)
**Área**: Enrutamiento de IA / Observabilidad

## Contexto
Aparecieron dos componentes nuevos sin documentar ni commitear previamente:
`state-manager/state-manager.py` y `decision-engine/decision_engine.py`,
parte de una arquitectura "v3" mencionada en sus propias cabeceras.

## Qué hace cada componente

### state-manager.py — ACTIVO EN PRODUCCIÓN
- Recopila estado del sistema (GPU vía nvidia-smi, RAM, disco) cada 60s.
- Escribe `/mnt/ssd_ia_datos/lab-state/state.json`.
- Solo lectura del sistema; no ejecuta comandos mutadores.
- Gestionado por systemd: `lab-state-manager.service` (confirmado con
  `systemctl --user status` el 2026-07-14).

### decision_engine.py — ESCRITO PERO NO CONECTADO
- Determinista, sin LLM. Lee `state.json` + `policies/*.yaml`, devuelve
  `{provider, model, reason}` según precedencia:
  privacidad → disponibilidad → costes → horario → preferencias.
- No modifica `config.yaml` ni ejecuta nada; solo calcula y registra su
  decisión en `~/.hermes/ultima-decision.json` y su propio log.
- Verificado con `grep -rn "decide()"` que ningún script externo lo llama
  todavía (2026-07-14). No sustituye a `router-cron.sh`, que sigue siendo
  el mecanismo activo real.
- Corregido: `FALLBACK_MODEL` cambiado de `deepseek-chat` (alias legacy,
  DeepSeek lo retira 2026-07-24) a `deepseek-v4-flash`.

## Pendiente antes de activar decision_engine.py
- Revisar que el modelo de fallback en `evaluar_costes()` (`qwen2.5:7b`)
  no se use como `model.default` si algún día sustituye a `router-cron.sh`,
  por el límite de contexto de 32K (Hermes exige mínimo 64K).
- Decidir explícitamente si sustituye a `router-cron.sh` o convive con él.
- Revisar el parser YAML casero (`_parse_yaml_simple`) contra casos reales
  antes de depender de él en producción.

## Motivos
- Evita que estos componentes queden como "código huérfano" sin contexto.
- Deja constancia de que decision_engine.py está inactivo, para no asumir
  que ya gobierna el enrutamiento cuando no es así.

## Referencias
- `docs/decisiones/2026-07-14-github-remoto-externo.md`
