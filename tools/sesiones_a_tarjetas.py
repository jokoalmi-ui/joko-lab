#!/usr/bin/env python3
"""sesiones_a_tarjetas.py — Puente episodico: sesiones de Hermes -> tarjetas .md indexables.

Origen : 04-operations/metrics/sesiones/sesiones-acumulado.jsonl (1,3 GB, JSONL)
Destino: 04-operations/metrics/sesiones/tarjetas/*.md  (type: session)

Por que asi: tools/indexer.py solo indexa .md/.yaml/.yml de ~/joko-lab, asi que
las sesiones (JSONL) NUNCA entran al RAG. Una tarjeta es un resumen heuristico
LOCAL (sin LLM, coste 0) de cada sesion, con frontmatter para poder filtrar
`type: session` en la busqueda.

Uso:
  python3 sesiones_a_tarjetas.py --dry-run           # cuenta, no escribe
  python3 sesiones_a_tarjetas.py --limite 30        # muestra de 30
  python3 sesiones_a_tarjetas.py                     # todas las que pasan el filtro
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

HOME = Path.home()
LAB = HOME / "joko-lab"
ACUMULADO = LAB / "04-operations" / "metrics" / "sesiones" / "sesiones-acumulado.jsonl"
OUT_DEF = LAB / "04-operations" / "metrics" / "sesiones" / "tarjetas"

# --- redaccion de secretos y datos personales -------------------------------
PATRONES = [
    (re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}"), "[SECRETO]"),
    (re.compile(r"\b(ghp|gho|ghs|ghu)_[A-Za-z0-9]{20,}"), "[SECRETO]"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}"), "[SECRETO]"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[SECRETO]"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{5,}"), "[JWT]"),
    (re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._\-]{12,}"), r"\1 [SECRETO]"),
    (re.compile(r"(?i)\b(api[_-]?key|token|secret|password|passwd|clave|contrasena|contraseña)\b\s*[:=]\s*['\"]?[^\s'\"]{6,}"),
     r"\1: [SECRETO]"),
    (re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"), "[EMAIL]"),
    (re.compile(r"(?<!\d)(?:\+34[\s.\-]?)?[6-9]\d{2}[\s.\-]?\d{2}[\s.\-]?\d{2}[\s.\-]?\d{2}(?!\d)"), "[TELEFONO]"),
    (re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"), "[IP]"),
]
_contador: dict[str, int] = {}


def redactar(txt: str) -> str:
    for rx, rep in PATRONES:
        txt, n = rx.subn(rep, txt)
        if n:
            _contador[rx.pattern[:24]] = _contador.get(rx.pattern[:24], 0) + n
    return txt


# --- utilidades ------------------------------------------------------------
RE_COMPACT = re.compile(r"^\s*\[CONTEXT COMPACTION[^\]]*\]", re.S)
# Ruido que nunca es una peticion del usuario: handoffs de compactacion, resumenes, salidas
RUIDO = re.compile(
    r"^(?:Eres mi agente|\[CONTEXT|Earlier turns were compacted|This session is being continued|"
    r"Resumen de la conversaci|Salida cruda|\[OUT-OF-BAND|\[CONTEXT|\[System|\[STILL IN PROGRESS)|\(líneas |^\(",
    re.I)
RE_PATH = re.compile(r"(?:/home/jokoalmi|~)/[\w./\-]+\.(?:py|sh|md|json|jsonl|yaml|yml|db|js|html|css|txt|pdf|csv|sql|service|toml|cfg|ini|png)\b")
RE_TOOLREAD = re.compile(r"^\[(\w+)\]")


def limpiar(txt: str, tope: int) -> str:
    txt = (txt or "").strip()
    txt = RE_COMPACT.sub("", txt).strip()
    txt = re.sub(r"\s+", " ", txt)
    return txt[:tope]


def fecha(ts) -> str:
    try:
        return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "?"


def tarjeta(rec: dict) -> str | None:
    msgs = rec.get("messages") or []
    if not msgs:
        return None
    usuarios = [m for m in msgs if m.get("role") == "user"]
    asistentes = [m for m in msgs if m.get("role") == "assistant" and (m.get("content") or "").strip()]
    # peticiones reales: usuario, sin handoffs de compactacion, con sustancia
    peticiones: list[str] = []
    for u in usuarios:
        c = limpiar(u.get("content"), 500)
        if len(c) < 30 or RUIDO.match(c):
            continue
        if c not in peticiones:
            peticiones.append(c)
    if not peticiones:
        return None
    peticion = peticiones[0]
    posteriores = [p[:220] for p in peticiones[1:] if p[:120] != peticion[:120]][:3]

    herramientas: dict[str, int] = {}
    rutas: list[str] = []
    for m in msgs:
        if m.get("role") != "tool":
            continue
        nombre = (m.get("tool_name") or "").strip()
        if not nombre:
            mm = RE_TOOLREAD.match((m.get("content") or "").lstrip())
            nombre = mm.group(1) if mm else ""
        if nombre:
            herramientas[nombre] = herramientas.get(nombre, 0) + 1
        for p in RE_PATH.findall(str(m.get("content") or "")):
            if "/cache/scratch/" in p or p.startswith("/tmp"):
                continue
            if p not in rutas:
                rutas.append(p)

    cierre = ""
    for a in reversed(asistentes):
        c = limpiar(a.get("content"), 600)
        if len(c) < 80 or RUIDO.match(c) or "CONTEXT COMPACTION" in c:
            continue
        if "handoff from a previous context window" in c:
            continue
        cierre = c
        break

    top_tools = sorted(herramientas.items(), key=lambda kv: -kv[1])[:8]
    sid = rec.get("id") or "?"
    inicio = fecha(rec.get("started_at"))
    titulo = (rec.get("title") or "").strip()
    if len(titulo) < 8 or RUIDO.match(titulo):
        titulo = peticion[:70]
    coste = rec.get("estimated_cost_usd")
    abierta = rec.get("ended_at") is None

    fm = [
        "---",
        f"title: {json.dumps(redactar(titulo)[:120], ensure_ascii=False)}",
        "type: session",
        f"status: {'abierta' if abierta else 'cerrada'}",
        f"session_id: {sid}",
        f"fecha: {inicio}",
        f"origen: {rec.get('source') or '?'}",
        f"mensajes: {rec.get('message_count') or len(msgs)}",
        f"coste_usd: {round(float(coste), 4) if isinstance(coste, (int, float)) else 0}",
        "tags: [sesion, episodico]",
        "---",
        "",
        f"# {redactar(titulo)[:120]}",
        "",
        f"Sesión `{sid}` · {inicio} · {rec.get('source') or '?'} · "
        f"{rec.get('message_count') or len(msgs)} mensajes.",
        "",
        f"**Tema:** {redactar(titulo)[:120]}",
        "",
        "## Petición",
        "",
        redactar(peticion),
        "",
    ]
    if posteriores:
        fm += ["## Peticiones posteriores", ""] + [f"- {redactar(p)}" for p in posteriores] + [""]
    if cierre:
        fm += ["## Cómo terminó", "", redactar(cierre), ""]
    if top_tools:
        fm += ["## Herramientas", "", ", ".join(f"`{k}` ×{v}" for k, v in top_tools), ""]
    if rutas:
        fm += ["## Ficheros mencionados", ""] + [f"- `{redactar(p)}`" for p in rutas[:8]] + [""]
    return "\n".join(fm)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=0, help="maximo de tarjetas a escribir (0 = todas)")
    ap.add_argument("--min-msgs", type=int, default=10)
    ap.add_argument("--dias", type=int, default=365)
    ap.add_argument("--out", default=str(OUT_DEF))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not ACUMULADO.exists():
        print(f"[!] No existe {ACUMULADO}")
        return 1
    out = Path(args.out)
    tope = time.time() - args.dias * 86400

    vistas = validas = escritas = 0
    bytes_tot = 0
    t0 = time.time()
    with open(ACUMULADO, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            vistas += 1
            try:
                rec = json.loads(linea)
            except Exception:
                continue
            if (rec.get("message_count") or 0) < args.min_msgs:
                continue
            if (rec.get("started_at") or 0) < tope:
                continue
            texto = tarjeta(rec)
            if not texto:
                continue
            validas += 1
            if args.dry_run:
                continue
            if args.limite and escritas >= args.limite:
                continue
            out.mkdir(parents=True, exist_ok=True)
            nombre = f"{fecha(rec.get('started_at'))[:10]}_{rec.get('id')}.md"
            (out / nombre).write_text(texto, encoding="utf-8")
            escritas += 1
            bytes_tot += len(texto.encode())

    dur = round(time.time() - t0, 1)
    print(f"vistas={vistas} validas={validas} escritas={escritas} "
          f"bytes={bytes_tot} ({bytes_tot/1024:.0f} KB) destino={out} {dur}s")
    if _contador:
        print("redacciones:", ", ".join(f"{k}…×{v}" for k, v in sorted(_contador.items(), key=lambda kv: -kv[1])))
    else:
        print("redacciones: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
