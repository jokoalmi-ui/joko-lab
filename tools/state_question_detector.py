#!/usr/bin/env python3
"""state_question_detector.py — Detector central de preguntas de estado (HEL fase 2).

Intervención acotada (opción A, 14-ago-2026): la detección de pregunta de
estado debe ser la MISMA para medición y para intervención, para que cada paso
sea medible con el mismo criterio.

Este módulo importa la lógica real del instrumento (registrar_hel_diario.py,
KEYWORDS_ESTADO + filtro RUIDO con golden set C2) y la expone de forma
reutilizable. NO duplica lógica: si cambia el filtro, cambia en ambos sitios.

Uso:
    from state_question_detector import es_pregunta_estado, clasificar
"""
import importlib.util
import os

_INSTRUMENTO = os.path.join(os.path.dirname(__file__), 'registrar_hel_diario.py')

_spec = importlib.util.spec_from_file_location('registrar_hel_diario', _INSTRUMENTO)
_instr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_instr)

# Re-export de la lógica compartida (una sola fuente de verdad)
KEYWORDS_ESTADO = _instr.KEYWORDS_ESTADO
RUIDO = _instr.RUIDO
es_ruido = _instr.es_ruido
es_pregunta_estado = _instr.es_pregunta_estado

# Tipos de pregunta (RULE-PROC-005, versión acotada — sin el gate completo)
TIPOS = ('descriptiva', 'estado', 'historica', 'configuracion', 'operativa')


def clasificar(texto: str) -> str:
    """Clasifica el tipo de pregunta (versión acotada de RULE-PROC-005).

    - estado: pasa el detector (keywords de estado y no es ruido)
    - operativa: incluye verbos de acción sobre el sistema sin keyword de estado
    - historica: pide decisiones/registros pasados
    - configuracion: pide configuración real
    - descriptiva: resto
    """
    t = (texto or '').strip().lower()
    if es_pregunta_estado(t):
        return 'estado'
    if any(k in t for k in ('config', 'yaml', 'json de config', 'ajustes')):
        return 'configuracion'
    if any(k in t for k in ('cuando', 'antes', 'decision fue', 'historico', 'historia', 'pasado')):
        return 'historica'
    if any(k in t for k in ('ejecuta', 'lanza', 'levanta', 'arranca', 'instala', 'crea el', 'haz el')):
        return 'operativa'
    return 'descriptiva'


if __name__ == '__main__':
    import sys
    for arg in sys.argv[1:]:
        print(f'{clasificar(arg):14s} | {arg[:70]}')
