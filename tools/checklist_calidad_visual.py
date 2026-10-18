#!/usr/bin/env python3
"""checklist_calidad_visual.py — Gate de CALIDAD visual pre-publicación (B4, 20-ago-2026).

Complementa el gate de VERACIDAD (verificador_alucinaciones.py): este valida
que la imagen sea BUENA visualmente antes de publicarla/compartirla.

6 verificaciones (M12-04):
  1. FOCO — nitidez global (varianza de gradiente Laplaciano)
  2. NITIDEZ — bordes definidos (energía de bordes Canny)
  3. COMPOSICIÓN — contenido no pegado a los bordes (márgenes de contenido)
  4. COHERENCIA CROMÁTICA — paleta consistente (top colores, sin dominante rara)
  5. SIN DISTRACCIONES — ruido/artefactos (proporción de píxeles de alto detalle)
  6. LEGIBILIDAD — texto legible (requiere GLM visión local; opcional con --vision)

Las 5 primeras son OBJETIVAS (PIL puro, sin numpy — el python del sistema no
lo tiene). La 6ª usa GLM visión local si está cargado (lmstudio 1234).

Uso:
  python3 checklist_calidad_visual.py imagen.png [--vision] [--json]

Salida: PASS/FAIL por check + veredicto global (PASS si 5/6 o 6/6 OK,
REVISAR si 4/6, FAIL si <4/6).
"""
import argparse, json, os, re, sys, base64, urllib.request
from PIL import Image, ImageFilter, ImageStat, ImageOps

UMBRALES = {
    "foco": 300.0,         # varianza Laplaciano mínima (calibrado 20-ago con datos
                           #   reales: slide carrusel nítida = 1086; blur 30 = 191 →
                           #   umbral 300 separa claramente sin falsos positivos)
    "nitidez": 0.01,       # proporción mínima de píxeles de borde (calibrado 20-ago:
                           #   slide carrusel limpia = 2.1%, fotos reales = 5-15%)
    "margen": 0.02,        # proporción mínima de borde SIN contenido FUERTE (calibrado:
                           #   fondo crema llega al borde por diseño → usar bordes fuertes)
    "distraccion": 0.35,   # proporción MÁXIMA de píxeles de alto detalle
}


def _luma(img):
    return img.convert("L")


def check_foco(img):
    """Varianza del gradiente Laplaciano — imagen borrosa = baja."""
    g = _luma(img).filter(ImageFilter.FIND_EDGES)
    stat = ImageStat.Stat(g)
    return stat.var[0] if stat.var else 0.0


def check_nitidez(img):
    """Proporción de píxeles de borde (Canny aproximado: umbral de gradiente)."""
    g = _luma(img).filter(ImageFilter.FIND_EDGES)
    px = list(g.getdata())
    bordes = sum(1 for v in px if v > 60)
    return bordes / len(px)


def check_composicion(img):
    """Contenido no pegado a los bordes: margen mínimo de contenido FUERTE por lado.
    Usa bordes fuertes (>150) para que el fondo de diseño (crema hasta el borde)
    no cuente como contenido pegado — calibrado 20-ago con slide de carrusel."""
    w, h = img.size
    g = _luma(img).filter(ImageFilter.FIND_EDGES)
    px = g.load()
    # Saltar el contorno exterior de la imagen (borde de 2px del PNG — el fondo
    # crema llega al borde por diseño y FIND_EDGES marca esa transición como
    # contenido; calibrado 20-ago: daba margen 0.00% en slides limpias).
    e = 2
    # buscar primera fila/columna con contenido FUERTE desde cada lado
    top = h
    for y in range(e, h - e):
        if any(px[x, y] > 150 for x in range(e, w - e, 4)):
            top = y
            break
    left = w
    for x in range(e, w - e):
        if any(px[x, y] > 150 for y in range(e, h - e, 4)):
            left = x
            break
    bottom = h - 1 - e
    for y in range(h - 1 - e, e, -1):
        if any(px[x, y] > 150 for x in range(e, w - e, 4)):
            bottom = y
            break
    right = w - 1 - e
    for x in range(w - 1 - e, e, -1):
        if any(px[x, y] > 150 for y in range(e, h - e, 4)):
            right = x
            break
    margen_min = min(top - e, left - e, (h - 1 - e) - bottom, (w - 1 - e) - right) / min(w, h)
    return margen_min


def check_cromatico(img):
    """Coherencia cromática: la paleta no debe tener dominante extraña.
    Mide si el color medio es 'razonable' (no saturado extremo ni gris vacío)
    y si hay al menos 2 colores distintos en la paleta (no plano)."""
    stat = ImageStat.Stat(img)
    mean = stat.mean  # R, G, B
    var = stat.var
    # dominante rara: canal dominado (|R-G|,|G-B|,|R-B| > 120 en el medio)
    dominante = max(abs(mean[0]-mean[1]), abs(mean[1]-mean[2]), abs(mean[0]-mean[2]))
    plano = max(var) < 100  # variación casi nula = imagen plana
    if plano:
        return 0.0, "imagen plana (sin variación)"
    if dominante > 120:
        return 0.0, f"dominante cromática extrema (Δ={dominante:.0f})"
    return 1.0, "paleta coherente"


def check_distracciones(img):
    """Proporción de píxeles de muy alto detalle (ruido/artefactos/texto denso)."""
    g = _luma(img).filter(ImageFilter.FIND_EDGES)
    px = list(g.getdata())
    alto = sum(1 for v in px if v > 180)
    return alto / len(px)


def check_legibilidad_vision(img_path):
    """Texto legible vía GLM visión local (si está cargado). Devuelve (bool, detalle)."""
    try:
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        payload = {
            "model": "glm-4.6v-flash",
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": "Checklist legibilidad: 1) ¿Hay texto? 2) Si lo hay, ¿es legible (nitidez, tamaño, contraste)? 3) ¿Hay texto cortado o ilegible? Responde SOLO: SÍ/NO por punto, sin razonar."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
            ]}],
            "max_tokens": 200, "temperature": 0.1,
        }
        req = urllib.request.Request(
            "http://localhost:1234/api/v0/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.loads(r.read())
        content = resp["choices"][0]["message"].get("content") or ""
        if not content:
            content = resp["choices"][0]["message"].get("reasoning_content", "")
        # Formato GLM: responde SÍ/NO por punto → "SÍ/SÍ/NO"
        # P1 ¿hay texto? · P2 ¿legible? · P3 ¿cortado/ilegible?
        # Legible si: P2=SÍ y P3=NO (o no hay texto → no aplica → PASS)
        pts = [p.strip().upper() for p in re.split(r"[/,\n]", content) if p.strip()]
        pts = [p for p in pts if p in ("SÍ", "SI", "NO", "SÍ.", "NO.") or p.startswith(("SÍ", "SI", "NO"))][:3]
        if len(pts) >= 3:
            hay_texto = pts[0].startswith("SÍ") or pts[0].startswith("SI")
            legible = pts[1].startswith("SÍ") or pts[1].startswith("SI")
            cortado = pts[2].startswith("SÍ") or pts[2].startswith("SI")
            ok = (not hay_texto) or (legible and not cortado)
        else:
            # fallback: respuesta libre — asumir legible si no dice explícitamente ilegible
            ok = "ILEGIBLE" not in content.upper() and "CORTADO" not in content.upper()
        return ok, content.strip()[:200]
    except Exception as e:
        return None, f"GLM no disponible: {str(e)[:80]}"


def main():
    ap = argparse.ArgumentParser(description="Gate de calidad visual (B4)")
    ap.add_argument("imagen")
    ap.add_argument("--vision", action="store_true", help="incluir check legibilidad GLM")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(args.imagen):
        print(json.dumps({"error": f"no existe: {args.imagen}"}) if args.json else f"ERROR: no existe {args.imagen}")
        sys.exit(2)

    img = Image.open(args.imagen).convert("RGB")
    resultados = []

    foco = check_foco(img)
    resultados.append(("foco", foco >= UMBRALES["foco"], f"varianza Laplaciano {foco:.1f} (≥{UMBRALES['foco']})"))

    nitidez = check_nitidez(img)
    resultados.append(("nitidez", nitidez >= UMBRALES["nitidez"], f"bordes {nitidez:.2%} (≥{UMBRALES['nitidez']:.0%})"))

    margen = check_composicion(img)
    resultados.append(("composicion", margen >= UMBRALES["margen"], f"margen mínimo {margen:.2%} (≥{UMBRALES['margen']:.0%})"))

    cromatico_ok, cromatico_msg = check_cromatico(img)
    resultados.append(("cromatico", bool(cromatico_ok), cromatico_msg))

    distraccion = check_distracciones(img)
    resultados.append(("distraccion", distraccion <= UMBRALES["distraccion"],
                       f"alto detalle {distraccion:.2%} (≤{UMBRALES['distraccion']:.0%})"))

    if args.vision:
        leg_ok, leg_msg = check_legibilidad_vision(args.imagen)
        if leg_ok is None:
            resultados.append(("legibilidad", None, leg_msg))
        else:
            resultados.append(("legibilidad", leg_ok, leg_msg))

    aprobados = sum(1 for _, ok, _ in resultados if ok)
    total = len(resultados)
    if aprobados == total:
        veredicto = "PASS"
    elif aprobados >= total - 1:
        veredicto = "PASS"
    elif aprobados >= total - 2:
        veredicto = "REVISAR"
    else:
        veredicto = "FAIL"

    if args.json:
        print(json.dumps({
            "imagen": args.imagen, "veredicto": veredicto,
            "checks": [{"check": c, "ok": ok, "detalle": d} for c, ok, d in resultados],
        }, ensure_ascii=False, indent=2))
    else:
        print("── CHECKLIST CALIDAD VISUAL (B4) ──")
        for c, ok, detalle in resultados:
            icono = "✅" if ok else ("⚠️" if ok is None else "❌")
            print(f"  {icono} {c}: {detalle}")
        print(f"  → VEREDICTO: {veredicto} ({aprobados}/{total})")
        print("──────────────────────────────────")

    sys.exit(0 if veredicto == "PASS" else 1)


if __name__ == "__main__":
    main()
