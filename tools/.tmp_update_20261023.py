#!/usr/bin/env python3
"""Actualizacion diaria EXP-002 - pasada 23-oct-2026 (solo append; backup previo hecho en shell)."""
import json
from pathlib import Path

BASE = Path("/home/jokoalmi/joko-lab/lpa/experiments/bolsa")
ESTADO = BASE / "estado-juego.json"
LEDGER = BASE / "ledger-operaciones.jsonl"
FECHA = "2026-10-23"
HORA = "22:32:13"
FX = 0.891529

motivo = (
    "Dia 50 del juego: 50a entrada no_operar consecutiva (06-ago a 23-oct; 0 operaciones; "
    "1.000 EUR virtuales intactos). DATOS: snapshot 2026-10-23T22:32:13 con CIERRE OFICIAL DEL DIA "
    "10/23/2026 en los 14 tickers con dato (campo live_close de /api/quote/{ticker}/info, secondaryData "
    "'Closed at ... 4:00 PM ET'); la serie /historical sigue publicando con un dia de retraso (ultimo punto "
    "10/22/2026 en los 14: 28a confirmacion del lag del API). Cierres oficiales del 23-oct y variacion sobre "
    "el 22-oct: NVDA 210,96 (-0,59%); V 408,00 (-1,52%); GOOGL 320,21 (-1,24%); MSFT 524,51 (+0,66%); "
    "AAPL 347,73 (-0,14%); CCL 26,12 (-3,55%); WDC 343,67 (-2,97%); MRVL 228,51 (+2,26%); REGN 805,02 "
    "(-1,72%); PLTR 196,75 (+0,29%); FSLY 24,41 (+8,73%); MCHP 74,05 (-0,65%); UAA 4,67 (-4,40%); "
    "NKE 37,33 (-0,50%). VSCO fuera por serie insuficiente. FX del dia: 1 USD = 0,891529 EUR "
    "(open.er-api.com, actualizado 23-oct-2026 00:02 UTC; EUR/USD ~1,1217); sin posiciones abiertas, "
    "sin impacto operativo. CANDIDATAS_L con el cierre de hoy (2): (1) FSLY 24,41 USD (+8,73%), "
    "patron_live L-swing (con la serie con lag era descendente, REC 1,72%), DD -18,69% desde el maximo de "
    "3 meses 30,02 y REC 10,60% desde el valle de 30 dias 22,07 (fijado AYER): upside al maximo 22,98% "
    "(pasa la referencia del 20%) pero el filtro de recovery FALLA por mucho (10,60% << 50%) = sigue pegada "
    "al valle, seria buy the dip, prohibido por el metodo. Ademas concurren tres descalificadores "
    "independientes: es software/CDN (sector que Dani evita), presenta Q3 2026 el 04-nov-2026 tras el cierre "
    "(evento binario a 8 sesiones, dentro del horizonte de swing; investors.fastly.com 08-oct-2026) y acumula "
    "ventas de insiders en la subida (CEO Kip Compton 9.016 acciones el 20-oct y 284.681,70 USD el 23-oct; "
    "CTO Artur Bergman 993.015,59 USD el 14-oct; americanbankingnews/marketbeat/insidertrades 20-23-oct-2026). "
    "(2) UAA 4,67 USD (-4,40%), patron_live L-swing, DD -34,59% desde 7,14 y REC 9,37% desde 4,27: "
    "upside al maximo 52,89% (pasa de sobra el 20%) pero el filtro de recovery FALLA por mucho (9,37% << 50%) "
    "-> 18a confirmacion de que los dos filtros del juego son CONJUNTOS y no intercambiables; su evento "
    "binario propio (Q2 FY27) es el 06-nov-2026 antes de apertura (comunicado oficial Under Armour 14-oct-2026, "
    "via stocktitan) y el consenso sigue dividido (Barclays Underweight PT 5,00; Morgan Stanley Underweight "
    "PT 4,00; UBS Buy PT 9,00; Baird Neutral PT 5,50 tras retirar su Bearish Fresh Pick el 06-oct; "
    "investing.com/marketbeat). NINGUNA pasa el filtro de entrada. GUARDARRAIL EXTERNO REFORZADO: el Brent "
    "cerro en 116,72 USD (+3,14%, +6% en la semana y tercera semana consecutiva al alza), maximo desde finales "
    "de abril, tras una serie de ataques houthis en Arabia Saudi (sede del Ministerio de Defensa en Riad, "
    "aeropuertos de Dammam y Abha, refineria de Yanbu), la evacuacion de la sede de Saudi Aramco en Dhahran el "
    "22-oct y un vertido de crudo detectado frente a Umm Al Quwain (EAU); octubre es el peor mes de ataques a "
    "navegacion comercial en Ormuz desde que hay registro, Trump descarto negociar con Iran ('algo pasara "
    "relativamente pronto') y NYT publico preparativos de EEUU e Israel para una nueva ofensiva tras las "
    "midterms del 03-nov (Reuters/euronext 23-oct-2026; Boursorama 23-oct-2026; Infobae 23-oct-2026; "
    "economiafinanzas 23-oct-2026). Wall Street en rojo con el petroleo: S&P 500 7.623,86 (-0,52%), Nasdaq "
    "25.955,34 (-0,21%), Dow 52.209,16 (-1,25%), 10 anos al 4,99% (Reuters/AP 23-oct-2026). "
    "AUTOCORRECCION (hipotesis del 22-oct medida): la tesis era que WDC podia ser el primer 'dip de histeria' "
    "del experimento si el beat (ingresos 4.381 M +55% YoY, guia Q2 +12%/+20%) se imponia al selloff; el "
    "cierre de hoy lo REFUTA: WDC 343,67 USD (-2,97% sobre 354,19), sigue descendente (DD -37,35%, REC 3,52%), "
    "es decir el beat no arreglo el patron y la decision de no entrar ayer (con el print a 1 dia) evito otra "
    "perdida. Se mantiene sin posicion. Segundo hallazgo: por tercera vez FSLY cambia de categoria por el "
    "movimiento de UNA sola sesion (+14,9% el 21-sep, +13,69% el 23-sep, +8,73% hoy) - su clasificacion no es "
    "estable con cadencia diaria y hoy ademas entra en L-swing justo cuando arranca su cuenta atras de "
    "resultados; un swing tan inestable no es operable con este instrumento."
)

fuente = (
    "nasdaq.com /api/quote/{ticker}/info y /historical (snapshot 2026-10-23T22:32:13); Reuters via "
    "live.euronext.com y finance.yahoo.com 23-oct-2026 (Brent 116,72-117,18; ataques houthis; Aramco Dhahran; "
    "Trump sin negociacion); AP News 23-oct-2026 (S&P 500 -0,52%, Brent >116, 10y 4,99%); Boursorama 23-oct-2026 "
    "(cierre Brent 116,72 +3,14%, +6% semanal); Infobae 23-oct-2026 (Brent 116,9; bloqueo 100 dias; NYT ofensiva "
    "tras midterms); economiafinanzas.com 23-oct-2026 (Ormuz parcial, vertido EAU, UKMTO); 247wallst 23-oct-2026 "
    "y Simply Wall St 23-oct-2026 (FSLY +8%, JioCDN, proximos resultados); investors.fastly.com 08-oct-2026 "
    "(Q3 2026 el 04-nov); stocktitan/Under Armour 14-oct-2026 (Q2 FY27 el 06-nov); MarketBeat/Investing.com "
    "20-23-oct-2026 (insiders FSLY y ratings UAA); open.er-api.com 23-oct-2026 (FX 0,891529)"
)

# 1) LEDGER (append)
entry = {
    "fecha": FECHA,
    "hora": HORA,
    "tipo": "no_operar",
    "ticker": None,
    "precio_usd": None,
    "precio_entrada_usd": None,
    "precio_salida_usd": None,
    "retorno_pct_usd": None,
    "retorno_pct_eur": None,
    "capital_virtual_eur": 1000.0,
    "posiciones_abiertas": [],
    "fx_usd_eur": FX,
    "horizonte": None,
    "candidatas_L": [
        {
            "ticker": "FSLY",
            "precio_usd": 24.41,
            "var_dia_pct": 8.73,
            "patron": "L-swing",
            "drawdown_pct": -18.69,
            "recovery_pct": 10.60,
            "upside_max_3m_pct": 22.98,
            "filtro_recovery": "FALLA",
            "filtro_upside": "PASA",
            "evento_binario": "Q3 2026 el 04-nov-2026 tras el cierre",
            "sector": "software/CDN (sector a evitar)",
            "categoria": "DESCARTAR",
        },
        {
            "ticker": "UAA",
            "precio_usd": 4.67,
            "var_dia_pct": -4.40,
            "patron": "L-swing",
            "drawdown_pct": -34.59,
            "recovery_pct": 9.37,
            "upside_max_3m_pct": 52.89,
            "filtro_recovery": "FALLA",
            "filtro_upside": "PASA",
            "evento_binario": "Q2 FY27 el 06-nov-2026 antes de apertura",
            "sector": "apparel (en reestructuracion)",
            "categoria": "VIGILAR",
        },
    ],
    "guardarrail_externo": (
        "ACTIVO y REFORZADO - Brent 116,72 USD (+3,14%, +6% semanal, maximo desde finales de abril); "
        "ataques houthis a Riad/Dammam/Abha/Yanbu, evacuacion de Aramco en Dhahran, vertido en EAU; octubre, "
        "peor mes de ataques a navegacion en Ormuz; Trump descarta negociar; EEUU/Israel prepararian ofensiva "
        "tras las midterms del 03-nov"
    ),
    "motivo": motivo,
    "fuente": fuente,
}

with LEDGER.open("a", encoding="utf-8") as f:
    f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# 2) ESTADO (decision + aprendizaje)
estado = json.loads(ESTADO.read_text(encoding="utf-8"))
estado.setdefault("decisiones", []).append({
    "fecha": "2026-10-23T22:32:13+02:00",
    "decision": "no_operar",
    "motivo": motivo,
    "candidatas_ignoradas": ["FSLY", "UAA"],
})
estado.setdefault("aprendizajes", []).append({
    "fecha": FECHA,
    "tema": "la hipotesis del 'dip de histeria' de WDC queda REFUTADA al cierre siguiente (el beat no arregla el patron) y FSLY cambia de categoria por tercera vez en una sola sesion",
    "detalle": (
        "1) AUTOCORRECCION MEDIDA: el 22-oct se dejo WDC en VIGILAR con la hipotesis de que, si el beat "
        "(ingresos 4.381 M USD +55% YoY vs 4,14 mM esperados; guia Q2 5,0-5,2 mM y EPS 5,60-6,00) se imponia "
        "al selloff, seria el primer 'dip de histeria' del experimento. El cierre del 23-oct lo refuta: WDC "
        "343,67 USD (-2,97% sobre 354,19), descendente, DD -37,35% y REC 3,52%. Un print bueno no cambia la "
        "clasificacion del patron cuando el sector sigue en selloff; la regla operativa que se consolida es "
        "'no se entra ni se reabre tesis con el cierre oficial aun en patron roto', y la decision de no entrar "
        "el 21-oct (evento binario a 1 dia) evito una perdida adicional. 2) INSTRUMENTO: FSLY ha cambiado de "
        "categoria por el movimiento de UNA sola sesion tres veces en el experimento (+14,9% el 21-sep, "
        "+13,69% el 23-sep y +8,73% hoy 23-oct, pasando de descendente a L-swing con el mismo cierre). "
        "Consecuencia: su clasificacion no es estable a cadencia diaria, y hoy entra en L-swing justo cuando "
        "arranca la cuenta atras de sus resultados (04-nov) y con ventas de insiders durante la subida "
        "(CEO Compton 9.016 acciones el 20-oct y 284.681,70 USD el 23-oct; CTO Bergman 993.015,59 USD el "
        "14-oct). Para el lab: un ticker cuyo patron se invierte en una sesion no es operable con este "
        "instrumento aunque cumpla los filtros al cierre. 3) El filtro de recovery sigue siendo el cuello de "
        "botella estructural (18a confirmacion de filtros conjuntos): las dos candidatas pasan el upside al "
        "maximo (FSLY 22,98%, UAA 52,89%) y fallan REC (10,60% y 9,37%), y ambas tienen evento binario dentro "
        "del horizonte de swing (04-nov y 06-nov). 4) Guardarrail con el shock energetico mas fuerte del mes: "
        "Brent 116,72 USD (+3,14%, +6% semanal) tras los ataques houthis a infraestructura saudita y con "
        "EEUU/Israel preparando una ofensiva tras las midterms del 03-nov; ninguno de los tres criterios "
        "explicitos de levantamiento se cumple. 5) FX del dia 0,891529 USD/EUR (sin posiciones, sin impacto)."
    ),
    "fuente": fuente,
})
ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("OK ledger lineas:", sum(1 for _ in LEDGER.open(encoding="utf-8")))
print("OK decisiones:", len(estado["decisiones"]), "aprendizajes:", len(estado["aprendizajes"]))
print("posiciones:", estado["posiciones"], "capital_libre_eur:", estado["capital_libre_eur"])
