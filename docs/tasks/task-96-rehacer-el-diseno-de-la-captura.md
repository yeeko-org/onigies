---
type: task
id: task-96
title: Rehacer el diseño de la captura numérica y los panels de Generales
state: open
date: 2026-08-09
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-09-sesion-task-93-y-drift-del-harness]]", "[[2026-08-11-auditoria-del-arbol-de-trabajo-y-reorganizacion]]"]
related: ["[[task-67]]", "[[task-66]]", "[[task-93]]"]
---

# Rehacer el diseño de la captura numérica y los panels de Generales

La primera implementación del rediseño ([[task-67]] y decisiones de [[task-93]]) quedó funcional pero visualmente mala a juicio de Ricardo; se commiteó como base en `4987fa7` sin revertir, y el rehacer vive aquí.

El 11 de agosto Ricardo trabajó ese rehacer a mano, sin IA de por medio, y cerró con criterio visual propio varias de las preguntas abiertas. **Esos veredictos son definitivos y no se rediscuten**; lo que sigue abierto es lo de abajo. Este cuerpo se reescribió contra el estado real del código el 11 de agosto: la versión anterior describía el diseño que ese trabajo ya deshizo.

## Decisiones cerradas por Ricardo (2026-08-11)

1. **El campo numérico no lleva señal visual.** Se probaron dos íconos —`123` y luego `tag` (#)— y Ricardo descartó ambos. El ícono salió de los defaults del alias y no se sustituyó por nada. Es un veredicto, no un pendiente: la señalización por ícono queda cerrada en contra.
2. **La pregunta va encima del campo, no a su izquierda.** El componente de renglón-pregunta pasó a disposición en columna. Revierte la primera decisión de [[task-93]], que pedía la pregunta a la izquierda y el campo fijo a la derecha; la reversión es deliberada.
3. **Anchos:** 160 en el renglón-pregunta —con `max-width`, que es lo que el framework realmente respeta, y ahí estaba el diagnóstico del campo que renderizaba enorme— y 120 por defecto en el alias, que es lo que heredan las celdas de las tablas matriz.
4. **La franja gris se revierte.** Los panels vuelven al encabezado gris claro anterior, sin la franja lateral oscura ni el fondo propio. También revierte la regla de ancho y margen automático que [[task-66]] había cerrado para las celdas de conteo; la consecuencia de esa reversión —el número pegado al margen derecho— entra abajo como pendiente.

## Pendientes que absorbe

- **La unidad no se ve.** El sufijo del framework solo se pinta con foco o con valor, así que en un campo vacío la unidad del seed —«instancias», «planes»— es invisible. Ricardo prefiere resolverlo **con una etiqueta visible**, no con el sufijo.
- **Subir el módulo a `text-body-1`**, de forma consistente en la captura de la sección.
- **Legibilidad tipo tabla en los grupos de campos cortos.** Autocrítica de Ricardo en la demo del 11 de agosto: en textos cortos como los planes de estudio el espaciado actual dificulta identificar el contenido. El grupo de campos numéricos se pinta hoy como una columna de renglones sueltos, sin estructura tabular.
- **El número de conteo no debe quedar pegado al margen derecho.** Es la consecuencia de la reversión de [[task-66]], y la otra autocrítica de la demo.
- **Reordenar la tabla de autoridades a mujeres antes que hombres.** La tabla de poblaciones ya se reordenó y la de autoridades quedó incoherente con ella. La convención —mujeres antes que hombres, en todas partes: tablas, formularios y exportaciones— está anotada en el `CLAUDE.md` raíz.
- **Los encabezados de las columnas de conteo quedaron centrados** mientras el contenido sigue alineado a la derecha.
- **La columna Total de la tabla de poblaciones necesita ancho fijo**, idéntico al de Mujeres y Hombres.
- [[task-67]] nombra todavía el componente por su nombre viejo en su prosa.

## Criterios de aceptación

- [ ] La unidad se lee sin foco y con el campo vacío, con etiqueta visible
- [ ] Los grupos de campos cortos se leen como tabla, no como renglones sueltos
- [ ] El número de conteo no queda pegado al margen derecho de su celda
- [ ] La tabla de autoridades ordena mujeres antes que hombres, igual que la de poblaciones
- [ ] Encabezado y contenido de cada columna de conteo comparten alineación
- [ ] La columna Total tiene el mismo ancho fijo que Mujeres y Hombres
- [ ] Diseño de panels y captura aprobado visualmente por Ricardo
