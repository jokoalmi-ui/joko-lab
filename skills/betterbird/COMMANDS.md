# betterbird — Comandos

## Diagnóstico

```bash
# Verificar si Betterbird está instalado
which betterbird

# Verificar si está ejecutándose
ps aux | grep betterbird

# Ver perfil de datos
ls ~/.thunderbird/

# Ver estructura del perfil
ls -la ~/.thunderbird/*.default-release/
```

## Comandos de solo lectura

```bash
# Saber qué cliente de correo está activo actualmente
ps aux | grep -iE 'evolution|betterbird|thunderbird' | grep -v grep
```

## Sin más comandos definidos

Esta skill está en etapa 1 (Comprender). Betterbird no está activo actualmente. Si se reactiva, se documentarán comandos de búsqueda específicos.
