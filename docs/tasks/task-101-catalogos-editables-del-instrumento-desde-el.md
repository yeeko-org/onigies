---
type: task
id: task-101
title: Catálogos editables del instrumento desde el dashboard
state: open
date: 2026-08-11
owner: ai
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
---

# Catálogos editables del instrumento desde el dashboard

Raíz nueva. En la reunión del 11 de agosto Rubén acordó que cada bloque de la información base tendrá título, subtítulo, instrucción y complemento propios, **editables desde el dashboard igual que hoy se editan los criterios de buenas prácticas**, y que las preguntas también se podrán editar.

Hoy no existe nada de eso. El catálogo `GeneralGroup`, en `api/indicator/models.py`, tiene cinco campos —nombre, nombre público, el esquema de campos en JSON, la marca de población y el orden— y ninguno de texto largo; el instrumento por observable sí modela encabezado y subtítulo por pregunta, así que la asimetría es del modelo, no del instrumento. Tampoco está dado de alta como catálogo: no hay esquema de catálogo suyo en el API. Y el menú del dashboard, en `nuxt/app/layouts/dashboard.vue`, ya lista un ítem «Grupos de preguntas» cuyo nombre de colección no corresponde a ningún modelo ni esquema registrado — un enlace muerto en el hueco exacto donde esto va.

Es raíz propia y no hija de [[task-3]] ni de [[task-41]] porque cruza las tres capas: el modelo en la app de indicadores, el registro de catálogos del API y el menú del frontend.

**Hijas** (diseñadas en diálogo con Ricardo el 11 de agosto):

- [[task-107]] — el modelo `GeneralQuestion` y los campos de texto de `GeneralGroup`, que matan el JSON de campos.
- [[task-108]] — el alta de los dos como catálogos del dashboard, con la entrada de menú «Preguntas base».
- [[task-109]] — evaluar, más adelante, un modelo abstracto común para toda la familia de preguntas.

La adaptación del frontend al contrato nuevo va aparte, en [[task-113]], porque se hace junto con la unificación de los componentes de grupo.

Compromiso operativo de esta semana: dejar lista la edición de `GeneralGroup` y `GeneralQuestion` poco antes de la presentación del viernes, para que el equipo de Rubén edite lo fino sin tocar el seed ni el admin.

## Criterios de aceptación

- [ ] El equipo de Rubén edita los textos de la información base desde el dashboard, sin pasar por el seed ni por el admin de Django
- [ ] El ítem de menú «Grupos de preguntas» apunta a una colección que existe
