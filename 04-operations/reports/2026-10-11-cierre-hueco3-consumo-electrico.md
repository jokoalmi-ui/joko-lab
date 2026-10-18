# Cierre — HUECO 3: consumo eléctrico del lab (medido)

**Fecha:** 2026-10-11 (domingo), ventanas 14:10:25 · 14:13:36 · 14:16:08 · 14:17:52 CEST.
**Cierra:** hueco 3 declarado en `tfm/ANEXO-METODOLOGICO-JOKO-LAB.txt:107-112` y prioridad nº1 del trabajo futuro (línea 117).
**Variante elegida por el usuario:** **sin privilegios** (no se lee RAPL, no se eleva nada, no hay medidor físico).
**Cierre con la terna** (`PLANTILLA-cierre-outcome-trayectoria-constraints.md` v1.0).

---

## 0. Veredicto en una línea

Antes: «consumo eléctrico **no medido**». Ahora: **medido en la parte que se puede medir sin privilegios** (GPU por `nvidia-smi`, ~98 % del límite de 70 W en inferencia sostenida, ~9,2 W en reposo), con el resto **declarado NO MEDIBLE** por falta de permiso y de medidor físico — no por falta de trabajo.

---

## 1. `outcome` — qué hay medido (cifras reales, no estimaciones)

Instrumento: `instruments/consumo-electrico/medir_consumo.py` v0.1 (solo lectura).
Histórico: `instruments/consumo-electrico/outputs/consumo.jsonl` (4 líneas al cierre).

- **Reposo del lab** (20,042 s y 45 s de ventana; sin carga):

  | ventana | GPU P media | GPU P máx | energía GPU | CPU ocupación |
  |---|---|---|---|---|
  | 20,0 s (14:10:25) | **9,37 W** | 10,26 W | 0,0521 Wh | 23,32 % |
  | 45,0 s (14:17:52) | (incluye flancos) | 40,92 W | 0,4432 Wh | 39,94 % |

- **Inferencia sostenida — solape DEMOSTRADO por hora absoluta por muestra**
  (15 muestras entre 14:17:17 y 14:17:32; trabajo: 2 pasadas seguidas de la batería `json`+`tool_calling` con `qwen2.5:7b` en Ollama, `num_ctx=8192`):

  - P media **65,94 W** · P máx **68,75 W** → **98,2 % del límite de 70 W** de la RTX A2000.
  - Utilización GPU 89–97 % · VRAM 6.226 MiB (modelo ya cargado).
  - Energía del tramo: **0,27157 Wh = 977,6 J** en 15,4 s.
  - Serie literal (W): `35.47, 68.33, 68.39, 68.36, 68.27, 68.51, 67.32, 64.81, 68.62, 68.75, 68.22, 68.60, 68.29, 68.71, 68.47`.

- **Coste energético de una corrida de la batería** (8 casos, ~7,6 s en caliente): **≈0,13–0,14 Wh**.
- **Referencia de arranque en frío** (heredada del cierre del hueco 2, 99 s con carga del modelo): **≈1,65 Wh**.

### NO MEDIDO (declarado, con motivo)

- **CPU / RAM / SoC en vatios:** RAPL detecta **6 dominios** (`intel-rapl`, `intel-rapl:0`, `:0:0`, `:0:1`, `:0:2`, `intel-rapl:1`) y **0 son legibles** sin privilegio (`energy_uj` → `PermissionError`, 0400 root). Sin lectura no se estima: solo se registra **ocupación** (23–25 % en reposo).
- **Discos, ventiladores, USB y pérdidas de la fuente:** fuera del alcance de `nvidia-smi` y de RAPL.
- **Medida «de pared»:** requiere medidor físico. **El lab no tiene ninguno.**
- **Coste en €:** no se calcula (no se aportó precio/kWh; el instrumento lo exige explícito y solo cubriría la GPU).

---

## 2. `trayectoria` — cómo se llegó, incluido lo que falló

1. Sonda previa (13:53): RAPL existe, `energy_uj` es 0400 root → se descarta la vía con privilegios.
2. Escritura del instrumento v0.1 (solo lectura, molde `critic-loop`: no toca config, no para servicios, escribe solo en `outputs/`).
3. **Corrida 1 en reposo** (20 s) → OK: 9,37 W media, RAPL 0/6 legibles (el límite queda medido, no supuesto).
4. **Corrida 2 (falso negativo):** ventana de 150 s lanzada en el mismo turno que la carga → **el muestreador arrancó DESPUÉS de que la carga terminara** (la batería en caliente dura 7,6 s) → midió reposo (9,09 W) con etiqueta de carga. **No se borra ni se disimula: queda en el histórico como línea 2 y se explica aquí.**
5. **Corrida 3:** lanzada en paso separado → capturó actividad (P máx 35,42 W durante 16,5 s) pero con **origen no identificable** porque las muestras no tenían hora absoluta → **mejora del instrumento**: serie de muestras + **hora absoluta por muestra**.
6. **Corrida 4 (confirmación):** ventana de 45 s arrancada antes y parada después de la carga, con la carga fechada por `date` (14:17:17,259 → 14:17:32,652) → **solape demostrado**: 15 muestras dentro del intervalo, 65,94 W de media, 68,75 W de pico.

**Hallazgo de trayectoria que la terna obliga a declarar:** en este régimen la potencia **no es un número, es una curva** (9,2 W reposo / ~25 W pasada corta aislada / 65,9 W sostenido). Cualquier cifra única de «consumo del lab» sin declarar el régimen es un dato mal leído.

---

## 3. `constraints` — límites y coste del propio cierre

- **Privilegios: 0.** No se usó `sudo`, no se cambió ningún permiso, no se leyó `energy_uj`.
- **Servicios tocados: 0** (no se arrancó, paró ni reinició nada; Ollama se usó como estaba).
- **Vector de daño del propio test: ninguno** — el instrumento solo ejecuta `nvidia-smi` y lecturas de `/proc` y `/sys`; escribe únicamente en su carpeta `outputs/`.
- **Coste en € del cierre: 0** (todo local).
- **Energía consumida por el propio cierre:** las 4 ventanas del instrumento (20+150+120+45 s) más las corridas de la batería: **≈0,5–0,7 Wh de GPU** en total.
- **Riesgo residual:** un muestreo a 1 Hz puede perder picos más cortos que el intervalo; el pico real **no es menor** que el medido.
- **Incertidumbre pendiente:** sin hora absoluta por muestra no se puede atribuir un tramo a un trabajo concreto; desde v0.1.2 ese agujero está cerrado.

---

## 4. Qué aporta al temario del reel y límite honesto

Cubre el **problema 13 (Cost)** del reel `DeCI09WTN51` en su parte medible: coste energético **por corrida** con cifra real y por régimen. Límite: **no** es una medida de pared, **no** incluye CPU (sin privilegio) y **no** cubre el resto del sistema. Un «Failure Recovery Cost» o un «kWh/mes por servicio» completo exigiría o el permiso de RAPL o un medidor físico: decisión del usuario, no del instrumento.
