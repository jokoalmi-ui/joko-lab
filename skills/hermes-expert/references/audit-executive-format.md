# Auditoría Ejecutiva — Formato y Patrón

## Cuándo usarlo

Al finalizar una sesión de trabajo intensa en Joko Lab, o cuando el usuario pida explícitamente una auditoría de sistema.

## Estructura del archivo

El archivo se guarda como `auditoria-AAAA-MM-DD.txt` en la raíz de `hermes-lab/`.

## Secciones

### 1. Nivel de Madurez del Laboratorio

Puntuación global sobre 10. **ATENCIÓN:** Mide resiliencia y madurez, NO esfuerzo ni satisfacción. Un 9/10 significa que el sistema está completamente automatizado y gobernado sin intervención.

```
   Gobierno           ███████░░░  N/10 (Políticas, decisiones, roadmap)
   Operacion          ████████░░  N/10 (Skills tácticas, despliegues)
   Conocimiento       ████████░░  N/10 (Arquitectura, documentación real)
   Certificacion      ██████░░░░  N/10 (Validación de comprensión)
   IA y Enrutamiento  █████████░  N/10 (Arquitectura híbrida, routers)
```

### 2. Métrica Estrella: Autonomía del Laboratorio

¿Cuánto podría mantener otra persona (o IA limpia) utilizando únicamente HERMES.md, las skills y la documentación, sin depender de la memoria del propietario?

```
   Autonomía          ███████░░░  N %
```

### 3. Riesgo Principal

Identificar explícitamente el mayor punto de fallo o dependencia oculta actual en la infraestructura o en los procesos (ej. "Conocimiento implícito del creador sobre cómo levantar N servicio").

### 4. Comparativa con auditoría anterior

Tabla comparativa categoría por categoría con diferencia, más total anterior vs actual. Ajustar la escala si hubo un cambio de metodología.

### 5. Resumen global

Estado general y evaluación crítica de la arquitectura.

### 6. Logros de la sesión

Lista con checklist de todo lo completado en la sesión actual.

### 7. Infraestructura y servicios

Hardware, servicios activos con puertos y estado, proveedores IA, backups.

### 8. Próximos pasos priorizados (Backlog)

Ordenado por prioridad. **IMPORTANTE sobre Skills Vacías:** No preguntar "si hay que borrarlas", sino validar: *"¿Siguen teniendo un rol dentro de la arquitectura?"*.

## Encabezado y pie

```
=========================================================
   AUDITORIA EJECUTIVA — JOKO LAB
   Fecha: AAAA-MM-DD
=========================================================
...
=========================================================
   FIN DE AUDITORIA
   Fecha | Salud: N/10 | Autonomía: N% | +/- desde ultima
=========================================================
```

## Reglas

- La puntuación debe ser honesta y crítica. Si falta gobierno automático o certificación, la nota baja.
- Hacer commit del archivo inmediatamente después de crearlo.