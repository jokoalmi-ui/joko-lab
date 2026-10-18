---
type: infrastructure
subtype: infrastructure
status: active
tags: [infrastructure]
created: 2026-07-28
---
# Protocolo

PROTOCOLO DE CIERRE — fin
============================
Pertenece a: 02-infrastructure/fin/
Version: 1.0.0
Fecha: 2026-07-28

═══════════════════════════════════════════════════════════
PROPOSITO
═══════════════════════════════════════════════════════════

Registrar el estado final del laboratorio al terminar una
sesion de trabajo. Detectar cambios ocurridos durante la
sesion, generar backup si es necesario, y dejar un registro
que permita detectar anomalias en el proximo arranque.

═══════════════════════════════════════════════════════════
CONTRATO
═══════════════════════════════════════════════════════════

El protocolo fin garantiza:

1. Se captura el estado completo del laboratorio
   (servicios, herramientas, git, PATH, directorios)

2. Se compara con el estado-inicial.json de la sesion
   (que cambio durante el trabajo)

3. Si hay cambios en el repositorio, se hace commit + bundle
   (backup incremental)

4. Se escribe un informe de cierre en 04-operations/reports/

5. Se guarda estado-final.json para el proximo inicio

═══════════════════════════════════════════════════════════
SECUENCIA
═══════════════════════════════════════════════════════════

  1. SNAPSHOT — estado actual de servicios
  2. SNAPSHOT — estado de git (rama, cambios, ultimo commit)
  3. SNAPSHOT — estado de herramientas y PATH
  4. DIFF — comparar contra estado-inicial.json
  5. LOG — escribir cambios de la sesion
  6. BACKUP — si hay cambios, git commit + bundle
  7. REGISTRO — escribir informe en 04-operations/reports/
  8. CIERRE — guardar estado-final.json
  9. CLOSE — senal de cierre

═══════════════════════════════════════════════════════════
FORMATO DE SALIDA
═══════════════════════════════════════════════════════════

fin.sh debe producir una salida como esta:

  === FIN: Joko Lab ===
  Fecha: 2026-07-28 22:15:00 CEST
  Duracion sesion: 2h 45m

  --- CAMBIOS DETECTADOS ---
  Git: 2 commits nuevos (master)
  Herramientas: sin cambios
  PATH: sin cambios
  Servicios: sin cambios

  --- BACKUP ---
  Commit: OK (2 archivos)
  Bundle: OK (hermes-lab-20260728.bundle)
  Rescue: OK (USB)

  --- REGISTRO ---
  Informe: 04-operations/reports/2026-07-28-cierre-joko-lab.txt
  Estado: 02-infrastructure/fin/estado-final.json

  === SESION CERRADA ===

═══════════════════════════════════════════════════════════
DEPENDENCIAS
═══════════════════════════════════════════════════════════

- Requiere estado-inicial.json generado por inicio
- Si no existe estado-inicial.json, el diff se omite
  (sesion no inicio con el protocolo)
- estado-final.json se sobreescribe en cada ejecucion
- El backup NO se ejecuta si no hay cambios detectados

═══════════════════════════════════════════════════════════
FIN DEL PROTOCOLO
═══════════════════════════════════════════════════════════

## Conexiones

- [[inicio]] — inicio: protocolo gemelo de apertura
- [[checkpoint]] — checkpoint: guarda estado para el cierre
