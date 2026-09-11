---
type: task
id: task-150
title: Exportación del cuestionario a Word desde el dashboard
state: open
date: 2026-09-11
owner: ai
parent: "[[task-2]]"
source: ["[[2026-09-04-reunion-con-ruben]]"]
related: ["[[2026-09-04-reunion-con-ruben]]", "[[task-116]]", "[[task-50]]"]
---

# Exportación del cuestionario a Word desde el dashboard

Paso tres de los cinco que Rubén enumeró en la reunión del 4 de septiembre para publicar el cuestionario, y la pieza que cierra el principio de fuente única: si el dashboard manda sobre los textos ([[adr-0014]], [[adr-0015]]), el Word tiene que **salir** de ahí y no editarse aparte.

**El problema que resuelve.** Rubén venía editando en Word y Ricardo en la base, y eso duplica la fuente. Ricardo lo planteó al revés, `[25:55]`: «lo que yo te decía es al revés: que ya no edites nada en Word, que tú lo edites en el dashboard y agregas un botón de exportación […] y entonces el Word ya no hace formato, entonces ya no tienes que editar en dos lados, y la fuente, la única fuente, el único lugar donde está…».

**La objeción de Rubén, que es el criterio de calidad.** `[26:24]` «yo no lo digo por aquí, lo digo porque otras veces exporto cosas de plataformas y es media hora estar poniéndoles espacios». A eso Ricardo respondió con «formato a medias», `[35:01]`: «algo no crudo, crudo, que tengas que…, sino algo en lo que ya des pocas ediciones de tu parte; la parte fina, para no tardarme yo haciéndola».

**El documento que Rubén quiere producir con esto**, `[24:16]`: «hay que generar una especie de documento que se llame "Cuestionario final final", y ya con los errores que tenga, ni modo, que se quede […] Y con base en ese documento nada más me explicas cómo entrar a corregir, corrijo, y tú ya con eso publicas».

**Por qué corre prisa aunque la plataforma no esté lista.** Las IES necesitan el documento antes que la plataforma para pedir información a sus áreas una sola vez ([[task-41]]), `[23:38]`: «incluso lo necesitan antes de la plataforma […] porque tienen que pedirle la información a las áreas».

## Input obligado: el formato que hay que respetar

`docs/records/assets/vf-2025-ONIGIES-maquetado.docx` es el cuestionario con el formato que el cliente ya maquetó y entregó. **La exportación tiene que producir algo compatible con ese formato**, no un volcado con estilos propios. Es la referencia visual y estructural de esta task.

## Esto no se resuelve aquí

Cómo exportar los datos para que tengan sentido en papel —qué se agrupa, qué encabezados, cómo se rinden las tablas de criterios y las opciones, qué se omite— **es trabajo de su propia sesión**. Esta task guarda el encargo, el porqué y el formato de referencia; el diseño se hace cuando se abra.

Estimación de Ricardo en la reunión, `[26:35]`: «es algo que me va a tomar una hora, y esa hora creo que vale la pena». Léase como su expectativa, no como alcance acordado.

**Alcance ampliado que él mismo propuso** y que conviene decidir dentro de la sesión: que la descarga viva también en la parte pública, `[27:08]` «Incluso esa descarga podría estar en la plataforma también pública […] así pueden descargar el cuestionario y ya no depende de que se los pases».

## Criterios de aceptación

- [ ] Desde el dashboard se descarga el cuestionario completo en .docx
- [ ] El resultado respeta el formato de `vf-2025-ONIGIES-maquetado.docx` lo bastante para que Rubén no reformatee más de unos minutos
- [ ] Rubén produjo con ella el «Cuestionario final final» y lo mandó a las IES
