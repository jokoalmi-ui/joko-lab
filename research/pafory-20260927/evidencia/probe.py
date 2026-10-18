import json, re, html, urllib.request, concurrent.futures

UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}

t = open('/tmp/pafory/leni.html', encoding='utf-8', errors='ignore').read()
m = re.search(r'id="__NEXT_DATA__"[^>]*>(.*?)</script>', t, re.S)
print('NEXT_DATA encontrado:', bool(m))
if m:
    raw = m.group(1)
    open('/tmp/pafory/next_data.json', 'w').write(raw)
    d = json.loads(raw)
    print('len NEXT_DATA:', len(raw))
    print('top keys:', list(d.keys()))
    pp = d.get('props', {}).get('pageProps', {})
    print('pageProps keys:', list(pp.keys()))
    print('buildId:', d.get('buildId'))
    s = json.dumps(d)
    for kw in ['api.', 'influencer', 'influencers', 'strapi', 'graphql', 'cms.']:
        hits = sorted(set(re.findall(r'[\w:/.@-]{0,40}' + re.escape(kw) + r'[\w:/.@-]{0,60}', s)))[:6]
        print('KW', kw, hits)

# enlaces de las 29 landing pages antiguas
try:
    lp = json.load(open('/tmp/pafory/lp.json'))
    print('--- landingpages (29) ---')
    for it in lp:
        print(it.get('slug'), '->', it.get('link'))
except Exception as e:
    print('lp error', e)

# prueba de slugs candidatos en la ruta nueva
cands = """lenisscents schikitasplace schikitas_place frankasfavorites franka claudiswelt claudi
echtkathrin kathrin thetays tays rosa87lie jennyshighlights fruehstueck
fraganceando raulskiscents raul maxaoud max-aoud meloshmusc ameelyrose amelyrose
lidi lidiassr lubella yvonne tamara miriam hanan buonprofumo selectthescent
olfactoryambition minambery insporia niklassteenfatt addictedtomakeup jusebeauty niia jasmin xenia
angelina davisa luigi swana jamina delara peter thomas nico erika cansil""".split()
base = 'https://pafory.com/de/inspiration/influencer/'

def probe(slug):
    url = base + slug
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read().decode('utf-8', 'ignore')
            cod = re.findall(r'[Cc]ode[: ]+([A-Za-z0-9_-]{3,20})', re.sub(r'<[^>]+>', ' ', body))
            tt = re.search(r'<title>(.*?)</title>', body, re.S)
            return slug, r.status, (tt.group(1).strip()[:60] if tt else ''), ','.join(sorted(set(cod))[:3])
    except urllib.error.HTTPError as e:
        return slug, e.code, '', ''
    except Exception as e:
        return slug, 'ERR ' + str(e)[:30], '', ''

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    res = list(ex.map(probe, cands))
ok = [r for r in res if r[1] == 200]
print('--- slugs OK: %d de %d ---' % (len(ok), len(cands)))
for r in ok:
    print(r)
print('--- 404 (primeros 12) ---')
for r in [r for r in res if r[1] == 404][:12]:
    print(r[0])
