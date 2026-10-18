#!/usr/bin/env python3
"""
AUDITOR DE COBERTURA DE BACKUPS — "¿qué datos del lab viven FUERA de la cadena?"

Carencia que resuelve (detectada a mano 2 veces, nunca automatizada):
  - 05-sep-2026 (auditoría de backups): el mapa de la cadena diaria cubre
    ~/joko-lab (rsync, capa 1) y ~/.hermes (tar, capa 2) + volúmenes docker.
  - 08-09-2026 (backlog, entrada 22:54): /home/jokoalmi/perfume-ia/data/coleccion.db
    queda FUERA de toda capa diaria; la propuesta quedó "ANOTADO, sin implementar".
  - 14-sep-2026: sigue sin implementar, y el mismo hueco afecta a otros almacenes
    (cafe-ia/data/cafes.db, perfume-ia/data/futuribles.db) que nadie audita.
  El riesgo es de CLASE (data loss silencioso): cualquier almacén nuevo de un
  proyecto del lab nace fuera de la cadena y solo se descubre revisando a mano.

Qué hace (SOLO LECTURA; no copia, no mueve, no borra, no toca servicios):
  1. Deriva las RAÍCES CUBIERTAS leyendo los scripts REALES de backup (SRC= /
     HERMES=) — si mañana cambia un script, la auditoría lo refleja sin tocar código.
  2. Inventaría los almacenes de datos del home (*.db, *.sqlite*, *.jsonl)
     excluyendo ruido (cachés, perfiles de navegador, copias .BACKUP/.bak) y las
     raíces ya cubiertas.
  3. Clasifica cada almacén CUBIERTO / NO CUBIERTO y propone la acción.

Uso:
  python3 tools/auditar_cobertura_backups.py              # informe legible
  python3 tools/auditar_cobertura_backups.py --json       # JSON (crons)
  python3 tools/auditar_cobertura_backups.py --profundidad 3
  python3 tools/auditar_cobertura_backups.py --base /tmp/prueba --raiz /tmp/prueba/cub
  python3 tools/auditar_cobertura_backups.py --solo-no-cubiertos

Código de salida: 0 = todos los DATOS del lab detectados están cubiertos,
1 = hay almacenes de datos sin cubrir (apps/config no cuentan, para crons).
"""

import argparse
import fnmatch
import json
import os
import time
from pathlib import Path

# --- Configuración (rutas reales del lab, no inventadas) ---------------------

HOME = Path(os.path.expanduser("~"))

# Scripts que DEFINEN la cobertura por path (capas 1, 1b y 2 de la cadena).
SCRIPTS_FUENTE = (
    HOME / "hermes-lab/scripts/backup-joko-lab.sh",
    HOME / "hermes-lab/scripts/backup-hermes-state.sh",
    HOME / "hermes-lab/scripts/backup-perfume-ia.sh",
    HOME / "hermes-lab/scripts/backup-cafe-ia.sh",
)

PATRONES_DATOS = ("*.db", "*.sqlite", "*.sqlite3", "*.jsonl")

# Ruido: cachés, perfiles de aplicaciones y árboles que no son datos del lab.
RUIDO = (
    "/.git/", "/node_modules/", "/.venv/", "/venv/", "/__pycache__/",
    "/.cache", "/.thunderbird/", "/.mozilla/", "/snap/", "/.npm/", "/.cargo/",
    "/.local/share/tracker", "/.local/share/Trash", "/.local/state",
    "joko-lab.BACKUP", "hermes-backup-pre", "/backup_n8n_",
    "/Respaldo_Evolution/", "/.hermes/", "/Escritorio/", "/Descargas/",
    "/cbm-prueba/",  # copia de PRUEBA de joko-lab (5,2 G, 25-sep-2026) para el MCP
                     # codebase-memory: sus .jsonl duplican ~/joko-lab/research/rsi-v0
)

# Almacenes de apps/config (NO son datos del lab): se cuentan aparte para que el
# titular del informe sean solo los huecos accionables.
PATRONES_APP = (
    "/.config/", "/.pki/", "/.lmstudio/", "/nautilus/", "/hermes-lab/recovery/",
    "/ComfyUI/", "/.var/app/",
    # estado de apps externas (seguridad/CLI): no son datos del lab y son reinstalables
    "/.local/share/tirith/",    # log.jsonl del gate fail-closed (~9,4 M)
    "/.local/share/opencode/",  # opencode.db, sesiones del CLI (~8,5 M)
)

PROFUNDIDAD_DEFECTO = 5


# --- Helpers puros (testeables sin tocar el lab) -----------------------------

def normalizar(ruta) -> Path:
    """Convierte cualquier ruta (str/Path, con ~ y $VAR) en Path absoluta."""
    return Path(os.path.abspath(os.path.expanduser(os.path.expandvars(str(ruta)))))


def extraer_fuentes(texto: str, origen: str = "script") -> list:
    """Extrae las raíces FUENTE (SRC=, SOURCE=, HERMES=) de un script de backup.

    Solo líneas de asignación entrecomilladas; el DESTINO no es cobertura.
    Devuelve [(Path, origen)]."""
    fuentes = []
    for linea in texto.splitlines():
        limpia = linea.strip()
        if limpia.startswith("#") or "=" not in limpia:
            continue
        clave, _, valor = limpia.partition("=")
        if clave.strip() not in ("SRC", "SOURCE", "HERMES", "ORIGEN"):
            continue
        valor = valor.strip()
        # Solo valores ENTRE COMILLAS (un `SRC=$VAR` sin comillas es ambiguo)
        if len(valor) < 3 or valor[0] not in "\"'" or valor[-1] != valor[0]:
            continue
        fuentes.append((normalizar(valor[1:-1]), origen))
    return fuentes


def esta_cubierto(ruta, raices) -> bool:
    """True si la ruta está dentro de alguna raíz cubierta (sin trampa de prefijo)."""
    r = normalizar(ruta)
    for raiz in raices:
        rr = normalizar(raiz)
        if r == rr or rr in r.parents:
            return True
    return False


def es_ruido(ruta, ruido=RUIDO) -> bool:
    """True si la ruta cae en zona de caché o es una copia ya existente."""
    s = str(ruta)
    if any(pat in s for pat in ruido):
        return True
    nombre = os.path.basename(s)
    return (".BACKUP." in nombre or ".bak" in nombre
            or nombre.endswith("-wal") or nombre.endswith("-shm"))


def es_almacen(nombre: str) -> bool:
    """True si el nombre de archivo corresponde a un patrón de almacén de datos."""
    return any(fnmatch.fnmatch(nombre, pat) for pat in PATRONES_DATOS)


def categoria(ruta) -> str:
    """Clasifica un almacén: 'datos' (lab, accionable) o 'app' (config de apps)."""
    s = str(ruta)
    return "app" if any(pat in s for pat in PATRONES_APP) else "datos"


def total_bytes(items) -> int:
    """Suma de bytes de una lista de items del inventario."""
    return sum(i["bytes"] for i in items)


def tamano_legible(num_bytes: int) -> str:
    """Formatea bytes en K/M/G (una decimal)."""
    for unidad, factor in (("G", 1024 ** 3), ("M", 1024 ** 2), ("K", 1024)):
        if num_bytes >= factor:
            return f"{num_bytes / factor:.1f}{unidad}"
    return f"{num_bytes}B"


# --- Inventario y clasificación ----------------------------------------------

def candidatos(base, profundidad, raices=()):
    """Genera rutas de almacenes candidatos bajo `base`, podando ruido y cubiertos.

    `profundidad` = niveles de directorio a recorrer por debajo de `base`.
    Las raíces ya cubiertas se PODAN (no se desciende en ellas): sus almacenes
    no se inventarían, así el informe se centra en los huecos y el escaneo no
    recorre ~/joko-lab entero."""
    base = normalizar(base)
    partes_base = len(base.parts)
    for dirpath, dirs, files in os.walk(base):
        actual = Path(dirpath)
        if len(actual.parts) - partes_base >= profundidad:
            dirs[:] = []
            continue
        dirs[:] = sorted(d for d in dirs
                         if not es_ruido(actual / d)
                         and not esta_cubierto(actual / d, raices))
        for nombre in sorted(files):
            ruta = actual / nombre
            if es_almacen(nombre) and not es_ruido(ruta):
                yield ruta


def inventariar(base, profundidad, raices) -> list:
    """Inventaría almacenes de datos clasificando su cobertura por la cadena."""
    items = []
    for ruta in candidatos(base, profundidad, raices):
        try:
            st = ruta.stat()
        except OSError:
            continue
        items.append({
            "ruta": str(ruta),
            "bytes": st.st_size,
            "mtime": time.strftime("%Y-%m-%d", time.localtime(st.st_mtime)),
            "cubierto": esta_cubierto(ruta, raices),
            "categoria": categoria(ruta),
        })
    return sorted(items, key=lambda i: (i["cubierto"], -i["bytes"]))


def cargar_raices_cubiertas(scripts=SCRIPTS_FUENTE) -> list:
    """Lee los scripts reales de backup y devuelve [(Path, origen)] existentes."""
    raices, vistos = [], set()
    for script in scripts:
        script = normalizar(script)
        if not script.is_file():
            continue
        try:
            texto = script.read_text(errors="ignore")
        except OSError:
            continue
        for ruta, origen in extraer_fuentes(texto, script.name):
            if ruta not in vistos and ruta.exists():
                vistos.add(ruta)
                raices.append((ruta, origen))
    return raices


# --- Informe -----------------------------------------------------------------

def _seccion_raices(raices) -> list:
    """Líneas de la sección de raíces cubiertas."""
    lineas = ["## ✅ Raíces cubiertas (derivadas de los scripts reales)"]
    for ruta, origen in raices:
        lineas.append(f"- `{ruta}`  ← {origen}")
    return lineas if raices else ["- ⚠️ No se pudo derivar ninguna raíz de los scripts"]


def _seccion_items(titulo, items) -> list:
    """Líneas de una sección de almacenes."""
    if not items:
        return [titulo, "- (ninguno)", ""]
    lineas = [titulo]
    for it in items:
        lineas.append(f"- {tamano_legible(it['bytes']):>7}  {it['ruta']}"
                      f"  (mod {it['mtime']})")
    return lineas + [""]


def huecos_lab(items) -> list:
    """Almacenes de DATOS del lab que quedan fuera de la cadena (accionables)."""
    return [i for i in items if i["categoria"] == "datos" and not i["cubierto"]]


def formatear_informe(items, raices) -> str:
    """Construye el informe legible."""
    lab = huecos_lab(items)
    app = [i for i in items if i["categoria"] == "app" and not i["cubierto"]]
    cubiertos = [i for i in items if i["cubierto"]]
    lineas = ["# 🔐 AUDITORÍA DE COBERTURA DE BACKUPS (solo lectura)", ""]
    lineas += _seccion_raices(raices) + [""]
    lineas.append("Nota: los almacenes DENTRO de esas raíces no se inventarían "
                  "(se podan del escaneo); el informe lista los de fuera.")
    lineas.append("")
    lineas += _seccion_items(f"## 🔴 Datos del lab NO cubiertos ({len(lab)})", lab)
    if app:
        lineas.append(f"## ⚪ Apps/config fuera de la cadena: {len(app)} ficheros "
                      f"({tamano_legible(total_bytes(app))}) — no son datos del lab")
        lineas.append("")
    if cubiertos:
        lineas += _seccion_items(f"## 🟢 Almacenes cubiertos ({len(cubiertos)})", cubiertos)
    lineas.append("## 🎯 Siguiente paso")
    if lab:
        lineas.append(f"- {len(lab)} almacén(es) de datos fuera de la cadena diaria: "
                      "diseñar copia con rotación (NO ejecutar sin OK del usuario).")
    else:
        lineas.append("- Todos los datos del lab detectados están dentro de la cadena ✅")
    return "\n".join(lineas)


def _resumen_json(items, raices) -> dict:
    """Resumen estructurado serializable (sin lambdas ni Paths)."""
    return {
        "raices": [{"ruta": str(r), "origen": o} for r, o in raices],
        "total": len(items),
        "datos_no_cubiertos": huecos_lab(items),
        "app_no_cubiertos": len([i for i in items
                                 if i["categoria"] == "app" and not i["cubierto"]]),
        "cubiertos": len([i for i in items if i["cubierto"]]),
    }


def _parsear_args(argv=None):
    """Argumentos de CLI."""
    p = argparse.ArgumentParser(description="Auditoría de cobertura de backups (solo lectura)")
    p.add_argument("--base", default=str(HOME), help="raíz a inventariar (def: $HOME)")
    p.add_argument("--profundidad", type=int, default=PROFUNDIDAD_DEFECTO,
                   help=f"profundidad máxima de escaneo (def: {PROFUNDIDAD_DEFECTO})")
    p.add_argument("--raiz", action="append", default=[],
                   help="raíz cubierta extra (repetible)")
    p.add_argument("--solo-no-cubiertos", action="store_true",
                   help="imprime solo los almacenes sin cubrir")
    p.add_argument("--json", action="store_true", help="salida JSON")
    return p.parse_args(argv)


def main(argv=None) -> int:
    """Punto de entrada: audita y devuelve 1 si hay DATOS del lab sin cubrir."""
    args = _parsear_args(argv)
    raices = cargar_raices_cubiertas()
    raices += [(normalizar(r), "--raiz") for r in args.raiz]
    items = inventariar(args.base, args.profundidad, [r for r, _ in raices])
    huecos = huecos_lab(items)
    if args.json:
        print(json.dumps(_resumen_json(items, raices), ensure_ascii=False, indent=2))
    elif args.solo_no_cubiertos:
        for it in huecos:
            print(f"{tamano_legible(it['bytes']):>7}  {it['ruta']}")
    else:
        print(formatear_informe(items, raices))
    return 1 if huecos else 0


if __name__ == "__main__":
    raise SystemExit(main())
