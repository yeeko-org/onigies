---
type: task
id: task-107
title: "Modelo GeneralQuestion: las preguntas base dejan de ser un JSON"
state: closed
date: 2026-08-11
owner: ai
parent: "[[task-101]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
---

# Modelo GeneralQuestion: las preguntas base dejan de ser un JSON

Hoy las preguntas de la sección viven como un JSON en `GeneralGroup.fields` —una lista de objetos con clave, rótulo, tipo y a veces unidad— que se siembra desde `api/question/seed_data/catalogs.py` y viaja tal cual al frontend. Ese JSON no se puede editar desde un formulario, no tiene orden propio y no tiene dónde separar el texto de la pregunta del rótulo del campo. Se sustituye por un modelo.

**`GeneralQuestion` vive en la app `question`**, junto a las cinco clases de pregunta del cuestionario por observable —AQuestion, BQuestion, ReachQuestion, PlanQuestion y SpecialQuestion— y con su misma convención: un texto, un orden y una FK al padre.

Sus campos:

- `general_group` — FK al grupo.
- `name` — clave estable. Mapea a la columna del Survey donde aterriza la respuesta y ancla el comportamiento custom que vive en código. **No editable desde el dashboard:** cambiarla rompe la persistencia.
- `text` — la pregunta como la lee la IES. Editable.
- `label` — rótulo corto opcional del campo, para cuando lo que se cuenta no son personas: «Planes», «Instancias». Editable.
- `q_type` — `integer` o `boolean`.
- `order`.
- `addl_config` — JSON con diccionario vacío por defecto, para parámetros de comportamiento. **No editable desde el dashboard.**

`GeneralGroup` gana `title`, `subtitle` e `instruction`. **Se descarta «complemento»** hasta que aparezca un caso real que lo pida.

**Rompe el frontend a propósito.** El JSON de campos desaparece del modelo y del serializer, y con él el contrato que hoy consumen los componentes de grupo. Ricardo lo autorizó explícitamente. La adaptación del frontend es [[task-113]], y **va en el mismo lote y el mismo commit que esta**: entre una y otra la sección de captura queda rota, así que no se separan.

**Sin migración de datos.** Los datos de generales en producción son desechables: se re-siembra y ya. No se escribe data migration.

El seed se rehace en la misma pasada, y ahí entran dos pendientes que venían de la reunión del 11 de agosto. El primero es **partir los rótulos actuales** en los campos nuevos; el caso claro es forma de gobierno, donde hoy cada opción es una frase completa y debe quedar como nombre del tipo, en negritas, más su descripción. El segundo es el **orden de los grupos**: forma de gobierno pasa a ser el primero —acuerdo con Rubén, `[27:36]`–`[29:38]`, «hasta por eso la primera»— y **poblaciones se mantiene antes que autoridades**, decisión de Ricardo tras diálogo, porque la sección va de lo general a lo específico.

## Cierre (2026-08-12, sesión orquestada)

Entregada en `943c7ac`, adelantada de su sesión original a la misma noche por decisión de Ricardo («hoy todo»). El modelo quedó con **ocho campos, no siete**: Ricardo agregó en el cierre `unit` (con la regla `effective_label = label or unit`) y `hint` (texto de ayuda editable, promovido desde `addl_config` cuando Ricardo detectó que ahí el equipo de Rubén no podría corregirlo). El AC de «siete campos» queda desfasado a sabiendas y así se cierra. Gobierno se modeló como una sola booleana `name=is_centralized` con los textos de opción en `addl_config`. Inventario sembrado: 7 preguntas en 5 grupos (ninguna inventada para autoridades). Decisión posterior clave: **«textos solo al crear»** en el seed (`create_defaults`) para que las ediciones del cliente sobrevivan al re-seed, con backfill de textos de grupo dentro de `indicator/0009` porque las filas de producción ya existen (hallazgo D1 de la revisión crítica). Costo documentado: cambios de redacción en la semilla ya no bajan a filas existentes — se editan vía catálogo ([[task-108]]).

## Criterios de aceptación

- [x] Existe el modelo GeneralQuestion con sus ~~siete~~ ocho campos y su migración
- [x] GeneralGroup tiene title, subtitle e instruction
- [x] El JSON de campos ya no existe ni en el modelo ni en el serializer
- [x] El seed siembra las preguntas de los cinco grupos, con forma de gobierno primero y poblaciones antes que autoridades
- [x] Las dos opciones de forma de gobierno están partidas en nombre del tipo y descripción
