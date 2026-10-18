---
type: operations
subtype: report
status: active
tags: [operations, report]
created: 2026-07-28
---
# Informe: Captura de Firefox con computer_use (cua-driver)

**Fecha:** 17 julio 2026
**Sesiones implicadas:** 4 (08:36, 11:05, 11:14, 13:49)
**Estado:** Fallo persistente en timepo real. Fixes de código committeados pendientes de reinicio de sesión.

---

## 1. Objetivo

Conseguir que `computer_use capture app=Firefox mode=som` funcione — es decir, tomar una captura de la ventana de Firefox en segundo plano sin robar el foco del usuario.

---

## 2. Contexto técnico

| Elemento | Valor |
|----------|-------|
| OS | Ubuntu 26.04 LTS |
| Display server | Wayland (GNOME) |
| cua-driver | 0.8.3 (actualizado desde 0.6.8) |
| Hermes Agent | profile=default, backend Python en `tools/computer_use/cua_backend.py` |
| Firefox | PID 39309, ejecutándose |
| GPU | RTX A2000 12GB |

---

## 3. Historial de fixes aplicados

### Commit `6eacecfa` — fix z_index=None

**Problema:** En Wayland/GNOME, cua-driver cae a fallback AT-SPI cuando no encuentra los protocolos `wlr_ext_foreign_toplevel`. AT-SPI devuelve ventanas con `z_index=null`, y `sort()` crashea con:

> `<` not supported between instances of 'NoneType' and 'NoneType'

**Fix:** `w.get('z_index') or 0` en lugar de `w.get('z_index', 0)`

**Tests:** 7/7 unit tests pasados (None→0, missing→0, 5→5, sorting mixto, Wayland inject, manual override, no-Wayland).

### Commit `5c9c9d12` — fix session=None + reset _started

**Problema:** Cuando cua-driver se reinicia (kill + rearranque automático), el objeto `CuaBackend` queda con `session=None`. Al llamar a `_call_tool_async` sin sesión, se produce `BrokenPipeError`. Ademas, `_started` no se resetea al salir del lifecycle, dejando el backend en un estado zombie.

**Fix:** Manejar `session=None` → `BrokenPipeError` + resetear `_started` en lifecycle exit.

**Tests:** 167/167 passed (test_computer_use.py completo, 4.95s).

---

## 4. Pruebas realizadas en la sesión actual (13:49)

### Prueba 1: capture app=Firefox
```python
computer_use(action='capture', app='Firefox', mode='som')
```
**Resultado:** Ventana 0x0, `"<no on-screen window matched app='Firefox'>"`, 0 elementos interactivos.

### Prueba 2: list_apps
```python
computer_use(action='list_apps')
```
**Resultado:** Firefox listado con PID 39309 y múltiples procesos hijo (39571, 39598, 39605, 39614, 39660, 39877, 39986, 42063, 42066, 42113). Firefox sí está en ejecución, pero cua-driver no lo reconoce como ventana visible.

### Prueba 3: capture app=screen (modo SOM)
```python
computer_use(action='capture', app='screen')
```
**Resultado:** Captura 1568x882, app=gjs (GNOME Shell), 0 elementos interactivos. Visión por IA falló con: `unknown variant 'image_url', expected 'text'` (error de serialización JSON en el modelo).

### Prueba 4-6: captures sin filtro / modo vision
```python
computer_use(action='capture', mode='vision')
computer_use(action='capture')  # modo SOM por defecto
computer_use(action='capture', app='desktop')
```
**Resultado:** Las 3 fallaron con `"capture failed: "` (error vacío).

### Prueba 5: doctor (diagnóstico)
```bash
hermes computer-use doctor
```
**Resultado:**
```
⚠️ cua-driver 0.8.3 on linux — degraded
  ✅ binary_version: 0.8.3
  ✅ platform_supported: Ubuntu 26.04 LTS
  ✅ session_active
  ✅ ax_capability (AT-SPI reachable)
  ✅ screen_capture_capability (xdg-desktop-portal reachable)
  ❌ wayland_backend: compositor sin adaptador target-activation
      (foreign-toplevel=false, screencopy=false, ext-image-copy=false)
      → Solución: instalar WinRects Shell helper de GNOME
```

### Prueba 6: estado del proceso cua-driver
```bash
ps aux | grep cua-driver
```
**Resultado:** PID 110317, **99.4% CPU sostenido** (2:54 de CPU acumulado desde las 13:49). Anormal.

---

## 5. Fallos identificados

### Fallo A — cua-driver en estado degradado (activo)

| Síntoma | Causa raíz |
|---------|-----------|
| capture devuelve 0x0 o error vacío | Wayland backend no tiene adaptador de activación de ventanas |
| 99.4% CPU sostenido | Driver posiblemente en bucle intentando resolver ventanas |
| "no window matched" aunque Firefox existe | Sin target-activation, cua-driver no puede asociar ventanas GNOME |

### Fallo B — xdg-desktop-portal consent

La captura de pantalla en Wayland pasa por `xdg-desktop-portal Screenshot`, que requiere **un consentimiento visual por sesión** (pop-up de GNOME). Si ese diálogo está mostrándose o bloqueado, capture falla.

### Fallo C — Fixes en código no efectivos hasta reinicio

Los commits `6eacecfa` y `5c9c9d12` están en disco pero Hermes los cargó en memoria al iniciar la sesión. Python no recarga módulos, así que los parches no están activos en esta sesión.

---

## 6. Dependencias para solucionar

1. **Reiniciar sesión de Hermes** (`fin` + volver a entrar) para que se carguen los fixes de `cua_backend.py`
2. **Instalar WinRects Shell helper** — extensión de GNOME que cua-driver usa para activación de ventanas en Wayland
3. **Matar el proceso cua-driver actual** (99.4% CPU) para que Hermes lo reinicie limpio
4. **Aceptar el diálogo de consentimiento** de xdg-desktop-portal la primera vez

---

## 7. Resumen de commits

| Commit | Archivo | Descripción |
|--------|---------|-------------|
| `6eacecfa` | `tools/computer_use/cua_backend.py` | Fix `z_index=None` → `or 0` |
| `5c9c9d12` | `tools/computer_use/cua_backend.py` | Fix `session=None` → `BrokenPipeError` + reset `_started` |

---

## 8. Próximo paso recomendado

Cerrar esta sesión (`fin`), volver a entrar con Hermes recargado, y entonces:

1. Verificar que los fixes están activos en la nueva sesión
2. Matar cua-driver zombie si sigue al 99% CPU
3. Probar `computer_use capture app=Firefox mode=som`
4. Si sigue fallando, instalar WinRects helper
