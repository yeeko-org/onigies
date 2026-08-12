---
type: task
id: task-106
title: Validar la captura de Generales antes de guardar y enviar
state: open
date: 2026-08-11
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
depends-on: ["[[task-112]]"]
---

# Validar la captura de Generales antes de guardar y enviar

Intención de Ricardo que hasta hoy no existe en el código: la captura de la información base **no valida campos vacíos**, ni al guardar ni al enviar. La función que persiste, en `nuxt/app/components/dashboard/survey/GeneralGroupList.vue`, hace el PATCH directo sin reglas; el constructor del payload en `nuxt/app/composables/useGeneralSurvey.js` simplemente omite las filas sin conteo; y ninguno de los cuatro componentes de grupo monta un formulario con reglas. La única compuerta es la del motor —la lista de estatus válidos de los hijos bloquea el envío hasta que los cinco grupos estén completados—, y esa mira estatus, no contenido.

Urgente por dos razones. La primera es la ventana: la sección se abre a las IES esta semana, con la sección visible el jueves 13 y el anuncio el viernes 14.

La segunda es que esta validación es **el supuesto sobre el que descansa el «No aplica» de autoridades** decidido el 11 de agosto ([[task-56]]). Ricardo se lo explicó a Rubén como «para que se pueda marcar y así pasar la validación, que hoy no permite guardar con campos vacíos». Sin la validación, «No aplica» no desbloquea nada, porque nada estaba bloqueado.

## Criterios de aceptación

- [ ] Un grupo con campos vacíos no puede marcarse como completado
- [ ] La interfaz señala qué falta, no solo que falta
- [ ] «No aplica» en una fila de autoridades hace pasar la validación de esa fila
