"""
Comparador determinista para el banco de verificación de Joko Lab.

Principio: la corrección la decide una función, nunca un modelo con criterio libre.
Esto es lo que evita que la métrica se pueda "convencer a sí misma" de que algo
está bien (Goodhart's Law aplicado a evaluación de LLMs).

Tres tipos de pregunta soportados:
  - numerico:            compara un número extraído de la respuesta contra un valor esperado ± tolerancia
  - exacto_normalizado:  el valor esperado debe aparecer literalmente (normalizado) en la respuesta
  - keywords_obligatorias: todas las keywords deben aparecer (normalizadas) en la respuesta

Si necesitas un tipo nuevo, añádelo al diccionario EVALUADORES al final del archivo.
No metas aquí nada que requiera "juicio" (p.ej. "¿es una buena respuesta?") — eso
vuelve a introducir el problema que este script existe para evitar.
"""
import re
import unicodedata


def normalizar(texto: str) -> str:
    """Minúsculas, espacios colapsados. CONSERVA tildes.

    Fix 06-ago-2026 (EXP KCR-001): eliminar tildes colisionaba 'sí'
    (afirmación, prohibida) con 'si' (conjunción condicional) — la respuesta
    correcta 'no debe usarse si existe un bloqueo' se marcaba FALLO. Al
    conservar tildes, cada keyword matchea solo su forma canónica. Las keywords
    del banco no llevan tilde salvo 'sí', así que el resto no se ve afectado."""
    texto = texto.lower().strip()
    texto = re.sub(r"\s+", " ", texto)
    return texto


def contiene_palabra(texto_normalizado: str, kw_normalizada: str) -> bool:
    """¿Contiene la keyword como PALABRA COMPLETA (no subcadena)?

    Fix 06-ago-2026 (EXP KCR-001): el 'in' simple daba falsos positivos por
    subcadena — p.ej. prohibido 'si' (= 'sí') aparecía dentro de 'usarse si
    existe' y marcaba FALLO una respuesta correcta. Ahora exige fronteras de
    palabra (espacios, puntuación, comillas, **, etc.)."""
    return re.search(rf"(?<![a-z0-9]){re.escape(kw_normalizada)}(?![a-z0-9])", texto_normalizado) is not None


def extraer_numeros(texto: str) -> list[float]:
    """Extrae números del texto, admitiendo coma o punto decimal."""
    crudos = re.findall(r"-?\d+[.,]?\d*", texto)
    numeros = []
    for n in crudos:
        n = n.replace(",", ".")
        try:
            numeros.append(float(n))
        except ValueError:
            continue
    return numeros


def evaluar_numerico(item: dict, respuesta: str) -> bool:
    numeros = extraer_numeros(respuesta)
    esperado = item["respuesta_esperada"]
    tolerancia = item.get("tolerancia", 0)
    return any(abs(n - esperado) <= tolerancia for n in numeros)


def evaluar_exacto_normalizado(item: dict, respuesta: str) -> bool:
    return contiene_palabra(normalizar(respuesta), normalizar(item["respuesta_esperada"]))


def evaluar_keywords_obligatorias(item: dict, respuesta: str) -> bool:
    texto = normalizar(respuesta)
    return all(contiene_palabra(texto, normalizar(kw)) for kw in item["respuesta_esperada"])


def evaluar_completitud_parcial(item: dict, respuesta: str) -> bool:
    texto = normalizar(respuesta)
    obligatorios_ok = all(contiene_palabra(texto, normalizar(kw)) for kw in item["respuesta_esperada"])
    prohibidos = item.get("prohibido", [])
    sin_prohibidos = not any(contiene_palabra(texto, normalizar(kw)) for kw in prohibidos)
    return obligatorios_ok and sin_prohibidos


EVALUADORES = {
    "numerico": evaluar_numerico,
    "exacto_normalizado": evaluar_exacto_normalizado,
    "keywords_obligatorias": evaluar_keywords_obligatorias,
    "completitud_parcial": evaluar_completitud_parcial,
}


def evaluar(item: dict, respuesta_hermes: str) -> bool:
    tipo = item["tipo"]
    if tipo not in EVALUADORES:
        raise ValueError(
            f"Tipo de evaluación desconocido: '{tipo}' (item {item.get('id')}). "
            f"Tipos válidos: {list(EVALUADORES.keys())}"
        )
    return EVALUADORES[tipo](item, respuesta_hermes)
