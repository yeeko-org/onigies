---
type: reference
id: 2026-09-07-clasificacion-armonizacion-institucionalizacion
title: Clasificación a mano de las 280 opciones del bloque A en armonización o institucionalización
state: current
date: 2026-09-07
related: ["[[adr-0014]]", "[[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]]", "[[task-135]]"]
---

# Clasificación a mano de las 280 opciones del bloque A en armonización o institucionalización

**Estado: descartada como dato del sistema.** El 7 de septiembre de 2026 Ricardo decidió no almacenar la distinción ([[adr-0014]] §3): el bloque A se llama «Armonización e institucionalización» en todos lados y cada opción no lleva clase. Esta tabla se conserva para que, si algún día un cálculo o un desglose la necesita (por ejemplo en la reunión del viernes 11, [[task-135]]), no haya que rehacer el trabajo.

**Criterio pendiente.** Quedó sin decidir si «la norma que obliga a una práctica» cuenta como armonización o como institucionalización (ver la banda «ARM-mandato» abajo). Esa decisión mueve 30 opciones y voltea dos observables enteros (4.9 y 4.12).

## Criterio aplicado

Se clasificó por **el objeto que la opción predica**, no por el vocabulario:

- **ARM (armonización)**: el objeto es un instrumento normativo (norma, legislación, reglamento, lineamiento, protocolo, disposición, criterio vinculante, política formalizada) y lo que se mide es qué dice o cómo está ese instrumento.
- **INST (institucionalización)**: el objeto es una estructura, programa, presupuesto, personal, procedimiento operativo, servicio, infraestructura, diagnóstico, evaluación o actividad, y lo que se mide es que exista o se haga.
- **DUD (dudosa)**: la opción predica ambos objetos a la vez, o el objeto es indecidible.
- **N/A**: opción abierta de texto libre, no clasificable.

Dos etiquetas acuñadas en el análisis, que no existen en el material del cliente:

- **ARM-mandato** (marcado con †): subfamilia de ARM donde la norma prescribe una práctica operativa («Se establece la obligatoriedad de emitir informes estadísticos…»). El objeto medido es la norma, pero el contenido es institucionalización. Se contaron como ARM; es la banda donde el criterio pendiente cambia el resultado.
- **Estructura + norma nombrada**: subfamilia de DUD donde la opción afirma que una estructura existe *y* que está reconocida en la normatividad. Son 4 y se trataron igual.

## Totales

| Clase | Opciones | % |
|---|---|---|
| Armonización | 123 | 43.9 % |
| Institucionalización | 143 | 51.1 % |
| Dudosas | 13 | 4.6 % |
| Texto libre | 1 | 0.4 % |
| **Total** | **280** | |

Por eje: eje 1 → 40 ARM / 58 INST / 5 DUD (103). Eje 2 → 16 / 22 / 1 + 1 N/A (40). Eje 3 → 17 / 15 / 2 (34). Eje 4 → 50 / 48 / 5 (103).

**Observables 100 % armonización (12):** 1.1, 1.2, 1.3, 1.6, 1.15, 2.1, 3.1, 4.1, 4.2, 4.3, 4.9, 4.12.
**Observables 100 % institucionalización (9):** 1.4, 1.9, 1.11, 1.17, 2.6, 3.3, 3.4, 4.8, 4.14.
**Observables mixtos o con dudosas (20):** 1.5, 1.7, 1.8, 1.10, 1.12, 1.13, 1.14, 1.16, 2.2, 2.3, 2.4, 2.5, 3.2, 4.4, 4.5, 4.6, 4.7, 4.10, 4.11, 4.13. En 1.12, 1.13, 1.14, 4.4 y 4.11 la mezcla es una sola opción disidente.

Si el criterio pendiente se resuelve como «institucionalización», el balance pasa a ≈93 ARM / 173 INST y 4.9 y 4.12 dejan la lista de puros de armonización para entrar a la de institucionalización.

## Tabla por observable

Formato: `[índice] CLASE — íncipit`. `†` = ARM-mandato. Los textos completos están en `api/question/seed_data/axis_*.py` (llave `a_options`, mismo orden).

### Eje 1 — Igualdad de género

**1.1 Proceso de armonización normativa** (7) — todas ARM
`[1] ARM` Análisis general de las normas vigentes… · `[2] ARM` Análisis específico la normatividad vigente… · `[3] ARM` Identificación de actualizaciones, modificaciones o desarrollo de disposiciones internas… · `[4] ARM` Planificación o programación de una ruta de modificaciones normativas. · `[5] ARM` Aplicación de las actualizaciones… · `[6] ARM` La armonización da cumplimiento al conjunto de obligaciones legales… · `[7] ARM` Proceso participativo para la armonización normativa interna.

**1.2 Norma principal de carácter general** (6) — todas ARM
`[1] ARM` Reconoce o integra explícitamente el término «igualdad de género»… · `[2] ARM` Atiende la observación del Comité CEDAW… · `[3] ARM` …hace referencia y explica otros conceptos… · `[4] ARM` Explicita o desagrega cuál es el alcance… · `[5] ARM` Es de observancia obligatoria… · `[6] ARM` Se encuentra vigente sin una temporalidad…

**1.3 Normas y disposiciones para la igualdad de género** (5) — todas ARM
`[1] ARM` Su diseño incluye un enfoque complejo e integral… · `[2] ARM` …carácter jurídicamente vinculante… · `[3] ARM` Son normas específicas en materia de igualdad de género… · `[4] ARM` Explícita o desagrega cuál es el alcance… · `[5] ARM` Se encuentra vigente sin una temporalidad…

**1.4 Planeación institucional** (6) — todas INST
`[1] INST` instrumento de planeación debidamente formalizado… · `[2] INST` Su contenido aborda a la igualdad de género de manera integral… · `[3] INST` define objetivos y metas claras… · `[4] INST` establece tiempos de ejecución… · `[5] INST` Se definen áreas responsables… · `[6] INST` mecanismos e indicadores de medición de avances…

**1.5 Estructuras para la igualdad de género** (7) — 6 INST, 1 DUD
`[1] DUD` (ver dudosas) · `[2] INST` Está adscrita directamente a la autoridad central… · `[3] INST` Cuenta con atribuciones claras… · `[4] INST` estructura organizacional interna con áreas de trabajo… · `[5] INST` Cuenta con presupuesto propio… · `[6] INST` Cuenta con personal y recursos materiales propios… · `[7] INST` Cuenta con perfiles de contratación oficiales…

**1.6 Principio de paridad en la normatividad** (5) — todas ARM
`[1] ARM` Se establece de manera explícita (no de facto) el principio de paridad… · `[2] ARM` La disposición es jurídicamente vinculante… · `[3] ARM` Se establece la paridad como base, y no como límite máximo… · `[4] ARM` …establece acciones afirmativas… · `[5] ARM` Se aplica en las disposiciones de integración de todos los cuerpos colegiados…

**1.7 Integración paritaria y políticas de aumento** (6) — 5 ARM, 1 DUD
`[1] DUD` (ver dudosas) · `[2] ARM` La política incluye disposiciones o criterios jurídicamente vinculantes… · `[3] ARM` La política favorece el ingreso y permanencia de mujeres… · `[4] ARM` …favorece el ingreso de personas LGBTIQ+. · `[5] ARM` …pueblos originarios, indígenas y/o afrodescendientes. · `[6] ARM` …personas con discapacidad.

**1.8 Estadísticas y diagnósticos** (9) — 2 ARM, 7 INST
`[1] ARM†` Existe una política institucional explícita que solicita la desagregación por sexo-género… · `[2] INST` Existe una instancia o conjunto de instancias responsables… · `[3] INST` Se emite un anuario estadístico… · `[4] ARM†` Existe una política institucional explícita que solicita la realización de diagnósticos… · `[5]–[9] INST` Se cuenta con un diagnóstico sobre… (brechas / violencia contra mujeres / violencia por otras razones / cuidados / diversidades)

**1.9 Programas y actividades de sensibilización** (4) — todas INST
`[1] INST` programa o programas institucionales, formalizados en la planificación… · `[2] INST` actividades formativas como cursos, seminarios y talleres… · `[3] INST` actividades de sensibilización durante fechas clave… · `[4] INST` política de comunicación de temas y materiales…

**1.10 Presupuestos** (7) — 1 ARM, 5 INST, 1 DUD
`[1] ARM†` instrumento interno de planeación y asignación presupuestal (reglamento, manual) que establezca la obligatoriedad… · `[2] INST` El presupuesto ha sido definido a partir de un diagnóstico… · `[3] DUD` (ver dudosas) · `[4] INST` incluye recursos etiquetados… · `[5] INST` Los recursos etiquetados fueron asignados como resultado de la identificación de una problemática… · `[6] INST` Los recursos asignados son adicionales al sueldo… · `[7] INST` La IES asigna recursos aun cuando no existe etiquetado.

**1.11 Evaluaciones en igualdad de género** (5) — todas INST
`[1]–[5] INST` Evaluaciones diagnósticas / sobre políticas / sobre programas / por indicadores de resultados / por indicadores de impacto.

**1.12 Planes y programas de estudio** (6) — 1 ARM, 5 INST
`[1] ARM` Existe una normatividad que establece a la perspectiva de género como requisito para el diseño y aprobación de planes de estudio. · `[2] INST` La perspectiva de género se establece como enfoque transversal en los planes de estudio. · `[3] INST` asignaturas curriculares obligatorias… · `[4] INST` asignaturas optativas… · `[5] INST` asignaturas que parcialmente incorporan… · `[6] INST` actividades de inducción o extracurriculares…

**1.13 Formación docente** (6) — 1 ARM, 5 INST
`[1] ARM†` La formación en igualdad y/o perspectiva de género es obligatoria para el personal… · `[2] INST` programa para desarrollar competencias… · `[3] INST` oferta periódicamente capacitaciones… · `[4] INST` programas formativos de mediana o larga duración… · `[5] INST` capacitaciones específicas para incorporar la PEG en el quehacer docente. · `[6] INST` realiza diagnóstico para conocer la aplicación de la PEG…

**1.14 Investigación académica** (7) — 1 ARM, 5 INST, 1 DUD
`[1] DUD` (ver dudosas) · `[2] INST` Estas instancias están formalizadas y son permanentes. · `[3] INST` líneas de investigación institucionalizadas… · `[4] INST` grupos académicos institucionalizados… · `[5] INST` política para promover la investigación… de manera transversal… · `[6] ARM` política para incorporar la PEG en los criterios para la aprobación de proyectos de investigación… · `[7] INST` acciones afirmativas para impulsar a las mujeres…

**1.15 Evaluación y promoción académica** (4) — todas ARM
`[1] ARM` Los mecanismos y criterios existentes están formalizados y son vinculantes… · `[2] ARM` incorporan la perspectiva de género, particularmente el enfoque de cuidados… · `[3] ARM` incorporan disposiciones favorables… composición paritaria de los grupos evaluadores. · `[4] ARM` reconocen como puntos favorables… la participación del personal académico…

**1.16 Ingreso, permanencia y evaluación estudiantil** (8) — 2 ARM, 5 INST, 1 DUD
`[1] ARM` Los mecanismos y criterios existentes están formalizados y son vinculantes para toda la universidad… · `[2] ARM` incorporan la perspectiva de género, especificar… · `[3] DUD` (ver dudosas) · `[4] INST` mecanismos focalizados en la permanencia de diversidades y disidencias… · `[5] INST` …pueblos originarios… · `[6] INST` …personas con discapacidades. · `[7] INST` …son integrales y no se limitan a apoyos económicos… · `[8] INST` mecanismos o criterios para la conciliación de la vida escolar o laboral con la familiar y de cuidados.
Nota: el objeto es «mecanismos **y** criterios», que fusiona una práctica y una regla; si se quiere pureza, este observable es candidato a redacción, no a etiqueta.

**1.17 Evaluaciones académicas** (5) — todas INST
`[1]–[5] INST` La IES ha realizado evaluaciones sobre planes y programas / docentes / de investigación / por indicadores de resultados / de impacto.

### Eje 2 — Inclusión y no discriminación

**2.1 Políticas institucionales para la inclusión** (7) — todas ARM
`[1] ARM` Considera mecanismos de inclusión y no discriminación específicos para las mujeres… · `[2] ARM` …diversidades sexogenéricas (LGBTIQ+)… · `[3] ARM` …afrodescendientes, originarios y/o indígenas. · `[4] ARM` …personas con discapacidades. · `[5] ARM` Las normas y/o políticas son explícitas en su objetivo y alcance… · `[6] ARM` …carácter jurídicamente vinculante… · `[7] ARM` Incluyen políticas integrales… medidas afirmativas, de inclusión y/o de nivelación.

**2.2 Políticas institucionales y académicas de inclusión** (6) — 2 ARM, 4 INST
`[1] ARM` Se tratan de normas y políticas oficiales y vigentes. · `[2] ARM` Establecen en su literalidad la no discriminación… · `[3] INST` Incluyen actividades institucionales de alto impacto… · `[4] INST` Incluyen materiales de sensibilización… · `[5] INST` Incluyen formación y capacitación… · `[6] INST` Considera la habilitación de sanitarios y otros espacios sin distinción de género.

**2.3 Reconocimiento de la diversidad sexo-genérica** (5) — 1 ARM, 3 INST, 1 DUD
`[1] ARM` El derecho a la identidad de género está establecido en la normatividad y políticas institucionales. · `[2] INST` procedimiento institucional para actualizar el nombre legal y el marcador de género… · `[3] INST` mecanismo formal para la solicitud de reconocimiento social de la identidad de género… · `[4] DUD` (ver dudosas) · `[5] INST` Se implementan actividades de sensibilización…

**2.4 Lenguaje incluyente** (7) — 4 ARM, 3 INST
`[1] ARM` instrumento que establece directrices oficiales para los usos del lenguaje… · `[2] ARM` Formalmente, hay disposiciones para que todas las instancias den cumplimiento… · `[3] INST` Todos los títulos, diplomas y certificados se expiden en femenino para mujeres. · `[4] ARM` Los documentos normativos de la institución usan lenguaje incluyente al referirse a cargos… · `[5] INST` Las credenciales… usan marcas gramaticales femeninas para mujeres. · `[6] ARM` instrumento institucional para prevenir discursos y comunicaciones discriminatorias… · `[7] INST` La IES realiza procesos de sensibilización y capacitación…

**2.5 Prevención primaria** (9) — 2 ARM, 6 INST, 1 N/A
`[1] ARM†` Se establece de manera institucional la responsabilidad de las autoridades universitarias de prevenir… · `[2] ARM` La IES ha emitido de manera formal una declaratoria contra las violencias… · `[3] INST` campañas y actividades de sensibilización… · `[4] INST` formación al alto funcionariado… · `[5] INST` senderos seguros… · `[6] INST` luminarias y otros servicios… · `[7] INST` políticas preventivas de la violencia digital… · `[8] INST` información sobre las rutas de atención… · `[9] N/A` «Otra (mencione cuál o cuáles).» — la única opción abierta de las 280.

**2.6 Trabajo con hombres** (6) — todas INST
`[1] INST` programa formalizado de trabajo con hombres… · `[2] INST` documentos de diseño metodológico… · `[3] INST` enfoque crítico de las masculinidades… · `[4] INST` enfoque interseccional… · `[5] INST` agenda amplia y permanente de actividades… · `[6] INST` enfoques vivenciales y de trabajo autorreflexivo…

### Eje 3 — Cuidados corresponsables

**3.1 Políticas para la corresponsabilidad de los cuidados** (9) — todas ARM
`[1] ARM` política institucional establecida formalmente en instrumentos normativos… · `[2] ARM` Se define formalmente a los cuidados como un derecho… · `[3] ARM` Incluye una definición integral de corresponsabilidad… · `[4] ARM` Reconoce a los cuidados como un compromiso con la igualdad… · `[5] ARM` Incluye un enfoque relacional de género… · `[6] ARM` Incluye disposiciones que favorecen el tiempo de descanso… · `[7] ARM` Contempla licencias o políticas de flexibilidad laboral… · `[8] ARM` Considera el derecho a la desconexión… · `[9] ARM†` Establece acciones de sensibilización, concientización y capacitación…

**3.2 Licencias y permisos** (10) — 8 ARM, 2 DUD
`[1] ARM` Licencia de maternidad superior a la ley para trabajadoras. · `[2] ARM` Permisos de maternidad para alumnas. · `[3] ARM` Licencia de paternidad superior a la ley… · `[4] ARM` Permisos de paternidad para alumnos. · `[5] ARM` Permisos para lactancia superiores a la ley. · `[6] ARM` Licencias y permisos remunerados en más del 75%. · `[7] DUD` (ver dudosas) · `[8] DUD` (ver dudosas) · `[9] ARM` Permisos o licencias menstruales. · `[10] ARM` Permisos para eventos escolares…
Ambigüedad de bloque: las prestaciones se miden por comparación con la ley, lo que las vuelve enunciados sobre el marco normativo laboral interno (ARM). Leídas como beneficios efectivamente otorgados serían INST completo. Es el único observable que puede voltearse entero por una sola decisión.

**3.3 Infraestructura de cuidados** (10) — todas INST
`[1]–[10] INST` salas de lactancia / cambiadores / sanitarios familiares / estancias infantiles / ludotecas / menstruación digna / accesibilidad / descanso / enfermerías / accesibilidad a todos los sectores.

**3.4 Servicios y convenios de cuidados** (5) — todas INST
`[1]–[5] INST` servicio externo gratuito de cuidado infantil / salud psicoemocional gratuita / convenios de precios preferenciales infancias / convenios salud psicoemocional / servicios en periodos vacacionales.

### Eje 4 — Vida libre de discriminaciones y violencias

**4.1 Proceso de armonización normativa** (9) — todas ARM (misma estructura que 1.1)
`[1]–[4] ARM` Análisis general/específico, mujeres / otros grupos · `[5] ARM` Identificación de actualizaciones… · `[6] ARM` Planificación de ruta… · `[7] ARM` Aplicación de las actualizaciones… · `[8] ARM` La armonización da cumplimiento… · `[9] ARM` Proceso participativo…

**4.2 Legislación para atención de casos** (7) — todas ARM
`[1]–[4] ARM` incluye en su legislación / cuenta con marco normativo específico (mujeres y otros grupos) · `[5] ARM` jurídicamente vinculante… · `[6] ARM` vigentes sin temporalidad… · `[7] ARM` explicita el alcance…

**4.3 Normas específicas (protocolo)** (9) — todas ARM
`[1][2] ARM` instrumento institucional específico (mujeres / otros grupos) · `[3] ARM` formalizado y de observancia obligatoria… · `[4] ARM` Define la coordinación entre áreas responsables… · `[5][6] ARM` Establece principios de atención y actuación… · `[7] ARM` Es armónico con los estándares de mayor protección… · `[8][9] ARM†` Cuenta con mecanismos no sancionatorios para modificar condiciones de desigualdad…

**4.4 Personas de primer contacto** (9) — 1 ARM, 8 INST
`[1][2] INST` fueron capacitadas (mujeres / otros grupos) · `[3][4] INST` fueron seleccionadas a partir de valoración de perfiles · `[5] ARM` Existe un código de conducta y/o reglamento que regula la práctica de las figuras de primer contacto. · `[6][7] INST` reciben formación continua · `[8] INST` certificadas en el estándar EC0539 · `[9] INST` El programa ha sido evaluado…

**4.5 Medidas de protección inmediata** (5) — 4 ARM, 1 DUD
`[1] DUD` (ver dudosas) · `[2] ARM` son vinculantes para las áreas… · `[3] ARM` Se emiten de manera provisional y sin necesidad de haber concluido investigación… · `[4] ARM` Incluye enfoque de víctimas… · `[5] ARM` Prevén la posibilidad de que sean dirigidas a la persona señalada como agresora…

**4.6 Estructuras especializadas** (11) — 10 INST, 1 DUD
`[1] DUD` (ver dudosas) · `[2][3] INST` atribuciones claras (mujeres / otros grupos) · `[4] INST` estructura interna con áreas y funciones · `[5] INST` recursos humanos, materiales y financieros propios · `[6] INST` Establece claramente su alcance o ámbito de competencia · `[7] INST` prevén canalizaciones y acompañamiento · `[8][9] INST` áreas especializadas · `[10][11] INST` capacidad sancionatoria

**4.7 Puestos especializados** (9) — 8 INST, 1 DUD
`[1] DUD` (ver dudosas) · `[2][3] INST` se solicita que la titular acredite experiencia y formación · `[4][5] INST` se ofrecen procesos de profesionalización y capacitación · `[6][7] INST` abogadas con formación acreditada · `[8][9] INST` psicólogas con formación acreditada

**4.8 Servicios especializados** (5) — todas INST
`[1]–[5] INST` orientación previa / primeros auxilios psicológicos / acompañamiento psicoemocional completo / notificación continua del estatus / asesoría legal.

**4.9 Responsabilidades de actuación y vinculación interinstitucional** (4) — todas ARM (todas †)
`[1] ARM†` Se establece la responsabilidad de coordinación con otras instituciones… · `[2] ARM†` …de notificar a las autoridades judiciales… · `[3] ARM†` …de asistir a personas en situación de víctima que decidan denunciar… · `[4] ARM†` …de canalizar a servicios de atención psicoemocional…

**4.10 Justicia restaurativa y no repetición** (9) — 7 ARM, 2 DUD
`[1][2] ARM` Se prevé en la normatividad que todas las resoluciones incluyan medidas… · `[3] DUD` (ver dudosas) · `[4] ARM` Las medidas se diferencian de las sanciones y se orientan a la transformación… · `[5] ARM` Las medidas incluyen la reparación de afectaciones académicas o administrativas… · `[6] DUD` (ver dudosas) · `[7] ARM` posibilidad de emitir medidas dirigidas a las comunidades… · `[8] ARM` posibilidad de emitir medidas para cambiar infraestructura, normas, procedimientos… · `[9] ARM†` Se establece la responsabilidad de que las personas responsables acudan a espacios de trabajo reflexivo…

**4.11 Seguimiento de casos** (5) — 1 ARM, 4 INST
`[1] INST` Existe una instancia con facultades para dar seguimiento integral… · `[2] ARM†` Se establece la responsabilidad de notificación continua a las personas en situación de víctima… · `[3][4][5] INST` mecanismo formal de seguimiento a medidas de protección / a sanciones / a medidas de justicia restaurativa.

**4.12 Documentación, sistematización y transparencia** (4) — todas ARM (todas †)
`[1]–[4] ARM†` Se establece la obligatoriedad de emitir informes estadísticos sobre quejas / resoluciones (mujeres y otros grupos).

**4.13 Evaluación de procedimientos formales** (7) — 4 ARM, 3 INST
`[1][2] INST` Existen mecanismos para recabar la opinión de las personas usuarias… · `[3][4][5][6] ARM†` Se establece la obligatoriedad de emitir informes estadísticos de uso interno / públicos… · `[7] INST` Existe evidencia de que la IES utiliza las opiniones recabadas…

**4.14 Evaluación del mecanismo de atención** (10) — todas INST
`[1] INST` evaluación formal con objetivos, metodología, resultados, equipo especializado · `[2]–[8] INST` ámbitos evaluados: satisfacción / uso de opiniones / eficiencia / eficacia / desempeño / suficiencia presupuestaria / resoluciones · `[9] INST` Considera evaluar la armonización del mecanismo con los máximos criterios y estándares de atención a víctimas (INST porque el objeto es la evaluación; es la única opción que usa la palabra «armonización» del lado institucional) · `[10] INST` realizada por instancia externa.

## Las 13 dudosas, con texto íntegro y recomendación

| # | Texto | Por qué dudosa | Recomendación |
|---|---|---|---|
| **1.5 [1]** | «Es una instancia formalmente creada, reconocida jurídicamente dentro de la estructura orgánica y marco normativo de la IES.» | Estructura + norma nombrada: la instancia existe *y* el marco normativo la reconoce. | **INST** — el sujeto es la instancia; el reconocimiento jurídico la califica. |
| **1.7 [1]** | «Se trata de políticas institucionalizadas (no de facto) en la literalidad para el aumento de mujeres y grupos históricamente discriminados en espacios donde su presencia ha sido limitada.» | Dice «institucionalizadas» pero la prueba es textual («en la literalidad», «no de facto»), criterio normativo. | **ARM** — se verifica que la política esté escrita. |
| **1.10 [3]** | «El presupuesto se incluye en algún instrumento de planeación y asignación presupuestal.» | Un recurso constando en un instrumento formal. | **INST** — el objeto medido es el presupuesto; el resto del observable es INST. |
| **1.14 [1]** | «Existen instancias académicas, reconocidas dentro de la normatividad de la IES, dedicadas a la investigación feminista y en estudios de género como línea principal de estudios.» | Estructura + norma nombrada (idéntica a 1.5 [1]). | **INST** — por consistencia con 1.5 [1]. |
| **1.16 [3]** | «Los mecanismos y criterios existentes focalizados en la permanencia de alumnas, se han definido a partir de la identificación de obstáculos en sus trayectorias.» | Criterio normativo + proceso de diagnóstico previo. | **INST** — se mide el proceso de definición. |
| **2.3 [4]** | «A partir de disposiciones institucionales, las personas trans* pueden participar en las diversas actividades académicas, deportivas y artísticas conforme a la autodeterminación de su identidad de género.» | Práctica habilitada explícitamente por una disposición: el caso literal de «práctica registrada en una norma». | **ARM** — la disposición es el antecedente; sin ella la opción no se cumple. |
| **3.2 [7]** | «Flexibilidad en horarios para personas a cargo del cuidado de infancias.» | Puede ser prestación normada o práctica de gestión; no se compara con la ley como [1]–[6]. | **ARM** — por coherencia con el bloque de prestaciones. |
| **3.2 [8]** | «Flexibilidad en horarios para personas cuidadoras de personas adultas mayores, enfermas y/o con discapacidades.» | Igual que [7]. | **ARM** — igual que [7]. |
| **4.5 [1]** | «Se establecen de manera oficial y existe una instancia responsable de su emisión.» | Mezcla explícita en una sola frase: establecimiento oficial (norma) **y** existencia de instancia (estructura). La dudosa más nítida. | **Partir en dos opciones** si el cliente lo permite; si no, **ARM** (el resto del observable es ARM). |
| **4.6 [1]** | «Las estructuras se encuentran institucionalizadas en la normatividad de la IES, con validez y vinculación jurídica.» | Estructura + norma nombrada. | **INST** — consistente con 1.5 [1] y 1.14 [1]. |
| **4.7 [1]** | «Las descripciones de puestos se establecen de manera formal en la normatividad interna de las estructuras responsables de la atención de la violencia por razones de género.» | Elemento institucional (perfil de puesto) establecido en norma. | **ARM** — aquí el objeto medido sí es la norma («se establecen … en la normatividad»). |
| **4.10 [3]** | «Las actas de resolución incluyen, de manera complementaria a las sanciones, medidas de justicia restaurativa y no repetición de carácter obligatorio.» | Práctica documental («las actas incluyen») con carga normativa («de carácter obligatorio»). | **INST** — se verifica sobre las actas emitidas. |
| **4.10 [6]** | «Las medidas incluyen la atención psicoemocional especializada de las personas en situación de víctima como elemento de reparación del daño.» | Contenido de la medida, pero nombra un servicio. | **ARM** — el sujeto sigue siendo «las medidas», como en [4], [5], [7], [8]. |

## La banda ARM-mandato: 30 opciones que dependen del criterio pendiente

Contadas como ARM porque el objeto es la norma, pero cuyo contenido es institucionalización pura. Si «la norma que obliga a hacer X» cuenta como institucionalización, se mueven en bloque:

1.8 [1] [4] · 1.10 [1] · 1.13 [1] · 2.5 [1] · 3.1 [9] · 4.3 [8] [9] · 4.9 [1] [2] [3] [4] · 4.10 [9] · 4.11 [2] · 4.12 [1] [2] [3] [4] · 4.13 [3] [4] [5] [6].

Dos observables completos viven en esta banda y cambiarían de clase entera: **4.9** (4/4) y **4.12** (4/4).

## Observación sobre la definición de «armonización»

En sentido técnico, la armonización normativa es la alineación del marco interno con estándares externos; solo 1.1, 4.1 y 1.2 [2] (CEDAW) la miden así. El resto de lo clasificado como ARM es más bien *existencia y calidad de la norma interna*. Si el nombre que verá la IES es «armonización», 1.1 y 4.1 son los únicos que le hacen honor literal. Queda como observación, no como propuesta.
