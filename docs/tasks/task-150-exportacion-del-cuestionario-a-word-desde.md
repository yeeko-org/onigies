---
type: task
id: task-150
title: Exportación del cuestionario a Word desde el dashboard
state: closed
date: 2026-09-11
owner: ai
parent: "[[task-2]]"
source: ["[[2026-09-04-reunion-con-ruben]]"]
related: ["[[2026-09-04-reunion-con-ruben]]", "[[task-116]]", "[[task-50]]", "[[task-151]]", "[[2026-09-22-exportacion-del-cuestionario-a-word]]", "[[task-161]]", "[[task-162]]", "[[task-20]]", "[[2026-09-23-reunion-ruben]]"]
---

# Exportación del cuestionario a Word desde el dashboard

Paso tres de los cinco que Rubén enumeró en la reunión del 4 de septiembre para publicar el cuestionario, y la pieza que cierra el principio de fuente única: si el dashboard manda sobre los textos ([[adr-0014]], [[adr-0015]]), el Word tiene que **salir** de ahí y no editarse aparte.

**El problema que resuelve.** Rubén venía editando en Word y Ricardo en la base, y eso duplica la fuente. Ricardo lo planteó al revés, `[25:55]`: «lo que yo te decía es al revés: que ya no edites nada en Word, que tú lo edites en el dashboard y agregas un botón de exportación […] y entonces el Word ya no hace formato, entonces ya no tienes que editar en dos lados, y la fuente, la única fuente, el único lugar donde está…».

**La objeción de Rubén, que es el criterio de calidad.** `[26:24]` «yo no lo digo por aquí, lo digo porque otras veces exporto cosas de plataformas y es media hora estar poniéndoles espacios». A eso Ricardo respondió con «formato a medias», `[35:01]`: «algo no crudo, crudo, que tengas que…, sino algo en lo que ya des pocas ediciones de tu parte; la parte fina, para no tardarme yo haciéndola».

**El documento que Rubén quiere producir con esto**, `[24:16]`: «hay que generar una especie de documento que se llame "Cuestionario final final", y ya con los errores que tenga, ni modo, que se quede […] Y con base en ese documento nada más me explicas cómo entrar a corregir, corrijo, y tú ya con eso publicas».

**Por qué corre prisa aunque la plataforma no esté lista.** Las IES necesitan el documento antes que la plataforma para pedir información a sus áreas una sola vez ([[task-41]]), `[23:38]`: «incluso lo necesitan antes de la plataforma […] porque tienen que pedirle la información a las áreas».

## Input obligado: el formato que hay que respetar

`docs/records/assets/vf-2025-ONIGIES-maquetado.docx` es el cuestionario con el formato que el cliente ya maquetó y entregó. **La exportación tiene que producir algo compatible con ese formato**, no un volcado con estilos propios. Es la referencia visual y estructural de esta task.

## Esto no se resuelve aquí

Cómo exportar los datos para que tengan sentido en papel —qué se agrupa, qué encabezados, cómo se rinden las tablas de criterios y las opciones, qué se omite— **es trabajo de su propia sesión**. Esta task guarda el encargo, el porqué y el formato de referencia; el diseño se hace cuando se abra.

Estimación de Ricardo en la reunión, `[26:35]`: «es algo que me va a tomar una hora, y esa hora creo que vale la pena». Léase como su expectativa, no como alcance acordado.

**Alcance ampliado que él mismo propuso** y que conviene decidir dentro de la sesión: que la descarga viva también en la parte pública, `[27:08]` «Incluso esa descarga podría estar en la plataforma también pública […] así pueden descargar el cuestionario y ya no depende de que se los pases».

## Sesión del 2026-09-22: primera versión construida

Record de la sesión: [[2026-09-22-exportacion-del-cuestionario-a-word]]. Rama `task-150-word-export`.

**Qué quedó.** El constructor vive en `api/question/export/` (`questionnaire.py` con `build_questionnaire_docx()`, `writer.py` con las primitivas de python-docx, `texts.py` con toda cadena fija, `make_template.py` que regenera `template.docx` a partir del maquetado). Campo nuevo `Observable.note` con la migración `indicator/0011`, que además siembra las tres notas del maquetado (1.2, 1.3 y 3.1); Rubén las edita en «Definición del observable». La descarga es pública, sin token, a través del modelo `PublicDocument` ([[task-151]]): `GET /api/public-documents/cuestionario-2026/download/`. El botón «Descargar Word» en la barra del interruptor del cuestionario (`QuestionnaireGate.vue`) apunta a esa URL. Los paneles de Poblaciones y Autoridades de información de base muestran la nota recíproca hacia el 1.7.

**Decisiones de Ricardo en la sesión.**

- Es un documento de referencia, no un formulario: «no es un cuestionario para que llenen, sirve solo como referencia». Se eliminaron la columna «Sí / Parcialmente / No» de las opciones A, el número antes de «instancias académicas / administrativas» y el número antes de los planes.
- python-docx aprobado como dependencia; se descartó pandoc (perdía fuente del cuerpo, bordes de tabla y exigía un paquete de sistema en el servidor compartido de Yeeko) y docxtpl (metía la lógica condicional en el Word).
- Regla de fidelidad: el texto sale de la base y la exportación normaliza lo que en el maquetado era inconsistente (niveles de encabezado, puntuación de números de observable, títulos viejos de la lista de verificación, comillas rectas); el maquetado manda solo en lo visual.
- Índice como campo vivo con actualización al abrir el documento.
- Textos sin fuente en la base: constantes en `texts.py`, validadas una por una. Las etiquetas «Variable A/B» salen de `QuestionType.public_name`; fuera la línea «proyectos de investigación de un total de ____» (no existe en la base), la marca «O» de la lista de verificación y las tres líneas de nivel bajo los planes (el texto ya termina en el nivel); la etiqueta de la titular sale del sector `is_ies_head`; queda un solo título «Lista de verificación inicial».
- Las notas del instrumento viven en `Observable.note`; las tres se imprimen tras la pregunta inicial. Ricardo aceptó que la del 1.3, que en el maquetado iba tras la tabla A, quede ahí también.
- Notas cruzadas del 1.7: en el observable, «Las cifras de composición por sexo-género de autoridades y poblaciones que evalúa este observable se capturan en los apartados «Poblaciones» y «Autoridades» de la sección Información de base.» —así imprime el Word, con los grupos en el orden de la base; la redacción que Ricardo aprobó llevaba «Autoridades» primero y él aceptó el orden de la base—; en cada apartado de información de base, «Las cifras de este apartado alimentan la calificación del observable 1.7.» (número desde la base).
- Una sola ruta de descarga, la pública; la vista solo para revisoras de la primera ronda se eliminó. Los registros generados de `PublicDocument` no se pueden borrar desde el API.
- Limpieza de datos: producción no tenía preguntas «Nueva pregunta»; en local se borraron `ReachQuestion` 36, `BQuestion` 41 y su fila puente 124 del 1.12.

**Lo que Rubén tiene que revisar** (para decírselo con precisión):

- El Word exportado completo contra su «Cuestionario final final».
- Las instrucciones de «Estructuras» y «Planes de estudio»: están vacías en la base y por eso no salen en el Word; las llena desde el dashboard.
- Las tres notas (1.2, 1.3, 3.1), ya editables en el observable.
- El año «2025» en la instrucción de la lista de verificación («Identifique si su IES tuvo vigentes en 2025 avances…»), fijo en `texts.py`.
- La redacción «Planeación general sin focalizar un sector específico» (ver [[task-160]]).
- «Levantamiento 2026» y las demás líneas de la portada: viven en la plantilla (`template.docx`, derivada del maquetado), no en `texts.py`; cambiarlas es regenerar la plantilla.
- Los cambios que el Word introduce frente al instrumento que las IES ya conocen:
  - las etiquetas «Variable A/B» se acortan a los nombres públicos de `QuestionType`;
  - «Titular de la IES:» en lugar de «La persona titular de la institución es:»;
  - sale la línea de respuesta del 1.14 («proyectos de investigación de un total de ____»);
  - los apartados de información de base van en el orden de la base;
  - la nota del 1.3 se imprime antes del bloque A (en el maquetado iba tras la tabla A);
  - las opciones de la titular son ahora Mujer / Hombre / No binaria.
- Dos datos de producción revisados hoy por SSH: «Forma de gobierno», «Estructuras» y «Planes de estudio» tampoco tienen instrucción en producción; y una pregunta general más una instrucción de grupo todavía dicen «sexo y género» en producción (la convención es «sexo-género»).

**Decisiones finales del 2026-09-22** (tras el critic de cierre):

- La línea del 1.14 queda fuera: «Opción 1». La alternativa era sacarla de los `verbose_name` de `SpecialResponse.total/complying`.
- La numeración de preguntas se queda en el Word: «Se queda y se anota en la tarea aplicar al dashboard». La numeración de [[task-20]] aplica solo al dashboard.
- El slug de los documentos generados es de solo lectura: «ok».
- En la lista pública, la fecha de un documento generado es la hora de generación: «Sí».
- El Word sembrado nace publicado: «No, que nacer como publicado está bien».
- «No binaria» se agrega a las opciones de la titular: «Sí agrégalo».
- El deploy se hace en una sesión nueva justo después del commit; las pruebas, después del deploy ([[task-161]]).

**Deploy hecho el 2026-09-22** (detalle en [[2026-09-22-exportacion-del-cuestionario-a-word]], sección «Deploy»): commit db07698 en `production`, `python-docx` instalado, migraciones `indicator/0011`, `documents/0001` y `0002` aplicadas, `migrate_ps_schemas` corrido (insertó tres filas de `Collection`: `survey`, `general_package` y `public_document`), frontend publicado en Netlify. La descarga pública responde en producción con el .docx generado desde la base. Falta el enlace a la URL de descarga en el sitio público legado (servidor de la UNAM). Pendiente de decisión de Ricardo, de prioridad baja: si la descarga pública se cachea ([[task-162]]).

**Pruebas de regresión: plan acordado.** Las pruebas 1, 3 y 4 las escribe un ejecutor después del deploy; la 2 es opcional. Detalle en [[task-161]]: (1) descarga pública —anónimo 200 con tipo y nombre de adjunto, slug desconocido 404, borrador 404 anónimo y 200 para revisora—; (2, opcional) conteos estructurales del constructor sobre un fixture chico más la nota del 1.7; (3) `template.docx` conserva los estilos y numeraciones que busca el writer (`Option Table`, `List Item`, `OnigiesLetter`, `image2.png`, `updateFields`); (4) `PublicDocument` —archivo-o-generador 400, gestión cerrada a anónimos e IES, slug desduplicado, borrado y cambio de slug de un generado rechazados—.

## Criterios de aceptación

- [ ] Desde el dashboard se descarga el cuestionario completo en .docx (en producción la URL pública a la que apunta el botón devuelve el .docx; falta el clic desde el dashboard)
- [ ] El resultado respeta el formato de `vf-2025-ONIGIES-maquetado.docx` lo bastante para que Rubén no reformatee más de unos minutos
- [ ] Rubén produjo con ella el «Cuestionario final final» y lo mandó a las IES

## Reunión con Rubén, 2026-09-23, y cierre

Fuente: [[2026-09-23-reunion-ruben]]. Ricardo, `[11:00]`: «¿viste el exportador cómo quedó?». Rubén, `[11:18]`: «Más o menos. Se ve casi idéntico». Ricardo, `[11:21]`–`[11:25]`: «¿no le harías ningún cambio? Bueno, yo hice algunos cambios: quité algunas cosas, puse otras, porque estandaricé». Rubén, `[11:34]`: «no lo revisé a detalle, porque además ya había terminado los cambios; ya los mandé a las IES. Pero sí vi lo que me mandaste, y cuando lo abrí dije: es casi igual, salvo algunas cositas». Ricardo, `[11:52]`: «¿Quieres comentármelas de una vez, si está fácil?»; Rubén, `[11:59]`: «Veamos primero el cuestionario». Al final, Ricardo, `[1:20:31]`–`[1:20:37]`: «¿Tenías un comentario de la exportación, o nada?»; Rubén pasó a las buenas prácticas sin dar ninguno (`[1:20:36]`, `[1:20:44]`). `[1:24:28]` (párrafo con dos voces fundidas, duda 4 de la limpia): «Las preguntas se pueden descargar, y la idea de ese Word es que después lo exportes a PDF. Ya quedó».

Las notas del observable, que el Word imprime: Ricardo, `[25:15]`–`[25:34]`, «Esto es algo que tú habías puesto como notas […] son aclaraciones. Solo tres lugares lo tienen, pero podríamos ponerlo sin problema en otros lugares»; Rubén, `[25:44]`–`[25:46]`, «Sí, lo podemos checar, pero está bastante bien así como quedó»; Ricardo, `[25:46]`, en la 1.3 «la nota estaba abajo de esta pregunta, y yo las puse todas al principio», y `[26:43]`, «se pueden ir agregando en el dashboard a medida que queramos, en el mismo lugar de los observables».

**Cerrada el 2026-09-23 por decisión de Ricardo:** el exportador queda cerrado, sin más cambios. Los criterios se dejan como estaban, porque el cierre descansa en su declaración y no en ellos: el primero está cumplido en producción por la URL pública (el clic desde el dashboard no se verificó); del segundo, Rubén solo dijo «casi idéntico»; del tercero, que mandó sus cambios a las IES, sin decir si fue con el Word exportado. Lo que sigue vive en sus tasks, que pasaron de hijas de esta a hijas de [[task-2]] para que el cierre no las arrastre: [[task-158]] (errores de borrado en EditCommon), [[task-161]] (pruebas) y [[task-162]] (caché).
