"""Every fixed text of the Word export: nothing here has a home in the DB.

One named constant per string, so each can be edited or dropped without
touching the builder. Placeholders in braces are filled from the DB.
"""

DOCUMENT_TITLE = 'Cuestionario ONIGIES 2026'

TOC_TITLE = 'Contenido'
TOC_PLACEHOLDER = (
    'Para generar el índice, haga clic derecho aquí y elija '
    '«Actualizar campo».')

BASE_INFO_TITLE = 'Información de base'
IES_HEAD_LABEL = '{name}:'
IES_HEAD_OPTIONS = ('Mujer', 'Hombre', 'No binaria')
YES_NO_OPTIONS = ('Sí', 'No')
POPULATION_PRESENCE_ONLY = '{name} (solo se indica si está presente)'
GENERAL_OPTION = '{name} — {description}'
BASE_INFO_OBSERVABLE_NOTE = (
    'Las cifras de este apartado alimentan la calificación del observable '
    '{numbers}.')

CHECKLIST_TITLE = 'Lista de verificación inicial'
CHECKLIST_INSTRUCTION = (
    'Identifique si su IES tuvo vigentes en 2025 avances en los '
    'siguientes elementos observables:')
CHECKLIST_ROW = '{number} {name}'

QUESTIONNAIRE_TITLE = 'Cuestionario'
AXIS_HEADING = '{number}. Materia: {name}'
COMPONENT_HEADING = 'Componente: {name}'
OBSERVABLE_HEADING = 'Observable {number} {name}'

INIT_QUESTION_LABEL = 'Pregunta inicial:'
INIT_QUESTION = '{order}. {text}'
INIT_ANSWER_NO = 'No (pasar a la pregunta del siguiente observable)'
INIT_ANSWER_YES = 'Sí (responder las preguntas específicas)'
# Followed by the QuestionType.public_name of a_questions / b_questions.
VARIABLE_A_PREFIX = 'Variable A. '
VARIABLE_B_PREFIX = 'Variable B. '
OBSERVABLE_NOTE_LABEL = 'Nota: '

SECTOR_WITH_DESCRIPTION = '{name} ({description})'
GENERAL_PLANNING_OPTION = (
    'Planeación general sin focalizar un sector específico')
ACADEMIC_INSTANCES = 'instancias académicas'
ADMIN_INSTANCES = 'instancias administrativas'
POPULATION_OBSERVABLE_NOTE = (
    'Las cifras de composición por sexo-género de autoridades y '
    'poblaciones que evalúa este observable se capturan en los apartados '
    '{groups} de la sección {section}.')
GROUP_NAME = '«{title}»'
GROUP_JOIN = ' y '

