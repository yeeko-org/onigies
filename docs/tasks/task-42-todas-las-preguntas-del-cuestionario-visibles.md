---
type: task
id: task-42
title: Todas las preguntas del cuestionario visibles y editables en el dashboard
state: closed
date: 2026-08-03
owner: ai
parent: "[[task-2]]"
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
depends-on: ["[[task-14]]"]
validate-paths: false
---

# Todas las preguntas del cuestionario visibles y editables en el dashboard

Acuerdo explícito de la reunión, con fecha comprometida el **2026-08-03**. `[33:11]` «Eso también puede ser como un acuerdo de hoy, que para el lunes tengamos en el dashboard visible no solo los observables, sino todas las preguntas en producción. En producción, quiero decir, como en la página, en la base de datos, para que me ayudes a validar».

No basta con que estén sembradas: al preguntarle si se trataba solo de la integración, la respuesta fue `[37:32]` «No sólo la integración, sino la visualización para que se puedan editar».

Es la hermana de superficie de [[task-14]]: aquella corre `load_questionnaire` en producción, esta construye la vista del dashboard que lista y permite editar cada pregunta. Sin el seed desplegado no hay nada que mostrar, de ahí la dependencia.

Es además el habilitador de [[task-50]]: Rubí y su equipo hacen la revisión pregunta por pregunta sobre esta misma superficie, corrigiendo ellas los textos.

## Hallazgos previos (exploración 2026-08-03)

La sesión del 2026-08-03 exploró el terreno antes de diferir la tarea. Estado real:

- **Los cinco modelos de pregunta no existen como colecciones.** `api/question/catalog_schema.py` solo registra `AOptionSchema`, `QuestionTypeSchema` y `AOptionsFilterGroup`. `AQuestion`, `BQuestion`, `ReachQuestion`, `PlanQuestion` y `SpecialQuestion` (todos en `api/question/models.py`, todos con FK a `Observable`) no tienen registro, serializer ni viewset — hoy no hay nada navegable ni editable. El grueso del trabajo backend es registrarlas vía el skill `manage-collections`.
- **Observable no tiene componentes propios en el dashboard** (`nuxt/app/components/dashboard/indicator/observable/` no existe): cae al fallback genérico. Solo existen `AxisEdit`, `ComponentEdit` y `ComponentHeader`. No hay carpeta `question/` en components/dashboard.
- **Navegación:** en `nuxt/app/layouts/dashboard.vue` ni `observables` ni ninguna colección de preguntas aparece en `main_items` ni en «Gestión Catálogos»; a Observable solo se llega por el árbol de filtros `axes`. Habrá que decidir dónde entran las vistas nuevas.
- **Decisión de diseño abierta** (nadie la ha tomado): ¿cinco colecciones independientes por tipo de pregunta, o preguntas anidadas en el detalle del Observable (un `ObservableEditSimple` que edite todo inline, al estilo de `ComponentFullSerializer` que anida observables)? Para el caso de uso real — Rubí corrigiendo textos pregunta por pregunta ([[task-50]]) — la vista por observable se acerca más a cómo ella piensa el instrumento; las colecciones planas dan búsqueda y filtros gratis. Es llamada de Ricardo.
- **El criterio «en producción»** dependía de [[task-14]]: el seed ya corrió allá con el instrumento definitivo y task-14 cerró el 2026-09-07 ([[2026-09-07-cotejo-del-instrumento-maquetado]]).

## Avance (2026-09-04): prototipo construido y desplegado

En una sesión duo arrancada antes de una reunión con Rubén, un ejecutor construyó front y back de golpe y Ricardo pidió subirlo a producción ese mismo día. Está en `bad2f71` (más `e01c3e6`, que arregló el build de Netlify); el relato completo en [[2026-09-04-prototipo-edicion-cuestionario-deploy-e-incidente-netlify]].

La decisión de diseño que estaba abierta se resolvió por la vía anidada: las cinco familias de preguntas cuelgan del detalle del observable, cada una además como catálogo propio filtrado por observable. Solo se editan textos —los seis del observable y el `text` de cada pregunta—; número, orden, componente, ponderaciones y banderas viajan de solo lectura y no hay alta ni baja. Escribir exige `is_reviewer`. La entrada de menú pasó a «Cuestionario: ejes, observables y preguntas».

Producción ya tenía los 41 observables sembrados, así que el tercer criterio se cumple; [[task-14]] cerró el 2026-09-07 con el cotejo del instrumento final.

Tres puntos quedaron abiertos aquí como «llamadas de Ricardo»; se resolvieron el 2026-09-07 ([[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]], [[adr-0014]]): `order` no se hace editable (clave natural del seed); `Observable.reach_instances_question` se eliminó y el texto vive solo en `BQuestion.text`; el test de regresión del PATCH de revisora (cambia `text`, no mueve `order` ni `observable`, la IES recibe 403) sigue sin escribir y pasa como propuesta a [[task-131]], que toca esos mismos serializers. El 2026-09-10 pasó a la lista de [[task-140]] (punto 3 del backend), junto con los tests de la compuerta del cuestionario. La superficie de edición se rediseña ahí.

Fuera de alcance y anotado: `Axis` y `Component` siguen con alta y baja desde el dashboard (ya lo eran); la lectura anónima de catálogos es preexistente y ahora cubre los textos del instrumento.

## Criterios de aceptación

- [x] El dashboard lista todas las preguntas, no solo los ejes, componentes y observables
- [x] Cada pregunta se puede editar desde el dashboard
- [x] Está desplegado en producción, no solo en local (`bad2f71`, 2026-09-04)
