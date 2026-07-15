# Decisión Técnica: Metodología de Cálculo para la Métrica de Autonomía de Joko Lab

**Fecha**: 2026-07-13
**Estado**: Propuesta
**Área**: Metodología y Auditoría

## Contexto
La métrica de "Autonomía" (establecida en la decisión del 2026-07-10) se concibió para responder a la pregunta: *"¿Cuánto podría mantener otra persona o una IA limpia la infraestructura utilizando únicamente la documentación existente sin intervención del creador?"*. 
Sin embargo, en la auditoría ejecutiva del 2026-07-13, el valor global de **48%** se basó en una media simple de estimaciones heurísticas individuales por dimensión (60%, 70%, 50%, 40%, 20%), careciendo de indicadores reproducibles y objetivos.

## Problema
- **Subjetividad:** La asignación manual de porcentajes reintroduce el sesgo de auto-evaluación optimista.
- **Riesgos de Seguridad:** El borrador original de la rúbrica incluía "reinicios de servicios" dentro de las tareas desasistidas (*SAFE*), violando la regla constitucional de Joko Lab de no mutar el sistema de forma asíncrona o desasistida.
- **Ausencia de Verificación:** No existía ningún enlace programático entre la documentación declarada y el estado real del sistema.

## Decisión
1. **Rúbrica Estricta de 5 Dimensiones:** Cada dimensión constará de 4 ítems de igual peso (25% cada uno).
2. **Clasificación del Tipo de Check:** Cada indicador se marcará de forma explícita como:
   - **[M] (Manual/Auditado):** Verificado cualitativamente por el agente.
   - **[A] (Automatizado/Programático):** Validado por un script de solo lectura sin intervención humana.
3. **Frontera de Seguridad Absoluta en Dimensión 4 (Operación):** El perfil de automatización asíncrona (*SAFE*) se limitará **exclusivamente** a tareas de solo lectura (diagnóstico, logs, exportaciones de configuración y backups). Cualquier acción mutadora (reiniciar, recrear, apagar o modificar servicios) es estrictamente **PRIVILEGED** y queda excluida del cálculo de la autonomía asíncrona desasistida.
4. **Validación de Bindeo y Puertos Opcionales:** El script de validación inicial comprobará la seguridad del bindeo de los sockets reales (`127.0.0.1` o `[::1]` frente a `0.0.0.0` o `*`) utilizando la salida de `ss -tln` para mitigar riesgos de exposición externa, y tratará puertos dinámicos como LM Studio (1234) como opcionales para no generar falsos negativos.

## Rúbrica de Autonomía de Joko Lab (Modificada)

### Dimensión 1: Gobierno (Máximo 100%)
- **[M] (25%)** La constitución (`HERMES.md`) está actualizada, sin contradicciones ni deuda de gobernanza.
- **[M] (25%)** Registro de decisiones de arquitectura (`docs/decisiones/`) documenta cada cambio de estado mayor.
- **[M] (25%)** `ROADMAP.md` activo con hitos claros, realistas y secuenciales.
- **[A] (25%)** El formato de los archivos del registro de decisiones cumple la convención `AAAA-MM-DD-tema.md` y contiene la estructura reglamentaria.

### Dimensión 2: Conocimiento (Máximo 100%)
- **[A] (25%)** Los puertos expuestos reales coinciden al 100% con los declarados en `docs/arquitectura.md` y están bindeados de forma segura a localhost.
- **[M] (25%)** Existe un plano actualizado de arquitectura física y de contenedores en `docs/arquitectura.md`.
- **[M] (25%)** La documentación técnica detalla el flujo de datos completo y las dependencias entre servicios.
- **[M] (25%)** Existe un manual de recuperación ante desastres que permite reconstruir el entorno desde cero solo con los backups y los documentos.

### Dimensión 3: Inteligencia Artificial (Máximo 100%)
- **[M] (25%)** Las directivas operativas de los modelos (Directores y Especialistas) están formalizadas en sus respectivas skills de gobierno.
- **[M] (25%)** El sistema cuenta con mecanismos de control de consumo de tokens y costes.
- **[M] (25%)** Se dispone de logs de enrutamiento y auditoría de llamadas de IA en `decision.log` (JSON por línea, `/mnt/ssd_ia_datos/lab-state/logs/decision.log`). Se evaluó crear ledger agregado (`decision-ledger.json`) y se descartó 2026-07-15.
- **[M] (25%)** El sistema puede alternar entre proveedores locales y en la nube (fallback) de forma transparente ante caídas del servicio principal.

### Dimensión 4: Operación (Máximo 100% - Enfoque de Solo Lectura)
- **[M] (25%)** El agente dispone de perfiles y scripts no interactivos (*SAFE*) que ejecutan lecturas de telemetría y diagnósticos sin approvals.
- **[M] (25%)** Las tareas de exportación de datos de n8n y copias de seguridad de volumen de solo lectura están totalmente configuradas y automatizadas.
- **[A] (25%)** Existe telemetría local de hardware (CPU, VRAM, temperatura GPU) accesible de forma automatizada por el agente (verificable de forma programática mediante ping al monitor local).
- **[M] (25%)** El sistema de rotación y verificación de integridad de copias de seguridad (lectura de hashes) funciona de forma autónoma.

### Dimensión 5: Certificación (Máximo 100%)
- **[M] (25%)** Existe una suite de pruebas automatizadas que verifica el comportamiento correcto de las herramientas principales (`docker compose`, conexiones de red).
- **[M] (25%)** Cada skill del laboratorio cuenta con al menos un caso de validación en `certification/` para verificar su funcionamiento operativo.
- **[M] (25%)** Existe un script de humo (`smoke-test.sh` o equivalente) que valida el correcto levantamiento del laboratorio tras un reinicio del host.
- **[M] (25%)** El agente puede ejecutar la validación completa del sistema de forma desasistida y reportar discrepancias.

## Motivos
- Garantiza que la "Autonomía" sea un indicador científico basado en hechos y no en valoraciones optimistas del agente.
- Mantiene la consistencia con las reglas críticas de seguridad de la constitución.
- Permite la transición gradual de la auditoría manual a la auditoría programática autónoma.

## Consecuencias
- La métrica de autonomía en las próximas auditorías reflejará exactamente la fracción de casillas validadas que sume la rúbrica.
- Se desarrolla el primer script de validación automatizada enfocado únicamente en la correspondencia y bindeo seguro de puertos declarados en `docs/arquitectura.md`.
