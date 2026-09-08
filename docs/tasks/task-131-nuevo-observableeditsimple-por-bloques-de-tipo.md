---
type: task
id: task-131
title: Nuevo ObservableEditSimple por bloques de tipo de pregunta y ObservableSheet no automático
state: open
date: 2026-09-07
owner: ai
parent: "[[task-2]]"
source: ["[[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]]"]
depends-on: ["[[task-42]]"]
---

# Nuevo ObservableEditSimple por bloques de tipo de pregunta y ObservableSheet no automático

Fase 3 del rediseño de la edición de observables. El texto de Ricardo del prompt inicial (7 de septiembre de 2026), íntegro:

> ### Detalle (Edit y SheetCommon)
>
> Quiero cambiar completamente y creo que lo ideal es hacer un EditSimple desde cero, cambiando toda la lógica: Quiero primero seea "name", "number", "order", "description" e "init_question".
>
> Después de ese bloque, quiero que se organice por tipo de preguna. Dentro de cada tipo de pregunta quiero que tenga las preguntas directo con los <v-textarea> (sin los expansion panels que creo que aquí no tienen sentido) y con un botón de guardado por pregunta. También con la posibilidad de agregar una pregunta en cada tipo. Dime si se te ocurre (a ti o al SAG correspondiente) una idea distinta para yo validarla antes de hacer la ejecución. Cada bloque o tipo debería tener primero sus preguntas generales ancladas a Observable () + sus pesos (en la misma línea o sin que ocupe tanto espacio eso)
>
> La lista de tipos es:
> **Institucionalización/Armonización**
> **Transversalidad sectorial**: la lista de sectores (bueno, el campo de "has_main_sectors" con los nombres de los sectores allí incluídos junto a "other_sectors" con un <v-select> múltiple, tal vez con chips, no sé; con has_general planning al final (que aparezca el texto real del cuestionario)
> **Transversalidad orgánica**: La pregunta para instancias académicas y administrativas y si aplica ambos o no (academic y admin). Por default todos están en true?
> **Planes de Estudio** De PlanQuestion
> **Especiales** SpecialQuestion
> **Population** Hay una pregunta que sí tiene pop_weight
>
> Los grupos o tipos de pregunta que no tengan nada dentro, deberían estar ocultos, pero hay que pensar en cómo desplegarlos (si con el botón +) si de repente se agrega un tipo de pregunta a un observable. Igual vamos dialogando esto, dame una propuesta y lo rebotamos.
>
> # Ponderación global
>
> A ver, hay otra idea que atraviesa todo esto y creo que no la había expresado antes:
>
> Mi idea central es que a_weight, b_weight y reach_weight tengan valores globales editables, ya está en `QuestionType` , pero aún no tiene un lugar en el dashboard. Esos valores se pueden cambiar en algunos Observables. Para visualizar eso se me ocurren dos ideas: que exista un campo booleano del modelo Observable para "Pesos personalizados", o que en el dashboard, si el campo de los weigths está vacío poner el default de alguna manera visible y claro (no sé cómo). No estoy seguro que el valor de default_weight en `QuestionType` deba ser 0 o nulo en los otros tipos que no aparecen en todos lados.
>
> Ahora, un paso atrás con eso, creo que no existe un lugar que diga si el Observable tiene los plans, special o population. Tal vez deberíamos tener un M2M en Observable con QuestionType, aunque eso nos llevaría a una importación circular problemática, rebotemos ideas de cómo lo podemos solucionar. (Creo que esto resuelve una de las dudas de cómo incluir un nuevo tipo que anoté más arriba)
>
> Algo importante que no sé si esté registado: todos los observables deben tener a_questions y b_questions, esos 2 tipos tal vez deberían compartir una nueva flag en QuestionType con una flag en true de "required". Creo que actualmente hay un Observable que no tiene su BQuestion.
>
> `reach` lo tienen 35 de 41 observables, es algo que hay que comentar con Rubén el próxima reunión del viernes 11 de septiembre, si no debería ser algo obligatorio.
>
> También necesitamos una validación para que, si existe algún tipo de pregunta no 'required' en el observable, el valor de todos los weigths del observable (incluidos los 2 required) deberían tener un valor no nulo.

## Lo que ya quedó resuelto en la sesión del 7 de septiembre (no se rediscute)

- La «Ponderación global» ya existe: [[adr-0014]]. `ObservableQuestionType` (app `question`) dice qué tipos aplican a cada observable y lleva el peso propio (`weight`, nullable; efectivo = propio o `QuestionType.default_weight`). Tiene catálogo propio (`observable_question_type`, filtros por `observable` y `question_type`) con solo `weight` escribible, así que se guarda con `saveElement` estándar. No hay flag «pesos personalizados»: peso propio nulo = usa el default; el editor debe mostrar el default visible cuando el propio está vacío.
- `QuestionType.order` fija el orden de los bloques (A=1, sectorial=2, orgánica=3, planes=4, especial=5, población=6). `QuestionType.required` es verdadero en A y orgánica. `public_name` es la fuente de los nombres: leerlo de `cats.question_type` (ya llega en el payload), nunca hardcodear. Nombres vigentes: «Armonización e institucionalización», «Transversalidad sectorial», «Transversalidad orgánica», «Planes de estudio», «Pregunta especial», «Distribución de población».
- El detalle del observable (`ObservableFullSerializer`) anida `observable_question_types` (con `question_type`, `weight`, `final_weight`, `public_name`, `id`) y las cinco familias (`a_questions`, `b_questions`, `reach_questions`, `plan_questions`, `special_questions`).
- `Observable.reach_instances_question` ya no existe: el texto de transversalidad orgánica vive solo en `BQuestion.text`. `a_main_subtitle` está poblado (instrucción del bloque A). `number` y `order` siguen de solo lectura y **`order` no será editable** (clave natural del seed).
- El editor compartido `question/common/ObservableQuestionEdit.vue` ya es «un `v-textarea` + botón Guardar» por pregunta y lee la etiqueta de `cats.question_type`; se reutiliza directo dentro de cada bloque.
- La validación de pesos («si hay un tipo no requerido, todos los pesos no nulos») es **aviso**, no bloqueo: se permiten nulos.
- El nombre real del campo es `others_sectors` (no `other_sectors`).
- El Sheet del observable deja de ser automático: `ObservableSheet.vue` propio o vacío, porque el editor nuevo absorbe las familias y el bloque «Ponderaciones por tipo de pregunta», que hoy se pinta como «SIN NOMBRE/TÍTULO» bajo el observable.

## Decisiones que abren la fase (pospuestas el 8 de septiembre por Ricardo)

- **Conteo de observables en `ComponentHeader`**: hoy se calcula en el frontend desde el árbol de ejes en memoria porque la fila de componente no trae conteo. Alternativa: `count_fields` en `ComponentSchema`, como ya hace `ObservableSchema`. Para Eje no aplica (sus filas no pasan por el endpoint anotado). Recomendación: backend para Componente.
- **`TYPE_CHIPS` en `ObservableHeader`**: el mapa existe porque ícono y color de cada chip salen de la colección de preguntas y población no tiene colección. Alternativa: `icon` y `color` en `QuestionType` (dos campos, migración pequeña, editables en «Tipos de pregunta»), con lo que el chip lee todo del catálogo y el mapa se reduce al campo de conteo. Recomendación: agregarlos.

- **Etiqueta del textarea de cada pregunta**: hoy es el `public_name` a secas («Transversalidad orgánica»); decidir si debe leerse «Pregunta de …», como Ricardo pidió para el nombre de la colección de A.
- **Solo lectura en editores**: un dato de solo lectura es un campo `readonly` del mismo tipo (`v-text-field`, `v-checkbox`), nunca un chip (corrección de Ricardo del 8 de septiembre, [[global:fb-448]]); falta escribir la convención en `dashboard-collections`.
- **`ux-designer`**: usar el skill para el layout de los bloques, como Ricardo sugirió en el prompt inicial y no se hizo en la sesión.

## Pendientes del cierre del 8 de septiembre para revisar al abrir

- Revisar en PyCharm el diff de los dos commits (código y documental) de la rama `edicion-cuestionario-v2`.
- El comentario que explicaba `white-space: normal` en `TitleCommon.vue` no se restauró porque Ricardo lo había borrado a mano; el porqué vive en `dashboard-collections` y en [[task-136]].
- `load_questionnaire` aborta ahora si un componente fue renombrado desde el dashboard ([[task-134]]); confirmar que el resembrado del siguiente deploy pasa ese pre-flight.

## Lo que sigue abierto y hay que decidir con Ricardo antes de ejecutar

- Crear preguntas desde el editor exige que `observable` deje de ser `read_only` en `ObservableQuestionSerializer` (`api/api/views/question/serializers.py`); `NoDeleteMixin` permite POST, `hide_create` es solo cosmético. Es contradicción con la política escrita «solo textos» y va a ADR (enmienda de [[adr-0014]]).
- Los campos de reach (`has_main_sectors`, `others_sectors`, `has_general_planning`) y de B (`includes_academic`, `includes_admin`) siguen `read_only` en sus serializers; abrirlos es la misma decisión.
- Cómo re-agregar un tipo oculto: propuesta pendiente de validar, un menú «+ tipo» con los tipos del catálogo no presentes en el observable, que solo crea la fila puente (y con ella el bloque vacío) sin tocar la API hasta guardar la primera pregunta o el peso. Presentar alternativas y esperar el ok (ver [[global:fb-434]] sobre «para que la valide»).
- Distribución de población: tipo sin modelo de pregunta; su bloque muestra solo el peso.
- Propuesta de layout ya presentada y no validada: bloque 1 (name, number, order, description, init_question, a_main_question, a_main_subtitle) con un Guardar; luego una tarjeta por tipo con cabecera «nombre del tipo · Ponderación [ ] (def. N) · Guardar» y las preguntas debajo, cada una con su Guardar; «+ agregar pregunta» al pie de cada bloque.

Test heredado de [[task-42]], propuesto y no escrito: un PATCH de revisora cambia `text` pero no mueve `order` ni `observable`, y la IES recibe 403.

## Criterios de aceptación

- [ ] El detalle del observable muestra primero name, number (solo lectura), description, init_question, a_main_question y a_main_subtitle con un solo Guardar
- [ ] Un bloque por tipo de pregunta que aplica al observable, en el orden de QuestionType.order y con el nombre de public_name
- [ ] Cada bloque muestra el peso propio del observable con el default del tipo visible cuando el propio está vacío, y lo guarda por el catálogo observable_question_type
- [ ] Cada pregunta se edita en su textarea con su propio Guardar, sin expansion panels
- [ ] Se puede agregar una pregunta en cada bloque y agregar un tipo no presente, con la mecánica validada por Ricardo
- [ ] Los tipos sin contenido quedan ocultos
- [ ] ObservableSheet propio: bajo el editor no se listan colecciones hijas automáticas
- [ ] La validación de pesos no nulos aparece como aviso, nunca bloquea el guardado
