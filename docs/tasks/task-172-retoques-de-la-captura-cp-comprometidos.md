---
type: task
id: task-172
title: Retoques de la captura cp comprometidos con Rubén el 23 de septiembre
state: open
date: 2026-09-23
owner: ai
parent: "[[task-2]]"
source: ["[[2026-09-23-reunion-ruben]]"]
related: ["[[task-21]]", "[[2026-09-25-deploy-del-cuestionario-principal-y-documento-para-ruben]]"]
---

# Retoques de la captura cp comprometidos con Rubén el 23 de septiembre

Los ajustes visuales de la captura cp que Ricardo dijo en voz alta, mientras se la mostraba a Rubén el 23 de septiembre ([[2026-09-23-reunion-ruben]]). Son de interfaz, sin decisión metodológica detrás.

**Precedencia (Ricardo, 23 de septiembre: «Lo que dije en la reunión es lo más actual»):** donde lo dicho en la reunión contradiga lo que decidió la sesión paralela de la captura cp, manda la reunión. La tensión con «Drop shadows» de la limpieza de estilos de [[task-170]] quedó resuelta: la sesión de diseño cp ya aplicó la sombra a las tarjetas de grupo.

## Reunión con Rubén, 2026-09-23

1. **«Ver preguntas» a la derecha.** Ricardo, `[15:01]`: «lo ideal es que este botón esté aquí a la derecha; estaba haciendo ajustes pequeñitos al respecto. Entonces el "ver preguntas" se pone así, y ya te saca todas las preguntas, por bloque… ay, qué horror, enorme. Así quedó».
2. **Tarjetas de grupo con sombra.** Ricardo, `[16:38]`: «Le voy a poner como una carta, con sombrita, para que se distingan».
3. **«Eje …» en el título.** Ricardo, `[22:01]`: «Aquí le voy a poner "Eje Cuidados", para que sea claro que es un eje: Eje Igualdad de género, Eje Inclusión, Eje No violencia».
4. **La palabra «Nota» visible.** Ricardo, `[25:46]`: «aquí está la nota; le puedo poner la palabra "Nota" para que sea muy claro».
5. **Paréntesis redundante en una etiqueta.** Ricardo, `[27:54]`: «Creo que puedo quitar esta cosa entre paréntesis, porque ya está dentro de la propia etiqueta». Lo dijo mostrando la pregunta especial (`[26:43]`, «Hay otro tipo de pregunta, la especial, que es esta»); la reunión no nombra la etiqueta.
6. **Tamaño del eje Cuidados.** Ricardo, `[20:13]`: «Algo que no me encanta, y te pregunto qué opinas: cuidados queda muy chiquito, porque solo son 4 observables; igualdad son 17 y no violencia 14; esos son los extremos. Se ve raro que esté chiquito, pero tampoco es problema». Rubén, `[21:53]`: «Y así se ve un poco el avance de los derechos: se nota cuáles se han sofisticado más. Está muy bien». Rubén lo leyó como información, no como defecto: el punto es decidir si se toca.

## Criterios de aceptación

- [ ] El botón «Ver preguntas» está a la derecha — probablemente ya hecho: en HEAD, `CpObservablePanel.vue` tiene `<v-spacer />` antes del botón, y Ricardo en `[15:01]`: «Justo ahorita lo estoy acomodando… Así quedó»; verificar en navegador antes de marcar
- [x] Las tarjetas de grupo llevan sombra — lo aplicó la sesión de diseño cp el 2026-09-23 (`CpGroupCard.vue`, `elevation="2"`, commit c7816fd)
- [x] Los títulos de eje dicen «Eje …» — «Eje N. Nombre» con el `order` del eje (Ricardo, 2026-09-25: «Poner "Eje {N}. {Axis.name}"»), en `CpAxisCapture.vue`, commit `d290636`; como el componente es compartido, la revisora también ve «Eje N.» en el dashboard
- [x] Las notas del observable llevan la palabra «Nota» — «Nota:» en negrita junto al ícono de info, `CpObservablePanel.vue`, commit `d290636`. ⚠️ ligero: el «Sí de una vez» de Ricardo respondió a una pregunta que decía *quitar* «Eje» y «Nota» (brief invertido del coordinador); «Eje» quedó confirmado después por su «Eje {N}. {Axis.name}», «Nota:» no volvió a confirmarse; confirmar que se queda
- [ ] El paréntesis redundante de la etiqueta de la pregunta especial se quitó
- [ ] El tamaño del eje Cuidados se ajustó o se dejó con la razón escrita
