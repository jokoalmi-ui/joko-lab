---
type: knowledge
subtype: observation
status: active
tags: [knowledge, observation, rag]
created: 2026-11-08
---
# OBS-273: El corpus propio compite con la biblioteca externa
===============================================

## Datos basicos
  ID: OBS-273
  Fecha: 2026-11-08
  Origen: A/B grep vs LanceDB y banco adversarial v2 (sesion 08-11)

## Observacion

De 6 consultas fuera del dominio del lab, 5 devuelven como top-1 un documento de
01-knowledge/references/ (biblioteca externa), no conocimiento propio.

  consultas fuera de dominio .... 6
  top-1 en biblioteca externa .... 5
  distancias top-1 .............. 0,48 - 0,65 (media 0,58)

La trampa 'sagemaker' ilustra el mecanismo: figura en el indice como
"AWS SageMaker Model Registry" dentro de
wshobson-agents/plugins/machine-learning-ops/agents/mlops-engineer.md,
pero rg no la ve porque .gitignore excluye references/ y rg respeta .gitignore.
La verificacion valida es contra el indice, no contra el arbol de ficheros.

Tamano de la capa externa: 3.795 ficheros .md en 01-knowledge/references/ (6
directorios), dentro de un indice de 61.733 filas.

Coincide con OBS-263 y OBS-266 (desequilibrio del RAG) y con OBS-272, que registra:
"Documento mas recuperado: 04-operations/backlogs/2026-07-31-backlog.md (355 veces)."

## Relacionado
  OBS-263, OBS-266 (desequilibrio del RAG)
  OBS-272 (telemetria: el backlog como hub)
  tools/evaluar_rag_adversarial.py (lo mide: bloque A y contador externos_a)

## Sin accion
Observacion sin HYP. No se modifica el indice, el pipeline ni el banco de evaluacion
por este documento.
