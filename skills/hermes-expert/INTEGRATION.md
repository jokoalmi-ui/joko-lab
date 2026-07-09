# Integración de skills de hermes-lab en Hermes Agent

## Contexto

Hermes Agent carga skills desde `~/.hermes/skills/`. Cada skill es un directorio con un archivo `SKILL.md` como mínimo. Las skills de `hermes-lab/` tienen una estructura de documentación más rica (README, COMMANDS, SAFETY, etc.) que debe simplificarse a un solo SKILL.md para que Hermes las cargue.

## Estructura esperada por Hermes

```
~/.hermes/skills/<nombre>/
├── SKILL.md        → obligatorio (lo que Hermes carga)
├── references/     → opcional (archivos de referencia)
└── templates/      → opcional (plantillas)
```

## Estructura de origen en hermes-lab

```
~/hermes-lab/skills/<nombre>/
├── SKILL.md         → debe pasar a ~/.hermes/skills/<nombre>/
├── README.md        → explicación humana (no la usa Hermes)
├── COMMANDS.md      → procedimientos (opcional, referencia)
├── SAFETY.md        → riesgos (opcional, referencia)
├── KNOWLEDGE.md     → conocimiento profundo (opcional)
└── ...
```

## Procedimiento para integrar una skill

### 1. Copiar el SKILL.md

```bash
# Crear directorio en Hermes
mkdir -p ~/.hermes/skills/<nombre>

# Copiar SKILL.md
cp ~/hermes-lab/skills/<nombre>/SKILL.md ~/.hermes/skills/<nombre>/

# Verificar
cat ~/.hermes/skills/<nombre>/SKILL.md | head -10
```

### 2. Opcional: copiar soporte

Si la skill tiene `references/` o `templates/`, copiarlos también:

```bash
cp -r ~/hermes-lab/skills/<nombre>/references ~/.hermes/skills/<nombre>/ 2>/dev/null
cp -r ~/hermes-lab/skills/<nombre>/templates ~/.hermes/skills/<nombre>/ 2>/dev/null
```

### 3. Probar que se carga

```bash
# Listar skills — debe aparecer como "local"
hermes skills list | grep <nombre>

# Verificar que no da error
hermes doctor
```

### 4. Probar que funciona en sesión

```bash
# Cargar la skill explícitamente
hermes -s <nombre>
```

### 5. Para desinstalar

```bash
rm -rf ~/.hermes/skills/<nombre>
```

## Skills actuales de hermes-lab (julio 2026)

| Skill | Integrada en Hermes | Estado |
|---|---|---|
| hermes-expert | No | Documentación interna del laboratorio |
| joko-lab | No | Filosofía y principios |
| docker-admin | No | Etapa 3 — Actuar (scripts de backup, healthcheck, cron, actualización) |
| n8n-admin | No | Pendiente |
| ai-router | No | Pendiente |
| betterbird | No | Pendiente |
| perfumes | No | Pendiente |
| evolution | No | Pendiente |

## Notas

- Hermes distingue "local" vs "builtin" vs "hub". Las skills copiadas manualmente aparecen como "local".
- No es necesario reiniciar Hermes. Las skills se recargan en cada sesión.
- Las skills locales pueden editarse directamente en `~/.hermes/skills/`.
- Si una skill existe en `hermes-lab/` y en `~/.hermes/skills/`, la de `~/.hermes/skills/` es la que Hermes usa realmente.
