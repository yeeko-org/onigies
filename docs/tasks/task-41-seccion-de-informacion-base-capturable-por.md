---
type: task
id: task-41
title: Sección de información base capturable por las IES
state: open
date: 2026-08-03
owner: ai
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
related: ["[[task-2]]"]
---

# Sección de información base capturable por las IES

Compromiso central de la reunión del 28 de julio y la pieza que ordena el calendario del resto del cuestionario. Rubí propuso invertir el orden de trabajo: en lugar de abrir observables y validar avances, cerrar primero la información base y validarla con las revisoras, porque si las IES mueven los datos base después cambian los denominadores de todos los indicadores. El porqué está razonado en [[adr-0007]].

Fechas comprometidas en la reunión:

- **2026-08-03 (lunes):** la sección lista para captura de las IES; esa semana Rubí la valida con su equipo. `[37:15]` «de aquí al lunes trabajas en tener lista la sección de información base para captura de las IES».
- **2026-08-10:** se abre la plataforma a las IES para esta sección. `[31:06]` «el 10 abrimos la plataforma para esa sección».
- **2026-08-14:** sesión informativa de Rubí con las IES, ya con la sección abierta.

El modelo de datos existe y está descrito en el skill `gen-general-info`; lo que falta es la superficie de captura. [[task-18]] es la parte de poblaciones y autoridades y cuelga de aquí.

Dentro de este alcance entra también la composición sexo-genérica y el sexo de la máxima autoridad, que se preguntan aquí aunque alimenten el indicador del observable 1.7 — ver [[adr-0004]], ratificado en la reunión `[28:17]`.

## Criterios de aceptación

- [x] La IES captura la sección completa de información base desde /respuestas
- [ ] Rubí y su equipo validaron la sección antes de abrirla
- [ ] La sección está abierta a las IES en producción
