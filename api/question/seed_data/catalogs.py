"""Catálogos del cuestionario: escala de opciones A y grupos generales.

QuestionType NO se define aquí: ya se siembra en question/initial_data.py
(comando migrate_initial_data). Los sectores viven en load_sectors.
"""

# Escala global de respuesta para las preguntas de institucionalización
# (AQuestion). En el cuestionario original cada opción tenía una columna
# "Sí" constante: la respuesta es marcar o no cada opción.
A_OPTIONS = [
    {"text": "Sí", "value": 1},
    {"text": "No", "value": 0},
]

# POB-ESTÁNDAR (12 poblaciones) = los 10 sectores is_main=True más estos
# dos, que van en others_sectors cuando el alcance es estándar.
STANDARD_EXTRA_SECTORS = ["Población externa", "Público en general"]

# Grupos de la sección "Información de base" del cuestionario.
# Cada grupo lleva sus textos de encabezado (title, subtitle, instruction)
# y su lista de `questions`, que se siembra en question.GeneralQuestion:
# name (clave estable de la pregunta; el valor aterriza en
# GeneralQuestionResponse), text (la pregunta), label (rótulo corto
# opcional; si va vacío el rótulo efectivo es `unit`), unit, q_type
# ("integer" | "boolean"), order y addl_config (parámetros de
# comportamiento, entre ellos `allow_no_apply`).
# Los grupos de checklist (poblaciones, autoridades) arman sus filas
# desde el catálogo Sector, no desde `questions`.
# El orden de esta lista ES el orden del instrumento: `_load_general_groups`
# lo escribe en GeneralGroup.order (mismo patrón que load_sectors).
GENERAL_GROUPS = [
    {
        # Primero por acuerdo con Rubén (reunión del 11 de agosto):
        # la forma de gobierno enmarca todo lo demás.
        "name": "forma_gobierno",
        "public_name": "Forma de gobierno",
        "title": "Forma de gobierno",
        "subtitle": "",
        "instruction": "",
        "is_population": False,
        "questions": [
            {
                # Una sola pregunta booleana y dos opciones excluyentes.
                # Van en addl_config partidas en nombre del tipo (que el
                # componente pinta en negritas) y descripción.
                "name": "is_centralized",
                "text": "Señale cuál de las siguientes descripciones "
                        "corresponde a la forma de gobierno de su "
                        "institución.",
                "q_type": "boolean",
                "order": 1,
                "addl_config": {
                    "options": [
                        {
                            "value": False,
                            "name": "Descentralizada",
                            "description":
                                "Da autonomía a las autoridades de cada "
                                "instancia académica y/o administrativa.",
                        },
                        {
                            "value": True,
                            "name": "Centralizada",
                            "description":
                                "Dota de facultades a su titular para "
                                "emitir disposiciones vinculantes a todas "
                                "las áreas académicas y administrativas.",
                        },
                    ],
                },
            },
        ],
    },
    {
        "name": "estructuras",
        "public_name": "Estructuras",
        "title": "Estructuras",
        "subtitle": "",
        "instruction": "",
        "is_population": False,
        "questions": [
            {
                "name": "academic_instances",
                "text": "Instancias académicas reconocidas en el marco "
                        "normativo u organigrama de la IES",
                "unit": "instancias",
                "order": 1,
            },
            {
                "name": "admin_instances",
                "text": "Instancias administrativas reconocidas en el "
                        "marco normativo u organigrama de la IES",
                "unit": "instancias",
                "order": 2,
            },
        ],
    },
    {
        # Checklist de poblaciones: los ítems salen del catálogo Sector
        # (POB-ESTÁNDAR). La única pregunta propia es la previa.
        "name": "poblaciones",
        "public_name": "Poblaciones",
        "title": "Poblaciones",
        "subtitle": "Señale las poblaciones que integran a la comunidad "
                    "de su institución, así como todas aquellas que están "
                    "presentes física o virtualmente y con las que "
                    "mantiene vínculos a través de sus actividades "
                    "institucionales.",
        "instruction": "Para cada población marcada, indique cuántas "
                       "personas la integran según su sexo y género. Si "
                       "no cuenta con el dato exacto, registre su mejor "
                       "estimación.",
        "is_population": True,
        "questions": [
            {
                "name": "measures_non_binary",
                "text": "En sus registros de sexo y género, ¿su "
                        "institución contempla la categoría no binaria?",
                "hint": "Si responde Sí, las tablas de esta sección "
                        "incluirán una columna para el conteo de "
                        "personas no binarias.",
                "q_type": "boolean",
                "order": 1,
            },
        ],
    },
    {
        # Checklist de autoridades: los ítems salen de los Sector con
        # is_authority=True; captura en PopulationQuantity (ver 1.7).
        "name": "autoridades",
        "public_name": "Autoridades",
        "title": "Autoridades",
        "subtitle": "",
        "instruction": "Indique cuántas personas integran, según su sexo "
                       "y género, cada uno de los siguientes órganos y "
                       "conjuntos de autoridades de su institución.",
        "is_population": True,
        "questions": [],
    },
    {
        # Nombres alineados con PlanResponse (media/superior/postgraduate).
        "name": "planes_estudio",
        "public_name": "Planes de estudio",
        "title": "Planes de estudio",
        "subtitle": "",
        "instruction": "",
        "is_population": False,
        # Las tres ofrecen «No aplica»: una IES puede no impartir un
        # nivel, y sin la casilla su cero no se distinguiría de «no
        # ofrecemos ese nivel».
        "questions": [
            {
                "name": "media_plans",
                "text": "Planes de estudio vigentes de nivel medio "
                        "superior",
                "unit": "planes",
                "order": 1,
                "addl_config": {"allow_no_apply": True},
            },
            {
                "name": "superior_plans",
                "text": "Planes de estudio vigentes de nivel superior "
                        "(licenciatura)",
                "unit": "planes",
                "order": 2,
                "addl_config": {"allow_no_apply": True},
            },
            {
                "name": "postgraduate_plans",
                "text": "Planes de estudio vigentes de nivel posgrado "
                        "(especialidad, maestría y doctorado)",
                "unit": "planes",
                "order": 3,
                "addl_config": {"allow_no_apply": True},
            },
        ],
    },
]
