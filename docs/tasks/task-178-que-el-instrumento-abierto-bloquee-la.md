---
type: task
id: task-178
title: Que el instrumento abierto bloquee la visibilidad del cuestionario principal a las IES
state: open
date: 2026-09-25
owner: ricardo
parent: "[[task-2]]"
related: ["[[adr-0015]]", "[[adr-0018]]", "[[task-163]]", "[[task-143]]"]
---

# Que el instrumento abierto bloquee la visibilidad del cuestionario principal a las IES

Idea de Ricardo la noche del deploy (2026-09-25), ante el riesgo 2 de [[task-163]]: con `QuestionnaireSettings.content_open=True` ([[adr-0015]]) Rubén puede crear o borrar observables y preguntas desde el dashboard mientras las IES ya ven y capturan; crear no reprovisiona el árbol eager y borrar arrastra en cascada las respuestas existentes (`on_delete=CASCADE` en `api/answer/models.py`). Ricardo: «Eso debería ser un bloqueante de que las IES puedan ver, pero le aviso a Rubén ahora mismo».

Mientras no exista el bloqueo, el riesgo se maneja avisando a Rubén: Ricardo dijo que le avisaría «ahora mismo» para que no toque la estructura del instrumento y avise cuando lo cierre con el interruptor (que cierra de ida y pide dump previo, [[task-143]]). No hay constancia de que el aviso se diera ni de la respuesta de Rubén: es pendiente, no acuerdo. ⚠️ Leído en producción a la 01:30 del 25: `content_open=True` con `cp_open_at` ya fijado; decidir qué se le dice a Rubén antes de la presentación.

Lectura alterna, de la crítica de cierre: «Eso debería ser un bloqueante de que las IES puedan ver» pudo querer decir una precondición antes de publicar (cerrar el instrumento primero), no un cambio de diseño en la compuerta; solo Ricardo lo aclara, y de eso depende si esta task es diseño o fue un paso omitido del deploy.

**Qué habría que decidir.** Hoy la compuerta de las IES ([[adr-0018]]) mira `Period.cp_open_at` y `gen_finished`; agregar `content_open` como tercera llave cambia el contrato: con el instrumento abierto, ¿las IES no ven nada, ven sin capturar, o ven con un aviso? ¿Aplica a las IES de prueba? ¿Y a la revisora? Alternativas menos duras que también cubren el riesgo: reprovisionar tras cada edición estructural y pasar los borrados a `PROTECT` cuando haya respuestas (opciones ya anotadas en [[task-163]]). Es un cambio de diseño y de comportamiento visible para el cliente: decisión de Ricardo, con ADR si se hace.

## Criterios de aceptación

- [ ] Ricardo aclaró si su frase era precondición del deploy o cambio de diseño, y eligió entre bloquear la visibilidad por `content_open`, proteger los borrados y reprovisionar, o dejar el manejo por aviso a Rubén
- [ ] Si se bloquea, hay ADR y la compuerta de adr-0018 queda enmendada
