---
type: decision
id: adr-0005
title: La configuración de colecciones vive en clases de Python, no en la base
state: accepted
date: 2026-06-10
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-06-10-port-de-ps-schema]]"]
affects: ["api/ps_schema/", "api/ies/catalog_schema.py", "api/indicator/catalog_schema.py", "api/example/catalog_schema.py", "api/question/catalog_schema.py"]
---

# La configuración de colecciones vive en clases de Python, no en la base

## Contexto

El dashboard es genérico: cada colección —institución, periodo, eje, observable, buena práctica— trae una configuración que declara sus campos, filtros, nivel, ícono y acciones, y de ahí salen las rutas, los viewsets y el payload de `/catalogs/all/` que consume el frontend. Esa configuración tiene que vivir en algún lado. Hasta junio de 2026 vivía en la base de datos: `constants.py` sembraba tablas ricas al arrancar y `CatalogsView` las leía. El port del rediseño de ibero obligó a decidir si se conservaba ese esquema o se adoptaba el nuevo.

## Opciones consideradas

- **La base manda** (lo que había) — la configuración se edita sin desplegar, pero cada definición queda partida entre `constants.py`, las tablas, los viewsets registrados a mano y los serializers.
- **Las clases de Python mandan** — un `catalog_schema.py` por app declara cada colección completa; el registry genera rutas, viewsets y dump en runtime, y la tabla `Collection` se reduce a siete campos con los overrides editables.

## Resultado

Mandan las clases. La razón es de mantenimiento: **el esquema anterior duplicaba muchísimo y partía las definiciones en muchos lugares**; para entender cómo estaba configurada una colección había que reconstruirla de cuatro fuentes. Ahora vive completa en un solo archivo, se lee en el IDE y viaja en el diff. Se borraron los modelos `Level` y `FilterGroup`, y `constants.py` desapareció.

Decisión ligada, aún provisional: la mecánica se copió a onigies en local **en vez de extraer un paquete compartido**, con los puntos de acople inyectados desde `settings.PS_SCHEMA` para no cerrarse la puerta. Se reevalúa cuando exista un tercer proyecto que la use.

### Consecuencias

- **Bueno:** una sola fuente por colección; agregar una es escribir una clase (ver el skill `manage-collections`).
- **Malo:** cambiar la configuración exige desplegar; y mientras el mismo motor viva en onigies y en ibero, toda mejora hay que portarla a mano en ambos —el backport de `open_insertion` quedó pendiente de commitear en ibero.
- Mismo principio que [[adr-0006]]: control explícito en código por encima de generación implícita desde datos.

## Cómo se comprueba

`/catalogs/all/` responde igual con la tabla `Collection` vacía de filas de catálogo: solo las tres colecciones primarias conservan overrides.
