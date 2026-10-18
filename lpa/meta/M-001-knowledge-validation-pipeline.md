---
type: lpa
subtype: meta
status: active
tags: [lpa, meta]
created: 2026-07-30
---
# M-001: Knowledge Assimilation Pipeline (KAP)

**Tipo:** Procedimiento LPA — Fase 1 (prompt estructurado)
**Dominio:** Asimilación de conocimiento externo
**Fecha:** 2026-07-24 (v3: 2026-07-24 — clasificación de 4 resultados)
**Estado:** Activo — 3 usos completados
**Origen:** Pipeline YouTube→Hermes→ChatGPT→Hermes + crítica metodológica real

---

## Qué es

Un procedimiento nativo de Hermes para transformar cualquier fuente externa en conocimiento operativo para Joko Lab. No es un pipeline de transcripción ni de resumen. Es un mecanismo de asimilación: filtrar, validar y solo entonces incorporar.

**Fuentes que cubre:** vídeos, libros, artículos, papers, podcasts, conferencias, conversaciones con otras IAs, cursos.

**Misión (v3):** KAP no extrae conocimiento. KAP **actualiza el estado del conocimiento del laboratorio.** Cada fuente externa se clasifica en uno de 4 resultados:

| Resultado | Significado | Acción |
|---|---|---|
| **Crea** | Conocimiento genuinamente nuevo | Candidate Pattern en pattern-incubator/ |
| **Confirma** | Refuerza un patrón existente | Incrementa peso de evidencia, no duplica |
| **Contradice** | Debilita o refuta un patrón existente | Se registra como contraevidencia, puede degradar el patrón |
| **No modifica** | No cambia el estado del conocimiento | Se archiva como recurso (herramientas, ejemplos, inspiración) |

---

## Regla de las dos preguntas

Toda fuente analizada debe responder **dos preguntas independientes**:

1. **¿Cómo modifica el conocimiento del laboratorio?** → CREA / CONFIRMA / CONTRADICE / NO MODIFICA
2. **¿Qué artefactos útiles deja aunque no modifique LPA?** → herramientas, casos, legislación, ejemplos, tecnologías, bibliografía, datasets, workflows

Esto evita dos errores simétricos: contaminar LPA con recursos que no son principios, y perder recursos valiosos solo porque no son principios.

### Árbol de decisión

```
Nueva información
        │
        ▼
¿Modifica el conocimiento del laboratorio?
        │
 ┌──────┴────────┐
Sí               No
│                │
▼                ▼
LPA          ¿Es útil como recurso?
│                │
│         ┌──────┴─────────┐
│        Sí                No
│        │                 │
│        ▼                 ▼
│   Knowledge          Se descarta
│   Library
│
├── CREA → Candidate Pattern
├── CONFIRMA → Incrementa peso de evidencia
└── CONTRADICE → Se registra contraevidencia

---

## Regla de Oro

> Ningún recurso externo entra en LPA por ser interesante.
> Solo entra si cambia la forma en la que el laboratorio trabaja, aprende o construye.

---

## Shift mental obligatorio

La primera pregunta de Hermes ante cualquier recurso externo NO es:

> "¿Qué ideas tiene este vídeo?"

Es:

> **"¿Qué cambia en la forma de trabajar de Joko Lab después de ver este recurso?"**

Esto obliga a pensar en metodología, no en contenido.

---

## Las tres fases

### Fase A — Knowledge Extraction

```
Fuente externa (vídeo, libro, paper, podcast...)
        ↓
    Transcripción / texto completo
        ↓
      Hermes
        ↓
    Ideas clasificadas por tipo (sin juzgar validez)
```

**Responsable:** Hermes
**Objetivo:** Extraer y clasificar. No decidir todavía.

### Fase B — Adversarial Review

```
    Ideas clasificadas
        ↓
      Modelo externo (ChatGPT / Claude / otro)
        ↓
    Crítica metodológica
        ↓
      Hermes
        ↓
    Las 6 preguntas obligatorias (5 originales + 1 de confirmación)
```

**Responsable:** Modelo externo (crítica) + Hermes (decisión)
**Objetivo:** Someter cada idea a revisión adversarial y a las 6 preguntas

### Fase C — Asimilación

```
    Ideas que sobreviven
        ↓
      Hermes
        ↓
    Clasificación final + ubicación en LPA
```

**Responsable:** Hermes
**Objetivo:** Solo lo que pasa todos los filtros entra en el sistema

---

## Procedimiento completo

### Paso 1 — Obtener transcripción

```bash
# Para YouTube: usar youtube-content (local)
/home/jokoalmi/.hermes/.venv/bin/python3 \
  ~/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py \
  "URL" --text-only --timestamps --language es,en

# Para otras fuentes: extraer texto completo como sea necesario
```

### Paso 2 — Fase A: Extracción con Hermes

Prompt para Hermes:

```
Voy a pasarte la transcripción de [fuente]. NO me digas qué ideas tiene.
NO me digas si son válidas. Solo clasifícalas.

1. CLASIFICA cada idea según su tipo:
   □ Observación (dato puntual)
   □ Heurística (regla práctica, "suele funcionar")
   □ Procedimiento (secuencia de pasos)
   □ Patrón (se ha visto en 2+ contextos)
   □ Dato (cifra, estadística, hecho verificable)

2. EXTRAE solo Observaciones, Heurísticas, Procedimientos, Patrones y Datos.
   Descarta: opiniones, inspiración, marketing, filosofía, contexto histórico.

   Para cada una: timestamp, cita textual, tipo.

No evalúes. No decidas. Solo clasifica y extrae.
```

### Paso 3 — Fase B: Crítica adversarial (v5, 2026-07-31)

Copiar la salida de Hermes a un modelo externo (ChatGPT, Claude) con el prompt completo v5.

**Prompt actualizado:** `lpa/meta/M-001-prompts-v5.md`

La v5 incorpora respecto a v1: separación HECHO/INFERENCIA/HIPÓTESIS/OPINIÓN, origen de evidencia [FUENTE]/[HERMES]/[LAB]/[EXTERNO], condición de parada (EVIDENCIA INSUFICIENTE), 4 dimensiones por métrica (tokens, latencia, precisión, cobertura), falsación de conclusiones, categorías DESCARTAR/NO ACCIONABLE, backlog priorizado, metaevaluación con sesgo y experto.

### Paso 4 — Fase B: Las 6 preguntas obligatorias (5 originales + 1 de confirmación)

Copiar la crítica a Hermes. Para cada idea, responder en este orden:

---

**Pregunta 1 — ¿Ya lo sabíamos?**

Si ya está documentado en LPA → pasar a la pregunta 1b. No descartar automáticamente.

---

**Pregunta 1b — ¿Qué problema estructural de Joko Lab confirma esta fuente?**

Aunque la fuente no aporte nada nuevo, puede confirmar que estamos resolviendo el problema correcto. Eso es conocimiento útil.

| Respuesta | Significado | Acción |
|-----------|-------------|--------|
| Confirma un patrón existente | La fuente externa valida nuestra dirección | Incrementa peso de evidencia del patrón |
| Confirma que el problema existe | La fuente externa sufre el mismo problema | El problema no es imaginario. Se registra como evidencia externa |
| No confirma nada | La fuente aborda otro problema o la conexión es débil | Seguir a pregunta 2 sin cambios |

**Caso concreto:** Si una fuente propone "Graph Engineering" y Joko Lab ya tiene delegate_task + pipeline multi-modelo, la respuesta correcta es "Confirma el patrón CP-001" — no descartar porque "ya lo sabíamos".

---

**Pregunta 2 — ¿Cambia realmente cómo trabaja Joko Lab?**

Considerar:
- ¿Cambia LPA? (principios, niveles, definiciones)
- ¿Cambia Hermes? (skills, prompts, configuración)
- ¿Cambia la estructura del laboratorio?
- ¿Cambia un pipeline o workflow existente?
- ¿Cambia un proyecto activo?

Si la respuesta a TODAS es "no" → no entra. Es interesante, no operativo.

---

**Pregunta 3 — ¿Acelera la obtención de resultados físicos?**

El objetivo de Joko Lab no es escribir documentos. Es construir.
Si una idea no acerca el laboratorio a un resultado tangible
(una feature, un prototipo, un experimento, un producto),
probablemente no es conocimiento operativo todavía.

---

**Pregunta 4 — ¿Pertenece al proyecto o pertenece a LPA?**

Muchas cosas pertenecen solo a Perfume IA. Muy pocas pertenecen al laboratorio.

- Solo este proyecto → no entra en LPA
- Proyectos similares → candidate pattern
- Todo Joko Lab → procedimiento
- Todo LPA → principio

---

**Pregunta 5 — ¿Qué experimento concreto podremos hacer mañana gracias a esta idea?**

Si no desemboca en un experimento o mejora tangible del laboratorio,
probablemente aún no está madura para convertirse en conocimiento del sistema.

---

### Paso 5 — Filtro de transferibilidad

Para cada idea que sobreviva a las 6 preguntas:

> ¿Dónde volveremos a usar esto?

| Alcance | Acción |
|---|---|
| Solo este proyecto | No documentar en LPA. Dejar en el proyecto. |
| Proyectos similares | Candidate Pattern en pattern-incubator/ |
| Todo Joko Lab | Procedimiento en meta/ o procedures/ |
| Todo LPA | Principio en KNOWN.md |

### Paso 6 — Fase C: Documentar

Solo las ideas que superan los 6 filtros + transferibilidad entran.
Hermes escribe la decisión en la ubicación que corresponda.
Las ideas descartadas se registran con el motivo de descarte.

---

## Principios que aplica

- **Falsabilidad:** El revisor externo intenta romper antes de aceptar
- **Impacto real como filtro:** 6 preguntas, no solo "es interesante"
- **Resultados físicos > Documentación:** Pregunta 3 como anti-burocracia
- **Separación proyecto/LPA:** Pregunta 4 evita contaminación
- **Transferibilidad:** Solo se convierte en metodología lo que se usará en múltiples contextos
- **Autoridad final en Hermes:** El revisor externo critica, Hermes decide

---

## Conexiones con LPA

| Conexión | Detalle |
|---|---|
| **Nivel 3 (Epistemología)** | Responde a "¿cómo verificamos conocimiento?" con un mecanismo de 6 filtros |
| **Pipeline GLM→Gemma→Hermes** | Primera instancia del patrón multi-modelo |
| **Este pipeline (KAP)** | Segunda instancia. Mismo patrón, distinto dominio |
| **H-001 (Knowledge Layer)** | El output validado de KAP alimentaría la Knowledge Layer |
| **patterns-observed.md entradas 7+9** | Evidencia del patrón External Knowledge Assimilation |

---

## Estado de maduración

| Fase | Estado |
|---|---|
| 1. Prompt estructurado | ✅ Documentado aquí (v2 con mejoras) |
| 2. Instrumento | 🔄 Primer uso completado. Probado con Founders (1h). El contenido del vídeo no entró en LPA pero el pipeline demostró funcionar |
| 3. Skill LPA | ❌ Pendiente: validar en 2+ dominios distintos |
| 4. Automatización (n8n) | ❌ No antes de fase 3 |

---

## Historial de uso

| Fecha | Fuente | Ideas | Resultado | Notas |
|-------|--------|-------|-----------|-------|
| 2026-07-24 | Founders D1: Producción con IA | 13 → 0 | **No modifica** (Confirma patterns existentes) | Contenido ya operativo en Joko Lab. El pipeline funcionó: la crítica adversarial real mejoró KAP con 5 filtros. |
| 2026-07-24 | Founders D2: Spot publicitario | 8 → 0 | **Confirma** CP-00X (5ª instancia) | Evidencia externa independiente de workflows como activos reutilizables. |
| 2026-07-24 | Founders D3: Monetización | 7 → 0 | **No modifica** (aporta recursos) | H-02 (IA como asesor de negocio) es nuevo como concepto pero no alcanza nivel de patrón. Método 3-2-1 es recurso práctico, no principio LPA. El vídeo aporta herramientas, ejemplos y vocabulario — valioso como recurso, no como conocimiento LPA. |
| 2026-07-31 | PKM = Matemáticas (3 teorías) | 7 ideas → 0 nuevas, 3 confirmaciones | **CONFIRMA** (CP-00X, contract-first, necesidad estructura) | Video de 14m50s sobre PKM basado en grafos/conjuntos/orden. Métrica clave: 55x ahorro tokens con estructura. Fase B pendiente. P1 (medición tokens) iniciado: contexto RAG actual ~280 tokens, estructurado estimado ~70 tokens (ahorro ~75%). Prompt Fase B actualizado a v4 (10 mejoras). |
