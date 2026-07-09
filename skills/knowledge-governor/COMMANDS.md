# knowledge-governor — COMMANDS

Órdenes y procedimientos para el control de calidad del conocimiento.

---

## Comprobaciones individuales

Cada comprobación se ejecuta con el script `scripts/governor-check.sh`.

### governor-check.sh --duplicados

Busca archivos en `docs/` y `certification/` con contenido idéntico.

```bash
bash scripts/governor-check.sh --duplicados
```

**Salida esperada:** Lista de pares de archivos duplicados o mensaje
"0 duplicados detectados."

**Severidad:** MEDIA — reducir redundancia.

---

### governor-check.sh --rotos

Busca referencias a rutas relativas que apunten a archivos inexistentes.

Busca en: `docs/`, `certification/`, `skills/` y `HERMES.md`.

```bash
bash scripts/governor-check.sh --rotos
```

**Salida esperada:** Archivo, línea, ruta rota.

**Severidad:** ALTA — enlace roto = documentación incorrecta.

---

### governor-check.sh --decisiones-pendientes

Busca en `docs/decisiones/` archivos cuyo Estado sea distinto de "Vigente"
y que tengan más de 30 días desde su creación.

```bash
bash scripts/governor-check.sh --decisiones-pendientes
```

**Salida esperada:** Lista de decisiones con Estado obsoleto.

**Severidad:** ALTA — decisiones olvidadas erosionan la confianza.

---

### governor-check.sh --skills-huerfanas

Busca skills en `skills/` que no son mencionadas en ningún otro documento
del laboratorio (`docs/`, `HERMES.md`, `certification/`, otras skills).

```bash
bash scripts/governor-check.sh --skills-huerfanas
```

**Salida esperada:** Nombres de skills no referenciadas.

**Severidad:** BAJA — puede ser intencional (skill en creación).

---

### governor-check.sh --changelogs

Busca archivos modificados en los últimos 7 días cuyo CHANGELOG.md
(o archivo de cambios correspondiente) no se haya actualizado.

```bash
bash scripts/governor-check.sh --changelogs
```

**Salida esperada:** Archivos modificados sin changelog actualizado.

**Severidad:** MEDIA — pérdida de trazabilidad.

---

### governor-check.sh --certificaciones

Verifica que cada caso C-XXX en `certification/tests/` referencia
documentos que realmente existen en `docs/`.

```bash
bash scripts/governor-check.sh --certificaciones
```

**Salida esperada:** Casos C-XXX con referencias rotas.

**Severidad:** ALTA — certificación inválida si referencia docs inexistentes.

---

### governor-check.sh --todo

Ejecuta todas las comprobaciones anteriores secuencialmente.

```bash
bash scripts/governor-check.sh --all
```

**Salida esperada:** Informe completo con resumen por categoría.

---

## Procedimientos

### Auditoría rápida (5 minutos)

```bash
cd ~/hermes-lab
bash skills/knowledge-governor/scripts/governor-check.sh --all
```

Revisar el informe en terminal. Los problemas ALTA deben corregirse antes
de cerrar la sesión. Los MEDIA pueden esperar a la siguiente sesión.

### Auditoría completa (20-30 minutos)

1. Ejecutar `--all`.
2. Revisar cada hallazgo manualmente.
3. Para cada hallazgo ALTA: corregir o registrar decisión de no corregir.
4. Para cada hallazgo MEDIA: priorizar para la siguiente sesión.
5. Actualizar CHANGELOG.md de la skill tras cada ejecución significativa.
