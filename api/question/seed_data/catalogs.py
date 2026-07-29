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
# Esquema de cada field: name (clave interna), label (texto visible),
# type ("integer" | "boolean").
GENERAL_GROUPS = [
    {
        "name": "estructuras",
        "public_name": "Estructuras",
        "is_population": False,
        "fields": [
            {
                "name": "academic_instances",
                "label": "Instancias académicas reconocidas en el marco "
                         "normativo u organigrama de la IES",
                "type": "integer",
            },
            {
                "name": "admin_instances",
                "label": "Instancias administrativas reconocidas en el "
                         "marco normativo u organigrama de la IES",
                "type": "integer",
            },
        ],
    },
    {
        # Checklist de poblaciones: los ítems salen del catálogo Sector
        # (POB-ESTÁNDAR), no de fields; por eso va vacío.
        "name": "poblaciones",
        "public_name": "Poblaciones",
        "is_population": True,
        "fields": [],
    },
    {
        # Checklist de autoridades: los ítems salen de los Sector con
        # is_authority=True; captura en PopulationQuantity (ver 1.7).
        "name": "autoridades",
        "public_name": "Autoridades",
        "is_population": True,
        "fields": [],
    },
    {
        # Nombres alineados con PlanResponse (media/superior/postgraduate).
        "name": "planes_estudio",
        "public_name": "Planes de estudio",
        "is_population": False,
        "fields": [
            {
                "name": "media_plans",
                "label": "Planes de estudio vigentes de nivel medio "
                         "superior",
                "type": "integer",
            },
            {
                "name": "superior_plans",
                "label": "Planes de estudio vigentes de nivel superior "
                         "(licenciatura)",
                "type": "integer",
            },
            {
                "name": "postgraduate_plans",
                "label": "Planes de estudio vigentes de nivel posgrado "
                         "(especialidad, maestría y doctorado)",
                "type": "integer",
            },
        ],
    },
    {
        "name": "forma_gobierno",
        "public_name": "Forma de gobierno",
        "is_population": False,
        "fields": [
            {
                "name": "decentralized",
                "label": "Cuenta con una forma de gobierno descentralizada "
                         "que da autonomía a las autoridades de cada "
                         "instancia académica y/o administrativa",
                "type": "boolean",
            },
            {
                "name": "centralized",
                "label": "Cuenta con una forma de gobierno centralizada "
                         "que dota de facultades a su titular para emitir "
                         "disposiciones vinculantes a todas las áreas "
                         "académicas y administrativas",
                "type": "boolean",
            },
        ],
    },
]
