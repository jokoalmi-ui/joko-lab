# Informes ejecutivos de Joko Lab

Un archivo por semana con el estado del laboratorio.

Convención:
- Fichero: `YYYY-MM-DD.txt` (fecha del informe, no del commit)
- Frecuencia: semanal, o ante un cambio significativo
- No se sobrescriben — cada semana es un archivo nuevo

Para generar un nuevo informe:
  El cron diario (`informe-diario-joko-lab`) lo crea automáticamente
  si han pasado 7+ días desde el último, o si detecta un cambio
  significativo (bug corregido, fix aplicado, cambio de provider).
