---
title: "Deuda técnica — Joko Lab"
type: operations
---

# Deuda técnica — Joko Lab

Registro de deuda técnica del laboratorio. Una entrada por TD. Formato: YAML + contexto.

---

## TD-001 — Verification Hook: falso negativo recurrente

```yaml
id: TD-001
tipo: Operativa
componente: Verification Hook (detector de verificacion de Hermes)
sintoma: >
  El detector evalúa el estado en el momento del hook, ANTES de que exista la
  evidencia persistente (log en /tmp), y no registra la verificacion posterior.
  Resultado: pide repetir la verificacion ad-hoc en cada turno siguiente aunque
  el verifier ya haya pasado con log guardado.
impacto: >
  Falsos negativos recurrentes. Ruido en el flujo de trabajo (10+ peticiones
  identicas en la sesion del 04-ago). Disminuye la confianza en el pipeline de
  validacion: una verificacion verde con evidencia persistente no se registra.
evidencia: >
  Sesion 04-ago-2026: verifier ejecutado 10 veces (todas PASS, log persistente
  en /tmp/hermes-verify-*.log en cada una) y el detector repitió la misma
  peticion en cada turno siguiente, incluso con el .py y el log en disco.
frecuencia: Recurrente (cada edicion de archivo en la sesion)
estado: Pendiente
prioridad: Media
accion_propuesta: >
  Revisar el hook de verificacion: debería (a) esperar/verificar la existencia
  de evidencia reciente (p.ej. log hermes-verify-* con timestamp posterior al
  cambio) o (b) registrar el resultado de la verificacion en un estado
  persistente que el detector consulte, en lugar de evaluar solo el momento
  del hook.
creado: 2026-08-04
```

**Contexto:** el fallo ya no es un incidente aislado: es una limitación de la
infraestructura de validación. No bloquea el trabajo (la verificacion se hace
igual y la evidencia queda en /tmp), pero degrada la confianza del pipeline y
genera ruido. No mezclar con los niveles de verificacion de los artefactos
(esos sí están verificados).
