#!/usr/bin/env python3
"""Sondeo de tiendas ES de perfume/decants: capa de colaboradores y redes.
Solo lectura, robots.txt respetado, UA de navegador, salida a /tmp/pafory-es/."""
import re, pathlib, urllib.robotparser, urllib.request, urllib.parse, json

D = pathlib.Path("/tmp/pafory-es"); D.mkdir(exist_ok=True)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

SITES = {
    "decants.es": "https://decants.es/",
    "oasisparadise.es": "https://www.oasisparadise.es/",
    "decantsperfumespain.com": "https://www.decantsperfumespain.com/",
    "lesecretdumarais.es": "http://www.lesecretdumarais.es/",
    "nadiaperfumeria.com": "https://www.nadiaperfumeria.com/",
    "arabicparfums.es": "https://www.arabicparfums.es/",
    "anyaperfumes.es": "https://anyaperfumes.es/",
    "ponsaparfums.com": "https://ponsaparfums.com/",
}

SIGNAL = re.compile(r"(colabora\w*|afiliad\w*|embajador\w*|influencer\w*|creador\w*|"
                    r"partner\w*|programa|club\s|recomienda|c[oó]digo\s+descuento|"
                    r"cup[oó]n|sorteo|nano|micro)", re.I)
SOCIAL = re.compile(r"https?://(?:www\.)?(instagram\.com|tiktok\.com|youtube\.com|facebook\.com)/[A-Za-z0-9_.\-/@]*")
LINK = re.compile(r'href="([^"]+)"')

def get(url, timeout=25):
    rq = urllib.request.Request(url, headers={"User-Agent": UA,
         "Accept-Language": "es-ES,es;q=0.9", "Accept": "text/html,*/*"})
    with urllib.request.urlopen(rq, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "ignore")

rows = []
for name, url in SITES.items():
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(urllib.parse.urljoin(url, "/robots.txt"))
        try:
            rp.read()
            allowed = rp.can_fetch(UA, url)
        except Exception:
            allowed = True  # robots ausente
        if not allowed:
            rows.append((name, "robots_disallow", 0, "", "", "", "")); continue
        st, html = get(url)
        txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
        txt = re.sub(r"<[^>]+>", " ", txt)
        txt = re.sub(r"\s+", " ", txt)
        title = (re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I) or [None, ""])[1]
        title = re.sub(r"\s+", " ", title)[:90].strip()
        # rutas internas con pinta de programa de colaboradores
        paths = set()
        for h in LINK.findall(html):
            low = h.lower()
            if any(k in low for k in ("colabora", "afiliad", "embajador", "influencer", "partner", "creador", "programa")):
                paths.add(h[:110])
        socials = sorted({m.group(0).rstrip("/") for m in SOCIAL.finditer(html)})
        hits = sorted({m.group(0).lower() for m in SIGNAL.finditer(txt)})
        (D / f"{name}.txt").write_text(txt[:120000], encoding="utf-8")
        rows.append((name, st, len(html), title, " | ".join(sorted(paths))[:220],
                     " | ".join(socials)[:220], ", ".join(hits)[:220]))
    except Exception as e:
        rows.append((name, f"ERROR {type(e).__name__}: {e}"[:70], 0, "", "", "", ""))

print(f"{'sitio':26s} {'HTTP':6s} {'bytes':>7s}  titulo / rutas_programa / redes / señales")
for r in rows:
    print(f"{r[0]:26s} {str(r[1]):6s} {r[2]:7d}  {r[3][:60]}")
    print(f"    rutas: {r[4] or '(ninguna)'}")
    print(f"    redes: {r[5] or '(ninguna)'}")
    print(f"    señales: {r[6] or '(ninguna)'}")
(D / "resumen.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
