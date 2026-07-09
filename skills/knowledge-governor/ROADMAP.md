# knowledge-governor — ROADMAP

Qué le falta a esta skill para madurar.

---

## Próximo paso inmediato (etapa 2)

- [ ] Crear `scripts/governor-check.sh` con las 7 comprobaciones.
  - Prioridad: ALTA. Sin script la skill es solo documentación.

---

## Corto plazo (etapa 3)

- [ ] Probar cada comprobación contra el laboratorio real y ajustar falsos positivos.
- [ ] Añadir `scripts/governor-check.sh --automated` para ejecución sin supervisión.
- [ ] Documentar en COMMANDS.md los umbrales exactos de cada comprobación.

---

## Medio plazo (etapa 4)

- [ ] Integrar con lab-manager para que lab-manager pueda invocar governor-check
  antes de una auditoría.
- [ ] Añadir comprobación de consistencia entre `docs/roadmap.md` y las tareas
  reales documentadas en skills.
- [ ] Generar informe en formato markdown legible (no solo salida de terminal).

---

## Largo plazo (nivel 5+)

- [ ] Auditoría formal de la skill (revisión de su propia eficacia).
- [ ] Pruebas automatizadas (shellspec o bats) para cada comprobación.

---

## Riesgos conocidos

- Falsos positivos en skills huérfanas (skills recién creadas que aún no
  tienen referencias). Mitigación: severidad BAJA, no requiere acción inmediata.
- Enlaces rotos en documentación generada dinámicamente. Mitigación: el script
  solo revisa archivos estáticos.
