# A(T2) — MTP en llama.cpp y LM Studio (celda A: sesión directa)

- Tarea T2. Iniciada 15:36 CEST. Método: búsqueda web + extracción + verificación local.
- Respuesta 1 — llama.cpp: MTP entró con la PR #22673 (merged 2026-05-16, commit de merge 255582687b8dd211fdbc582e43ab842491554e94). Flags: `--spec-type draft-mtp` + `--spec-draft-n-max N` (default 3). Los flags antiguos están removidos: `--draft-max` → "the argument has been removed. use --spec-draft-n-max".
- Respuesta 2 — LM Studio: soporte MTP desde 0.4.22 (28-ago-2026), requiere engine llama.cpp ≥ 2.29.1.
- Respuesta 3 — Lab: la app instalada es 0.4.20+1 → NO trae el soporte (llega en 0.4.22). El engine instalado (carpeta 2.38.0; `--version` = 0.4.1-dev build 1, commit dfe4516) SÍ acepta `--spec-type draft-mtp`.
- Respuesta 4 — Límites oficiales: el prompt processing empeora con MTP (transferencias D2H); decodificación paralela soportada pero no optimizada; compatible con visión y tensor/pipeline parallelism.
- Respuesta 5 — Aceptación declarada por el autor: ~75% con 3 tokens de draft, >2× de velocidad.
- Evidencia de primera mano (no verificable por curl, sí reproducible): 52 flags `--spec-*` en el binario; `--spec-type none,draft-simple,draft-eagle3,draft-mtp,draft-dflash,draft-dspark,ngram-*` con default `none`; `--spec-draft-n-max` con default 3.
- Verificación: 4 citas en 2 URLs oficiales + 1 control negativo. Medidor: `/tmp/exp007/calidad-A-T2.json`.
