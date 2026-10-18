#!/usr/bin/env python3
"""monitor_yt.py — Vigila canales de YouTube de referencia del lab (A4, 20-ago-2026).

Consulta los feeds RSS públicos de los canales consolidados del lab (skill vigilancia-canales-youtube;
la lista efectiva es SIEMPRE el dict CANALES de aquí abajo — el doc
research/canales-referencia-lab.md quedó archivado el 02-sep-2026), compara con el estado
previo (archivo de vídeos ya vistos) e imprime SOLO los nuevos. Vacío =
silencio (patrón watchdog, apto para cron no_agent).

Channel IDs verificados 20-ago-2026 con salida real (externalId del HTML del
canal — NO inventados; un ID mal puesto da 404 en el feed).

USO:
    python3 monitor_yt.py            # comprueba y muestra nuevos (si los hay)
    python3 monitor_yt.py --reset    # marca todos los actuales como vistos
    python3 monitor_yt.py --check    # solo estado (sin modificar el state)

State: ~/.hermes/state/monitor_yt_state.json  {video_id: {canal, titulo, fecha}}
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Canales de referencia del lab (consolidado 15-ago + skill youtube-content)
# + Nate Herk / Nick Saraev (02-sep, carrusel dineroalgrano — Claude Code/agentes)
# + Joaquín Ruiz / @jokioki (25-sep, canal técnico verificable — research/analisis-canal-jokiruiz-20260925.md)
# + NotFound404 / @NOTFOUND404dev (09-oct-2026, tras analizar 4 vídeos —
#   research/canal-notfound404-videos-20261009.md; ID verificado con su RSS el 09-oct)
CANALES = {
    "Nichonauta": "UCz6Mu2Iv4-gitXurg9amisw",
    "IBM Technology": "UCKWaEZ-_VweaEx1j62do_vQ",
    "Rodolfo Carrasco": "UCl_Q5EJxh9Fj73SIpErFE6g",
    "Fazt Code": "UCMn28O1sQGochG94HdlthbA",
    "hdeleon.net": "UCDUdeFslCNoM29MAlZOfdWQ",
    "Nate Herk": "UC2ojq-nuP8ceeHqiroeKhBA",
    "Nick Saraev": "UCbo-KbSjJDG6JWQ_MTZ_rNA",
    "Joaquín Ruiz": "UCnZCS1XKBTi_RpM67O3DiRg",
    "NotFound404": "UCBYcKHnzmc9nkOXCRJ0VZJQ",
}
STATE_FILE = Path(os.path.expanduser("~/.hermes/state/monitor_yt_state.json"))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"


def _fetch(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def _parse_feed(xml: str) -> list:
    """Extrae (video_id, titulo, fecha, views) de un feed RSS de YouTube."""
    videos = []
    for m in re.finditer(r"<entry>(.*?)</entry>", xml, re.S):
        e = m.group(1)
        vid = re.search(r"<yt:videoId>([^<]+)</yt:videoId>", e)
        titulo = re.search(r"<title>(.*?)</title>", e, re.S)
        fecha = re.search(r"<published>([^<]+)</published>", e)
        views = re.search(r'<media:statistics views="([0-9]+)"', e)
        if vid and titulo:
            videos.append({
                "id": vid.group(1),
                "titulo": titulo.group(1).strip(),
                "fecha": fecha.group(1) if fecha else "",
                "views": int(views.group(1)) if views else None,
            })
    return videos


def _get_suscriptores(cid: str) -> int | None:
    """Obtiene suscriptores del canal desde el HTML (patrón verificado 01-sep)."""
    try:
        html = _fetch(f"https://www.youtube.com/channel/{cid}")
    except Exception:
        return None
    m = re.search(r'"content":"([0-9][0-9.,]*)\s*([KM])?\s*suscriptores"', html)
    if not m:
        return None
    num = float(m.group(1).replace(".", "").replace(",", "."))
    if m.group(2) == "K":
        num *= 1000
    elif m.group(2) == "M":
        num *= 1_000_000
    return int(num)


def _cargar_cerrados() -> dict:
    """IDs ya cerrados (04-operations/metrics/outliers_cerrados.jsonl) -> dict id: registro.

    Un outlier cerrado NO se vuelve a imprimir por muy alto que sea su score: el
    radar recalcula sobre los vídeos actuales del canal y resucitaba piezas ya
    analizadas (Kimi K3 del 11-ago, 17-oct-2026). Fichero ausente = sin cierres.
    """
    cerrados = {}
    ruta = Path(__file__).resolve().parent.parent / "04-operations/metrics/outliers_cerrados.jsonl"
    try:
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    reg = json.loads(linea)
                except json.JSONDecodeError:
                    continue
                if isinstance(reg, dict) and reg.get("id"):
                    cerrados[reg["id"]] = reg
    except FileNotFoundError:
        pass
    return cerrados


def _detectar_outliers(videos: list, suscriptores: int | None,
                       min_views: int = 100, n_baseline: int = 15) -> list:
    """outlierScore = views ÷ mediana baseline (excluye candidato). Método Apify.

    min_views 1000 -> 100 (09-oct-2026, decidido por el usuario): con 1000 el
    filtro dejaba ciego por construcción a un canal de alcance bajo — Nichonauta
    (mediana 117 views) no aportaba ni un candidato y su max_score salía 0.0.
    Medido: con 100 sí entran candidatos, pero su máximo (526) sigue por debajo
    del corte (4,5x < 10x), así que da cobertura SIN añadir ruido al radar.
    Ajustable por CLI con --min-views.

    Calibrado 01-sep con datos reales (5 canales del lab): la condición
    "views > suscriptores" sola dispara en casi TODO canal pequeño sano
    (mediana de breakouts sub-100k = 12,89x — el discriminante real es
    outlierScore >= 10x). La condición viral queda como dato informativo,
    no como disparador.
    """
    if not videos:
        return []
    outliers = []
    for v in videos:
        if v["views"] is None or v["views"] < min_views:
            continue
        otros = [x["views"] for x in videos if x["id"] != v["id"] and x["views"]]
        if not otros:
            continue
        baseline = sorted(otros)[len(otros) // 2]
        if baseline <= 0:
            continue
        score = v["views"] / baseline
        if score >= 10:
            outliers.append({**v, "outlier_score": round(score, 1),
                             "baseline": baseline, "suscriptores": suscriptores})
    return outliers


def _cargar_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _guardar_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(STATE_FILE)


def main() -> int:
    ap = argparse.ArgumentParser(description="Monitor YouTube canales del lab")
    ap.add_argument("--reset", action="store_true", help="marca los actuales como vistos")
    ap.add_argument("--check", action="store_true", help="solo estado, no modifica")
    ap.add_argument("--outliers", action="store_true",
                    help="detecta vídeos outlier (views ÷ mediana baseline >= 10x o views > subs)")
    ap.add_argument("--max-edad-dias", type=int, default=14,
                    help="ignora vídeos más viejos que N días (por defecto 14)")
    ap.add_argument("--min-views", type=int, default=100,
                    help="views mínimas para ser candidato a outlier (por defecto 100 desde 09-oct-2026; antes 1000)")
    args = ap.parse_args()

    state = _cargar_state()
    nuevos = []
    errores = []

    for canal, cid in CANALES.items():
        try:
            xml = _fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}")
            videos = _parse_feed(xml)
            for v in videos[:5]:  # solo los 5 más recientes por canal
                if v["id"] in state:
                    continue
                # Filtrar por edad (opcional)
                if args.max_edad_dias and v["fecha"]:
                    try:
                        pub = datetime.fromisoformat(v["fecha"].replace("Z", "+00:00"))
                        edad = (datetime.now(timezone.utc) - pub).days
                        if edad > args.max_edad_dias:
                            continue
                    except Exception:
                        pass
                nuevos.append({**v, "canal": canal})
                if not args.check:
                    state[v["id"]] = {"canal": canal, "titulo": v["titulo"], "fecha": v["fecha"]}
        except Exception as e:
            errores.append(f"{canal}: {str(e)[:80]}")

    if args.check:
        total = sum(1 for _ in state) if state else 0
        print(f"State: {total} vídeos vistos | feeds OK: {len(CANALES) - len(errores)}/{len(CANALES)}")
        if errores:
            for e in errores:
                print(f"  ERROR {e}")
        return 0

    if not args.reset and nuevos:
        for n in nuevos:
            print(f"[{n['canal']}] {n['titulo']}")
            print(f"  https://youtu.be/{n['id']}  ({n['fecha'][:10]})")
    if args.reset:
        print(f"Reset: {len(nuevos)} vídeos nuevos marcados como vistos (state {len(state)}).")

    # Detección de outliers (modo --outliers): watchdog, vacío = silencio
    if args.outliers and not args.check:
        cerrados = _cargar_cerrados()
        for canal, cid in CANALES.items():
            try:
                xml = _fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}")
                videos = _parse_feed(xml)
                subs = _get_suscriptores(cid)
                outliers = _detectar_outliers(videos, subs, min_views=args.min_views)
                for o in outliers:
                    if o["id"] in cerrados:
                        continue  # cerrado en el ledger: no se reabre
                    print(f"[OUTLIER] {canal}: {o['titulo']}")
                    print(f"  https://youtu.be/{o['id']} · views={o['views']} "
                          f"(baseline {o['baseline']}) · score={o['outlier_score']}x "
                          f"· subs={o['suscriptores']}")
            except Exception as e:
                errores.append(f"{canal}: {str(e)[:80]}")

    if not args.check:
        _guardar_state(state)

    # Exit: 0 siempre (watchdog; si hay salida, el cron la entrega)
    return 0


if __name__ == "__main__":
    sys.exit(main())
