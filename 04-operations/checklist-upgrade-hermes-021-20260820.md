---
title: "Checklist de upgrade Hermes 0.21 — preparado el 20-ago-2026 (A3, bloqueado hasta 23-ago)"
type: operations
---

# Checklist de upgrade Hermes 0.21 — preparado el 20-ago-2026 (A3, bloqueado hasta 23-ago)

fecha: 2026-08-20
estado: PREPARADO (ejecutar el 23-ago o cuando el usuario confirme)
objetivo: desbloquear A3 (Bot Mode / A2A) sin romper skills, config, crons, bundles ni MCPs.

## Por qué
- El lab está en Hermes 0.17.0; Bot Mode/A2A requieren ≥0.20.
- El .0 suele tener bugs (lección del análisis Hermes 0.20 Gerald: esperar el .x).
- Hito: revisar el 23-ago (ver itinerario, Parte 4).

## ANTES de actualizar (mismo día, con salida real)

1. Anotar versión actual:
   ```bash
   hermes --version
   ```
2. Backup de config ([[RULE-008]]):
   ```bash
   cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak-YYYYMMDD-pre021
   ```
3. Snapshot del estado actual (para comparar después):
   ```bash
   hermes bundles list              # esperado: 4 (lab-diag, perfume-dia, vigilar-ig, bolsa)
   hermes mcp list                  # esperado: animation-server, lab-db, lancedb (21 tools)
   hermes skills list | grep -c enabled
   hermes cron list --all | grep -c active
   ```
4. Verificar que los scripts del lab no dependen de APIs de Hermes internas:
   - `~/.hermes/scripts/*.sh` (45 archivos) — la mayoría son bash puro (curl, python, lancedb), no tocan internals de Hermes. Verificar los que sí: session-heartbeat.sh, ceder-control.sh, domain-bus.sh.
   - `grep -rn "hermes" ~/.hermes/scripts/*.sh | grep -v "^Binary" | head -20`

## DURANTE la actualización

5. Actualizar con el método oficial (ver skill hermes-agent — NO inventar el comando):
   ```bash
   hermes update            # o el comando que documente la skill en ese momento
   ```
   (Si la skill hermes-agent cambió, seguirla — es la fuente de verdad.)

## DESPUÉS (verificación obligatoria, misma sesión)

6. Versión nueva:
   ```bash
   hermes --version | grep -E "0\.(2[0-9]|[0-9])"
   ```
7. Config intacta:
   ```bash
   diff <(grep -vE "^\s*#|^\s*$" ~/.hermes/config.yaml) \
        <(grep -vE "^\s*#|^\s*$" ~/.hermes/config.yaml.bak-YYYYMMDD-pre021) | head -30
   # → sin diferencias = OK
   ```
8. Bundles 4/4:
   ```bash
   hermes bundles list
   ```
9. MCPs 3/3 (21 tools):
   ```bash
   hermes mcp list
   ```
10. Crons activos (verificar que siguen enabled; los no_agent son los más frágiles):
    ```bash
    hermes cron list --all | grep -cE "\[active\]"
    ```
11. Skills (ninguna local rota):
    ```bash
    hermes skills list | grep -c "enabled"
    ```
12. Probar un arranque real de sesión + una búsqueda RAG (depende de MCP lancedb):
    ```bash
    hermes mcp test lancedb
    ```

## DESPUÉS de la verificación — A3 desbloqueado (NO ejecutar sin confirmación)

- Bot Mode: configurar agente persistente multi-rol (documentar en skill).
- A2A: formalizar colaboración CLI↔Telegram (el gateway TG ya está operativo).

## Reglas
- NO actualizar sin confirmación explícita del usuario.
- Si algo falla tras el upgrade: restaurar config del backup y reportar el error
  exacto (no concluir "todo roto").
- Registrar el resultado en backlog + shared-events (RULE-009).
