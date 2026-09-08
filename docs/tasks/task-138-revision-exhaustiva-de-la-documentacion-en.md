---
type: task
id: task-138
title: "Revisión exhaustiva de la documentación en código: dónde vive, dónde se duplica, qué se queda"
state: open
date: 2026-09-08
owner: ai
parent: "[[task-3]]"
source: ["[[2026-09-07-rediseno-edicion-observables-pesos-y-nomenclatura]]"]
---

# Revisión exhaustiva de la documentación en código: dónde vive, dónde se duplica, qué se queda

Revisión exhaustiva y semiautomática de la documentación que vive en el código de todo el proyecto, `api/` y `nuxt/`: dónde vive cada explicación, dónde está duplicada (docstring, comentario, skill y ADR contando lo mismo), dónde sí dejarla y dónde quitarla.

La regla que se aplica es la de Ricardo, en el CLAUDE.md global: se comenta solo el porqué no obvio (decisión, trade-off, gotcha, workaround, invariante que el nombre no carga); nunca el qué que el código ya muestra, nunca el cambio respecto a lo anterior (eso vive en el commit y en la ADR), nunca listas de quién llama.

Motivación, en palabras de Ricardo al revisar el diff de la sesión del 7 de septiembre de 2026:

> «QuestionTypeCatalogSerializer, qué cantidad de comentarios, son más que las líneas reales»

> «question/catalog_schema.py quedó con una cantidad exagerada y sin sentido de comentarios, tantos que me abruman»

> «luego llegan otros agentes que ven eso y replican la lógica de chingos de comentarios»

Ese último punto es el riesgo de fondo: el exceso se reproduce solo, porque cada ejecutor toma el estilo del archivo vecino como norma ([[global:fb-445]]).

## Método propuesto

1. Un script (en `.claude/` del monorepo, desechable) que mida por archivo la proporción de líneas de comentario y docstring contra líneas de código, para `.py` (fuera de `venv/` y `migrations/`) y `.vue`/`.js` (fuera de `node_modules/` y `.nuxt/`), y liste los peores ordenados por proporción y por líneas absolutas de comentario.
2. Revisión humana de esa lista, archivo por archivo, con tres destinos por explicación: se queda (es un porqué no obvio), se mueve (a un skill o a una ADR, si es conocimiento de proyecto y no de ese archivo), se borra.
3. Un segundo barrido sobre duplicados: explicaciones que aparecen a la vez en un docstring y en un skill o ADR; se deja una sola casa, con preferencia por el skill o la ADR cuando es conocimiento de proyecto.

El 8 de septiembre ya se hizo una pasada sobre los archivos tocados en la sesión del 7 (serializers y schemas de `question` e `indicator`, `load_questionnaire`, y los componentes nuevos de `nuxt/app/components/dashboard/`); esta task cubre el resto del proyecto y fija el método para que no vuelva a acumularse. La idea de un critic específico para reglas de documentación quedó como [[global:fb-444]].

## Criterios de aceptación

- [ ] Existe el script de proporción comentario/código y su lista de peores archivos quedó como referencia en docs/
- [ ] Cada archivo de la lista se revisó con Ricardo y sus comentarios quedaron solo con porqués no obvios
- [ ] Ninguna explicación de proyecto vive a la vez en un docstring y en un skill o ADR
