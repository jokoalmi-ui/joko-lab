# Registro de decisiones

## 2026-07-05

### Estructura de documentación de Joko Lab

**Contexto**

La documentación del laboratorio estaba dispersa: `decisiones.md` acumulaba todas las decisiones en un solo archivo, `arquitectura.md` estaba vacío, y no había una convención clara de organización.

**Problema**

Necesitábamos un sistema ordenado, mantenible y consultable para la documentación del laboratorio.

**Alternativas consideradas**

- Wiki
- Notion
- Documentación en los propios skills de Hermes

**Decisión adoptada**

Toda la documentación vive dentro de `~/hermes-lab/docs/`, en archivos Markdown independientes organizados por tema y fecha.

**Motivos**

- **Por qué toda la documentación vive en hermes-lab:** un solo punto de verdad dentro del laboratorio, accesible y versionable junto al resto del proyecto.
- **Por qué se usan Markdown:** formato universal, legible en crudo, sin dependencias, renderizable en cualquier plataforma (GitHub, terminal, editores).
- **Por qué todo debe ser legible desde terminal:** el laboratorio se opera principalmente desde CLI con Hermes Agent; la documentación debe consultarse sin salir del terminal.
- **Por qué evitar herramientas externas como Notion:** dependencia de conexión, interfaz gráfica, sin control de versiones nativo y fuera del flujo de trabajo local.

**Consecuencias**

- Las decisiones futuras se añaden como `AAAA-MM-DD-tema.md` en `docs/decisiones/`.
- La documentación se puede navegar con `cat`, `less` o `find` desde el terminal.

**Estado**

Vigente
