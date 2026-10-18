#!/usr/bin/env python3
"""
verificar_research.py — Post-procesador de veracidad para análisis del lab (16-ago-2026)

Escanea archivos de joko-lab/research/*.md y añade a la cabecera la etiqueta
de veracidad del contenido, usando verificador_alucinaciones.py.

Modos:
  --todos        : procesa TODOS los análisis (backfill histórico)
  --recientes N  : procesa los N archivos modificados más recientemente (default)
  --archivo X    : procesa un archivo concreto
  --nuevos       : solo los que NO tienen etiqueta de veracidad aún
  --juez         : añade también la etiqueta CALIDAD (LLM-as-Judge, A2) —
                   opcional; sin él el comportamiento es idéntico al de antes
                   (la veracidad no se ralentiza). El juez evalúa el análisis
                   como respuesta (pregunta = título) y añade:
                   **CALIDAD:** PASA/REVISA/FALLA (promedio, estado).

La etiqueta se inserta después de la línea `**Fuente:**` (o del título si no
hay Fuente). NO modifica el cuerpo. Si el archivo ya tiene `VERACIDAD:`,
se actualiza la línea (idempotente).

Ejecución típica (tras guardar un análisis):
  python3 tools/verificar_research.py --archivo research/analisis-X.md
  python3 tools/verificar_research.py --nuevos   # los que faltan
  python3 tools/verificar_research.py --archivo research/analisis-X.md --juez
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verificador_alucinaciones import verificar
from llm_as_judge import juzgar, consolidar, JUEZ1_DEF, JUEZ2_DEF

RESEARCH = Path(__file__).resolve().parent.parent / "research"
ETIQUETA_RE = re.compile(r"^\*\*VERACIDAD:\*\*.*$", re.M)
CALIDAD_RE = re.compile(r"^\*\*CALIDAD:\*\*.*$", re.M)


def etiquetar_texto(texto: str) -> str:
    """Devuelve la etiqueta [VERIFICADO]/[ALCANCE INTERNO]/[NO VERIFICADO]/[REVISAR]."""
    # Extraer tema del título si es posible (mejora la relevancia)
    titulo = texto.split("\n", 1)[0] if texto else ""
    r = verificar(texto, tema=titulo[:80] if titulo else None)
    return r["etiqueta"]


def etiquetar_calidad(texto: str) -> str:
    """Devuelve la etiqueta CALIDAD (LLM-as-Judge A2): PASA/REVISA/FALLA/DISCREPANCIA.

    Evalúa el análisis como respuesta (pregunta = título del archivo). Los
    jueces son locales (glm + gpt-oss vía LM Studio). Si ninguno responde
    (LM Studio apagado o modelos no cargados), devuelve 'no disponible'
    — nunca bloquea la veracidad.
    """
    titulo = texto.split("\n", 1)[0][:120] if texto else ""
    # El análisis completo es la "respuesta"; su título es la "pregunta".
    j1 = juzgar(texto, pregunta=titulo, contexto="", model=JUEZ1_DEF)
    j2 = juzgar(texto, pregunta=titulo, contexto="", model=JUEZ2_DEF)
    res = consolidar(j1, j2)
    if res.get("estado") == "SIN_JUEZ":
        return "no disponible (LM Studio sin jueces)"
    veredicto = res.get("veredicto", "REVISA")
    promedio = res.get("promedio", 0)
    estado = res.get("estado", "")
    detalle = res.get("detalle", "")
    return f"{veredicto} (promedio {promedio}, {estado}) — {detalle}"


def procesar_archivo(path: Path, dry_run: bool = False, con_juez: bool = False) -> tuple:
    """Procesa un archivo: añade/actualiza la línea VERACIDAD (y CALIDAD si con_juez).
    Devuelve (ok, etiqueta)."""
    try:
        texto = path.read_text(encoding="utf-8")
    except Exception as e:
        return (False, f"ERROR lectura: {e}")

    # Si ya tiene etiqueta, actualizar solo si cambia (idempotente)
    etiqueta = etiquetar_texto(texto)

    if ETIQUETA_RE.search(texto):
        nuevo = ETIQUETA_RE.sub(f"**VERACIDAD:** {etiqueta}", texto)
    else:
        # Insertar después de **Fuente:** o tras el título
        if "\n\n**Fuente:**" in texto:
            nuevo = texto.replace(
                "\n\n**Fuente:**", f"\n\n**VERACIDAD:** {etiqueta}\n\n**Fuente:**", 1)
        else:
            primer_salto = texto.find("\n", texto.find("# "))
            if primer_salto > 0:
                nuevo = (texto[:primer_salto] + f"\n**VERACIDAD:** {etiqueta}"
                         + texto[primer_salto:])
            else:
                nuevo = f"**VERACIDAD:** {etiqueta}\n" + texto

    # Capa CALIDAD (LLM-as-Judge) — opcional, tras VERACIDAD
    if con_juez:
        calidad = etiquetar_calidad(nuevo)
        if CALIDAD_RE.search(nuevo):
            nuevo = CALIDAD_RE.sub(f"**CALIDAD:** {calidad}", nuevo)
        else:
            # Insertar justo después de la línea VERACIDAD
            m = ETIQUETA_RE.search(nuevo)
            if m:
                pos = m.end()
                nuevo = nuevo[:pos] + f"\n**CALIDAD:** {calidad}" + nuevo[pos:]

    if not dry_run and nuevo != texto:
        path.write_text(nuevo, encoding="utf-8")
    return (True, etiqueta)


def main():
    ap = argparse.ArgumentParser(description="Post-procesador de veracidad para research/")
    ap.add_argument("--todos", action="store_true", help="procesar todos los análisis")
    ap.add_argument("--recientes", type=int, default=0, help="N archivos más recientes")
    ap.add_argument("--archivo", help="procesar un archivo concreto")
    ap.add_argument("--nuevos", action="store_true", help="solo los que no tienen etiqueta")
    ap.add_argument("--dry-run", action="store_true", help="no escribir, solo mostrar")
    ap.add_argument("--juez", action="store_true",
                    help="añadir también la etiqueta CALIDAD (LLM-as-Judge, A2)")
    args = ap.parse_args()

    if args.archivo:
        archivos = [Path(args.archivo)]
        if not archivos[0].is_absolute():
            # Si la ruta empieza por "research/", no duplicarla (RESEARCH ya incluye research)
            if archivos[0].parts and archivos[0].parts[0] == "research":
                archivos[0] = RESEARCH / Path(*archivos[0].parts[1:])
            else:
                archivos[0] = RESEARCH / archivos[0]
    else:
        archivos = sorted(RESEARCH.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        if args.recientes > 0:
            archivos = archivos[:args.recientes]
        if args.nuevos:
            archivos = [p for p in archivos if not ETIQUETA_RE.search(p.read_text(encoding="utf-8"))]

    if not archivos:
        print("Sin archivos a procesar.")
        return

    ok = 0
    fallos = []
    for p in archivos:
        r, etiqueta = procesar_archivo(p, dry_run=args.dry_run, con_juez=args.juez)
        if r:
            ok += 1
            extra = " +CALIDAD" if args.juez else ""
            print(f"{'[DRY]' if args.dry_run else '  ✅'} {p.name}: {etiqueta}{extra}")
        else:
            fallos.append((p.name, etiqueta))

    print(f"\nProcesados: {ok} | Fallos: {len(fallos)}")
    for nombre, err in fallos:
        print(f"  ❌ {nombre}: {err}")


if __name__ == "__main__":
    main()
