---
type: task
id: task-165
title: "Agenda pendiente con Rubén: el 1.14, la unidad de análisis y lo heredado del 11 de septiembre"
state: open
date: 2026-09-22
owner: ricardo
parent: "[[task-5]]"
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
related: ["[[task-135]]", "[[adr-0017]]", "[[task-28]]", "[[task-15]]"]
---

# Agenda pendiente con Rubén: el 1.14, la unidad de análisis y lo heredado del 11 de septiembre

La reunión del 11 de septiembre ([[task-135]]) no ocurrió; su agenda pasa aquí. La siguiente reunión con Rubén es el 23 de septiembre de 2026 a las 11.

1. **El 1.14 en una IES sin función de investigación** (Normales, privadas pequeñas con RVOE solo docentes, Universidades para el Bienestar): con [[adr-0017]] un «No» vale 0; ¿se mantiene para el 1.14 o esa IES queda fuera del promedio? Argumento a favor del 0: excluirlo mejora a esas IES frente a las que investigan poco. Único candidato a «no aplica» que dejó el análisis de los 41 observables.
2. **Unidad de análisis en IES no autónomas** (campus del TecNM, Normales, unidades de la UPN): ¿responde el campus por sí mismo, contestando «No» donde no tiene la palanca (presupuesto etiquetado, promoción docente, licencias laborales, perfiles de puesto), o reporta la normatividad de su sistema?
3. Heredado de task-135: si el alcance sectorial es obligatorio (lo tienen 35 de 41; sin ella 1.1, 1.12, 1.14, 1.15, 4.1, 4.7); el 1.12 sin pregunta B; simular calificaciones antes de fijar la ponderación (pesos propios siguen nulos, [[task-15]]).
4. Para cuando exista cálculo: las reglas 0/0 (especial del 1.14 con cero proyectos; parte administrativa de B con cero instancias) y la herencia gen → cp de los denominadores (`is_present`, `no_apply`).
5. **Ritmo de aprobación de generales, condición de la apertura del 25.** En la copia de producción del 22 de septiembre, 0 de 66 paquetes de generales están en `gen_finished` (51 `gen_draft`, 14 `gen_sent`, 1 `gen_need_changes`). Con [[adr-0018]], ninguna IES captura cp hasta que la revisión finalice su información base, aunque la fecha haya pasado; sin un ritmo de revisión acordado, la apertura del 25 no abre nada ([[task-163]]).

## Criterios de aceptación

- [ ] Respuesta de Rubén sobre el 1.14 registrada
- [ ] Unidad de análisis en IES no autónomas decidida y registrada
- [ ] Alcance obligatorio, 1.12 y simulación de calificaciones acordados o agendados
- [ ] Ritmo de aprobación de generales acordado de cara a la apertura del 25
