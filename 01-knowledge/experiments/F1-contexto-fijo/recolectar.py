#!/usr/bin/env python3
"""F1 / Fase F1.0 — RECOLECCIÓN de las piezas reales del contexto fijo.

SOLO LECTURA sobre ~/.hermes y ~/joko-lab. No llama a ningún modelo, no toca config.
Salida: /tmp/f1-contexto/piezas.json  (con inventario de tamaños y cobertura)

Uso:  python3 recolectar.py
"""
import json
import os
import re
import subprocess
import sys

H = "/home/jokoalmi/.hermes"
LAB = "/home/jokoalmi/joko-lab"
SAL = "/tmp/f1-contexto/piezas.json"

# --- piezas exactas de fichero -------------------------------------------------
FICHEROS = {
    "B1_soul": f"{H}/SOUL.md",
    "B2_memoria": f"{H}/memories/MEMORY.md",
    "B2_user": f"{H}/memories/USER.md",
    "config_yaml": f"{H}/config.yaml",
    "snapshot_skills": f"{H}/.skills_prompt_snapshot.json",
}


def leer(p):
    """Devuelve el texto o None. None = no_calculable (NUNCA se imputa cadena vacía)."""
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def frontmatter(txt):
    """name/description del frontmatter YAML sin PyYAML. Devuelve (name, desc, multilinea)."""
    if not txt or not txt.startswith("---"):
        return None, None, False
    fin = txt.find("\n---", 3)
    if fin < 0:
        return None, None, False
    fm = txt[3:fin]
    name = desc = None
    multilinea = False
    lineas = fm.splitlines()
    for i, ln in enumerate(lineas):
        if name is None:
            m = re.match(r"\s*name:\s*(.+?)\s*$", ln)
            if m:
                name = m.group(1).strip("\"'")
        if desc is None:
            m = re.match(r"\s*description:\s*(.*?)\s*$", ln)
            if m:
                val = m.group(1).strip()
                if val in ("|", ">", "|-", ">-", ""):
                    # descripción plegada: unir las líneas indentadas siguientes
                    partes = []
                    for sig in lineas[i + 1:]:
                        if re.match(r"\s+\S", sig):
                            partes.append(sig.strip())
                        elif sig.strip() == "":
                            continue
                        else:
                            break
                    desc = " ".join(partes)
                    multilinea = True
                else:
                    desc = val.strip("\"'")
    return name, desc, multilinea


def skills_activas():
    """Rutas de SKILL.md bajo ~/.hermes/skills y ~/.hermes/plugins/**/skills."""
    fuera = []
    for raiz in (f"{H}/skills", f"{H}/plugins"):
        if not os.path.isdir(raiz):
            continue
        for dirpath, _dirnames, filenames in os.walk(raiz):
            for fn in filenames:
                if fn == "SKILL.md":
                    fuera.append(os.path.join(dirpath, fn))
    return sorted(fuera)


def bloque_skills(rutas):
    """Reconstruye el índice de skills con el formato observado en el prompt:
         <categoria>:
           - <name>: <description>
    Devuelve (texto, avisos)."""
    porcat = {}
    sin_desc = []
    con_desc = 0
    for p in rutas:
        txt = leer(p)
        name, desc, _ml = frontmatter(txt)
        rel = os.path.relpath(p, f"{H}/skills") if p.startswith(f"{H}/skills") else \
              os.path.relpath(p, f"{H}/plugins")
        partes = rel.split(os.sep)
        cat = partes[0] if len(partes) > 2 else "(raiz)"
        nom = name or partes[-2]
        if desc:
            con_desc += 1
        else:
            sin_desc.append(nom)
            continue
        porcat.setdefault(cat, []).append(f"    - {nom}: {desc}")
    lineas = []
    for cat in sorted(porcat):
        lineas.append(f"  {cat}:" if cat != "(raiz)" else "  (sin categoria):")
        lineas.extend(sorted(porcat[cat]))
    avisos = {
        "skills_encontradas": len(rutas),
        "en_dir_skills": sum(1 for r in rutas if r.startswith(f"{H}/skills")),
        "en_plugins": sum(1 for r in rutas if r.startswith(f"{H}/plugins")),
        "con_descripcion": con_desc,
        "sin_descripcion": len(sin_desc),
        "sin_descripcion_lista": sin_desc[:20],
        "formato": "reconstruido (categoria -> name: description); NO es el string literal del runtime",
        "cota": ("SUPERIOR, no exacta: se cuentan las SKILL.md presentes en disco. En el perfil "
                 "default el config.yaml no define `skills.disabled` (comprobado), asi que en "
                 "principio todas estan activas; si el runtime lista menos, la diferencia es "
                 "visibilidad/plugins y hay que declararla, no imputarla"),
    }
    return "\n".join(lineas), avisos


def main():
    os.makedirs("/tmp/f1-contexto", exist_ok=True)
    piezas = {"_meta": {}}

    # hora real (RULE-012): del sistema, no del reloj del modelo
    try:
        piezas["_meta"]["fecha"] = subprocess.run(
            ["date", "-Iseconds"], capture_output=True, text=True).stdout.strip()
    except OSError:
        piezas["_meta"]["fecha"] = "no_calculable"

    inventario = {}
    for k, p in FICHEROS.items():
        t = leer(p)
        piezas[k] = t
        inventario[k] = {"ruta": p, "existe": t is not None,
                         "bytes": os.path.getsize(p) if t is not None else None,
                         "chars": len(t) if t is not None else None}

    # config: solo las claves que definen el contexto (no el fichero entero)
    cfg = piezas.get("config_yaml") or ""
    mk = {}
    for clave in ("toolsets", "mcp_servers", "platform_toolsets", "model:", "delegation"):
        mk[clave] = (
            f"presente (linea {cfg[:cfg.find(chr(10)*0)+len(cfg)].count(chr(10))+1})"
            if clave in cfg else "AUSENTE en config.yaml")
    piezas["_meta"]["config_claves"] = mk

    rutas = skills_activas()
    texto_skills, avisos = bloque_skills(rutas)
    piezas["B3_skills"] = texto_skills
    piezas["_meta"]["skills"] = avisos
    inventario["B3_skills"] = {"ruta": f"{len(rutas)} SKILL.md", "existe": True,
                               "bytes": None, "chars": len(texto_skills)}

    # B4: no hay string literal de las herramientas en disco -> se declara
    piezas["B4_tools_hermescli"] = None
    piezas["_meta"]["B4"] = ("NO DISPONIBLE COMO TEXTO: las definiciones del toolset hermes-cli "
                             "las construye el runtime. Fase F1.4 las obtiene del MCP real; "
                             "para las nativas, se mide por diferencia con el ledger o se pide "
                             "un volcado explicito al runtime.")
    inventario["B4_tools_hermescli"] = {"ruta": None, "existe": False, "bytes": None, "chars": None}

    piezas["_meta"]["inventario"] = inventario
    with open(SAL, "w", encoding="utf-8") as f:
        json.dump(piezas, f, ensure_ascii=False, indent=1)

    # resumen por stdout (corto, sin volcar contenidos)
    print(f"escrito: {SAL}  ({os.path.getsize(SAL)} B)")
    print(f"fecha: {piezas['_meta']['fecha']}")
    for k, v in inventario.items():
        print(f"  {k:22s} chars={v['chars']}")
    print(f"  skills: {avisos['skills_encontradas']} encontradas, "
          f"{avisos['con_descripcion']} con descripcion, {avisos['sin_descripcion']} sin ella")
    if avisos["sin_descripcion"]:
        print(f"  sin descripcion (primeras): {avisos['sin_descripcion_lista']}")


if __name__ == "__main__":
    sys.exit(main())
