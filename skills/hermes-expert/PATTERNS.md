# hermes-expert — Patrones de experiencia

> Registro de problemas recurrentes, su diagnóstico habitual y solución.
> No es documentación teórica. Es experiencia operativa acumulada.
> Se añade una entrada cada vez que se resuelve un problema repetible.

## Formato de cada entrada

```
## YYYY-MM-DD — Título del patrón

### Problema
Descripción clara del síntoma.

### Causa habitual
Qué suele estar pasando realmente.

### Diagnóstico
Comandos o comprobaciones para confirmar la causa.

### Solución
Pasos para resolverlo.

### Notas
Contexto adicional, variantes, cosas que no funcionaron.
```

---

## 2026-07-05 — Hermes no encuentra una skill

### Problema
Una skill existe en `~/.hermes/skills/` pero Hermes no la carga o no la reconoce.

### Causa habitual
El directorio de la skill existe pero no tiene `SKILL.md` con metadatos válidos, o el archivo está vacío.

### Diagnóstico
```bash
# Verificar si la skill tiene SKILL.md
ls ~/.hermes/skills/<nombre>/SKILL.md

# Verificar si el SKILL.md tiene contenido
cat ~/.hermes/skills/<nombre>/SKILL.md

# Ver skills que Hermes reconoce como activas
cat ~/.hermes/.skills_prompt_snapshot.json | python3 -m json.tool 2>/dev/null | head -30
```

### Solución
Asegurarse de que `SKILL.md` existe, no está vacío y contiene al menos:

```yaml
---
name: <nombre-skill>
description: <descripción breve>
---
```

### Notas
- De las 18 skills instaladas, solo 4 tienen SKILL.md propio. Las 14 restantes usan DESCRIPTION.md. Está pendiente verificar si DESCRIPTION.md también las carga.
- Las skills de `hermes-lab/` no están en `~/.hermes/skills/`. Son independientes. Hermes no las reconoce aunque tengan SKILL.md.

---

## 2026-07-05 — Hermes pregunta demasiadas cosas en cada turno

### Problema
Hermes pide confirmación constante para acciones que deberían ser rutinarias. La conversación avanza muy lenta.

### Causa habitual
No hay suficiente contexto sobre preferencias y reglas del usuario en `HERMES.md`, `USER.md` o `MEMORY.md`. Hermes no tiene suficiente información para tomar decisiones con confianza.

### Diagnóstico
```bash
# Ver tamaño del USER.md
wc -c ~/.hermes/memories/USER.md

# Ver tamaño del MEMORY.md
wc -c ~/.hermes/memories/MEMORY.md

# Buscar directivas de confirmación
grep -i "confirm" ~/.hermes/config.yaml
```

### Solución
Añadir contexto más explícito en `USER.md` sobre preferencias del usuario y en `MEMORY.md` sobre reglas operativas. Por ejemplo:

```
User prefers: soluciones simples, comando único, preguntar solo si hay riesgo real.
```

### Notas
- No confundir con la regla de seguridad "no ejecutar comandos automáticamente". Esa es deliberada. El problema es cuando Hermes pregunta cosas que ya debería saber por contexto.

---

## 2026-07-05 — La documentación del laboratorio se contradice

### Problema
Dos archivos de `hermes-lab/` dicen cosas diferentes sobre el mismo tema (por ejemplo, una regla aparece en `HERMES.md` y otra diferente en una `SKILL.md`).

### Causa habitual
Se creó documentación sin seguir el orden de consulta definido en `HERMES.md` §3, o se duplicó información en lugar de referenciar el archivo fuente.

### Diagnóstico
```bash
# Buscar temas duplicados entre archivos
grep -rl "tema" ~/hermes-lab/HERMES.md ~/hermes-lab/README.md ~/hermes-lab/docs/ ~/hermes-lab/skills/
```

### Solución
1. Identificar el archivo fuente según el orden de consulta (HERMES.md > arquitectura.md > decisiones > skill).
2. Unificar en el archivo fuente.
3. En los demás archivos, reemplazar el contenido duplicado por una referencia: "Ver HERMES.md §X".
4. Registrar la decisión en `docs/decisiones/` si el cambio es significativo.

### Notas
- HERMES.md §3 es la regla: HERMES.md → docs/arquitectura.md → docs/decisiones/ → skill → notificar incoherencias → no duplicar.
- SKILL.md joko-lab ya se limpió de principios duplicados y apunta a HERMES.md.

---

## 2026-07-05 — Servicio Docker no responde pero el contenedor parece activo

### Problema
El comando `docker compose ps` muestra el servicio como "Up" pero no responde en su puerto.

### Causa habitual
El contenedor está levantado pero el proceso interno está en estado de error (bucle de reinicio, configuración incorrecta, dependencia caída).

### Diagnóstico
```bash
# Ver logs del servicio
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml logs --tail=80 <servicio>

# Ver si realmente escucha en el puerto
ss -ltnp | grep <puerto>
```

### Solución
Revisar los logs. Si el error es de configuración, corregir y recargar solo ese servicio:
```bash
docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml up -d <servicio>
```

### Notas
- No confundir "Up" con "funcionando". Un contenedor puede estar vivo pero inutilizable.
- Este patrón aplica especialmente a n8n, Ollama y servicios con dependencias de base de datos o red.
