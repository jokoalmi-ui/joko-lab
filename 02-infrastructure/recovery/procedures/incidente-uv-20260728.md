---
type: infrastructure
subtype: infrastructure
status: active
tags: [infrastructure]
created: 2026-07-28
---
# Incidente uv 20260728

INCIDENTE: Desaparicion de ~/.local/share/uv
================================================
Fecha: 2026-07-28
Gravedad: ALTA
Estado: RESUELTO
Registrado por: jokoalmi

═══════════════════════════════════════════════════════════
QUE OCURRIO
═══════════════════════════════════════════════════════════

Al iniciar la sesion del 2026-07-28, el perfil de Linux
estaba danado. El directorio ~/.local/share/uv habia
desaparecido, lo que dejo a Hermes sin toolchain de Python.

Los sintomas fueron:
- Hermes no arrancaba correctamente
- Los comandos de uv fallaban
- El PATH estaba incompleto
- Los entornos virtuales (.venv) no funcionaban

═══════════════════════════════════════════════════════════
CAUSA PROBABLE
═══════════════════════════════════════════════════════════

No se determino la causa exacta. Posibles:

1. Limpieza automatica del sistema (tmpwatch/systemd-tmpfiles)
   que elimino ~/.local/share/uv por error.

2. Restauracion parcial de un backup que no incluyo
   el directorio de uv.

3. Problema con el perfil de usuario o con el mounting
   del home directory.

Lo relevante es que el mecanismo de backup existente
(NO se detecto la anomalia al arrancar) porque:
  - El backup solo cubria el repositorio (~/hermes-lab/)
  - No cubria el entorno de ejecucion (uv, cargo, ~/.local/bin)
  - No habia diff de estado entre sesiones

═══════════════════════════════════════════════════════════
SINTOMAS
═══════════════════════════════════════════════════════════

- uv --version → command not found
- ~/.local/share/uv/ → no existe el directorio
- Hermes no podia ejecutar Python con las herramientas
  del toolchain
- Los .venv existentes apuntaban a python3.14 que uv
  gestionaba, y al desaparecer uv el enlace se rompio

═══════════════════════════════════════════════════════════
DIAGNOSTICO
═══════════════════════════════════════════════════════════

1.  Verificar existencia de ~/.local/share/uv/
2.  Verificar comando uv funciona
3.  Verificar python3 --version
4.  Verificar .venv/bin/python existe
5.  Verificar PATH contiene ~/.local/bin

Comandos usados en el diagnostico:
  ls -la ~/.local/share/uv/ 2>&1
  uv --version 2>&1
  python3 --version
  echo $PATH | tr ':' '\n'

═══════════════════════════════════════════════════════════
REPARACION
═══════════════════════════════════════════════════════════

Paso 1: Reinstalar uv
  curl -LsSf https://astral.sh/uv/install.sh | sh

Paso 2: Verificar instalacion
  uv --version
  ls ~/.local/share/uv/

Paso 3: Restaurar el PATH en .bashrc si es necesario
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

Paso 4: Probar Hermes
  hermes

Tiempo total de reparacion: ~5 minutos

═══════════════════════════════════════════════════════════
PREVENCION (implementado post-incidente)
═══════════════════════════════════════════════════════════

1. Anadido ~/.local/share/uv/ al backup en rescue.sh
   (commit 93d2b44 en hermes-lab)

2. Anadido ~/.cargo/bin/ y ~/.local/bin/ al backup

3. Creado protocolo inicio/fin con:
   - check-uv.sh: verifica que uv existe
   - estado-inicial.json: snapshot del estado al arrancar
   - estado-final.json: snapshot al cerrar
   - diff automatico entre estados para detectar anomalias

4. Creado check-path.sh: verifica que PATH contiene
   las rutas criticas (~/.local/bin, ~/.cargo/bin)

═══════════════════════════════════════════════════════════
LECCIONES APRENDIDAS
═══════════════════════════════════════════════════════════

- El backup del repositorio NO es suficiente.
  El entorno de ejecucion (toolchains, binarios, PATH)
  debe respaldarse por separado.

- Sin un diff de estado entre sesiones, una anomalia
  como esta solo se detecta cuando algo falla.

- El protocolo inicio/fin convierte la deteccion de
  anomalias de reactiva a preventiva.

- Los directorios de usuario (~/.local/, ~/.cargo/) son
  vulnerables a limpiezas automaticas del sistema.
  Deben estar monitorizados.

═══════════════════════════════════════════════════════════
REFERENCIAS
═══════════════════════════════════════════════════════════

- rescue.sh: ~/hermes-lab/scripts/rescue.sh (commit 93d2b44)
- Protocolo inicio: ~/joko-lab/02-infrastructure/inicio/protocolo.md
- Protocolo fin: ~/joko-lab/02-infrastructure/fin/protocolo.md
- check-uv.sh: ~/joko-lab/02-infrastructure/inicio/checks/check-uv.sh
- check-path.sh: ~/joko-lab/02-infrastructure/inicio/checks/check-path.sh
- Documento de estructura: ~/informes-joko-lab/2026-07-28-estructura-joko-lab-5-pilares.txt

═══════════════════════════════════════════════════════════
FIN DEL INFORME
═══════════════════════════════════════════════════════════

## Conexiones

- [[checklist-recuperacion]] — checklist-recuperacion: procedimiento que responde a este incidente
- [[GUIA-JOKO-LAB]] — GUIA-JOKO-LAB: mapa oficial del lab afectado
