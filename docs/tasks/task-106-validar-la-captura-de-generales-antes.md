---
type: task
id: task-106
title: Validar la captura de Generales antes de guardar y enviar
state: closed
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

## Cierre (2026-08-12, sesión orquestada)

Entregada en `943c7ac` con las reglas madre dialogadas por Ricardo: **null = sin responder = bloquea; false y «No aplica» eximen; el 0 es 0** (todo valor numérico cero se captura explícito, nunca como vacío). La compuerta vive solo en la transición — guardar es libre — y cubre `gen_completed` y `gen_adjusted` (el reenvío de segunda ronda, decisión posterior de Ricardo). Doble capa tras la revisión crítica: `useGeneralValidation.js` señala por fila/campo con alerta que enumera faltantes, y `api/survey/general_validation.py` es el espejo de integridad en el servidor (400 con los mismos textos), enganchado al hook del motor de flujo sin tocarlo. Reglas por grupo en esos dos archivos; `needs_name` no exige el nombre. Los planes de estudio ganaron «No aplica» por fila vía [[task-117]] (`GeneralQuestionResponse`); las instancias no lo llevan (ahí 0 sí significa 0). Verificada con 15 escenarios sobre el código real, sonda HTTP y smoke en navegador.

## Criterios de aceptación

- [x] Un grupo con campos vacíos no puede marcarse como completado
- [x] La interfaz señala qué falta, no solo que falta
- [x] «No aplica» en una fila de autoridades hace pasar la validación de esa fila
