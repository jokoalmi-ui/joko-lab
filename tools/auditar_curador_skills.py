#!/usr/bin/env python3
"""Auditoria forense del curador de skills (Joko Lab) -- SOLO LECTURA.

Reconstruye que escribio el curador de fondo en ~/.hermes/skills/ durante una
ventana de tiempo, a partir de las dos fuentes de verdad:

  1. ~/.hermes/skills/.curator_ledger.jsonl  (id, ts UTC, actor, action, skill,
     before[], after[], evidence{session_id, file_path})
  2. ~/.hermes/cache/spillover/*.txt         (volcados intermedios del curador,
     con el contenido que iba a escribir y su mtime)

Uso tipico:
  python3 tools/auditar_curador_skills.py                    # ultimas 6 horas
  python3 tools/auditar_curador_skills.py --horas 48
  python3 tools/auditar_curador_skills.py --desde "2026-09-30 14:00"   # hora local
  python3 tools/auditar_curador_skills.py --skill edicion-aditiva-registros
  python3 tools/auditar_curador_skills.py --diff <spillover.txt> --skill <nombre>
  python3 tools/auditar_curador_skills.py --salida /tmp/forense.txt

No escribe NADA dentro de ~/.hermes/: las skills solo se leen (bytes, lineas,
md5, mtime). El volcado se imprime o se escribe en --salida (por defecto /tmp).

Por que existe: el `[session_id]` que el log del CLI pone delante de
`tool skill_manage completed` es el de la SESION que ejecuta, y el curador usa
el mismo ejecutor, asi que ese id NO identifica al autor. La autoria real esta
en el campo `actor` de este ledger.
"""
from __future__ import annotations

import argparse
import difflib
import glob
import hashlib
import json
import os
import re
import time
from datetime import datetime, timedelta, timezone

SKILLS = "/home/jokoalmi/.hermes/skills"
LEDGER = os.path.join(SKILLS, ".curator_ledger.jsonl")
SPILLOVER = "/home/jokoalmi/.hermes/cache/spillover"

L: list[str] = []


def p(*a) -> None:
    L.append(" ".join(str(x) for x in a))


def ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


def cortes(args) -> tuple[datetime, datetime]:
    """Devuelve (desde, hasta) en UTC."""
    hasta = ahora_utc()
    if args.desde:
        d = datetime.strptime(args.desde, "%Y-%m-%d %H:%M").astimezone(timezone.utc)
        return d, hasta
    return hasta - timedelta(hours=args.horas), hasta


def leer_ledger() -> list[dict]:
    filas = []
    with open(LEDGER, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                filas.append(json.loads(ln))
    return filas


def ts_de(fila: dict) -> datetime | None:
    t = fila.get("ts")
    if not t:
        return None
    try:
        return datetime.fromisoformat(t)
    except ValueError:
        return None


def loc(dt: datetime) -> str:
    return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S")


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def payload(path: str) -> str:
    """Extrae el texto del volcado del curador (JSON con content/text/result/body, o crudo)."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    try:
        j = json.loads(raw)
        if isinstance(j, dict):
            for k in ("content", "text", "result", "body"):
                if isinstance(j.get(k), str):
                    return j[k]
    except Exception:
        pass
    return raw


def ruta_de_skill(nombre: str, sub: str | None = None) -> str | None:
    hits = glob.glob(os.path.join(SKILLS, "**", nombre, "SKILL.md"), recursive=True)
    if not hits:
        return None
    ruta = os.path.dirname(hits[0])
    return os.path.join(ruta, sub) if sub else os.path.join(ruta, "SKILL.md")


def sec_ledger(filas: list[dict], desde: datetime, hasta: datetime, skill: str | None) -> list[dict]:
    p("=== 1. LEDGER DEL CURADOR ===")
    p(f"fichero: {LEDGER}")
    p(f"filas totales: {len(filas)}  |  ventana: {loc(desde)} -> {loc(hasta)} (hora local)")
    vent = [f for f in filas if (t := ts_de(f)) and desde <= t <= hasta]
    if skill:
        vent = [f for f in vent if f.get("skill") == skill]
    if not vent:
        p("  (sin operaciones en la ventana)")
        return vent

    por_actor: dict[str, int] = {}
    por_skill: dict[str, int] = {}
    por_sesion: dict[str, int] = {}
    for f in vent:
        por_actor[f.get("actor", "?")] = por_actor.get(f.get("actor", "?"), 0) + 1
        por_skill[f.get("skill", "?")] = por_skill.get(f.get("skill", "?"), 0) + 1
        sid = (f.get("evidence") or {}).get("session_id", "?")
        por_sesion[sid] = por_sesion.get(sid, 0) + 1

    p(f"operaciones en la ventana: {len(vent)}")
    p("  por actor:  " + " · ".join(f"{k}={v}" for k, v in sorted(por_actor.items(), key=lambda x: -x[1])))
    p("  por skill:  " + " · ".join(f"{k}={v}" for k, v in sorted(por_skill.items(), key=lambda x: -x[1])))
    p("  por sesion: " + " · ".join(f"{k}={v}" for k, v in sorted(por_sesion.items(), key=lambda x: -x[1])))
    p("")
    p("  detalle (hora local | actor | action | skill | fichero | id):")
    for f in vent:
        ev = f.get("evidence") or {}
        t = ts_de(f)
        p("   ", loc(t) if t else "-", "|", f.get("actor", "?"), "|", f.get("action", "?"), "|",
          f.get("skill", "?"), "|", ev.get("file_path", "-"), "|", f.get("id", "?"))
    return vent


def sec_spillover(desde: datetime, hasta: datetime) -> None:
    p("")
    p("=== 2. VOLCADOS INTERMEDIOS (spillover) ===")
    p(f"directorio: {SPILLOVER}")
    if not os.path.isdir(SPILLOVER):
        p("  (no existe)")
        return
    cutoff = desde.timestamp()
    fin = hasta.timestamp()
    ficheros = [f for f in glob.glob(os.path.join(SPILLOVER, "*.txt")) if cutoff <= os.path.getmtime(f) <= fin]
    ficheros.sort(key=os.path.getmtime)
    p(f"ficheros en la ventana: {len(ficheros)}")
    for f in ficheros:
        raw = open(f, encoding="utf-8", errors="replace").read()
        m = re.findall(r'name="([a-z0-9_\-/]+)"', raw[:4000]) or re.findall(r"'name':\s*'([^']+)'", raw[:4000])
        cabeza = raw[:140].replace("\n", " ")
        p("-", os.path.basename(f), "| mtime", time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(f))),
          "| bytes", len(raw), "| skill?", (m[0] if m else "?"), "| head:", cabeza)


def sec_estado(vent: list[dict]) -> None:
    p("")
    p("=== 3. ESTADO EN DISCO DE LO TOCADO EN LA VENTANA ===")
    vistas: dict[str, set[str]] = {}
    for f in vent:
        nombre = f.get("skill")
        if nombre:
            vistas.setdefault(nombre, set()).add((f.get("evidence") or {}).get("file_path", "") or "SKILL.md")
    if not vistas:
        p("  (nada que medir)")
        return
    for nombre, subs in sorted(vistas.items()):
        for sub in sorted(subs):
            ruta = ruta_de_skill(nombre, None if sub in ("", "SKILL.md") else sub)
            if not ruta or not os.path.exists(ruta):
                p("-", nombre, sub, "| NO ENCONTRADO")
                continue
            st = os.stat(ruta)
            lineas = sum(1 for _ in open(ruta, encoding="utf-8", errors="replace"))
            p("-", ruta.replace(SKILLS + "/", ""), "| bytes", st.st_size, "| lineas", lineas,
              "| sha256", sha256(ruta)[:16] + "...", "| mtime", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)))


def sec_diff(spill: str, skill: str, sub: str | None) -> None:
    p("")
    p("=== 4. DIFF: volcado del curador vs fichero ACTUAL ===")
    ruta = ruta_de_skill(skill, sub)
    if not ruta or not os.path.exists(ruta):
        p("  (skill no encontrada:", skill, ")")
        return
    a = payload(spill).splitlines()
    b = open(ruta, encoding="utf-8", errors="replace").read().splitlines()
    p(f"volcado: {spill}  ({os.path.getsize(spill)} B, mtime {time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(spill)))})")
    p(f"actual : {ruta}  ({os.path.getsize(ruta)} B, mtime {time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(ruta)))})")
    d = list(difflib.unified_diff(a, b, fromfile="volcado_curador", tofile="actual", lineterm="", n=1))
    add = [x for x in d if x.startswith("+") and not x.startswith("+++")]
    p(f"lineas de diff: {len(d)}  |  lineas anadidas: {len(add)}")
    for ln in d[:200]:
        p("   ", ln[:300])
    if not d:
        p("  (sin diferencias: el volcado coincide con el fichero actual)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Auditoria forense del curador de skills (solo lectura)")
    ap.add_argument("--horas", type=float, default=6.0, help="ventana hacia atras en horas (por defecto 6)")
    ap.add_argument("--desde", help='inicio explicito en hora LOCAL, formato "YYYY-MM-DD HH:MM"')
    ap.add_argument("--skill", help="limitar el informe a una skill")
    ap.add_argument("--diff", dest="spill", help="volcado del curador a comparar con el fichero actual")
    ap.add_argument("--sub", help="ruta relativa dentro de la skill para --diff (p. ej. references/x.md)")
    ap.add_argument("--salida", help="fichero de salida (por defecto: stdout)")
    args = ap.parse_args()

    desde, hasta = cortes(args)
    p(f"# Auditoria del curador de skills | generado {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    p("")
    filas = leer_ledger()
    vent = sec_ledger(filas, desde, hasta, args.skill)
    sec_spillover(desde, hasta)
    sec_estado(vent)
    if args.spill:
        sec_diff(args.spill, args.skill or "", args.sub)

    texto = "\n".join(L) + "\n"
    if args.salida:
        open(args.salida, "w", encoding="utf-8").write(texto)
        print(f"OK -> {args.salida} ({len(L)} lineas)")
    else:
        print(texto, end="")


if __name__ == "__main__":
    main()
