---
type: record
id: 2026-09-07-cotejo-del-instrumento-maquetado
title: Cotejo del instrumento maquetado 2026 contra el original, el seed y la base
date: 2026-09-07
related: ["[[2026-07-03-instrumento-cuestionario-2026]]", "[[cuestionario-2026-reducido]]", "[[task-19]]", "[[task-14]]", "[[task-2]]", "[[task-16]]", "[[task-17]]", "[[task-15]]", "[[task-116]]"]
---

# Cotejo del instrumento maquetado 2026 contra el original, el seed y la base

## Qué llegó

El cliente entregó la versión maquetada y final del cuestionario 2026: `~/Descargas/vf-2025-ONIGIES-maquetado.docx`. Es el documento que [[task-19]] llevaba esperando desde el acuerdo §6 de la reunión de junio —«Rubén entregaría una versión actualizada del cuestionario»— y el que las tasks [[task-2]] y [[task-14]] llaman «el instrumento definitivo» en sus criterios de aceptación.

## Método

1. **Conversión**: `pandoc -t gfm --wrap=none` sobre el .docx, para obtener markdown comparable con [[2026-07-03-instrumento-cuestionario-2026]], que en su día salió de la misma ruta Word→markdown.
2. **Normalización en cuatro niveles**, para descartar el ruido que introduce la conversión y no el autor: pipe-tables frente a `<table>` en bloque, `_` frente a `*` como marca de énfasis, viñetas frente a numeración, y `&nbsp;` frente a espacio ordinario.
3. **Diff por sección**: se segmentaron ambos documentos y se compararon uno a uno.
4. **Cotejo literal contra el seed y contra la base**: cada texto sembrado en `api/question/seed_data/` y cada texto vivo en la base local se buscó literalmente en los dos documentos.

Los scripts y el markdown convertido fueron material desechable de la sesión: se borraron tras el cotejo y no se versionaron. Repetir el cotejo toma minutos con `pandoc -t gfm --wrap=none` sobre el .docx y un diff por sección.

## Resultado: son el mismo instrumento

**Misma estructura, exacta**: 61 secciones en ambos documentos —4 materias, 41 observables y las 5 subsecciones de información de base—, sin una sola sección de más ni de menos.

**Dos diferencias, ambas triviales y de forma**: en el observable 2.3 la «Pregunta inicial» gana dos puntos, y en la lista de verificación 41 casillas pierden un espacio duro. Nada más.

**Cero cambios sustantivos**: ninguna pregunta nueva, ninguna opción nueva, ningún texto de pregunta u opción reescrito. Se conserva el orden Mujeres antes que Hombres, y ambos documentos escriben «sexo-género» —dato que toca el punto B.2 del documento de correcciones, donde se proponía unificar las tres grafías del instrumento—.

**Seed frente a base local: 0 diferencias.** Nadie ha editado textos desde el dashboard todavía, así que la superficie de edición que entregó [[task-42]] no ha divergido del seed.

**Seed y base frente a los dos documentos**: 442 de 443 textos del seed y 482 de 488 textos de la base coinciden literalmente con **ambos** documentos, y **ninguno coincide con uno solo** —que es la prueba de fondo de que la versión maquetada no introdujo texto nuevo—. Los no coincidentes no son discrepancias: son cadenas que el seed compone (la `PlanQuestion` del 1.12, que lleva sufijo de nivel, y la `SpecialQuestion` del 1.14) más la errata que sigue abajo.

## La errata «mensturales» sigue en la versión final

Los **dos** documentos —el original de julio y el maquetado final— dicen «Permisos o licencias **mensturales**» en el observable 3.2, opción A n.º 9. El seed (`api/question/seed_data/axis_3.py:159`) y la base dicen «menstruales.»: la corrección es correcta y se queda.

Esto reabre un supuesto: [[2026-07-03-reduccion-del-cuestionario]] daba «mensturales» por resuelta en el reducido, y el documento de correcciones del 4 de septiembre la archivó en su bloque informativo B.5 como «errata ya corregida, no requiere decisión». Corregida está —en la plataforma—, pero el documento del cliente la conserva, y quien vuelva a maquetar desde ese archivo la reintroduce.

## Lo que la versión final no trae

- **No corrige el observable 4.4**: la pregunta de alcance poblacional sigue copiada de los observables de armonización normativa. [[task-16]] sigue esperando la definición del cliente.
- **No define el alcance de 2.1 y 2.2**: siguen diciendo solo «instancias académicas». [[task-17]] sigue abierta.
- **No trae ponderaciones**: no hay tabla de pesos por observable en ninguna parte del documento. [[task-15]] sigue bloqueada exactamente igual, con los pesos en `null` y el fallback a `QuestionType.default_weight`.
- **No incorpora ninguna de las correcciones** del documento que se armó el 4 de septiembre para la CIGU ([[2026-09-04-correcciones-de-redaccion-del-instrumento]], [[task-116]]). Era previsible —la maquetación es anterior a esa entrega— pero conviene dejarlo escrito para que nadie lea el .docx final como si ya las respondiera.

## Consecuencia operativa: no hace falta re-sembrar

Como el texto es el mismo, `load_questionnaire` no tiene nada que propagar: la base de producción ya corresponde al instrumento definitivo. Tampoco hay que tocar [[cuestionario-2026-reducido]], que sigue siendo una reducción fiel de un texto que no cambió. Todo lo que queda por corregir en el instrumento son decisiones de la CIGU, no integración de una versión nueva.
