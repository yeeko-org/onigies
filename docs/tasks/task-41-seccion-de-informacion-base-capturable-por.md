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

## Calendario vigente (2026-08-11)

Las fechas de arriba quedaron rebasadas. La reunión del 11 de agosto ([[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]) fijó otras, y conviene distinguir qué comprometió quién:

- **Jueves 13 de agosto: la sección visible para todas las IES.** Es lo único que puso Rubén, junto con el anuncio.
- **Viernes 14 de agosto: anuncio en la reunión con los enlaces** (las personas enlace de las IES).
- El ofrecimiento de Ricardo de subir los cambios el miércoles por la noche **quedó sin respuesta de Rubén**: es plan interno, no compromiso acordado.

Plan interno de Ricardo para llegar: trabajar hoy y la madrugada para subir la noche previa a la presentación los cambios fundamentales, y poco antes dejar lista la edición de `GeneralGroup` y `GeneralQuestion` ([[task-101]]) para que el equipo de Rubén edite lo fino sin tocar el seed.

Rubén revisará los cambios de redacción antes de la publicación definitiva y pidió que su equipo haga una prueba adicional antes de publicar en producción.

Hacer visible la sección es cambiar la constante de secciones publicadas del frontend, el mecanismo transicional que fija [[adr-0009]]; toma unos minutos y se dispara cuando Rubén lo indique.

Bugs que bloquean la presentación: [[task-105]] (el colapso de panels falló en vivo en la demo) y [[task-104]] (el logo exigido al guardar). Y [[task-106]], la validación de campos vacíos, es prerrequisito del «No aplica» de autoridades decidido el mismo día.

## Criterios de aceptación

- [x] La IES captura la sección completa de información base desde /respuestas
- [ ] Rubí y su equipo validaron la sección antes de abrirla, con la prueba adicional que pidió
- [ ] La sección está visible para todas las IES en producción el jueves 13
- [ ] La sección quedó anunciada a los enlaces el viernes 14
