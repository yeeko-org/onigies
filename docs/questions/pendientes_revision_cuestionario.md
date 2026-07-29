# Pendientes de revisión — Cuestionario ONIGIES 2026

Generado al reducir `all_questions.md` a `all_questions_reduced.md`. No se
corrigió ningún contenido del cuestionario original; todo lo aquí listado
requiere una decisión o corrección de Ricardo antes de convertir el
documento a JSON de inserción.

> **Estado al 2026-07-03:** resueltos los pendientes de forma (§2 y §3).
> Las dudas de contenido que requieren al cliente (§1 y las instancias de
> §2) se trasladaron a `dudas_a_resolver_con_cliente.md`. Siguen abiertos,
> como pendientes de fondo/diseño de Ricardo, §4 (`Sector.is_main`) y §5
> (correr `makemigrations`/`migrate`).

## 1. Error de contenido real (no solo de forma) — MOVIDO A DUDAS CON CLIENTE

*Trasladado a `dudas_a_resolver_con_cliente.md`, punto 1. Se conserva aquí
el detalle original.*

**Observable 4.4 — Personas de primer contacto especializadas en materia
de violencias de género.** La pregunta de "Variable B" (alcance
poblacional) dice textualmente:

> ¿A qué poblaciones se consideró **este proceso de armonización**?

Este texto es un copy-paste de la pregunta de los observables de
armonización normativa (1.1/4.1) y no corresponde al tema de 4.4
(personas de primer contacto). Se dejó verbatim en el documento reducido,
marcado con ⚠️. **Falta redactar el texto correcto** (algo como "¿A qué
poblaciones se dirige esta atención de primer contacto?").

## 2. Erratas ortográficas / de redacción

| Ubicación | Problema | Estado |
|---|---|---|
| Observable 3.2, opción 9 | "Permisos o licencias **mensturales**" → "menstruales" | ✅ Corregido en el reducido |
| Título Observable 4.6 | "violenci**aS** basadas" — mayúscula suelta | ✅ Ya en minúscula en el reducido (el error solo persiste en el original, que no se toca) |
| Línea 460 del original (antes de Obs. 1.5) | Carácter suelto "s" huérfano, artefacto de la conversión Word→Markdown | ✅ No sobrevivió a la reducción |
| Varios (líneas 1671, 1733, 1775-1779, 2008-2010 del original) | Encabezados `#####`/`####` vacíos, mismo artefacto de conversión | ✅ No sobrevivieron a la reducción |
| Observable 2.1 y 2.2 | La pregunta de instancias dice "¿Cuántas instancias académicas implementan dichas políticas?" pero la tabla original incluye también una fila de "instancias administrativas". | ➡️ Duda de contenido; se mantiene "solo académicas" y se trasladó a `dudas_a_resolver_con_cliente.md`, punto 2 |

## 3. Discrepancias de título entre "Lista de verificación inicial" y el Cuestionario

Se resolvió guardar ambos textos sin pérdida: `name` = título del
Cuestionario, `description` = título de la lista de verificación (ya
aplicado en `all_questions_reduced.md`). Se listan aquí para que Ricardo
confirme que ningún caso amerita, en realidad, unificar/corregir uno de
los dos textos:

> **Resuelto (2026-07-03):** confirmada la estrategia dual-save para las 9
> discrepancias restantes (1.7, 1.12, 1.16, 1.17, 2.2, 2.3, 4.3, 4.9,
> 4.13); ninguna se unifica. El caso 1.11 sí se corrigió: se eliminó el
> sufijo "/ características de los observables" del `name` (ver nota al
> final de esta sección).

| Observable | Lista de verificación | Cuestionario |
|---|---|---|
| 1.7 | Integración paritaria y políticas para el aumento de mujeres y grupos históricamente discriminados en áreas segregadas | Integración paritaria |
| 1.11 | Evaluaciones de las políticas de igualdad de género | Evaluaciones en igualdad de género / características de los observables *(el sufijo "/ características de los observables" parece un resto de nota interna de trabajo, no un título)* |
| 1.12 | Planes y programas de estudio con perspectiva de género | Planes y programas de estudio, y asignaturas para la igualdad de género y con perspectiva de género (docencia) |
| 1.16 | Mecanismos y criterios de permanencia estudiantil para la igualdad | Mecanismos y criterios de ingreso, permanencia y evaluación estudiantil para la igualdad y no discriminación |
| 1.17 | Evaluaciones de las políticas académicas en materia de igualdad de género | Evaluaciones académicas en materia de igualdad de género |
| 2.2 | Políticas institucionales de no discriminación a la población LGBTIQ+ | Políticas institucionales y académicas de inclusión y no discriminación |
| 2.3 | Mecanismos institucionales para el reconocimiento legal y social de las identidades de género | Mecanismos institucionales de reconocimiento de la diversidad sexo-genérica |
| 4.3 | Mecanismo específico para la atención de casos de discriminación / violencia basada en el género | Normas específicas para la atención de casos de discriminación / violencia basada en el género |
| 4.9 | Responsabilidades de actuación **con instancias externas** para atender casos de discriminación y violencia basada en el género | Responsabilidades de actuación para atender casos de discriminación y violencia basada en el género |
| 4.13 | Evaluación de la experiencia de las personas usuarias de los mecanismos de atención de la violencia de género | Evaluación de atención de procedimientos formales (quejas o denuncias) de atención de casos de violencias de género |

*(Nota 1.11 — ✅ **Resuelto (2026-07-03):** se confirmó que el sufijo
"/ características de los observables" era una nota de trabajo pegada por
error. Se eliminó del `name`, que queda como "Evaluaciones en igualdad de
género".)*

## 4. Pendiente de diseño — `Sector.is_main`

En `api/indicator/management/commands/load_sectors.py`, "Población
externa" y "Público en general" están marcados `is_main=False` (junto con
"Titular de la IES", "Máximo cuerpo colegiado de toda la IES" y
"Autoridades y alto funcionariado"). Sin embargo, en el cuestionario
aparecen junto con los 10 sectores `is_main=True` en la inmensa mayoría de
las preguntas de alcance poblacional (33 de 35 observables con lista de
poblaciones; las únicas excepciones son 1.13 y 1.16, que usan listas
totalmente distintas).

Además, el bloque adicional del Observable 1.7 ("¿Cuál es la integración
por sexo-género de las siguientes poblaciones de la IES?") lista
explícitamente **solo los 10 sectores `is_main=True`**, sin incluir
"Población externa" ni "Público en general" — lo cual es consistente con
que esos dos sectores NO deberían tratarse como "principales" para efectos
de indicadores de composición por sexo-género, pero SÍ deberían incluirse
en el alcance normativo/programático general.

**Para discutir en la próxima iteración:** ¿conviene mantener el diseño
actual (`has_main_sectors=True` + `others_sectors` explícito con
"Población externa"/"Público en general" en cada `ReachQuestion`
estándar), o cambiar `is_main=True` para esos dos sectores y usar
`others_sectors` únicamente para los casos realmente excepcionales
(1.6, 1.13, 1.16)? Esta segunda opción reduciría la carga de captura al
crear cada `ReachQuestion` en el JSON de inserción.

## 5. Cambio de modelo ya aplicado

Se agregó `Observable.reach_instances_question` (TextField, análogo a
`a_main_question`/`a_main_subtitle`) en `api/indicator/models.py` para
poder almacenar el texto de la pregunta "¿Cuántas instancias académicas y
administrativas...?" que acompaña a casi todas las preguntas de alcance
poblacional. **Falta ejecutar `makemigrations`/`migrate`** (Ricardo lo
corre manualmente).
