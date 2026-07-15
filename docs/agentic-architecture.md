# Arquitectura Agéntica de Joko Lab v3.0: Plano Maestro

## 1. Introducción y Visión de la Plataforma

Joko Lab v3.0 evoluciona de ser una colección estructurada de habilidades y servicios independientes a convertirse en una **plataforma multiagente gobernada por políticas**. 

En este nuevo paradigma, los modelos de Inteligencia Artificial (tanto en la nube como locales) dejan de ser el centro del sistema y se transforman en **recursos intercambiables y especializados** bajo la supervisión de un marco de gobernanza superior y transversal.

### Principios Fundacionales de la v3.0:
1. **Desacoplo de Políticas y Modelos:** Las reglas de seguridad, asincronía y uso de recursos no se delegan en el razonamiento del modelo; se arbitran a nivel de plataforma.
2. **Resiliencia Autónoma:** El sistema es capaz de degradar su capacidad ante fallos (caída de Internet, caída de proveedores) de forma automática sin bloquear la operatividad del laboratorio.
3. **Gestión Física de Recursos:** Se monitoriza e interviene el hardware local (VRAM de la GPU RTX A2000) para garantizar la estabilidad del sistema bajo carga.
4. **Gobierno Basado en Evidencia:** Cada decisión tomada por la plataforma se registra, cuantifica y audita basándose en datos empíricos, eliminando la intuición del análisis de rendimiento.

---

## 2. Mapa de Capas de Joko Lab v3.0

```
┌────────────────────────────────────────────────────────────────────────┐
│                          CAPA 0: CONSTITUCIÓN                          │
│                               HERMES.md                                │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        CAPA 1: GOBIERNO (POLICY)                       │
│                             Policy Engine                              │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        CAPA 2: ORQUESTACIÓN (IA)                       │
│    Semantic Router  ·  GPU Scheduler  ·  Director Cognitivo (Cloud)    │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        CAPA 3: EJECUCIÓN (LOCAL)                       │
│               Especialista Local (Ollama)  ·  VLM (LM Studio)          │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                           CAPA 4: INFRAESTRUCTURA                      │
│                  Docker  ·  n8n  ·  Git  ·  Filesystem                 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Policy Engine (Motor de Políticas de Seguridad)

El *Policy Engine* es el árbitro lógico transversal de la plataforma. Su función es evaluar si una acción propuesta por cualquier agente o tarea automatizada está permitida antes de invocar herramientas o delegar subtareas.

### 3.1 Perfiles de Ejecución: SAFE vs PRIVILEGED

Para solucionar el bloqueo provocado por la directiva `approvals.mode: manual` durante tareas nocturnas asíncronas, se introduce la segmentación estricta de acciones por riesgo:

```
                            Acción Propuesta
                                   │
                                   ▼
                     ¿La acción altera el sistema?
                                   │
                    ┌──────────────┴──────────────┐
                    ├── No                        ├── Sí
                    ▼                             ▼
              Perfil SAFE                  Perfil PRIVILEGED
        (Lectura, Logs, Estado)      (Escritura, Borrado, Docker)
                    │                             │
                    ├──────────────┐              │
                    ▼              ▼              │
             ¿Sesión Interactiva?                 │
             ┌──────┴──────┐                      │
             ├── Sí        ├── No                 │
             ▼             ▼                      ▼
         Ejecutar      Ejecutar             ¿Usuario Presente?
         con aviso    silencioso            ┌─────┴─────┐
                                            ├── Sí      ├── No
                                            ▼           ▼
                                        Confirmación  BLOQUEAR Y
                                           manual     REGISTRAR
```

#### Perfil SAFE (No interactivo, de bajo riesgo)
* **Acciones permitidas:** Listar archivos, leer logs, comprobar estado de puertos, healthchecks de Docker, backups de solo lectura/copia, consultas de API.
* **Política de ejecución:** Puede ejecutarse en segundo plano sin intervención humana. Permite la asincronía total de backups nocturnos y tareas de mantenimiento programadas.

#### Perfil PRIVILEGED (Interactivos, de alto riesgo)
* **Acciones restringidas:** Borrado de archivos (`rm`), movimiento o edición de ficheros (`mv`, `patch`, `write_file`), parada/arranque/recreación de contenedores Docker, reescritura de configuraciones base, modificación de bases de datos.
* **Política de ejecución:** Requiere de forma obligatoria la presencia del usuario y la confirmación explícita mediante la interfaz interactiva. Si ocurre en segundo plano de forma asíncrona, la tarea se **bloquea inmediatamente**, se registra la denegación en el *Decision Ledger* y se notifica al usuario en la apertura de la siguiente sesión.

---

## 4. Semantic Router (Enrutamiento Dinámico)

El *Semantic Router* sustituye la rigidez del cron horario por un árbol de decisión dinámico y adaptativo en tiempo real basado en el contexto de la petición, el coste, el consumo histórico y la salud del sistema.

### 4.1 Árbol de Decisión del Router Semántico

```
                            Prompt del Usuario
                                    │
                                    ▼
                         ¿Contiene datos privados?
                                    │
                     ┌──────────────┴──────────────┐
                     ├── Sí                        ├── No
                     ▼                             ▼
              Especialista Local             ¿Requiere imágenes/PDF?
                                                   │
                                    ┌──────────────┴──────────────┐
                                    ├── Sí                        ├── No
                                    ▼                             ▼
                             ¿LM Studio VLM?               ¿Es mecánico/repetitivo?
                                    │                             │
                      ┌─────────────┴──────┐        ┌─────────────┴─────┐
                      ├── Disponible       ├── No   ├── Sí              ├── No
                      ▼                    ▼        ▼                   ▼
                  VLM Local             Gemini   Especialista    ¿Es complejo/razonamiento?
                                                 Local (Ollama)         │
                                                                 ┌──────┴──────┐
                                                                 ├── Sí        ├── No
                                                                 ▼             ▼
                                                             ¿Hora 03-12?   Mistral
                                                                 │           Nemo
                                                           ┌─────┴─────┐
                                                           ├── Sí      ├── No
                                                           ▼           ▼
                                                        Gemini     DeepSeek
```

### 4.2 Criterios Dinámicos de Decisión

1. **Datos Privados:** Si se detecta información confidencial, claves o propiedad industrial, se enruta de forma mandatoria al **Especialista Local** (offline 24/7).
2. **Coste y Franja Horaria:** El router evalúa la hora de España. Si se requiere un modelo en la nube y la hora está en la franja cara (03:00 - 12:00 CEST), prioriza **Gemini-3.5-flash** sobre DeepSeek para ahorrar tokens.
3. **Disponibilidad (Healthcheck Activo):** Antes de enrutar a una API en la nube, el router comprueba si hay conexión a Internet. Si se detecta desconexión total o caída del proveedor, el router activa automáticamente el **Director de Emergencia Local** (Mistral Nemo en Ollama) de forma degradada.

---

## 5. GPU Scheduler (Gestor de VRAM)

El hardware de Joko Lab cuenta con una GPU NVIDIA RTX A2000 de 12 GB de VRAM. Cargar múltiples modelos masivos simultáneamente degrada el sistema por swapping o cuelga el stack por Out-Of-Memory (OOM). El *GPU Scheduler* arbitra el ciclo de vida de los modelos locales.

### 5.1 Reglas del Scheduler de VRAM

*   **Capacidad Máxima de VRAM:** 12,288 MB.
*   **Margen de Seguridad de Pantalla/Sistema:** 1,000 MB (siempre libres para el host y el entorno gráfico).
*   **VRAM Disponible para Modelos:** 11,288 MB.

```
                              Petición de Carga
                               (Ej: Gemma-4 12B)
                                      │
                                      ▼
                      ¿VRAM Libre + Inactiva >= Gemma VRAM?
                                      │
                       ┌──────────────┴──────────────┐
                       ├── Sí                        ├── No
                       ▼                             ▼
           ¿VRAM Libre >= Gemma VRAM?          Rechazar carga /
                       │                       Escalar a Cloud
         ┌─────────────┴─────────────┐
         ├── Sí                      ├── No
         ▼                           ▼
    Cargar modelo              Descargar modelo
                               inactivo e intentar
```

### 5.2 Estrategia de Descarga por Inactividad (Prune en Caliente)

Antes de invocar un modelo local vía Ollama o LM Studio, el *GPU Scheduler* interviene:
1. Comprueba el estado de memoria vía `nvidia-smi`.
2. Si un modelo inactivo (ej. un VLM en LM Studio de una tarea visual pasada) sigue ocupando 5 GB de VRAM y el Especialista Local necesita cargar Mistral Nemo (que requiere ~11 GB VRAM), el Scheduler llama a la API de LM Studio para **descargar en caliente** el VLM antes de permitir que Ollama levante Mistral Nemo.
3. Si los recursos locales están al límite y no es seguro descargar modelos activos, el Scheduler **deniega el uso local** y escala la subtarea al Director Cloud de forma transparente.

---

## 6. Decision Ledger (Observabilidad de IA)

Para transformar la intuición del rendimiento en métricas empíricas de ingeniería, cada interacción y enrutamiento se registra en `decision.log` (JSON por línea en `/mnt/ssd_ia_datos/lab-state/logs/decision.log`). Se evaluó crear un ledger agregado (`decision-ledger.json`) el 2026-07-15 y se descartó por no tener consumidor real — `decision.log` ya cubre la necesidad.

### 6.1 Esquema del Ledger (Estructura JSON de la decisión)

```json
{
  "timestamp": "2026-07-13T08:46:12Z",
  "prompt_id": "tx-8921a-90",
  "routing": {
    "semantic_route": "cloud_planning",
    "model_assigned": "gemini-3.5-flash",
    "provider": "google",
    "reason": "Franja horaria 03-12 CEST, optimización de coste activa"
  },
  "metrics": {
    "latency_seconds": 1.45,
    "input_tokens": 1204,
    "output_tokens": 305,
    "cost_estimated_usd": 0.0001815
  },
  "hardware": {
    "vram_allocated_mb": 0,
    "gpu_temp_celsius": 48
  },
  "status": {
    "success": true,
    "fallback_used": false,
    "error_message": ""
  }
}
```

### 6.2 Utilidad del Ledger

*   **Auditoría de Costes:** Genera un análisis exacto del gasto mensual del laboratorio por proveedor.
*   **Análisis de Deuda:** Muestra el porcentaje de veces que el sistema tuvo que recurrir al fallback de emergencia local por caídas de Internet o caídas de APIs.
*   **Optimización del Hardware:** Permite relacionar la latencia de respuesta del Especialista Local con la temperatura y el uso de VRAM de la GPU RTX A2000.

---

## 7. Plan de Transición Gradual (El Camino a la v3.0)

La implementación de este plano maestro no se realizará mediante un rediseño de golpe, sino mediante iteraciones controladas y validadas por el ciclo de madurez de Joko Lab:

### Fase 1: Consolidación Documental y Criterios (Hoy)
- [x] Crear el borrador del plano maestro (`docs/agentic-architecture.md`).
- [x] Sincronizar las fichas técnicas y eliminar duplicidades dispersas en las skills.
- [x] Integrar la checklist `ROUTER_AUDIT.md` para verificación rápida.

### Fase 2: Implementación de la Observabilidad y Fronteras (Próximos días)
- [x] Implementar el **Decision Ledger** — evaluado y DESCARTADO el 2026-07-15. `decision.log` (JSON por línea) cubre la necesidad. Sin dashboard ni consumidor real que justifique el ledger agregado.
- [ ] Desarrollar los perfiles de asincronía **SAFE vs PRIVILEGED** dentro del código de automatización para evitar congelamientos nocturnos de n8n y de copias de seguridad.

### Fase 3: Automatización del GPU Scheduler
- [ ] Escribir el script de gobernanza de hardware que consulte `nvidia-smi` y las APIs de descarga de Ollama/LM Studio antes de levantar modelos pesados.

### Fase 4: Despliegue del Semantic Router
- [ ] Sustituir la lógica de `router-cron.sh` por la llamada en caliente al enrutador dinámico basado en tipo de tarea, coste de API y disponibilidad de Internet.
