---
type: task
id: task-52
title: Renombrar «características» y «aspectos» a «criterios» en la capa de presentación
state: open
date: 2026-08-03
owner: ai
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
---

# Renombrar «características» y «aspectos» a «criterios» en la capa de presentación

El mismo concepto se llama de tres maneras según dónde se mire. `[41:34]` «En el menú dice aspectos buenas prácticas y cuando te metes dice características». El nombre canónico lo fijó Rubí en la reunión: `[45:32]` «Criterios» → `[45:33]` «Criterios. Sí, criterios. Lo voy a cambiar a criterios».

De paso quedó fijada la composición: son **10 criterios — 2 obligatorios, 7 opcionales y 1 abierto** para que la institución agregue algo no listado (`[43:15]` «Son 8 y los 2 obligatorios» → `[43:23]` «son 10 porque son 2 obligatorios, 7 opcionales y 1...»).

**Alcance: solo la capa de presentación.** Los identificadores de código (`Feature`, `FeatureOption`, `FeatureGoodPractice`, `feature_values`, `feature_good_practice`) **no se tocan** — el costo de renombrar el modelo no se justifica y rompería el contacto con el histórico. Lo que cambia es:

- `api/example/catalog_schema.py`: `name` y `plural_name` de `FeatureSchema`, `FeaturesFilterGroup` y `FeatureGoodPracticeSchema`.
- Los `verbose_name` / `verbose_name_plural` de los modelos en `api/example/models.py`.
- Los textos del frontend: `nuxt/app/components/dashboard/example/good_practice/GoodPracticeCard.vue`, `FeatureItem.vue`, `FeatureList.vue`, `GoodPracticeEditSimple.vue`.
- Los textos de catálogo en `api/example/initial_data.py`.
- El rótulo del menú del dashboard.

Incluye además la revisión de consistencia terminológica que abre el acta: «Revisar los términos técnicos y nombres de las secciones de la plataforma del observatorio (como “criterios”, “aspectos”, “información base” y “datos generales”) para asegurar consistencia a lo largo de toda la aplicación». En particular, **«información base» vs. «datos generales»** se usan como sinónimos en la conversación y en la interfaz; hay que elegir uno y aplicarlo.

## Criterios de aceptación

- [ ] En toda la interfaz el concepto se llama «criterio», nunca «característica» ni «aspecto»
- [ ] Ningún identificador de código cambió de nombre
- [ ] Se eligió un solo nombre entre «información base» y «datos generales», y se aplicó en toda la aplicación
