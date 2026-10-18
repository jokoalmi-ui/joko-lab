#!/usr/bin/env python3
"""Comprime los dumps de sesiones del lab con zstd, verificando md5 antes de
borrar cada original. Nada se borra sin comprobar que el .zst descomprime
byte a byte identico. Si la verificacion falla, se deja el .jsonl intacto.

Dos protecciones aprendidas el 16-oct-2026:
  - El log va junto a los dumps, no en /tmp (/tmp es tmpfs: se pierde al
    reiniciar y el LEEME quedaba apuntando a un fichero inexistente).
  - EXCLUIR: nunca comprime ficheros VIVOS (sesiones-acumulado.jsonl, que el
    consolidador lee y reescribe). Comprimirlo dejaria al consolidador sin
    acumulado y el historial se reconstruiria desde cero.

Directorio configurable: JOKO_SESIONES_DIR=/ruta (para probar en un sandbox)."""
import hashlib, os, subprocess, sys, time
from pathlib import Path

DIR = Path(os.environ.get("JOKO_SESIONES_DIR",
                          "/home/jokoalmi/joko-lab/04-operations/metrics/sesiones"))
EXCLUIR = {"sesiones-acumulado.jsonl"}
_base = DIR / f"compresion-dumps-{time.strftime('%Y%m%d')}"
LOG = _base.with_suffix(".log")
_n = 2
while LOG.exists():
    LOG = _base.with_name(f"{_base.name}-{_n}").with_suffix(".log")
    _n += 1


def md5_fh(fh):
    h = hashlib.md5()
    for b in iter(lambda: fh.read(8 << 20), b""):
        h.update(b)
    return h.hexdigest()


def md5_file(p):
    with open(p, "rb") as fh:
        return md5_fh(fh)


def md5_zst(p):
    pr = subprocess.Popen(["zstd", "-dc", str(p)], stdout=subprocess.PIPE)
    h = hashlib.md5()
    for b in iter(lambda: pr.stdout.read(8 << 20), b""):
        h.update(b)
    pr.stdout.close()
    if pr.wait() != 0:
        return None
    return h.hexdigest()


def main():
    files = sorted(DIR.glob("sesiones-*.jsonl"))
    if not files:
        print("nada que comprimir")
        return 0
    tot_antes = tot_despues = 0
    ok = fallos = 0
    t0 = time.time()
    lineas = []
    for f in files:
        if f.name in EXCLUIR:
            lineas.append(f"SKIP {f.name} (excluido: fichero vivo, lo lee el consolidador)")
            continue
        z = f.with_name(f.name + ".zst")
        if z.exists():
            lineas.append(f"SKIP {f.name} (ya existe {z.name})")
            continue
        antes = f.stat().st_size
        m1 = md5_file(f)
        pr = subprocess.run(["zstd", "-3", "-T0", "-q", "-f", "-o", str(z), str(f)])
        if pr.returncode != 0 or not z.exists():
            lineas.append(f"FALLO comprimiendo {f.name} (rc={pr.returncode}) — original intacto")
            fallos += 1
            continue
        m2 = md5_zst(z)
        if m1 != m2:
            z.unlink(missing_ok=True)
            lineas.append(f"FALLO md5 {f.name}: {m1} != {m2} — original intacto")
            fallos += 1
            continue
        despues = z.stat().st_size
        f.unlink()          # solo aqui, con el md5 ya verificado
        ok += 1
        tot_antes += antes
        tot_despues += despues
        lineas.append(f"OK {f.name} {antes/1e6:.0f} MB -> {despues/1e6:.0f} MB  md5={m1[:12]}")
    dur = time.time() - t0
    resumen = [
        f"Comprimidos: {ok} ficheros ({tot_antes/1e9:.2f} GB -> {tot_despues/1e9:.2f} GB, "
        f"ahorro {(tot_antes-tot_despues)/1e9:.2f} GB, ratio {(tot_antes/tot_despues if tot_despues else 0):.1f}x)",
        f"Fallos (original intacto): {fallos}",
        f"Tiempo total: {dur:.1f} s",
    ]
    LOG.write_text("\n".join(lineas + ["", *resumen]) + "\n")
    print("\n".join(resumen))
    print(f"detalle: {LOG}")
    return 0 if fallos == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
