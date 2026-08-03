"""Datos del cuestionario 2026 — Eje 4.

Transcrito de docs/reference/cuestionario-2026-reducido.md. No editar a mano
sin actualizar el documento fuente.
"""

AXIS = {
    "order": 4,
    "name": "Una vida libre de discriminaciones y violencias",
    "description": (
        "Eje de políticas de no discriminación y una vida libre de "
        "violencias"
    ),
    "components": [
        {
            "name": "Normas y políticas institucionales",
            "observables": [
                {
                    "number": "4.1",
                    "name": "Proceso de armonización normativa",
                    "description": None,
                    "init_question": (
                        "¿La IES ha llevado a cabo un proceso formal para "
                        "armonizar su legislación o normatividad interna "
                        "en materia de violencias contra las mujeres y "
                        "otras formas de violencias basadas en el género, "
                        "conforme a la Ley General de Educación Superior y "
                        "otra normatividad vigente en la misma materia?"
                    ),
                    "a_main_question": (
                        "¿En qué términos se ha realizado este proceso? "
                        "(Marque todas las características o elementos "
                        "que resulten aplicables a este instrumento)"
                    ),
                    "a_options": [
                        (
                            "Análisis general de las normas vigentes y "
                            "aplicables a la IES y sus funciones, en "
                            "materia de una vida libre de violencia para "
                            "las mujeres."
                        ),
                        (
                            "Análisis general de las normas vigentes y "
                            "aplicables a la IES y sus funciones, en "
                            "materia de una vida libre de violencia para "
                            "otros grupos en situación de vulnerabilidad."
                        ),
                        (
                            "Análisis específico de la normatividad "
                            "vigente en materia de una vida libre de "
                            "violencia para las mujeres."
                        ),
                        (
                            "Análisis específico de la normatividad "
                            "vigente en materia de una vida libre de "
                            "violencia para otros grupos en situación de "
                            "vulnerabilidad."
                        ),
                        (
                            "Identificación de actualizaciones, "
                            "modificaciones o desarrollo de disposiciones "
                            "internas, derivado del análisis normativo."
                        ),
                        (
                            "Planificación o programación de una ruta de "
                            "modificaciones normativas."
                        ),
                        (
                            "Aplicación de las actualizaciones, "
                            "modificaciones o desarrollo de disposiciones "
                            "internas."
                        ),
                        (
                            "La armonización da cumplimiento al conjunto "
                            "de obligaciones legales aplicables a la IES "
                            "en estas materias."
                        ),
                        (
                            "Proceso participativo para la armonización "
                            "normativa interna."
                        ),
                    ],
                    "reach": None,
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿A qué instancias académicas y administrativas "
                        "se consideró para este proceso de armonización?"
                    ),
                    # Solo instancias; cubierto por BQuestion.
                },
                {
                    "number": "4.2",
                    "name": (
                        "Legislación para la atención de casos de "
                        "discriminación / violencia basada en el género"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con legislación en materia de "
                        "atención de la discriminación y violencia por "
                        "razones de género (distinta a los protocolos de "
                        "atención)?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en dicha legislación? (Mencione todas "
                        "las características o elementos que resulten "
                        "aplicables)"
                    ),
                    "a_options": [
                        (
                            "La IES incluye en su legislación a la "
                            "violencia por razones de género hacia las "
                            "mujeres como causa de responsabilidad "
                            "aplicable de todos los sectores de su "
                            "comunidad."
                        ),
                        (
                            "La IES incluye en su legislación a la "
                            "violencia por razones de género hacia otros "
                            "grupos en situación de vulnerabilidad como "
                            "causa de responsabilidad aplicable a todos "
                            "los sectores de su comunidad."
                        ),
                        (
                            "La IES cuenta con un marco normativo "
                            "específico que establece la responsabilidad "
                            "de actuación ante casos de violencia y "
                            "discriminación por razones de género para "
                            "las mujeres."
                        ),
                        (
                            "La IES cuenta con un marco normativo "
                            "específico que establece la responsabilidad "
                            "de actuación ante casos de violencia y "
                            "discriminación por razones de género para "
                            "otros grupos en situación de vulnerabilidad."
                        ),
                        (
                            "Las normas existentes tienen carácter "
                            "jurídicamente vinculante y de observancia "
                            "obligatoria."
                        ),
                        (
                            "Las normas se encuentran vigentes sin una "
                            "temporalidad o fecha de término de vigencia, "
                            "y son resultado de un proceso interno de "
                            "formalización, de acuerdo con las normas y "
                            "procedimientos previstos por la propia IES."
                        ),
                        (
                            "Su contenido explicita o desagrega cuál es "
                            "alcance o ámbito de aplicación de sus "
                            "disposiciones dentro de la IES."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué sectores es aplicable la legislación "
                            "para la actuación ante casos de violencia de "
                            "género?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Qué instancias aplican la legislación para la "
                        "actuación ante casos de violencia de género?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "4.3",
                    "name": (
                        "Normas específicas para la atención de casos de "
                        "discriminación / violencia basada en el género"
                    ),
                    "description": (
                        "Mecanismo específico para la atención de casos "
                        "de discriminación / violencia basada en el "
                        "género"
                    ),
                    "init_question": (
                        "¿La IES cuenta con un instrumento (tipo "
                        "protocolo) de actuación ante casos de "
                        "discriminación y violencia por razones de "
                        "género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en dicho instrumento? (Mencione todas "
                        "las características o elementos que resulten "
                        "aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se trata de un instrumento institucional "
                            "específico para actuar ante la "
                            "discriminación y violencia por razones de "
                            "género contra las mujeres."
                        ),
                        (
                            "Se trata de un instrumento institucional "
                            "específico para actuar ante la "
                            "discriminación y violencia por razones de "
                            "género contra otros grupos en situación de "
                            "vulnerabilidad."
                        ),
                        (
                            "Se encuentra formalizado y es de observancia "
                            "obligatoria para el personal encargado de la "
                            "atención y resolución de casos al interior "
                            "de la IES."
                        ),
                        (
                            "Define la coordinación entre las áreas "
                            "responsables de la atención de la "
                            "discriminación y la violencia a fin de "
                            "garantizar la debida diligencia."
                        ),
                        (
                            "Establece principios de atención y actuación "
                            "con enfoque de género hacia las mujeres, "
                            "interseccionalidad y derechos humanos."
                        ),
                        (
                            "Establece principios de atención y actuación "
                            "con enfoque de género hacia otros grupos en "
                            "situación de vulnerabilidad, "
                            "interseccionalidad y derechos humanos."
                        ),
                        (
                            "Es armónico con los estándares de mayor "
                            "protección a las personas en situación de "
                            "víctima."
                        ),
                        (
                            "Cuenta con mecanismos no sancionatorios para "
                            "modificar condiciones de desigualdad y "
                            "discriminación por razones de género en "
                            "contra de las mujeres en la IES."
                        ),
                        (
                            "Cuenta con mecanismos no sancionatorios para "
                            "modificar condiciones de desigualdad y "
                            "discriminación por razones de género en "
                            "contra de otros grupos en situación de "
                            "vulnerabilidad en la IES."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué sectores considera dicho instrumento?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿En qué instancias se implementa dicho "
                        "instrumento?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "4.4",
                    "name": (
                        "Personas de primer contacto especializadas en "
                        "materia de violencias de género"
                    ),
                    "description": None,
                    "init_question": (
                        "La institución cuenta con figuras de primer "
                        "contacto calificado, competente y especializado "
                        "para orientar a personas que consideren haber "
                        "sido víctimas de violencia por razones de "
                        "género?"
                    ),
                    "a_main_question": (
                        "¿En qué términos? (Marque todas las "
                        "características o elementos que resulten "
                        "aplicables a este instrumento)"
                    ),
                    "a_options": [
                        (
                            "Las personas que brindan atención de primer "
                            "contacto fueron capacitadas para llevar a "
                            "cabo su labor con enfoque de género hacia "
                            "las mujeres, derechos humanos y atención de "
                            "las violencias."
                        ),
                        (
                            "Las personas que brindan atención de primer "
                            "contacto fueron capacitadas para llevar a "
                            "cabo su labor con enfoque de género hacia "
                            "otros grupos en situación de vulnerabilidad, "
                            "derechos humanos y atención de las "
                            "violencias."
                        ),
                        (
                            "Las personas que brindan atención de primer "
                            "contacto fueron seleccionadas a partir de un "
                            "proceso de valoración de sus perfiles con "
                            "enfoque de género hacia las mujeres, "
                            "derechos humanos y atención de las "
                            "violencias."
                        ),
                        (
                            "Las personas que brindan atención de primer "
                            "contacto fueron seleccionadas a partir de un "
                            "proceso de valoración de sus perfiles con "
                            "enfoque de género hacia otros grupos en "
                            "situación de vulnerabilidad, derechos "
                            "humanos y atención de las violencias."
                        ),
                        (
                            "Existe un código de conducta y/o reglamento "
                            "que regula la práctica de las figuras de "
                            "primer contacto."
                        ),
                        (
                            "Las personas que brindan atención de primer "
                            "contacto reciben formación continua y "
                            "actualización en estándares vinculados con "
                            "la atención de violencia por razones de "
                            "género hacia las mujeres."
                        ),
                        (
                            "Las personas que brindan atención de primer "
                            "contacto reciben formación continua y "
                            "actualización en estándares vinculados con "
                            "la atención de violencia por razones de "
                            "género hacia otros grupos en situación de "
                            "vulnerabilidad."
                        ),
                        (
                            "Las personas que brindan atención de primer "
                            "contacto están certificadas en el estándar "
                            "de competencia EC0539. Atención presencial "
                            "de primer contacto a mujeres víctimas de "
                            "violencia de género."
                        ),
                        (
                            "El programa de primer contacto ha sido "
                            "evaluado en términos de sus resultados "
                            "alcanzados, considerando la satisfacción de "
                            "las personas usuarias."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué poblaciones se consideró este proceso "
                            "de armonización?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿A cuántas instancias académicas y "
                        "administrativas se consideró para este proceso "
                        "de armonización?"
                    ),
                    "special_raw": (
                        "reach_question: ⚠️ texto tal cual aparece en el "
                        "original — es un error de copiado (pertenece al "
                        "patrón de las preguntas de armonización "
                        "normativa 1.1/4.1, no corresponde al tema de "
                        "este observable). Se deja verbatim; ver "
                        "`dudas_a_resolver_con_cliente.md`, punto 1.\n\n"
                        "reach_instances_question: ⚠️ mismo error de "
                        "copiado que la pregunta anterior."
                    ),
                },
                {
                    "number": "4.5",
                    "name": (
                        "Políticas y medidas de prevención secundaria y "
                        "terciaria de las discriminaciones / violencias "
                        "basadas en el género enfocadas a las personas "
                        "responsables de su ejercicio"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con políticas y/o medidas de "
                        "protección inmediata ante situaciones de "
                        "violencia por razones de género para evitar su "
                        "reiteración o la ampliación de sus efectos?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en las políticas y medidas de "
                        "protección inmediata de las discriminaciones / "
                        "violencias basadas en el género? (Mencione "
                        "todas las características o elementos que "
                        "resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se establecen de manera oficial y existe una "
                            "instancia responsable de su emisión."
                        ),
                        (
                            "Una vez que se emiten, son vinculantes para "
                            "las áreas de la IES que tengan alguna "
                            "responsabilidad en su implementación."
                        ),
                        (
                            "Se emiten de manera provisional y sin "
                            "necesidad de haber concluido un proceso de "
                            "investigación y/o sanción."
                        ),
                        (
                            "Incluye enfoque de víctimas, a fin de que se "
                            "diseñen conforme a las necesidades y "
                            "particularidades de la persona que se "
                            "encuentra en dicha situación."
                        ),
                        (
                            "Prevén la posibilidad de que sean dirigidas "
                            "a la persona señalada como agresora a fin de "
                            "que desista de cualquier violencia o "
                            "represalia."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿Qué sectores están considerados en el "
                            "diseño de las medidas de protección "
                            "inmediata?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿En cuántas instancias se implementan medidas "
                        "de protección inmediata?"
                    ),
                    "special_raw": None,
                },
            ],
        },
        {
            "name": "Estructuras institucionales",
            "observables": [
                {
                    "number": "4.6",
                    "name": (
                        "Estructuras especializadas para la atención de "
                        "casos de discriminación / violencias basadas en "
                        "el género"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con estructuras especializadas "
                        "para atender casos de discriminación y violencia "
                        "basada en el género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en las estructuras especializadas "
                        "para atender casos de discriminación / violencia "
                        "basada en el género? (Mencione todas las "
                        "características o elementos que resulten "
                        "aplicables)"
                    ),
                    "a_options": [
                        (
                            "Las estructuras se encuentran "
                            "institucionalizadas en la normatividad de la "
                            "IES, con validez y vinculación jurídica."
                        ),
                        (
                            "Las estructuras cuentan con atribuciones "
                            "claras en materia de atención a la violencia "
                            "de género hacia las mujeres y resolución de "
                            "los casos."
                        ),
                        (
                            "Las estructuras cuentan con atribuciones "
                            "claras en materia de atención a la violencia "
                            "de género hacia otros grupos en situación de "
                            "vulnerabilidad y resolución de los casos."
                        ),
                        (
                            "Las instancias cuentan con una estructura "
                            "interna que define áreas y funciones "
                            "organizacionales para la adecuada atención "
                            "de los casos."
                        ),
                        (
                            "Las estructuras cuentan con recursos "
                            "humanos, materiales y financieros propios."
                        ),
                        (
                            "Establece claramente su alcance o ámbito de "
                            "competencia."
                        ),
                        (
                            "Las estructuras prevén las canalizaciones y "
                            "acompañamiento a instancias internas o "
                            "externas, en los casos que sean necesarios."
                        ),
                        (
                            "Las instancias cuentan con áreas "
                            "especializadas en violencias por razones de "
                            "género hacia las mujeres."
                        ),
                        (
                            "Las instancias cuentan con áreas "
                            "especializadas en violencias por razones de "
                            "género hacia otros grupos en situación de "
                            "vulnerabilidad."
                        ),
                        (
                            "Las instancias tienen capacidad "
                            "sancionatoria en los casos de violencias por "
                            "razones de género hacia las mujeres."
                        ),
                        (
                            "Las instancias tienen capacidad "
                            "sancionatoria en los casos de violencias por "
                            "razones de género hacia otros grupos en "
                            "situación de vulnerabilidad."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿A qué sectores son accesibles dichas "
                            "instancias especializadas?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Cuántas instancias cuentan con enlaces u "
                        "oficinas para la presentación de quejas por "
                        "violencia de género?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "4.7",
                    "name": (
                        "Puestos especializados para la atención de "
                        "casos de discriminación / violencias basadas en "
                        "el género"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES establece descripciones de puesto "
                        "especializados para atender casos de "
                        "discriminación / violencia basada en el género, "
                        "institucionalizados mediante documentos "
                        "administrativos que sirvan como referente para "
                        "el reclutamiento, selección y ocupación de los "
                        "puestos?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en las descripciones de puesto "
                        "profesionales especializados en materia de "
                        "discriminación / violencia basada en el género? "
                        "(Mencione todas las características o elementos "
                        "que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Las descripciones de puestos se establecen "
                            "de manera formal en la normatividad interna "
                            "de las estructuras responsables de la "
                            "atención de la violencia por razones de "
                            "género."
                        ),
                        (
                            "Se solicita que la persona titular de la "
                            "estructura para la atención de casos "
                            "acredite experiencia y formación suficiente "
                            "en materia de violencias por razones de "
                            "género hacia las mujeres."
                        ),
                        (
                            "Se solicita que la persona titular de la "
                            "estructura para la atención de casos "
                            "acredite experiencia y formación suficiente "
                            "en materia de violencias por razones de "
                            "género hacia otros grupos en situación de "
                            "vulnerabilidad."
                        ),
                        (
                            "Se ofrecen procesos de profesionalización y "
                            "capacitación por parte de las IES para el "
                            "personal en atención a las violencia de "
                            "violencias por razones de género hacia las "
                            "mujeres."
                        ),
                        (
                            "Se ofrecen procesos de profesionalización y "
                            "capacitación por parte de las IES para el "
                            "personal en atención a las violencia de "
                            "violencias por razones de género hacia otros "
                            "grupos en situación de vulnerabilidad."
                        ),
                        (
                            "Se solicita que las abogadas contratadas "
                            "acrediten formación y experiencia suficiente "
                            "en atención de violencias por razones de "
                            "género hacia las mujeres."
                        ),
                        (
                            "Se solicita que las abogadas contratadas "
                            "acrediten formación y experiencia suficiente "
                            "en atención de violencias por razones de "
                            "género hacia otros grupos en situación de "
                            "vulnerabilidad."
                        ),
                        (
                            "Se solicita que las psicólogas contratadas "
                            "acrediten formación y experiencia suficiente "
                            "en atención de violencias por razones de "
                            "género hacia las mujeres."
                        ),
                        (
                            "Se solicita que las psicólogas contratadas "
                            "acrediten formación y experiencia suficiente "
                            "en atención de violencias por razones de "
                            "género hacia otros grupos en situación de "
                            "vulnerabilidad."
                        ),
                    ],
                    "reach": None,
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿En cuántas instancias existe personal "
                        "especializado para la atención de las "
                        "violencias por razones de género?"
                    ),
                    # Solo instancias; cubierto por BQuestion.
                },
                {
                    "number": "4.8",
                    "name": (
                        "Servicios especializados para la atención de "
                        "casos de discriminación / violencia basadas en "
                        "el género"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES ofrece servicios especializados para "
                        "las personas denunciantes, adicionales a la "
                        "formalización de su procedimiento formal "
                        "(queja, denuncia, etc.)?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en los servicios especializados que "
                        "ofrece la IES en el marco de la atención de "
                        "casos de discriminación / violencia basada en "
                        "el género? (Mencione todas las características "
                        "o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se ofrecen servicios de orientación previos "
                            "a la presentación formal del procedimiento "
                            "(queja, denuncia, etc.) o de primer "
                            "contacto, con enfoque de género e "
                            "interseccionalidad."
                        ),
                        (
                            "Se ofrecen servicios de primeros auxilios "
                            "psicológicos y de contención psicoemocional."
                        ),
                        (
                            "Se ofrecen servicios completos de "
                            "acompañamiento psicoemocional."
                        ),
                        (
                            "Se ofrecen servicios de notificación "
                            "continua y oportuna del estatus del caso."
                        ),
                        (
                            "Se ofrece asesoría y/o acompañamiento legal "
                            "para presentación de denuncias en el ámbito "
                            "judicial."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿Para qué sectores están disponibles dichos "
                            "servicios?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿En cuántas instancias se cuenta con dichos "
                        "servicios especializados?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "4.9",
                    "name": (
                        "Responsabilidades de actuación para atender "
                        "casos de discriminación y violencia basada en "
                        "el género"
                    ),
                    "description": (
                        "Responsabilidades de actuación con instancias "
                        "externas para atender casos de discriminación y "
                        "violencia basada en el género"
                    ),
                    "init_question": (
                        "¿La IES establece responsabilidades de "
                        "actuación que involucran el vínculo con "
                        "instancias externas para atender casos de "
                        "discriminación y violencia basada en el género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en la vinculación interinstitucional "
                        "para la atención de las violencias? (Mencione "
                        "todas las características o elementos que "
                        "resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se establece la responsabilidad de "
                            "coordinación con otras instituciones con "
                            "las que la IES tenga vínculos académicos, "
                            "diplomáticos, de proyectos de colaboración, "
                            "etcétera, para la atención de casos que "
                            "requieran una actuación coordinada cuando "
                            "alguna de las partes en una situación de "
                            "violencia se encuentre o pertenezca a tales "
                            "instituciones."
                        ),
                        (
                            "Se establece la responsabilidad de notificar "
                            "a las autoridades judiciales sobre hechos "
                            "que constituyan delitos."
                        ),
                        (
                            "Se establece la responsabilidad de asistir "
                            "a personas en situación de víctima que "
                            "decidan presentar una denuncia judicial."
                        ),
                        (
                            "Se establece la responsabilidad de canalizar "
                            "a servicios de atención psicoemocional a "
                            "personas en situación de víctima, en caso de "
                            "no existir disponibilidad del servicio "
                            "dentro de la IES o no contar con las "
                            "atribuciones."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿Para qué sectores están disponibles dichos "
                            "servicios?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿En cuántas instancias se ofrecen dichos "
                        "servicios?"
                    ),
                    "special_raw": None,
                },
            ],
        },
        {
            "name": "Procesos y recursos institucionales",
            "observables": [
                {
                    "number": "4.10",
                    "name": (
                        "Criterios de resolución y medidas de no "
                        "repetición en el marco de la justicia "
                        "restaurativa"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES establece la responsabilidad de emitir "
                        "medidas de justicia restaurativa (no mediación) "
                        "y/o garantías de no repetición en todos los "
                        "casos de discriminación y violencia por razones "
                        "de género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en las medidas de justicia "
                        "restaurativa y/o garantías de no repetición? "
                        "(Mencione todas las características o elementos "
                        "que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se prevé en la normatividad de la IES que "
                            "todas las resoluciones ante casos de "
                            "violencia y discriminación por razones de "
                            "género hacia las mujeres incluyan medidas de "
                            "justicia restaurativa y no repetición."
                        ),
                        (
                            "Se prevé en la normatividad de la IES que "
                            "todas las resoluciones ante casos de "
                            "violencia y discriminación por razones de "
                            "género hacia otros grupos en situación de "
                            "vulnerabilidad incluyan medidas de justicia "
                            "restaurativa y no repetición."
                        ),
                        (
                            "Las actas de resolución incluyen, de manera "
                            "complementaria a las sanciones, medidas de "
                            "justicia restaurativa y no repetición de "
                            "carácter obligatorio."
                        ),
                        (
                            "Las medidas se diferencian de las sanciones "
                            "y se orientan principalmente a la "
                            "transformación de las condiciones que "
                            "posibilitaron las violencias y/o "
                            "discriminación."
                        ),
                        (
                            "Las medidas incluyen la reparación de "
                            "afectaciones académicas o administrativas "
                            "vividas por las personas en situación de "
                            "víctima dentro de la IES como efecto de la "
                            "discriminación o violencia (incluyendo "
                            "acciones de formación y concientización "
                            "para evitar vuelvan a ocurrir)."
                        ),
                        (
                            "Las medidas incluyen la atención "
                            "psicoemocional especializada de las personas "
                            "en situación de víctima como elemento de "
                            "reparación del daño."
                        ),
                        (
                            "Se establece la posibilidad de emitir "
                            "medidas dirigidas a las comunidades donde "
                            "ocurrieron las violencias como medida de "
                            "reparación del daño colectivo."
                        ),
                        (
                            "Se establece la posibilidad de emitir "
                            "medidas y recomendaciones para cambiar "
                            "infraestructura, normas, procedimientos, "
                            "etcétera, que resulten discriminatorias o "
                            "hayan posibilitado el ejercicio de las "
                            "violencias."
                        ),
                        (
                            "Se establece la responsabilidad de que las "
                            "personas responsables del ejercicio de las "
                            "violencias, particularmente hombres, acudan "
                            "a espacios de trabajo reflexivo "
                            "especializados."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿En qué sectores se implementan las medidas "
                            "de justicia restaurativa y/o garantías de "
                            "no repetición?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿A cuántas instancias son aplicables las "
                        "medidas de justicia restaurativa y/o garantías "
                        "de no repetición?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "4.11",
                    "name": (
                        "Mecanismos de seguimiento de casos y "
                        "cumplimiento de resoluciones"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con mecanismos de seguimiento de "
                        "casos de discriminación / violencia basada en "
                        "el género y de las resoluciones emitidas, en el "
                        "marco de su ámbito de competencia?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en los mecanismos de seguimiento de "
                        "casos y sus resoluciones emitidas en el ámbito "
                        "de su competencia? (Mencione todas las "
                        "características o elementos que resulten "
                        "aplicables)"
                    ),
                    "a_options": [
                        (
                            "Existe una instancia con facultades para dar "
                            "seguimiento integral a los procesos de "
                            "atención de las violencias, desde su "
                            "comienzo hasta su conclusión."
                        ),
                        (
                            "Se establece la responsabilidad de "
                            "notificación continua a las personas en "
                            "situación de víctima de todo el proceso."
                        ),
                        (
                            "Se cuenta con un mecanismo formal para el "
                            "seguimiento a las medidas de protección "
                            "emitidas a favor de la persona en situación "
                            "de víctima, de ser el caso."
                        ),
                        (
                            "Se cuenta con un mecanismo formal para el "
                            "seguimiento al cumplimiento de las "
                            "sanciones."
                        ),
                        (
                            "Se cuenta con un mecanismo formal para el "
                            "seguimiento de las medidas de justicia "
                            "restaurativa y no repetición."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿Qué sectores son considerados en el "
                            "seguimiento de casos y resoluciones "
                            "emitidas?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿En cuántas instancias se implementan medidas "
                        "de seguimiento de casos y resoluciones "
                        "emitidas?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "4.12",
                    "name": (
                        "Documentación, sistematización de información "
                        "y transparencia"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES cuenta con mecanismos de documentación, "
                        "sistematización de información y transparencia "
                        "sobre los casos y resoluciones emitidas por "
                        "discriminación / violencia basada en el género, "
                        "en su ámbito de competencia?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes en mecanismos de documentación, "
                        "sistematización de información y transparencia "
                        "sobre los casos y resoluciones emitidas por "
                        "discriminación / violencia basada en el género, "
                        "en su ámbito de competencia? (Mencione todas "
                        "las características o elementos que resulten "
                        "aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se establece la obligatoriedad de emitir "
                            "informes estadísticos sobre la presentación "
                            "de quejas por violencia y discriminación "
                            "por razones de género hacia las mujeres "
                            "atendidos."
                        ),
                        (
                            "Se establece la obligatoriedad de emitir "
                            "informes estadísticos sobre la presentación "
                            "de quejas por violencia y discriminación "
                            "por razones de género hacia otros grupos en "
                            "situación de vulnerabilidad atendidos."
                        ),
                        (
                            "Se establece la obligatoriedad de emitir "
                            "informes estadísticos sobre la resolución de "
                            "casos de violencia y discriminación por "
                            "razones de género hacia las mujeres "
                            "atendidas."
                        ),
                        (
                            "Se establece la obligatoriedad de emitir "
                            "informes estadísticos sobre la resolución de "
                            "casos de violencia y discriminación por "
                            "razones de género hacia otros grupos en "
                            "situación de vulnerabilidad atendidos."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿Qué sectores son considerados en la "
                            "emisión de dichos informes?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Cuántas instancias emiten o participan en la "
                        "presentación de dichos informes?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "4.13",
                    "name": (
                        "Evaluación de atención de procedimientos "
                        "formales (quejas o denuncias) de atención de "
                        "casos de violencias de género"
                    ),
                    "description": (
                        "Evaluación de la experiencia de las personas "
                        "usuarias de los mecanismos de atención de la "
                        "violencia de género"
                    ),
                    "init_question": (
                        "¿La IES ha llevado a cabo un proceso de "
                        "evaluación de las experiencias y satisfacción "
                        "de las personas usuarias de los procedimientos "
                        "formales (queja o denuncia) de atención de "
                        "casos de violencia por razones de género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes? (Mencione todas las características "
                        "o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Existen mecanismos para recabar la opinión "
                            "de las personas usuarias de los "
                            "procedimientos formales (queja o denuncia) "
                            "de atención de casos de violencia por "
                            "razones de género en contra de las mujeres."
                        ),
                        (
                            "Existen mecanismos para recabar la opinión "
                            "de las personas usuarias de los "
                            "procedimientos formales (queja o denuncia) "
                            "de atención de casos de violencia por "
                            "razones de género en contra de otros grupos "
                            "en situación de vulnerabilidad."
                        ),
                        (
                            "Se establece la obligatoriedad de emitir "
                            "informes estadísticos de uso interno sobre "
                            "la satisfacción de las personas usuarias "
                            "durante proceso de presentación de quejas "
                            "por violencia y discriminación por razones "
                            "de género en contra de las mujeres."
                        ),
                        (
                            "Se establece la obligatoriedad de emitir "
                            "informes estadísticos de uso interno sobre "
                            "la satisfacción de las personas usuarias "
                            "durante proceso de presentación de quejas "
                            "por violencia y discriminación por razones "
                            "de género en contra de otros grupos en "
                            "situación de vulnerabilidad."
                        ),
                        (
                            "Se establece la obligatoriedad de emitir "
                            "informes estadísticos públicos sobre la "
                            "satisfacción de las personas usuarias "
                            "durante el proceso de presentación de "
                            "quejas por violencia y discriminación por "
                            "razones de género en contra de las mujeres."
                        ),
                        (
                            "Se establece la obligatoriedad de emitir "
                            "informes estadísticos públicos sobre la "
                            "satisfacción de las personas usuarias "
                            "durante el proceso de presentación de "
                            "quejas por violencia y discriminación por "
                            "razones de género en contra de otros grupos "
                            "en situación de vulnerabilidad."
                        ),
                        (
                            "Existe evidencia de que la IES utiliza las "
                            "opiniones recabadas de las personas usuarias "
                            "para optimizar sus mecanismos de atención."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿Qué sectores son considerados en la "
                            "emisión de dichos informes?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Cuántas instancias emiten o participan en la "
                        "presentación de dichos informes?"
                    ),
                    "special_raw": None,
                },
                {
                    "number": "4.14",
                    "name": (
                        "Evaluación de atención de mecanismo de atención "
                        "de las violencias por razones de género"
                    ),
                    "description": None,
                    "init_question": (
                        "¿La IES ha llevado a cabo un proceso de "
                        "evaluación de su mecanismo de atención de las "
                        "violencias por razones de género?"
                    ),
                    "a_main_question": (
                        "¿Cuáles de las siguientes características están "
                        "presentes? (Mencione todas las características "
                        "o elementos que resulten aplicables)"
                    ),
                    "a_options": [
                        (
                            "Se trata de una evaluación formal que "
                            "cuenta con objetivos, metodología, "
                            "resultados y fue realizada por un equipo de "
                            "evaluación especializado."
                        ),
                        (
                            "Considera dentro de los ámbitos a evaluar la "
                            "satisfacción de las personas usuarias del "
                            "mecanismo."
                        ),
                        (
                            "Existe evidencia de que la IES utiliza las "
                            "opiniones recabadas de las personas usuarias "
                            "para optimizar sus mecanismos de atención."
                        ),
                        (
                            "Considera dentro de los ámbitos a evaluar la "
                            "eficiencia en la implementación de los "
                            "procedimientos (tiempo de espera para "
                            "obtener una primera cita, tiempo de espera "
                            "para resoluciones, carga de trabajo del "
                            "personal operativo)."
                        ),
                        (
                            "Considera dentro de los ámbitos a evaluar la "
                            "eficacia de los procedimientos (tasa de "
                            "casos resueltos, tasa de casos pendientes)."
                        ),
                        (
                            "Considera dentro de los ámbitos a evaluar el "
                            "desempeño del personal operativo."
                        ),
                        (
                            "Considera dentro de los ámbitos a evaluar la "
                            "suficiencia presupuestaria de la instancia "
                            "responsable del procedimiento de atención."
                        ),
                        (
                            "Considera dentro de los ámbitos a evaluar "
                            "las resoluciones emitidas por las "
                            "autoridades competentes."
                        ),
                        (
                            "Considera dentro de los ámbitos a evaluar la "
                            "armonización del mecanismo con los máximos "
                            "criterios y estándares de atención a "
                            "víctimas."
                        ),
                        (
                            "La evaluación ha sido realizada por alguna "
                            "instancia externa a la responsable del "
                            "mecanismo de atención."
                        ),
                    ],
                    "reach": {
                        "text": (
                            "¿Qué sectores son considerados en la "
                            "emisión de dichos informes?"
                        ),
                        "populations": "standard",
                    },
                    "has_general_planning": False,
                    "reach_instances_question": (
                        "¿Cuántas instancias emiten o participan en la "
                        "presentación de dichos informes?"
                    ),
                    "special_raw": None,
                },
            ],
        },
    ],
}
