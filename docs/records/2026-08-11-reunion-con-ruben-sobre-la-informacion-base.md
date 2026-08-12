---
type: record
id: 2026-08-11-reunion-con-ruben-sobre-la-informacion-base
title: "Reunión con Rubén: la sección de información base antes de abrirla a las IES"
date: 2026-08-11
---

# Reunión con Rubén: la sección de información base antes de abrirla a las IES

Reunión de 59 minutos entre Ricardo y Rubén (Rubí), responsable de ONIGIES, el 11 de agosto de 2026. La transcripción cruda y una versión organizada por tema viven en el repositorio written.django, en su carpeta de records, con el id `2026-08-11-transcripcion-organizada-reunion-con-ruben-onigies`; los proyectos no se enlazan entre sí, así que se cita en texto plano. Los timestamps de esta acta referencian la transcripción cruda.

Esta acta separa a propósito tres cosas que la conversación mezcla: **acuerdos** (lo que Rubén aprobó o pidió), **decisiones de Ricardo** (lo que él resolvió, con o sin venia de Rubén) y **aperturas** (lo que quedó sin cerrar). La distinción no es cosmética: una primera lectura del acta organizada convirtió en acuerdos varias cosas que en el raw son descripciones, autocríticas o propuestas sin respuesta, y una auditoría de fidelidad las corrigió. Donde ocurrió, se anota.

## Calendario

La única fecha que puso Rubén es **jueves 13: la sección visible; viernes 14: anuncio en la reunión con los enlaces** (las personas enlace de las IES). El ofrecimiento de Ricardo de subir los cambios el miércoles por la noche quedó sin respuesta de Rubén y no es, por tanto, un compromiso acordado.

Plan interno de Ricardo para llegar: trabajar hoy y la madrugada para subir la noche previa a la presentación los cambios fundamentales, y poco antes dejar lista la edición de `GeneralGroup` y `GeneralQuestion` para que el equipo de Rubén edite lo fino sin tocar el seed ni el admin.

Rubén revisará los cambios de redacción antes de la publicación definitiva. **La prueba adicional del equipo la pidió Ricardo**, no Rubén: fue propuesta suya y Rubén respondió «Buenísimo».

En el tramo del recordatorio automático se mencionaron fechas de cierre de periodo. **Fueron ejemplo retórico, no fechas reales**, y así lo aclaró Ricardo: no hay nada que verificar ni que agendar a partir de ellas.

## 1. Buenas prácticas y el estatus «no acreditado» `[08:18–10:14]`

Las revisoras del equipo de Rubén ya trabajaron con la plataforma sin problemas. La mayoría de las prácticas enviadas no califican, y eso habrá que comunicarlo con cuidado en la reunión del viernes; Rubén valora que el estatus se llame **«no acreditado»** porque no dice que la práctica sea mala, solo que no acredita los criterios. El estatus ya existe y está sembrado como `bp_rejected` («No acreditada») en `api/flow/seed.py`: no hay nada que construir.

Dato de proceso que conviene no perder: el equipo partió la revisión en dos fases no previstas — primero un **cotejo** de que existan los documentos probatorios, y solo después la revisión de calidad, para no duplicar trabajo si falta lo básico. Ricardo confirmó que el «rebote» automático no hace falta en la plataforma: es metodológico del equipo, no del sistema. Este dato es el que sostiene [[adr-0011]].

## 2. Despliegue por secciones `[10:14–11:53]`

Rubén reiteró la dosificación ya decidida en [[adr-0007]]: arrancar solo con la información base porque todo lo demás depende de que esa parte esté bien resuelta, y presentar después el instrumento completo por ejes. Nada nuevo; el ADR sigue vigente tal cual.

## 3. Demo de la sección `[11:53–15:11]`

**Corrección de fidelidad: Rubén no validó el comportamiento de los panels.** El colapso automático al completar un grupo **falló en vivo** durante la demo, `[13:24]` — no llegó a verse funcionando. Es un bug y tiene task propia: [[task-105]].

Los dos pendientes de presentación que salieron aquí y en `[27:36–29:38]` son **autocríticas de Ricardo**, no observaciones de Rubén: mejorar la disposición tipo tabla, porque en textos cortos como los planes de estudio el espaciado dificulta identificar el contenido; y mover el número de conteo para que no quede pegado al margen derecho. Ambas se absorben en [[task-96]].

## 4. Evidencia probatoria `[15:11–15:40]`

**Acuerdo:** Rubén pide quitar la opcionalidad de la evidencia probatoria, porque sí se va a necesitar, sobre todo en el organigrama; en el resto de los bloques quizás no. Ricardo quitó el rótulo «(opcional)» en el momento.

**Decisión posterior de Ricardo (misma jornada, tras la reunión):** no habrá obligatoriedad técnica. Razonada en [[adr-0011]]; cierra [[task-68]].

## 5. Instrucciones, títulos y subtítulos editables `[15:40–17:26]`

**Propuesta de Ricardo, sin respuesta de Rubén:** cada bloque tendrá su propia instrucción, título y subtítulo, **editables desde el dashboard** igual que hoy se editan los criterios de buenas prácticas; también se podrán editar las preguntas. Fue un turno suyo que Rubén no contestó, así que no es acuerdo: es la dirección que Ricardo anunció y que después ejecutó. (El «complemento» que mencionó en la llamada quedó **descartado** al diseñar el modelo, hasta que aparezca un caso real que lo pida — ver [[task-107]].)

**Acuerdo:** la evidencia probatoria aplica **a todo el bloque, no por ítem** — ratifica el nivel que [[adr-0010]] ya había fijado (`GeneralGroupResponse`) y responde en parte el criterio pendiente de [[task-57]].

Es el tema con más consecuencias de modelo de datos de toda la reunión, y hoy no existe nada de eso: `GeneralGroup` en `api/indicator/models.py` tiene cinco campos y ninguno de texto largo, y no está dado de alta como catálogo del dashboard. Es la raíz [[task-101]].

**Sin cambio:** Ricardo explicó que unificó la pregunta de poblaciones de generales con la equivalente dentro de un observable. Es la implementación de [[adr-0004]], que Rubén vio y no objetó.

## 6. Columna «no binaria» `[17:26–22:03]`

**Acuerdo:** se agrega una columna «no binaria» junto a mujeres y hombres. Rubén señala que ya hay instituciones —la UNAM entre ellas— con personas no binarias formalmente registradas. Las tres columnas existen para producir estadísticas de distribución por género.

**Acuerdo:** la **pregunta previa** («¿se mide la población no binaria?») aplicaría solo en poblaciones. En autoridades Rubén la considera de facto un acto político —«nadie va a poner que tiene un rector no binario»—, aunque acepta incluir la columna ahí si no cuesta tiempo extra, porque la estructura de medición no debe constreñir la posibilidad aunque en la práctica no ocurra.

**Abierto en la llamada, cerrado el mismo día:** si la pregunta previa se hace explícita o se omite y se deja la columna en cero. A Rubén le convencían ambas alternativas, así que la elección era de Ricardo, y también dónde vivía. Se resolvió en sesión: **una sola pregunta previa para las dos tablas**, porque es una capacidad de medición de la institución y no una propiedad de cada tabla — dos preguntas independientes abrirían el estado absurdo de una IES que mide población no binaria en poblaciones y no en autoridades. Es [[task-110]].

Estado real al momento de la reunión: la columna ya estaba pintada en el frontend, pero **el dato se perdía al guardar** — `PopulationQuantity` no tenía el campo, el payload no lo mandaba y el total no lo sumaba. El respaldo completo va en la misma [[task-110]].

## 7. Fórmula de paridad `[22:03–22:42]`

**Apertura declarada:** Rubén confirma que falta construir una fórmula para medir, en términos de paridad, qué tan cerca está la distribución por género de 50-50. Con tres columnas el problema deja de ser trivial. Ricardo matiza que la existencia del indicador no cambia la realidad del registro, solo la mide.

Es hermana de [[task-27]], [[task-28]] y [[task-29]], bajo [[task-5]]. Quedó abierta como [[task-111]] el mismo día.

## 8. Redacción de la pregunta de poblaciones `[22:42–27:36]`

**Acuerdo:** poblaciones y autoridades **siguen separadas**. Rubén lo explica bien: poblaciones mide segregación horizontal y autoridades, vertical. No se fusionan.

**Apertura en la llamada, cerrada el mismo día:** Rubén objeta la palabra «se atiende» para poblaciones. Anticipa que muchas IES dirán que no atienden a familias o proveedores, porque esa relación no es de atención sino de trabajo colaborativo, y la palabra haría que se omitan poblaciones que sí están presentes. Propone cubrir poblaciones presentes física o virtualmente y con las que se mantienen vínculos. Ricardo quedó en pensarlo y lo resolvió en sesión: el encabezado pasa a **«Está presente»**, sin signos de interrogación. Va junto con el cambio a tri-estado, en [[task-112]].

**Acuerdo:** en la leyenda de la tabla de conteo, «sexo» pasa a **«sexo y género»**. Ya es convención del repo, anotada en el `CLAUDE.md` raíz.

## 9. Orden de los bloques `[27:36–29:38]`

**Acuerdo:** **forma de gobierno va primero**, antes que estructuras. A pregunta expresa de Ricardo, Rubén responde «hasta por eso la primera». El formato pedido: nombre del tipo en negritas, seguido de su descripción.

El orden lo manda `GeneralGroup.order`, que se escribe desde el orden de la lista en `api/question/seed_data/catalogs.py`, donde hoy forma de gobierno es el quinto y último. El formato exige además partir en dos el texto del seed, que hoy es una frase completa por opción. Entra en el lote de diseño en diálogo.

## 10. «Se atiende»: de casilla a selector de tres estados `[29:38–30:41]`

**Pospuesto en la llamada, resuelto el mismo día.** Ricardo propone un selector de sí / no / vacío para distinguir «no contestado» de «no» explícito. Rubén señala el riesgo de que quien no sabe deje pasar y quede registrado como «no» cuando en realidad es «no sé». Ricardo lo acepta como parte del diseño del módulo y lo deja para después.

Tiene consecuencia de esquema: hasta ese momento la existencia de una población **era** la pertenencia al M2M `Survey.sectors`, y un M2M solo distingue presente de ausente. La decisión quedó tomada en sesión posterior y razonada en [[adr-0012]], que enmienda el punto 3 de [[adr-0008]]; la implementación es [[task-112]].

## 11. Publicación y la bandera de prueba `[31:01–34:50]`

Ricardo le explicó a Rubén el mecanismo que ya existe y que es exactamente [[adr-0009]]: cada institución tiene un campo de prueba, invisible para las propias IES, y en producción solo las instituciones marcadas así ven las secciones nuevas; hacer visible la sección a todas es cambiar una constante y toma unos tres minutos.

Aquí, en vivo, `[31:59]`, apareció un bug: **el logo institucional se exige al guardar y no debería**. Ricardo dijo que lo corrige: [[task-104]].

## 12. Catálogos editables y «no aplica» en autoridades `[35:12–39:00]`

**Propuesta de Ricardo, sin respuesta de Rubén:** habrá una sección de gestión de catálogos en el dashboard, como ya existe para buenas prácticas, donde se editen textos y preguntas de la información base. Otro turno suyo que Rubén no contestó; se registra como la dirección que él fijó, no como acuerdo. Es la raíz [[task-101]].

**Compromiso de Ricardo,** `[38:38]`, «te lo mando en cuanto cerramos»: enviarle a Rubén el documento con los textos de correcciones de redacción. Es [[task-116]].

**Decisión unilateral de Ricardo:** agregar la opción «No aplica» en las tres categorías de autoridades. La conversación exploró si alguna IES podría carecer de alguna —la persona titular existe siempre; del cuerpo colegiado en instituciones privadas y de los titulares de áreas administrativas Rubén no estaba seguro—, pero **no quedó pendiente confirmarlo**: se asume que puede faltar y se pone «No aplica» en cada fila, punto. Actualiza [[task-56]].

El supuesto sobre el que descansa esa decisión —que la validación hoy no deja guardar con campos vacíos— **no es cierto en el código**: no existe tal validación. Por eso «No aplica» necesita que primero exista la validación, [[task-106]].

## 13 y 14. Respaldos y migración de servidor `[41:00–50:17]`

Nada de esto tenía task hasta hoy; solo un roadmap declarado esqueleto en el skill `deployment`. Ahora es la raíz [[task-100]], con la reunión con Cómputo ([[task-102]]) y la decisión que la sigue ([[task-103]]) como primeras hijas.

Lo sustantivo: el servidor actual es de 2018 y está obsoleto; el trámite del nuevo lo inició Sandy y Nazul podría ayudar; mientras tanto la plataforma vive en un servidor de Yeeko con respaldo diario de la base retenido siete días. Ricardo evalúa el riesgo real: no el colapso de la base —está en AWS y es estable— sino el **borrado accidental por una persona usuaria**, único caso donde la ventana de siete días ha servido de verdad. Rubén subraya que el periodo más vulnerable es el actual, con la estructura todavía cambiando y datos reales entrando en paralelo.

**Preferencia de Ricardo, no decisión:** que sea un servidor nuevo y no el mismo que gestionó Sandra, porque serían proyectos distintos con entornos distintos aunque ambos de la CIGU — «pero preguntamos». Por eso no hay ADR: se decide después de la reunión con Cómputo UNAM.

Esa reunión la propuso Ricardo para resolver antes de arrancar el procedimiento de solicitud, qué pasa con el dominio durante la transición y la capacidad de disco. Rubén está fuera de la oficina; probablemente la gestione la próxima semana.

Pendiente adicional: en un servidor nuevo los respaldos hay que configurarlos desde cero. Ricardo tiene una idea sin resolver — sincronizarlos con su propia computadora como salvaguarda — sobre la que no ha decidido si es apropiado que ahí vivan datos institucionales.

## 15. Recordatorio automático y doble factor `[50:24–52:59]`

**Corrección de fidelidad importante: ninguna de las dos fue aprobada.** Ricardo las planteó y describió —para el doble factor, un código de seis dígitos por correo, con el doble objetivo de reducir el riesgo de contraseña adivinada y de asegurar que quien llena la información tiene acceso a esa cuenta en vez de compartir la contraseña—, pero **eso fue descripción suya, no acuerdo**.

La única respuesta de Rubén fue la del tema siguiente: en casos así, que Ricardo le diga si está cotizado o si implica pago adicional. Ambas quedan, por tanto, como **candidatas de la lista de extras, pendientes de cotización**: [[task-89]] y [[task-90]] no se cierran.

## 16. Presupuesto: distinguir lo cotizado de lo adicional `[52:59–57:01]`

**Acuerdo de proceso.** Ante cualquier ajuste nuevo, Ricardo indica si está contemplado en la cotización ya entregada a Norma o si implica costo adicional; lleva una lista de tareas fuera del alcance original, señaladas como tales, para agruparlas si hay ampliación de presupuesto; y Rubén decide caso por caso, para no generar trabajo que después no se pueda pagar.

Ricardo aclaró que ajustes como la columna no binaria o el cambio de «se atiende» no le representan mucho trabajo y los considera parte de la lógica natural de afinar el instrumento, no características extra.

Consecuencia para este sistema de documentación: hoy no hay forma de producir esa lista sin leer las tareas una por una. Haría falta una convención de frontmatter que marque el alcance presupuestal. Toca el esquema de documenter, que es global: es decisión de Ricardo y no se ejecuta aquí.

## 17 y 18. Pagos y cierre `[57:01–59:21]`

Administrativo, fuera del alcance del repositorio. Rubén se reúne con Norma —que ya tiene la cotización, revisada recién— para definir el esquema de pago, por entrega o por honorarios, y acelerar los primeros pagos.

## Lo que la reunión no tocó

De los pendientes que Ricardo llevaba quedaron intactos: el despliegue de preguntas iniciales y específicas ([[task-21]]); los pesos reales por observable ([[task-15]]); el taller de estados ([[task-26]] y su rama); y la versión actualizada del cuestionario que Rubén debía entregar ([[task-19]]).

Los textos del instrumento —el observable 4.4 y el alcance de 2.1 y 2.2, [[task-16]] y [[task-17]]— **no quedaron intactos del todo**: no se discutieron en sustancia, pero la reunión produjo el canal por el que van a resolverse, que es el documento de correcciones de redacción que Ricardo se comprometió a enviar ([[task-116]]).

Con esa salvedad, la reunión fue monográfica sobre la información base: casi todo lo que dependía de Rubén sobre el cuestionario por observable sigue igual que antes.
