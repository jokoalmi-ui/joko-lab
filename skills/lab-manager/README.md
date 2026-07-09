# lab-manager — Director de proyecto de Joko Lab

## ¿Qué es?

lab-manager es la skill que **gestiona el laboratorio en sí mismo**. No sabe de Docker, n8n ni IA. Sabe qué skills existen, qué documentación hay, qué decisiones se tomaron, qué está pendiente y qué debería hacerse ahora.

## ¿Para qué sirve?

Cuando no sepas por dónde seguir, pregúntale a lab-manager:

- "¿Qué está pendiente?"
- "¿Qué ha cambiado esta semana?"
- "¿Qué skills están maduras?"
- "¿Qué documentación está desactualizada?"
- "¿Qué decisiones de arquitectura tomamos?"
- "¿Qué deberíamos hacer ahora?"

## ¿Cómo se relaciona con las demás skills?

lab-manager **no sustituye** a las skills especializadas. Las consulta y coordina:

- **docker-admin** → para estado de Docker
- **n8n-admin** → para estado de n8n
- **ai-router** → para estado de modelos de IA
- **hermes-expert** → para estado de Hermes
- Las skills vacías (betterbird, perfumes, evolution) → monitoriza si progresan

## Filosofía

- **No toca nada.** Solo lee, analiza, prioriza y recomienda.
- **No duplica.** Si otra skill ya tiene la información, la referencia.
- **Proactivo.** Detecta incoherencias y documentación obsoleta antes de que sea un problema.
