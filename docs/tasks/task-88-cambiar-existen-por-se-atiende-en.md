---
type: task
id: task-88
title: Cambiar «existen» por «se atiende» en la redacción de las preguntas
state: open
date: 2026-08-06
owner: ai
parent: "[[task-2]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-50]]", "[[task-112]]"]
---

# Cambiar «existen» por «se atiende» en la redacción de las preguntas

§6 de la reunión con Fernanda, `[12:17]`–`[13:07]`. Ricardo señaló que en una de las preguntas la palabra **«existen»** no es la mejor redacción; entre ambos surgieron alternativas: «se atiende», «es parte de», «está presente».

**Decisión de Ricardo (2026-08-06): implementar ya «Se atiende».** Anotación suya en la misma respuesta: **igual hay que corroborarlo con Rubén**, porque en la llamada él mismo lo marcó como tema metodológico. O sea: se implementa sin esperar, pero la validación sigue debiendo — si Rubén prefiere otra redacción, se cambia.

El texto vive en el seed del cuestionario (`api/question/seed_data/`, ver skill `cp-questionnaire`) y llega a la base con `load_questionnaire`. La revisión completa pregunta por pregunta que hará Rubí con su equipo es [[task-50]]; este cambio no la espera, pero es un buen ejemplo del tipo de hallazgo que ella va a producir.

## Acotación (2026-08-11)

**Esta task cubre el seed del cuestionario por observable (`cp`) y solo eso.** El encabezado equivalente de la sección de información base tiene su propio destino y no se decide aquí.

La razón es que la reunión del 11 de agosto ([[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]) partió el tema en dos. Rubén **objetó «se atiende» para la tabla de poblaciones de generales**: anticipa que muchas IES dirán que no atienden a familias o proveedores, porque esa relación no es de atención sino de trabajo colaborativo, y la palabra haría que se omitan poblaciones que sí están presentes. Propuso cubrir poblaciones presentes física o virtualmente y con las que se mantienen vínculos. Ricardo quedó en pensarlo: **la redacción de generales sigue abierta** y se está resolviendo en diálogo.

**El hilo de gen ya tiene dueño y desenlace.** La redacción se cerró el mismo 11 de agosto: el encabezado de la tabla de poblaciones pasa a **«Está presente»**, sin signos de interrogación, que es la que recoge el «presentes física o virtualmente» de Rubén. Va junto con el cambio a tri-estado del campo, en [[task-112]]. El «Se atiende» que entró al frontend con el trabajo sin commitear de ese día es, por tanto, provisional y muere ahí.

Para `cp` la corroboración de Rubén sigue debiendo: la reunión fue monográfica sobre la información base y no llegó al cuestionario por observable.

**Actualización (2026-08-12):** el hilo de gen quedó consumado — [[task-112]] entregó el encabezado «Está presente» en `943c7ac` y el «Se atiende» provisional murió del frontend (verificado: cero apariciones). Esta task queda abierta solo por su parte `cp`: el seed del cuestionario por observable y la corroboración de Rubén.

## Criterios de aceptación

- [ ] La pregunta del seed de `cp` usa «Se atiende» en lugar de «existen»
- [ ] El cambio quedó en el seed y en la base, no solo en un lado
- [ ] Rubén corroboró la redacción para `cp`, o quedó anotado que sigue pendiente
