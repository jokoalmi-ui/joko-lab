#!/usr/bin/env python3
"""Puente manual LAB <-> Gemini web (Google AI Pro). Ver README del puente.

Ordenes:
  nuevo "<tema>" [--herramienta X] [--contexto FICHERO] [--nota-interna TXT]
        -> crea el prompt en outbox/
  estado
        -> que hay pendiente y ultimos movimientos
  archivar <fichero> [--valor N] [--herramienta X] [--nota TXT]
        -> mueve de inbox/ a procesados/ y anade la linea al registro

Base por defecto: <repo joko-lab>/04-operations/puente-gemini/
Override para pruebas: variable de entorno PUENTE_BASE.
No toca la red, no borra nada y no sale de la carpeta del puente.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime

HERRAMIENTAS = ("3.1-pro", "deep-research", "notebooklm", "gem", "workspace")
TOPE_CONTEXTO = 400 * 1024  # aviso si el contexto es enorme


def repo_root():
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return "/home/jokoalmi/joko-lab"


def base():
    return os.environ.get("PUENTE_BASE") or os.path.join(
        repo_root(), "04-operations", "puente-gemini")


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", "-", t.lower()).strip("-")
    return (t[:48] or "tema")


def ahora():
    return datetime.now()


def fichero_prompt(tema, herramienta, contexto, nota_interna):
    ts = ahora().strftime("%Y-%m-%d-%H%M")
    nombre = f"{ts}-{slug(tema)}.md"
    bloque_ctx = contexto.strip() if contexto else "<completar: extracto minimo necesario>"
    txt = f"""# Puente Gemini — {tema}

- **Preparado:** {ahora().strftime('%Y-%m-%d %H:%M')}
- **Herramienta prevista:** {herramienta}
- **Fichero:** {nombre}
- **[NO PEGAR]:** credenciales/claves/tokens · datos de terceros · sesiones o logs completos
"""
    if nota_interna:
        txt += f"- **Nota interna (no pegar):** {nota_interna}\n"
    txt += f"""
## PROMPT (copiar SOLO el bloque de abajo)

```
<completar: rol + objetivo + formato de salida + puntos obligatorios 1..N>

CONTEXTO:
{bloque_ctx}

SALIDA: <estructura pedida>. Si un dato no esta en el contexto, escribe
"no aparece en el contexto" en vez de inventarlo.
```

## Como devolver

Guarda la respuesta completa, sin editar, como `inbox/{ts}-{slug(tema)}-respuesta.txt`
y avisa por Telegram: «trae el inbox». Luego el LAB la verifica y la archiva.
"""
    return nombre, txt


def orden_nuevo(args):
    b = base()
    out = os.path.join(b, "outbox")
    if not os.path.isdir(out):
        return f"ABORTA: no existe {out}"
    herramienta = args.herramienta
    if herramienta not in HERRAMIENTAS:
        return f"ABORTA: herramienta '{herramienta}' no valida. Opciones: {', '.join(HERRAMIENTAS)}"
    contexto = None
    if args.contexto:
        p = os.path.expanduser(args.contexto)
        if not os.path.isfile(p):
            return f"ABORTA: no existe el contexto {p}"
        tam = os.path.getsize(p)
        aviso = ""
        if tam > TOPE_CONTEXTO:
            aviso = f"\n  AVISO: el contexto pesa {tam} B; valora recortarlo (1M de Gemini no obliga a volcar todo)."
        contexto = open(p, encoding="utf-8", errors="replace").read()
        print(f"contexto: {p} ({tam} B){aviso}")
    nombre, txt = fichero_prompt(args.tema, herramienta, contexto, args.nota_interna)
    destino = os.path.join(out, nombre)
    if os.path.exists(destino):
        return f"ABORTA: ya existe {destino}"
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return (f"OK — prompt creado\n  {destino}\n  herramienta: {herramienta}\n"
            f"  siguiente paso (usuario): abrir el fichero, copiar el bloque PROMPT, pegarlo en Gemini web,\n"
            f"  y guardar la respuesta como inbox/{nombre[:-3]}-respuesta.txt")


def orden_estado(_args):
    b = base()
    lineas = [f"puente: {b}"]
    for nombre in ("outbox", "inbox", "procesados"):
        d = os.path.join(b, nombre)
        if not os.path.isdir(d):
            lineas.append(f"- {nombre}/: NO EXISTE")
            continue
        ficheros = sorted(f for f in os.listdir(d) if not f.startswith("."))
        lineas.append(f"- {nombre}/: {len(ficheros)}")
        for f in ficheros[-6:]:
            lineas.append(f"    {f}  ({os.path.getsize(os.path.join(d, f))} B)")
    reg = os.path.join(b, "registro-puente.md")
    lineas.append("- ultimos movimientos:")
    if os.path.isfile(reg):
        movs = [l.rstrip() for l in open(reg, encoding="utf-8") if l.startswith("- ")]
        lineas += [f"    {m}" for m in movs[-5:]] or ["    (registro sin lineas)"]
    else:
        lineas.append("    (no existe registro-puente.md)")
    return "\n".join(lineas)


def orden_archivar(args):
    b = base()
    inbox = os.path.join(b, "inbox")
    proc = os.path.join(b, "procesados")
    fichero = os.path.basename(args.fichero)
    origen = os.path.join(inbox, fichero)
    if not os.path.isfile(origen):
        candidatos = [f for f in os.listdir(inbox) if not f.startswith(".")] if os.path.isdir(inbox) else []
        return (f"ABORTA: no existe {origen}\n  en inbox hay: {', '.join(candidatos) or '(vacio)'}")
    if args.valor is not None and not 1 <= args.valor <= 5:
        return "ABORTA: --valor debe estar entre 1 y 5"
    os.makedirs(proc, exist_ok=True)
    destino = os.path.join(proc, fichero)
    if os.path.exists(destino):
        return f"ABORTA: ya archivado antes ({destino})"
    shutil.move(origen, destino)
    tema = fichero[:-4] if fichero.endswith(".txt") else fichero
    tema = re.sub(r"^\d{4}-\d{2}-\d{2}-\d{4}-", "", tema)
    tema = re.sub(r"-respuesta$", "", tema)
    valor = str(args.valor) if args.valor is not None else "?"
    linea = (f"- {ahora().strftime('%Y-%m-%d %H:%M')} · {tema} · {args.herramienta} · "
             f"valor {valor} · local: {args.local} · {args.nota or '(sin nota)'}")
    reg = os.path.join(b, "registro-puente.md")
    if os.path.isfile(reg):
        contenido = open(reg, encoding="utf-8").read()
        # quita el placeholder inicial, sea cual sea su redaccion/acentos
        contenido = "\n".join(l for l in contenido.splitlines() if not l.startswith("(ninguno"))
        contenido = contenido.rstrip("\n") + "\n"
        with open(reg, "w", encoding="utf-8") as fh:
            fh.write(contenido + linea + "\n")
    return (f"OK — archivado\n  {destino}\n  registro: {linea}\n"
            f"  PENDIENTE: verificar la respuesta contra datos reales (gate-veracidad) antes de usarla.")


def main():
    p = argparse.ArgumentParser(description="Puente manual LAB <-> Gemini web")
    sub = p.add_subparsers(dest="orden", required=True)
    n = sub.add_parser("nuevo", help="crea el prompt en outbox/")
    n.add_argument("tema")
    n.add_argument("--herramienta", default="3.1-pro", choices=HERRAMIENTAS)
    n.add_argument("--contexto", default=None, help="fichero de texto con el contexto a incluir")
    n.add_argument("--nota-interna", default=None)
    n.set_defaults(func=orden_nuevo)
    e = sub.add_parser("estado", help="que hay pendiente")
    e.set_defaults(func=orden_estado)
    a = sub.add_parser("archivar", help="mueve inbox/ -> procesados/ y registra")
    a.add_argument("fichero")
    a.add_argument("--valor", type=int, default=None)
    a.add_argument("--herramienta", default="sin-especificar")
    a.add_argument("--local", default="no", choices=("si", "no"))
    a.add_argument("--nota", default=None)
    a.set_defaults(func=orden_archivar)
    args = p.parse_args()
    print(args.func(args))
    return 0


if __name__ == "__main__":
    sys.exit(main())
