---
type: record
id: 2026-08-11-cierre-de-sesion-duo-reunion-auditorias-y-reorganizacion
title: "Cierre de sesión duo del 11 de agosto: reunión con Rubén, tres auditorías y reorganización del grafo"
date: 2026-08-11
related: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]", "[[2026-08-11-auditoria-del-arbol-de-trabajo-y-reorganizacion]]"]
---

# Cierre de sesión duo del 11 de agosto: reunión con Rubén, tres auditorías y reorganización del grafo

Sesión duo del 11 de agosto de 2026, corrida hasta la madrugada. Empezó con una reunión de 59 minutos con Rubén y terminó con el sistema de tareas reorganizado de arriba abajo y el diseño de la sección de información base cerrado.

## Qué produjo la sesión

**La reunión, transcrita y organizada.** El audio se transcribió y se agrupó por tema; ese material vive en el repositorio written.django. El acta con valor para este proyecto es [[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]].

**Una auditoría de fidelidad, y lo que destapó.** Al contrastar la versión organizada contra el raw aparecieron **lecturas infladas**: cosas que la organización presentaba como acuerdos y que en el audio son turnos de Ricardo sin respuesta de Rubén, descripciones suyas, autocríticas o preferencias condicionadas. El teléfono descompuesto no venía de la transcripción sino de la capa que la ordenó.

El caso más claro es el doble factor. La organización lo listaba como pendiente acordado, con mecanismo y todo. En el raw, el mecanismo —código de seis dígitos por correo— es **descripción de Ricardo**, y la única respuesta de Rubén fue la del acuerdo de presupuesto que vino después: que le diga si está cotizado o si implica pago adicional. Por eso [[task-89]] y [[task-90]] **no se cerraron como respondidas**: pasaron a candidatas de la lista de extras, pendientes de cotización.

Otros dos del mismo tipo: el servidor nuevo de la UNAM, que la organización daba por decidido y que en el raw es preferencia de Ricardo con un «pero preguntamos» pegado —de ahí que [[task-103]] sea una task de decisión y no un ADR—; y un referente inventado en el hilo de «se atiende». La transcripción organizada quedó marcada con una advertencia que remite al acta corregida.

De ahí sale la disciplina que el acta adopta y que conviene conservar: **separar siempre acuerdos, decisiones de Ricardo y aperturas**, porque las tres se leen igual en una transcripción y significan cosas muy distintas seis semanas después.

**Una auditoría del trabajo manual sin commitear de Ricardo**, contrastado contra las tareas abiertas: qué cubría por completo, qué a medias y qué no tenía task. Está en [[2026-08-11-auditoria-del-arbol-de-trabajo-y-reorganizacion]], junto con dos reversiones suyas que se registraron **como decisiones deliberadas, no como regresiones**.

**La reorganización completa del grafo.** Había 33 tareas abiertas sin madre. Se abrieron cuatro raíces —[[task-98]] flujo y UX, [[task-99]] comentarios, [[task-100]] migración a la UNAM y [[task-101]] catálogos editables—, se repartieron las huérfanas entre esas y las raíces existentes, y [[task-84]] pasó a ser madre de [[task-82]] y [[task-83]]. Quedaron cinco sueltas a propósito.

**El lote de diseño de la sección**, cerrado en diálogo la misma jornada: de [[task-107]] a [[task-115]], más [[adr-0011]] (la evidencia probatoria no es obligatoria) y [[adr-0012]] (la existencia de una población pasa a tri-estado), que **enmienda el punto 3 de [[adr-0008]]** sin reemplazarlo — el esquema no modela supersede parcial, así que la enmienda quedó escrita en los dos documentos.

**Un barrido crítico final**, del que salieron ocho correcciones aplicadas en el último lote: los cuatro pendientes del acta que habían cerrado el mismo día y seguían escritos como abiertos; dos «acuerdos» que eran turnos sin respuesta; la autoría de la prueba adicional del equipo; el cierre del acta que daba [[task-16]] y [[task-17]] por intactas cuando la reunión sí produjo el canal para resolverlas ([[task-116]]); el criterio de [[task-57]] que atribuía a Rubí una decisión que es de Ricardo; el nombre del campo, de `is_attended` a `is_present`, para no perpetuar la palabra que Rubén objetó; las secuencias que faltaban entre tareas; y la advertencia en la transcripción de origen.

## Decisiones de proceso

Dos, ambas de alcance general y por tanto registradas en el repositorio global, no aquí:

- **Los cambios manuales directos de Ricardo sobre el código valen como decisión final.** Cuando él toca el árbol de trabajo con criterio propio, eso no se audita como desviación ni se propone revertirlo: se documenta como veredicto. Es lo que ordenó tratar sus dos reversiones —el ancho de celda de [[task-66]] y la disposición de la pregunta de [[task-93]]— como decisiones y no como errores.
- **Sin pre-conclusiones mientras haya ejecutores en curso.** No se presenta ni se decide sobre trabajo delegado hasta que vuelve completo.

## Agrupación de sesiones acordada

El trabajo pendiente se repartió en tres sesiones, ordenadas por la ventana de apertura de la sección:

**Sesión A — que la captura sea correcta.** Ventana miércoles a jueves, antes de que la sección se haga visible: [[task-110]] (columna no binaria con su respaldo y su pregunta previa), [[task-112]] («Está presente» y el tri-estado), [[task-106]] (validación de campos vacíos, que depende de la anterior), [[task-104]] (el logo al guardar) y los criterios exprés de [[task-96]].

**Sesión B — que el equipo de Rubén pueda editar.** [[task-107]], [[task-108]] y [[task-113]] **en el mismo lote y el mismo commit**: el modelo nuevo rompe el contrato que consume el frontend, así que separarlas deja la sección rota entre una y otra.

**Sesión C — después del viernes.** [[task-114]] (diseño visual de la evidencia), [[task-62]] (lenguaje «De prueba»), [[task-105]] (el colapso de panels), [[task-115]] (DEBUG y CORS, deliberadamente después del jueves) y el arranque de [[task-98]].

**En paralelo, por cuenta de Ricardo:** [[task-102]] (la reunión con Cómputo UNAM), [[task-111]] (la fórmula de paridad) y el bloque de definiciones metodológicas de [[task-5]].
