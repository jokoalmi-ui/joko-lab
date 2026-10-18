#!/usr/bin/env python3
"""ventana_perfume.py — instrumento de Joko Lab para el "perfume del día".

PROBLEMA QUE RESUELVE (medido 20-sep-2026): la elección del perfume se decidía con
la temperatura del MOMENTO de generar la ficha (~08:18), pero el día tiene una rampa
térmica grande. Ese día en Erandio: 15,2 C a las 08:00 -> 24,9 C a las 16:00
(sensación 14,7 -> 26,1; amplitud 10,1 C real y 11,4 C de sensación). Una sola
recomendación anclada a la primera hora resulta excesiva a media tarde.

QUÉ HACE: lee el clima horario REAL de open-meteo y devuelve, para la ventana de uso
(horas en que el perfume va a estar en piel):
  - sensación térmica (apparent_temperature) min / media / max de la ventana
  - amplitud térmica del día
  - banda climática de la ventana y si la elección debe ser de rango ancho
  - dosis sugerida (sprays) para la ventana

VENTANA DE USO POR DEFECTO (08-18) — hipótesis derivada de datos medidos, no inventada:
las fichas se generan entre 05:33 y 09:32 (mtime de los PNG + `created_at` de los 12
últimos registros de uso_diario) y la primera queja por "excesivo" llegó a media tarde
(~16:30-17:00). Encaja con aplicación única a primera hora y 8-10 h en piel. La BD NO
guarda la ventana real: el sistema la aprende del cierre de la ficha
(`[VAL: ... | ventana HH-HH]`, ver skill perfume-del-dia). Revisar el default cuando
haya >=10 ventanas registradas (RULE-015).

Uso:
  python3 ventana_perfume.py [--ventana 08-18] [--lat 43.3054] [--lon -2.9754] [--json]

Solo LECTURA: no escribe en BD, ni en el lab, ni publica nada. No toca la GPU.
Fail-closed: si la API falla o la ventana no tiene datos, imprime AVISO y sale 2
(NUNCA silencio: un instrumento mudo es peor que un instrumento ausente).
Variable VENTANA_API_URL: permite apuntar a otra URL (pruebas de fallo).

UMBRALES: son HIPÓTESIS a calibrar con usos reales, NO datos validados (RULE-015).
Deben revisarse cuando haya valoraciones registradas (RULE-008 del lab).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

API_DEFECTO = "https://api.open-meteo.com/v1/forecast"
TZ = "Europe/Madrid"

# --- Umbrales (HIPÓTESIS, a calibrar; no a priori como verdad) ---
BANDAS = [  # (limite_superior_sensacion_media, banda, que buscar)
    (8.0, "frio", "ambarado / especiado calido"),
    (15.0, "fresco", "amaderado / especiado suave"),
    (22.0, "templado", "cualquiera; preferir perfil medio"),
    (27.0, "calido", "fresco citrico / acuatico"),
    (99.0, "caluroso", "acuatico / citrico ligero, baja dosis"),
]
DOSIS = [  # (limite_superior_sensacion, sprays sugeridos)
    (15.0, "3-4"),
    (20.0, "3"),
    (24.0, "2-3"),
    (27.0, "2"),
    (99.0, "1-2"),
]
UMBRAL_AMPLITUD_MEDIA = 6.0
UMBRAL_AMPLITUD_AMPLIA = 10.0


def parse_ventana(txt: str):
    """'09-19' o '09:00-19:00' -> (9, 19). inicio>fin = cruza medianoche."""
    partes = txt.replace(":", "").split("-")
    if len(partes) != 2:
        raise ValueError("ventana invalida: %r (formato HH-HH)" % txt)
    ini, fin = int(partes[0]), int(partes[1])
    if not (0 <= ini <= 23 and 0 <= fin <= 23):
        raise ValueError("ventana fuera de rango 0-23: %r" % txt)
    return ini, fin


def horas_ventana(ini: int, fin: int):
    if ini <= fin:
        return set(range(ini, fin + 1))
    return set(range(ini, 24)) | set(range(0, fin + 1))


def consulta(lat: float, lon: float, url: str):
    q = ("%s?latitude=%s&longitude=%s&hourly=temperature_2m,relative_humidity_2m,"
         "apparent_temperature,precipitation_probability&timezone=%s&forecast_days=1"
         % (url, lat, lon, TZ.replace("/", "%2F")))
    with urllib.request.urlopen(q, timeout=30) as r:
        return json.load(r)


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--ventana", default="08-18",
                    help="horas de uso en piel, formato HH-HH (defecto 08-18: hipotesis medida, ver docstring)")
    ap.add_argument("--lat", type=float, default=43.3054, help="defecto Erandio")
    ap.add_argument("--lon", type=float, default=-2.9754)
    ap.add_argument("--json", action="store_true", help="salida JSON")
    a = ap.parse_args()

    try:
        ini, fin = parse_ventana(a.ventana)
    except ValueError as e:
        print("AVISO ventana_perfume: %s" % e)
        return 2

    url = os.environ.get("VENTANA_API_URL", API_DEFECTO)
    try:
        d = consulta(a.lat, a.lon, url)
    except Exception as e:
        print("AVISO ventana_perfume: no se pudo leer el clima (%s: %s). "
              "NO emitir recomendacion anclada a una temperatura de memoria."
              % (type(e).__name__, e))
        return 2

    h = d.get("hourly") or {}
    tiempos = h.get("time") or []
    temps = h.get("temperature_2m") or []
    sens = h.get("apparent_temperature") or []
    hum = h.get("relative_humidity_2m") or []
    lluv = h.get("precipitation_probability") or []
    if not tiempos or not temps or not sens or len(sens) != len(tiempos):
        print("AVISO ventana_perfume: la API respondio sin los campos horarios "
              "esperados (claves: %s)." % sorted(h.keys()))
        return 2

    hs = horas_ventana(ini, fin)
    i_ven = [i for i, t in enumerate(tiempos) if int(t[11:13]) in hs and sens[i] is not None]
    if not i_ven:
        print("AVISO ventana_perfume: la ventana %s no tiene horas validas en la "
              "respuesta." % a.ventana)
        return 2

    sv = [sens[i] for i in i_ven]
    tv = [temps[i] for i in i_ven if temps[i] is not None]
    hv = [hum[i] for i in i_ven if i < len(hum) and hum[i] is not None]
    pv = [lluv[i] for i in i_ven if i < len(lluv) and lluv[i] is not None]
    s_dia = [s for s in sens if s is not None]
    t_dia = [t for t in temps if t is not None]

    s_min, s_med, s_max = min(sv), sum(sv) / len(sv), max(sv)
    t_min, t_max = min(t_dia), max(t_dia)
    amplitud_real = t_max - t_min
    amplitud_sens = max(s_dia) - min(s_dia)

    banda, buscar = next((b, q) for lim, b, q in BANDAS if s_med < lim)
    if amplitud_sens >= UMBRAL_AMPLITUD_AMPLIA:
        amp_banda = "amplia"
    elif amplitud_sens >= UMBRAL_AMPLITUD_MEDIA:
        amp_banda = "media"
    else:
        amp_banda = "estrecha"
    dosis = next(d for lim, d in DOSIS if s_med < lim)

    # D (20-sep-2026): dos tramos. Con amplitud no estrecha, una sola eleccion para
    # toda la ventana esconde que la manana y la tarde piden cosas distintas.
    tramos = []
    if amp_banda != "estrecha" and len(i_ven) >= 3:
        mitad = i_ven[len(i_ven) // 2]
        for nombre, idxs in (("manana", [i for i in i_ven if i < mitad]),
                             ("tarde", [i for i in i_ven if i >= mitad])):
            if not idxs:
                continue
            sv_t = [sens[i] for i in idxs]
            med_t = sum(sv_t) / len(sv_t)
            b_t, q_t = next((b, q) for lim, b, q in BANDAS if med_t < lim)
            d_t = next(d for lim, d in DOSIS if med_t < lim)
            tramos.append({
                "tramo": nombre,
                "horas": "%s-%s" % (tiempos[idxs[0]][11:13], tiempos[idxs[-1]][11:13]),
                "sens_media": round(med_t, 1),
                "banda": b_t,
                "buscar": q_t,
                "dosis": d_t,
            })

    i_tmax = max(range(len(temps)), key=lambda i: temps[i])
    i_smax = max(range(len(sens)), key=lambda i: sens[i])

    res = {
        "ventana": a.ventana,
        "coords": [a.lat, a.lon],
        "consultado": datetime.now(timezone(timedelta(hours=2))).strftime("%Y-%m-%d %H:%M:%S %Z"),
        "fuente": "open-meteo hourly apparent_temperature",
        "sens_min": round(s_min, 1),
        "sens_media": round(s_med, 1),
        "sens_max": round(s_max, 1),
        "dia_min": round(t_min, 1),
        "dia_max": round(t_max, 1),
        "hora_max": tiempos[i_tmax][11:16],
        "hora_sens_max": tiempos[i_smax][11:16],
        "amplitud_real": round(amplitud_real, 1),
        "amplitud_sensacion": round(amplitud_sens, 1),
        "humedad_media": round(sum(hv) / len(hv)) if hv else None,
        "lluvia_max": max(pv) if pv else None,
        "banda": banda,
        "buscar": buscar,
        "amplitud_banda": amp_banda,
        "dosis": dosis,
        "tramos": tramos,
    }
    if amp_banda == "amplia":
        res["regla_amplitud"] = ("evitar extremos (ni acuatico puro ni gourmand/oud); "
                                 "perfil de rango ancho y declarar tramos en la ficha")
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    print("VENTANA %s (%.4f/%.4f) · fuente: open-meteo · %s"
          % (a.ventana, a.lat, a.lon, res["consultado"]))
    print("sensacion ventana: min %.1f | MEDIA %.1f | max %.1f"
          % (s_min, s_med, s_max))
    print("dia: min %.1f (%s) | max %.1f (%s) | amplitud %.1f C | amplitud sensacion %.1f C"
          % (t_min, tiempos[min(range(len(temps)), key=lambda i: temps[i])][11:16],
             t_max, res["hora_max"], amplitud_real, amplitud_sens))
    print("humedad ventana: %s%% | lluvia max: %s%%"
          % (res["humedad_media"], res["lluvia_max"]))
    print("BANDA: %s (sensacion media %.1f) -> buscar %s" % (banda, s_med, buscar))
    print("AMPLITUD: %s -> %s" % (amp_banda, res.get("regla_amplitud", "una eleccion unica vale")))
    print("DOSIS sugerida: %s sprays (si la tarde supera %.1f, bajar un escalon)"
          % (dosis, s_max))
    for t in tramos:
        print("TRAMO %s (%s): sensacion media %.1f -> buscar %s | %s sprays"
              % (t["tramo"], t["horas"], t["sens_media"], t["buscar"], t["dosis"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
