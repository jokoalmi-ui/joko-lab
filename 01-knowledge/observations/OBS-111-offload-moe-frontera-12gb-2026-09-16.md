---
type: knowledge
subtype: observation
status: active
tags: [knowledge, observation, moe, offload, llama.cpp, vram, gpu, rendimiento]
created: 2026-09-16
---
# OBS-111: El offload de MoE arranca el 35B en 12 GB (1,44 tok/s) y se rompe entre 20 y 24 capas
===============================================

## Datos basicos
  ID: OBS-111
  Fecha: 2026-09-16 (ventana 16:29:03-16:35:30 CEST)
  Origen: peticion del usuario ("Haz la prueba") dentro de EXP-20260916-007, tarea T3.
          Metodo: llama.cpp PROPIO 2.38.0 en ventana aislada (:8099), sin tocar
          LM Studio (:1234), el headless de vision (:1235), Ollama (:11434) ni n8n.
          VRAM liberada antes (GLM descargado), ComfyUI detenido.

## Observacion

El offload de expertos (n-cpu-moe / ncmoe) permite ARRANCAR un MoE que no cabe en
12 GB, pero no permite TRABAJAR con el: 1,44 tok/s frente a ~40 tok/s de un modelo
que si cabe entero (OBS-110). La frontera fisica de esta GPU esta entre 20 y 24
capas de expertos en GPU: con 24 arranca (VRAM pico 11.068 de 12.282 MiB), con 20
NO arranca y ademas PIDE MAS memoria (un unico buffer de 11.303 MiB).

Con menos capas en GPU el consumo sube, no baja: el reparto que funciona es dejar
en CPU justo los expertos que no caben, no "cuantos mas mejor".

## Evidencia literal (medida en el lab, 2026-09-16)

Modelo: unsloth/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -> 22.663.387.424 B (21,1 GiB),
MoE A3B (35B totales / ~3B activos), 753 tensores, `qwen35moe.nextn_predict_layers = 1`,
bloque MTP `blk.40.nextn.*` = 20 tensores / 504,4 MB.

1) CPU puro (`-ngl 0`):
   carga 84,2 s | prompt 0,34 tok/s | generacion 0,37 tok/s | VRAM pico 1.631 MiB | rss 3,64 GiB

2) Hibrido 24 (`-ngl 99 -ncmoe 24`):
   carga 84,4 s | prompt 1,04 tok/s | generacion 1,44 tok/s (x3,9) | VRAM pico 11.068 MiB | rss 3,4 GiB

3) Hibrido 20 (`-ngl 99 -ncmoe 20`):
   NO ARRANCA (rc=1): `cudaMalloc failed: out of memory`, pidiendo 11.303 MiB
   en un solo buffer.

4) Prefill (mismo prompt, 32 tokens): CPU puro 34,9 s vs hibrido 11,5 s (x3,0).

5) El bloque MTP del GGUF NO cuesta VRAM si no se activa decodificacion especulativa:
   el motor avisa "unused tensor blk.40.nextn.*" (20 tensores, 504,4 MB) y los ignora.

6) El tiempo de carga (~84 s) es identico en las tres configuraciones: el cuello de
   arranque es leer 21,1 GiB de disco a RAM, no el reparto GPU/CPU.

## Alcance

- RTX A2000 de 12 GB (12.282 MiB) con el escritorio ocupando ~1,1-1,6 GiB; CPU i5-9500.
- Un solo modelo y un solo quant (A3B, Q4_K_M): la frontera 20-24 capas es de ESTE
  modelo en ESTA GPU, no una constante.
- La direccion del efecto es coherente con el mecanismo: el offload cambia lectura de
  VRAM por transferencia por PCIe y lectura de RAM; el MoE con ~3B activos sigue
  necesitando mover todos los expertos que toquen.
- Regla operativa derivada: en esta maquina, para el 35B MoE el offload es la ultima
  opcion (sirve para no fallar, no para trabajar); si se usa, ncmoe >= 24 y ~1,4 tok/s.

## Que NO dice

- No mide calidad de respuesta: solo velocidad de prompt y generacion.
- No afina la frontera: no se probo ncmoe 21, 22 ni 23.
- No prueba el regimen combinado MTP + offload (`--spec-draft-n-cpu-moe`), que es el
  que aprovecharia a la vez el bloque nextn y el offload: sin dato.
- No se probo con KV cache cuantizada ni contextos grandes (el prompt era corto).
- No compara con otras GPU ni con el mismo modelo en un quant mas pequeno.

## Acciones derivadas

- Datos crudos: `/tmp/exp007/moe_empirico.jsonl`; logs por configuracion en
  `/tmp/exp007/moe_server_{cpu_puro,hibrido_ncmoe24,hibrido_ncmoe20}.log`.
- Script de la bateria: `/tmp/prueba_moe_offload.py` (3 configs en serie, libera VRAM
  al terminar cada una).
- Informe: EXP-20260916-007, `f2-A-T3-empirico.md`; veredicto en `f3-veredicto.md`.
- Relacionado: OBS-110 (MTP: GPU +28,1% / CPU -18%); el MTP NO rescata este caso
  porque el cuello del offload es memoria, no computo.
- Pendiente (si se retoma): afinar ncmoe 21-23. El combinado MTP+offload ya NO esta
  pendiente: medido y anotado abajo. Queda sin medir el flag `--spec-draft-n-cpu-moe`
  (MoE del modelo draft en CPU) y la curva n-max 2/3 en este regimen.

## Actualizacion 2026-09-16 (combinado medido: MTP sobre el offload)

- El regimen que esta OBS dejaba como pendiente YA esta medido: sobre `-ncmoe 24`,
  activar `--spec-type draft-mtp --spec-draft-n-max 1` sube de 2,07 a 2,18 tok/s
  (+5,3%, dentro del ruido entre tandas) y cuesta +680 MiB de VRAM (11.093 -> 11.773,
  margen 509 MiB). La medicion completa vive en OBS-110, seccion "Actualizacion
  2026-09-16 (MTP + offload de MoE: el borrador no compensa)".
- Consecuencia para la regla operativa de esta OBS: el offload sigue siendo la ultima
  opcion en esta maquina y NO se le anade MTP, porque el borrador no compensa cuando
  el cuello es memoria y no computo.
