"""Datos del cuestionario 2026 — Eje 1.

Transcrito de docs/reference/cuestionario-2026-reducido.md. No editar a mano
sin actualizar el documento fuente.
"""

AXIS = {
    "order": 1,
    "name": "Igualdad de género",
    "description": (
        "Eje de políticas de igualdad sustantiva, inclusión y cuidados "
        "corresponsables"
    ),
    "components": [
        {
            "name": "Normas y políticas",
            "observables": [
                {
                    "number": "1.1",
                    "name": "Proceso de armonización normativa",
                    "description": None,
                    "init_question": (
                        "¿La IES ha llevado a cabo un proceso formal para "
                        "armonizar su legislación o normatividad interna en "
                        "materia de igualdad sustantiva e inclusión, conforme "
                        "a la Ley General de Educación Superior?"
                    ),
                    "a_main_question": (
                        "¿En qué términos se ha realizado este proceso? "
                        "(Marque todas las características o elementos que "
                        "resulten aplicables a este instrumento)"
                    ),
                    "a_options": [
                        (
                            "Análisis general de las normas vigentes y "
                            "aplicables a la IES y sus funciones, en materia "
                            "de igualdad sustantiva, inclusión, no "
                            "discriminación, así como otros derechos humanos."
                        ),
                        (
                            "Análisis específico la normatividad vigente en "
                            "materia de educación superior e igualdad "
                            "sustantiva, inclusión, no discriminación, así "
                            "como otros derechos humanos."
                        ),
                        (
                            "Identificación de actualizaciones, modificaciones "
                            "o desarrollo de disposiciones internas, derivado "
                            "del análisis normativo."
                        ),
                        (
                            "Planificación o programación de una ruta de "
                            "modificaciones normativas."
                        ),
                        (
                            "Aplicación de las actualizaciones, modificaciones "
                            "o desarrollo de disposiciones internas."
                        ),
                        (
                            "La armonización da cumplimiento al conjunto de "
                            "obligaciones legales aplicables a la IES en estas "
                            "materias."
                        ),
                        (
                            "Proceso participativo para la armonización "
                            "normativa interna."
                        ),
                    ],
                    "reach": None,
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas y administrativas se "
                        "consideró para este proceso de armonización?"
                    ),
                    # Solo instancias; cubierto por BQuestion.
                },
                {
                    "number": "1.2",
                    "name": (
                        "Norma principal de carácter general que integra la "
                        "igualdad de género"
                    ),
                    "description": None,
                    "init_question": (
                        'El máximo documento jurídico interno de carácter '
                        'general de la IES vigente en el año, ¿reconoce o '
                        'integra explícitamente a la "igualdad de género" en '
                        'su contenido?'
                    ),
                    "a_main_question": (
                        '¿En qué términos se reconoce o integra a la "igualdad '
                        'de género" en dicho documento? (Marque todas las '
                        'características o elementos que resulten aplicables a '
                        'este instrumento)'
                    ),
                    "a_options": [
                        (
                            'Reconoce o integra explícitamente el término de '
                            '"igualdad de género", o bien, uno o más términos '
                            'que remiten a una acepción más amplia o integral, '
                            'entre otros: la igualdad sustantiva, la igualdad '
                            'entre mujeres y hombres o la igualdad entre los '
                            'géneros.'
                        ),
                        (
                            'Atiende la observación del Comité para la '
                            'eliminación de todas las formas de discriminación '
                            'contra las mujeres (Comité CEDAW) al Estado '
                            'mexicano, referente a no tratar de forma '
                            'indistinta los términos igualdad y equidad de '
                            'género, y remitirse en todo momento a aquel de '
                            '"igualdad de género".'
                        ),
                        (
                            "Además del o de los términos relativos a la "
                            "igualdad de género, hace referencia y explica "
                            "otros conceptos que se articulan con la igualdad "
                            "de género en diferentes ámbitos y dimensiones de "
                            "la materia, como son: la no discriminación, "
                            "inclusión, los cuidados corresponsables y una "
                            "vida libre de violencia, entre otros."
                        ),
                        (
                            "Explicita o desagrega cuál es el alcance o ámbito "
                            "de aplicación de la igualdad de género dentro de "
                            "la IES."
                        ),
                        (
                            "Es de observancia obligatoria a las instancias y "
                            "población que forman parte de la IES."
                        ),
                        (
                            "Se encuentra vigente sin una temporalidad o fecha "
                            "de término de vigencia, y es resultado de un "
                            "proceso interno de formalización, de acuerdo con "
                            "las normas y procedimientos previstos por la "
                            "propia IES."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué poblaciones es aplicable el instrumento?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas y administrativas es "
                        "aplicable el instrumento?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "1.3",
                    "name": "Normas y disposiciones para la igualdad de género",
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con normatividad interna focalizada o "
                        "especializada específicamente en materia de igualdad "
                        "de género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características forman "
                        "parte de su normatividad interna en materia de "
                        "igualdad de género? (Marque todas las características "
                        "o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Su diseño incluye un enfoque complejo e integral "
                            "a partir de diversos ejes de trabajo que buscan "
                            "incidir en la transformación de las diferentes "
                            "desigualdades de género que existen en la IES, "
                            "como son: paridad, no discriminación, inclusión, "
                            "cuidados corresponsables y una vida libre de "
                            "violencias."
                        ),
                        (
                            "Se trata de normas internas de la IES que tienen "
                            "carácter jurídicamente vinculante y de "
                            "observancia obligatoria."
                        ),
                        (
                            "Son normas específicas en materia de igualdad de "
                            "género en su integralidad, y son distintas a "
                            "aquellas adoptadas en materia de violencia de "
                            "género. En caso de abordar la materia de "
                            "violencia de género, se focalizan en la "
                            "prevención primaria y no reducen el alcance de la "
                            "igualdad de género al abordaje de las violencias "
                            "de género."
                        ),
                        (
                            "Explícita o desagrega cuál es el alcance o ámbito "
                            "de aplicación de la igualdad de género dentro de "
                            "la IES."
                        ),
                        (
                            "Se encuentra vigente sin una temporalidad o fecha "
                            "de término de vigencia, y es resultado de un "
                            "proceso interno de formalización, de acuerdo con "
                            "las normas y procedimientos previstos por la "
                            "propia IES."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿Cuáles son las poblaciones de la IES a las que "
                            "les son aplicables las disposiciones normativas "
                            "específicas en materia de igualdad de género?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿A cuántas instancias académicas y administrativas "
                        "les son aplicables o cuentan con normas internas para "
                        "la igualdad de género?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "1.4",
                    "name": (
                        "Planeación institucional para la igualdad de género"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con una planeación institucional y "
                        "programática (plan, política o programa "
                        "institucional) de carácter general en materia de "
                        "igualdad de género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características forman "
                        "parte de la planeación institucional y programática "
                        "en materia de igualdad de género? (Mencione todas las "
                        "características o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se trata de un instrumento de planeación "
                            "debidamente formalizado mediante un procedimiento "
                            "de aprobación y/o publicación, por lo que es "
                            "público y se encuentra disponible por medios "
                            "institucionales."
                        ),
                        (
                            "Su contenido aborda a la igualdad de género de "
                            "manera integral, y no se reduce a la actuación "
                            "frente a la violencia de género."
                        ),
                        (
                            "La planeación define objetivos y metas claras en "
                            "materia de igualdad de género."
                        ),
                        (
                            "La planeación establece tiempos de ejecución "
                            "(anuales y multianuales)."
                        ),
                        (
                            "Se definen áreas responsables de la ejecución de "
                            "los planes en distintas áreas de la IES."
                        ),
                        (
                            "Se cuenta con mecanismos e indicadores de "
                            "medición de avances en su gestión, resultados, "
                            "impacto (este último, sólo si aplica)."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué poblaciones es aplicable la planeación "
                            "institucional y programática de carácter general "
                            "(al menos una acción explícita para cada sector)?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": True,
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas y administrativas "
                        "cuentan con una planeación interna para la igualdad "
                        "de género?"
                    ),
                    "special_raw": None,
                },
            ],
        },
        {
            "name": "Estructuras organizacionales",
            "observables": [
                {
                    "number": "1.5",
                    "name": "Estructuras para la igualdad de género",
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con una instancia ejecutiva interna "
                        "(unidad, coordinación, órgano, departamento) para "
                        "diseñar, implementar, dar seguimiento y evaluar "
                        "políticas y/o acciones institucionales en materia de "
                        "igualdad de género aplicables a toda la institución?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en dicha instancia? (Marque todas las "
                        "características o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Es una instancia formalmente creada, reconocida "
                            "jurídicamente dentro de la estructura orgánica y "
                            "marco normativo de la IES."
                        ),
                        (
                            "Está adscrita directamente a la autoridad central "
                            "o en el primer plano de la administración "
                            "central."
                        ),
                        (
                            "Cuenta con atribuciones claras en materia de "
                            "políticas de transversalización e "
                            "institucionalización de la igualdad de género (no "
                            "de atención a la violencia de género) para toda "
                            "la IES."
                        ),
                        (
                            "Cuenta con una estructura organizacional interna "
                            "con áreas de trabajo (no un sólo puesto, no un "
                            "enlace, no programa con temporalidad)."
                        ),
                        (
                            "Cuenta con presupuesto propio, asignado "
                            "formalmente, para realizar sus actividades "
                            "institucionales."
                        ),
                        (
                            "Cuenta con personal y recursos materiales propios "
                            "y suficientes para el área y sus funciones."
                        ),
                        (
                            "Cuenta con perfiles de contratación oficiales que "
                            "establecen el requerimiento de experiencia y "
                            "formación en materia de políticas de igualdad de "
                            "género."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿En qué sectores implementa dicha instancia las "
                            "políticas y acciones que desarrolla? (Al menos "
                            "una acción que impacte directamente para cada "
                            "sector)"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas y administrativas "
                        "cuentan con una estructura formal dedicada a "
                        "transversalizar las políticas para la igualdad de "
                        "género a nivel interno?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "1.6",
                    "name": "Principio de paridad de género en la normatividad",
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con disposiciones normativas que "
                        "establezcan el principio de paridad de género para la "
                        "conformación de sus autoridades y espacios de toma de "
                        "decisiones (administrativos y académicos)?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en las disposiciones en materia de paridad "
                        "de género de la IES? (Marque todas las "
                        "características o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se establece de manera explícita (no de facto) el "
                            "principio de paridad de género en espacios de "
                            "toma de decisiones (administrativos y académicos) "
                            "de la IES."
                        ),
                        (
                            "La disposición es jurídicamente vinculante y de "
                            "observancia obligatoria."
                        ),
                        (
                            "Se establece la paridad como base, y no como un "
                            "límite máximo a la comunidad menor representada "
                            "históricamente en los espacios de toma de "
                            "decisión (administrativos y académicos)."
                        ),
                        (
                            "En articulación con el principio de paridad de "
                            "género, establece acciones afirmativas que "
                            "aceleren el avance de las mujeres y comunidades "
                            "menos representadas históricamente en los "
                            "espacios de toma de decisión (administrativos y "
                            "académicos), sin confundirlo con el principio de "
                            "paridad de género."
                        ),
                        (
                            "Se aplica en las disposiciones de integración de "
                            "todos los cuerpos colegiados de máximo nivel y en "
                            "los cargos de elección donde históricamente no "
                            "exista la paridad."
                        ),
                    ],
                    "reach": {
                        # El MD no trae texto propio de alcance para 1.6;
                        # se reutiliza el texto estándar de 1.2 (mismo tipo
                        # de disposición normativa).
                        "text": (
                            "¿A qué poblaciones es aplicable el instrumento?"
                        ),
                        "populations": [
                            "Titular de la IES",
                            "Máximo cuerpo colegiado de toda la IES",
                        ],
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿En cuántas instancias académicas y administrativas "
                        "se aplica de manera explícita el principio de paridad "
                        "de género para la conformación de sus autoridades y/o "
                        "máximas figuras de toma de decisión?"
                    ),
                },
                {
                    "number": "1.7",
                    "name": (
                        "Integración paritaria y políticas para el aumento de "
                        "mujeres y grupos históricamente discriminados en "
                        "áreas segregadas"
                    ),
                    "description": "Integración paritaria",
                    "init_question": (
                        "¿La IES cuenta con una política para aumentar la "
                        "presencia, inclusión y participación de mujeres y "
                        "grupos históricamente discriminados en espacios "
                        "académicos, administrativos y escolares, donde su "
                        "presencia ha sido limitada?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en la o las políticas para aumento de "
                        "mujeres y grupos históricamente discriminados en la "
                        "IES? (Marque todas las características o elementos "
                        "que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se trata de políticas institucionalizadas (no de "
                            "facto) en la literalidad para el aumento de "
                            "mujeres y grupos históricamente discriminados en "
                            "espacios donde su presencia ha sido limitada."
                        ),
                        (
                            "La política incluye disposiciones o criterios que "
                            "son jurídicamente vinculantes o de observancia "
                            "obligatoria."
                        ),
                        (
                            "La política favorece el ingreso y permanencia de "
                            "mujeres en áreas donde su presencia es limitada "
                            "y/o históricamente subrrepresentada."
                        ),
                        (
                            "La política favorece el ingreso de personas "
                            "LGBTIQ+."
                        ),
                        (
                            "La política favorece el ingreso de personas "
                            "pertenecientes a pueblos originarios, indígenas "
                            "y/o afrodescendientes."
                        ),
                        (
                            "La política favorece el ingreso de personas con "
                            "discapacidad."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿En qué sectores de la IES se aplica de manera "
                            "explícita esta política? (Al menos una política "
                            "específicamente dirigida)"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿En cuántas instancias académicas y administrativas "
                        "se aplica de manera explícita la política referida?"
                    ),
                    # El bloque de composición sexo-genérica se pregunta en
                    # Generales (GeneralGroup autoridades + poblaciones);
                    # captura en PopulationQuantity (ver
                    # docs/records/2026-07-04-seed-del-cuestionario.md).
                },
            ],
        },
        {
            "name": "Procesos y recursos institucionales",
            "observables": [
                {
                    "number": "1.8",
                    "name": (
                        "Estadísticas y diagnósticos con perspectiva de género"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con mecanismos institucionales para "
                        "generar estadísticas y diagnósticos con perspectiva "
                        "de género? Esto es, mecanismos para la generación de "
                        "información y procesos diagnósticos de las "
                        "desigualdades, discriminaciones y violencias de "
                        "género y por cualquier otro motivo."
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en los mecanismos institucionales para "
                        "generar estadísticas y diagnósticos con perspectiva "
                        "de género? (Marque todas las características o "
                        "elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Existe una política institucional explícita que "
                            "solicita la desagregación por sexo-género de toda "
                            "la información estadística correspondiente a "
                            "todos los sectores de la IES."
                        ),
                        (
                            "Existe una instancia o conjunto de instancias que "
                            "son responsables de sistematizar y asegurar que "
                            "toda la información de la IES se desagregue por "
                            "sexo-género."
                        ),
                        (
                            "Se emite un anuario estadístico con información "
                            "desagregada por sexo-género para todos los "
                            "sectores de la IES."
                        ),
                        (
                            "Existe una política institucional explícita que "
                            "solicita la realización de diagnósticos sobre "
                            "desigualdades de género en todos los sectores de "
                            "la IES."
                        ),
                        (
                            "Se cuenta con un diagnóstico sobre brechas de "
                            "desigualdad de género en la IES con vigencia "
                            "máxima de 5 años."
                        ),
                        (
                            "Se cuenta con un diagnóstico sobre formas de "
                            "violencia y discriminación contra las mujeres por "
                            "razones de género, con vigencia máxima de 5 años."
                        ),
                        (
                            "Se cuenta con un diagnóstico sobre formas de "
                            "violencia y discriminación por razones de género "
                            "y/u otras razones, con vigencia máxima de 5 años."
                        ),
                        (
                            "Se cuenta con un diagnóstico sobre cuidados "
                            "corresponsables y/o división sexual del trabajo "
                            "con vigencia máxima de 5 años."
                        ),
                        (
                            "Se cuenta con un diagnóstico sobre diversidades "
                            "sexuales y de género con vigencia máxima de 5 "
                            "años."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué sectores consideran los diagnósticos "
                            "generales de igualdad de género de la IES?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas y administrativas "
                        "cuentan con un diagnóstico interno de igualdad de "
                        "género?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "1.9",
                    "name": (
                        "Programas y actividades de sensibilización, "
                        "concientización y capacitación en igualdad de género"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con programas específicos y "
                        "actividades para la sensibilización, concientización "
                        "y capacitación de sus comunidades en materia de "
                        "igualdad de género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en los programas específicos y actividades "
                        "para la sensibilización, concientización y "
                        "capacitación en igualdad de género? (Marque todas las "
                        "características o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se trata de un programa o programas "
                            "institucionales, formalizados en la planificación "
                            "de la IES."
                        ),
                        (
                            "Los programas incluyen actividades formativas "
                            "como cursos, seminarios y talleres con "
                            "perspectiva de género o abordan la agenda de la "
                            "igualdad de género (duración mínima: 2 sesiones, "
                            "4 horas)."
                        ),
                        (
                            "Los programas incluyen actividades de "
                            "sensibilización durante las fechas clave para la "
                            "igualdad, por ejemplo: el 11 de febrero (día de "
                            "las mujeres y las niñas en la ciencia), el 8 de "
                            "marzo (día internacional de la mujer), junio (mes "
                            "del orgullo LGBTIQ+), 25 de noviembre, etc."
                        ),
                        (
                            "Los programas incluyen una política de "
                            "comunicación de temas y materiales para la "
                            "igualdad de género en medios de amplia difusión "
                            "en las IES."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué sectores de la IES consideran o se dirigen "
                            "los programas de sensibilización, concientización "
                            "y/o capacitación en igualdad de género?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": True,
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas y administrativas "
                        "implementaron un programa de sensibilización, "
                        "concientización y/o capacitación en igualdad de "
                        "género?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "1.10",
                    "name": (
                        "Presupuestos institucionales para la igualdad de "
                        "género"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con un presupuesto anual sensible al "
                        "género y/o con presupuesto etiquetado específicamente "
                        "para la igualdad de género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en la asignación de presupuesto de la IES? "
                        "(Marque todas las características o elementos que "
                        "resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "La IES cuenta con algún instrumento interno de "
                            "planeación y asignación presupuestal (reglamento, "
                            "manual, entre otros) que establezca la "
                            "obligatoriedad y/o los criterios para realizar "
                            "presupuestos sensibles al género y/o presupuestos "
                            "etiquetados específicamente para la igualdad de "
                            "género."
                        ),
                        (
                            "El presupuesto institucional general de la IES ha "
                            "sido definido a partir de un diagnóstico, así "
                            "como analizado y construido desde la perspectiva "
                            "de género."
                        ),
                        (
                            "El presupuesto se incluye en algún instrumento de "
                            "planeación y asignación presupuestal."
                        ),
                        (
                            "El presupuesto institucional de la IES incluye "
                            "recursos etiquetados en materia de igualdad de "
                            "género (no reservados para la atención de las "
                            "violencias)."
                        ),
                        (
                            "Los recursos etiquetados (si existen) en materia "
                            "de igualdad de género, fueron asignados como "
                            "resultado de la identificación de una "
                            "problemática de desigualdad de género al interior "
                            "de la IES, y se orienta a su eventual solución."
                        ),
                        (
                            "Los recursos asignados son adicionales al sueldo "
                            "del personal que realiza las actividades para la "
                            "igualdad de género y los gastos corrientes de las "
                            "instancias dedicadas a esta materia (no incluir "
                            "los recursos en materia de violencia de género, "
                            "ya que se reportará más adelante)."
                        ),
                        (
                            "La IES asigna recursos para proyectos en materia "
                            "de igualdad de género aun cuando no existe un "
                            "proceso de etiquetado."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué sectores se consideró en la asignación de "
                            "presupuesto para la igualdad de género en la IES?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas y administrativas "
                        "ejercieron presupuesto específico para la igualdad de "
                        "género?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "1.11",
                    "name": "Evaluaciones en igualdad de género",
                    "description": (
                        "Evaluaciones de las políticas de igualdad de género"
                    ),
                    "init_question": (
                        "¿La IES cuenta o ha realizado alguna evaluación "
                        "institucional en materia de igualdad de género de sus "
                        "políticas, programas, procesos y/o recursos "
                        "institucionales?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en las evaluaciones institucionales en "
                        "materia de igualdad de género? (Marque todas las "
                        "características o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Evaluaciones diagnósticas de desigualdades "
                            "basadas en el género."
                        ),
                        (
                            "Evaluaciones sobre sus políticas y/o planeación "
                            "institucional para la igualdad de género."
                        ),
                        (
                            "Evaluaciones sobre sus programas y/o actividades "
                            "institucionales para la igualdad de género."
                        ),
                        (
                            "Evaluaciones a partir de indicadores de "
                            "resultados en materia de igualdad de género."
                        ),
                        (
                            "Evaluaciones a partir de indicadores de impacto "
                            "en materia de igualdad de género."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué sectores consideran las evaluaciones "
                            "institucionales en materia de igualdad de género "
                            "realizadas en la IES?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿A cuántas instancias académicas y administrativas "
                        "consideran las evaluaciones institucionales en "
                        "materia de igualdad de género realizadas en la IES?"
                    ),
                    "special_raw": None,
                },
            ],
        },
        {
            "name": "Procesos y recursos académicos",
            "observables": [
                {
                    "number": "1.12",
                    "name": (
                        "Planes y programas de estudio, y asignaturas para la "
                        "igualdad de género y con perspectiva de género "
                        "(docencia)"
                    ),
                    "description": (
                        "Planes y programas de estudio con perspectiva de "
                        "género"
                    ),
                    "init_question": (
                        "¿La IES cuenta con planes de estudio con perspectiva "
                        "de género y asignaturas para la igualdad de género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en los planes y programas de estudio de la "
                        "IES? (Mencione todas las características o elementos "
                        "que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Existe una normatividad que establece a la "
                            "perspectiva de género como un requisito para el "
                            "diseño y aprobación de planes de estudio."
                        ),
                        (
                            "La perspectiva de género se establece como un "
                            "enfoque transversal en los planes de estudio."
                        ),
                        (
                            "Existen asignaturas curriculares obligatorias "
                            "específicas en sus objetivos, título y contenidos "
                            "para el aprendizaje y la aplicación de la "
                            "perspectiva de género."
                        ),
                        (
                            "Existen asignaturas curriculares optativas "
                            "específicas en sus objetivos, título y contenidos "
                            "para el aprendizaje y la aplicación de la "
                            "perspectiva de género."
                        ),
                        (
                            "Existen asignaturas que parcialmente incorporan "
                            "en sus contenidos la perspectiva de género (al "
                            "menos en un 50%)."
                        ),
                        (
                            "Existen actividades de inducción o "
                            "extracurriculares obligatorias para el alumnado "
                            "que incorporan la perspectiva de género."
                        ),
                    ],
                    "reach": None,
                    "has_general_planning": False,
                    "reach_instances_question": None,
                    # Se mide por nivel de plan de estudios (PlanResponse ya
                    # trae los 3 niveles), con 4 sub-preguntas independientes.
                    "plan_questions": [
                        {
                            "order": 1,
                            "text": (
                                "¿En cuántos planes de estudio se establece "
                                "como un enfoque transversal la perspectiva "
                                "de género? — nivel medio superior / "
                                "licenciatura / posgrado"
                            ),
                        },
                        {
                            "order": 2,
                            "text": (
                                "¿En cuántos planes de estudio se incorpora "
                                "al menos una asignatura obligatoria "
                                "específica en nombre y contenidos para la "
                                "igualdad de género? — nivel medio superior "
                                "/ licenciatura / posgrado"
                            ),
                        },
                        {
                            "order": 3,
                            "text": (
                                "¿En cuántos planes de estudio se incorpora "
                                "al menos una asignatura optativa específica "
                                "en nombre y contenidos para la igualdad de "
                                "género? — nivel medio superior / "
                                "licenciatura / posgrado"
                            ),
                        },
                        {
                            "order": 4,
                            "text": (
                                "¿En cuántos planes de estudio se incorporan "
                                "asignaturas con al menos un 50% de "
                                "contenidos con perspectiva de género? — "
                                "nivel medio superior / licenciatura / "
                                "posgrado"
                            ),
                        },
                    ],
                },
                {
                    "number": "1.13",
                    "name": "Formación docente con perspectiva de género",
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con programas de formación para su "
                        "personal académico y administrativo en materia de "
                        "igualdad y no discriminación?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en la formación del personal académico y "
                        "administrativo de su IES? (Mencione todas las "
                        "características o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "La formación en igualdad y/o perspectiva de "
                            "género es obligatoria para el personal académico "
                            "y administrativo de la IES."
                        ),
                        (
                            "La IES cuenta con un programa para desarrollar "
                            "las competencias en perspectiva de género "
                            "dirigido al personal docente."
                        ),
                        (
                            "La IES oferta periódicamente capacitaciones "
                            "específicas en materia de igualdad y/o "
                            "perspectiva de género para su personal académico "
                            "y administrativo (fuera del programa mencionado "
                            "anteriormente)."
                        ),
                        (
                            "Las actividades de capacitación son programas "
                            "formativos de mediana o larga duración, son "
                            "diferentes a charlas o conferencias (o "
                            "actividades de sesiones únicas), y cuentan con "
                            "objetivos específicos en materia de igualdad de "
                            "género."
                        ),
                        (
                            "En el caso del personal académico, se cuenta con "
                            "capacitaciones específicas para incorporar la "
                            "perspectiva de género en su quehacer docente."
                        ),
                        (
                            "La IES realiza diagnóstico para conocer la "
                            "aplicación de la perspectiva de género del "
                            "personal académico, que retroalimente los "
                            "programas o acciones de capacitación que se "
                            "ofrecen en este sector."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿En qué sectores del personal académico y "
                            "administrativo de la IES se implementó la "
                            "formación durante el año ___?"
                        ),
                        "populations": [
                            (
                                "Personal académico de tiempo parcial / por "
                                "horas / por asignatura"
                            ),
                            "Personal académico de tiempo completo",
                            "Personal administrativo de base",
                            "Personal administrativo de confianza",
                            "Personal administrativo por honorarios",
                            "Autoridades y alto funcionariado",
                        ],
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿En cuántas instancias de la IES se implementó la "
                        "formación durante el año que estamos midiendo?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "1.14",
                    "name": "Investigación académica con perspectiva de género",
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con investigación académica con "
                        "perspectiva de género (centros, líneas de "
                        "investigación, grupos académicos para la igualdad de "
                        "género y no discriminación)?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en la investigación académica de su IES? "
                        "(Mencione todas las características o elementos que "
                        "resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Existen instancias académicas, reconocidas dentro "
                            "de la normatividad de la IES, dedicadas a la "
                            "investigación feminista y en estudios de género "
                            "como línea principal de estudios."
                        ),
                        (
                            "Estas instancias académicas están formalizadas y "
                            "son permanentes (sin temporalidad de vigencia)."
                        ),
                        (
                            "Existen líneas de investigación "
                            "institucionalizadas en estudios de género y "
                            "feministas dentro de instancias académicas "
                            "dedicadas a distintos ámbitos de conocimientos."
                        ),
                        (
                            "Existen grupos académicos institucionalizados en "
                            "la IES dedicados explícitamente a la "
                            "investigación desde los estudios de género y "
                            "feministas."
                        ),
                        (
                            "La institución cuenta con una política para "
                            "promover la investigación en estudios de género y "
                            "feministas de manera transversal a todas sus "
                            "instancias académicas."
                        ),
                        (
                            "La institución cuenta con una política para "
                            "incorporar la perspectiva de género en los "
                            "criterios para la aprobación de proyectos de "
                            "investigación (liderazgo de mujeres académicas, "
                            "grupos diversos, incorporación de la variable "
                            "sexo/género)."
                        ),
                        (
                            "La institución cuenta con acciones afirmativas "
                            "para impulsar a las mujeres en avanzar en sus "
                            "niveles como investigadoras."
                        ),
                    ],
                    "reach": None,
                    "has_general_planning": False,
                    # Texto solo menciona "académicas" (hallazgo de la
                    # 2ª ronda, no estaba en la lista original 1.15/2.1/2.2).
                    "b_includes": (True, False),
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas cuentan con una área o "
                        "grupo formal de investigación en estudios de género y "
                        "feministas?"
                    ),
                    "special_questions": [
                        {
                            "text": (
                                "¿Del total de proyectos de investigación "
                                "financiados por la IES cuántos son dirigidos "
                                "por mujeres? (proyectos dirigidos por "
                                "mujeres / total de proyectos)"
                            ),
                        },
                    ],
                },
                {
                    "number": "1.15",
                    "name": (
                        "Mecanismos y criterios de evaluación y promoción "
                        "académica (docencia e investigación) para la igualdad "
                        "y no discriminación"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con mecanismos y criterios en materia "
                        "de igualdad y no discriminación para las evaluaciones "
                        "y promociones de su personal académico?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en los mecanismos y criterios en materia de "
                        "igualdad y no discriminación en las evaluaciones y "
                        "promociones académicas? (Mencione todas las "
                        "características o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Los mecanismos y criterios existentes están "
                            "formalizados y son vinculantes para toda la "
                            "universidad."
                        ),
                        (
                            "Los mecanismos y criterios existentes incorporan "
                            "la perspectiva de género, particularmente el "
                            "enfoque de cuidados, como un componente que "
                            "comprende las cargas de trabajo y los ritmos de "
                            "las trayectorias de mujeres y otras personas "
                            "cuidadoras."
                        ),
                        (
                            "Los mecanismos y criterios existentes incorporan "
                            "disposiciones favorables para la evaluación con "
                            "perspectiva de género, como la composición "
                            "paritaria de los grupos evaluadores."
                        ),
                        (
                            "Los mecanismos y criterios existentes reconocen "
                            "como puntos favorables para la evaluación la "
                            "participación del personal académico en "
                            "actividades para la igualdad, no discriminación y "
                            "una vida libre de violencias en la IES."
                        ),
                    ],
                    "reach": None,
                    "has_general_planning": False,
                    "b_includes": (True, False),
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas cuentan con políticas "
                        "de evaluación y promoción con enfoque de igualdad y "
                        "no discriminación dirigidas al personal académico?"
                    ),
                },
                {
                    "number": "1.16",
                    "name": (
                        "Mecanismos y criterios de ingreso, permanencia y "
                        "evaluación estudiantil para la igualdad y no "
                        "discriminación"
                    ),
                    "description": (
                        "Mecanismos y criterios de permanencia estudiantil "
                        "para la igualdad"
                    ),
                    "init_question": (
                        "¿La IES cuenta con mecanismos y criterios para el "
                        "ingreso, permanencia, fortalecimiento de las "
                        "trayectorias, evaluación, egreso y titulación de "
                        "mujeres alumnas y alumnado perteneciente a grupos "
                        "históricamente discriminados?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en tales los mecanismos y criterios? "
                        "(Mencione todas las características o elementos que "
                        "resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Los mecanismos y criterios existentes están "
                            "formalizados y son vinculantes para toda la "
                            "universidad, especificar: Ingreso, Permanencia, "
                            "Fortalecimiento de las trayectorias, Evaluación, "
                            "Egreso, Titulación."
                        ),
                        (
                            "Los mecanismos y criterios existentes incorporan "
                            "la perspectiva de género, especificar: Ingreso, "
                            "Permanencia, Fortalecimiento de las trayectorias, "
                            "Evaluación, Egreso, Titulación."
                        ),
                        (
                            "Los mecanismos y criterios existentes focalizados "
                            "en la permanencia de alumnas, se han definido a "
                            "partir de la identificación de obstáculos en sus "
                            "trayectorias."
                        ),
                        (
                            "Existen mecanismos y criterios focalizados en la "
                            "permanencia de personas pertenecientes las "
                            "poblaciones de las diversidades y disidencias "
                            "sexuales y de género."
                        ),
                        (
                            "Existen mecanismos y criterios focalizados en la "
                            "permanencia de personas pertenecientes a pueblos "
                            "originarios, indígenas y/o afrodescendientes."
                        ),
                        (
                            "Existen mecanismos y criterios focalizados en la "
                            "permanencia de personas con discapacidades."
                        ),
                        (
                            "Los mecanismos y criterios existentes en todos "
                            "los casos son integrales y no se limitan a apoyos "
                            "económicos y/o materiales."
                        ),
                        (
                            "Existen mecanismos o criterios para la "
                            "conciliación de la vida escolar o laboral con la "
                            "familiar y de cuidados."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿En qué sectores del alumnado se implementan "
                            "dichos mecanismos?"
                        ),
                        "populations": [
                            "Alumnado de nivel medio superior",
                            "Alumnado de nivel licenciatura",
                            "Alumnado de nivel posgrado",
                        ],
                    },
                    "has_general_planning": False,
                    # Texto solo menciona "académicas" (mismo hallazgo que
                    # 1.14; ver el registro del seed del cuestionario).
                    "b_includes": (True, False),
                    "reach_instances_question": (
                        "¿Cuántas instancias académicas implementan dichos "
                        "mecanismos?"
                    ),
                },
                {
                    "number": "1.17",
                    "name": (
                        "Evaluaciones académicas en materia de igualdad de "
                        "género"
                    ),
                    "description": (
                        "Evaluaciones de las políticas académicas en materia "
                        "de igualdad de género"
                    ),
                    "init_question": (
                        "¿La IES cuenta o ha realizado alguna evaluación en "
                        "materia de igualdad de género de sus políticas, "
                        "programas, procesos y/o recursos académicos?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en las evaluaciones académicas en materia "
                        "de igualdad de género? (Marque todas las "
                        "características o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "La IES ha realizado evaluaciones sobre sus planes "
                            "y programas de estudio para la igualdad de "
                            "género."
                        ),
                        (
                            "La IES ha realizado evaluaciones docentes para la "
                            "igualdad de género."
                        ),
                        (
                            "La IES ha realizado evaluaciones de investigación "
                            "para la igualdad de género."
                        ),
                        (
                            "La IES ha realizado evaluaciones académicas a "
                            "partir de indicadores de resultados en materia de "
                            "igualdad de género."
                        ),
                        (
                            "La IES ha realizado evaluaciones académicas a "
                            "partir de indicadores de impacto en materia de "
                            "igualdad de género."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué sectores consideran las evaluaciones "
                            "académicas en materia de igualdad de género "
                            "realizadas en la IES?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿A cuántas instancias académicas y administrativas "
                        "consideran las evaluaciones académicas en materia de "
                        "igualdad de género realizadas en la IES?"
                    ),
                    "special_raw": None,
                },
            ],
        },
    ],
}
