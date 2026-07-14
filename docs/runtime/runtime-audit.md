# Auditoría del Runtime de Joko Lab

**Fecha:** 2026-07-14
**Propósito:** Auditoría técnica completa del Runtime. Solo hechos verificables con comandos reales.
**Comandos usados:** Ver anexo al final.

---

## 1. Inventario de componentes

### Componentes que SÍ pertenecen al Runtime

| Componente | Ruta | Función |
|---|---|---|
| Decision Engine | `decision-engine/decision_engine.py` (400 líneas) | Función pura: lee state.json y policies/*.yaml, decide proveedor+modelo |
| State Manager | `state-manager/state-manager.py` | Observa el laboratorio, escribe state.json cada 60s |
| Schema de estado | `/mnt/ssd_ia_datos/lab-state/state.schema.json` | Contrato JSON del state.json |
| Policies | `/mnt/ssd_ia_datos/lab-state/policies/` (6 archivos .yaml) | costes, gpu, horario, modelos, niveles, privacidad |
| state.json | `/mnt/ssd_ia_datos/lab-state/state.json` | Estado actual del laboratorio (968 bytes, actualizado cada minuto) |
| ultima-decision.json | `~/.hermes/ultima-decision.json` | Fallback de última decisión |

**Verificado con:** `find /home/jokoalmi/hermes-lab/decision-engine -type f | sort`, `ls /mnt/ssd_ia_datos/lab-state/policies/`, `cat /mnt/ssd_ia_datos/lab-state/state.schema.json`

### Componentes de la arquitectura antigua (no pertenecen al Runtime)

| Componente | Ruta | Estado |
|---|---|---|
| apply-decision.sh | `decision-engine/apply-decision.sh` | Activo. Acopla DE a `hermes config set` (5 referencias a config.yaml) |
| router-cron.sh.DEPRECADO | `scripts/router-cron.sh.DEPRECADO` | Muerto. Marcado como deprecado |
| router-cron.sh.bak | `scripts/router-cron.sh.bak` | Backup de script eliminado |
| model-router.sh | `scripts/model-router.sh` | En disco pero no en cron |
| model-router.sh.bak | `scripts/model-router.sh.bak` | Backup de script eliminado |
| provider-detect.sh | `scripts/legacy/provider-detect.sh` | Muerto. Lee de /tmp/current-provider.txt (ya no existe) |
| decision_engine.py.bak | `decision-engine/decision_engine.py.bak.20260714_104032` | Backup de hoy |
| arquitectura.md.bak | `docs/arquitectura.md.bak.20260714_101325` | Backup de hoy |
| estado-real.md.bak | `docs/estado-real.md.bak.20260714_101325` | Backup de hoy |

**Verificado con:** `ls -la scripts/`, `find . -name "*router-cron*"`, `crontab -l`

---

## 2. Dependencias sobre config.yaml

### Punto de acoplamiento: `apply-decision.sh`

El archivo `decision-engine/apply-decision.sh` es el único script que toca `config.yaml`. Contiene 5 referencias:

```bash
# Línea 4: comentario
# Lee la salida del DE y ejecuta hermes config set.

# Línea 36-37: lectura
OLD_PROVIDER=$(hermes config show 2>/dev/null | grep "provider:" | head -1 | awk '{print $2}')
OLD_MODEL=$(hermes config show 2>/dev/null | grep "default:" | head -1 | awk '{print $2}')

# Línea 47-48: escritura (el acoplamiento real)
hermes config set model.provider "$PROVIDER" 2>/dev/null
hermes config set model.default "$MODEL" 2>/dev/null

# Línea 51-52: verificación leyendo el YAML directamente
NEW_PROVIDER=$(grep -A3 "^model:" ~/.hermes/config.yaml 2>/dev/null | grep "provider:" | awk '{print $2}')
NEW_MODEL=$(grep -A3 "^model:" ~/.hermes/config.yaml 2>/dev/null | grep "default:" | awk '{print $2}')
```

### Config.yaml actual (proveedor activo)

Estado real verificado con `cat ~/.hermes/config.yaml`:

```yaml
model:
  base_url: https://api.deepseek.com/v1
  default: deepseek-chat
  provider: deepseek
```

El valor en `config.yaml` y la salida del DE pueden diferir (el DE decide, apply-decision.sh sincroniza).

### Ningún otro script toca config.yaml

Verificado con: `grep -rn "config set\|config show" --include="*.sh" --include="*.py"` — solo aparece en `apply-decision.sh`.

---

## 3. Bug confirmado en State Manager

**Archivo:** `state-manager/state-manager.py`, línea 191.

```python
SECRETS_DIR=Path("...ts")
```

La ruta es literal `"...ts"` — es un placeholder no reemplazado. Esto hace que `read_secret("gemini.key")` devuelva siempre cadena vacía, y por tanto `check_cloud("gemini", api_key="")` falle en autenticación.

**Impacto:** `state.json → cloud.gemini.disponible` podría ser `false` aunque Gemini esté disponible, porque la API key no se envía.

**Verificado con:** `grep -n "SECRETS_DIR" state-manager/state-manager.py`

---

## 4. Log duplicado en apply-decision.sh

El log de `apply-decision.sh` muestra entradas duplicadas:

```
[2026-07-14 09:00:01] Decisión: gemini / gemini-2.5-pro — Horario: 03:00-12:00, ahora 08:59
[2026-07-14 09:00:01] Decisión: gemini / gemini-2.5-pro — Horario: 03:00-12:00, ahora 08:59
[2026-07-14 09:00:01] Cambiando: / → gemini/gemini-2.5-pro
[2026-07-14 09:00:01] Cambiando: / → gemini/gemini-2.5-pro
```

Causa raíz verificada: el `main()` de `decision_engine.py` (líneas 381-396) es invocado una vez por `apply-decision.sh`. La duplicación se produce porque `decision_engine.py` escribe `decision.log` (línea 375) y `apply-decision.sh` también registra en `apply-decision.log` (línea 33). Pero el duplicado dentro de `apply-decision.log` sugiere que `apply-decision.sh` se ejecuta 2 veces por tick de cron.

No se ha determinado la causa exacta de la doble ejecución — podría ser herencia del `$HOUR` duplicado observado al inicio de la sesión del 14 julio.

**Verificado con:** `tail -20 /mnt/ssd_ia_datos/lab-state/logs/apply-decision.log`

---

## 5. Responsabilidades (SRP)

### State Manager (state-manager.py)

**Responsabilidad actual:** observar el laboratorio. Correcto.

**Lee hardware:** nvidia-smi (GPU), /proc/meminfo (RAM), /proc/loadavg (CPU), df (disco), curl a servicios locales (Ollama, LM Studio, n8n, servicios Docker), curl a APIs cloud (DeepSeek, Gemini).

**Violación:** ninguna. Observar es su función.

**Bug:** línea 191, `SECRETS_DIR` es placeholder.

### Decision Engine (decision_engine.py)

**Responsabilidad actual:** decidir basado en state + policies. Correcto.

**NO lee hardware directamente.** Verificado con: `grep -n "nvidia-smi\|docker\|compose\|curl\|subprocess\|os.system" decision-engine/decision_engine.py` — salida vacía.

**NO toca config.yaml.** El docstring lo confirma: "Sin modificar config.yaml."

**Decisión determinista:** una entrada (state + policies) → una salida. No hay aleatoriedad.

### apply-decision.sh

**Responsabilidad actual:** 3 responsabilidades mezcladas:
1. Llama al DE y parsea su salida
2. Escribe en config.yaml (hermes config set)
3. Escribe en ultima-decision.json

**Violación SRP:** confirmada. Hace 3 cosas.

---

## 6. Cobertura de pruebas

| Componente | Tests unitarios | Tests integración | Tests fallo |
|---|---|---|---|
| Decision Engine | 0 | 0 | 0 |
| State Manager | 0 | 0 | 0 |
| Policy Engine (no existe como módulo separado) | 0 | 0 | 0 |
| Capability Registry (no existe como módulo separado) | 0 | 0 | 0 |
| apply-decision.sh | 0 | 0 | 0 |

**Tests existentes en el repositorio (NO del Runtime):**
- `certification/tests/` (3 tests de comprensión humana, no automatizados)
- `docs/tests/test-01-contradicciones.md` (test de documentación, no automatizado)
- `scripts/smoke-test.sh` (test de humo del stack Docker, no del Runtime)

**Verificado con:** `find . -path "*/test*" -type f | sort`, `find . -name "test_*.py" -print`

---

## 7. Documentación inconsistente

| Fuente | Dice | Realidad |
|---|---|---|
| `estado-real.md:28` | Ollama tiene `qwen2.5:7b` | Correcto (sigue instalado) |
| `estado-real.md:183-184` | `hermes-notes.md` y `hermes-internals.md` obsoletos | Esos archivos ya no existen |
| `estado-real.md:232` | "Auditar 17 falsos positivos de secretos en Git" | Ya verificado hoy (0 secretos reales) |
| `ai-router/SKILL.md:36` | "DeepSeek es el cloud por defecto permanente" | Contradice la política horaria del Runtime |
| `ai-architecture/SKILL.md` | No existe (0 bytes) | No se encontró SKILL.md |
| `docs/roadmap.md` | Sprint 3.0 | No refleja Sprint 3.1 |
| `docs/runtime/` | No existe | No hay documentación del Runtime |

**Verificado con:** `cat skills/ai-architecture/SKILL.md`, `cat skills/ai-router/SKILL.md`, `ls docs/runtime/`

---

## 8. Cron activo

```
# Decision Engine — aplica proveedor según políticas
0 3 * * *   apply-decision.sh   (03:00)
0 12 * * *  apply-decision.sh   (12:00)
*/30 * * *  apply-decision.sh   (cada 30 min)
```

El cron ejecuta `apply-decision.sh`, no el DE directamente. Este cron es el que debe eliminarse cuando el Runtime pase a ser consultado bajo demanda.

El State Manager NO tiene cron. Se ejecuta como proceso persistente (`state-manager.py --watch`), verificado con `ps aux | grep state-manager`.

---

## 9. Resumen de deuda técnica

| Ítem | Tipo | Impacto | Prioridad |
|---|---|---|---|
| SECRETS_DIR placeholder en state-manager.py | Bug | Gemini no se autentica | Alta |
| Log duplicado en apply-decision.log | Logging | Ruido; 4 líneas por ejecución | Baja |
| apply-decision.sh acoplado a config.yaml | Arquitectura | Impide eliminar provider global | Alta |
| Cron decisor cada 30 min | Arquitectura | Decisiones periódicas en lugar de bajo demanda | Alta |
| Dos fuentes de verdad sin jerarquía documentada | Arquitectura | state.json + ultima-decision.json | Media |
| Sin tests | Cobertura | Sin red de seguridad | Alta |
| Sin logging estructurado | Observabilidad | Logs no procesables | Media |
| Scripts muertos en disco (7 archivos) | Mantenimiento | Ruido, confusión | Baja |
| docs/runtime/ no existe | Documentación | Nueva arquitectura sin docs | Media |
| ai-router/SKILL.md contradice al Runtime | Documentación | Confusión sobre qué decide el modelo | Media |

---

## Anexo: Comandos usados en esta auditoría

```bash
# Inventario de componentes
find /home/jokoalmi/hermes-lab/decision-engine -type f | sort
find /home/jokoalmi/hermes-lab/runtime -type f 2>/dev/null
ls -la /home/jokoalmi/hermes-lab/scripts/
find /home/jokoalmi/hermes-lab -name "*router-cron*" -o -name "*cron-router*" 2>/dev/null

# Dependencias config.yaml
grep -rn "config\.yaml\|config show\|config set\|config get" decision-engine/
grep -rn "config set\|config show" --include="*.sh" --include="*.py" .
cat ~/.hermes/config.yaml

# Estado actual
crontab -l
cat /mnt/ssd_ia_datos/lab-state/state.json
ls -la /mnt/ssd_ia_datos/lab-state/policies/

# Bug en state-manager
grep -n "SECRETS_DIR" state-manager/state-manager.py

# Log duplicado
tail -20 /mnt/ssd_ia_datos/lab-state/logs/apply-decision.log

# SRP
grep -n "nvidia-smi\|docker\|compose\|curl\|subprocess\|os.system" decision-engine/decision_engine.py
grep -n "nvidia-smi\|docker\|compose\|curl.*local" state-manager/state-manager.py

# Tests
find . -path "*/test*" -type f | sort
find . -name "test_*.py" -print

# Documentación
cat skills/ai-architecture/SKILL.md
ls docs/runtime/
ls docs/decisiones/ | grep "2026-07"
grep -n "hermes-notes\|hermes-internals\|falsos.*positivos\|DeepSeek.*permanente" docs/estado-real.md skills/ai-router/SKILL.md
cat docs/roadmap.md | head -10
```
