---
type: task
id: task-50
title: Revisión humana del cuestionario pregunta por pregunta
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]", "[[2026-07-03-dudas-del-instrumento-con-el-cliente]]", "[[2026-07-03-reduccion-del-cuestionario]]"]
depends-on: ["[[task-42]]"]
---

# Revisión humana del cuestionario pregunta por pregunta

Acuerdo de la reunión: el instrumento sembrado nunca lo ha leído completo una persona con la versión final del cuestionario en la cabeza, y eso tiene que pasar antes de abrir el cuestionario a las IES. `[33:11]` «no estaría mal hacer una validación humana como de leer pregunta por pregunta para asegurarse que neta todo tenga congruencia. Eso sí tiene que pasar por un humano consciente con la versión final y que tenga muy presente cómo es el cuestionario real, para que pueda identificar cualquier cosa que se escape».

Quien la ejecuta es Rubí con su grupo de trabajo, no Ricardo. `[37:37]` «nosotras acá con mi grupo de trabajo haríamos la revisión de todos esos errores humanos que pueda... A ver, me pones un ejemplo para corregirlo y tú nos explicas cómo corregirlo nosotras mismas». Por eso la task queda con `owner: ricardo`: lo que él debe es habilitarla, no ejecutarla.

Dos partes:

1. **Enseñarle a Rubí a corregir los textos ella misma** desde el dashboard, sobre la base de producción. Depende de [[task-42]], que es la superficie donde se editan las preguntas.
2. **Acompañar la revisión** y resolver lo que ella detecte.

Se trabaja sobre la base real, no sobre un documento suelto — decisión explícita de la reunión, por trazabilidad: `[36:41]` «Mejor el lunes. El lunes para que ya se haga directo sobre la base final, o sea, porque si te la mando yo voy a tener que meterme al script y no sé qué, y se va a perder, como que es más difícil trazabilidad. Y ya si lo hacemos con la base real real pues no va a haber problema, no se va a volar».

Esta task absorbe los hallazgos previos detectados con asistencia de IA sobre los textos del instrumento (`[33:11]` «he encontrado typos... lo hice asistido con la IA y se dio cuenta de algunas cositas muy simples»):

- El documento que se leyó en pantalla durante la reunión es [[2026-07-03-dudas-del-instrumento-con-el-cliente]]. Su §1 ya es [[task-16]] y su §2 es [[task-17]]; **su §3, «Otras dudas detectadas en el documento original», no tiene task propia y entra aquí**.
- Las erratas ortográficas y las discrepancias de título de [[2026-07-03-reduccion-del-cuestionario]] (§2 y §3) figuran como resueltas el 2026-07-03; conviene confirmarlo contra la base sembrada durante esta revisión.

## Criterios de aceptación

- [ ] Rubí sabe corregir los textos de las preguntas desde el dashboard sin intermediación
- [ ] Se recorrió el instrumento completo pregunta por pregunta
- [ ] La §3 de [[2026-07-03-dudas-del-instrumento-con-el-cliente]] está resuelta o descartada
- [ ] Los hallazgos quedaron corregidos en la base de producción
