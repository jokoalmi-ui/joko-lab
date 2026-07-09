# hermes-expert — Comandos

> Comandos para explorar y diagnosticar Hermes.
> Solo lectura salvo indicación contraria.

## Estructura

```bash
# Árbol completo de ~/.hermes/
ls -la ~/.hermes/

# Skills instaladas
ls ~/.hermes/skills/

# Skills con SKILL.md propio
for s in ~/.hermes/skills/*/SKILL.md; do echo "$(basename $(dirname "$s"))"; done

# Memorias
cat ~/.hermes/memories/MEMORY.md
cat ~/.hermes/memories/USER.md

# Logs
ls ~/.hermes/logs/
```

## Configuración

```bash
# Ver configuración completa
cat ~/.hermes/config.yaml

# Ver solo modelo
grep -A5 '^model:' ~/.hermes/config.yaml

# Ver solo agente
grep -A20 '^agent:' ~/.hermes/config.yaml

# Ver personalidades
grep -A2 'personalities:' ~/.hermes/config.yaml

# Ver toolsets
grep -A10 'platform_toolsets:' ~/.hermes/config.yaml

# Ver proveedores personalizados
grep -A10 'custom_providers:' ~/.hermes/config.yaml

# Contar líneas de config
wc -l ~/.hermes/config.yaml
```

## Estado

```bash
# Tamaño de la base de datos de sesiones
ls -lh ~/.hermes/state.db*

# Skills snapshot
cat ~/.hermes/.skills_prompt_snapshot.json | python3 -m json.tool 2>/dev/null | head -50

# Procesos activos
cat ~/.hermes/processes.json 2>/dev/null

# SOUL.md (personalidad activa)
wc -l ~/.hermes/SOUL.md
head -30 ~/.hermes/SOUL.md
```

## hermes CLI

```bash
# Ayuda general
hermes --help

# Diagnóstico
hermes doctor

# Versión
hermes --version
```

## Diagnóstico de skills del laboratorio

```bash
# Listar skills de hermes-lab
ls ~/hermes-lab/skills/

# Ver estructura de una skill
ls -la ~/hermes-lab/skills/<nombre>/

# Estado de carga real vs documentado
echo "Skills en ~/.hermes/skills/: $(ls ~/.hermes/skills/ | wc -l)"
echo "Skills con SKILL.md: $(for s in ~/.hermes/skills/*/SKILL.md; do echo 1; done | wc -l)"
echo "Skills en hermes-lab/: $(ls ~/hermes-lab/skills/ | wc -l)"
```
