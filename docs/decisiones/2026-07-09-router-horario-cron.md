# Router Horario con Cron y Modificación de config.yaml

## Contexto

**ACTUALIZACION 2026-07-14: Esta decision queda obsoleta por datos de coste reales.**

Se utilizaba DeepSeek como proveedor principal de IA, asumiendo que su facturación se duplicaba en la franja horaria de 03:00 a 12:00 (hora de España) o que Gemini era mas barato. Tras consultar los precios oficiales a julio 2026:

| Modelo | Input ($/1M tok) | Output ($/1M tok) | Coste consulta tipica* |
|--------|:-:|:-:|:-:|
| DeepSeek V4 Flash | $0.077 | $0.154 | $0.00023 |
| Gemini 2.5 Flash | $0.300 | $2.500 | $0.00305 |
| Gemini 2.5 Flash-Lite | $0.100 | $0.400 | $0.00050 |
| Ollama local | $0.000 | $0.000 | $0.00000 |

*Consulta tipica ≈ 2.000 input + 500 output tokens.

**DeepSeek V4 Flash es 13x mas barato que Gemini 2.5 Flash y 2.2x mas barato que Gemini Flash-Lite en output.** No hay motivo para cambiar a Gemini en franja cara por ahorro de costes. DeepSeek V4 Flash se mantiene como modelo cloud por defecto permanentemente.

El unico motivo para usar Ollama local sigue siendo la privacidad de datos, no el coste.

### Historial de la decision original (obsoleta)

Originalmente se asumia que DeepSeek facturaba el doble en franja 03:00-12:00 y que Gemini era mas economico. Los datos reales demuestran que esto no es asi.

## Problema (original, ya resuelto)
La solución inicial usaba un script llamado en `~/.bashrc` para cambiar la variable de entorno `HERMES_MODEL`. Sin embargo, esto fallaba al arrancar Hermes desde atajos de escritorio o entornos gráficos, ya que estos no leen `~/.bashrc` al iniciar. Hermes conservaba el último modelo usado, resultando en facturación no deseada.

## Alternativas
1. Forzar la lectura de variables de entorno en la interfaz gráfica (complejo y dependiente del sistema de escritorio).
2. **Modificar dinámicamente el archivo maestro de configuración `~/.hermes/config.yaml`.**

## Decisión
Se implementa un script en Python (`scripts/router-modelo.py`) programado mediante `cron` a nivel de sistema. 
- A las 03:00, `cron` cambia la configuración a `gemini-2.5-flash`.
- A las 12:00, `cron` la devuelve a `deepseek-v4-flash`.

## Motivos
- Es una solución agnóstica al entorno gráfico o de terminal. 
- Garantiza que cualquier nueva sesión que se abra leerá directamente del archivo modificado.

## Consecuencias y Reglas Operativas
1. El cambio se realiza correctamente de manera silenciosa en el sistema.
2. **Limitación Importante**: Hermes no cambia de modelo "en caliente". Si hay una sesión iniciada antes de la hora de corte y se sigue usando después, se continuará usando el modelo original de la sesión. 
3. **Regla**: Para aplicar el router horario, **es obligatorio cerrar y abrir una nueva sesión** de Hermes si se atraviesa la hora de corte (03:00 o 12:00).

|## Estado
**OBSOLETA (14 de julio de 2026)** — Los precios reales demuestran que DeepSeek V4 Flash es mas barato que Gemini en cualquier franja. El router horario queda desactivado. Ver `scripts/model-router.sh` para la version actual (no-op).

## Historial
- **09-jul-2026**: Implementación inicial con cron inline. Falló en el primer disparo (3:00 del 10-jul) porque el `&&` encadenado impedía escribir el log si el primer comando fallaba, y no se pudo diagnosticar.
- **10-jul-2026**: Reemplazado por script `scripts/router-cron.sh` que:
  - Auto-detecta la franja horaria (un solo cron para ambas transiciones).
  - Siempre escribe en el log, independientemente del resultado.
  - Reporta códigos de retorno de cada operación.
  - Se invoca a las 3:00 y 12:00 desde crontab del usuario.

## Archivos involucrados
| Archivo | Propósito |
|---------|-----------|
| `scripts/router-cron.sh` | Script ejecutado por cron (nuevo, robusto) |
| `scripts/model-router.sh` | Script para source en `.bashrc` (convive, funciona en terminal) |
| `~/.hermes/config.yaml` | Config modificada por el router |
| `logs/router-modelo.log` | Log del router |
| `~/.bashrc` línea 127 | Source de model-router.sh para terminal interactiva |
