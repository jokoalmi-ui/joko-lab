#!/usr/bin/python3
"""OCR local del Joko Lab.

Regla de decisión:
  - PDF con capa de texto en la página  -> pdftotext (exacto, instantáneo, gratis)
  - PDF escaneado / imagen / foto       -> HunyuanOCR 1,1B (llama-server en 127.0.0.1:8099)
  - Nunca se usa OCR para sustituir una capa de texto existente.

Uso:
  ocr_local.py archivo.pdf                     # todas las páginas, salida ./archivo.ocr.md
  ocr_local.py archivo.pdf --pages 1-3         # solo esas páginas
  ocr_local.py foto.jpg --out texto.md
  ocr_local.py archivo.pdf --keep-server       # deja el servidor cargado al terminar
  ocr_local.py archivo.pdf --force-ocr         # ignora la capa de texto y pasa OCR

AVISO medido en el lab (30-oct-2026): el OCR acierta el texto grande y puede INVENTAR
cifras y marcas en gráficos con collage. Todo importe, referencia o fecha se verifica
contra el original antes de meterlo en una BD.
"""
import argparse
import base64
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

HOME = os.path.expanduser("~")
SERVER_SH = os.path.join(HOME, "joko-lab", "tools", "ocr_local_server.sh")
LOG = os.path.join(tempfile.gettempdir(), "ocr_local_server.log")
MIN_TEXTO = 60          # caracteres no-espacio por página para considerar que hay capa de texto
PROMPT = "OCR"
AVISO = ("\n\n---\n> Aviso del lab: el OCR puede inventar cifras, marcas y fechas en gráficos "
         "con collage. Verifica importes y referencias contra el original antes de fiarte.\n")


# --------------------------------------------------------------------------- servidor
def health(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def arrancar_servidor(port, espera=240):
    """Devuelve el Popen si lo hemos arrancado nosotros, o None si ya estaba vivo."""
    if health(port):
        print(f"[ocr] servidor ya activo en :{port}", file=sys.stderr)
        return None
    print(f"[ocr] arrancando llama-server en :{port} …", file=sys.stderr)
    log = open(LOG, "wb")
    p = subprocess.Popen(["bash", SERVER_SH], stdout=log, stderr=subprocess.STDOUT,
                         start_new_session=True, env={**os.environ, "OCR_PORT": str(port)})
    t0 = time.time()
    while time.time() - t0 < espera:
        if health(port):
            print(f"[ocr] servidor listo en {time.time()-t0:.1f}s", file=sys.stderr)
            return p
        if p.poll() is not None:
            sys.exit(f"[ocr] el servidor murió al arrancar. Log: {LOG}")
        time.sleep(1)
    parar_servidor(p)
    sys.exit(f"[ocr] timeout de arranque ({espera}s). Log: {LOG}")


def parar_servidor(p):
    if not p:
        return
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        p.wait(timeout=15)
    except Exception:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except Exception:
            pass


# --------------------------------------------------------------------------- OCR
def ocr_imagen(ruta, port, max_tokens=4096):
    b64 = base64.b64encode(open(ruta, "rb").read()).decode()
    payload = {
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": PROMPT},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
        ]}],
        "temperature": 0, "max_tokens": max_tokens, "stream": False,
    }
    req = urllib.request.Request(f"http://127.0.0.1:{port}/v1/chat/completions",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        d = json.load(r)
    dt = time.time() - t0
    u = d.get("usage", {})
    return d["choices"][0]["message"]["content"], dt, u.get("completion_tokens", 0)


def capa_texto(pdf, pagina):
    r = subprocess.run(["pdftotext", "-f", str(pagina), "-l", str(pagina), pdf, "-"],
                       capture_output=True, text=True)
    return r.stdout


def render(pdf, pagina, dpi, tmpdir):
    base = os.path.join(tmpdir, f"pag{pagina:03d}")
    subprocess.run(["pdftoppm", "-f", str(pagina), "-l", str(pagina), "-r", str(dpi), "-png",
                    "-singlefile", pdf, base], check=True, capture_output=True)
    return base + ".png"


def paginas_totales(pdf):
    r = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True)
    for l in r.stdout.splitlines():
        if l.startswith("Pages:"):
            return int(l.split()[1])
    return 0


def parse_pages(spec, total):
    if not spec:
        return list(range(1, total + 1))
    out = []
    for trozo in spec.split(","):
        trozo = trozo.strip()
        if "-" in trozo:
            a, b = trozo.split("-", 1)
            out += list(range(int(a), int(b) + 1))
        elif trozo:
            out.append(int(trozo))
    return [p for p in out if 1 <= p <= total]


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="OCR local: pdftotext si hay capa de texto, HunyuanOCR si no.")
    ap.add_argument("archivo")
    ap.add_argument("--out", help="fichero de salida (por defecto ./<nombre>.ocr.md)")
    ap.add_argument("--pages", help="páginas, p.ej. 1-3 o 2,5 (solo PDF)")
    ap.add_argument("--dpi", type=int, default=200, help="resolución de render para OCR (def. 200)")
    ap.add_argument("--port", type=int, default=8099)
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--force-ocr", action="store_true", help="pasa OCR aunque haya capa de texto")
    ap.add_argument("--keep-server", action="store_true", help="no para el servidor al terminar")
    a = ap.parse_args()

    if not os.path.isfile(a.archivo):
        sys.exit(f"no existe: {a.archivo}")
    if not shutil.which("pdftotext") or not shutil.which("pdftoppm"):
        sys.exit("faltan pdftotext/pdftoppm (poppler-utils)")

    ext = os.path.splitext(a.archivo)[1].lower()
    stem = os.path.splitext(os.path.basename(a.archivo))[0]
    out = a.out or f"{stem}.ocr.md"
    partes, resumen, proc = [], [], None
    tmpdir = tempfile.mkdtemp(prefix="ocr_local_")
    t_inicio = time.time()

    try:
        if ext == ".pdf":
            total = paginas_totales(a.archivo)
            if total == 0:
                sys.exit("no puedo leer el número de páginas (¿PDF corrupto?)")
            pags = parse_pages(a.pages, total)
            # decide si hace falta el servidor alguna vez
            necesita = a.force_ocr or any(
                len("".join(capa_texto(a.archivo, p).split())) < MIN_TEXTO for p in pags)
            if necesita:
                proc = arrancar_servidor(a.port)

            for p in pags:
                txt = "" if a.force_ocr else capa_texto(a.archivo, p)
                limpio = "".join(txt.split())
                if len(limpio) >= MIN_TEXTO:
                    partes.append(f"<!-- página {p} · pdftotext · capa de texto nativa -->\n{txt.strip()}")
                    resumen.append((p, "pdftotext", 0.0, 0, len(txt)))
                else:
                    if proc is None and not health(a.port):
                        proc = arrancar_servidor(a.port)
                    png = render(a.archivo, p, a.dpi, tmpdir)
                    txt, dt, tok = ocr_imagen(png, a.port, a.max_tokens)
                    partes.append(f"<!-- página {p} · OCR HunyuanOCR · {dt:.1f}s -->\n{txt.strip()}")
                    resumen.append((p, "ocr", dt, tok, len(txt)))
        else:
            proc = arrancar_servidor(a.port)
            img = a.archivo
            if ext not in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"):
                tmp = os.path.join(tmpdir, "entrada.png")
                subprocess.run(["pdftoppm", "-png", "-singlefile", "-r", str(a.dpi), img, tmp[:-4]],
                               check=False)
                img = tmp if os.path.exists(tmp) else img
            txt, dt, tok = ocr_imagen(img, a.port, a.max_tokens)
            partes.append(f"<!-- imagen · OCR HunyuanOCR · {dt:.1f}s -->\n{txt.strip()}")
            resumen.append((1, "ocr", dt, tok, len(txt)))

        open(out, "w", encoding="utf-8").write("\n\n".join(partes) + AVISO)

        print(f"salida: {out}")
        for p, m, dt, tok, n in resumen:
            extra = f"{dt:.1f}s {tok} tok" if m == "ocr" else "instantáneo"
            print(f"  pág {p}: {m:9s} {extra:18s} {n} chars")
        ocr_n = sum(1 for r in resumen if r[1] == "ocr")
        print(f"total {time.time()-t_inicio:.1f}s · {len(resumen)} págs · {ocr_n} por OCR")
        if ocr_n:
            print("AVISO: revisa cifras y referencias contra el original (el OCR inventa datos en collages).")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
        if not a.keep_server:
            parar_servidor(proc)


if __name__ == "__main__":
    main()
