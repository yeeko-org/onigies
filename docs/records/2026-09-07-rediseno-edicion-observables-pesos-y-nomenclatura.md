---
type: record
id: 2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura
date: 2026-09-07
related: ["[[2026-09-04-prototipo-edicion-cuestionario-deploy-e-incidente-netlify]]", "[[2026-09-07-cotejo-del-instrumento-maquetado]]", "[[task-42]]", "[[task-15]]"]
---

# Rediseño de la edición de observables: ponderación por modelo intermedio, nomenclatura de los tipos de pregunta y headers de la jerarquía

Sesión duo del lunes 7 de septiembre de 2026, sobre la rama `edicion-cuestionario-v2`, sin commit al cierre de este record (secuencia acordada el 8 de septiembre: `critic` → dos commits, código y documental → revisión del diff en PyCharm al abrir la fase 3, [[task-131]]). Arrancó con un prompt largo de Ricardo que planteaba tres definiciones de dominio y una lista de cambios de interfaz; se acordó atenderlo en fases y las fases 3 y 4 quedaron como tareas ([[task-131]], [[task-132]]).

## Lo que produjo la sesión

**Fase 1, modelo y seeds.** Nace `ObservableQuestionType` en la app `question`: una fila por (observable, tipo de pregunta) con `weight` nullable; el peso efectivo es el de la fila o, si es nulo, el `default_weight` del tipo. `Observable` perdió las seis columnas `*_weight`, `reach_instances_question`, `get_default_weight` y los `final_*_weight`; gana `weight_for(type_name)`. `QuestionType` perdió `weight_name` y el M2M `observables` (se declaró y se retiró en la misma sesión: las dos FK del modelo intermedio bastan), y ganó `order` y `required`. Cinco migraciones (`question` 0005–0008, `indicator` 0010); la de datos creó las 120 filas puente (41 A, 41 B, 35 sectorial, 1 planes, 1 especial, 1 población en el 1.7) y escribió los nombres nuevos de los tipos. `load_questionnaire` escribe textos solo al crear (`create_defaults`) y sincroniza las filas puente sin tocar pesos; el flag `--overwrite-texts` restaura el pisado para el resembrado único del siguiente deploy y nunca toca Eje ni Componente. `migrate_initial_data` siembra `public_name` y `default_weight` solo al crear. Los 40 subtítulos del bloque A («Mencione/Marque todas las características o elementos que resulten aplicables[ a este instrumento]:») pasaron de coletilla entre paréntesis dentro de `a_main_question` a llave explícita `a_main_subtitle` en `seed_data`, con las tres redacciones intactas y 2.1 sin subtítulo, como en el instrumento. `QuestionType` es catálogo editable con guardas y entrada de menú «Tipos de pregunta»; `ObservableQuestionType` es catálogo con solo `weight` escribible. Tests: 94 → 103 (tres bloques nuevos, todos con prueba de que muerden). Respaldo previo de la base local en `~/databases/onigies-local-2026-09-07-pre-through-model.dump`.

**Fase 2, headers y sheets.** `AxisHeader` y `AxisSheet` nuevos (componentes desde el árbol en memoria, porque los ejes no piden detalle al servidor; observables solo contados); `ComponentSheet` nuevo (observables anidados del detalle); ambos sin buenas prácticas. `ObservableHeader`: ícono del eje, leyenda del componente encima del título, título en `TitleCommon` a 520 px y fila de 78 px, y en `#details` un `HeaderChip` por tipo de pregunta que aplica al observable (orden del catálogo): armonización e institucionalización cuenta preguntas, sectorial cuenta sectores (10 principales más los propios), orgánica muestra los íconos de instancias académicas y administrativas que aplican, planes cuenta preguntas, especial solo ícono, población palomita verde con tooltip «se captura en Información de base». Íconos y colores viven en las clases Schema (`indigo` para los tres comunes, `deep-purple` para los tres especiales). `count_fields` en `ObservableSchema` con una constante compartida con el detalle del componente. `QuestionType`: `name_field = "public_name"` (override nuevo en la clase base de los schemas), `QuestionTypeEditSimple` con los campos estructurales en `readonly` (no chips), `QuestionTypeHeader` con el conteo de observables donde aplica, y `QuestionTypeSheet` vacío. Regla genérica: la llave primaria nunca se pinta editable (`EditCommonFields`).

**`TitleCommon`.** Ricardo veía los títulos en una sola línea recortada; las capturas de los ejecutores mostraban dos. Causa: Vuetify pone `white-space: nowrap` en el título y `TitleCommon` lo contrarrestaba solo con `text-wrap: pretty`, que Firefox ignora. Se agregó `white-space: normal`; el recorte a dos líneas (54 px) queda como estaba. El bug nació en ocsa en octubre de 2024 y onigies lo heredó en el port de marzo de 2026; la misma línea se aplicó hoy en `~/dev/ibero/ocsa` sin commitear ([[task-136]]).

## Hallazgos

- El nombre de cada tipo de pregunta vivía en cuatro lugares que divergían: `QuestionType.public_name` (que nadie leía), `verbose_name` del modelo, `name` del `CatalogSchema` y etiquetas fijas en Nuxt. `b_weight` tenía un quinto («Ponderación cumplimiento»). Ahora `public_name` es la fuente y el frontend lo lee de `cats.question_type`.
- El seed de `QuestionType` pisaba `public_name` y `default_weight` en cada `migrate_initial_data` (no en cada arranque, como se creyó al principio: el comando no está en el runbook de deploy).
- De los seis `final_*_weight` solo uno era `@property`; `weight_name` no era único y el fallback hacía `.get()` sobre él. Ambos desaparecieron con el modelo intermedio.
- El observable 1.12 (planes de estudio) es el único sin pregunta de transversalidad orgánica pese a que el tipo es requerido; se ve como triángulo de advertencia en su renglón y va a la reunión del 11 ([[task-135]]).
- `load_questionnaire` borra opciones y planes sobrantes con CASCADE a `AResponse`/`PlanResponse` sin dry-run ([[task-133]]); `load_sectors` busca por `name`, editable y no único ([[task-134]]).
- El instrumento original ya traía la distinción «contenido armonizado e institucionalizado» como rótulo del bloque A en los 41 observables; el seed la descartó. La clasificación a mano de las 280 opciones de sí/no (123 armonización, 143 institucionalización, 13 dudosas, 1 texto libre; 12 observables 100 % armonización y 9 100 % institucionalización) se hizo y se descartó por decisión de no separar; la tabla completa (280 filas, dudosas con recomendación y la banda «ARM-mandato» pendiente de criterio) está en [[2026-09-07-clasificacion-armonizacion-institucionalizacion]].
- `a_main_subtitle` existía desde la migración inicial, nunca se llenó y sí era editable: estaba pensado exactamente para la instrucción del bloque A.

## Decisiones

Las de esquema y nomenclatura están en [[adr-0014]]. Las de sesión que no ameritan ADR: `order` de observables y preguntas no editable (clave natural del seed); la validación «si hay un tipo no requerido, todos los pesos no nulos» es aviso, no bloqueo; el Sheet de observable deja de ser automático en la fase 3; el nombre del componente va como leyenda encima del título del observable; el detalle visual de altura entre chips no importa.

## Conversación de WhatsApp con Rubén (7 de septiembre de 2026)

Fuente de la nomenclatura y de la ponderación tentativa. Textual:

> Ricardo: Hola rubén!
> Rubén: Hola, Ricardo
> Rubén: Qué tal
> Ricardo: oye... una pregunta rápida: Las preguntas que son de Sí/No dentro de cada observable, son de "institucionalización" o "armonización"?
> Rubén: Son de armonización
> Rubén: Pero están mezcladas con institucionalización
> Rubén: Es algo como armonización institucionalizada
> Ricardo: Ooooh, entiendo! Son una u otra, pero al grupo de eso junto hay que ponerle los dos nombres?
> Rubén: Creo que no entendí la pregunta, jeje
> Ricardo: cómo le llamamos a ese tipo de preguntas? (que incluyen de transversalización y de armonización)
> Ricardo: Le ponemos "Preguntas de institucionalización y armonización"?
> Rubén: ahh sí, perfecto
> Rubén: está bien así
> Ricardo: Tengo otra pregunta: La pregunta de "alcance" (los sectores que se consideran o a los que se impactan) es una pregunta dentro del grupo de "transversalización" (que tiene las instancias académicas y administrativas)?
> Ricardo: O son grupos separados?
> Rubén: sip
> Rubén: es transversalidad
> Rubén: en este caso sectorial
> Rubén: la transversalidad de instancias es transversalidad orgánica
> Ricardo: Oye, y cuánto suma cada uno? Cada uno tiene su propio peso o "ponderador" o cómo funciona eso?
> Rubén: para las estructuras sería como antes
> Rubén: del total, cuántas aplican X política
> Rubén: de sectores sería: si declaró que es una población existente, aplica o no aplica la política a este grupo?
> Ricardo: ajá, pero lo de "sectorial" cómo suma o resta al indicador?
> Ricardo: o sea, qué pasa si tengo el 60% de instancias que sí cumplen, pero tengo el 100% de los sectores considerados?
> Ricardo: O qué pasa si tengo el 60% de instancias que sí cumplen, pero solo el 20% de los sectores considerados?
> Ricardo: Cómo cambia o impacta cada parte al valor de la IES en "transversalización" de cada observable?
> Rubén: creo que podemos seguir con la lógica de promediar
> Rubén: promediar sectorial con orgnánico
> Ricardo: mmmh
> Ricardo: no sé, no me agrada
> Ricardo: perooo
> Ricardo: tengo una solución
> Rubén: te parece si lo pensamos?
> Ricardo: a ver qué te parece: tengo los pesos separados, si vemos que ambos valgan lo mismo, la solución es simple
> Ricardo: o sea, ponle que acordemos que "transversalización" quede con 5/10 puntos (el peso), pues cada subgrupo tendría 2.5
> Ricardo: y listo!
> Ricardo: así no tenemos que resolverlo ahora y la plataforma queda lista para cualquier decisión
> Rubén: tú dices que institucionalización y armonización valga 5 y transversalidad sectorial 2.5 y tansversalidad orgnánica 2.5?
> Ricardo: o sea, si decidimos que valgan la mitad cada uno
> Rubén: yap, creo que son buenas ideas
> Ricardo: pero bueno, es parte de las decisiones metodológicas que por ahora dejaría tentativas ahora
> Rubén: quizás sólo podamos darnos un rato para analizar sus implicaciones
> Rubén: lo tienes que programar ya ahora?
> Ricardo: Si después decimos 3 y 2 (que yo creo que algo así sería más sensato), pues cambiarlo es fácil.
> Rubén: yap, entiendo
> Rubén: me da nervios regarla por no ver alguna implicación de hacer el cálculo así
> Rubén: entiendo que con tu propuesta se pueden ajustar los valores
> Ricardo: exacto!
> Rubén: sòlo que trabajaríamos en una lógica de asignarles puntos a cada rubro
> Ricardo: Ajá, hay que pensar eso con mucha calma
> Rubén: sipi
> Rubén: quisiera hacer contigo una simulación
> Rubén: de qué puntos saca una IEs midiendo de una u otra manera
> Rubén: nomás para no regarla
> Ricardo: va va!
> Rubén: ya estamos en ùltimos preparativos del diplomado
> Rubén: de la clausura que te conté
> Rubén: pero pasando el miércoles le entro de lleno a onigies
> Ricardo: sí! sin tema!
> Ricardo: yo estoy de lleno!
> Rubén: yuuupi
> Rubén: mil gracias
> Rubén: le acabo de mostrar a Norma y Pati la plataforma
> Rubén: y están felices
> Rubén: estuvimos viendo las buenas prácticas
> Ricardo: ah, genial!!

Ricardo fijó después el orden de las palabras en «Armonización e institucionalización», que es el del rótulo del instrumento.

## Verificación y artefactos no versionados

Pytest 103, Vitest 9, cero errores de consola en el dashboard. Capturas de trabajo en `/tmp/fase2*.png` (no versionadas). La reunión presencial con Rubén del 4 de septiembre sigue sin record; Ricardo trae el audio ([[task-137]]).

## Limpieza de comentarios (8 de septiembre)

Al revisar el diff, Ricardo encontró que los archivos nuevos y tocados traían más líneas de comentario que de código (serializers y schemas de `question`, `ObservableHeader.vue`, los `*EditSimple.vue`, `AxisSheet.vue`), que `api/CLAUDE.md` había quedado con la fila de `question` enumerando campos y que `api/TESTING.md` creció de más. Se hizo una pasada de limpieza sobre todo lo tocado en la sesión, con la regla del CLAUDE.md global (solo el porqué no obvio). El barrido del resto del proyecto y el método para que no se repita quedaron en [[task-138]]; las correcciones sobre el harness, en [[global:fb-443]], [[global:fb-444]] y [[global:fb-445]].
