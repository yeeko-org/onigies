---
type: decision
id: adr-0012
title: La existencia de una población se captura como tri-estado en PopulationQuantity
state: accepted
date: 2026-08-11
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
affects: ["api/survey/models.py", "nuxt/app/composables/useGeneralSurvey.js"]
related: ["[[adr-0008]]", "[[task-56]]", "[[task-112]]"]
---

# La existencia de una población se captura como tri-estado en PopulationQuantity

## Contexto y planteamiento del problema

[[adr-0008]] fijó que la existencia de una población vive en el M2M `Survey.sectors`, y que solo persisten filas de `PopulationQuantity` con algún conteo: una fila sin hombres ni mujeres no aportaba nada y la sincronización por omisión la borraba. Funcionó mientras la respuesta fuera binaria.

En la reunión del 11 de agosto, `[29:38]`–`[30:41]`, Ricardo planteó el problema: con una casilla no se puede saber si la persona la dejó sin tocar o si de verdad contestó que no. Rubén señaló el riesgo inverso —quien no sabe la respuesta la deja pasar y queda registrada como «no» cuando en realidad es «no sé»— y Ricardo lo aceptó como parte del diseño del módulo. En la llamada quedó pospuesto; se resolvió el mismo día en diálogo posterior.

La distinción no es cosmética: para el observable 1.7, «cero», «sin dato» y «no existe» son tres cosas distintas en los denominadores. Es la misma preocupación que abrió [[task-56]].

## Opciones consideradas

- **Dejarlo en el M2M.** Cero costo, pero «no contestado» y «no» siguen siendo indistinguibles.
- **Reusar el `no_apply` que `PopulationQuantity` ya trae.** No cuesta migración, pero ese campo tiene otra semántica —el opt-out de excepción rara que [[task-56]] destina a las autoridades— y mezclarlos dejaría dos significados en una sola columna.
- **Columna propia de tres estados.**

## Resultado

Columna propia: `PopulationQuantity.is_present`, booleano que admite nulo. Verdadero es «está presente», falso es un «no» explícito, y nulo es la fila que nadie tocó. **La fila se persiste en cuanto hay respuesta, sí o no, aunque no lleve ningún conteo.**

`Survey.sectors` deja de ser el lugar donde vive la existencia y pasa a ser **derivado**: una propiedad calculada sobre las filas con `is_present` verdadero. Se conserva porque hay código que lo consume, no porque siga siendo la fuente de verdad.

## Enmienda a adr-0008

Esta decisión **modifica el punto 3 de [[adr-0008]]** y la premisa de su punto 4. Sus puntos 1 y 2 —que el contenido se escribe siempre contra el Survey, y que las cantidades de población tienen semántica de sincronización total— quedan intactos y siguen gobernando.

**No se marca adr-0008 como reemplazada**, porque no lo está: cambia uno de sus cuatro puntos, y retirarla entera dejaría sin autoridad escrita las dos reglas que sí siguen vigentes y que el skill `gen-general-info` cita. La enmienda queda anotada también en el cuerpo de adr-0008, para que nadie lo lea sin ella.

### Consecuencias

- **Bueno:** «no contestado» y «no» dejan de confundirse, que era el problema que abrió esto.
- **Bueno:** la lectura de composición deja de exigir cruzar dos fuentes. Ya no hay que cruzar el M2M con las cantidades: la respuesta y el conteo viven en la misma fila.
- **Malo:** hay que barrer los usos de `Survey.sectors` en tres lugares —el serializer de generales, el composable del frontend y el cálculo del observable 1.7—, y cualquiera que quede sin migrar leerá un M2M que ya no se escribe.
- **Malo, y lo señaló Rubén:** un «no» sigue sin distinguirse de un «no sé». Esta decisión resuelve el primer nivel de ambigüedad, no el segundo.
- El riesgo de que proliferen filas vacías es real pero acotado: son doce poblaciones por survey.

## Cómo se comprueba

Una fila marcada «No» y sin ningún conteo sobrevive a un guardado y vuelve como «No» al recargar.

## Más información

La implementación es [[task-112]]. La primera pregunta de [[task-56]] —si «existe pero sin dato» debe ser capturable, distinto de no marcar el sector— queda absorbida por este tri-estado en lo que toca a poblaciones.
