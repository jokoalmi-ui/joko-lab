#!/usr/bin/env python3
"""monitor_tg.py — Vigila canales de TELEGRAM con vista web pública (A, 09-oct-2026).

Lee https://t.me/s/<usuario> (vista web pública, sin login ni token), compara con el
estado previo e imprime SOLO las publicaciones nuevas. Vacío = silencio (patrón
watchdog, apto para cron no_agent). Mismo patrón que tools/monitor_yt.py.

Primera ejecución de un canal: se registra su histórico visible SIN imprimirlo
(evita inundar Telegram con las ~20 publicaciones ya existentes).

Canales habilitados: SOLO los que tienen vista web pública, comprobado con curl el
09-oct-2026 (HTTP real, no supuesto):
    techwith_ram  -> 200 (128.187 B)  -> VÁLIDO
    jugaldb       -> 302 -> https://t.me/jugaldb       (sin vista web)
    dailydoseofds -> 302 -> https://t.me/dailydoseofds (sin vista web)
Los que devuelven 302 NO se pueden vigilar por esta vía: quedan documentados abajo.

USO:
    python3 monitor_tg.py            # comprueba y muestra lo nuevo (si lo hay)
    python3 monitor_tg.py --check    # solo estado (no modifica nada)
    python3 monitor_tg.py --reset    # marca lo actual como visto

State: ~/.hermes/state/monitor_tg_state.json  {usuario/mensaje: {canal, fecha, texto}}
"""
import argparse
import html as html_mod
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

# usuario de Telegram -> nombre visible
CANALES = {
    "techwith_ram": "Techwith Ram",
}
# Medidos el 09-oct-2026 y NO vigilables por t.me/s (302 = sin vista web pública):
#   "jugaldb", "dailydoseofds"

STATE_FILE = Path(os.path.expanduser("~/.hermes/state/monitor_tg_state.json"))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
MAX_TEXTO = 300


def _fetch(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def _parse_posts(pagina: str) -> list:
    """Extrae [{id, fecha, texto}] de la vista web pública de un canal."""
    posts = []
    for bloque in re.split(r'(?=<div class="tgme_widget_message[ "])', pagina):
        m = re.search(r'data-post="([^"]+)"', bloque)
        if not m:
            continue
        f = re.search(r'<time datetime="([^"]+)"', bloque)
        texto = ""
        t = re.search(
            r'class="tgme_widget_message_text[^"]*"[^>]*>(.*?)'
            r'(?:<div class="tgme_widget_message_(?:footer|reply_markup)|</div></div>)',
            bloque, re.S)
        if t:
            texto = re.sub(r"<br\s*/?>", " ", t.group(1))
            texto = re.sub(r"<[^>]+>", " ", texto)
            texto = html_mod.unescape(texto)
            texto = re.sub(r"\s+", " ", texto).strip()
        posts.append({"id": m.group(1), "fecha": f.group(1) if f else "", "texto": texto})
    return posts


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
    ap = argparse.ArgumentParser(description="Monitor de canales de Telegram del lab")
    ap.add_argument("--reset", action="store_true", help="marca lo actual como visto")
    ap.add_argument("--check", action="store_true", help="solo estado, no modifica")
    ap.add_argument("--max-edad-dias", type=int, default=0,
                    help="ignora publicaciones más viejas que N días (0 = sin límite)")
    args = ap.parse_args()

    state = _cargar_state()
    canales_previos = {v.get("canal") for v in state.values() if isinstance(v, dict)}
    nuevos, primera_vez, errores = [], {}, []

    for usuario, nombre in CANALES.items():
        try:
            pagina = _fetch(f"https://t.me/s/{usuario}")
        except Exception as e:
            errores.append(f"{usuario}: {str(e)[:80]}")
            continue
        posts = _parse_posts(pagina)
        if not posts:
            errores.append(f"{usuario}: vista web sin publicaciones (¿canal sin vista pública?)")
            continue
        for p in posts:
            if p["id"] in state:
                continue
            if args.max_edad_dias and p["fecha"]:
                try:
                    from datetime import datetime, timezone
                    pub = datetime.fromisoformat(p["fecha"])
                    if (datetime.now(timezone.utc) - pub).days > args.max_edad_dias:
                        continue
                except Exception:
                    pass
            entrada = {"canal": nombre, "fecha": p["fecha"], "texto": p["texto"][:MAX_TEXTO]}
            if nombre not in canales_previos:
                primera_vez[nombre] = primera_vez.get(nombre, 0) + 1
            else:
                nuevos.append({"id": p["id"], "canal": nombre, **entrada})
            if not args.check and not args.reset:
                state[p["id"]] = entrada

    if args.check:
        por_canal = {}
        for v in state.values():
            por_canal[v.get("canal", "?")] = por_canal.get(v.get("canal", "?"), 0) + 1
        print(f"State: {len(state)} publicaciones vistas " + json.dumps(por_canal, ensure_ascii=False))
        for e in errores:
            print(f"  ERROR {e}")
        return 0

    if args.reset:
        for usuario, nombre in CANALES.items():
            try:
                for p in _parse_posts(_fetch(f"https://t.me/s/{usuario}")):
                    state[p["id"]] = {"canal": nombre, "fecha": p["fecha"], "texto": p["texto"][:MAX_TEXTO]}
            except Exception as e:
                errores.append(f"{usuario}: {str(e)[:60]}")
        _guardar_state(state)
        print(f"Reset: {len(state)} publicaciones marcadas como vistas.")
        return 0

    for nombre, n in primera_vez.items():
        print(f"[TG {nombre}] primera vez: {n} publicaciones registradas como vistas (sin novedades).")
    for n in nuevos:
        print(f"[TG {n['canal']}] {n['fecha'][:10]}")
        print(f"  https://t.me/{n['id']}")
        if n["texto"]:
            print(f"  {n['texto'][:MAX_TEXTO]}")
    for e in errores:
        print(f"[ERROR TG] {e}")

    _guardar_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
