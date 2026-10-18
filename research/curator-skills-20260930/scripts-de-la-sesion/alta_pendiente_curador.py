#!/usr/bin/env python3
# Anade a pendientes.md el bloque del hallazgo del curador (OBS-154). Fail-closed.
# SIN --apply = dry-run. Con --apply escribe, reverifica desde disco y comprueba
# que NINGUNA linea previa se ha perdido (subsecuencia exacta).
import sys, hashlib, pathlib, datetime

REPO = pathlib.Path("/home/jokoalmi/joko-lab")
DEST = REPO / "04-operations/backlogs/pendientes.md"
MARCA = "curador-skills-20260930"
APPLY = "--apply" in sys.argv
OBS = "01-knowledge/observations/OBS-154-curador-edita-skills-sin-ok-2026-09-30.md"

ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
bloque = f"""
## {ahora} CEST — HALLAZGO: el curador de Hermes edita skills del lab sin OK (51 operaciones hoy sobre 7 skills) y el estado dice `paused: true`

MARCA: {MARCA}

- **Que se vio**: al ir a anotar una leccion en `instagram-content-extraction`, `SKILL.md` habia cambiado bajo los pies del agente: 99346 B / md5 `825ab7c738a05ce6230d755ddf49c299` (16:12) -> 99517 B / md5 `f813f884c349b0ab93805b38d63e3c7a` (16:15:08). Escritor: el pase de curaduria de Hermes (`actor: curator`), dentro de la sesion del propio agente.
- **Evidencia**: ledger `.hermes/skills/.curator_ledger.jsonl` (1750 filas desde el 01-sep): **51 operaciones hoy sobre 7 skills** (`hermes-cron-jobs` 27, `render-html-a-imagen` 10, `edicion-aditiva-registros` 7, `instagram-content-extraction` 4, y 1 en `watchdog-salud-sistema`, `delegacion-subagentes` y `vigilancia-canales-youtube`). Confirmado con un segundo instrumento (`hermes curator ledger`). Copias: `.hermes/.curator_backups/blobs/` con 2709 blobs, incluido el previo exacto de `SKILL.md` -> rollback por mutacion verificado.
- **Lo que YA cubria RULE-018** (20-sep): un proceso de fondo no escribe contenido de skills sin OK; y su procedimiento "si la leccion ya esta escrita, NO se escribe nada: se reporta" -> aplicado: el curador habia escrito la leccion ~40 s antes (referencia nueva + puntero, sin bloque aditivo), asi que NO se duplico.
- **Lo NUEVO (2)**: (a) escala (51 ops / 7 skills en un dia, frente a 16 en 4 h / 4 skills el 20-sep); (b) el cortafuegos que cita RULE-018 no aplica: `.curator_state` con `paused: true` desde el 23-sep y las escrituras continuan; el criterio efectivo es `created_by` (curator-managed escribe; user-owned se rechaza con `the skill is not curator-managed (created_by=None)`).
- **Limite**: no se ha medido si el curador PRESERVA lo escrito a mano por el agente; y no se ha probado si `pause` detendria el pase por turno (experimento pendiente, requiere OK).
- **Efecto colateral**: el md5/tamaño de la skill que cita la entrada de hoy mas arriba quedo obsoleto a las 16:15:08 (la reescribio el curador). Se deja como estaba (era correcto al medirlo) y se hace constar aqui.
- **Detalle completo**: `{OBS}`.
- **Escrito por**: agente (Hermes) a peticion del usuario. Nada de este bloque es obra del curador.
"""

err = []
pre_txt = DEST.read_text(encoding="utf-8")
pre = pre_txt.splitlines()
print("== 0. destino ==")
print("fichero: %d B, %d lineas, md5 %s" % (len(DEST.read_bytes()), len(pre), hashlib.md5(DEST.read_bytes()).hexdigest()))
if MARCA in pre_txt:
    err.append("la MARCA %s YA esta en el fichero (idempotencia)" % MARCA)
if not (REPO / OBS).exists() and APPLY:
    err.append("el OBS citado no existe todavia: %s" % OBS)
nuevas = bloque.splitlines()
print("== 1. bloque ==")
print("  %d lineas nuevas | marca: %s" % (len(nuevas), MARCA))
if len(nuevas) < 10: err.append("bloque sospechosamente corto")
for frag in ("MARCA: " + MARCA, OBS, "actor: curator", "paused: true", "not curator-managed"):
    if frag not in bloque: err.append("falta en el bloque: %s" % frag)
print("== 2. el OBS citado ==")
print("  existe:", (REPO / OBS).exists())
if err:
    print("\nGATE FAIL-CLOSED: %d fallo(s), NO se escribe nada:" % len(err))
    for e in err: print("  -", e)
    sys.exit(1)

nuevo_txt = pre_txt if pre_txt.endswith("\n") else pre_txt + "\n"
nuevo_txt += bloque.lstrip("\n")
nuevo = nuevo_txt.splitlines()
print("== 3. prediccion ==")
print("  antes: %d lineas | despues: %d lineas (+%d)" % (len(pre), len(nuevo), len(nuevo) - len(pre)))
# ninguna linea previa se pierde, y en el mismo orden
i = 0
for ln in nuevo:
    if i < len(pre) and ln == pre[i]: i += 1
print("  lineas previas conservadas en orden: %d/%d" % (i, len(pre)))
if i != len(pre): err.append("se perderian lineas previas (%d/%d)" % (i, len(pre)))
if err:
    print("\nGATE FAIL-CLOSED: %d fallo(s), NO se escribe nada:" % len(err))
    for e in err: print("  -", e)
    sys.exit(1)

if not APPLY:
    print("\nDRY-RUN OK. Volver a lanzar con --apply para escribir.")
    sys.exit(0)

print("== 4. copia previa ==")
bak = DEST.with_name(DEST.name + ".bak-20260930-hallazgo-curador")
if not bak.exists():
    bak.write_bytes(DEST.read_bytes())
print("  backup:", bak.name, "| %d B | md5 %s" % (len(bak.read_bytes()), hashlib.md5(bak.read_bytes()).hexdigest()))
print("  backup == estado previo:", bak.read_bytes() == DEST.read_bytes())

print("== 5. escritura ==")
DEST.write_text(nuevo_txt, encoding="utf-8")
print("  ahora: %d B, %d lineas, md5 %s" % (len(DEST.read_bytes()), len(DEST.read_text(encoding='utf-8').splitlines()), hashlib.md5(DEST.read_bytes()).hexdigest()))

print("== 6. verificacion desde disco ==")
disco = DEST.read_text(encoding="utf-8"); dl = disco.splitlines()
print("  md5 disco == predicho:", hashlib.md5(DEST.read_bytes()).hexdigest() == hashlib.md5(nuevo_txt.encode()).hexdigest())
print("  lineas:", len(dl), "| marca presente:", ("MARCA: " + MARCA) in disco)
j = 0
for ln in dl:
    if j < len(pre) and ln == pre[j]: j += 1
print("  previas intactas: %d/%d" % (j, len(pre)))
err2 = []
if len(dl) != len(nuevo): err2.append("lineas: %d != %d" % (len(dl), len(nuevo)))
if j != len(pre): err2.append("previas perdidas")
if err2:
    print("\nFALLO TRAS ESCRIBIR:"); [print("  -", e) for e in err2]; sys.exit(2)
print("\nANEXO_OK: anadido y verificado; backup %s" % bak.name)
