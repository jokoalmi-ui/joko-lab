# LOOP ENGINEERING — Implementación para Joko Lab

## 1. ¿Qué es Loop Engineering en Joko Lab?

Es el paradigma de diseñar sistemas donde la IA puede:

1. **Generar** una solución
2. **Ejecutarla** o someterla a prueba
3. **Leer sus propios errores**
4. **Corregirse autónomamente**
5. **Iterar** hasta cumplir un estándar

El humano ya no escribe el prompt perfecto. El humano diseña el bucle de validación.

---

## 2. Gradiente de autonomía

Joko Lab implementa 3 niveles de Loop Engineering según el riesgo:

| Nivel | Nombre | Loop | Humano | Aplicación |
|-------|--------|------|--------|------------|
| **L1** | HITL (Human In The Loop) | Diagnóstico → Propuesta → Confirmación → Acción | Gatekeeper obligatorio | Mutaciones en stack, n8n, Docker |
| **L2** | Semi-autónomo | Generación → Ejecución en sandbox → Feedback → Iteración (N intentos) → Propuesta final | Aprueba el resultado final, no los intentos intermedios | Código, scripts, configuraciones |
| **L3** | Autónomo (puro) | Generación → Ejecución → Feedback → Iteración hasta aprobar | Solo supervisa logs | Watchdogs, tests, auto-reparación de servicios no críticos |

---

## 3. Patrón básico de Loop Engineering

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  GENERACIÓN  │────▶│  EJECUCIÓN   │────▶│  VALIDACIÓN  │
│  (subagente) │     │  (sandbox)   │     │  (métrica)   │
└─────────────┘     └──────────────┘     └──────┬───────┘
                                                │
                                          ┌─────▼─────┐
                                          │ ¿Aprobado? │
                                          └─────┬──┬───┘
                                           Sí   │  │ No
                                           ┌────┘  │
                                           ▼       │
                                     ┌─────────┐   │
                                     │ ENTREGAR │   │
                                     └─────────┘   │
                                                    │
                                          ┌─────────▼─────────┐
                                          │ CONTADOR INTENTOS │
                                          │ ¿N < max_intentos? │
                                          └─────────┬─────────┘
                                               Sí   │  No
                                               ┌────┘
                                               ▼
                                        ┌──────────────┐
                                        │ REALIMENTAR   │
                                        │ → GENERACIÓN  │
                                        └──────────────┘
```

---

## 4. Implementación concreta para Joko Lab

### 4.1. L2 — Loop de código (sandbox)

Usar `delegate_task` con instrucciones explícitas de loop:

```
Contexto:
- Genera el script Python/bash solicitado
- Ejecútalo con terminal() en /tmp/ (sandbox)
- Lee la salida y errores
- Si falla, corrige el código y vuelve a ejecutar
- Máximo 5 intentos
- En el intento 5, aunque falle, devuelve el mejor intento + errores
- Devuelve el código final y el resultado de la última ejecución
```

Ejemplo real de invocación:

```bash
hermes delegar "Crea un script que monitorice el uso de VRAM de Ollama cada 10 segundos y lo guarde en CSV" \
  --context "Sandbox: /tmp/. Usa bash o python3. Ejecútalo para verificar. Max 3 intentos." \
  --tools "terminal,file"
```

### 4.2. L1 — Loop de diagnóstico + propuesta (HITL)

El patrón existente en Joko Lab. Secuencia:

1. **Diagnóstico**: comandos de solo lectura
2. **Análisis**: el agente interpreta la salida
3. **Propuesta**: el agente ofrece solución numerada
4. **Confirmación**: el usuario aprueba (o dice "sigue")
5. **Ejecución**: el agente actúa

Este patrón ya existe en `diagnostico-stack-local`.

### 4.3. L3 — Watchdog con auto-reparación

Cron job que ejecuta un script y, si detecta anomalía, ejecuta una acción correctiva sin preguntar. Aplica SOLO a servicios no críticos.

Ejemplo: watchdog de VRAM que, si supera 95%, descarga el modelo menos usado de LM Studio.

```bash
# ~/.hermes/scripts/vram-watchdog.sh
#!/bin/bash
VRAM_PCT=$(nvidia-smi --query-gpu=utilization.memory --format=csv,noheader,nounits | head -1)
if [ "$VRAM_PCT" -gt 95 ]; then
  /home/jokoalmi/.lmstudio/bin/lms unload --all
  echo "$(date) VRAM al ${VRAM_PCT}% — modelos descargados" >> /tmp/vram-watchdog.log
fi
```

Cron job:
```bash
hermes cron create \
  --name "vram-watchdog" \
  --schedule "*/5 * * * *" \
  --script ~/.hermes/scripts/vram-watchdog.sh \
  --no-agent true
```

---

## 5. Skill de Loop Engineering (nuevo)

Propongo crear un skill `loop-engineering` con:

- **SKILL.md**: definición del paradigma y cuándo usarlo
- **references/loop-patterns.md**: catálogo de patrones de loop reutilizables
- **scripts/loop-template.sh**: plantilla para crear loops rápidamente
- **examples/**: ejemplos de invocación para L1, L2, L3

### Catálogo de patrones (borrador)

| Patrón | Nivel | Descripción |
|--------|-------|-------------|
| **code-sandbox** | L2 | Generar código → ejecutar en /tmp/ → leer errores → corregir → repetir |
| **diagnose-fix** | L1 | Diagnosticar → proponer → esperar confirmación → ejecutar |
| **watchdog-correct** | L3 | Script de monitorización → si umbral → acción correctiva |
| **audit-iterate** | L2 | Subagente A genera → Subagente B audita → Feedback a A → repetir |
| **delegate-loop** | L2 | delegate_task con instrucción explícita de iteración |

---

## 6. Ejemplo completo: L2 code-sandbox

```bash
# Paso 1: El agente recibe la petición
# Usuario: "Crea un script que convierta los exports de n8n a markdown"

# Paso 2: El agente genera el código

# Paso 3: El agente lo ejecuta en /tmp/
python3 /tmp/convert_exports.py test_input.json 2>&1

# Paso 4: El agente lee el error
# Error: KeyError: 'nodes'

# Paso 5: El agente corrige
# (iteración 2)

# Paso 6: Repite hasta aprobar o alcanzar max_intentos

# Paso 7: Devuelve el código final verificado
```

El agente nunca pregunta "¿lo ejecuto?" durante las iteraciones. Solo pregunta al final para que el usuario decida si instalar el script en producción.

---

## 7. Límites y seguridad

### Reglas obligatorias

1. **Nunca hacer loop sobre datos reales de n8n** — usar copias en /tmp/
2. **Máximo 5 intentos por defecto** — evita loops infinitos y consumo innecesario
3. **Timeout por intento: 30 segundos** — si un intento tarda más, se marca como fallo
4. **Sandbox obligatorio para L2** — todo código se ejecuta en /tmp/ o /mnt/ssd_ia_datos/tmp/
5. **No loops sobre el stack de Docker** — ni siquiera L3. Todo lo que afecte a docker-compose.yml requiere L1 (confirmación humana)
6. **Log obligatorio** — cada iteración se registra en /tmp/loop-engineering.log con timestamp, intento, error y resultado

### Formato del log

```
2026-07-14T10:00:00 | code-sandbox | int 1/5 | FAIL | KeyError: 'nodes'
2026-07-14T10:00:03 | code-sandbox | int 2/5 | FAIL | json.decoder.JSONDecodeError
2026-07-14T10:00:06 | code-sandbox | int 3/5 | PASS | Archivo generado en /tmp/output.md
2026-07-14T10:00:06 | code-sandbox | COMPLETED | 3 intentos, duración 6s
```

---

## 8. Integración con la arquitectura actual

### Relación con skills existentes

| Skill | Relación |
|-------|----------|
| `ai-architecture` | Loop Engineering es un nuevo principio arquitectónico. Esta skill lo define. |
| `diagnostico-stack-local` | El L1 (diagnose-fix) ya existe aquí. Loop Engineering lo formaliza y extiende con L2 y L3. |
| `ai-router` | No afecta. El enrutamiento sigue siendo determinista. |
| `lab-manager` | Loop Engineering añade un nuevo patrón de gobierno: diseñar bucles en lugar de prompts. |
| `hermes-expert` | No afecta. |

### Estado actual de Joko Lab frente a Loop Engineering

| Capacidad | Estado | Prioridad |
|-----------|--------|-----------|
| L1 — HITL (diagnose-fix) | ✅ Implementado en diagnostico-stack-local | Ninguna |
| L2 — code-sandbox | ⚠️ Posible con delegate_task pero no formalizado | Alta |
| L2 — audit-iterate | ⚠️ Posible pero no hay un subagente auditor dedicado | Media |
| L3 — watchdog-correct | ⚠️ Posible con cron + script, pero no implementado | Baja |
| Log de iteraciones | ❌ No existe | Media |
| Contador de intentos | ❌ No existe. Los subagentes no tienen límite explícito | Alta |

---

## 9. Próximos pasos recomendados

1. **Formalizar L2** — Crear la skill `loop-engineering` con el catálogo de patrones
2. **Implementar límite de intentos en delegate_task** — Añadir max_iterations como parámetro estándar en las instrucciones a subagentes
3. **Crear log de iteraciones** — Script que registre cada intento con timestamp y resultado
4. **Documentar ejemplos** — 3 casos de uso reales de Joko Lab usando Loop Engineering
5. **Evaluar L3** — Decidir qué servicios son candidatos a watchdog autónomo sin riesgo

---

## 10. Referencias

- Artículo original: Xataka, Junio 2026 — "El paradigma del Loop Engineering"
- Boris Cherny (Claude Code): "Mi trabajo es escribir bucles"
- Addy Osmani (Google Cloud): "El humano es el diseñador del sistema de validación"
- Implementación local: `/home/jokoalmi/hermes-lab/loop-engineering/`
