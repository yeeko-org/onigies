---
type: task
id: task-42
title: Todas las preguntas del cuestionario visibles y editables en el dashboard
state: open
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
- **El criterio «en producción» sigue gateado por [[task-14]]**: `load_questionnaire` nunca ha corrido allá y su ventana depende de los textos abiertos del cliente. Se puede dejar todo desplegable sin correr el seed.

## Avance (2026-09-04): prototipo construido y desplegado

En una sesión duo arrancada antes de una reunión con Rubén, un ejecutor construyó front y back de golpe y Ricardo pidió subirlo a producción ese mismo día. Está en `bad2f71` (más `e01c3e6`, que arregló el build de Netlify); el relato completo en [[2026-09-04-prototipo-edicion-cuestionario-deploy-e-incidente-netlify]].

La decisión de diseño que estaba abierta se resolvió por la vía anidada: las cinco familias de preguntas cuelgan del detalle del observable, cada una además como catálogo propio filtrado por observable. Solo se editan textos —los seis del observable y el `text` de cada pregunta—; número, orden, componente, ponderaciones y banderas viajan de solo lectura y no hay alta ni baja. Escribir exige `is_reviewer`. La entrada de menú pasó a «Cuestionario: ejes, observables y preguntas».

Producción ya tenía los 41 observables sembrados, así que el tercer criterio se cumple aunque la dependencia de [[task-14]] siga abierta como tal; conviene revisar esa task contra ese dato.

**Llamadas de Ricardo pendientes** (la task no se cierra hasta resolverlas):

- `order` quedó de solo lectura, contra lo que pedía el encargo, porque en `AQuestion`, `BQuestion` y `PlanQuestion` forma con `observable` la clave natural del seed: reordenar desde el dashboard haría que `load_questionnaire` duplique filas. Reordenar de verdad exige otra clave natural (modelo + migración). En `GeneralQuestion` el orden sí es editable porque su clave es `name`.
- `BQuestion.text` duplica `Observable.reach_instances_question`: el seed copia uno del otro y hoy ambos son editables por separado. Salidas: esconder uno, propagar la edición o cambiar el seed.
- Test de regresión propuesto, no escrito: en `question/tests.py`, un PATCH de revisora cambia `text` pero no mueve `order` ni `observable`, y la IES recibe 403.

Fuera de alcance y anotado: `Axis` y `Component` siguen con alta y baja desde el dashboard (ya lo eran); la lectura anónima de catálogos es preexistente y ahora cubre los textos del instrumento.

## Criterios de aceptación

- [x] El dashboard lista todas las preguntas, no solo los ejes, componentes y observables
- [x] Cada pregunta se puede editar desde el dashboard
- [x] Está desplegado en producción, no solo en local (`bad2f71`, 2026-09-04)
