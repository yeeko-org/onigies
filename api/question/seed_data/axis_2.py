"""Datos del cuestionario 2026 — Eje 2.

Transcrito de docs/questions/all_questions_reduced.md. No editar a mano
sin actualizar el documento fuente.
"""

AXIS = {
    "order": 2,
    "name": "Inclusión y no discriminación",
    "description": None,
    "components": [
        {
            "name": (
                "Normas y políticas institucionales y académicas"
            ),
            "observables": [
                {
                    "number": "2.1",
                    "name": "Políticas institucionales para la inclusión",
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con políticas institucionales "
                        "dirigidas a la inclusión de grupos "
                        "históricamente discriminados?"
                    ),
                    "a_main_question": (
                        "Mencione todas las características o elementos "
                        "que están presentes en tales políticas de "
                        "inclusión y no discriminación:"
                    ),
                    "a_options": [
                        (
                            "Considera mecanismos de inclusión y no "
                            "discriminación específicos para las mujeres "
                            "en la IES."
                        ),
                        (
                            "Considera políticas de inclusión y no "
                            "discriminación hacia las diversidades "
                            "sexogenéricas (comunidad LGBTIQ+) en la IES."
                        ),
                        (
                            "Considera políticas de inclusión y no "
                            "discriminación hacia las personas "
                            "pertenecientes a grupos afrodescendientes, "
                            "originarios y/o indígenas."
                        ),
                        (
                            "Considera políticas de inclusión y no "
                            "discriminación hacia las personas con "
                            "discapacidades."
                        ),
                        (
                            "Las normas y/o políticas son explícitas en "
                            "su objetivo y alcance para la inclusión de "
                            "grupos históricamente discriminados por "
                            "razones de género y otros motivos."
                        ),
                        (
                            "Se trata de políticas internas de la IES "
                            "que tienen carácter jurídicamente "
                            "vinculante y de observancia obligatoria."
                        ),
                        (
                            "Incluyen políticas integrales que toman en "
                            "consideración la aplicación de medidas "
                            "afirmativas, medidas de inclusión y/o "
                            "medidas de nivelación."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿En qué sectores se implementan dichas "
                            "políticas?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    # Pendiente con cliente: texto solo menciona
                    # "académicas" (ver pendientes_revision_cuestionario.md).
                    "b_includes": (True, False),
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas implementan "
                        "dichas políticas?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "2.2",
                    "name": (
                        "Políticas institucionales y académicas de "
                        "inclusión y no discriminación"
                    ),
                    "description": (
                        "Políticas institucionales de no discriminación "
                        "a la población LGBTIQ+"
                    ),
                    "init_question": (
                        "¿La IES cuenta con políticas institucionales "
                        "dirigidas a la no discriminación de las "
                        "diversidades sexuales y de género (LGBTIQ+)?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características "
                        "están presentes en políticas institucionales y "
                        "académicas de inclusión y no discriminación? "
                        "(Mencione todas las características o "
                        "elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        "Se tratan de normas y políticas oficiales y "
                        "vigentes.",
                        (
                            "Establecen en su literalidad la no "
                            "discriminación en la IES por motivos de "
                            "orientación sexual, identidad de género, "
                            "expresión de género, características "
                            "sexuales y cualquier otro motivo vinculado "
                            "con la diversidad y disidencia sexual y de "
                            "género."
                        ),
                        (
                            "Incluyen actividades institucionales de "
                            "alto impacto para la visibilidad y "
                            "conmemoración de las reivindicaciones de "
                            "las personas LGBTIQ+."
                        ),
                        (
                            "Incluyen materiales de sensibilización "
                            "sobre los derechos de las personas LGBTIQ+ "
                            "ampliamente difundidos en la comunidad de "
                            "la IES."
                        ),
                        (
                            "Incluyen formación y capacitación sobre "
                            "derechos humanos de las personas LGBTIQ+."
                        ),
                        (
                            "Considera la habilitación de sanitarios y "
                            "otros espacios sin distinción de género "
                            "para prevenir la discriminación y la "
                            "violencia por razones de género."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿En qué sectores se implementan dichas "
                            "políticas?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    # Pendiente con cliente: texto solo menciona
                    # "académicas" (ver pendientes_revision_cuestionario.md).
                    "b_includes": (True, False),
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas implementan "
                        "dichas políticas?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "2.3",
                    "name": (
                        "Mecanismos institucionales de reconocimiento "
                        "de la diversidad sexo-genérica"
                    ),
                    "description": (
                        "Mecanismos institucionales para el "
                        "reconocimiento legal y social de las "
                        "identidades de género"
                    ),
                    "init_question": (
                        "¿La IES cuenta con mecanismos institucionales "
                        "formales para el reconocimiento de las "
                        "identidades de género de las personas que "
                        "integran su comunidad conforme a su "
                        "autodeterminación, particularmente personas "
                        "integrantes a la comunidad trans* y no "
                        "binarie?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características "
                        "están presentes en los mecanismos "
                        "institucionales? (Mencione todas las "
                        "características o elementos que resulten "
                        "aplicables)"
                    ),
                    "a_options": [
                        (
                            "El derecho a la identidad de género está "
                            "establecido en la normatividad y políticas "
                            "institucionales para la igualdad y no "
                            "discriminación."
                        ),
                        (
                            "Se cuenta con un procedimiento "
                            "institucional para actualizar el nombre "
                            "legal y el marcador de género de las "
                            "personas cuando han realizado previamente "
                            "su actualización de documentos legales."
                        ),
                        (
                            "Se cuenta con un mecanismo formal para la "
                            "solicitud de reconocimiento social de la "
                            "identidad de género al interior de la "
                            "institución, que favorece que las personas "
                            "sean nombradas conforme a sus nombres "
                            "elegidos y pronombres, independientemente "
                            "de que cuenten con sus datos legales "
                            "actualizados."
                        ),
                        (
                            "A partir de disposiciones institucionales, "
                            "las personas trans* pueden participar en "
                            "las diversas actividades académicas, "
                            "deportivas y artísticas conforme a la "
                            "autodeterminación de su identidad de "
                            "género."
                        ),
                        (
                            "Se implementan actividades de "
                            "sensibilización a la comunidad para "
                            "respetar las identidades de género trans* "
                            "y no binaries."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué sectores están dirigidas las "
                            "políticas para el reconocimiento de la "
                            "identidad de género?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿En qué instancias se implementan las "
                        "políticas de reconocimiento de la identidad de "
                        "género?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "2.4",
                    "name": (
                        "Lenguaje incluyente, no discriminatorio y no "
                        "sexista"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con criterios institucionales "
                        "para el uso del lenguaje incluyente, no "
                        "discriminatorio y no sexista en la "
                        "documentación oficial?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características "
                        "están presentes en los criterios "
                        "institucionales para el uso del lenguaje "
                        "incluyente, no discriminatorio y no sexista? "
                        "(Mencione todas las características o "
                        "elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se cuenta con un instrumento que establece "
                            "directrices oficiales para los usos del "
                            "lenguaje en toda la institución."
                        ),
                        (
                            "Formalmente, hay disposiciones para que "
                            "todas las instancias de la IES (académicas "
                            "y administrativas) den cumplimiento al "
                            "lenguaje incluyente en todas las formas e "
                            "instrumentos de comunicación."
                        ),
                        (
                            "Todos los títulos, diplomas y certificados "
                            "se expiden en femenino para mujeres."
                        ),
                        (
                            "Los documentos normativos de la "
                            "institución usan lenguaje incluyente al "
                            "referirse a cargos y nombramientos."
                        ),
                        (
                            "Las credenciales que expide la IES a su "
                            "personal usa marcas gramaticales femeninas "
                            "para mujeres."
                        ),
                        (
                            "Se cuenta con un instrumento institucional "
                            "para prevenir discursos y comunicaciones "
                            "discriminatorias hacia las mujeres, las "
                            "disidencias sexogenéricas, pueblos "
                            "originarios, personas con discapacidades y "
                            "cualquier grupo históricamente "
                            "discriminado."
                        ),
                        (
                            "La IES realiza procesos de sensibilización "
                            "y capacitación sobre usos del lenguaje "
                            "incluyente y no discriminatorio."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿En cuáles de los documentos normativos "
                            "que rigen a los siguientes sectores se "
                            "aplica la política de lenguaje incluyente, "
                            "no discriminatorio y no sexista? (Por "
                            "ejemplo, reglamento de inscripciones, o "
                            "reglamento de posgrado)"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas y "
                        "administrativas implementan la política de "
                        "uso del lenguaje incluyente, no discriminatorio "
                        "y no sexista? (al menos una acción "
                        "sustantiva)"
                    ),
                    "special_raw": None,
                },
            ],
        },
        {
            "name": (
                "Procesos y recursos institucionales y académicos"
            ),
            "observables": [
                {
                    "number": "2.5",
                    "name": (
                        "Programas y acciones institucionales de "
                        "prevención primaria de la discriminación y la "
                        "violencia"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con programas y acciones "
                        "institucionales de prevención primaria de las "
                        "discriminaciones y violencias por razones de "
                        "género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características "
                        "están presentes en los programas y acciones "
                        "institucionales de prevención primaria? "
                        "(Mencione todas las características o "
                        "elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se establece de manera institucional la "
                            "responsabilidad de la o las autoridades "
                            "universitarias de prevenir la violencia "
                            "por razones de género."
                        ),
                        (
                            "La IES ha emitido de manera formal una "
                            "declaratoria contra las violencias por "
                            "razones de género."
                        ),
                        (
                            "Incluye campañas y actividades de "
                            "sensibilización sobre las violencias por "
                            "razones de género."
                        ),
                        (
                            "Incluye la formación al alto funcionariado "
                            "en materia de prevención de las violencias "
                            "por razones de género."
                        ),
                        "Incluye senderos seguros para mujeres "
                        "integrantes de las IES.",
                        (
                            "Incluye luminarias y otros servicios que "
                            "amplían la seguridad espacial con "
                            "perspectiva de género."
                        ),
                        (
                            "Considera políticas preventivas de la "
                            "violencia digital contra las mujeres y por "
                            "razones de género."
                        ),
                        (
                            "Incluye información sobre las rutas de "
                            "atención de las violencias por razones de "
                            "género."
                        ),
                        "Otra (mencione cuál o cuáles).",
                    ],
                    "reach": {
                        "text": (
                            "¿A qué sectores están dirigidas dichos "
                            "programas y acciones de prevención?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿En qué instancias se aplican dichos programas "
                        "y acciones de prevención (al menos una acción "
                        "sustantiva)?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "2.6",
                    "name": (
                        "Programas y acciones institucionales de "
                        "trabajo con hombres para la igualdad de género"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con programas y acciones "
                        "institucionales de trabajo con hombres desde "
                        "un enfoque de género, interseccionalidad y "
                        "derechos humanos, orientadas a prevenir las "
                        "violencias y construir igualdad de género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características "
                        "están presentes en los programas y acciones "
                        "institucionales de trabajo con hombres? "
                        "(Mencione todas las características o "
                        "elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Existe un programa formalizado de trabajo "
                            "con hombres en la IES para construir "
                            "igualdad y prevenir las violencias a cargo "
                            "de las instancias responsables en la "
                            "materia."
                        ),
                        (
                            "Cuenta con documentos de diseño "
                            "metodológico específicos y propios de la "
                            "IES en construcción de igualdad y "
                            "prevención de las violencias focalizados "
                            "en hombres."
                        ),
                        (
                            "Se construye desde un enfoque crítico de "
                            "las masculinidades que se orienta al "
                            "cambio subjetivo y colectivo de los "
                            "hombres, como agentes de cambio para la "
                            "igualdad y la eliminación de las "
                            "desigualdades patriarcales."
                        ),
                        (
                            "Incluye un enfoque interseccional en el "
                            "trabajo con hombres, desde un diseño que "
                            "permite reconocer distintas realidades, "
                            "como son: edad, identidad de género, "
                            "orientación sexual, etnicidad, tipo de "
                            "población de la IES, clase social, entre "
                            "otras."
                        ),
                        (
                            "Incluye una agenda amplia y permanente de "
                            "actividades para el abordaje de las "
                            "masculinidades."
                        ),
                        (
                            "Incluye enfoques vivenciales y de trabajo "
                            "autorreflexivo para los hombres."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué sectores se incluye en las acciones "
                            "institucionales de trabajo con hombres? "
                            "(al menos una acción sustantiva)"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Qué instancias implementan los programas y "
                        "acciones institucionales de trabajo con "
                        "hombres?"
                    ),
                    "special_raw": None,
                },
            ],
        },
    ],
}
