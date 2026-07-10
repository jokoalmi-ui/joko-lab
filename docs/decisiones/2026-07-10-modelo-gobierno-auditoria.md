# Decisión Técnica: Transición a Sistema de Gobierno Técnico y Madurez

**Fecha**: 2026-07-10
**Estado**: Aceptada
**Área**: Metodología y Auditoría

## Contexto
La evaluación de las auditorías ejecutivas recientes ha revelado un sesgo optimista. El sistema puntuaba el *esfuerzo* y el *volumen* de trabajo (llegando a 8.8/10) en lugar de evaluar la *resiliencia* y la *madurez* real de la infraestructura. Joko Lab ha pasado de ser una colección de scripts a un sistema complejo que requiere un modelo de gobierno explícito.

## Problema
- Las métricas actuales no reflejan la autonomía del sistema frente al conocimiento implícito del propietario (factor memoria).
- Puntuar casi un 9/10 transmite la falsa sensación de que el laboratorio está terminado, bloqueando el margen psicológico y real para el crecimiento.
- Se carece de una dimensión que mida el "Gobierno" (roadmap, decisiones, políticas).

## Decisión
1. **Reestructurar el concepto del laboratorio** en 5 dominios principales:
   - **Gobierno:** `HERMES.md`, decisiones, lab-manager, roadmap.
   - **Operación:** Skills tácticas (docker-admin, n8n-admin).
   - **Conocimiento:** Documentación y arquitectura (`docs/`).
   - **Certificación:** Pruebas de validación y comprensión.
   - **IA:** Orquestación, `ai-router` y arquitectura híbrida.
2. **Añadir la métrica de Autonomía:** "¿Cuánto podría mantener otra persona/IA usando solo la documentación?"
3. **Incluir un Riesgo Principal** en cada auditoría, en lugar de listas de tareas menores.
4. **Calibrar la puntuación** a "grado de madurez", bajando las notas actuales drásticamente para reflejar el camino que falta por recorrer.

## Motivos
- Rompe el sesgo de autocomplacencia.
- Transforma la mejora continua en un elemento cuantificable (de dependencia humana a autonomía documental).
- Evita que skills vacías se borren por "limpieza estética" si aún justifican un rol en la arquitectura.

## Consecuencias
- La próxima auditoría ejecutiva tendrá una nota global previsiblemente mucho más baja (rango 6-7), reflejando la realidad de un sistema en maduración.
- La plantilla `audit-executive-format.md` se actualiza para exigir estas nuevas dimensiones de forma estandarizada.

## Referencias
- `HERMES.md` (Principio: "Aumentar el conocimiento del sistema" y "Mejorar la capacidad de operar autónomamente").