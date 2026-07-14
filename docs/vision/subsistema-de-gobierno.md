# Subsistema de Gobierno de Joko Lab

Fecha: 2026-07-10
Versión: 0.1.0 (propuesta inicial)
Estado: Pendiente de implementación

## 1. ¿Qué es el subsistema de gobierno?

El subsistema de gobierno es el conjunto de reglas, roles, documentos y
mecanismos que permiten que Joko Lab opere de forma coherente, predecible
y mantenible. No es una skill nueva. Es la capa que organiza cómo cooperan
las skills existentes.

## 2. Estructura

```
HERMES.md  ← Constitución: principios, normas, organización
    │
    ▼
joko-lab  ← Identidad: contexto global del laboratorio
    │
    ▼
lab-manager  ← Arquitecto técnico: coordina, no ejecuta
    │
    ├── docs/          ← Conocimiento documentado
    │   ├── arquitectura.md
    │   ├── estado-real.md
    │   ├── roadmap.md
    │   ├── vision/    ← Documentos de visión
    │   └── decisiones/
    │
    ├── certification/ ← Validación de conocimiento
    │   ├── casos (C-001, C-002, C-003)
    │   └── rúbrica de evaluación
    │
    ├── auditoría      ← Inspección periódica del estado
    │   └── scripts/auditor-completo.py
    │
    ├── roadmap        ← Plan de evolución del laboratorio
    │
    └── ai-router      ← Política de decisión de IA
        │
        ├── Ollama (Arquitecto residente)     ← 24/7
        ├── DeepSeek (Especialista razonam.)  ← Franja normal
        └── Gemini (Especialista apoyo)       ← Franja cara
```

## 3. Reglas del gobierno

### 3.1. Quién gobierna

lab-manager es el único responsable del gobierno. No ejecuta cambios,
pero decide:

- Qué skills necesitan evolucionar
- Qué documentación necesita revisión
- Qué certificaciones validar
- Qué decisiones registrar

### 3.2. Cómo se gobierna

1. Por diagnóstico: lab-manager inspecciona el estado del laboratorio
   con sus scripts (diagnosticar.sh, deuda-tecnica.sh, cambios-ultima.sh).

2. Por documentación: toda decisión se registra en docs/decisiones/.
   La fuente de verdad es docs/. certification/ solo verifica.

3. Por política: ai-router aplica una política de decisión (no un simple
   cambio de proveedor). La política se documenta y se certifica.

### 3.3. Dominios gobernados

| Dominio | Responsable | Qué supervisa |
|---------|-------------|---------------|
| Documentación | lab-manager | Coherencia, actualización, no duplicación |
| Certificación | lab-manager | Casos activos, rúbrica, resultados |
| Auditoría | lab-manager | Estado real vs documentado |
| Roadmap | lab-manager | Prioridades, dependencias, progreso |
| IA (ai-router) | lab-manager | Política de decisión, roles de modelo |

### 3.4. Relación con las skills

lab-manager NO reemplaza a las skills. Las skills ejecutan. lab-manager
gobierna:

- Una skill dice: "Ollama responde en localhost:11434"
- lab-manager dice: "Eso cumple la política de decisión documentada"

## 4. Ciclo de gobierno

```
Inicio de sesión
    │
    ▼
lab-manager diagnóstica estado actual
    │
    ├── ¿Documentación coherente? → seguir
    │       └── No → registrar incidencia
    │
    ├── ¿Skills maduras? → seguir
    │       └── No → priorizar evolución
    │
    ├── ¿IA operativa según política? → seguir
    │       └── No → notificar a ai-router
    │
    └── ¿Decisiones registradas? → seguir
            └── No → proponer registro
```

## 5. Próximos pasos

1. Formalizar lab-manager como skill de gobierno (ya existe, evolucionar)
2. Añadir ai-router como subsistema bajo lab-manager
3. Añadir las comprobaciones de gobierno a diagnosticar.sh
4. Crear caso de certificación C-004: política de decisión de IA
