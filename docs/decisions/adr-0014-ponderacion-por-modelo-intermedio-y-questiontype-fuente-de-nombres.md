---
type: decision
id: adr-0014
title: La ponderación y la aplicabilidad de los tipos de pregunta viven en un modelo intermedio; QuestionType es la fuente de nombres y pesos default; el dashboard manda sobre los textos del instrumento
state: accepted
date: 2026-09-07
origin: ricardo
deliberation: dialogued
source: ["[[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]]"]
rationale: recorded
supersedes: null
superseded-by: null
affects:
  - api/question/models.py
  - api/indicator/models.py
  - api/question/initial_data.py
  - api/question/management/commands/load_questionnaire.py
  - api/question/catalog_schema.py
  - api/api/views/indicator/serializers.py
  - api/api/views/question/serializers.py
  - nuxt/app/components/dashboard/common/generic/EditCommonFields.vue
related: ["[[task-15]]", "[[task-42]]", "[[task-131]]", "[[adr-0003]]", "[[adr-0005]]"]
---

# La ponderación y la aplicabilidad de los tipos de pregunta viven en un modelo intermedio; QuestionType es la fuente de nombres y pesos default; el dashboard manda sobre los textos del instrumento

## Contexto y planteamiento del problema

Hasta el 7 de septiembre de 2026 el observable tenía seis columnas nullable de peso (`a_weight` … `pop_weight`) que replicaban por convención de nombre la tabla `QuestionType` (`weight_name`), y «qué tipos de pregunta aplican a un observable» solo se infería de que existieran filas de pregunta. El nombre público de cada tipo vivía en cuatro lugares que divergían (`QuestionType.public_name`, que nadie leía; `verbose_name` del modelo; `name` del `CatalogSchema`; etiquetas fijas en Nuxt), y el seed de `QuestionType` pisaba nombre y peso en cada `migrate_initial_data`. Además, dos textos escritos se contradecían: el docstring de `load_questionnaire` («los ajustes hechos por admin se pierden a propósito») y el del catálogo de observables («la superficie donde se corrige el instrumento»). Ricardo quería pesos globales editables con override por observable, saber qué tipos tiene cada observable, y que el equipo de la CIGU corrija textos desde el dashboard sin que un deploy los revierta. Rubén fijó por WhatsApp la nomenclatura (ver la fuente).

## Criterios de decisión

- Un solo lugar por cada dato: nombre público, peso default, aplicabilidad y peso propio.
- Agregar un tipo de pregunta no debe exigir columnas nuevas en `Observable`.
- Lo que el cliente edita no lo pisa un deploy; lo que es estructura del instrumento lo gobierna el seed.
- Nada de importación circular ni referencias por string que la disimulen.

## Opciones consideradas

- **Aplicabilidad y pesos**: (A) M2M simple `Observable↔QuestionType` y conservar las seis columnas; (B) modelo intermedio `ObservableQuestionType(observable, question_type, weight)` que reemplaza las columnas; (C) flag booleano «pesos personalizados» en `Observable`.
- **Distinción armonización/institucionalización**: (A) campo en `Observable`; (B) campo por opción en `AQuestion`; (C) dos `QuestionType`; (D) no almacenarla y nombrar el bloque con las dos palabras.
- **Textos del instrumento**: (A) el seed manda (como [[adr-0003]] para `flow.Status`); (B) el dashboard manda y el seed escribe solo al crear.
- **Instrucción del bloque A**: (A) fidelidad literal, campo `a_main_subtitle` por observable con las tres redacciones del instrumento; (B) una sola instrucción en `QuestionType`.

## Resultado

1. **Modelo intermedio** `ObservableQuestionType` en la app `question` (`question` ya importa `indicator`; no hay ciclo). Una fila por (observable, tipo) = «el tipo aplica»; `weight` nullable = peso propio; efectivo = propio o `QuestionType.default_weight`. Las seis columnas de `Observable`, `QuestionType.weight_name` y los `final_*_weight` desaparecen. No se declara `ManyToManyField(through=…)`: las dos FK bastan y el M2M solo inflaba el payload. Los pesos siguen nulos hasta que el cliente los entregue ([[task-15]]); la validación «si aplica un tipo no requerido, todos los pesos no nulos» es aviso, no bloqueo.
2. **`QuestionType` es la fuente de verdad** de `public_name` (el frontend lo lee de `cats.question_type`, nunca lo hardcodea), `default_weight`, `order` (orden de bloques: A, sectorial, orgánica, planes, especial, población) y `required` (A y orgánica). Editable desde el dashboard solo en `public_name`, `default_weight` y `order`; sin crear ni borrar. `migrate_initial_data` siembra nombre y peso solo al crear (`create_defaults`) y re-afirma la estructura.
3. **Nomenclatura**: «Armonización e institucionalización» (bloque A; el instrumento lo rotula «contenido armonizado e institucionalizado» en los 41 observables), «Transversalidad sectorial» (reach) y «Transversalidad orgánica» (B), por decisión de Rubén. La distinción por opción entre armonización e institucionalización **no se almacena** (opción D); la clasificación a mano se conserva en [[2026-09-07-clasificacion-armonizacion-institucionalizacion]]; el criterio «norma que obliga a una práctica» quedó sin decidir.
4. **El dashboard manda sobre los textos del instrumento** (opción B): `load_questionnaire` escribe `name`, `description`, `init_question`, `a_main_question`, `a_main_subtitle` y los `text` de las cinco familias solo al crear; `--overwrite-texts` restaura el pisado para un resembrado explícito (se usará una vez en el siguiente deploy, porque nadie ha editado aún), y nunca toca `Axis` ni `Component`, que sí se han editado. Es la política contraria a [[adr-0003]], deliberadamente: el catálogo de estados es intrincado y no se delega; los textos del cuestionario son contenido del cliente.
5. **Estructura no editable**: `number`, `order`, `component` del observable y `observable`, `order` y las banderas de reach y B de las preguntas siguen de solo lectura; abrirlas para el editor nuevo es una enmienda a esta ADR ([[task-131]]). `Observable.reach_instances_question` se elimina: el texto vive en `BQuestion.text`. En el motor genérico del dashboard, la llave primaria solo se captura al crear un elemento (una llave de texto hay que teclearla) y queda bloqueada después; nunca se edita sobre una fila existente.
6. **`a_main_subtitle`** con fidelidad literal (opción A): la instrucción es llave explícita del seed, con sus tres redacciones y sin subtítulo en 2.1, como en el instrumento.

### Consecuencias

- **Bueno:** un séptimo tipo de pregunta es una fila de `QuestionType` y filas puente, sin migración de `Observable`; el editor por bloques ([[task-131]]) lee todo de un solo catálogo; los nombres cambian desde el dashboard sin deploy; el dashboard puede mostrar qué tipos aplican (chips) sin inferirlo.
- **Malo:** la aplicabilidad ahora tiene dos fuentes posibles (fila puente y existencia de preguntas) que pueden divergir: hoy el 1.12 tiene fila de orgánica sin pregunta ([[task-135]]); el seed sincroniza filas faltantes pero no borra; `--overwrite-texts` es un arma que hay que usar a conciencia; `QuestionType.public_name` y el `verbose_name`/`CatalogSchema.name` siguen coexistiendo como nombre técnico y nombre público.

### Cómo se comprueba

Migraciones `question` 0005–0008 e `indicator` 0010 aplicadas; `ObservableQuestionType` con 120 filas (41/41/35/1/1/1); `QuestionType` sin `weight_name` y con `order`/`required`; tests `SeedTextOwnershipTests`, `TypeWeightSyncTests`, `FinalWeightTests` en `api/question/tests.py` (103 en total).

## Más información

[[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]] (incluye la conversación de WhatsApp con Rubén), [[task-42]], [[2026-09-04-prototipo-edicion-cuestionario-deploy-e-incidente-netlify]].
