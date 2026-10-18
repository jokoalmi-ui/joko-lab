#!/usr/bin/env python3
"""
contrastar_externo.py — Gate externo de veracidad (Fase 3, 16-ago-2026)

Cómo funciona REALMENTE (verificado):
  - La búsqueda web directa desde Python NO es fiable: DDG/Bing bloquean curl
    (anti-bot) y la API EXA del lab está desactivada (comentada en .env).
  - Por tanto, la contrastación externa la hace el AGENTE (Hermes) con su
    herramienta web_search (que sí funciona). Este script:
      1. Verifica un texto con verificador_alucinaciones.py
      2. Si marca [NO VERIFICADO] → dice "BUSCAR" + extrae las palabras clave
         para la búsqueda web
      3. El agente busca, obtiene fuentes, y llama a `--actualizar` para
         re-etiquetar con las fuentes encontradas
  - Así el gate externo es un flujo agente+script, no un script solo.

Uso (flujo agente):
  1. python3 contrastar_externo.py --texto "..." --tema "..." 
     → salida: [VERIFICADO] | [ALCANCE INTERNO] | BUSCAR:<keywords>
  2. Si BUSCAR → agente hace web_search(keywords) → extrae URLs
  3. python3 contrastar_externo.py --texto "..." --tema "..." --fuentes "url1 url2"
     → salida: [VERIFICADO] (con fuentes)
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verificador_alucinaciones import verificar


def extraer_keywords(texto: str, max_kw: int = 5) -> str:
    """Extrae palabras clave para la búsqueda web (nombres propios, números, entidades)."""
    # Palabras con mayúscula (entidades/nombres propios) + números con contexto
    entidades = re.findall(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}\b", texto)
    numeros = re.findall(r"\b[\d]+(?:[.,]\d+)?%?\b", texto)
    # Stopwords básicas
    STOP = {"El", "La", "Los", "Las", "Un", "Una", "Según", "Datos", "Informe"}
    kws = [w for w in entidades if w not in STOP and len(w) > 3]
    resultado = kws[:max_kw] + numeros[:3]
    return " ".join(resultado) if resultado else texto[:80]


def main():
    ap = argparse.ArgumentParser(description="Gate externo de veracidad (Fase 3)")
    ap.add_argument("--texto", required=True, help="texto a verificar")
    ap.add_argument("--tema", help="tema esperado")
    ap.add_argument("--fuentes", help="URLs de fuentes encontradas por el agente (separadas por espacio)")
    args = ap.parse_args()

    r = verificar(args.texto, tema=args.tema)

    # Si el agente aportó fuentes → re-etiquetar como VERIFICADO
    if args.fuentes:
        fuentes = args.fuentes.split()
        # Añadir las fuentes al texto y re-verificar
        texto_con_fuentes = args.texto + " [VERIFICADO] " + " ".join(fuentes)
        r2 = verificar(texto_con_fuentes, tema=args.tema)
        r = r2
        r["fuentes_aportadas"] = fuentes

    veredicto = r["veredicto"]
    etiqueta = r["etiqueta"]

    if veredicto == "BLOQUEADO_SIN_FUENTE":
        kws = extraer_keywords(args.texto)
        print(f"BUSCAR:{kws}")
        print(f"motivo: afirma hechos sin fuente — busca '{kws}' y repite con --fuentes 'url1 url2'")
        sys.exit(1)
    elif veredicto == "REVISAR":
        print(f"{etiqueta} (revisar contradicción/irrelevancia antes de emitir)")
        sys.exit(1)
    else:
        print(f"{etiqueta} ({veredicto})")
        sys.exit(0)


if __name__ == "__main__":
    main()
