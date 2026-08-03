"""Datos del cuestionario 2026 (levantamiento).

Transcripción de docs/reference/cuestionario-2026-reducido.md a estructuras
Python consumidas por el comando load_questionnaire. No editar a mano
sin actualizar el documento fuente.
"""
from .axis_1 import AXIS as AXIS_1
from .axis_2 import AXIS as AXIS_2
from .axis_3 import AXIS as AXIS_3
from .axis_4 import AXIS as AXIS_4

ALL_AXES = [AXIS_1, AXIS_2, AXIS_3, AXIS_4]
