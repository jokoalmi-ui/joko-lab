#!/usr/bin/env python3
"""serie_estado.py — seguimiento de publicacion de la serie (curso IA/agentes).

Fuente unica: seguimiento.json   Vista legible generada: SEGUIMIENTO.md

Uso:
  python3 serie_estado.py                     estado + avisos
  python3 serie_estado.py md                  regenera SEGUIMIENTO.md
  python3 serie_estado.py siguiente           que toca producir ahora
  python3 serie_estado.py set <id> <estado>   cambia estado (backup previo)
  python3 serie_estado.py verificacion <id> [--fecha AAAA-MM-DD]
  python3 serie_estado.py publicar <id> --url URL [--fecha AAAA-MM-DD]
  python3 serie_estado.py nueva <id> <nivel> "<titulo>" [--tras <id_anterior>]

Reglas del lab que el script vigila (no son invento: guion maestro 01-sep):
  cadencia lunes+miercoles+viernes (3/semana) - colchon de 3 - verificacion visual antes de publicar
  - publicacion manual (nada sale solo) - no publicar cifra sin fuente.
"""
import json, sys, shutil, argparse, datetime, os

BASE = os.path.dirname(os.path.abspath(__file__))
JSON = os.path.join(BASE, "seguimiento.json")
MD = os.path.join(BASE, "SEGUIMIENTO.md")
ORDEN = ["idea", "guion", "arte", "render", "verificado", "publicado"]


def cargar():
    with open(JSON, encoding="utf-8") as f:
        return json.load(f)


def guardar(d):
    shutil.copy2(JSON, JSON + ".bak-" + datetime.date.today().isoformat())
    with open(JSON, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def hoy():
    return datetime.date.today().isoformat()


def busca(d, pid):
    for p in d["piezas"]:
        if p["id"] == pid:
            return p
    sys.exit("id no existe: " + pid)


def avisos(d):
    a = []
    pubs = [p for p in d["piezas"] if p["estado"] == "publicado"]
    for p in d["piezas"]:
        if p["estado"] == "publicado" and not (p.get("url") and p.get("fecha_publicacion")):
            a.append("[FALTA DATO] %s esta publicada sin url/fecha" % p["id"])
        if p["estado"] == "publicado" and not p.get("verificado_visual"):
            a.append("[REGLA-9] %s publicada sin verificacion visual registrada" % p["id"])
        if p["estado"] in ("render", "verificado") and not p.get("verificado_visual") and p["estado"] == "verificado":
            a.append("[INCOHERENCIA] %s marcada verificada pero verificado_visual=false" % p["id"])
        if p.get("gancho_a") and p["gancho_a"] not in [q["id"] for q in d["piezas"]]:
            a.append("[HILO ROTO] %s apunta a %s, que no existe" % (p["id"], p["gancho_a"]))
    if pubs:
        ult = max(p["fecha_publicacion"] for p in pubs)
        dias = (datetime.date.today() - datetime.date.fromisoformat(ult)).days
        if dias > d.get("cadencia_dias", 7):
            a.append("[CADENCIA] %d dias desde la ultima publicacion (%s); la cadencia es %s" % (dias, ult, d.get("cadencia_texto") or ("1 pieza cada %d dias" % d.get("cadencia_dias", 7))))
    colchon = [p for p in d["piezas"] if p["estado"] in ("verificado",) and not p.get("fecha_publicacion")]
    if len(colchon) < d.get("colchon_minimo", 2):
        a.append("[COLCHON] %d pieza(s) listas sin publicar; el minimo del lab es %d" % (len(colchon), d.get("colchon_minimo", 2)))
    for p in d["piezas"]:
        obj = p.get("objetivo")
        if obj and p["estado"] != "publicado" and datetime.date.fromisoformat(obj) <= datetime.date.today():
            a.append("[CALENDARIO] %s tenia objetivo %s y sigue en '%s'" % (p["id"], obj, p["estado"]))
    prox = d.get("proxima_publicacion")
    if prox and datetime.date.fromisoformat(prox) < datetime.date.today() and not pubs:
        a.append("[CALENDARIO] fecha prevista %s ya pasada" % prox)
    return a


def tabla(d):
    L = []
    for p in d["piezas"]:
        L.append("%-5s | n%s | %-11s | %-3s | %s" % (
            p["id"], p["nivel"], p["estado"],
            "si" if p.get("verificado_visual") else "--",
            (p["url"] or p["titulo"])[:70]))
    return L


def escribe_md(d):
    hoy_ = hoy()
    L = ["---", 'title: "SEGUIMIENTO — %s"' % d["serie"], "type: research", "---", "",
         "# SEGUIMIENTO DE PUBLICACIÓN — %s" % d["serie"], "",
         "Generado por `serie_estado.py md` el %s. **Fuente de datos: `seguimiento.json`** (no editar este .md a mano)." % hoy_, "",
         "Canal: **%s** · Cadencia: %s · Colchón mínimo: %d" % (d["canal_principal"], d.get("cadencia_texto") or ("1 pieza cada %d días" % d["cadencia_dias"]), d["colchon_minimo"]), "",
         "## Piezas", "", "| id | nivel | título | estado | verificado visual | publicada | url |",
         "|---|---|---|---|---|---|---|"]
    for p in d["piezas"]:
        L.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            p["id"], p["nivel"], p["titulo"], p["estado"],
            "sí" if p.get("verificado_visual") else "—",
            p.get("fecha_publicacion") or "—", p.get("url") or "—"))
    L += ["", "Estados: " + " → ".join(ORDEN), ""]
    av = avisos(d)
    L += ["## Avisos (%d)" % len(av), ""] + (["- " + x for x in av] if av else ["Ninguno."]) + [""]
    L += ["## Notas por pieza", ""]
    for p in d["piezas"]:
        if p.get("notas") or p.get("objetivo"):
            pre = ("(objetivo %s) " % p["objetivo"]) if p.get("objetivo") else ""
            pre += ("(doc: %s) " % p["titulo_documento"]) if p.get("titulo_documento") else ""
            L.append("- **%s** — %s%s" % (p["id"], pre, p.get("notas") or ""))
    L += ["", "## Bitácora", ""]
    for b in d["bitacora"][-20:]:
        L.append("- %s — %s" % (b["fecha"], b["detalle"]))
    L += ["", "## Cómo se registra la publicación", "",
          "La publicación es MANUAL (la hace Joseba). Cuando el post esté arriba, se registra:", "",
          "```bash", "python3 serie_estado.py publicar <id> --url <url-del-post>", "```", "", "Ejecutar el script desde su carpeta (research/infografias/serie-ia-agentes/)."]
    open(MD, "w", encoding="utf-8").write("\n".join(L) + "\n")
    return MD


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="estado")
    ap.add_argument("args", nargs="*")
    ap.add_argument("--url"); ap.add_argument("--fecha"); ap.add_argument("--tras"); ap.add_argument("--objetivo")
    ns = ap.parse_args()
    d = cargar()
    if ns.cmd == "estado":
        for l in tabla(d): print(l)
        av = avisos(d)
        print("\nAVISOS (%d):" % len(av))
        for x in av: print("  - " + x)
    elif ns.cmd == "md":
        print("escrito: " + escribe_md(d))
    elif ns.cmd == "siguiente":
        for p in d["piezas"]:
            if p["estado"] != "publicado":
                print("SIGUIENTE: %s (nivel %s) — %s [estado: %s]" % (p["id"], p["nivel"], p["titulo"], p["estado"]))
                break
    elif ns.cmd == "set":
        pid, est = ns.args[0], ns.args[1]
        if est not in ORDEN: sys.exit("estado invalido. Validos: " + ", ".join(ORDEN))
        p = busca(d, pid); p["estado"] = est
        guardar(d); escribe_md(cargar())
        print("%s -> %s" % (pid, est))
    elif ns.cmd == "verificacion":
        pid = ns.args[0]; f = ns.fecha or hoy()
        p = busca(d, pid) if False else busca(d, pid)
        p["verificado_visual"] = True; p["fecha_verificacion"] = f
        if ORDEN.index(p["estado"]) < ORDEN.index("verificado"): p["estado"] = "verificado"
        guardar(d); escribe_md(cargar()); print("%s verificada (%s)" % (pid, f))
    elif ns.cmd == "publicar":
        pid = ns.args[0]; f = ns.fecha or hoy()
        if not ns.url: sys.exit("hace falta --url (la publicacion es manual y se registra con su url)")
        p = busca(d, pid)
        if not p.get("verificado_visual"): sys.exit("REGLA-9: %s no tiene verificacion visual; no se registra como publicada" % pid)
        p.update(estado="publicado", fecha_publicacion=f, url=ns.url)
        d["bitacora"].append({"fecha": f, "accion": "publicada " + pid, "detalle": ns.url})
        guardar(d); escribe_md(cargar()); print("%s publicada %s -> %s" % (pid, f, ns.url))
    elif ns.cmd == "nueva":
        pid, nivel, titulo = ns.args[0], int(ns.args[1]), ns.args[2]
        nueva = {"id": pid, "nivel": nivel, "titulo": titulo, "tipo": "leccion", "estado": "idea",
                 "fecha_guion": None, "fecha_render": None, "fecha_verificacion": None,
                 "verificado_visual": False, "fecha_publicacion": None, "canal": d["canal_principal"],
                 "url": None, "gancho_a": None, "objetivo": ns.objetivo, "notas": ""}
        if ns.tras:
            busca(d, ns.tras)["gancho_a"] = pid
            i = [q["id"] for q in d["piezas"]].index(ns.tras); d["piezas"].insert(i + 1, nueva)
        else:
            d["piezas"].append(nueva)
        guardar(d); escribe_md(cargar()); print("nueva pieza " + pid)
    elif ns.cmd == "nota":
        pid, txt = ns.args[0], ns.args[1]
        p = busca(d, pid)
        p["notas"] = ((p.get("notas") or "") + " " + txt).strip()
        d["bitacora"].append({"fecha": hoy(), "accion": "nota " + pid, "detalle": txt})
        guardar(d); escribe_md(cargar()); print("nota anadida a " + pid)
    else:
        sys.exit("comando no reconocido: " + ns.cmd)


if __name__ == "__main__":
    main()
