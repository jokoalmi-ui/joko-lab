---
type: knowledge
subtype: observation
status: active
tags: [knowledge, observation, mtp, speculative-decoding, llama.cpp, lmstudio, gpu, rendimiento]
created: 2026-09-16
---
# OBS-110: El MTP acelera en GPU (+28%) y frena en CPU (-18%); el optimo es 1 borrador, no 4
===============================================

## Datos basicos
  ID: OBS-110
  Fecha: 2026-09-16
  Origen: sesion 2026-09-16. A raiz del video gceu4XZas_I (Ricardo Bertran, repo
          qwen38-mtp-dflash-benchmark) y de la pregunta del usuario sobre si el MTP
          acelera la inferencia local. Metodo: llama.cpp propio en ventana aislada
          (:8099), sin tocar LM Studio, GLM de vision, ComfyUI ni n8n.

## Observacion

El MTP (Multi-Token Prediction: el propio modelo trae cabezas entrenadas para predecir
varios tokens y se usan como draft en decodificacion especulativa) NO es una capacidad
del motor, sino una CAPA que unos GGUF traen y otros no, del mismo modelo.

Medido en el lab: en GPU acelera de forma clara y sin cambiar el texto; en CPU frena.
El punto dulce de borradores es 1, no 4: la ganancia se hunde al subir n-max.

## Evidencia literal (medida en el lab, 2026-09-16)

1) Ningun GGUF local traia MTP. Lectura de nombres de tensores en 8 arquitecturas
   (qwen35moe, gpt-oss, granite, granitehybrid, gemma4, glm4, lfm2, qwen2): 0 tensores
   `mtp`/`nextn`. El binario si lo soporta: llama-server 2.38.0, `--spec-type` ofrece
   none, draft-simple, draft-eagle3, draft-mtp, draft-dflash, draft-dspark, ngram-*.

2) Modelo usado para medir MTP real (opcion 1 aprobada por el usuario):
   DavidAU/Qwen3.5-9B-...-NEO-IMATRIX-MAX-MTP-GGUF -> IQ3_M, 5.722.667.232 B,
   442 tensores (427 sin MTP), `qwen35.nextn_predict_layers = 1`, 4 tensores
   `blk.32.nextn.{eh_proj,enorm,hnorm,shared_head_norm}`.

3) Criterio duro de activacion (no fallback silencioso): en modo `none` el binario
   avisa 4 veces "unused tensor blk.32.nextn.* - ignoring"; en `draft-mtp` ese aviso
   desaparece (unused=0) en las 9 pasadas. El mecanismo se engancha de verdad.

4) CPU (RTX no usada, -ngl 0, 3 rondas intercaladas, 128 tokens, temp 0):
   none 2,763 tok/s | n-max 2: 2,247 (-18,5%) | n-max 4: 1,606 (-42,3%)

5) GPU (RTX A2000, -ngl 99, flash-attn on, 3 rondas, mismo test):
   none 31,84 tok/s (dispersion 0,3%)
   n-max 2: 39,62 tok/s -> +24,0% (aceptacion 67,3%)
   n-max 4: 30,98 tok/s -> -3,0% (aceptacion 41,5%)
   Texto identico en los tres modos (coincidencia 1,0) -> sin perdida de calidad.
   VRAM con el modelo cargado: none 7.786 MiB | n2 8.414 | n4 8.832 MiB.

6) Curva de n-max en GPU (2 rondas mas, baseline contemporaneo):
   n1 40,60 tok/s -> +28,1% (aceptacion 82,6%)   <- OPTIMO
   n2 39,62       -> +24,0% (67,3%)
   n3 35,62       -> +12,4% (53,1%)
   n4 30,98       ->  -3,0% (41,5%)
   n6 24,72       -> -22,0% (30,1%)
   n8 20,68       -> -34,8% (21,2%)
   Interpretacion: la probabilidad de acertar TODOS los borradores cae en picado
   (82,6% -> 41,5% en cuatro pasos) mientras se paga la verificacion de todos.

7) LM Studio del lab YA soporta MTP nativo (verificado en `lms load --help`):
   --speculative-draft-mtp, --speculative-draft-max-tokens,
   --speculative-draft-min-tokens, --speculative-draft-min-continue-probability.
   Es decir, no hace falta montar llama.cpp externo para aprovecharlo.

8) Qwen 3.6 en el lab: el modelo local (noctrex MXFP4, `qwen3.6-35b-a3b_moe`) NO trae
   MTP; el de unsloth SI (`unsloth/Qwen3.6-35B-A3B-MTP-GGUF`, 753 tensores,
   `qwen35moe.nextn_predict_layers = 1`), con quants de 11,37 GB (UD-IQ1_M) a
   49,91 GB. Ninguno cabe entero en los 12 GB de la A2000 -> offload, como ya se usa.

## Alcance

- Medido en una RTX A2000 de 12 GB con un 9B hibrido SSM+atencion en IQ3_M.
- La direccion del efecto (GPU suma, CPU resta) es coherente con el mecanismo: MTP paga
  cuando el cuello es leer pesos de memoria (GPU) y no cuando es computo (CPU).
- Regla operativa derivada, aplicable ya al lab: si se usa MTP, n-max 1-2 y nunca 4+;
  en CPU, no activarlo.

## Que NO dice

- No es el "+73%" del video: alli es otro modelo (Qwen3.8-27B + dflash) y otra GPU.
  Nuestra cifra es +28,1% medido aqui, no extrapolable a otra maquina.
- El modelo medido es un fine-tune "uncensored/heretic": vale para medir mecanismo y
  tokens/s, NO como modelo de trabajo.
- No se ha medido todavia un Qwen 3.6 con MTP (round 2): la descarga se lanzo el
  2026-09-16. Sin dato.
- No se ha medido el regimen de offload parcial (parte GPU, parte CPU), que es el que
  usaria el 35B en esta maquina.
- La maquina estaba paginando durante las medidas (swap 3,7 GB, disco 110-200 MB/s):
  por eso la bateria usa rondas intercaladas con baseline contemporaneo, no un
  baseline viejo. Con el sistema en thrashing se midio 0,40 tok/s en el mismo modelo.

## Acciones derivadas

- Registro de las medidas: `/tmp/mtp-medicion-20260916.json` (13 bloques).
- Scripts de medida: `/tmp/mtp_control.py`, `/tmp/mtp_bateria2.py`,
  `/tmp/mtp_bateria3_gpu.py`, `/tmp/mtp_curva.py`; verificador de cabeceras GGUF
  `/tmp/gguf_tensores.py` (corregido: guarda TODOS los KV, no solo 5 claves).
- Verificacion del estado del sistema tras las pruebas: GLM de vision restaurado
  identico (IDLE, 7,95 GB, ctx 21504, 4 paralelos), puerto 8099 libre, sin procesos
  propios vivos.
- Pendiente (round 2): medir MTP en `unsloth/Qwen3.6-35B-A3B-MTP-GGUF`.

## Actualizacion 2026-09-16 (inventario completo del parque de modelos)

- Inventario real de los 16 GGUF del disco (14 modelos de LM Studio + los de la carpeta
  de vision): **solo 2 traen bloque MTP dentro** — `Qwen3.6-35B-A3B-UD-Q4_K_M` (unsloth,
  `blk.40.nextn.*`, 504,4 MB, `nextn_predict_layers = 1`) y `Qwen3.5-9B The Defiant Fable`
  (DavidAU, `blk.32.nextn.*`). El punto 1 de esta OBS ("ningun GGUF local traia MTP") era
  cierto ANTES de la descarga del 2026-09-16: queda superado por este inventario.
- De los modelos en uso, ninguno trae MTP salvo el 35B de unsloth. El candidato claro que
  NO se aprovecha es **Gemma 4 12B**: drafter oficial `google/gemma-4-12B-it-assistant`
  (MTP con KV compartida), empaquetado tambien en `unsloth/gemma-4-12b-it-GGUF/MTP/`.
- **GLM-4.6V-Flash NO tiene MTP**: `config.json` oficial (`zai-org/GLM-4.6V-Flash`) declara
  `Glm4vForConditionalGeneration`, 40 capas y 0 campos nextn. La familia GLM-4.5/4.6/4.7 de
  TEXTO si lleva MTP nativo; la de vision no.
- Sin MTP y sin drafter publicado: gpt-oss-20b, Granite 4.1-8b y 4.0-h-tiny,
  DeepSeek-R1-Distill-14B, LFM2.5 (2.6B y VL-3B), Dolphin3, embeddings.
- Matiz sobre el punto 7 de esta OBS: el CLI instalado (LM Studio 0.4.20+1) SI lista los
  flags `--speculative-draft-mtp*`, pero el changelog oficial situa la exposicion de MTP
  en 0.4.22. No se ha verificado en vivo una carga con MTP desde LM Studio: sin dato.
- Referencia cruzada: OBS-111 (frontera del offload de MoE medida en esta GPU).

## Actualizacion 2026-09-16 (MTP + offload de MoE: el borrador no compensa)

- Bateria nueva (17:09:05-17:16:14 CEST) sobre el MISMO modelo que trae MTP
  (unsloth/Qwen3.6-35B-A3B-UD-Q4_K_M, 21,1 GiB) en el regimen de offload que usa en
  esta GPU (`-ngl 99 -ncmoe 24`): una carga por config y, dentro de cada carga,
  1 calentamiento + 3 generaciones de 64 tokens (mismo prompt, temp 0, seed 1234).
- Sin MTP: 2,07 tok/s (1,75 / 2,07 / 2,18) con VRAM pico 11.093 MiB.
- Con MTP (`--spec-type draft-mtp --spec-draft-n-max 1`): 2,18 tok/s (1,93 / 2,18 /
  2,23) con VRAM pico 11.773 MiB -> **+5,3%**, muy lejos del +28,1% de GPU pura (punto 6).
- Criterio duro de activacion: el aviso "unused tensor blk.40.nextn.*" pasa de 4 a 0
  y el motor reporta 34 borradores / 28 aceptados (82,4%). El mecanismo SI se engancha:
  el +5,3% no es un fallo de montaje, es el techo de este regimen.
- Coste en VRAM: +680 MiB (11.093 -> 11.773) sobre 12.282, dejando 509 MiB de margen.
  Con `-ncmoe 24` ya se va al limite (ncmoe 20 no arranca, OBS-111): activar MTP ahi es
  quedarse sin colchon para contexto o KV.
- En tiempo real: 530 tokens pasan de 256,0 s a 243,1 s (13 s menos en mas de 4 min).
- Aviso de instrumento: la MISMA config `-ncmoe 24` dio 1,44 tok/s en la tanda de la
  manana (OBS-111) y 2,07 tok/s en esta; el regimen de offload varia entre tandas y las
  pruebas fueron en serie (A entera, luego B), no intercaladas. El +5,3% queda dentro
  del ruido observable: NO es un efecto solido.
- Conclusion: MTP y offload NO se combinan a favor en esta maquina. MTP paga cuando el
  cuello es computo (GPU pura); con los expertos en CPU el cuello es memoria/PCIe y el
  borrador no rescata nada. Se descarta activar MTP por defecto en el perfil del 35B.
- Pendiente declarado: sin medir la curva n-max 2/3 en este regimen ni el flag
  `--spec-draft-n-cpu-moe` (MoE del draft en CPU): sin dato.
- Datos crudos: /tmp/exp007/mtp_offload.jsonl, /tmp/exp007/mtp_offload_stdout.log y
  logs /tmp/exp007/mtp_server_{off_nomtp,off_mtp_n1}.log; script
  /tmp/prueba_mtp_offload.py (llama.cpp propio en :8099, cierra por PID; LM Studio,
  headless de vision, ComfyUI y n8n intactos).
