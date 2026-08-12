---
type: decision
id: adr-0011
title: "La evidencia probatoria no es obligatoria para enviar: la revisión retacha"
state: accepted
date: 2026-08-11
origin: ricardo
deliberation: unilateral
rationale: recorded
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
affects: ["nuxt/app/components/dashboard/survey/GeneralGroupPanel.vue"]
related: ["[[task-68]]", "[[adr-0010]]"]
---

# La evidencia probatoria no es obligatoria para enviar: la revisión retacha

## Contexto y planteamiento del problema

En la reunión del 11 de agosto, `[15:11]`, Rubén pidió quitar la opcionalidad de la evidencia probatoria porque sí se va a necesitar, «sobre todo en el organigrama; en el resto de los bloques quizás no». Ricardo quitó el rótulo «(opcional)» en el momento.

Quedaba abierto si eso debía convertirse en una obligatoriedad técnica: bloquear el envío del grupo o del paquete cuando falta el adjunto. [[task-68]] había dejado ese requisito **explícitamente fuera de su alcance**, con la nota de que la obligatoriedad es un requisito distinto de la capacidad de adjuntar y de que, si se confirmaba con Rubén, se abriría task propia. La reunión lo confirmó como expectativa, y esta decisión resuelve qué hacer con ella.

## Opciones consideradas

- **Bloquear el envío sin evidencia.** Garantiza que la revisión nunca reciba un bloque sin comprobante. Si además la obligatoriedad fuera por bloque —como sugiere el «sobre todo en el organigrama» de Rubén—, exige un campo nuevo en el catálogo de grupos, con su migración y su seed.
- **No bloquear:** comunicar la expectativa en la interfaz y dejar que la falta se resuelva en la revisión.

## Resultado

No se bloquea. Ricardo lo considera **burocracia innecesaria**: si a la revisión le falta evidencia para dictaminar, el camino correcto es retachar el envío dentro del proceso de revisión —que es exactamente lo que el motor ya sabe hacer con el estatus de ajustes requeridos— y no un candado que impida a la IES entregar lo que sí tiene.

El argumento tiene respaldo empírico de la misma reunión: el equipo de Rubén ya estrenó en buenas prácticas un **cotejo previo** —verificar que existan los documentos probatorios, antes de revisar calidad— precisamente porque descubrieron que hacía falta. Ese trabajo ya existe y ya lo hacen personas; duplicarlo como candado automático no agrega garantía, solo fricción.

### Consecuencias

- **Bueno:** la interfaz comunica la expectativa sin imponerla — el rótulo dice «Evidencia probatoria», sin «(opcional)».
- **Bueno:** no hace falta campo nuevo en el catálogo de grupos ni migración, que es lo que habría exigido la obligatoriedad por bloque.
- **Bueno:** la detección de la falta se queda donde ya vivía y donde hay criterio para juzgarla; una regla automática no sabe distinguir un organigrama faltante de uno que la IES publica en su portal.
- **Malo, y aceptado:** una IES puede enviar sin evidencia y consumir un ciclo de revisión completo para que se la pidan.
- Cierra [[task-68]], cuyo único criterio pendiente era la confirmación del nivel y del carácter del adjunto.

## Cómo se comprueba

Un grupo de generales sin ningún adjunto transiciona a enviado sin error.

## Más información

El **nivel** del adjunto —por bloque de preguntas, nunca por ítem ni por observable— quedó ratificado por Rubén en la misma reunión y está fijado en [[adr-0010]]. Esta decisión solo resuelve el carácter obligatorio, no el nivel.
