#!/usr/bin/env python3
"""Buscador de contactos SOLO con fuentes públicas de la propia empresa.

Reglas de diseño (no negociables):
  - Solo se leen páginas del dominio de la empresa. Nada de filtraciones, nada
    de directorios de terceros, nada de LinkedIn.
  - Solo se devuelven correos que aparecen LITERALMENTE en el HTML (incluido
    `mailto:` y la forma ofuscada `nombre (at) dominio (dot) es`).
  - No se inventan correos ni patrones. Si no hay correo publicado, la fila
    sale con `email` vacío y `motivo`.
  - Se respeta robots.txt y se espacia una petición por dominio.

Uso:
    python3 buscar_contacto_empresas.py --web https://www.uribecosta.com --nombre "Uribe Costa"
    python3 buscar_contacto_empresas.py --empresas empresas.txt
    python3 buscar_contacto_empresas.py --desde-db 40        # nombres de empleo.db
Salida: research/empleo-contactos/contactos-<fecha>.csv  +  .json
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")
CAB = {"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9,en;q=0.5"}

RUTAS = ["", "/contacto", "/contact", "/contacto/", "/aviso-legal", "/legal",
         "/politica-de-privacidad", "/trabaja-con-nosotros", "/empleo",
         "/rrhh", "/quienes-somos", "/empresa", "/about", "/es/contacto"]

RE_MAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
RE_OFUS = re.compile(
    r"([A-Za-z0-9._%+\-]+)\s*(?:\(|\[|\{)?\s*(?:at|arroba)\s*(?:\)|\]|\})?\s*"
    r"([A-Za-z0-9.\-]+)\s*(?:\(|\[|\{)?\s*(?:dot|punto)\s*(?:\)|\]|\})?\s*"
    r"([A-Za-z]{2,4})\b", re.I)
RE_HREF = re.compile(r'href=["\'](mailto:[^"\'?]+)', re.I)
RE_TAGS = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)

BASURA = ("example.com", "sentry.io", "wixpress.com", "domain.com", "email.com",
          "tudominio", "sitename", "localhost", "@2x", ".png", ".jpg", ".webp",
          ".svg", ".gif", "googlemail.com/", "sentry-next", "core.js")


def normaliza_txt(t):
    return (t or "").lower()


def trae(url, robots_cache, timeout=12):
    """GET con control de robots.txt. Devuelve (html, motivo)."""
    p = urllib.parse.urlsplit(url)
    if not p.scheme.startswith("http"):
        return None, "url_no_http"
    host = p.netloc
    if host not in robots_cache:
        robots_cache[host] = _robots_permite(p.scheme + "://" + host, p.path, robots_cache)
    if not robots_cache[host]:
        return None, "robots_prohibe"
    try:
        req = urllib.request.Request(url, headers=CAB)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            if "text/html" not in (r.headers.get("Content-Type") or ""):
                return None, "no_es_html"
            raw = r.read(1_500_000)
        try:
            return raw.decode("utf-8", "ignore"), None
        except Exception:
            return raw.decode("latin-1", "ignore"), None
    except urllib.error.HTTPError as e:
        return None, f"http_{e.code}"
    except (urllib.error.URLError, socket.timeout, ssl_error()):
        return None, "sin_conexion"
    except Exception as e:  # noqa: BLE001
        return None, f"error_{type(e).__name__}"


def ssl_error():
    import ssl
    return ssl.SSLError


def _robots_permite(base, path, cache):
    try:
        with urllib.request.urlopen(urllib.request.Request(base + "/robots.txt", headers=CAB),
                                    timeout=8) as r:
            txt = r.read(200_000).decode("utf-8", "ignore")
    except Exception:  # sin robots.txt => permitido
        return True
    bloqueado, aplica = [], False
    for ln in txt.splitlines():
        ln = ln.split("#")[0].strip()
        if not ln:
            continue
        if ln.lower().startswith("user-agent:"):
            aplica = ln.split(":", 1)[1].strip() in ("*", "Mozilla")
        elif aplica and ln.lower().startswith("disallow:"):
            d = ln.split(":", 1)[1].strip()
            if d:
                bloqueado.append(d)
    return not any(path.startswith(d) for d in bloqueado)


def limpia_html(html):
    return RE_TAGS.sub(" ", html)


def correos_de(html, dominio):
    """Correos literales del HTML, con su origen. Sin inventar."""
    out = {}
    for m in RE_HREF.finditer(html):
        e = urllib.parse.unquote(m.group(1)[7:]).strip().strip(".").lower()
        if "@" in e:
            out.setdefault(e, "mailto")
    txt = limpia_html(html)
    for m in RE_MAIL.finditer(txt):
        e = m.group(0).strip(".").lower()
        out.setdefault(e, "texto")
    for m in RE_OFUS.finditer(txt):
        e = f"{m.group(1)}@{m.group(2)}.{m.group(3)}".lower()
        out.setdefault(e, "ofuscado")
    return out


def filtra(correos, dominio):
    buenos, descartados = {}, {}
    dom_raiz = ".".join(dominio.split(".")[-2:]) if dominio else ""
    for e, via in correos.items():
        if len(e) > 90 or any(b in e for b in BASURA):
            descartados[e] = "basura_o_plantilla"
        elif not re.match(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", e):
            descartados[e] = "formato_invalido"
        else:
            buenos[e] = {"email": e, "via": via,
                         "mismo_dominio": e.split("@")[1].endswith(dom_raiz) if dom_raiz else None}
    return buenos, descartados


def tipo_de(e):
    loc = e.split("@")[0].lower()
    if any(k in loc for k in ("dpo", "gdpr", "rgpd", "privacidad", "privacy", "legal",
                              "aviso", "accessib", "cookies", "abuse", "postmaster")):
        return "legal_rgpd"
    if any(k in loc for k in ("rrhh", "empleo", "talento", "curriculum", "cv", "seleccion", "jobs", "career")):
        return "rrhh"
    if any(k in loc for k in ("info", "contacto", "hola", "admin", "ventas", "comercial", "administracion", "recepcion")):
        return "general"
    return "persona_probable" if ("." in loc or "_" in loc) else "general"


def mx(dominio):
    try:
        r = subprocess.run(["dig", "+short", "MX", dominio], capture_output=True, text=True, timeout=10)
        regs = [l.split()[-1].rstrip(".") for l in r.stdout.splitlines() if l.strip()]
        return (bool(regs), ",".join(regs[:3]))
    except Exception:  # noqa: BLE001
        return (None, "")


def enlaces_de(html, base):
    """Enlaces internos del propio dominio, con puntuación por interés."""
    host = urllib.parse.urlsplit(base).netloc.lower().removeprefix("www.")
    out = {}
    for m in re.finditer(r'href=["\']([^"\'#]{1,200})["\']', html, re.I):
        u = urllib.parse.urljoin(base + "/", m.group(1).strip())
        p = urllib.parse.urlsplit(u)
        if p.scheme not in ("http", "https") or p.netloc.lower().removeprefix("www.") != host:
            continue
        if re.search(r"\.(jpg|jpeg|png|webp|svg|gif|pdf|zip|css|js|ico|woff2?)$", p.path, re.I):
            continue
        ruta = p.path.rstrip("/") or "/"
        if ruta in out:
            continue
        low = ruta.lower()
        if re.search(r"contact|contacto|contacte|empleo|trabaja|rrhh|talento|career|job|curricul", low):
            out[ruta] = 3
        elif re.search(r"aviso|legal|privacidad|nosotros|quienes|empresa|about|empresa|empresas", low):
            out[ruta] = 1
        else:
            out[ruta] = 0
    return [r for r, _ in sorted(out.items(), key=lambda kv: -kv[1]) if r != "/"]


def urls_de_sitemap(base):
    """URLs de interés declaradas en sitemap.xml (incluido .gz)."""
    halladas = []
    for sm in ("/sitemap.xml", "/sitemap_index.xml", "/sitemap.xml.gz"):
        html, motivo = trae(base + sm, {}, timeout=10)
        if motivo:  # trae() solo acepta text/html; para XML se pide aparte
            try:
                req = urllib.request.Request(base + sm, headers=CAB)
                with urllib.request.urlopen(req, timeout=10) as r:
                    raw = r.read(1_000_000)
                if raw[:2] == b"\x1f\x8b":
                    import gzip
                    raw = gzip.decompress(raw)
                html = raw.decode("utf-8", "ignore")
            except Exception:  # noqa: BLE001
                continue
        for u in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", html or ""):
            if re.search(r"contact|empleo|trabaja|rrhh|career|job", u, re.I):
                p = urllib.parse.urlsplit(u)
                halladas.append(p.path.rstrip("/") or "/")
    return halladas[:6]


def explora(nombre, web, delay=1.0, max_paginas=8, verbose=True):
    p = urllib.parse.urlsplit(web if web.startswith("http") else "https://" + web)
    dominio = p.netloc.lower().removeprefix("www.")
    base = f"{p.scheme}://{p.netloc}"
    robots, vistos, hallados, intentos = {}, set(), {}, []
    # si el www no responde, probar el dominio raíz (muchos certificados solo cubren el apex)
    _h, _m = trae(base + "/", robots, timeout=8)
    if _m == "sin_conexion" and p.netloc.lower().startswith("www."):
        base = f"{p.scheme}://{p.netloc[4:]}"
        dominio = urllib.parse.urlsplit(base).netloc.lower()
        robots.pop(p.netloc, None)
    pendientes = list(RUTAS)  # semillas genéricas
    while pendientes and len(intentos) < max_paginas:
        ruta = pendientes.pop(0)
        url = base + ruta
        if url in vistos:
            continue
        vistos.add(url)
        html, motivo = trae(url, robots)
        intentos.append({"url": url, "motivo": motivo or "ok"})
        if html:
            for e, via in correos_de(html, dominio).items():
                hallados.setdefault(e, {"url": url, "via": via})
            for c in enlaces_de(html, base):
                if c not in pendientes and ruta in ("", "/"):
                    pendientes.insert(0, c)  # primero lo que descubre la home
            if ruta == "" and not any("sitemap" in x for x in vistos):
                pendientes = urls_de_sitemap(base) + pendientes
        time.sleep(delay)
    buenos, desc = filtra({e: d["via"] for e, d in hallados.items()}, dominio)
    mx_ok, mx_regs = mx(dominio)
    filas = []
    prioridad = {"rrhh": 0, "persona_probable": 1, "general": 2, "legal_rgpd": 3}
    for e, d in sorted(buenos.items(), key=lambda kv: (prioridad.get(tipo_de(kv[0]), 9), kv[0])):
        filas.append({
            "empresa": nombre, "dominio": dominio, "email": e,
            "tipo": tipo_de(e), "mismo_dominio": d["mismo_dominio"],
            "via": d["via"], "origen_url": hallados[e]["url"],
            "mx_ok": mx_ok, "mx_regs": mx_regs,
        })
    if not filas:
        filas.append({"empresa": nombre, "dominio": dominio, "email": "", "tipo": "",
                      "mismo_dominio": "", "via": "", "origen_url": "",
                      "mx_ok": mx_ok, "mx_regs": mx_regs,
                      "motivo": "sin correo publicado en las páginas leídas"})
    if verbose:
        print(f"[{nombre}] {dominio}: {len(filas)} fila(s), páginas ok "
              f"{sum(1 for i in intentos if i['motivo']=='ok')}/{len(intentos)}, "
              f"descartados {len(desc)}")
    return filas, intentos, desc


ATS = ("myworkdayjobs.com", "oraclecloud.com", "successfactors", "taleo", "icims",
       "greenhouse.io", "lever.co", "workable.com", "infojobs.net", "indeed.",
       "linkedin.", "glassdoor.", "springer.careers", "jobs.", "empleo.", "trabajo.",
       "computrabajo", "jobtrain", "recluta", "sepe", "lanbide", "enterprise.",
       "personio", "factorial", "teamtailor", "bamboohr", "smartrecruiters", "csod.com",
       "cornerstone", "tecnoempleo", "talentclue", "yobalia", "turijobs", "empleate",
       "aquiestaempleo", "dom6", "opositas", "buscojobs", "jobatus", "trabajastur")


def desde_db(limite):
    """Nombre + web cuando la propia oferta apunta al dominio de la empresa."""
    import sqlite3
    p = os.path.expanduser("~/empleo-seguimiento/sistema/empleo.db")
    c = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
    q = ("SELECT empresa, COUNT(*) n FROM ofertas WHERE empresa IS NOT NULL AND TRIM(empresa)<>'' "
         "GROUP BY empresa ORDER BY n DESC LIMIT ?")
    out = []
    for nombre, _n in c.execute(q, (limite,)):
        web = ""
        for (url,) in c.execute("SELECT url FROM ofertas WHERE empresa=? AND url IS NOT NULL LIMIT 5", (nombre,)):
            host = urllib.parse.urlsplit(url).netloc.lower().removeprefix("www.")
            if host and not any(a in host for a in ATS) and "." in host:
                web = "https://" + host
                break
        out.append((nombre, web))
    return out


TLD_OK = {"com", "es", "net", "org", "eu", "io", "biz", "info", "cat", "eus", "gal",
          "fr", "pt", "de", "uk", "it", "nl", "be", "mx", "ar", "cl", "co", "pe",
          "us", "ca", "online", "site", "shop", "store", "cloud", "tech", "group",
          "services", "solutions", "industries", "engineering", "systems", "energy",
          "construction", "logistics", "transport", "es.com", "com.es"}
CACHE_DOM = os.path.expanduser("~/joko-lab/research/empleo-contactos/dominios-cache.json")


def _cache_carga():
    try:
        with open(CACHE_DOM, encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return {}


def _cache_guarda(d):
    os.makedirs(os.path.dirname(CACHE_DOM), exist_ok=True)
    with open(CACHE_DOM, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)


def resuelve_dominio(nombre, verbose=True):
    """Busca el sitio oficial con DuckDuckGo lite. Sin adivinar: solo acepta un
    resultado cuyo dominio contenga el token significativo del nombre."""
    tok = re.sub(r"[^a-z0-9]", "", nombre.lower())[:14]
    if len(tok) < 3:
        return None, "nombre_demasiado_corto"
    cache = _cache_carga()
    if nombre in cache:
        return cache[nombre], None if cache[nombre] else "cache_sin_dominio"
    html = ""
    for base in ("https://html.duckduckgo.com/html/", "https://lite.duckduckgo.com/lite/"):
        for intento in range(2):
            try:
                u = base + "?q=" + urllib.parse.quote(f'"{nombre}" sitio oficial')
                req = urllib.request.Request(u, headers=CAB)
                with urllib.request.urlopen(req, timeout=15) as r:
                    html = r.read(400_000).decode("utf-8", "ignore")
                if "uddg=" in html or "result-link" in html:
                    break
            except Exception:  # noqa: BLE001
                html = ""
            time.sleep(2 + intento * 3)
        if html:
            break
    if not html:
        return None, "buscador_fallo"
    cands = re.findall(r'uddg=([^&"]+)', html)
    vistos = set()
    for c in cands:
        u = urllib.parse.unquote(c)
        if u in vistos:
            continue
        vistos.add(u)
        host = urllib.parse.urlsplit(u).netloc.lower().removeprefix("www.")
        if any(x in host for x in ("linkedin.", "facebook.", "instagram.", "infojobs.",
                                   "indeed.", "glassdoor.", "eleconomista", "wikipedia.",
                                   "youtube.", "twitter.", "x.com", "tiktok.", "duckduckgo")):
            continue
        if not re.match(r"^[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}$", host):
            continue
        if host.split(".")[-1] not in TLD_OK:
            continue
        if tok[:8] in re.sub(r"[^a-z0-9]", "", host):
            if verbose:
                print(f"  dominio resuelto: {host} (de {nombre})")
            cache[nombre] = "https://" + host
            _cache_guarda(cache)
            return u, None
    return None, "sin_dominio_que_coincida"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--web", help="URL de una sola empresa")
    ap.add_argument("--nombre", default="", help="nombre para --web")
    ap.add_argument("--empresas", help="fichero: una empresa por línea, opcional 'Nombre|https://web'")
    ap.add_argument("--desde-db", type=int, metavar="N", help="N empresas más frecuentes de empleo.db")
    ap.add_argument("--sin-buscador", action="store_true", help="no intentar resolver dominio; solo si viene en el fichero")
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--max-paginas", type=int, default=8)
    ap.add_argument("--salida-dir", default=os.path.expanduser("~/joko-lab/research/empleo-contactos"))
    a = ap.parse_args()

    lista = []
    if a.web:
        lista.append((a.nombre or urllib.parse.urlsplit(a.web).netloc, a.web))
    if a.empresas:
        with open(os.path.expanduser(a.empresas), encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if not ln or ln.startswith("#"):
                    continue
                if "|" in ln:
                    n, w = [x.strip() for x in ln.split("|", 1)]
                else:
                    n, w = ln, ""
                lista.append((n, w))
    if a.desde_db:
        lista += desde_db(a.desde_db)
    if not lista:
        ap.error("nada que buscar: usa --web, --empresas o --desde-db")

    filas, detalle = [], []
    for nombre, web in lista:
        if not web and not a.sin_buscador:
            web, err = resuelve_dominio(nombre)
            if not web:
                filas.append({"empresa": nombre, "dominio": "", "email": "", "tipo": "",
                              "mismo_dominio": "", "via": "", "origen_url": "",
                              "mx_ok": None, "mx_regs": "", "motivo": err})
                detalle.append({"empresa": nombre, "intentos": [], "descartados": {}})
                continue
        if not web:
            continue
        try:
            f, ints, desc = explora(nombre, web, a.delay, a.max_paginas)
            filas += f
            detalle.append({"empresa": nombre, "intentos": ints, "descartados": desc})
        except Exception as e:  # noqa: BLE001
            filas.append({"empresa": nombre, "dominio": "", "email": "", "tipo": "",
                          "mismo_dominio": "", "via": "", "origen_url": "",
                          "mx_ok": None, "mx_regs": "", "motivo": f"error_{type(e).__name__}"})

    os.makedirs(a.salida_dir, exist_ok=True)
    hoy = dt.date.today().isoformat()
    csv_p = os.path.join(a.salida_dir, f"contactos-{hoy}.csv")
    json_p = os.path.join(a.salida_dir, f"contactos-{hoy}.json")
    with open(csv_p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        for r in filas:
            w.writerow(r)
    with open(json_p, "w", encoding="utf-8") as f:
        json.dump({"generado": dt.datetime.now().isoformat(timespec="seconds"),
                   "empresas": len({r["empresa"] for r in filas}),
                   "filas": filas, "detalle": detalle}, f, ensure_ascii=False, indent=1)
    con_mail = [r for r in filas if r["email"]]
    print(f"\nCSV  : {csv_p}\nJSON : {json_p}")
    print(f"empresas {len({r['empresa'] for r in filas})} · con correo {len({r['empresa'] for r in con_mail})} · "
          f"correos {len(con_mail)}")
    for r in con_mail[:15]:
        print(f"  {r['empresa'][:32]:32} {r['email']:38} {r['tipo']:15} {r['origen_url']}")


if __name__ == "__main__":
    main()
