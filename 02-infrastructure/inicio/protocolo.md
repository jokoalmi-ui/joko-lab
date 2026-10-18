---
type: infrastructure
subtype: infrastructure
status: active
tags: [infrastructure]
created: 2026-07-28
---
# Protocolo

PROTOCOLO DE APERTURA — inicio
================================
Pertenece a: 02-infrastructure/inicio/
Version: 1.0.0
Fecha: 2026-07-28

═══════════════════════════════════════════════════════════
PROPOSITO
═══════════════════════════════════════════════════════════

Verificar que el laboratorio esta en estado operable antes
de empezar a trabajar. Levanta el stack Docker si no esta
corriendo (ciclo down/up con fin.sh) y detecta anomalias
comparando el estado actual contra el ultimo estado registrado.

═══════════════════════════════════════════════════════════
CONTRATO
═══════════════════════════════════════════════════════════

El protocolo inicio garantiza:

1. Todos los servicios criticos responden
   (docker, ollama, gateway, n8n)

2. Las herramientas de desarrollo estan instaladas
   (uv, cargo, python3, node, git)

3. Las rutas del PATH son correctas
   (~/.local/bin, ~/.cargo/bin)

4. Los directorios criticos existen
   (~/.local/share/uv, ~/.hermes, ~/automation-stack)

5. No hay cambios inesperados desde el ultimo cierre
   (diff contra estado-final.json)

6. Se genera un estado-inicial.json como referencia
   para el cierre

═══════════════════════════════════════════════════════════
SECUENCIA
═══════════════════════════════════════════════════════════

  1. STACK  — levantar stack Docker si no esta corriendo (up -d)
  2. CHECK  — servicios docker
  3. CHECK  — ollama
  4. CHECK  — gateway
  5. CHECK  — n8n
  6. CHECK  — herramientas (uv, cargo, python3, node, git)
  7. CHECK  — PATH (~/.local/bin, ~/.cargo/bin)
  8. CHECK  — directorios criticos
  9. SNAPSHOT — generar estado-inicial.json
  10. DIFF  — comparar contra ultimo estado-final.json
  11. REPORT — mostrar anomalias
  12. READY — senal de laboratorio listo

Cada check es un script independiente en checks/.
El script principal (inicio.sh) los invoca en orden.

═══════════════════════════════════════════════════════════
FORMATO DE SALIDA
═══════════════════════════════════════════════════════════

inicio.sh debe producir una salida como esta:

  === INICIO: Joko Lab ===
  Fecha: 2026-07-28 19:30:00 CEST

  docker  ............ OK (4/4 containers)
  ollama ............. OK (respuesta en 0.3s)
  gateway ............ OK (puerto 8080)
  n8n ................ OK (puerto 5678)
  uv ................. OK (toolchain ~/.local/share/uv)
  cargo .............. OK (~/.cargo/bin en PATH)
  python3 ............ OK (3.14.4)
  node ............... OK (v22.x)
  git ................ OK (rama master, limpio)
  PATH ............... OK (3 rutas criticas)
  directorios ........ OK (5/5 existen)

  --- DIFF contra ultimo cierre ---
  Sin diferencias detectadas.

  === LABORATORIO LISTO ===

Si hay anomalias:

  --- ANOMALIAS DETECTADAS ---
  [ALTA] ~/.local/share/uv — NO EXISTE
  [MEDIA] .bashrc — 37 bytes (esperados ~4000)
  [BAJA] Node.js version: v20.x (esperado v22.x)

═══════════════════════════════════════════════════════════
DEPENDENCIAS
═══════════════════════════════════════════════════════════

- Los checks deben ser independientes entre si
- Cada check retorna 0 = OK, 1 = WARNING, 2 = ERROR
- El script principal NO se detiene en WARNING
- El script principal se detiene en ERROR si es critico
- estado-inicial.json se sobreescribe en cada ejecucion

═══════════════════════════════════════════════════════════
FIN DEL PROTOCOLO
═══════════════════════════════════════════════════════════

## Conexiones

- [[fin]] — fin: protocolo gemelo de cierre
- [[checklist-recuperacion]] — checklist-recuperacion: usado si el inicio detecta anomalías
