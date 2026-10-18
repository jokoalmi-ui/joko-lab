---
type: infrastructure
subtype: infrastructure
status: active
tags: [infrastructure]
created: 2026-07-28
---
# Checklist recuperacion

CHECKLIST DE RECUPERACION — Joko Lab
======================================
Version: 1.0.0
Fecha: 2026-07-28

═══════════════════════════════════════════════════════════
PASO 1: DETECTAR LA ANOMALIA
═══════════════════════════════════════════════════════════

[ ] Ejecutar ./inicio.sh
[ ] Revisar anomalias reportadas
[ ] Si hay errores (FAIL), NO empezar a trabajar
[ ] Si hay advertencias (WARN), evaluar gravedad

═══════════════════════════════════════════════════════════
PASO 2: DIAGNOSTICO RAPIDO
═══════════════════════════════════════════════════════════

[ ] docker ps — contenedores activos
[ ] curl localhost:11434/api/tags — Ollama responde
[ ] uv --version — toolchain Python
[ ] cargo --version — toolchain Rust
[ ] python3 --version — interprete Python
[ ] node --version — Node.js
[ ] git status — repositorio limpio
[ ] hermes doctor — estado de Hermes

═══════════════════════════════════════════════════════════
PASO 3: REPARACION POR SINTOMA
═══════════════════════════════════════════════════════════

Sintoma: ~/.local/share/uv no existe
  curl -LsSf https://astral.sh/uv/install.sh | sh

Sintoma: cargo no instalado
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

Sintoma: docker no responde
  systemctl --user start docker
  sudo systemctl start docker

Sintoma: ollama no responde
  systemctl --user start ollama
  docker compose -f automation-stack/docker-compose.yml up -d ollama

Sintoma: gateway no responde
  hermes gateway start

Sintoma: n8n no responde
  docker compose -f automation-stack/docker-compose.yml up -d n8n

═══════════════════════════════════════════════════════════
PASO 4: VERIFICACION POST-REPARACION
═══════════════════════════════════════════════════════════

[ ] Ejecutar ./inicio.sh de nuevo
[ ] Todos los checks deben pasar (o solo WARN aceptables)
[ ] estado-inicial.json generado correctamente
[ ] Revisar diff. Si hay anomalias que persisten, documentar

═══════════════════════════════════════════════════════════
PASO 5: DOCUMENTAR
═══════════════════════════════════════════════════════════

[ ] Abrir incidente en 02-infrastructure/recovery/procedures/
[ ] Registrar: fecha, sintoma, causa, reparacion, tiempo
[ ] Anotar si se necesita actualizar check o backup

═══════════════════════════════════════════════════════════
FIN DEL CHECKLIST
═══════════════════════════════════════════════════════════

## Conexiones

- [[inicio]] — inicio: protocolo de apertura que invoca este checklist
- [[incidente-uv-20260728]] — incidente-uv-20260728: incidente que originó la recuperación
