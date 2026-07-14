# Visión de Joko Lab: Los Modeles como Roles

Fecha: 2026-07-10
Autor: Usuario + Hermes Agent

## El cambio de paradigma

Ya no se trata de "cómo hago que Hermes cambie entre DeepSeek y Ollama".

Se trata de:

> ¿Cómo quiero que piense Joko Lab cuando dispone de varios cerebros?

Los modelos ya no son proveedores. Son **roles** dentro del laboratorio.

## Los tres roles

| Modelo | Rol | Disponibilidad | Coste |
|--------|-----|---------------|-------|
| Mistral Nemo (Ollama) | Arquitecto residente | 24/7 | Gratuito |
| DeepSeek v4-flash | Especialista de alto razonamiento | Franja normal (12:00-03:00) | Bajo |
| Gemini 3.1 Flash Lite | Especialista de apoyo | Franja cara (03:00-12:00) | Bajo |

### Arquitecto residente (Mistral Nemo)

Siempre disponible. Privado. Sin coste. Debe resolver todo lo que pueda.

No se pregunta "¿activamos Ollama?". Se pregunta "¿esto necesita más capacidad
de la que tiene el arquitecto residente?".

### Especialistas externos (DeepSeek, Gemini)

Se usan cuando el arquitecto residente no puede resolver la tarea. La elección
entre DeepSeek y Gemini es una **regla horaria** por motivos de coste, no una
decisión técnica.

## La política de decisión

El ai-router deja de ser un script que cambia un proveedor. Pasa a ser la
**política de decisión del laboratorio**:

```
Usuario
   │
   ▼
ai-router
   │
   ├── ¿Puede resolverlo Mistral?
   │       │
   │       ├── Sí → Ollama
   │       │
   │       └── No
   │             │
   │             ├── 03:00-12:00 → Gemini
   │             │
   │             └── 12:00-03:00 → DeepSeek
   │
   └── Si el online falla → volver a Ollama
```

El horario es solo una **regla** dentro de la política. La arquitectura no
depende del horario; depende del rol que cumple cada modelo.

## Implicaciones para la arquitectura

1. Hermes arranca siempre con Ollama como modelo principal.
2. fallback_providers apunta al especialista de la franja horaria.
3. auxiliary tasks (visión, web extract, compression) van directo al
   especialista externo.
4. El cron solo actualiza qué especialista externo está activo según la hora.
5. Para escalar manualmente: /model deepseek o /model custom:local.

## Próximo salto: subsistema de gobierno

Esta visión de roles es el primer paso hacia un subsistema de gobierno donde
las skills ya no son independientes sino que cooperan bajo reglas comunes:

```
HERMES.md
     │
     ▼
joko-lab
     │
     ▼
lab-manager
     │
     ├── documentación
     ├── auditoría
     ├── certificación
     ├── roadmap
     └── ai-router
                │
                ├── Ollama
                ├── DeepSeek
                └── Gemini
```

Dejar de crear skills independientes y empezar a definir un sistema operativo
para el laboratorio.
