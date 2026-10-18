#!/usr/bin/env python3
"""2ª pasada: buscar en los sitemaps de cada tienda páginas de colaboradores/afiliados.
Si no existen en el sitemap, no tienen el programa (o no está publicado)."""
import re, gzip, io, pathlib, urllib.request, urllib.parse, json

D = pathlib.Path("/tmp/pafory-es")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
SITES = {
    "decants.es": "https://decants.es/",
    "oasisparadise.es": "https://www.oasisparadise.es/",
    "decantsperfumespain.com": "https://www.decantsperfumespain.com/",
    "nadiaperfumeria.com": "https://www.nadiaperfumeria.com/",
    "arabicparfums.es": "https://www.arabicparfums.es/",
    "anyaperfumes.es": "https://anyaperfumes.es/",
    "ponsaparfums.com": "https://ponsaparfums.com/",
    "sillagebarcelona.com": "https://sillagebarcelona.com/",
}
KEY = re.compile(r"(colabora|afiliad|embajador|influencer|creador|partner|ambassador|"
                 r"programa|sorteo|codigo-descuento|cupon)", re.I)

def get(url, timeout=25):
    rq = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip",
        "Accept-Language": "es-ES,es;q=0.9", "Accept": "*/*"})
    with urllib.request.urlopen(rq, timeout=timeout) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            try: raw = gzip.decompress(raw)
            except Exception: pass
        return r.status, raw.decode("utf-8", "ignore"), r.geturl()

def locs(xml):
    return re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml, re.I)

out = {}
for name, url in SITES.items():
    info = {"home": url, "robots": None, "sitemaps": [], "hits": [], "n_urls": 0, "nota": ""}
    try:
        _, rob, _ = get(urllib.parse.urljoin(url, "/robots.txt"))
        info["robots"] = [l.strip() for l in rob.splitlines() if "sitemap" in l.lower()][:5]
        sms = [re.sub(r"(?i)^sitemap:\s*", "", l).strip() for l in info["robots"]]
        if not sms:
            sms = [urllib.parse.urljoin(url, "sitemap.xml")]
        seen, urls = set(), []
        for sm in sms[:3]:
            try:
                st, xml, _ = get(sm)
            except Exception as e:
                info["sitemaps"].append(f"{sm} -> ERROR {type(e).__name__}"); continue
            l0 = locs(xml)
            info["sitemaps"].append(f"{sm} -> {st} {len(l0)} locs")
            subs = [u for u in l0 if u.lower().endswith((".xml", ".xml.gz")) and u not in seen]
            if subs:
                for s2 in subs[:4]:
                    try:
                        st2, xml2, _ = get(s2)
                        l0 += locs(xml2)
                        info["sitemaps"].append(f"  {s2.split('/')[-1]} -> {st2} {len(locs(xml2))} locs")
                    except Exception as e:
                        info["sitemaps"].append(f"  {s2.split('/')[-1]} -> ERROR")
            for u in l0:
                if u not in seen:
                    seen.add(u); urls.append(u)
        info["n_urls"] = len(urls)
        info["hits"] = sorted({u for u in urls if KEY.search(u)})[:25]
        (D / f"urls_{name}.txt").write_text("\n".join(urls), encoding="utf-8")
        if not info["hits"]:
            info["nota"] = "ninguna URL con colabora/afiliado/embajador/influencer/creador/programa/cupon"
    except Exception as e:
        info["nota"] = f"ERROR {type(e).__name__}: {e}"[:120]
    out[name] = info
    print(f"== {name} == {info['nota'] or 'HITS: ' + ', '.join(h.split('/')[-1][:60] for h in info['hits'][:8])}")
    print(f"   sitemaps: {'; '.join(info['sitemaps'][:6])}  (urls totales: {info['n_urls']})")
(D / "sitemaps_resumen.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
