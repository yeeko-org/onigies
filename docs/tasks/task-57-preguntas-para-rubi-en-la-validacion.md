---
type: task
id: task-57
title: Preguntas para Rubí en la validación de la sección de información base
state: open
date: 2026-08-04
owner: ricardo
parent: "[[task-41]]"
related: ["[[2026-09-04-reunion-con-ruben]]"]
---

# Preguntas para Rubí en la validación de la sección de información base

Batch de preguntas surgidas al construir la sección (sesión 2026-08-03/04). 1) Permiso de edición: el backend deja a la revisora calificar y transicionar pero no editar contenido del Survey, coherente con BP; si el equipo espera corregir datos durante la validación, hay que ampliar el permiso. 2) Los textos introductorios de los grupos los redactó la IA y uno cruza a lo metodológico: «Si no cuenta con el dato exacto, registre su mejor estimación» — invitar a estimar es decisión de medición. 3) El radio de la titular dice «Mujer / Hombre»; el resto del instrumento pregunta «según su sexo».

## Qué respondió la reunión del 11 de agosto

La reunión ([[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]) cerró dos de las cuatro preguntas y dejó las otras dos intactas.

**Evidencia probatoria: el nivel lo ratificó Rubí, el carácter lo decidió Ricardo.** Conviene no confundirlos. El **nivel** sí quedó ratificado por ella —«aplicará a todo el bloque, no por ítem», que es el anclaje que [[adr-0010]] ya tenía—. Sobre el **carácter**, lo que Rubí pidió, `[15:14]`, fue justo lo contrario de lo que se implementó: **quitar el «opcional»**, porque la evidencia sí se va a necesitar. Que no haya candado técnico es **decisión unilateral de Ricardo** ([[adr-0011]]), no algo que ella aprobara. Él la da por acordada en la reunión y decidió que no hace falta avisarle.

**Textos introductorios, resueltos por la vía estructural.** Rubén no los validó uno por uno, pero acordó algo que vuelve la pregunta menos urgente: los textos de cada bloque —título, subtítulo, instrucción y complemento— pasan a ser **editables desde el dashboard** ([[task-101]]), y él revisará los cambios de redacción antes de la publicación. La duda metodológica de fondo, la instrucción de «mejor estimación», **sigue sin responderse**: que el texto sea editable no decide si invitar a estimar es correcto.

**Sin tocar:** el permiso de edición de las revisoras y el registro de la plataforma (tuteo o usted).

Dato relacionado que sí se movió: el término «sexo» pasa a «sexo y género» en la leyenda de poblaciones, ya convención del `CLAUDE.md` raíz (desde la reunión del 2026-09-04 la convención es «sexo-género»). No es exactamente la pregunta de «Mujer/Hombre» para la persona titular, que sigue abierta.

## Acuerdos de la reunión con Rubén (2026-09-04)

**Queda respondida la pregunta que esta task daba por "sin tocar": el registro de la plataforma.** El criterio acordado es **doble, y la frontera es la superficie, no el documento**:

- **Las preguntas del cuestionario van en tercera persona.** `[56:13]` Rubén: «es que está en tercera persona la IES»; `[56:39]` Ricardo: «las del cuestionario sí tienen que estar en tercera persona».
- **Los mensajes de la plataforma van en tú**, incluidos los de estatus. `[56:39]` «yo me refiero a los mensajes de la plataforma, y sobre todo a la parte que tiene que ver con los estatus»; `[56:50]` «Está bien en "tú"»; `[56:52]` Rubén: «Todas están en "tú" y se ven re bien. Sí, ya la gente se acostumbró a usarlo así».

El ejemplo con el que se fijó el criterio fue un diálogo de confirmación: `[56:27]` «cuando eliminas: "¿Estás seguro de eliminar?"», y `[56:32]` Rubén: «Ahí sí puedes tutear».

**Procedencia del hallazgo:** no lo notó Ricardo sino el asistente, `[56:58]` «eso es algo que notó Clau […] me propusieron la redacción de "usted" y le dije "cámbialo a tú", y me dice "no, pero hay unas cosas en usted y en tú"».

Sigue sin tocarse el otro punto de esta task: el permiso de edición de las revisoras.

## Criterios de aceptación

- [ ] Rubí respondió si las revisoras necesitan corregir directamente datos de las generales (hoy: 403 deliberado)
- [ ] Rubí validó los textos introductorios de los 5 grupos, la instrucción de «mejor estimación» en poblaciones y el término «Mujer/Hombre» para la persona titular
- [ ] Rubí definió el registro de la plataforma: tutear (preferencia de Ricardo) o trato formal de usted — hoy conviven ambos (instrumento y sección gen en usted, textos del seed de flow en tú)
- [x] Rubí confirmó el **nivel** de la evidencia probatoria: por grupo de preguntas, no por ítem. Su **carácter** —que no sea obligatoria para enviar— no lo confirmó ella: es decisión unilateral de Ricardo ([[adr-0011]]), tomada después de que Rubí pidiera quitar el «opcional». Cierra [[task-68]]
