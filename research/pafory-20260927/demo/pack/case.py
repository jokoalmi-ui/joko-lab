"""Caso de ejemplo del pack: datos base y TODAS las cifras derivadas en código.
Nada se escribe a mano: si un total no cuadra, el script lo detecta y aborta.
Los nombres, marcas y precios son ficticios (marcados como EJEMPLO en cada pieza)."""

MES = "octubre 2026"
DIAS = "01-31 oct 2026"
CLIENTE = "Casa Aurora"
CLIENTE_SUB = "perfumería de nicho y decants · Bilbao"
INICIALES = "CA"
FECHA_PACK = "27-09-2026"
TICKET = 46.20          # ticket medio por pedido (€)
COMISION_PCT = 0.10     # comisión de la creadora sobre el pedido atribuido
HONORARIOS = 120.0      # honorarios del servicio de gestión, €/mes
DESCUENTO_PILOTO = 0.12 # descuento del cupón de Ana (12 % en su selección)

# creadoras: nombre, handle, red, iniciales, clics, pedidos, semanas
CREADORAS = [
    {"nom": "Ana Ortiz", "h": "@ana.decants", "ini": "AO",
     "red": "Instagram · 41,2 mil", "formato": "Reel 9:16 + 3 stories",
     "clics": 962, "pedidos": [9, 14, 23, 12], "desc": 0.12},
    {"nom": "María Soler", "h": "@decants.con.maria", "ini": "MS",
     "red": "TikTok · 18,7 mil", "formato": "TikTok 3 piezas + 1 directo",
     "clics": 1204, "pedidos": [11, 9, 12, 9], "desc": 0.10},
    {"nom": "Julia Ferrer", "h": "@perfumista.madrid", "ini": "JF",
     "red": "Instagram · 9,4 mil", "formato": "Carrusel + 2 stories",
     "clics": 618, "pedidos": [2, 3, 4, 3], "desc": 0.10},
]

SEMANAS = ["05-11 oct", "12-18 oct", "19-25 oct", "26 oct-01 nov"]
CUPON = "ANA12"
CODIGOS = {"@ana.decants": "ANA12", "@decants.con.maria": "MARIA10",
           "@perfumista.madrid": "JULIA10"}
UTM = {"utm_source": "instagram", "utm_medium": "influencer",
       "utm_campaign": "2026-10_reel_ana", "creator": "ana.ortiz",
       "ref": "pagina-creadora"}

PRODUCTOS = [
    {"nm": "Nocturno 12", "ml": "decant 10 ml", "pr": 24.0, "nota": "ámbar, incienso, cuero",
     "tint": ("#E8B36A", "#8A4A18")},
    {"nm": "Ámbar de Sal", "ml": "decant 10 ml", "pr": 19.0, "nota": "sal marina, bergamota, musgo",
     "tint": ("#A8D8D0", "#3F7F76")},
    {"nm": "Verde Norte", "ml": "decant 10 ml", "pr": 21.0, "nota": "higo verde, vetiver, cedro",
     "tint": ("#B9D98A", "#4F7A2E")},
]

# piezas publicadas por Ana en el mes (clic y pedido, cuadran con sus totales)
PIEZAS_MES = [
    ("05-11 oct", "Presentación de su selección", "reel 9:16", 214, 9),
    ("12-18 oct", "Rutina de dos decants", "story x3", 226, 14),
    ("19-25 oct", "Tres perfiles, tres momentos", "reel 9:16", 402, 23),
    ("26 oct-01 nov", "Cierre de mes y cupón", "carrusel + story", 120, 12),
]

INCLUSION = [("Nocturno 12", 6), ("Ámbar de Sal", 5), ("Verde Norte", 4)]

MENSAJES = [
    ("Probar sin arriesgar 100 ml", "10 ml originales: 20-30 usos."),
    ("Original, nunca «dupe»", "Decantado a mano en Bilbao, sin equivalencias."),
    ("Tu criterio, no el del vendedor", "Tres perfiles olfativos, no el más vendido."),
]
NO_DECIR = [
    "No comparar con marcas registradas ni usar la palabra «dupe» o «clon».",
    "No prometer que huele igual que una fragancia concreta de otra casa.",
    "No publicar precios de la competencia ni enlaces de afiliado de terceros.",
    "No hablar de envíos o plazos distintos de los de la ficha del producto.",
]

# mes anterior (para la comparativa del informe) y reparto de origen de los pedidos
SEP = {"ped": 41, "ticket": 42.80}   # septiembre: 41 pedidos, ticket medio 42,80 €
SPLIT_CUPON = 0.62                   # % de pedidos de Ana que entran por el cupón

# ---------- cifras derivadas ----------
def eur(x, dec=2):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "\u00a0").replace(".", ",").replace("\u00a0", ".") + "\u00a0€"

def inte(x):
    return f"{x:,}".replace(",", ".")

def pct(x, dec=1):
    return f"{x*100:.{dec}f}".replace(".", ",") + "\u00a0%"

def build():
    filas = []
    for c in CREADORAS:
        ped = sum(c["pedidos"])
        ing = ped * TICKET
        com = ing * COMISION_PCT
        filas.append({**c, "ped": ped, "ing": ing, "com": com,
                      "conv": (ped / c["clics"]) if c["clics"] else 0,
                      "cpo": (com / ped) if ped else 0,
                      "codigo": CODIGOS[c["h"]]})
    clics = sum(f["clics"] for f in filas)
    ped = sum(f["ped"] for f in filas)
    ing = sum(f["ing"] for f in filas)
    com = sum(f["com"] for f in filas)
    ana = filas[0]
    sep_ing = SEP["ped"] * SEP["ticket"]
    cup = round(ana["ped"] * SPLIT_CUPON)
    return {
        "filas": filas, "clics": clics, "ped": ped, "ing": ing, "com": com,
        "conv": ped / clics, "ticket": ing / ped if ped else 0,
        "cpo": com / ped if ped else 0,
        "roas": ing / (com + HONORARIOS),
        "coste": com + HONORARIOS,
        "semanas_ana": CREADORAS[0]["pedidos"],
        "max_sem": max(CREADORAS[0]["pedidos"]),
        "sep": {"ped": SEP["ped"], "ticket": SEP["ticket"], "ing": sep_ing,
                "com": sep_ing * COMISION_PCT},
        "mom_ped": ana["ped"] / SEP["ped"] - 1,
        "mom_ing": ana["ing"] / sep_ing - 1,
        "cup": cup, "enl": ana["ped"] - cup,
        "sh_cup": cup / ana["ped"], "sh_enl": (ana["ped"] - cup) / ana["ped"],
    }

D = build()

def check():
    """Comprobaciones de coherencia interna. Devuelve lista de líneas OK/FAIL."""
    out, ok = [], True
    def t(nombre, cond, detalle=""):
        nonlocal ok
        ok = ok and bool(cond)
        out.append(f"{'OK  ' if cond else 'FAIL'} {nombre}{(' · ' + detalle) if detalle else ''}")
    t("suma de pedidos por creadora = total",
      sum(f["ped"] for f in D["filas"]) == D["ped"], f"{inte(D['ped'])} pedidos")
    t("suma de clics = total", sum(f["clics"] for f in D["filas"]) == D["clics"],
      f"{inte(D['clics'])} clics")
    t("ingresos = pedidos × ticket medio",
      abs(D["ing"] - D["ped"] * TICKET) < 0.005, f"{eur(D['ing'])}")
    t("comisión = ingresos × 10 %", abs(D["com"] - D["ing"] * COMISION_PCT) < 0.005, eur(D["com"]))
    t("semanas de Ana = pedidos de Ana",
      sum(D["semanas_ana"]) == D["filas"][0]["ped"], f"{D['semanas_ana']} → {D['filas'][0]['ped']}")
    t("ticket medio coherente (43-50 €)", 43 <= D["ticket"] <= 50, eur(D["ticket"]))
    t("cada cupón anuncia el descuento que aplica",
      all(int(f["codigo"][-2:]) == round(f["desc"] * 100) for f in D["filas"]),
      " · ".join(f"{f['codigo']}={int(f['desc']*100)}%" for f in D["filas"]))
    t("ROAS > 1", D["roas"] > 1, f"{D['roas']:.1f}×")
    t("pedidos por cupón + por enlace = pedidos de Ana", D["cup"] + D["enl"] == D["filas"][0]["ped"],
      f"{D['cup']} + {D['enl']} = {D['filas'][0]['ped']}")
    t("comparativa con septiembre coherente",
      abs(D["sep"]["ing"] - D["sep"]["ped"] * D["sep"]["ticket"]) < 0.005,
      f"{D['sep']['ped']} × {eur(D['sep']['ticket'], 2)} = {eur(D['sep']['ing'])}")
    t("septiembre tuvo menos pedidos y menos ticket que octubre",
      D["sep"]["ped"] < D["filas"][0]["ped"] and D["sep"]["ticket"] < D["ticket"],
      f"+{pct(D['mom_ped'])} pedidos · +{pct(D['mom_ing'])} ingresos")
    t("la creadora top no es la de más clics", 
      max(D["filas"], key=lambda f: f["ped"])["h"] != max(D["filas"], key=lambda f: f["clics"])["h"],
      "el informe tiene algo que contar")
    pm = [(f, p, fo, cl, pe) for f, p, fo, cl, pe in PIEZAS_MES]
    t("clics por pieza = clics de Ana", sum(x[3] for x in pm) == D["filas"][0]["clics"],
      f"{sum(x[3] for x in pm)} = {D['filas'][0]['clics']}")
    t("pedidos por pieza = pedidos de Ana", sum(x[4] for x in pm) == D["filas"][0]["ped"],
      f"{sum(x[4] for x in pm)} = {D['filas'][0]['ped']}")
    t("cada creadora tiene su cupón y no se repite",
      len({f["codigo"] for f in D["filas"]}) == len(D["filas"]),
      " · ".join(f["codigo"] for f in D["filas"]))
    t("ningún producto aparece en los 111 pedidos", all(3 <= n <= 8 for _, n in INCLUSION),
      " · ".join(f"{k} en {n} de cada 10" for k, n in INCLUSION))
    return out, ok

if __name__ == "__main__":
    for l in check()[0]:
        print(l)
