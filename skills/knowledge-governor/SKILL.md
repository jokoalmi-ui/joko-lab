# knowledge-governor

**Propósito:** Vigilar la integridad del conocimiento documentado en Joko Lab.

**Autor:** Hermes Agent (creada por el propietario)
**Versión:** v0.1.0
**Etapa:** 1 — Comprender
**Nivel de madurez:** 1 — Definida

---

## ¿Qué es?

knowledge-governor es la skill responsable del control de calidad de la
documentación y el conocimiento del laboratorio.

No gestiona inventario, no prioriza trabajo, no ejecuta cambios.
Solo detecta e informa de incoherencias en el conocimiento documentado.

## ¿Qué vigila?

| Ámbito | Qué comprueba |
|--------|---------------|
| Documentos duplicados | Mismo contenido en dos rutas distintas |
| Enlaces rotos | Referencias a archivos que ya no existen |
| Decisiones sin implementar | Estado "Pendiente" con fecha >30 días sin avance |
| Roadmap desactualizado | Tareas marcadas como pendientes que ya se resolvieron |
| Certificaciones obsoletas | Casos C-XXX que referencian documentos modificados |
| Skills sin referencias | Skill que existe pero no aparece en ningún otro documento |
| Cambios sin changelog | Archivos modificados cuyo CHANGELOG no se actualizó |

## ¿Qué NO hace?

- No gestiona inventario de skills (lo hace lab-manager).
- No prioriza trabajo (lo hace lab-manager).
- No ejecuta cambios sobre los archivos.
- No audita el estado técnico de los servicios (Docker, n8n, etc.).

## Relación con lab-manager

lab-manager es el arquitecto del laboratorio. Conoce todo el sistema,
prioriza, diagnostica y coordina.

knowledge-governor es el revisor de calidad. Se centra exclusivamente en
el conocimiento documentado: docs/, decisions/, certification/, skills/.

No se solapan. Se complementan:

- lab-manager dice: "La skill X tiene deuda técnica alta."
- knowledge-governor dice: "El archivo Y se referencia desde 3 documentos
  pero ya no existe en disco."

## Cuándo usarla

- Al final de una sesión de trabajo, para verificar que no se han introducido
  incoherencias.
- Antes de una auditoría, para limpiar problemas documentales menores.
- Periódicamente (semanal o quincenal) como mantenimiento preventivo.
- Cuando se modifica la certificación, para verificar que los casos C-XXX
  siguen siendo válidos.

## Ciclo de ejecución recomendado

```
1. Ejecutar governor-check.sh --all
2. Revisar informes generados en /tmp/knowledge-governor/
3. Corregir los problemas detectados (cada dominio responsable)
4. Si se corrige algo, actualizar CHANGELOG del dominio afectado
5. Si no se corrige, registrar en docs/decisiones/ el motivo
```
