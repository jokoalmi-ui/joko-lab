# Router Horario con Cron y Modificación de config.yaml

## Contexto
Se utiliza DeepSeek como proveedor principal de IA, pero su facturación se duplica en la franja horaria de 03:00 a 12:00 (hora de España). Para ahorrar costes, se dispone de una licencia de Gemini Pro que puede utilizarse como alternativa en esa ventana horaria.

## Problema
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

## Estado
Activo (09 de julio de 2026).
