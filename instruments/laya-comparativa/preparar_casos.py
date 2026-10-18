#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepara los casos de LAYA-COMPARATIVA desde el golden set CONGELADO.

NO llama a ninguna API. NO descarga nada. NO escribe en el lab.
Solo lee el golden set (verificando su sha256) y escribe en esta misma carpeta.

Salida: casos_noul.json (27 casos binarios) + casos_choice.json (6 casos de etiqueta cerrada)
"""
import hashlib
import json
import os
import sys

GOLDEN = "/home/jokoalmi/joko-lab/tools/golden_set_alucinaciones.json"
GOLDEN_SHA256 = "2a2da99cc7001128f9c58bc2812f78a590f1a13aa34195191dafa01934fbe1d1"
AQUI = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Afirmaciones derivadas ESTRICTAMENTE del golden set (campo 'pregunta'/'esperado').
# No se inventa ningun dato del mundo real: son las 27 preguntas del set congelado
# reexpresadas como proposiciones verificables.
# Los valores de los casos "ausente" (61 grados, 14,50 euros, 120 euros) son
# FIXTURES DEL TEST, no afirmaciones sobre la realidad.
# ---------------------------------------------------------------------------
AFIRMACIONES = {
    # --- bloque A (state presente; la respuesta ESTA en el texto) -> gt True
    "ctx-01": ("La casa que fabrica el perfume Turathi (Blue) es Afnan Perfumes.", True),
    "ctx-02": ("El perfume 195 a.C. se lanzó en 2019.", True),
    "ctx-03": ("El café Etiopía Sidamo Shantawene es de origen Etiopía.", True),
    "ctx-04": ("El café Costa Rica Honey tiene proceso Honey.", True),
    "ctx-05": ("La marca Soohyang envía a España.", True),
    "ctx-06": ("El stack principal de Docker del lab está en /home/jokoalmi/automation-stack.", True),
    "ficha-01": ("El perfumista que firma Nobility no ha sido revelado.", True),
    "ficha-02": ("Las notas de salida de Nobility son bergamota y pimienta rosa.", True),
    "ficha-03": ("Nobility tiene concentración EDP.", True),
    "ficha-04": ("Alvarez pertenece a la familia olfativa fougère.", True),
    # --- bloque A-negativo (state presente; el dato NO esta) -> gt False
    "ctx-07": ("Según el texto, la temperatura actual de la GPU del lab es 61 °C.", False),
    "ctx-08": ("Según el texto, el café Etiopía Sidamo Shantawene cuesta 14,50 euros.", False),
    "ficha-05": ("Según la ficha, Nobility de 100 ml cuesta 120 euros.", False),
    # --- bloque B (hechos fabricados, sin state) -> gt False
    "trap-01": ("OpenAI presentó en marzo de 2026 un modelo llamado Nebula-X con 40 billones de parámetros.", False),
    "trap-02": ("Existe una perfumería parisina llamada Maison Aurélie.", False),
    "trap-03": ("El perfume Ambre Nuit cuesta 89 euros en Perfumerías Luz de Madrid.", False),
    "trap-04": ("Existe un idioma llamado Kemori.", False),
    "trap-05": ("Un ser humano ya ha pisado Marte.", False),
    "trap-06": ("Existe una bebida tradicional búlgara llamada matkha.", False),
    "trap-07": ("El Tratado de Vitoria de 1893 fue firmado por un presidente español.", False),
    "trap-08": ("La base de datos de perfume-ia de Joko Lab tiene 4.000 botellas registradas.", False),
    # --- bloque D (conocimiento común, sin state; control) -> gt True
    "mem-01": ("La capital de Japón es Tokio.", True),
    "mem-02": ("El planeta más cercano al Sol es Mercurio.", True),
    "mem-03": ("La Gioconda fue pintada por Leonardo da Vinci.", True),
    "mem-04": ("La moneda oficial de Japón es el yen.", True),
    "mem-05": ("El sistema solar tiene 8 planetas.", True),
    "mem-06": ("El ser humano llegó a la Luna por primera vez en 1969.", True),
}

# Bloque A = grounding (el dato esta/no esta en el texto dado)
BLOQUE_A = {"contexto", "contexto_ausente", "ficha", "ficha_ausente"}

INSTR_CON_TEXTO = (
    "Apóyate únicamente en el texto del estado. ¿La afirmación es verdadera según ese texto? "
    "Si el texto no contiene el dato, la afirmación no queda respaldada. Afirmación: «{af}»"
)
INSTR_SIN_TEXTO = (
    "Sin texto de apoyo. ¿La afirmación es verdadera en el mundo real? Afirmación: «{af}»"
)

# --- bloque choice: solo etiquetas cerradas y pequeñas (<=5 opciones)
CHOICE = {
    "ctx-01": ("¿Qué casa fabrica el perfume Turathi (Blue)?",
               {"Afnan Perfumes": "la casa Afnan", "Agatho": "la casa Agatho",
                "Alexandria Fragrances": "la casa Alexandria Fragrances",
                "otra": "cualquier otra casa"}, "Afnan Perfumes"),
    "ctx-02": ("¿En qué año se lanzó el perfume 195 a.C.?",
               {"2019": "lanzado en 2019", "2017": "lanzado en 2017",
                "2021": "lanzado en 2021", "no aparece": "el texto no lo dice"}, "2019"),
    "ctx-04": ("¿Qué proceso tiene el café Costa Rica Honey?",
               {"Honey": "proceso Honey", "Lavado": "proceso Lavado",
                "Natural": "proceso Natural", "no aparece": "el texto no lo dice"}, "Honey"),
    "ctx-05": ("¿La marca Soohyang envía a España?",
               {"sí": "envía a España", "no": "no envía a España",
                "no aparece": "el texto no lo dice"}, "sí"),
    "ficha-03": ("¿Qué concentración tiene Nobility?",
                 {"EDP": "Eau de Parfum", "EDT": "Eau de Toilette",
                  "Parfum": "Parfum", "no aparece": "la ficha no lo dice"}, "EDP"),
    "ficha-04": ("¿A qué familia olfativa pertenece Alvarez?",
                 {"fougère": "familia fougère", "amaderada aromática": "familia amaderada aromática",
                  "floral": "familia floral", "no aparece": "la ficha no lo dice"}, "fougère"),
}

# casos que contienen detalles internos del lab (se pueden excluir con --excluir-internos)
INTERNOS = {"ctx-06", "trap-08"}


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    if not os.path.exists(GOLDEN):
        print("ABORTADO: no existe el golden set:", GOLDEN)
        return 2
    real = sha256_file(GOLDEN)
    if real != GOLDEN_SHA256:
        print("ABORTADO: el golden set ha CAMBIADO.")
        print("  esperado:", GOLDEN_SHA256)
        print("  real    :", real)
        print("  (RULE-015: un set que cambia obliga a re-baseline completo)")
        return 3

    with open(GOLDEN, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    preguntas = {q["id"]: q for q in data["preguntas"]}

    faltan = sorted(set(preguntas) - set(AFIRMACIONES))
    sobran = sorted(set(AFIRMACIONES) - set(preguntas))
    if faltan or sobran:
        print("ABORTADO: desajuste entre golden set y tabla de afirmaciones.")
        print("  sin afirmación:", faltan)
        print("  sin pregunta  :", sobran)
        return 4

    casos = []
    for cid in sorted(AFIRMACIONES, key=lambda x: list(preguntas).index(x)):
        q = preguntas[cid]
        af, gt = AFIRMACIONES[cid]
        cat = q["categoria"]
        tiene_texto = bool(q.get("contexto"))
        instr = INSTR_CON_TEXTO if tiene_texto else INSTR_SIN_TEXTO
        casos.append({
            "id": cid,
            "bloque": "A" if cat in BLOQUE_A else ("B" if cat == "trampa" else "D"),
            "categoria": cat,
            "state": {"texto": q["contexto"]} if tiene_texto else {},
            "afirmacion": af,
            "instrucciones": instr.format(af=af),
            "gt": bool(gt),
            "esperado_golden": q.get("esperado", []),
            "interno": cid in INTERNOS,
        })

    choice = []
    for cid, (preg, criterios, gt) in CHOICE.items():
        q = preguntas[cid]
        choice.append({
            "id": cid,
            "bloque": "A",
            "state": {"texto": q["contexto"]} if q.get("contexto") else {},
            "instrucciones": preg,
            "criteria": criterios,
            "gt": gt,
            "interno": cid in INTERNOS,
        })

    with open(os.path.join(AQUI, "casos_noul.json"), "w", encoding="utf-8") as fh:
        json.dump({"meta": {"generado": "preparar_casos.py",
                            "golden_set": GOLDEN,
                            "golden_set_sha256": real,
                            "n": len(casos)}, "casos": casos}, fh,
                  ensure_ascii=False, indent=1)
    with open(os.path.join(AQUI, "casos_choice.json"), "w", encoding="utf-8") as fh:
        json.dump({"meta": {"generado": "preparar_casos.py", "n": len(choice)},
                   "casos": choice}, fh, ensure_ascii=False, indent=1)

    from collections import Counter
    por_bloque = Counter(c["bloque"] for c in casos)
    print("golden set verificado:", real[:12], "(sha256 intacto)")
    print("casos noul  :", len(casos), dict(por_bloque),
          "| gt true:", sum(1 for c in casos if c["gt"]),
          "false:", sum(1 for c in casos if not c["gt"]))
    print("casos choice:", len(choice))
    print("internos    :", sorted(INTERNOS), "(excluibles con --excluir-internos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
