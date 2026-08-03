---
type: reference
id: cuestionario-2026-reducido
title: Cuestionario ONIGIES 2026 — versión reducida e indexada
state: current
date: 2026-07-29
---

# Observatorio Nacional para la Igualdad de Género en las IES — Levantamiento 2026

**Cuestionario (versión reducida/indexada)**

> Este documento reduce [[2026-07-03-instrumento-cuestionario-2026]] eliminando boilerplate repetido
> (tablas de opciones "Sí" constante, listas de poblaciones repetidas letra
> por letra, placeholders numéricos de ejemplo) para facilitar su lectura y
> su futura conversión a JSON de inserción. **Ningún texto sustantivo fue
> modificado**; solo se indexó lo repetitivo. Ver
> [[2026-07-03-reduccion-del-cuestionario]] para erratas y decisiones abiertas.

## Leyenda

- **`init_question`** — pregunta numerada inicial (`Observable.init_question`).
  Todas siguen el mismo patrón fijo, **no repetido por observable**: es
  binaria Sí/No; si la respuesta es **No**, se salta el observable completo
  y no se responden Variable A ni B; si es **Sí**, se responden ambas.
- **`a_question`** — pregunta de la tabla "Variable A" (`AQuestion.text`),
  seguida de la lista de opciones (`AOption.text`). En el original cada
  opción tenía una columna "Sí" fija a la derecha; se omite aquí por ser
  constante.
- **`reach_question`** — pregunta de alcance poblacional "Variable B"
  (`ReachQuestion.text`), seguida de las poblaciones aplicables.
- **`reach_instances_question`** — segunda pregunta de "Variable B", sobre
  número de instancias académicas/administrativas (nuevo campo
  `Observable.reach_instances_question`). En el original iba seguida de un
  valor dummy ("1 instancias académicas"); se omite el placeholder.
- **POB-ESTÁNDAR** — lista de 12 poblaciones que se repite en la mayoría de
  las preguntas de alcance (ver sección "Poblaciones" abajo). Cuando un
  observable usa una lista distinta, se enumera explícitamente.

## Información de base

**Estructuras** — número de instancias académicas y administrativas
reconocidas en el marco normativo/organigrama de la IES.

**Poblaciones (POB-ESTÁNDAR)** — poblaciones que integran o se vinculan con
la comunidad de la IES (checklist inicial que la IES marca; corresponde al
fixture `Sector` ya cargado):

1. Alumnado de nivel medio superior
2. Alumnado de nivel licenciatura
3. Alumnado de nivel posgrado
4. Alumnado externo (de otras IES, intercambio o movilidad, servicio
   social, prácticas profesionales, voluntariado, etcétera)
5. Posdoctorantes
6. Personal académico de tiempo parcial / por horas / por asignatura
   (docencia, investigación)
7. Personal académico de tiempo completo (docencia, investigación)
8. Personal administrativo de base
9. Personal administrativo de confianza
10. Personal administrativo por honorarios
11. Población externa (familias, proveedores, etcétera)
12. Público en general (ex-alumnado y/o público asistente a actividades de
    extensión, artísticas, deportivas, etcétera)

**Planes de estudio** — número de planes de estudio vigentes: nivel medio
superior, nivel superior (licenciatura), nivel posgrado (especialidad,
maestría y doctorado).

**Forma de gobierno** — características a marcar:
- Cuenta con una forma de gobierno descentralizada que da autonomía a las
  autoridades de cada instancia académica y/o administrativa
- Cuenta con una forma de gobierno centralizada que dota de facultades a su
  titular para emitir disposiciones vinculantes a todas las áreas
  académicas y administrativas

---

# 1. Materia: Igualdad de género

*Eje de políticas de igualdad sustantiva, inclusión y cuidados
corresponsables*

## Componente: Normas y políticas

### 1.1. Proceso de armonización normativa

**init_question:** 1. ¿La IES ha llevado a cabo un proceso formal para
armonizar su legislación o normatividad interna en materia de igualdad
sustantiva e inclusión, conforme a la Ley General de Educación Superior?

**a_question:** ¿En qué términos se ha realizado este proceso? (Marque
todas las características o elementos que resulten aplicables a este
instrumento)
1. Análisis general de las normas vigentes y aplicables a la IES y sus
   funciones, en materia de igualdad sustantiva, inclusión, no
   discriminación, así como otros derechos humanos.
2. Análisis específico la normatividad vigente en materia de educación
   superior e igualdad sustantiva, inclusión, no discriminación, así como
   otros derechos humanos.
3. Identificación de actualizaciones, modificaciones o desarrollo de
   disposiciones internas, derivado del análisis normativo.
4. Planificación o programación de una ruta de modificaciones normativas.
5. Aplicación de las actualizaciones, modificaciones o desarrollo de
   disposiciones internas.
6. La armonización da cumplimiento al conjunto de obligaciones legales
   aplicables a la IES en estas materias.
7. Proceso participativo para la armonización normativa interna.

**reach_question:** *(especial: sin lista de poblaciones, solo conteo de
instancias)*

**reach_instances_question:** ¿Cuántas instancias académicas y
administrativas se consideró para este proceso de armonización?

### 1.2 Norma principal de carácter general que integra la igualdad de género

**init_question:** 2. El máximo documento jurídico interno de carácter
general de la IES vigente en el año, ¿reconoce o integra explícitamente a
la "igualdad de género" en su contenido?
_Nota: No son aplicables los documentos de planeación, mismos que se
reportan en otro apartado._

**a_question:** ¿En qué términos se reconoce o integra a la "igualdad de
género" en dicho documento? (Marque todas las características o elementos
que resulten aplicables a este instrumento)
1. Reconoce o integra explícitamente el término de "igualdad de género", o
   bien, uno o más términos que remiten a una acepción más amplia o
   integral, entre otros: la igualdad sustantiva, la igualdad entre
   mujeres y hombres o la igualdad entre los géneros.
2. Atiende la observación del Comité para la eliminación de todas las
   formas de discriminación contra las mujeres (Comité CEDAW) al Estado
   mexicano, referente a no tratar de forma indistinta los términos
   igualdad y equidad de género, y remitirse en todo momento a aquel de
   "igualdad de género".
3. Además del o de los términos relativos a la igualdad de género, hace
   referencia y explica otros conceptos que se articulan con la igualdad
   de género en diferentes ámbitos y dimensiones de la materia, como son:
   la no discriminación, inclusión, los cuidados corresponsables y una
   vida libre de violencia, entre otros.
4. Explicita o desagrega cuál es el alcance o ámbito de aplicación de la
   igualdad de género dentro de la IES.
5. Es de observancia obligatoria a las instancias y población que forman
   parte de la IES.
6. Se encuentra vigente sin una temporalidad o fecha de término de
   vigencia, y es resultado de un proceso interno de formalización, de
   acuerdo con las normas y procedimientos previstos por la propia IES.

**reach_question:** ¿A qué poblaciones es aplicable el instrumento?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Cuántas instancias académicas y
administrativas es aplicable el instrumento?

### 1.3 Normas y disposiciones para la igualdad de género

**init_question:** 3. ¿La IES cuenta con normatividad interna focalizada o
especializada específicamente en materia de igualdad de género?

**a_question:** ¿Cuáles de las siguientes características forman parte de
su normatividad interna en materia de igualdad de género? (Marque todas
las características o elementos que resulten aplicables)
1. Su diseño incluye un enfoque complejo e integral a partir de diversos
   ejes de trabajo que buscan incidir en la transformación de las
   diferentes desigualdades de género que existen en la IES, como son:
   paridad, no discriminación, inclusión, cuidados corresponsables y una
   vida libre de violencias.
2. Se trata de normas internas de la IES que tienen carácter jurídicamente
   vinculante y de observancia obligatoria.
3. Son normas específicas en materia de igualdad de género en su
   integralidad, y son distintas a aquellas adoptadas en materia de
   violencia de género. En caso de abordar la materia de violencia de
   género, se focalizan en la prevención primaria y no reducen el alcance
   de la igualdad de género al abordaje de las violencias de género.
4. Explícita o desagrega cuál es el alcance o ámbito de aplicación de la
   igualdad de género dentro de la IES.
5. Se encuentra vigente sin una temporalidad o fecha de término de
   vigencia, y es resultado de un proceso interno de formalización, de
   acuerdo con las normas y procedimientos previstos por la propia IES.

_Nota: No se considerarán para esta pregunta:_
- _Norma máxima reportada en la pregunta anterior._
- _Normas generales que sólo tengan una mención a la igualdad_
- _Normas en materia de violencia de género_
- _Manuales, guías, o documentos de referencia sin observancia jurídica_

**reach_question:** ¿Cuáles son las poblaciones de la IES a las que les son
aplicables las disposiciones normativas específicas en materia de igualdad
de género?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿A cuántas instancias académicas y
administrativas les son aplicables o cuentan con normas internas para la
igualdad de género?

### 1.4 Planeación institucional para la igualdad de género

**init_question:** 4. ¿La IES cuenta con una planeación institucional y
programática (plan, política o programa institucional) de carácter
general en materia de igualdad de género?

**a_question:** ¿Cuáles de las siguientes características forman parte de
la planeación institucional y programática en materia de igualdad de
género? (Mencione todas las características o elementos que resulten
aplicables)
1. Se trata de un instrumento de planeación debidamente formalizado
   mediante un procedimiento de aprobación y/o publicación, por lo que es
   público y se encuentra disponible por medios institucionales.
2. Su contenido aborda a la igualdad de género de manera integral, y no
   se reduce a la actuación frente a la violencia de género.
3. La planeación define objetivos y metas claras en materia de igualdad
   de género.
4. La planeación establece tiempos de ejecución (anuales y multianuales).
5. Se definen áreas responsables de la ejecución de los planes en
   distintas áreas de la IES.
6. Se cuenta con mecanismos e indicadores de medición de avances en su
   gestión, resultados, impacto (este último, sólo si aplica).

**reach_question:** ¿A qué poblaciones es aplicable la planeación
institucional y programática de carácter general (al menos una acción
explícita para cada sector)?
- poblaciones: POB-ESTÁNDAR
- `has_general_planning`: sí — opción extra: "Planeación general sin
  focalizar un sector específico"

**reach_instances_question:** ¿Cuántas instancias académicas y
administrativas cuentan con una planeación interna para la igualdad de
género?

## Componente: Estructuras organizacionales

### 1.5 Estructuras para la igualdad de género

**init_question:** 5. ¿La IES cuenta con una instancia ejecutiva interna
(unidad, coordinación, órgano, departamento) para diseñar, implementar,
dar seguimiento y evaluar políticas y/o acciones institucionales en
materia de igualdad de género aplicables a toda la institución?

**a_question:** ¿Cuáles de las siguientes características están presentes
en dicha instancia? (Marque todas las características o elementos que
resulten aplicables)
1. Es una instancia formalmente creada, reconocida jurídicamente dentro de
   la estructura orgánica y marco normativo de la IES.
2. Está adscrita directamente a la autoridad central o en el primer plano
   de la administración central.
3. Cuenta con atribuciones claras en materia de políticas de
   transversalización e institucionalización de la igualdad de género (no
   de atención a la violencia de género) para toda la IES.
4. Cuenta con una estructura organizacional interna con áreas de trabajo
   (no un sólo puesto, no un enlace, no programa con temporalidad).
5. Cuenta con presupuesto propio, asignado formalmente, para realizar sus
   actividades institucionales.
6. Cuenta con personal y recursos materiales propios y suficientes para
   el área y sus funciones.
7. Cuenta con perfiles de contratación oficiales que establecen el
   requerimiento de experiencia y formación en materia de políticas de
   igualdad de género.

**reach_question:** ¿En qué sectores implementa dicha instancia las
políticas y acciones que desarrolla? (Al menos una acción que impacte
directamente para cada sector)
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Cuántas instancias académicas y
administrativas cuentan con una estructura formal dedicada a
transversalizar las políticas para la igualdad de género a nivel interno?

### 1.6 Principio de paridad de género en la normatividad

**init_question:** 6. ¿La IES cuenta con disposiciones normativas que
establezcan el principio de paridad de género para la conformación de sus
autoridades y espacios de toma de decisiones (administrativos y
académicos)?

**a_question:** ¿Cuáles de las siguientes características están presentes
en las disposiciones en materia de paridad de género de la IES? (Marque
todas las características o elementos que resulten aplicables)
1. Se establece de manera explícita (no de facto) el principio de paridad
   de género en espacios de toma de decisiones (administrativos y
   académicos) de la IES.
2. La disposición es jurídicamente vinculante y de observancia
   obligatoria.
3. Se establece la paridad como base, y no como un límite máximo a la
   comunidad menor representada históricamente en los espacios de toma de
   decisión (administrativos y académicos).
4. En articulación con el principio de paridad de género, establece
   acciones afirmativas que aceleren el avance de las mujeres y
   comunidades menos representadas históricamente en los espacios de toma
   de decisión (administrativos y académicos), sin confundirlo con el
   principio de paridad de género.
5. Se aplica en las disposiciones de integración de todos los cuerpos
   colegiados de máximo nivel y en los cargos de elección donde
   históricamente no exista la paridad.

**reach_question:** *(especial: sin lista de poblaciones estándar; roles
fijos aplicables)*
- Titular de la IES
- Máximo cuerpo colegiado de toda la IES

**reach_instances_question:** ¿En cuántas instancias académicas y
administrativas se aplica de manera explícita el principio de paridad de
género para la conformación de sus autoridades y/o máximas figuras de toma
de decisión?

### 1.7 Integración paritaria y políticas para el aumento de mujeres y grupos históricamente discriminados en áreas segregadas

*(checklist inicial: "Integración paritaria")*

**init_question:** 7. ¿La IES cuenta con una política para aumentar la
presencia, inclusión y participación de mujeres y grupos históricamente
discriminados en espacios académicos, administrativos y escolares, donde
su presencia ha sido limitada?

**a_question:** ¿Cuáles de las siguientes características están presentes
en la o las políticas para aumento de mujeres y grupos históricamente
discriminados en la IES? (Marque todas las características o elementos
que resulten aplicables)
1. Se trata de políticas institucionalizadas (no de facto) en la
   literalidad para el aumento de mujeres y grupos históricamente
   discriminados en espacios donde su presencia ha sido limitada.
2. La política incluye disposiciones o criterios que son jurídicamente
   vinculantes o de observancia obligatoria.
3. La política favorece el ingreso y permanencia de mujeres en áreas
   donde su presencia es limitada y/o históricamente subrrepresentada.
4. La política favorece el ingreso de personas LGBTIQ+.
5. La política favorece el ingreso de personas pertenecientes a pueblos
   originarios, indígenas y/o afrodescendientes.
6. La política favorece el ingreso de personas con discapacidad.

**reach_question:** ¿En qué sectores de la IES se aplica de manera
explícita esta política? (Al menos una política específicamente dirigida)
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿En cuántas instancias académicas y
administrativas se aplica de manera explícita la política referida?

**Bloque adicional (contenido único, no boilerplate) — integración por
sexo-género:**

¿Cuál es la integración por sexo-género de las siguientes autoridades de
la IES?
- Titular de la IES: Mujer
- Máximo cuerpo colegiado de toda la IES: % Mujeres
- Titulares de instancias académicas: % Mujeres
- Titulares de instancias administrativas: % Mujeres

¿Cuál es la integración por sexo-género de las siguientes poblaciones de
la IES? *(nota: aquí la lista es de solo 10 — excluye "Población externa"
y "Público en general", ver [[2026-07-03-reduccion-del-cuestionario]])*
- Alumnado de nivel medio superior % Mujeres
- Alumnado de nivel licenciatura % Mujeres
- Alumnado de nivel posgrado % Mujeres
- Alumnado externo (de otras IES, intercambio o movilidad, servicio
  social, prácticas profesionales, voluntariado, etcétera) % Mujeres
- Posdoctorantes % Mujeres
- Personal académico de tiempo parcial / por horas / por asignatura
  (docencia, investigación) % Mujeres
- Personal académico de tiempo completo (docencia, investigación) %
  Mujeres
- Personal administrativo de base % Mujeres
- Personal administrativo de confianza % Mujeres
- Personal administrativo por honorarios % Mujeres

## Componente: Procesos y recursos institucionales

### 1.8 Estadísticas y diagnósticos con perspectiva de género

**init_question:** 8. ¿La IES cuenta con mecanismos institucionales para
generar estadísticas y diagnósticos con perspectiva de género? Esto es,
mecanismos para la generación de información y procesos diagnósticos de
las desigualdades, discriminaciones y violencias de género y por
cualquier otro motivo.

**a_question:** ¿Cuáles de las siguientes características están presentes
en los mecanismos institucionales para generar estadísticas y diagnósticos
con perspectiva de género? (Marque todas las características o elementos
que resulten aplicables)
1. Existe una política institucional explícita que solicita la
   desagregación por sexo-género de toda la información estadística
   correspondiente a todos los sectores de la IES.
2. Existe una instancia o conjunto de instancias que son responsables de
   sistematizar y asegurar que toda la información de la IES se
   desagregue por sexo-género.
3. Se emite un anuario estadístico con información desagregada por
   sexo-género para todos los sectores de la IES.
4. Existe una política institucional explícita que solicita la
   realización de diagnósticos sobre desigualdades de género en todos los
   sectores de la IES.
5. Se cuenta con un diagnóstico sobre brechas de desigualdad de género en
   la IES con vigencia máxima de 5 años.
6. Se cuenta con un diagnóstico sobre formas de violencia y discriminación
   contra las mujeres por razones de género, con vigencia máxima de 5
   años.
7. Se cuenta con un diagnóstico sobre formas de violencia y discriminación
   por razones de género y/u otras razones, con vigencia máxima de 5 años.
8. Se cuenta con un diagnóstico sobre cuidados corresponsables y/o
   división sexual del trabajo con vigencia máxima de 5 años.
9. Se cuenta con un diagnóstico sobre diversidades sexuales y de género
   con vigencia máxima de 5 años.

**reach_question:** ¿A qué sectores consideran los diagnósticos generales
de igualdad de género de la IES?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Cuántas instancias académicas y
administrativas cuentan con un diagnóstico interno de igualdad de género?

### 1.9 Programas y actividades de sensibilización, concientización y capacitación en igualdad de género

**init_question:** 9. ¿La IES cuenta con programas específicos y
actividades para la sensibilización, concientización y capacitación de
sus comunidades en materia de igualdad de género?

**a_question:** ¿Cuáles de las siguientes características están presentes
en los programas específicos y actividades para la sensibilización,
concientización y capacitación en igualdad de género? (Marque todas las
características o elementos que resulten aplicables)
1. Se trata de un programa o programas institucionales, formalizados en
   la planificación de la IES.
2. Los programas incluyen actividades formativas como cursos, seminarios
   y talleres con perspectiva de género o abordan la agenda de la
   igualdad de género (duración mínima: 2 sesiones, 4 horas).
3. Los programas incluyen actividades de sensibilización durante las
   fechas clave para la igualdad, por ejemplo: el 11 de febrero (día de
   las mujeres y las niñas en la ciencia), el 8 de marzo (día
   internacional de la mujer), junio (mes del orgullo LGBTIQ+), 25 de
   noviembre, etc.
4. Los programas incluyen una política de comunicación de temas y
   materiales para la igualdad de género en medios de amplia difusión en
   las IES.

**reach_question:** ¿A qué sectores de la IES consideran o se dirigen los
programas de sensibilización, concientización y/o capacitación en
igualdad de género?
- poblaciones: POB-ESTÁNDAR
- `has_general_planning`: sí — opción extra: "Planeación general sin
  focalizar un sector específico"

**reach_instances_question:** ¿Cuántas instancias académicas y
administrativas implementaron un programa de sensibilización,
concientización y/o capacitación en igualdad de género?

### 1.10 Presupuestos institucionales para la igualdad de género

**init_question:** 10. ¿La IES cuenta con un presupuesto anual sensible al
género y/o con presupuesto etiquetado específicamente para la igualdad de
género?

**a_question:** ¿Cuáles de las siguientes características están presentes
en la asignación de presupuesto de la IES? (Marque todas las
características o elementos que resulten aplicables)
1. La IES cuenta con algún instrumento interno de planeación y asignación
   presupuestal (reglamento, manual, entre otros) que establezca la
   obligatoriedad y/o los criterios para realizar presupuestos sensibles
   al género y/o presupuestos etiquetados específicamente para la
   igualdad de género.
2. El presupuesto institucional general de la IES ha sido definido a
   partir de un diagnóstico, así como analizado y construido desde la
   perspectiva de género.
3. El presupuesto se incluye en algún instrumento de planeación y
   asignación presupuestal.
4. El presupuesto institucional de la IES incluye recursos etiquetados en
   materia de igualdad de género (no reservados para la atención de las
   violencias).
5. Los recursos etiquetados (si existen) en materia de igualdad de
   género, fueron asignados como resultado de la identificación de una
   problemática de desigualdad de género al interior de la IES, y se
   orienta a su eventual solución.
6. Los recursos asignados son adicionales al sueldo del personal que
   realiza las actividades para la igualdad de género y los gastos
   corrientes de las instancias dedicadas a esta materia (no incluir los
   recursos en materia de violencia de género, ya que se reportará más
   adelante).
7. La IES asigna recursos para proyectos en materia de igualdad de género
   aun cuando no existe un proceso de etiquetado.

**reach_question:** ¿A qué sectores se consideró en la asignación de
presupuesto para la igualdad de género en la IES?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Cuántas instancias académicas y
administrativas ejercieron presupuesto específico para la igualdad de
género?

### 1.11. Evaluaciones en igualdad de género

*(checklist inicial: "Evaluaciones de las políticas de igualdad de
género")*

**init_question:** 11. ¿La IES cuenta o ha realizado alguna evaluación
institucional en materia de igualdad de género de sus políticas,
programas, procesos y/o recursos institucionales?

**a_question:** ¿Cuáles de las siguientes características están presentes
en las evaluaciones institucionales en materia de igualdad de género?
(Marque todas las características o elementos que resulten aplicables)
1. Evaluaciones diagnósticas de desigualdades basadas en el género.
2. Evaluaciones sobre sus políticas y/o planeación institucional para la
   igualdad de género.
3. Evaluaciones sobre sus programas y/o actividades institucionales para
   la igualdad de género.
4. Evaluaciones a partir de indicadores de resultados en materia de
   igualdad de género.
5. Evaluaciones a partir de indicadores de impacto en materia de igualdad
   de género.

**reach_question:** ¿A qué sectores consideran las evaluaciones
institucionales en materia de igualdad de género realizadas en la IES?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿A cuántas instancias académicas y
administrativas consideran las evaluaciones institucionales en materia de
igualdad de género realizadas en la IES?

## Componente: Procesos y recursos académicos

### 1.12 Planes y programas de estudio, y asignaturas para la igualdad de género y con perspectiva de género (docencia)

*(checklist inicial: "Planes y programas de estudio con perspectiva de
género")*

**init_question:** 12. ¿La IES cuenta con planes de estudio con
perspectiva de género y asignaturas para la igualdad de género?

**a_question:** ¿Cuáles de las siguientes características están presentes
en los planes y programas de estudio de la IES? (Mencione todas las
características o elementos que resulten aplicables)
1. Existe una normatividad que establece a la perspectiva de género como
   un requisito para el diseño y aprobación de planes de estudio.
2. La perspectiva de género se establece como un enfoque transversal en
   los planes de estudio.
3. Existen asignaturas curriculares obligatorias específicas en sus
   objetivos, título y contenidos para el aprendizaje y la aplicación de
   la perspectiva de género.
4. Existen asignaturas curriculares optativas específicas en sus
   objetivos, título y contenidos para el aprendizaje y la aplicación de
   la perspectiva de género.
5. Existen asignaturas que parcialmente incorporan en sus contenidos la
   perspectiva de género (al menos en un 50%).
6. Existen actividades de inducción o extracurriculares obligatorias para
   el alumnado que incorporan la perspectiva de género.

**reach_question:** *(especial: sin lista de poblaciones; se mide por
nivel de plan de estudios, con 4 preguntas independientes)*
1. ¿En cuántos planes de estudio se establece como un enfoque transversal
   la perspectiva de género? — nivel medio superior / licenciatura /
   posgrado
2. ¿En cuántos planes de estudio se incorpora al menos una asignatura
   obligatoria específica en nombre y contenidos para la igualdad de
   género? — nivel medio superior / licenciatura / posgrado
3. ¿En cuántos planes de estudio se incorpora al menos una asignatura
   optativa específica en nombre y contenidos para la igualdad de género?
   — nivel medio superior / licenciatura / posgrado
4. ¿En cuántos planes de estudio se incorporan asignaturas con al menos un
   50% de contenidos con perspectiva de género? — nivel medio superior /
   licenciatura / posgrado

**reach_instances_question:** *(no aplica; ver las 4 preguntas anteriores)*

### 1.13 Formación docente con perspectiva de género

**init_question:** 13. ¿La IES cuenta con programas de formación para su
personal académico y administrativo en materia de igualdad y no
discriminación?

**a_question:** ¿Cuáles de las siguientes características están presentes
en la formación del personal académico y administrativo de su IES?
(Mencione todas las características o elementos que resulten aplicables)
1. La formación en igualdad y/o perspectiva de género es obligatoria para
   el personal académico y administrativo de la IES.
2. La IES cuenta con un programa para desarrollar las competencias en
   perspectiva de género dirigido al personal docente.
3. La IES oferta periódicamente capacitaciones específicas en materia de
   igualdad y/o perspectiva de género para su personal académico y
   administrativo (fuera del programa mencionado anteriormente).
4. Las actividades de capacitación son programas formativos de mediana o
   larga duración, son diferentes a charlas o conferencias (o actividades
   de sesiones únicas), y cuentan con objetivos específicos en materia de
   igualdad de género.
5. En el caso del personal académico, se cuenta con capacitaciones
   específicas para incorporar la perspectiva de género en su quehacer
   docente.
6. La IES realiza diagnóstico para conocer la aplicación de la
   perspectiva de género del personal académico, que retroalimente los
   programas o acciones de capacitación que se ofrecen en este sector.

**reach_question:** ¿En qué sectores del personal académico y
administrativo de la IES se implementó la formación durante el año ___?
- poblaciones (NO estándar, lista explícita):
  - Personal académico de tiempo parcial / por horas / por asignatura
    (docencia, investigación)
  - Personal académico de tiempo completo (docencia, investigación)
  - Personal administrativo de base
  - Personal administrativo de confianza
  - Personal administrativo por honorarios
  - Autoridades y alto funcionariado

**reach_instances_question:** ¿En cuántas instancias de la IES se
implementó la formación durante el año que estamos midiendo?

### 1.14 Investigación académica con perspectiva de género

**init_question:** 14. ¿La IES cuenta con investigación académica con
perspectiva de género (centros, líneas de investigación, grupos
académicos para la igualdad de género y no discriminación)?

**a_question:** ¿Cuáles de las siguientes características están presentes
en la investigación académica de su IES? (Mencione todas las
características o elementos que resulten aplicables)
1. Existen instancias académicas, reconocidas dentro de la normatividad
   de la IES, dedicadas a la investigación feminista y en estudios de
   género como línea principal de estudios.
2. Estas instancias académicas están formalizadas y son permanentes (sin
   temporalidad de vigencia).
3. Existen líneas de investigación institucionalizadas en estudios de
   género y feministas dentro de instancias académicas dedicadas a
   distintos ámbitos de conocimientos.
4. Existen grupos académicos institucionalizados en la IES dedicados
   explícitamente a la investigación desde los estudios de género y
   feministas.
5. La institución cuenta con una política para promover la investigación
   en estudios de género y feministas de manera transversal a todas sus
   instancias académicas.
6. La institución cuenta con una política para incorporar la perspectiva
   de género en los criterios para la aprobación de proyectos de
   investigación (liderazgo de mujeres académicas, grupos diversos,
   incorporación de la variable sexo/género).
7. La institución cuenta con acciones afirmativas para impulsar a las
   mujeres en avanzar en sus niveles como investigadoras.

**reach_question:** *(especial: sin lista de poblaciones)*

**reach_instances_question:** ¿Cuántas instancias académicas cuentan con
una área o grupo formal de investigación en estudios de género y
feministas?

**Pregunta adicional (contenido único):** ¿Del total de proyectos de
investigación financiados por la IES cuántos son dirigidos por mujeres?
(proyectos dirigidos por mujeres / total de proyectos)

### 1.15 Mecanismos y criterios de evaluación y promoción académica (docencia e investigación) para la igualdad y no discriminación

**init_question:** 15. ¿La IES cuenta con mecanismos y criterios en
materia de igualdad y no discriminación para las evaluaciones y
promociones de su personal académico?

**a_question:** ¿Cuáles de las siguientes características están presentes
en los mecanismos y criterios en materia de igualdad y no discriminación
en las evaluaciones y promociones académicas? (Mencione todas las
características o elementos que resulten aplicables)
1. Los mecanismos y criterios existentes están formalizados y son
   vinculantes para toda la universidad.
2. Los mecanismos y criterios existentes incorporan la perspectiva de
   género, particularmente el enfoque de cuidados, como un componente que
   comprende las cargas de trabajo y los ritmos de las trayectorias de
   mujeres y otras personas cuidadoras.
3. Los mecanismos y criterios existentes incorporan disposiciones
   favorables para la evaluación con perspectiva de género, como la
   composición paritaria de los grupos evaluadores.
4. Los mecanismos y criterios existentes reconocen como puntos favorables
   para la evaluación la participación del personal académico en
   actividades para la igualdad, no discriminación y una vida libre de
   violencias en la IES.

**reach_question:** *(especial: sin lista de poblaciones; solo
instancias académicas)*

**reach_instances_question:** ¿Cuántas instancias académicas cuentan con
políticas de evaluación y promoción con enfoque de igualdad y no
discriminación dirigidas al personal académico?

### 1.16 Mecanismos y criterios de ingreso, permanencia y evaluación estudiantil para la igualdad y no discriminación

*(checklist inicial: "Mecanismos y criterios de permanencia estudiantil
para la igualdad")*

**init_question:** 16. ¿La IES cuenta con mecanismos y criterios para el
ingreso, permanencia, fortalecimiento de las trayectorias, evaluación,
egreso y titulación de mujeres alumnas y alumnado perteneciente a grupos
históricamente discriminados?

**a_question:** ¿Cuáles de las siguientes características están presentes
en tales los mecanismos y criterios? (Mencione todas las características o
elementos que resulten aplicables)
1. Los mecanismos y criterios existentes están formalizados y son
   vinculantes para toda la universidad, especificar: Ingreso,
   Permanencia, Fortalecimiento de las trayectorias, Evaluación, Egreso,
   Titulación.
2. Los mecanismos y criterios existentes incorporan la perspectiva de
   género, especificar: Ingreso, Permanencia, Fortalecimiento de las
   trayectorias, Evaluación, Egreso, Titulación.
3. Los mecanismos y criterios existentes focalizados en la permanencia de
   alumnas, se han definido a partir de la identificación de obstáculos
   en sus trayectorias.
4. Existen mecanismos y criterios focalizados en la permanencia de
   personas pertenecientes las poblaciones de las diversidades y
   disidencias sexuales y de género.
5. Existen mecanismos y criterios focalizados en la permanencia de
   personas pertenecientes a pueblos originarios, indígenas y/o
   afrodescendientes.
6. Existen mecanismos y criterios focalizados en la permanencia de
   personas con discapacidades.
7. Los mecanismos y criterios existentes en todos los casos son
   integrales y no se limitan a apoyos económicos y/o materiales.
8. Existen mecanismos o criterios para la conciliación de la vida escolar
   o laboral con la familiar y de cuidados.

**reach_question:** ¿En qué sectores del alumnado se implementan dichos
mecanismos?
- poblaciones (NO estándar, lista explícita):
  - Alumnado de nivel medio superior
  - Alumnado de nivel licenciatura
  - Alumnado de nivel posgrado

**reach_instances_question:** ¿Cuántas instancias académicas implementan
dichos mecanismos?

### 1.17. Evaluaciones académicas en materia de igualdad de género

*(checklist inicial: "Evaluaciones de las políticas académicas en materia
de igualdad de género")*

**init_question:** 17. ¿La IES cuenta o ha realizado alguna evaluación en
materia de igualdad de género de sus políticas, programas, procesos y/o
recursos académicos?

**a_question:** ¿Cuáles de las siguientes características están presentes
en las evaluaciones académicas en materia de igualdad de género? (Marque
todas las características o elementos que resulten aplicables)
1. La IES ha realizado evaluaciones sobre sus planes y programas de
   estudio para la igualdad de género.
2. La IES ha realizado evaluaciones docentes para la igualdad de género.
3. La IES ha realizado evaluaciones de investigación para la igualdad de
   género.
4. La IES ha realizado evaluaciones académicas a partir de indicadores de
   resultados en materia de igualdad de género.
5. La IES ha realizado evaluaciones académicas a partir de indicadores de
   impacto en materia de igualdad de género.

**reach_question:** ¿A qué sectores consideran las evaluaciones
académicas en materia de igualdad de género realizadas en la IES?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿A cuántas instancias académicas y
administrativas consideran las evaluaciones académicas en materia de
igualdad de género realizadas en la IES?

---

# 2. Materia: Inclusión y no discriminación

## Componente: Normas y políticas institucionales y académicas

### 2.1 Políticas institucionales para la inclusión

**init_question:** 18. ¿La IES cuenta con políticas institucionales
dirigidas a la inclusión de grupos históricamente discriminados?

**a_question:** Mencione todas las características o elementos que están
presentes en tales políticas de inclusión y no discriminación:
1. Considera mecanismos de inclusión y no discriminación específicos para
   las mujeres en la IES.
2. Considera políticas de inclusión y no discriminación hacia las
   diversidades sexogenéricas (comunidad LGBTIQ+) en la IES.
3. Considera políticas de inclusión y no discriminación hacia las
   personas pertenecientes a grupos afrodescendientes, originarios y/o
   indígenas.
4. Considera políticas de inclusión y no discriminación hacia las
   personas con discapacidades.
5. Las normas y/o políticas son explícitas en su objetivo y alcance para
   la inclusión de grupos históricamente discriminados por razones de
   género y otros motivos.
6. Se trata de políticas internas de la IES que tienen carácter
   jurídicamente vinculante y de observancia obligatoria.
7. Incluyen políticas integrales que toman en consideración la aplicación
   de medidas afirmativas, medidas de inclusión y/o medidas de nivelación.

**reach_question:** ¿En qué sectores se implementan dichas políticas?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Cuántas instancias académicas implementan
dichas políticas?

### 2.2 Políticas institucionales y académicas de inclusión y no discriminación

*(checklist inicial: "Políticas institucionales de no discriminación a la
población LGBTIQ+")*

**init_question:** 19. ¿La IES cuenta con políticas institucionales
dirigidas a la no discriminación de las diversidades sexuales y de género
(LGBTIQ+)?

**a_question:** ¿Cuáles de las siguientes características están presentes
en políticas institucionales y académicas de inclusión y no
discriminación? (Mencione todas las características o elementos que
resulten aplicables)
1. Se tratan de normas y políticas oficiales y vigentes.
2. Establecen en su literalidad la no discriminación en la IES por
   motivos de orientación sexual, identidad de género, expresión de
   género, características sexuales y cualquier otro motivo vinculado con
   la diversidad y disidencia sexual y de género.
3. Incluyen actividades institucionales de alto impacto para la
   visibilidad y conmemoración de las reivindicaciones de las personas
   LGBTIQ+.
4. Incluyen materiales de sensibilización sobre los derechos de las
   personas LGBTIQ+ ampliamente difundidos en la comunidad de la IES.
5. Incluyen formación y capacitación sobre derechos humanos de las
   personas LGBTIQ+.
6. Considera la habilitación de sanitarios y otros espacios sin
   distinción de género para prevenir la discriminación y la violencia
   por razones de género.

**reach_question:** ¿En qué sectores se implementan dichas políticas?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Cuántas instancias académicas implementan
dichas políticas?

### 2.3 Mecanismos institucionales de reconocimiento de la diversidad sexo-genérica

*(checklist inicial: "Mecanismos institucionales para el reconocimiento
legal y social de las identidades de género")*

**init_question:** 20. ¿La IES cuenta con mecanismos institucionales
formales para el reconocimiento de las identidades de género de las
personas que integran su comunidad conforme a su autodeterminación,
particularmente personas integrantes a la comunidad trans\* y no binarie?

**a_question:** ¿Cuáles de las siguientes características están presentes
en los mecanismos institucionales? (Mencione todas las características o
elementos que resulten aplicables)
1. El derecho a la identidad de género está establecido en la
   normatividad y políticas institucionales para la igualdad y no
   discriminación.
2. Se cuenta con un procedimiento institucional para actualizar el nombre
   legal y el marcador de género de las personas cuando han realizado
   previamente su actualización de documentos legales.
3. Se cuenta con un mecanismo formal para la solicitud de reconocimiento
   social de la identidad de género al interior de la institución, que
   favorece que las personas sean nombradas conforme a sus nombres
   elegidos y pronombres, independientemente de que cuenten con sus datos
   legales actualizados.
4. A partir de disposiciones institucionales, las personas trans\* pueden
   participar en las diversas actividades académicas, deportivas y
   artísticas conforme a la autodeterminación de su identidad de género.
5. Se implementan actividades de sensibilización a la comunidad para
   respetar las identidades de género trans\* y no binaries.

**reach_question:** ¿A qué sectores están dirigidas las políticas para el
reconocimiento de la identidad de género?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿En qué instancias se implementan las
políticas de reconocimiento de la identidad de género?

### 2.4 Lenguaje incluyente, no discriminatorio y no sexista

**init_question:** 21. ¿La IES cuenta con criterios institucionales para
el uso del lenguaje incluyente, no discriminatorio y no sexista en la
documentación oficial?

**a_question:** ¿Cuáles de las siguientes características están presentes
en los criterios institucionales para el uso del lenguaje incluyente, no
discriminatorio y no sexista? (Mencione todas las características o
elementos que resulten aplicables)
1. Se cuenta con un instrumento que establece directrices oficiales para
   los usos del lenguaje en toda la institución.
2. Formalmente, hay disposiciones para que todas las instancias de la IES
   (académicas y administrativas) den cumplimiento al lenguaje incluyente
   en todas las formas e instrumentos de comunicación.
3. Todos los títulos, diplomas y certificados se expiden en femenino para
   mujeres.
4. Los documentos normativos de la institución usan lenguaje incluyente
   al referirse a cargos y nombramientos.
5. Las credenciales que expide la IES a su personal usa marcas
   gramaticales femeninas para mujeres.
6. Se cuenta con un instrumento institucional para prevenir discursos y
   comunicaciones discriminatorias hacia las mujeres, las disidencias
   sexogenéricas, pueblos originarios, personas con discapacidades y
   cualquier grupo históricamente discriminado.
7. La IES realiza procesos de sensibilización y capacitación sobre usos
   del lenguaje incluyente y no discriminatorio.

**reach_question:** ¿En cuáles de los documentos normativos que rigen a
los siguientes sectores se aplica la política de lenguaje incluyente, no
discriminatorio y no sexista? (Por ejemplo, reglamento de inscripciones, o
reglamento de posgrado)
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Cuántas instancias académicas y
administrativas implementan la política de uso del lenguaje incluyente, no
discriminatorio y no sexista? (al menos una acción sustantiva)

## Componente: Procesos y recursos institucionales y académicos

### 2.5 Programas y acciones institucionales de prevención primaria de la discriminación y la violencia

**init_question:** 22. ¿La IES cuenta con programas y acciones
institucionales de prevención primaria de las discriminaciones y
violencias por razones de género?

**a_question:** ¿Cuáles de las siguientes características están presentes
en los programas y acciones institucionales de prevención primaria?
(Mencione todas las características o elementos que resulten aplicables)
1. Se establece de manera institucional la responsabilidad de la o las
   autoridades universitarias de prevenir la violencia por razones de
   género.
2. La IES ha emitido de manera formal una declaratoria contra las
   violencias por razones de género.
3. Incluye campañas y actividades de sensibilización sobre las violencias
   por razones de género.
4. Incluye la formación al alto funcionariado en materia de prevención de
   las violencias por razones de género.
5. Incluye senderos seguros para mujeres integrantes de las IES.
6. Incluye luminarias y otros servicios que amplían la seguridad espacial
   con perspectiva de género.
7. Considera políticas preventivas de la violencia digital contra las
   mujeres y por razones de género.
8. Incluye información sobre las rutas de atención de las violencias por
   razones de género.
9. Otra (mencione cuál o cuáles).

**reach_question:** ¿A qué sectores están dirigidas dichos programas y
acciones de prevención?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿En qué instancias se aplican dichos
programas y acciones de prevención (al menos una acción sustantiva)?

### 2.6 Programas y acciones institucionales de trabajo con hombres para la igualdad de género

**init_question:** 23. ¿La IES cuenta con programas y acciones
institucionales de trabajo con hombres desde un enfoque de género,
interseccionalidad y derechos humanos, orientadas a prevenir las
violencias y construir igualdad de género?

**a_question:** ¿Cuáles de las siguientes características están presentes
en los programas y acciones institucionales de trabajo con hombres?
(Mencione todas las características o elementos que resulten aplicables)
1. Existe un programa formalizado de trabajo con hombres en la IES para
   construir igualdad y prevenir las violencias a cargo de las instancias
   responsables en la materia.
2. Cuenta con documentos de diseño metodológico específicos y propios de
   la IES en construcción de igualdad y prevención de las violencias
   focalizados en hombres.
3. Se construye desde un enfoque crítico de las masculinidades que se
   orienta al cambio subjetivo y colectivo de los hombres, como agentes
   de cambio para la igualdad y la eliminación de las desigualdades
   patriarcales.
4. Incluye un enfoque interseccional en el trabajo con hombres, desde un
   diseño que permite reconocer distintas realidades, como son: edad,
   identidad de género, orientación sexual, etnicidad, tipo de población
   de la IES, clase social, entre otras.
5. Incluye una agenda amplia y permanente de actividades para el abordaje
   de las masculinidades.
6. Incluye enfoques vivenciales y de trabajo autorreflexivo para los
   hombres.

**reach_question:** ¿A qué sectores se incluye en las acciones
institucionales de trabajo con hombres? (al menos una acción sustantiva)
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Qué instancias implementan los programas y
acciones institucionales de trabajo con hombres?

---

# 3. Materia: Cuidados corresponsables

## Componente: Normas y políticas institucionales

### 3.1 Políticas institucionales para la corresponsabilidad de los cuidados

**init_question:** 24. ¿La IES cuenta con una política para la
corresponsabilidad de los cuidados, establecida formalmente en
instrumentos normativos y de política institucional, que incluye
criterios y acciones que son superiores a los derechos en la materia
establecidos por ley?
_Nota: Se consideran políticas para la corresponsabilidad de los cuidados
que son adicionales a las presentes en los contratos colectivos de
trabajo, y que impactan en la comunidad académica sin relaciones laborales
con la IES_

**a_question:** ¿Cuáles de las siguientes características están presentes
en la política para la corresponsabilidad de los cuidados? (Mencione
todas las características o elementos que resulten aplicables)
1. Se trata de una política institucional establecida formalmente en
   instrumentos normativos y de política institucional.
2. Se define formalmente a los cuidados corresponsables como un derecho
   que no se restringe a prestaciones laborales, por lo cual se incluye a
   la comunidad estudiantil.
3. Incluye una definición integral de corresponsabilidad social y de
   género de los cuidados que reconoce distintos vínculos y necesidades
   de cuidados, mismos que no se limitan a la reproducción y la crianza o
   al modelo de la familia nuclear, para abarcar a personas adultas
   mayores, infancias fuera del núcleo familiar, personas con alguna
   discapacidad, personas dependientes de cuidados, entre otras.
4. Reconoce a los cuidados corresponsables como un compromiso con la
   igualdad de género y con la redistribución del trabajo de cuidados no
   remunerado históricamente asignado a las mujeres.
5. Incluye un enfoque relacional de género que busca la participación de
   los hombres en labores de cuidados.
6. Incluye disposiciones que favorecen el tiempo de descanso, el
   autocuidado y el bienestar subjetivo y colectivo.
7. Contempla licencias o políticas de flexibilidad laboral que favorecen
   las actividades de cuidados.
8. Considera el derecho a la desconexión en horarios no laborales como
   parte del autocuidado.
9. Establece acciones de sensibilización, concientización y capacitación
   a las comunidades en materia de cuidados corresponsables que fomentan
   la corresponsabilidad de la IES y otros sectores de su comunidad en
   los cuidados.

**reach_question:** ¿Cuáles de los siguientes sectores están considerados
en la política para la corresponsabilidad de los cuidados?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿En qué instancias se implementa la política
para la corresponsabilidad de los cuidados?

## Componente: Procesos y recursos institucionales y académicos

### 3.2 Licencias y permisos con perspectiva de género y de cuidados

**init_question:** 25. ¿La IES cuenta con licencias y permisos para los
cuidados superiores a la ley con una perspectiva de género y de cuidados?

**a_question:** ¿Cuáles de las siguientes características están presentes
en las licencias y permisos con perspectiva de género y cuidados?
(Mencione todas las características o elementos que resulten aplicables)
1. Licencia de maternidad superior a la ley para trabajadoras.
2. Permisos de maternidad para alumnas.
3. Licencia de paternidad superior a la ley para trabajadores.
4. Permisos de paternidad para alumnos.
5. Permisos para lactancia para madres superiores a la ley.
6. Licencias y permisos de maternidad y paternidad remunerados en más del
   75% (de entre los anteriores).
7. Flexibilidad en horarios para personas a cargo del cuidado de
   infancias.
8. Flexibilidad en horarios para personas cuidadoras de personas adultas
   mayores, enfermas y/o con discapacidades.
9. Permisos o licencias menstruales.
10. Permisos para eventos escolares, o eventualidades de salud de las
    infancias u otras personas con necesidades de cuidados que están a
    cargo de la persona cuidadora.

**reach_question:** ¿A qué sectores están dirigidas las licencias y
permisos con perspectiva de género y cuidados?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Qué instancias implementan las licencias y
permisos con perspectiva de género y cuidados?

### 3.3 Infraestructura para el acceso y ejercicio de cuidados en corresponsabilidad

**init_question:** 26. ¿La IES cuenta con infraestructura dentro de sus
instalaciones para el acceso y ejercicio de cuidados en corresponsabilidad?

**a_question:** ¿Cuáles de las siguientes características están presentes
en la infraestructura para el acceso y ejercicio de los cuidados en
corresponsabilidad? (Mencione todas las características o elementos que
resulten aplicables)
1. Se cuenta con salas de lactancia acondicionadas.
2. Se cuenta con cambiadores de pañales en sanitarios no sólo de mujeres.
3. Se cuenta con sanitarios tipo familiares o de acceso universal, que
   posibilitan el cuidado de las infancias.
4. Se cuenta con estancias de cuidados para las infancias.
5. Se cuentan con espacios de juego y recreativos para las infancias
   (ludotecas).
6. Se cuenta con insumos para la menstruación digna.
7. Se cuenta con espacios acondicionados para la accesibilidad a personas
   con discapacidades.
8. Se cuenta con espacios acondicionados para el descanso y el
   autocuidado.
9. Se cuenta con enfermerías o áreas de atención de la salud.
10. La infraestructura destinada para el ejercicio de los cuidados es
    accesible a todos los sectores de la comunidad, incluyendo el sector
    estudiantil.

**reach_question:** ¿A qué sectores está dirigida la infraestructura para
el acceso y ejercicio de los cuidados en corresponsabilidad?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Qué instancias cuentan con infraestructura
para el acceso y ejercicio de los cuidados en corresponsabilidad?

### 3.4 Servicios para el acceso y ejercicio de cuidados en corresponsabilidad

**init_question:** 27. ¿La IES cuenta con convenios y servicios brindados
por instancias externas para el acceso y ejercicio de cuidados,
superiores a la ley?

**a_question:** ¿Cuáles de las siguientes características están presentes
en los convenios y servicios para los cuidados? (Mencione todas las
características o elementos que resulten aplicables)
1. Servicio externo gratuito de cuidado de niñas/os/es adicional a las
   instancias infantiles del IMSS y el ISSSTE.
2. Servicios gratuitos de salud psico-emocional.
3. Convenios para obtener precios preferenciales en servicios de cuidados
   para las infancias.
4. Convenios para acceso a precios preferenciales de salud
   psico-emocional.
5. Actividades y prestación de servicios de cuidados de infancias y
   adolescencias en periodos vacacionales, días de asueto, viernes de
   Consejo Técnico (escuelas públicas), o situaciones especiales que no
   se concilian con el calendario de las IES.

**reach_question:** ¿Cuáles de los siguientes sectores son beneficiarios
de los convenios y servicios para los cuidados?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Qué instancias ofrecen dichos servicios
para los cuidados?

---

# 4. Materia: Una vida libre de discriminaciones y violencias

*Eje de políticas de no discriminación y una vida libre de violencias*

## Componente: Normas y políticas institucionales

### 4.1. Proceso de armonización normativa

**init_question:** 28. ¿La IES ha llevado a cabo un proceso formal para
armonizar su legislación o normatividad interna en materia de violencias
contra las mujeres y otras formas de violencias basadas en el género,
conforme a la Ley General de Educación Superior y otra normatividad
vigente en la misma materia?

**a_question:** ¿En qué términos se ha realizado este proceso? (Marque
todas las características o elementos que resulten aplicables a este
instrumento)
1. Análisis general de las normas vigentes y aplicables a la IES y sus
   funciones, en materia de una vida libre de violencia para las mujeres.
2. Análisis general de las normas vigentes y aplicables a la IES y sus
   funciones, en materia de una vida libre de violencia para otros grupos
   en situación de vulnerabilidad.
3. Análisis específico de la normatividad vigente en materia de una vida
   libre de violencia para las mujeres.
4. Análisis específico de la normatividad vigente en materia de una vida
   libre de violencia para otros grupos en situación de vulnerabilidad.
5. Identificación de actualizaciones, modificaciones o desarrollo de
   disposiciones internas, derivado del análisis normativo.
6. Planificación o programación de una ruta de modificaciones normativas.
7. Aplicación de las actualizaciones, modificaciones o desarrollo de
   disposiciones internas.
8. La armonización da cumplimiento al conjunto de obligaciones legales
   aplicables a la IES en estas materias.
9. Proceso participativo para la armonización normativa interna.

**reach_question:** *(especial: sin lista de poblaciones, solo conteo de
instancias)*

**reach_instances_question:** ¿A qué instancias académicas y
administrativas se consideró para este proceso de armonización?

### 4.2 Legislación para la atención de casos de discriminación / violencia basada en el género

**init_question:** 29. ¿La IES cuenta con legislación en materia de
atención de la discriminación y violencia por razones de género (distinta
a los protocolos de atención)?

**a_question:** ¿Cuáles de las siguientes características están presentes
en dicha legislación? (Mencione todas las características o elementos que
resulten aplicables)
1. La IES incluye en su legislación a la violencia por razones de género
   hacia las mujeres como causa de responsabilidad aplicable de todos los
   sectores de su comunidad.
2. La IES incluye en su legislación a la violencia por razones de género
   hacia otros grupos en situación de vulnerabilidad como causa de
   responsabilidad aplicable a todos los sectores de su comunidad.
3. La IES cuenta con un marco normativo específico que establece la
   responsabilidad de actuación ante casos de violencia y discriminación
   por razones de género para las mujeres.
4. La IES cuenta con un marco normativo específico que establece la
   responsabilidad de actuación ante casos de violencia y discriminación
   por razones de género para otros grupos en situación de vulnerabilidad.
5. Las normas existentes tienen carácter jurídicamente vinculante y de
   observancia obligatoria.
6. Las normas se encuentran vigentes sin una temporalidad o fecha de
   término de vigencia, y son resultado de un proceso interno de
   formalización, de acuerdo con las normas y procedimientos previstos
   por la propia IES.
7. Su contenido explicita o desagrega cuál es alcance o ámbito de
   aplicación de sus disposiciones dentro de la IES.

**reach_question:** ¿A qué sectores es aplicable la legislación para la
actuación ante casos de violencia de género?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Qué instancias aplican la legislación para
la actuación ante casos de violencia de género?

### 4.3 Normas específicas para la atención de casos de discriminación / violencia basada en el género

*(checklist inicial: "Mecanismo específico para la atención de casos de
discriminación / violencia basada en el género")*

**init_question:** 30. ¿La IES cuenta con un instrumento (tipo protocolo)
de actuación ante casos de discriminación y violencia por razones de
género?

**a_question:** ¿Cuáles de las siguientes características están presentes
en dicho instrumento? (Mencione todas las características o elementos que
resulten aplicables)
1. Se trata de un instrumento institucional específico para actuar ante
   la discriminación y violencia por razones de género contra las
   mujeres.
2. Se trata de un instrumento institucional específico para actuar ante
   la discriminación y violencia por razones de género contra otros
   grupos en situación de vulnerabilidad.
3. Se encuentra formalizado y es de observancia obligatoria para el
   personal encargado de la atención y resolución de casos al interior
   de la IES.
4. Define la coordinación entre las áreas responsables de la atención de
   la discriminación y la violencia a fin de garantizar la debida
   diligencia.
5. Establece principios de atención y actuación con enfoque de género
   hacia las mujeres, interseccionalidad y derechos humanos.
6. Establece principios de atención y actuación con enfoque de género
   hacia otros grupos en situación de vulnerabilidad, interseccionalidad
   y derechos humanos.
7. Es armónico con los estándares de mayor protección a las personas en
   situación de víctima.
8. Cuenta con mecanismos no sancionatorios para modificar condiciones de
   desigualdad y discriminación por razones de género en contra de las
   mujeres en la IES.
9. Cuenta con mecanismos no sancionatorios para modificar condiciones de
   desigualdad y discriminación por razones de género en contra de otros
   grupos en situación de vulnerabilidad en la IES.

**reach_question:** ¿A qué sectores considera dicho instrumento?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿En qué instancias se implementa dicho
instrumento?

### 4.4. Personas de primer contacto especializadas en materia de violencias de género

**init_question:** 31. La institución cuenta con figuras de primer
contacto calificado, competente y especializado para orientar a personas
que consideren haber sido víctimas de violencia por razones de género?

**a_question:** ¿En qué términos? (Marque todas las características o
elementos que resulten aplicables a este instrumento)
1. Las personas que brindan atención de primer contacto fueron
   capacitadas para llevar a cabo su labor con enfoque de género hacia
   las mujeres, derechos humanos y atención de las violencias.
2. Las personas que brindan atención de primer contacto fueron
   capacitadas para llevar a cabo su labor con enfoque de género hacia
   otros grupos en situación de vulnerabilidad, derechos humanos y
   atención de las violencias.
3. Las personas que brindan atención de primer contacto fueron
   seleccionadas a partir de un proceso de valoración de sus perfiles con
   enfoque de género hacia las mujeres, derechos humanos y atención de
   las violencias.
4. Las personas que brindan atención de primer contacto fueron
   seleccionadas a partir de un proceso de valoración de sus perfiles con
   enfoque de género hacia otros grupos en situación de vulnerabilidad,
   derechos humanos y atención de las violencias.
5. Existe un código de conducta y/o reglamento que regula la práctica de
   las figuras de primer contacto.
6. Las personas que brindan atención de primer contacto reciben
   formación continua y actualización en estándares vinculados con la
   atención de violencia por razones de género hacia las mujeres.
7. Las personas que brindan atención de primer contacto reciben
   formación continua y actualización en estándares vinculados con la
   atención de violencia por razones de género hacia otros grupos en
   situación de vulnerabilidad.
8. Las personas que brindan atención de primer contacto están
   certificadas en el estándar de competencia EC0539. Atención presencial
   de primer contacto a mujeres víctimas de violencia de género.
9. El programa de primer contacto ha sido evaluado en términos de sus
   resultados alcanzados, considerando la satisfacción de las personas
   usuarias.

**reach_question:** ¿A qué poblaciones se consideró este proceso de
armonización? ⚠️ *texto tal cual aparece en el original — es un error de
copiado (pertenece al patrón de las preguntas de armonización normativa
1.1/4.1, no corresponde al tema de este observable). Se deja verbatim; ver
[[2026-07-03-dudas-del-instrumento-con-el-cliente]], punto 1.*
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿A cuántas instancias académicas y
administrativas se consideró para este proceso de armonización? ⚠️ *mismo
error de copiado que la pregunta anterior.*

### 4.5 Políticas y medidas de prevención secundaria y terciaria de las discriminaciones / violencias basadas en el género enfocadas a las personas responsables de su ejercicio

**init_question:** 32. ¿La IES cuenta con políticas y/o medidas de
protección inmediata ante situaciones de violencia por razones de género
para evitar su reiteración o la ampliación de sus efectos?

**a_question:** ¿Cuáles de las siguientes características están presentes
en las políticas y medidas de protección inmediata de las
discriminaciones / violencias basadas en el género? (Mencione todas las
características o elementos que resulten aplicables)
1. Se establecen de manera oficial y existe una instancia responsable de
   su emisión.
2. Una vez que se emiten, son vinculantes para las áreas de la IES que
   tengan alguna responsabilidad en su implementación.
3. Se emiten de manera provisional y sin necesidad de haber concluido un
   proceso de investigación y/o sanción.
4. Incluye enfoque de víctimas, a fin de que se diseñen conforme a las
   necesidades y particularidades de la persona que se encuentra en dicha
   situación.
5. Prevén la posibilidad de que sean dirigidas a la persona señalada como
   agresora a fin de que desista de cualquier violencia o represalia.

**reach_question:** ¿Qué sectores están considerados en el diseño de las
medidas de protección inmediata?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿En cuántas instancias se implementan
medidas de protección inmediata?

## Componente: Estructuras institucionales

### 4.6 Estructuras especializadas para la atención de casos de discriminación / violencias basadas en el género

**init_question:** 33. ¿La IES cuenta con estructuras especializadas para
atender casos de discriminación y violencia basada en el género?

**a_question:** ¿Cuáles de las siguientes características están presentes
en las estructuras especializadas para atender casos de discriminación /
violencia basada en el género? (Mencione todas las características o
elementos que resulten aplicables)
1. Las estructuras se encuentran institucionalizadas en la normatividad
   de la IES, con validez y vinculación jurídica.
2. Las estructuras cuentan con atribuciones claras en materia de atención
   a la violencia de género hacia las mujeres y resolución de los casos.
3. Las estructuras cuentan con atribuciones claras en materia de atención
   a la violencia de género hacia otros grupos en situación de
   vulnerabilidad y resolución de los casos.
4. Las instancias cuentan con una estructura interna que define áreas y
   funciones organizacionales para la adecuada atención de los casos.
5. Las estructuras cuentan con recursos humanos, materiales y financieros
   propios.
6. Establece claramente su alcance o ámbito de competencia.
7. Las estructuras prevén las canalizaciones y acompañamiento a
   instancias internas o externas, en los casos que sean necesarios.
8. Las instancias cuentan con áreas especializadas en violencias por
   razones de género hacia las mujeres.
9. Las instancias cuentan con áreas especializadas en violencias por
   razones de género hacia otros grupos en situación de vulnerabilidad.
10. Las instancias tienen capacidad sancionatoria en los casos de
    violencias por razones de género hacia las mujeres.
11. Las instancias tienen capacidad sancionatoria en los casos de
    violencias por razones de género hacia otros grupos en situación de
    vulnerabilidad.

**reach_question:** ¿A qué sectores son accesibles dichas instancias
especializadas?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Cuántas instancias cuentan con enlaces u
oficinas para la presentación de quejas por violencia de género?

### 4.7 Puestos especializados para la atención de casos de discriminación / violencias basadas en el género

**init_question:** 34. ¿La IES establece descripciones de puesto
especializados para atender casos de discriminación / violencia basada en
el género, institucionalizados mediante documentos administrativos que
sirvan como referente para el reclutamiento, selección y ocupación de los
puestos?

**a_question:** ¿Cuáles de las siguientes características están presentes
en las descripciones de puesto profesionales especializados en materia de
discriminación / violencia basada en el género? (Mencione todas las
características o elementos que resulten aplicables)
1. Las descripciones de puestos se establecen de manera formal en la
   normatividad interna de las estructuras responsables de la atención de
   la violencia por razones de género.
2. Se solicita que la persona titular de la estructura para la atención
   de casos acredite experiencia y formación suficiente en materia de
   violencias por razones de género hacia las mujeres.
3. Se solicita que la persona titular de la estructura para la atención
   de casos acredite experiencia y formación suficiente en materia de
   violencias por razones de género hacia otros grupos en situación de
   vulnerabilidad.
4. Se ofrecen procesos de profesionalización y capacitación por parte de
   las IES para el personal en atención a las violencia de violencias por
   razones de género hacia las mujeres.
5. Se ofrecen procesos de profesionalización y capacitación por parte de
   las IES para el personal en atención a las violencia de violencias por
   razones de género hacia otros grupos en situación de vulnerabilidad.
6. Se solicita que las abogadas contratadas acrediten formación y
   experiencia suficiente en atención de violencias por razones de género
   hacia las mujeres.
7. Se solicita que las abogadas contratadas acrediten formación y
   experiencia suficiente en atención de violencias por razones de género
   hacia otros grupos en situación de vulnerabilidad.
8. Se solicita que las psicólogas contratadas acrediten formación y
   experiencia suficiente en atención de violencias por razones de género
   hacia las mujeres.
9. Se solicita que las psicólogas contratadas acrediten formación y
   experiencia suficiente en atención de violencias por razones de género
   hacia otros grupos en situación de vulnerabilidad.

**reach_question:** *(especial: sin lista de poblaciones)*

**reach_instances_question:** ¿En cuántas instancias existe personal
especializado para la atención de las violencias por razones de género?

### 4.8 Servicios especializados para la atención de casos de discriminación / violencia basadas en el género

**init_question:** 35. ¿La IES ofrece servicios especializados para las
personas denunciantes, adicionales a la formalización de su procedimiento
formal (queja, denuncia, etc.)?

**a_question:** ¿Cuáles de las siguientes características están presentes
en los servicios especializados que ofrece la IES en el marco de la
atención de casos de discriminación / violencia basada en el género?
(Mencione todas las características o elementos que resulten aplicables)
1. Se ofrecen servicios de orientación previos a la presentación formal
   del procedimiento (queja, denuncia, etc.) o de primer contacto, con
   enfoque de género e interseccionalidad.
2. Se ofrecen servicios de primeros auxilios psicológicos y de contención
   psicoemocional.
3. Se ofrecen servicios completos de acompañamiento psicoemocional.
4. Se ofrecen servicios de notificación continua y oportuna del estatus
   del caso.
5. Se ofrece asesoría y/o acompañamiento legal para presentación de
   denuncias en el ámbito judicial.

**reach_question:** ¿Para qué sectores están disponibles dichos
servicios?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿En cuántas instancias se cuenta con dichos
servicios especializados?

### 4.9 Responsabilidades de actuación para atender casos de discriminación y violencia basada en el género

*(checklist inicial: "Responsabilidades de actuación con instancias
externas para atender casos de discriminación y violencia basada en el
género")*

**init_question:** 36. ¿La IES establece responsabilidades de actuación
que involucran el vínculo con instancias externas para atender casos de
discriminación y violencia basada en el género?

**a_question:** ¿Cuáles de las siguientes características están presentes
en la vinculación interinstitucional para la atención de las violencias?
(Mencione todas las características o elementos que resulten aplicables)
1. Se establece la responsabilidad de coordinación con otras
   instituciones con las que la IES tenga vínculos académicos,
   diplomáticos, de proyectos de colaboración, etcétera, para la atención
   de casos que requieran una actuación coordinada cuando alguna de las
   partes en una situación de violencia se encuentre o pertenezca a tales
   instituciones.
2. Se establece la responsabilidad de notificar a las autoridades
   judiciales sobre hechos que constituyan delitos.
3. Se establece la responsabilidad de asistir a personas en situación de
   víctima que decidan presentar una denuncia judicial.
4. Se establece la responsabilidad de canalizar a servicios de atención
   psicoemocional a personas en situación de víctima, en caso de no
   existir disponibilidad del servicio dentro de la IES o no contar con
   las atribuciones.

**reach_question:** ¿Para qué sectores están disponibles dichos
servicios?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿En cuántas instancias se ofrecen dichos
servicios?

## Componente: Procesos y recursos institucionales

### 4.10 Criterios de resolución y medidas de no repetición en el marco de la justicia restaurativa

**init_question:** 37. ¿La IES establece la responsabilidad de emitir
medidas de justicia restaurativa (no mediación) y/o garantías de no
repetición en todos los casos de discriminación y violencia por razones
de género?

**a_question:** ¿Cuáles de las siguientes características están presentes
en las medidas de justicia restaurativa y/o garantías de no repetición?
(Mencione todas las características o elementos que resulten aplicables)
1. Se prevé en la normatividad de la IES que todas las resoluciones ante
   casos de violencia y discriminación por razones de género hacia las
   mujeres incluyan medidas de justicia restaurativa y no repetición.
2. Se prevé en la normatividad de la IES que todas las resoluciones ante
   casos de violencia y discriminación por razones de género hacia otros
   grupos en situación de vulnerabilidad incluyan medidas de justicia
   restaurativa y no repetición.
3. Las actas de resolución incluyen, de manera complementaria a las
   sanciones, medidas de justicia restaurativa y no repetición de
   carácter obligatorio.
4. Las medidas se diferencian de las sanciones y se orientan
   principalmente a la transformación de las condiciones que
   posibilitaron las violencias y/o discriminación.
5. Las medidas incluyen la reparación de afectaciones académicas o
   administrativas vividas por las personas en situación de víctima
   dentro de la IES como efecto de la discriminación o violencia
   (incluyendo acciones de formación y concientización para evitar
   vuelvan a ocurrir).
6. Las medidas incluyen la atención psicoemocional especializada de las
   personas en situación de víctima como elemento de reparación del daño.
7. Se establece la posibilidad de emitir medidas dirigidas a las
   comunidades donde ocurrieron las violencias como medida de reparación
   del daño colectivo.
8. Se establece la posibilidad de emitir medidas y recomendaciones para
   cambiar infraestructura, normas, procedimientos, etcétera, que
   resulten discriminatorias o hayan posibilitado el ejercicio de las
   violencias.
9. Se establece la responsabilidad de que las personas responsables del
   ejercicio de las violencias, particularmente hombres, acudan a
   espacios de trabajo reflexivo especializados.

**reach_question:** ¿En qué sectores se implementan las medidas de
justicia restaurativa y/o garantías de no repetición?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿A cuántas instancias son aplicables las
medidas de justicia restaurativa y/o garantías de no repetición?

### 4.11 Mecanismos de seguimiento de casos y cumplimiento de resoluciones

**init_question:** 38. ¿La IES cuenta con mecanismos de seguimiento de
casos de discriminación / violencia basada en el género y de las
resoluciones emitidas, en el marco de su ámbito de competencia?

**a_question:** ¿Cuáles de las siguientes características están presentes
en los mecanismos de seguimiento de casos y sus resoluciones emitidas en
el ámbito de su competencia? (Mencione todas las características o
elementos que resulten aplicables)
1. Existe una instancia con facultades para dar seguimiento integral a
   los procesos de atención de las violencias, desde su comienzo hasta su
   conclusión.
2. Se establece la responsabilidad de notificación continua a las
   personas en situación de víctima de todo el proceso.
3. Se cuenta con un mecanismo formal para el seguimiento a las medidas de
   protección emitidas a favor de la persona en situación de víctima, de
   ser el caso.
4. Se cuenta con un mecanismo formal para el seguimiento al cumplimiento
   de las sanciones.
5. Se cuenta con un mecanismo formal para el seguimiento de las medidas
   de justicia restaurativa y no repetición.

**reach_question:** ¿Qué sectores son considerados en el seguimiento de
casos y resoluciones emitidas?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿En cuántas instancias se implementan
medidas de seguimiento de casos y resoluciones emitidas?

### 4.12 Documentación, sistematización de información y transparencia

**init_question:** 39. ¿La IES cuenta con mecanismos de documentación,
sistematización de información y transparencia sobre los casos y
resoluciones emitidas por discriminación / violencia basada en el género,
en su ámbito de competencia?

**a_question:** ¿Cuáles de las siguientes características están presentes
en mecanismos de documentación, sistematización de información y
transparencia sobre los casos y resoluciones emitidas por discriminación /
violencia basada en el género, en su ámbito de competencia? (Mencione
todas las características o elementos que resulten aplicables)
1. Se establece la obligatoriedad de emitir informes estadísticos sobre
   la presentación de quejas por violencia y discriminación por razones
   de género hacia las mujeres atendidos.
2. Se establece la obligatoriedad de emitir informes estadísticos sobre
   la presentación de quejas por violencia y discriminación por razones
   de género hacia otros grupos en situación de vulnerabilidad atendidos.
3. Se establece la obligatoriedad de emitir informes estadísticos sobre
   la resolución de casos de violencia y discriminación por razones de
   género hacia las mujeres atendidas.
4. Se establece la obligatoriedad de emitir informes estadísticos sobre
   la resolución de casos de violencia y discriminación por razones de
   género hacia otros grupos en situación de vulnerabilidad atendidos.

**reach_question:** ¿Qué sectores son considerados en la emisión de
dichos informes?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Cuántas instancias emiten o participan en
la presentación de dichos informes?

### 4.13 Evaluación de atención de procedimientos formales (quejas o denuncias) de atención de casos de violencias de género

*(checklist inicial: "Evaluación de la experiencia de las personas
usuarias de los mecanismos de atención de la violencia de género")*

**init_question:** 40. ¿La IES ha llevado a cabo un proceso de evaluación
de las experiencias y satisfacción de las personas usuarias de los
procedimientos formales (queja o denuncia) de atención de casos de
violencia por razones de género?

**a_question:** ¿Cuáles de las siguientes características están
presentes? (Mencione todas las características o elementos que resulten
aplicables)
1. Existen mecanismos para recabar la opinión de las personas usuarias de
   los procedimientos formales (queja o denuncia) de atención de casos de
   violencia por razones de género en contra de las mujeres.
2. Existen mecanismos para recabar la opinión de las personas usuarias de
   los procedimientos formales (queja o denuncia) de atención de casos de
   violencia por razones de género en contra de otros grupos en
   situación de vulnerabilidad.
3. Se establece la obligatoriedad de emitir informes estadísticos de uso
   interno sobre la satisfacción de las personas usuarias durante proceso
   de presentación de quejas por violencia y discriminación por razones
   de género en contra de las mujeres.
4. Se establece la obligatoriedad de emitir informes estadísticos de uso
   interno sobre la satisfacción de las personas usuarias durante proceso
   de presentación de quejas por violencia y discriminación por razones
   de género en contra de otros grupos en situación de vulnerabilidad.
5. Se establece la obligatoriedad de emitir informes estadísticos públicos
   sobre la satisfacción de las personas usuarias durante el proceso de
   presentación de quejas por violencia y discriminación por razones de
   género en contra de las mujeres.
6. Se establece la obligatoriedad de emitir informes estadísticos públicos
   sobre la satisfacción de las personas usuarias durante el proceso de
   presentación de quejas por violencia y discriminación por razones de
   género en contra de otros grupos en situación de vulnerabilidad.
7. Existe evidencia de que la IES utiliza las opiniones recabadas de las
   personas usuarias para optimizar sus mecanismos de atención.

**reach_question:** ¿Qué sectores son considerados en la emisión de
dichos informes?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Cuántas instancias emiten o participan en
la presentación de dichos informes?

### 4.14 Evaluación de atención de mecanismo de atención de las violencias por razones de género

**init_question:** 41. ¿La IES ha llevado a cabo un proceso de evaluación
de su mecanismo de atención de las violencias por razones de género?

**a_question:** ¿Cuáles de las siguientes características están
presentes? (Mencione todas las características o elementos que resulten
aplicables)
1. Se trata de una evaluación formal que cuenta con objetivos,
   metodología, resultados y fue realizada por un equipo de evaluación
   especializado.
2. Considera dentro de los ámbitos a evaluar la satisfacción de las
   personas usuarias del mecanismo.
3. Existe evidencia de que la IES utiliza las opiniones recabadas de las
   personas usuarias para optimizar sus mecanismos de atención.
4. Considera dentro de los ámbitos a evaluar la eficiencia en la
   implementación de los procedimientos (tiempo de espera para obtener
   una primera cita, tiempo de espera para resoluciones, carga de trabajo
   del personal operativo).
5. Considera dentro de los ámbitos a evaluar la eficacia de los
   procedimientos (tasa de casos resueltos, tasa de casos pendientes).
6. Considera dentro de los ámbitos a evaluar el desempeño del personal
   operativo.
7. Considera dentro de los ámbitos a evaluar la suficiencia
   presupuestaria de la instancia responsable del procedimiento de
   atención.
8. Considera dentro de los ámbitos a evaluar las resoluciones emitidas
   por las autoridades competentes.
9. Considera dentro de los ámbitos a evaluar la armonización del
   mecanismo con los máximos criterios y estándares de atención a
   víctimas.
10. La evaluación ha sido realizada por alguna instancia externa a la
    responsable del mecanismo de atención.

**reach_question:** ¿Qué sectores son considerados en la emisión de
dichos informes?
- poblaciones: POB-ESTÁNDAR

**reach_instances_question:** ¿Cuántas instancias emiten o participan en
la presentación de dichos informes?
