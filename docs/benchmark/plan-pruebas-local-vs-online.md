# Plan de pruebas: modelo local vs online vs combinado

## Objetivo
Comparar calidad de respuesta entre Ollama (local), DeepSeek (online) y
el sistema combinado (local con delegación a online para tareas complejas).

## Metodología

### Tareas de prueba (5 tareas representativas)

| # | Tarea | Tipo | Dominio |
|---|-------|------|---------|
| 1 | "Explica qué hace este Dockerfile" | Análisis simple | Docker |
| 2 | "Encuentra el error en este log de n8n" | Diagnóstico | n8n |
| 3 | "Diseña un workflow de n8n que lea un CSV, lo filtre y envíe un email" | Diseño | Automatización |
| 4 | "Optimiza este script bash: es lento y quiero que procese 10.000 archivos" | Optimización | Scripting |
| 5 | "Crea una expresión regular que extraiga fechas en formato DD/MM/AAAA de un texto, excluyendo las del año 2020" | Precisión técnica | Expresiones regulares |

### Criterios de evaluación (1-5)

| Criterio | Qué mide |
|----------|----------|
| Precisión | ¿La respuesta es correcta? ¿Hace lo que se pide? |
| Completitud | ¿Cubre todos los aspectos de la pregunta? |
| Claridad | ¿Está bien explicada? ¿Es útil para un humano? |
| Código funcional | Si genera código, ¿funcionaría sin modificaciones? |

### Ejecución

Cada tarea se ejecuta 3 veces:

1. **Local** — Ollama `llama31-8b-64k` (modelo actual)
2. **Online** — DeepSeek `deepseek-v4-flash` (modelo actual)
3. **Combinado** — Local analiza, online resuelve las partes complejas

Para las pruebas uso `delegate_task` que ya tengo como herramienta.

### Material de prueba

Necesito archivos reales para las tareas 1 y 2:
- Un `docker-compose.yml` o `Dockerfile` real del lab
- Un log real de n8n con algún error o warning

### Entrega

Una tabla comparativa como esta:

```
┌─────────────────────┬──────┬────────┬──────────┐
│ Tarea               │ Local│ Online │ Combinado│
├─────────────────────┼──────┼────────┼──────────┤
│ 1. Explicar Docker  │ 4.0  │ 4.5    │ 4.5      │
│ 2. Diagnosticar log │ 3.0  │ 5.0    │ 5.0      │
│ 3. Diseñar workflow │ 2.5  │ 4.5    │ 4.5      │
│ 4. Optimizar script │ 3.5  │ 5.0    │ 5.0      │
│ 5. Regex precisa    │ 2.0  │ 4.5    │ 4.5      │
├─────────────────────┼──────┼────────┼──────────┤
│ Media ponderada     │ 3.0  │ 4.7    │ 4.7      │
│ Coste estimado      │ 0€   │ ~0.05€ │ ~0.02€   │
└─────────────────────┴──────┴────────┴──────────┘
```
