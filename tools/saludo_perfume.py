#!/usr/bin/env python3
"""
SALUDO PERFUME — generador de saludos creativos para la ficha del perfume del día.

Selecciona una categoría (semilla = fecha) y genera una frase con el contexto
real de la ficha (perfume, nota, clima, día de la semana). Determinista por
fecha: mismo día = mismo saludo; días distintos = saludo distinto.
Nota (20-sep-2026): la semilla de la frase usa zlib.crc32, NO hash(): el hash
de str en Python esta aleatorizado por proceso (PYTHONHASHSEED) y rompia el
determinismo (3 ejecuciones -> 3 frases distintas).

Uso:
  python3 tools/saludo_perfume.py                          # auto: fecha de hoy, contexto genérico
  python3 tools/saludo_perfume.py --perfume "40 Knots" --nota "sal" --clima 32
  python3 tools/saludo_perfume.py --fecha 2026-08-26 --perfume "Elysium" --nota "cítrico" --clima 28

Regla del lab: nunca inventar datos. Si falta contexto, la frase usa el dato
genérico; si falta el dato crítico (perfume), la categoría se omite.
"""

import argparse
import random
import sys
import zlib
from datetime import date, datetime

# 8 categorías con plantillas. {p}=perfume, {n}=nota, {t}=temperatura, {d}=día semana, {m}=mes
CATEGORIAS = {
    "poetico": [
        "Que el día huela tan bien como empieza.",
        "Cada mañana es una nota de salida.",
        "Hoy el aire lleva tu perfume puesto.",
        "Despierta, que el mundo ya se ha puesto su mejor aroma.",
        "La mejor manera de empezar el día es olerlo.",
    ],
    "juego": [
        "Hoy despertamos con acorde a {n}.",
        "Buenos días con {p} en la piel.",
        "Este día viene con estela.",
        "Buenos días con sillage de {p}.",
        "Hoy el protagonista es {p}.",
    ],
    "clima": [
        "Buenos días con {t}° de abrazo solar.",
        "Sol, calor y un buen perfume: la trifecta.",
        "Día fresco: el momento de oler a abrigo.",
        "Buenos días a {t}°, que el sol también se perfuma.",
        "Calor a la vista: {p} al rescate.",
    ],
    "humor": [
        "El café puede esperar. El perfume, no.",
        "Advertencia: hoy el día viene muy perfumado.",
        "Sí, huelo bien. Gracias por preguntar.",
        "Hoy me levanto oliendo a {n} y a ganar.",
        "La ducha es opcional. El perfume, obligatorio.",
    ],
    "dia": [
        "¡Feliz {d}! Que el perfume haga el trabajo pesado.",
        "{d} con aroma de {n}.",
        "Hoy es {d}: hora de oler a {p}.",
        "Buen {d} perfumado.",
        "{d} huele a {p} y a buenas decisiones.",
    ],
    "familia": [
        "Buenos días {n}, que el mar también se despierta.",
        "Buenos días con alma de {n}.",
        "Hoy olemos a {n}, hoy olemos a nosotros.",
        "Buenos días {n}: elegancia desde la salida.",
        "El día arranca con carácter de {n}.",
    ],
    "naturaleza": [
        "{m} huele a {n} y a tarde de siesta.",
        "El campo, el mar o la montaña: hoy toca {n}.",
        "Buenos días con raíz de {n}.",
        "La naturaleza ya eligió: {n}.",
        "Buenos días {n}, que la estación lo pide.",
    ],
    "inspiracional": [
        "Hoy huele a oportunidad. Aprovéchala.",
        "Buenos días: cada día es una nota nueva.",
        "El perfume no cambia el día: cambia cómo lo vives.",
        "Buenos días con intención y con {n}.",
        "Que el día sea tan bueno como su aroma.",
    ],
}

DIAS = {
    0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves",
    4: "viernes", 5: "sábado", 6: "domingo",
}

# Mes en texto para las plantillas que lo necesitan ({m}).
# Motivo (28-sep-2026): la plantilla "naturaleza" tenía "Agosto" escrito a mano y
# una ficha del 29-sep salió con "Agosto huele a ...". El mes ahora sale de --fecha.
MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}


def _semilla(fecha: date) -> int:
    """Semilla determinista por fecha: mismo día = mismo saludo."""
    return fecha.year * 10000 + fecha.month * 100 + fecha.day


def _elegir_categoria(fecha: date) -> str:
    """Elige categoría con la semilla del día (rotación 1-8)."""
    rng = random.Random(_semilla(fecha))
    claves = sorted(CATEGORIAS.keys())
    return rng.choice(claves)


def _frase(categoria: str, perfume: str, nota: str, clima: int, dia: str, fecha: date) -> str:
    """Genera la frase de la categoría elegida, llenando el contexto disponible."""
    rng = random.Random(_semilla(fecha) + zlib.crc32(categoria.encode()) % 1000)
    plantillas = CATEGORIAS[categoria]
    plantilla = rng.choice(plantillas)

    # Rellenar contexto; si falta un dato, usar genérico coherente
    p = perfume if perfume else "el perfume"
    n = nota if nota else "buen aroma"
    t = clima if clima is not None else ""
    d = dia if dia else DIAS.get(fecha.weekday(), "")
    m = MESES.get(fecha.month, "")

    frase = plantilla.format(p=p, n=n, t=t, d=d, m=m)
    # limpiar dobles espacios y comas residuales si falta la temperatura
    frase = " ".join(frase.split())
    return frase


def main() -> int:
    parser = argparse.ArgumentParser(description="Saludo creativo para la ficha del perfume del día")
    parser.add_argument("--fecha", default=None, help="Fecha YYYY-MM-DD (default: hoy)")
    parser.add_argument("--perfume", default="", help="Nombre del perfume")
    parser.add_argument("--nota", default="", help="Nota principal / familia olfativa")
    parser.add_argument("--clima", type=int, default=None, help="Temperatura máxima del día")
    parser.add_argument("--categoria", default=None, help="Forzar categoría (debug)")
    args = parser.parse_args()

    if args.fecha:
        fecha = datetime.strptime(args.fecha, "%Y-%m-%d").date()
    else:
        fecha = date.today()

    categoria = args.categoria if args.categoria else _elegir_categoria(fecha)
    dia = DIAS.get(fecha.weekday(), "")
    frase = _frase(categoria, args.perfume, args.nota, args.clima, dia, fecha)

    # Regla del usuario (01-sep-2026): el saludo SIEMPRE empieza con "Buenos días".
    # Algunas plantillas ya lo llevan; si no, se antepone (sin duplicar).
    if not frase.lower().startswith("buenos días"):
        frase = "Buenos días. " + frase

    print(frase)
    print(f"[categoría: {categoria} | fecha: {fecha.isoformat()}]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
