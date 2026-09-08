---
type: task
id: task-132
title: Revisión de campos no editables y textos en código de question e indicator
state: open
date: 2026-09-07
owner: ricardo
parent: "[[task-101]]"
source: ["[[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]]"]
depends-on: ["[[task-131]]"]
---

# Revisión de campos no editables y textos en código de question e indicator

Fase 4 de la sesión del 7 de septiembre. Texto de Ricardo, íntegro:

> # Revisión extra
>
> Ayúdame a revisar si se nos están escapando campos importantes que no desplegamos en el edit de todos estos módulos que vimos hoy que involucran las apps `question` e `indicator`. Todo lo importante de esos módulos es editable?, qué textos de lo que se muestra a los usuarios que sea importante está ahora en el código y cuáles tendría sentido poder editar? Veamos esto también y dialoguemos.
>
> Creo que mucho de esto tocan los dos skills de collections, pero quiero que si algo de lo que describo no estaba contemplado, dialoguemos cuál podría ser la mejor manera, en lugar de generar algo hardcoding para resolverlo. Tal vez valga la pena llamar al skill ux-designer.

## Inventario ya levantado (7 de septiembre)

- Los catálogos sin serializer propio exponen todos sus campos escribibles y sin `NoDeleteMixin`: `Axis`, `Component`, `Sector`, `AOption`, `Feature`, `FeatureOption`, `Period`. Eje y Componente se crean y borran desde el dashboard (ya lo eran antes de la sesión).
- `Observable`: escribibles `name`, `description`, `init_question`, `a_main_question`, `a_main_subtitle`; solo lectura `component`, `number`, `order`. `a_main_subtitle` ahora sí está poblado.
- Preguntas: solo `text` escribible; `observable`, `order` y las banderas estructurales de reach y B son de solo lectura (ver [[task-131]]).
- `QuestionType`: escribibles `public_name`, `default_weight`, `order`; el resto solo lectura; sin crear ni borrar. Pendiente conectarlo a `/respuestas` cuando se rehaga esa captura.
- `GeneralQuestion`: escribibles `text`, `hint`, `label`, `unit`, `order`; solo lectura `name`, `q_type`, `addl_config`. `GeneralGroup`: todo salvo `name`.
- Textos hardcodeados en Nuxt que eran nombres de tipo ya leen `QuestionType.public_name`. Quedan por revisar los hints de los editores (`ObservableEditSimple`, `GeneralQuestionEditSimple`) y los textos de `/respuestas`.

## Criterio para el diálogo

Antes de abrir un campo a edición, decidir si es contenido del cliente (se edita) o estructura del instrumento (la mueve el seed); [[adr-0014]] fija esa frontera y se enmienda si cambia. No resolver con hardcoding lo que corresponde a un catálogo.

## Criterios de aceptación

- [ ] Lista acordada con Ricardo de qué campos de question e indicator son contenido editable y cuáles estructura del seed
- [ ] Los textos visibles al usuario que se decidan editables tienen su campo en un catálogo, sin hardcoding
- [ ] adr-0014 enmendada si la frontera cambia
