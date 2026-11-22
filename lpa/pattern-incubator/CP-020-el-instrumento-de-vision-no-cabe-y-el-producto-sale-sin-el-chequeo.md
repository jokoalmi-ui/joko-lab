---
type: candidate_pattern
id: CP-020
status: incubating
created: 2026-11-13
confidence: E0 (50 líneas de error en 7 días y 17 marcas de tiempo de 6 días consecutivos; producto entregado sin el chequeo y aviso solo dentro del artefacto; causa raíz propuesta = contención de VRAM, no medida con un control)
domain: observabilidad / instrumentos-de-verificacion
---

# CP-020 · El instrumento de visión no cabe en la VRAM, el chequeo se omite y el producto se entrega igual

> **Estado:** Incubación (E0)
> **Fecha:** 2026-11-13
> **Origen:** Revisión semanal LPA (`lpa/incidentes/revision-fallos-2026-11-13.md`). Detectado al leer el journal del gateway de la ventana 06→13-11 y el artefacto de la ficha de perfume del 12-11.
> **Nivel de confianza:** E0. La recurrencia y la degradación declarada están medidas; el mecanismo (VRAM ocupada por otro motor) es la explicación que encaja con todas las marcas, pero **no se ha ejecutado un control** (liberar VRAM y ver si carga).

---

## 1. Qué ocurrió

`vision_analyze` apunta a `google/gemma-4-12b-qat` servido por LM Studio en `:1234` (`~/.hermes/config.yaml`, bloque de visión). Ese modelo no carga. Cadena literal observada en el journal del gateway, repetida todos los días de la ventana:

```
ERROR tools.vision_tools: Error analyzing image: Error code: 400 -
{'error': {'message': 'Failed to load model "google/gemma-4-12b-qat".
 Error: Engine protocol runtime llama-server for 9O5FNmUwxJuSSrqesC02aeHb
 exited before becoming healthy. exitCode=1, signal=null', ...}}
ERROR tools.vision_tools: Error analyzing image: Error code: 400 - {'error': 'Model is unloaded.'}
WARNING agent.auxiliary_client: Auxiliary vision (async): request to
 http://localhost:1234/v1/ timed out after 180.0s (...) on custom, trying fallback
```

El consumidor no falla: sigue adelante y **entrega el producto sin el chequeo**, dejando el aviso dentro del propio artefacto. Cita literal del artefacto de la ficha del 12-11 (`cron/output/8bf412ac2ba3/2026-11-12_07-25-15.md`, línea 424):

> «**Chequeo visual por VLM no ejecutado**: `gemma-4-12b-qat` no carga (comfyui ocupa 8.080/12.282 MiB) y parar el servicio está bloqueado en modo cron (`BLOCKED: dangerous (stop/restart system service)`). Por tanto **el fondo klein no ha sido revisado por visión** para descartar letras inventadas — solo validado estructuralmente (1024², L media 184,6, esquinas claras).»

Medición de hoy (`nvidia-smi`, 13-11 17:3x): `NVIDIA RTX A2000 12GB, 8368 MiB usados / 12282 MiB`, ocupados por `llama-server` de LM Studio (8.276 MiB). El ocupante cambia (ComfyUI el 12-11, `llama-server` hoy); el resultado es el mismo: **quedan ~3,9 GB libres y un modelo de 12B no entra.**

---

## 2. Evidencia que lo respalda

- **50 líneas** con `Failed to load model "google/gemma-4-12b-qat"` en `journalctl --user` desde 2026-11-06 → **17 marcas de tiempo distintas en 6 días consecutivos** (07-11: 07:18, 09:02, 09:03, 09:11 ×2, 12:04 · 08-11: 08:25 · 09-11: 07:15, 19:14, 22:09 · 10-11: 07:38, 21:55 · 11-11: 07:12 · 12-11: 07:15, 07:24, 15:03, 15:10). Ningún día de la ventana se libra.
- **6 líneas** adicionales `{'error': 'Model is unloaded.'}` (segundo intento del mismo instrumento tras el fallo de carga).
- **Contextos distintos, mismo mecanismo:**
  1. *Ficha de perfume* (job `8bf412ac2ba3`, arranque 07:0x–07:2x, diario).
  2. *Corridas manuales de la misma ficha* el 12-11 (`source=direct`, 14:59 y 15:09; errores a las 15:03 y 15:10 → una por corrida).
  3. *Informe diario* (job `67d5fcc5b69e`, 09:0x: 07-11 09:02/09:03/09:11, 08-11 08:25, 09-11 07:15).
  4. *Franja nocturna* (09-11 19:14 y 22:09, 10-11 21:55) — sin job identificado en el artefacto; se anota como observación, no como ocurrencia contada.
- **Coste medido por intento:** 6,2–6,4 s hasta el 400 y después **180 s de timeout** del cliente auxiliar antes del fallback (12-11 15:03). Es decir, el fallo no es instantáneo: cada imagen que necesita visión quema ~3 min antes de degradar.
- **Degradación declarada y entregada:** el producto sale (ficha enviada el 12-11 con `delivered`), y el único sitio donde consta que el chequeo no se hizo es el artefacto del job. El usuario no recibe ese aviso en el mensaje.
- **El fallo persiste porque no tiene consecuencia:** 6 días seguidos, ningún job en rojo por esta causa, ninguna incidencia abierta en `cron_incidents` (0 filas con firma de visión).

---

## 3. Contradicciones o limitaciones

- **La causa no está aislada.** La contención de VRAM explica las 17 marcas, pero no se ha hecho el control: liberar VRAM (parar ComfyUI / descargar el LLM) y comprobar si `gemma-4-12b-qat` carga. Sin ese control, «no cabe» es hipótesis, no hecho. Alternativa no descartada: el motor `llama.cpp` instalado no soporta el formato QAT del modelo (`exitCode=1` del *engine*, no OOM explícito).
- **Un contador de 50 líneas no son 50 fallos independientes:** cada intento escribe 3 líneas (dos `ERROR tools.vision_tools` + el traceback). La cifra honesta son **17 marcas de tiempo**.
- **El fallo es a veces inocuo:** en el informe diario no se ha demostrado que la falta de visión cambie el producto; en la ficha sí hay una consecuencia concreta (fondo generado sin revisión de texto inventado).
- **No hay antídoto medido.** Ninguna de las dos salidas obvias (modelo de visión más pequeño que quepa, o turnos de VRAM) se ha probado; y `parar el servicio` está bloqueado en modo cron por diseño.
- **Dominio único hasta ahora** (Experimento 004, joko-lab): no hay evidencia fuera de este lab.

---

## 4. Principio que parece emerger

**Un instrumento de verificación que depende de un recurso compartido y escaso, cuando no consigue el recurso, no se apaga: se convierte en un «no comprobado» que viaja escondido dentro del producto.** El sistema no distingue «verificado y correcto» de «no verificado» en la superficie que ve el usuario; la diferencia solo existe en el log del instrumento y en una línea del artefacto. Si esa línea no se lee, el producto es indistinguible del verificado.

Corolario operativo: **todo chequeo que pueda degradarse a «no ejecutado» debe declararlo en el mismo canal por el que se entrega el producto**, y su causa (recurso escaso) debe tener un dueño explícito.

---

## 5. ¿En qué otros proyectos podría aplicarse?

- Cualquier pipeline con un verificador que comparte GPU/VRAM con el generador (visión + difusión en la misma tarjeta).
- CI con un linter/test que se salta silenciosamente por falta de recurso (timeout de runner, servicio auxiliar caído) y publica «verde».
- Revisión humana asistida: un revisor automático caído que deja pasar el documento como «revisado».
- Cualquier «gate» cuya indisponibilidad se resuelva con `continue` en lugar de `fail`.

---

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

Dos condiciones, cualquiera de ellas falsa el patrón:

1. **Control de recurso:** con la VRAM libre (≥ 10 GB disponibles, ningún otro motor cargado), `vision_analyze` sigue fallando con `exitCode=1` al cargar `gemma-4-12b-qat` → la causa no es la contención de VRAM y el principio «recurso escaso» no se sostiene (quedaría un patrón distinto: modelo incompatible).
2. **Contraejemplo de transparencia:** en **7 fichas consecutivas** el chequeo por visión se ejecuta (sin `Failed to load model` en el journal y sin la línea «no ejecutado» en el artefacto) **y** el aviso de degradación aparece en el mensaje entregado al usuario cuando no se ejecuta → el borde «no verificado indistinguible de verificado» deja de existir.

Falsación parcial adicional (degrada el nivel, no lo anula): encontrar un día en que el fallo de carga ocurriera con ≥ 10 GB de VRAM libre *y* el producto se entregara sin el chequeo — eso separaría las dos causas y obligaría a partir el patrón en dos.

---

## 7. Decisión

- [ ] Asciende a KNOWN.md como E1
- [ ] Asciende a procedures/ como procedimiento LPA
- [x] Sigue en incubación (falta evidencia)
- [ ] Se descarta (no sobrevive a otro dominio / fue falseado)
- [ ] Se fusiona con otro patrón

**Fecha de revisión:** 2026-11-13
**Justificación:** Se abre hoy por dos motivos que el ciclo exige: **2+ ocurrencias en contextos distintos** (ficha automática, corridas manuales de la ficha e informe diario) y **6 días consecutivos** de recurrencia medida en el journal. No se fusiona con CP-010 («un instrumento no validado miente en silencio»): CP-010 trata de un instrumento **que responde mal**; aquí el instrumento **no llega a ejecutarse** y el producto se entrega sin él. Tampoco con CP-009 («instrumento sin forzado se degrada»): allí el medidor deja de correr por falta de disparador; aquí se dispara todos los días y falla por recurso. Se queda en E0 porque falta el control que separa «no cabe en VRAM» de «el motor no soporta el modelo», y porque el dominio sigue siendo uno solo.

---

## Reexamen 2026-11-20 (semanal, ventana 13→20-11)

- **El fallo de carga sigue:** 43 líneas de `google/gemma-4-12b-qat` en el journal en 5 días (14, 15, 16, 17, 18-11), de ellas **34 `exited before becoming healthy`**; **0 cargas correctas**. El modelo **sí figura** en `/api/v0/models` con `state: not-loaded`: existe y no carga. **18 errores `vision_analyze`** en **7 de 8 días** (13, 14, 15, 16, 17, 18, 20-11).
- **Borde nuevo, más grave que la omisión:** en **4 fichas se afirma un veredicto de visión** (13-11 «VLM sobre el PNG suelto: sin letras ni marcos inventados»; 14-11 «visión local revisó el fondo suelto»; 18-11 «verificado por visión: lee «Papyrus Moléculaire / Maison Crivelli»»; 19-11 «VLM solo para lo atómico: sin texto inventado»), y **el journal de esos días solo contiene fallos**. El 18-11: `10:07:34` `400 Failed to load model`; `10:25:41` `Auxiliary vision (async): timed out after 180.0s`; el artefacto con la afirmación se escribió a las `10:26:46`. **1 de 8** fichas declara la degradación (17-11); **3 son silenciosas** (15, 16, 20-11).
- **Lo que NO se afirma:** que las 4 fichas mientan. La vía de respaldo (`glm-4.6v-flash`) **existe** en LM Studio y sus llamadas por `curl` no dejan rastro en el journal. Lo medido es que **la verificación no es trazable**: un `vision_analyze` correcto no escribe ninguna línea, así que «verificado por visión» y «no verificado» son **indistinguibles en el registro**. Este es el borde que el patrón pide cerrar, ahora con el agravante de que el producto **declara** la verificación.
- **Condición de falsación nº 2: NO se cumple.** Se exigían 7 fichas consecutivas con el chequeo ejecutado y aviso de degradación cuando no se ejecuta. Han sido 8 fichas: **0 ejecuciones confirmadas, 1 aviso de 8**. El patrón **no se cierra**.
- **Condición de falsación nº 1** (control con VRAM libre): **no ejecutada**. Sin ese control sigue sin saberse si la causa es VRAM o el propio GGUF.
- **Nivel:** sin cambio, **E0**. El reexamen no amplía dominio (Experimento 004, ficha diaria) pero **sí añade un mecanismo**: *la declaración de verificación sobrevive al instrumento que la haría falsa*. Para promover necesitaría el control de VRAM **y** una traza positiva; ninguna de las dos existe.
- Mejora propuesta (no aplicada): que `vision_analyze` registre también el éxito (modelo, ms, ruta) además del error, en el journal o en el artefacto. Sin eso, este patrón no es auditable nunca.
