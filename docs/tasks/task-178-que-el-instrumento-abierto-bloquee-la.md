---
type: task
id: task-178
title: Que el instrumento abierto bloquee la visibilidad del cuestionario principal a las IES
state: open
date: 2026-09-25
owner: ricardo
parent: "[[task-2]]"
related: ["[[adr-0015]]", "[[adr-0018]]", "[[task-163]]", "[[task-143]]", "[[task-184]]", "[[task-187]]", "[[task-188]]"]
---

# Que el instrumento abierto bloquee la visibilidad del cuestionario principal a las IES

Idea de Ricardo la noche del deploy (2026-09-25), ante el riesgo 2 de [[task-163]]: con `QuestionnaireSettings.content_open=True` ([[adr-0015]]) Rubén puede crear o borrar observables y preguntas desde el dashboard mientras las IES ya ven y capturan; crear no reprovisiona el árbol eager y borrar arrastra en cascada las respuestas existentes (`on_delete=CASCADE` en `api/answer/models.py`). Ricardo: «Eso debería ser un bloqueante de que las IES puedan ver, pero le aviso a Rubén ahora mismo».

Mientras no exista el bloqueo, el riesgo se maneja avisando a Rubén: Ricardo dijo que le avisaría «ahora mismo» para que no toque la estructura del instrumento y avise cuando lo cierre con el interruptor (que cierra de ida y pide dump previo, [[task-143]]). No hay constancia de que el aviso se diera ni de la respuesta de Rubén: es pendiente, no acuerdo. ⚠️ Leído en producción a la 01:30 del 25: `content_open=True` con `cp_open_at` ya fijado; decidir qué se le dice a Rubén antes de la presentación.

Lectura alterna, de la crítica de cierre: «Eso debería ser un bloqueante de que las IES puedan ver» pudo querer decir una precondición antes de publicar (cerrar el instrumento primero), no un cambio de diseño en la compuerta; solo Ricardo lo aclara, y de eso depende si esta task es diseño o fue un paso omitido del deploy.

**Qué habría que decidir.** Hoy la compuerta de las IES ([[adr-0018]]) mira `Period.cp_open_at` y `gen_finished`; agregar `content_open` como tercera llave cambia el contrato: con el instrumento abierto, ¿las IES no ven nada, ven sin capturar, o ven con un aviso? ¿Aplica a las IES de prueba? ¿Y a la revisora? Alternativas menos duras que también cubren el riesgo: reprovisionar tras cada edición estructural y pasar los borrados a `PROTECT` cuando haya respuestas (opciones ya anotadas en [[task-163]]). Es un cambio de diseño y de comportamiento visible para el cliente: decisión de Ricardo, con ADR si se hace.

## Criterios de aceptación

- [x] Ricardo aclaró si su frase era precondición del deploy o cambio de diseño, y eligió entre bloquear la visibilidad por `content_open`, proteger los borrados y reprovisionar, o dejar el manejo por aviso a Rubén — 2026-09-28: «Va con PROTECT»
- [ ] ~~Si se bloquea, hay ADR y la compuerta de adr-0018 queda enmendada~~ No se bloquea: la compuerta de adr-0018 no cambia
- [x] Los borrados de observables y preguntas con respuestas quedan en `PROTECT` en `api/answer/models.py`, con su migración — hecho el 2026-09-28: ocho FKs, migración `answer 0007` (sin efecto en SQL)
- [x] Un manejador global de `ProtectedError` en DRF responde 409 en lugar de 500 cuando un borrado choca con respuestas — hecho el 2026-09-28: `api/api/exception_handler.py`, registrado en `REST_FRAMEWORK`
- [ ] Ricardo decide sobre el riesgo de las altas: reprovisionar tras cada alta estructural (observable o tipo nuevos con IES dentro). Hoy `provision_cp_responses` solo corre en `Institution.save` y como backfill; un observable o tipo creado desde el dashboard no tiene `ObservableResponse`/`GroupResponse` para las encuestas existentes. Opciones: automatizar al crear, correrlo a mano tras cada edición, o descartar
- [ ] Desplegado en producción

## Decisión de Ricardo, 2026-09-28

Al leer el panorama ([[2026-09-28-panorama-onigies]]): «Va con PROTECT». No se bloquea la visibilidad por `content_open` ni se enmienda [[adr-0018]]; el manejo por aviso a Rubén sigue para las ediciones que no borran. «Va con PROTECT» se entendió como PROTECT solo: la mitad «reprovisionar» de la opción quedó sin decidir y es el criterio abierto de arriba. La task se cierra con el deploy.

**Decisión A, alcance del PROTECT (opción 1).** `ObservableResponse` y `GroupResponse` se crean de antemano para toda IES al aprovisionar, capture o no, así que con PROTECT en `ObservableResponse.observable` y `GroupResponse.question_type` ningún observable ni tipo de pregunta se puede borrar mientras exista una IES con encuesta, y por cascada tampoco componentes ni ejes. Ricardo eligió dejarlo así: desde el dashboard ya eran inborrables por `NoDeleteMixin`, y con IES dentro lo correcto es desactivar, no borrar. Descartadas: regresar esas dos FKs a CASCADE confiando en el PROTECT de las preguntas (un observable con solo el Sí/No inicial se iría con esa respuesta), y una guarda propia que bloquee solo con valor capturado (más código).

**Decisión B, manejo del error (opción 2).** Manejador global de DRF en vez de un try/except en `confirm-delete`; cubre los ModelViewSet planos y los mixins de borrado. `IntegrityError` no se extiende al manejador (recomendación aplicada por defecto, 2026-09-28): los que quedan son bugs o carreras, y un 409 genérico los disfrazaría de error del cliente.

Hallazgo colateral: quitar un tipo de pregunta a un observable borra la fila puente y deja huérfano el `GroupResponse` de cada IES, sin que la cascada ni `PROTECT` lo toquen; preexistente, va aparte en [[task-184]].

Derivadas el mismo día: el mensaje del editor cuando el borrado se bloquea ([[task-187]]) y si buenas prácticas y los valores de eje merecen el mismo PROTECT ([[task-188]]); la limpieza de ramas y la fusión de `cp-backend`, ligada a este deploy, en [[task-186]].
