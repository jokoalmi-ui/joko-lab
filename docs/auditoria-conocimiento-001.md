---
type: docs
subtype: docs
status: active
tags: [docs]
created: 2026-07-29
---
# Auditoria conocimiento 001

AUDITORIA DE CONOCIMIENTO — MODELO EMERGENTE
===============================================
Fecha: 2026-07-29
Metodo: Analisis de campos comunes en 3 experimentos, 3 decisiones,
        8 fichas de modelo, 2 patrones, 1 catalogo de anti-patrones.

═══════════════════════════════════════════════════════════
1. ¿QUE EXISTE?
═══════════════════════════════════════════════════════════

Se analizaron 17 entidades de 4 tipos distintos:

  Experimentos:  3 (EXP-20260726-001, 002, 003)
  Decisiones:    3 (DEC-001, 002, 003)
  Fichas modelo: 8 (deepseek, gemma, glm, qwen3, qwen3.5, dolphin, llama, granite)
  Patrones:      2 (large-creative-model, atomic-prompt-glm)
  Anti-patrones: 6 FATAL + 5 ALTA + 3 MEDIA + 1 BAJA

═══════════════════════════════════════════════════════════
2. CAMPOS QUE APARECEN EN TODAS LAS ENTIDADES
═══════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────┐
  │                     NUCLEO COMUN                      │
  ├─────────────────────────────────────────────────────┤
  │                                                       │
  │  1. IDENTIDAD       → ID unico del tipo               │
  │                       (EXP-NNN, DEC-NNN, model id)    │
  │                                                       │
  │  2. FECHA           → Cuando se creo o actualizo      │
  │                                                       │
  │  3. ESTADO          → activo, completado, descartado  │
  │                                                       │
  │  4. TIPO            → experimento, decision, patron   │
  │                       ficha, anti-patron              │
  │                                                       │
  │  5. CONTENIDO       → El cuerpo de la entidad         │
  │                       (lo que realmente dice)         │
  │                                                       │
  │  6. EVIDENCIA       → Referencia a otra entidad       │
  │                       que la respalda                 │
  │                                                       │
  │  7. APLICABILIDAD   → Modelos/contextos afectados     │
  │                                                       │
  └─────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════
3. CAMPOS ESPECIFICOS POR TIPO
═══════════════════════════════════════════════════════════

EXPERIMENTO:
  Nucleo comun + Objetivo + Condiciones + Resultados +
  Aprendizaje (E1/E2/E3) + Referencias

DECISION:
  Nucleo comun + Motivo + Confianza + Consecuencias +
  Fecha revision + Sustituida por

FICHA DE MODELO:
  Nucleo comun + Version + Cuantizacion + Engine +
  Fortalezas + Debilidades + Parametros +
  Prompts ideales + Prompts que fallan + Anti-patrones

PATRON:
  Nucleo comun + Proposito + Entrada + Salida +
  Riesgos + Mitigaciones + Modelos compatibles + Ejemplo

ANTI-PATRON:
  Nucleo comun + Gravedad (FATAL/ALTA/MEDIA/BAJA) +
  Modelos afectados + Contexto

═══════════════════════════════════════════════════════════
4. RELACIONES ENTRE ENTIDADES
═══════════════════════════════════════════════════════════

  Experimento ────produce────→ E1/E2/E3 (clasificacion LPA)
       │
       ├──respalda──→ Decision  (via "Evidencia")
       ├──respalda──→ Ficha     (via "Benchmarks")
       ├──respalda──→ Patron    (via "Experimentos de validacion")
       └──respalda──→ Anti-patron (via contexto)

  Decision ────afecta────→ Modelos (via "Aplica a")
       │
       └──caduca────→ Decision nueva (via "Sustituida por")

  Ficha ────contiene────→ Parametros recomendados
       │
       └──referencia──→ Anti-patrones asociados

  Patron ────aplica────→ Modelos compatibles
       │
       └──mitiga────→ Riesgos conocidos

═══════════════════════════════════════════════════════════
5. MODELO DE CONOCIMIENTO FORMALIZADO
═══════════════════════════════════════════════════════════

Basado en los campos que ya existen en los datos reales,
el modelo de conocimiento de Joko Lab es:

  Entidad = {
    id:          string        (unico por tipo)
    tipo:        enum          (experimento, decision, ficha,
                                 patron, anti-patron)
    fecha:       datetime      (creacion o actualizacion)
    estado:      enum          (activo, completado, descartado,
                                 pendiente)

    contenido:   text          (el cuerpo de la entidad)

    evidencia:   referencia[]  (ids de entidades que lo respaldan)
    aplica_a:    referencia[]  (modelos, scripts, procesos afectados)

    // Solo para decisiones y experimentos:
    confianza:   enum?         (ALTA, MEDIA, BAJA)
    revision:    datetime?     (cuando re-evaluar)

    // Solo para clasificacion LPA:
    lpa:         enum?         (E1, E2, E3)
  }

  Relacion = {
    origen:      id            (entidad que referencia)
    destino:     id            (entidad referenciada)
    tipo:        enum          (produce, respalda, afecta,
                                 caduca, contiene, referencia,
                                 aplica, mitiga)
  }

═══════════════════════════════════════════════════════════
6. PRINCIPIO DE COMPATIBILIDAD FUTURA
═══════════════════════════════════════════════════════════

Regla: Ningun dato nuevo podra almacenarse de forma que
impida su razonamiento automatico futuro.

Esto no impone formato (YAML, JSON, MD son validos).
Pero exige que cualquier entidad nueva tenga al menos:
  - ID unico
  - Fecha
  - Estado
  - Tipo explicito
  - Referencias a otras entidades cuando sea relevante

Sin esos 5 campos minimos, el conocimiento no es
reutilizable por una maquina en el futuro.

═══════════════════════════════════════════════════════════
7. SEPARACION: KNOWLEDGE MODEL vs KNOWLEDGE REPRESENTATION
═══════════════════════════════════════════════════════════

El modelo (que existe) es independiente de la representacion
(como se almacena).

  MODELO (logico):              REPRESENTACION (fisica):
  ───────────────────────────   ──────────────────────────
  Entidad con nucleo comun     YAML frontmatter (fichas)
  + campos especificos         Markdown plano (experimentos)
  + relaciones                 JSON (estado, configs)
                               JSONL (sesiones)
                               Directorios + archivos

La representacion puede cambiar (ej: migrar a SQLite).
El modelo no.

═══════════════════════════════════════════════════════════
8. PROXIMA AUDITORIA
═══════════════════════════════════════════════════════════

Ejecutar cuando se alcancen 20 experimentos O 50 entidades
totales (lo que ocurra primero).

Pregunta a responder:
  "¿Que estructuras comunes han emergido que no estaban
   en la auditoria anterior?"

Si un patron aparece repetidamente → formalizar como regla.
Si no aparece → no forzar.

═══════════════════════════════════════════════════════════
FIN DE LA AUDITORIA
═══════════════════════════════════════════════════════════
