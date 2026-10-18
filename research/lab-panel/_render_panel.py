#!/usr/bin/env python3
"""PNG del panel real: nodo P0 desplegado en su solapa, y solapa de huecos.

Los dos estados se eligen con el enlace directo del generador (hash), no
manipulando clases del HTML: '#<capa>~<id>' abre la solapa y despliega el
componente; '#falt' abre la solapa de huecos. El ancla del nodo se lee de
snapshot.json; si no aparece, se captura la solapa por defecto.
"""
import json, re, subprocess
from pathlib import Path

D = Path("/home/jokoalmi/joko-lab/research/lab-panel")
SRC = D / "index.html"
SNAP = D / "snapshot.json"
RENDER = "/home/jokoalmi/joko-lab/tools/render_html.sh"  # helper unico HTML->PNG/PDF del lab

# Altos MEDIDOS a 1600 px de ancho (23-sep-2026, panel por solapas):
#   04-operations con el nodo 'gitlab' desplegado -> 990 px
#   solapa 'que falta'                            -> 1127 px
# Re-medir antes de cambiarlos: si el alto se queda corto se recorta contenido.
W, H_P0, H_FALT = 1600, 1030, 1160


def ancla_p0(pista="control de versiones"):
    """'#<capa>~<id>' del nodo insignia, leido de la instantanea real."""
    try:
        d = json.loads(SNAP.read_text(encoding="utf-8"))
    except Exception as e:
        print("aviso: no puedo leer snapshot.json:", e)
        return ""
    for c in d.get("capas", []):
        for n in c.get("nodes", []):
            if re.search(pista, n.get("t", ""), re.I):
                return f"#{c['code']}~{n['id']}"
    print(f"aviso: ningun nodo casa con /{pista}/i — capturo la solapa por defecto")
    return ""


src = SRC.read_text(encoding="utf-8")
a0 = ancla_p0()
(D / "_tmp_map.html").write_text(src, encoding="utf-8")
(D / "_tmp_falt.html").write_text(src, encoding="utf-8")

for tmp, out, h, frag in [("_tmp_map.html", "panel-mapa.png", H_P0, a0),
                          ("_tmp_falt.html", "panel-que-falta.png", H_FALT, "#falt")]:
    cmd = ["bash", RENDER, "--espera=3000", f"{D/tmp}{frag}", str(D/out), str(W), str(h)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    print(out, "| ancla:", frag or "(por defecto)", "| rc:", p.returncode)
    if p.stdout.strip():
        print("   ", p.stdout.strip())

try:
    from PIL import Image
    for o in ("panel-mapa.png", "panel-que-falta.png"):
        im = Image.open(D / o)
        st = im.convert("RGB").getcolors(maxcolors=1_000_000)
        print(o, im.size, "colores distintos:", len(st) if st else ">1M")
except Exception as e:
    print("PIL:", e)
