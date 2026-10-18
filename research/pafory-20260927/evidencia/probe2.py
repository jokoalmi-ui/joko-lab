import urllib.request, urllib.error, concurrent.futures

UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}

es_slugs = ['fraganceando', 'losperfumesdesilvia', 'silvia', 'antoparfums', 'anto', 'perfumesdesilvia', 'carmen', 'lucia', 'maria', 'paula', 'nuria', 'sara', 'elena', 'cristina', 'andrea', 'marta', 'irene', 'rocio', 'alba', 'daniela', 'claudia', 'isabel', 'beatriz']
found_de = ['lenisscents', 'max-aoud', 'meloshmusc', 'lubella', 'yvonne', 'tamara', 'miriam', 'swana', 'nico', 'erika', 'madametamtam', 'frankasfavorites', 'claudiswelt', 'echtkathrin', 'schikitasplace', 'thetays', 'jennyshighlights', 'maxaoud']

urls = [(f'https://pafory.com/es/inspiration/influencer/{s}', 'ES') for s in es_slugs]
urls += [(f'https://pafory.com/es/inspiration/influencer/{s}', 'ES-' + s) for s in found_de]
urls += [(f'https://pafory.com/de/inspiration/influencer/{s}', 'DE-' + s) for s in ['frankasfavorites', 'claudiswelt', 'echtkathrin', 'schikitasplace', 'thetays', 'madametamtam', 'fraganceando']]

def check(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u[0], headers=UA), timeout=25)
        return (u[1], r.status, len(r.read()))
    except urllib.error.HTTPError as e:
        return (u[1], e.code, 0)
    except Exception as e:
        return (u[1], 'ERR ' + type(e).__name__, 0)

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    res = list(ex.map(check, urls))
for label, code, size in res:
    if code == 200:
        print(f'OK   {label} ({size} bytes)')
print('--- 404/resumen ---')
print('probadas:', len(res), '| ok:', sum(1 for _, c, _ in res if c == 200))
