---
type: record
id: 2026-07-04-seed-del-cuestionario
title: Seed del cuestionario 2026 — decisiones de modelado
date: 2026-07-04
---

# Seed del cuestionario 2026 — decisiones y pendientes

Fecha: 2026-07-04. Fuente: `docs/reference/cuestionario-2026-reducido.md`.
Implementación: `api/question/seed_data/` + comando `load_questionnaire`.

## Qué hace el comando

`python manage.py load_questionnaire [--sync-institutions]`

Idempotente (`update_or_create` por claves naturales, patrón de
`flow/seed.py`). Siembra/actualiza:

| Modelo | Clave de upsert | Notas |
|---|---|---|
| Axis | `order` | Actualiza `name` (corrige eje 4 «violencias») y `description` (subtítulo del eje). No toca icon/color/short_name |
| Component | `(axis, name)` | Sin cambios de nombre detectados |
| Observable | `(component, number)` | Actualiza name, description (alias checklist), init_question, a_main_question, reach_instances_question |
| AQuestion | `(observable, order)` | Una por opción del MD; borra sobrantes si el MD reduce opciones |
| AOption | `value` | Escala global Sí=1 / No=0 |
| ReachQuestion | `observable` | Solo casos estándar y custom; especiales diferidos |
| GeneralGroup | `name` (PK) | 4 grupos de «Información de base» |

No toca `QuestionType` (ya lo siembra `question/initial_data.py` vía
`migrate_initial_data`, con default_weight a=60, b=40) ni `Sector`
(`load_sectors`). `load_main_axis` queda obsoleto (anotado en su help).

Orden de ejecución tras migrar: `load_sectors` → `migrate_initial_data`
→ `load_questionnaire --sync-institutions`.

## Decisiones tomadas

1. **Estructura A**: texto de `a_question` → `Observable.a_main_question`;
   cada opción numerada → fila `AQuestion` (con nuevo campo `order`);
   `AOption` = escala global Sí=1/No=0 (ajustable en
   `seed_data/catalogs.py`).
2. **POB-ESTÁNDAR** (12 poblaciones) = 10 sectores `is_main=True` +
   «Población externa» y «Público en general» (`is_main=False`). El caso
   estándar se codifica `has_main_sectors=True` + esos 2 en
   `others_sectors`. Ligado al pendiente §4 de
   [[2026-07-03-reduccion-del-cuestionario]] (diseño de `Sector.is_main`).
3. **Listas custom**: 1.13 (6 poblaciones, incl. «Autoridades y alto
   funcionariado») y 1.16 (3 niveles de alumnado) →
   `has_main_sectors=False` + lista completa en `others_sectors`.
4. **`has_general_planning`**: solo 1.4 y 1.9.
5. **Preguntas abiertas con cliente sembradas verbatim**: 4.4 (texto de
   reach copiado de armonización, erróneo) y 2.1/2.2 («instancias
   académicas» sin «administrativas»). Al resolverse: corregir el MD,
   luego `seed_data/axis_N.py`, re-correr el comando.
6. **Pesos por observable**: sin fuente aún; quedan `null` y aplica el
   fallback a `QuestionType.default_weight`.
7. **GeneralGroup.fields**: esquema `{name, label, type}` con
   `type ∈ {integer, boolean}`; `poblaciones` con `fields=[]` porque su
   checklist sale del catálogo `Sector`. **Revisar/ajustar con Ricardo.**
8. **Cambio de modelo**: `AQuestion.order` (IntegerField, default 0,
   ordering) para clave natural de upsert. Migración pendiente de correr.

## Decisiones de la 2ª ronda (2026-07-04, con Ricardo)

Resuelven los antes «pendientes diferidos» 1–4, 6 y 7.

1. **Casos «solo conteo de instancias»** (1.1, 4.1, 1.15, 4.7): no
   llevan `ReachQuestion`; se cubren con la `BQuestion` del punto 2.
2. **BQuestion — opción (a)**: se siembra una `BQuestion` por cada
   observable con `reach_instances_question` (texto copiado de ese
   campo, que queda como fuente del seed). `includes_academic` /
   `includes_admin` explícitos en seed_data; default ambos `True`; solo
   académicas: 1.15, 2.1, 2.2 (estos dos últimos pendientes de cliente).
   Sin `BQuestion` las `BResponse` no tienen a qué colgarse; el campo de
   texto solo no basta.
3. **1.6**: `ReachQuestion` custom — `has_main_sectors=False` +
   others_sectors = «Titular de la IES» y «Máximo cuerpo colegiado de
   toda la IES» (mismo mecanismo que 1.13/1.16).
4. **1.12**: 4 filas de `PlanQuestion` (nuevo campo `order` para la
   clave de upsert); `PlanResponse` ya trae los 3 niveles.
5. **1.14**: `SpecialQuestion` — `SpecialResponse.total` = proyectos
   financiados, `complying` = dirigidos por mujeres.
6. **1.7 se pregunta en Generales, no en el observable**: la
   composición sexo-genérica es dato institucional del periodo. Captura
   en `PopulationQuantity` (ya tiene `number_men`/`number_women`). Las
   4 autoridades se modelan como `Sector` con nuevo flag
   `is_authority=True` (2 ya existían: Titular / Máximo cuerpo
   colegiado; 2 nuevos: «Titulares de instancias académicas» y
   «Titulares de instancias administrativas»). Nuevo `GeneralGroup`
   «autoridades» (`is_population=True`, `fields=[]`). El indicador de
   1.7 se calculará desde `PopulationQuantity` vía `pop_weight`; 1.7
   conserva solo su parte A.
7. **`has_general_planning`** confirmado como flag de opción de escape
   (no es población); la respuesta aterriza en
   `ReachResponse.not_focalized`.
8. **`Observable.number` → `CharField`** (como Decimal, «1.10» ==
   «1.1»: la identidad ya estaba rota). Se agrega **`Observable.order`**
   (global, lo asigna `load_questionnaire` por posición de recorrido) +
   `Meta.ordering = ['order']`. Gotcha de migración: en Postgres
   `numeric(4,2)` → texto produce «1.10», «4.70», etc.; la data
   migration debe mapear contra los strings del seed (match por
   componente + igualdad Decimal), no un rstrip ciego.
9. **`Sector.is_main` queda como está** (cerrado): el argumento de
   carga de captura lo absorbió `STANDARD_EXTRA_SECTORS`, y los 10
   `is_main=True` son justo la lista de composición de 1.7.
10. **`load_main_axis` se conserva** como dueño de
    `icon`/`color`/`short_name`; corregir su help (ya no está
    obsoleto).

## Pendientes que siguen abiertos

1. **Pesos reales** por observable — bloqueado: el cliente no ha
   entregado la fuente de ponderaciones. Sigue el fallback a
   `QuestionType.default_weight`.
2. **Textos con cliente**: 4.4 (reach erróneo, sembrado verbatim) y
   2.1/2.2 («instancias académicas» sin «administrativas»). Al
   resolverse: corregir MD → seed_data → re-correr comando (y ajustar
   `includes_admin` de 2.1/2.2 si aplica).
3. Frontend de Generales para el bloque autoridades/poblaciones
   (captura de `PopulationQuantity` por sector) — fuera del alcance del
   seed.
