---
title: "Diagnóstico — GPU colgada tras suspend/resume (23-ago-2026)"
type: research
---

# Diagnóstico — GPU colgada tras suspend/resume (23-ago-2026)
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 23-08-2026 · **Estado:** documentado, SIN solución aplicada (a la espera de actualización de Ubuntu/NVIDIA)
**PC:** Ubuntu 26.04 LTS · driver NVIDIA 595.84 · RTX A2000 12 GB

## Síntoma

- Tras suspender el PC (22-ago 22:58) y despertarlo (23-ago 07:02), `nvidia-smi` NO responde (timeout).
- 3 procesos `nvidia-smi` zombie colgados (13 min, 2:53, 39 s) → load average 7,16.
- ComfyUI y LM Studio llaman a `nvidia-smi` al arrancar → se quedan esperando para siempre (parecía fallo de ComfyUI, pero era la GPU).
- Solución de emergencia: reinicio del PC (arranque limpio → GPU responde).

## Evidencia (salida real)

```
=== Servicios NVIDIA ===
nvidia-suspend.service   enabled ✅
nvidia-resume.service    enabled ✅
nvidia-hibernate.service enabled ✅

=== Parámetro módulo ===
PreserveVideoMemoryAllocations: 1   ← fix clásico YA aplicado

=== Modo de suspensión ===
s2idle [deep]                        ← S3 deep, correcto

=== Secuencia del fallo ===
22:58:56  nvidia-suspend.service: Finished        ← suspend OK
22:58:57  kernel: PM: suspend entry (deep)
07:02:51  kernel: PM: Waking up from S3           ← 8h después
07:02:51  kernel: PM: suspend exit
07:02:53  nvidia-resume.service: Finished         ← "OK" aparente
07:35     nvidia-smi → COLGADO (timeout, 3 zombies)
```

## Diagnóstico

1. **El suspend fue correcto** (S3 deep, servicios NVIDIA OK).
2. **Los servicios NVIDIA hicieron su trabajo** (suspend/resume Finished).
3. **El fix clásico NO evitó el fallo** (`PreserveVideoMemoryAllocations: 1` + servicios enabled — aún así colgó).
4. **El driver vuelve pero la GPU queda inutilizable**: módulo `nvidia` cargado en lsmod, `/dev/nvidia*` presentes, pero cualquier llamada a nvidia-smi/CUDA se cuelga para siempre.

**Conclusión**: bug conocido de NVIDIA en Ubuntu 26.04 + driver 595 (mismo hilo que Quadro RTX 4000 — misma familia profesional que la A2000). El resume "funciona" a nivel kernel (S3 exit) pero el driver no recupera el control completo de la GPU. **No es un problema de configuración del lab.**

## No siempre falla

- Este episodio falló; otros suspend/resume previos funcionaron (no es determinista).
- Hipótesis: falla intermitente relacionada con el tiempo en suspend (8h) o estado de VRAM al suspender (modelos cargados).

## Soluciones evaluadas (NO aplicadas — pendiente de actualización)

| Opción | Impacto | Estado |
|---|---|---|
| Deshabilitar suspend (`mask sleep.target suspend.target...`) | Elimina el problema de raíz | NO aplicado (esperar fix Ubuntu) |
| Script GNOME/Wayland (joncorv) | Mantiene suspend, intenta arreglar | NO aplicado (script 3º) |
| nvhelper | Laptops híbridas — NO aplica (sobremesa) | Descartado |
| Esperar fix de NVIDIA/Ubuntu | — | **ACCIÓN ELEGIDA** |

## Notas para el futuro

- Si reaparece tras una actualización de Ubuntu/NVIDIA: comprobar primero si `nvidia-smi` responde; si NO, es el mismo bug.
- Prueba rápida de detección: `timeout 8 nvidia-smi --query-gpu=name,memory.used --format=csv,noheader` → si timeout, GPU colgada.
- Mientras tanto, el workaround operativo es: **reiniciar el PC** (arranque limpio recupera la GPU).
- Revisar en la próxima actualización de Ubuntu (26.04.x) o driver NVIDIA si el hilo del foro de NVIDIA tiene respuesta oficial.
