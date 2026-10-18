#!/usr/bin/env python3
"""Revision visual de las 7 slides de la Leccion 5 con GLM-4.6V-Flash (LM Studio).
Reescala cada PNG a 1024 px de ancho (la API local devuelve vacio con nativo).
Dos pasadas por slide: (1) defectos de maquetacion con modos de fallo NOMBRADOS;
(2) CONTROL DE LECTURA: transcripcion literal del titular y del pie, porque un
veredicto "SIN DEFECTOS" sin control de lectura no vale (VLM complaciente).
Reanudable: lee su JSON y salta las slides que ya tienen las dos pasadas."""
import base64, json, pathlib, sys, time
from PIL import Image
import urllib.request

LEC = pathlib.Path("/home/jokoalmi/joko-lab/research/infografias/serie-ia-agentes/leccion-5-produccion-fiabilidad-coste-y-limites")
OUT = LEC / ("revision-visual-" + time.strftime("%Y%m%d") + ".json")
TMP = pathlib.Path("/tmp/l5_1024")
TMP.mkdir(exist_ok=True)
MODELO = "glm-4.6v-flash"
API = "http://localhost:1234/v1/chat/completions"

PREGUNTA = (
    "Esta es una diapositiva vertical (1080x1350) de un carrusel para LinkedIn. "
    "Revisa SOLO defectos de maquetacion, no el estilo: "
    "(a) texto cortado por algun borde del lienzo; (b) texto solapado con otro texto o figura; "
    "(c) algun elemento que se salga del lienzo; (d) texto ilegible por tamano o contraste; "
    "(e) la imagen pequena del objeto, si aparece, deformada o cortada. "
    "Responde en espanol con una lista muy breve de defectos. "
    "Si no ves ningun defecto, responde exactamente: SIN DEFECTOS"
)

CONTROL = (
    "Transcribe literalmente, SIN inventar y sin corregir: (1) el titular grande de la "
    "diapositiva; (2) el texto del pie inferior (la linea en mayusculas, abajo del todo). "
    "Responde solo con esas dos lineas, precedidas de TITULAR: y PIE:. "
    "Si algo no se lee, escribe NO LEGIBLE en su lugar."
)

def preparar(p):
    im = Image.open(p).convert("RGB")
    w, h = im.size
    nw = 1024
    nh = int(h * nw / w)
    im2 = im.resize((nw, nh), Image.LANCZOS)
    dst = TMP / p.name
    im2.save(dst, "JPEG", quality=88)
    return dst

def preguntar(ruta, texto):
    b64 = base64.b64encode(ruta.read_bytes()).decode()
    payload = {
        "model": MODELO,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            {"type": "text", "text": texto},
        ]}],
        "max_tokens": 2048, "temperature": 0.0,
    }
    req = urllib.request.Request(API, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.loads(r.read())
    ch = d["choices"][0]["message"]
    txt = ch.get("content") or ""
    if not txt.strip():
        txt = "[VACIO] reasoning: " + (ch.get("reasoning_content") or "")[:400]
    return txt.strip(), d.get("usage", {})

def volcar(filas):
    OUT.write_text(json.dumps({"fecha": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                               "modelo": MODELO, "slides": filas}, ensure_ascii=False, indent=2),
                   encoding="utf-8")

slides = sorted((LEC / "slides").glob("*.png"))
filas = []
if OUT.exists():
    try:
        prev = json.loads(OUT.read_text(encoding="utf-8")).get("slides", [])
        hechas = {f["slide"]: f for f in prev
                  if f.get("respuesta") and f.get("control") and not f.get("error")}
        filas = [hechas[s.name] for s in slides if s.name in hechas]
        print(f"reanudando: {len(filas)}/{len(slides)} slides ya revisadas (2 pasadas)")
    except Exception as e:
        print("aviso: no se pudo reanudar:", e)
ya = {f["slide"] for f in filas}
for i, p in enumerate(slides, 1):
    if p.name in ya:
        print(f"[{i}/{len(slides)}] {p.name}: ya hecha, se salta")
        continue
    t0 = time.time()
    try:
        ruta = preparar(p)
        txt, _ = preguntar(ruta, PREGUNTA)
        seg = round(time.time() - t0, 1)
        t1 = time.time()
        ctl, _ = preguntar(ruta, CONTROL)
        seg2 = round(time.time() - t1, 1)
        filas.append({"slide": p.name, "segundos": seg, "respuesta": txt,
                      "segundos_control": seg2, "control": ctl})
        print(f"[{i}/{len(slides)}] {p.name} ({seg}s + {seg2}s): {txt[:200]} || CONTROL: {ctl[:200]}")
    except Exception as e:
        filas.append({"slide": p.name, "error": repr(e)[:300]})
        print(f"[{i}/{len(slides)}] {p.name} ERROR: {e!r}")
    volcar(filas)
    sys.stdout.flush()
volcar(filas)
print("\nESCRITO:", OUT, OUT.stat().st_size, "bytes")
