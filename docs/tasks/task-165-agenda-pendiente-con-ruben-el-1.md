---
type: task
id: task-165
title: "Agenda pendiente con Rubén: el 1.14, la unidad de análisis y lo heredado del 11 de septiembre"
state: open
date: 2026-09-22
owner: ricardo
parent: "[[task-5]]"
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
related: ["[[task-135]]", "[[adr-0017]]", "[[task-28]]", "[[task-15]]", "[[2026-09-23-reunion-ruben]]"]
---

# Agenda pendiente con Rubén: el 1.14, la unidad de análisis y lo heredado del 11 de septiembre

La reunión del 11 de septiembre ([[task-135]]) no ocurrió; su agenda pasa aquí. La siguiente reunión con Rubén es el 23 de septiembre de 2026 a las 11.

1. **El 1.14 en una IES sin función de investigación** (Normales, privadas pequeñas con RVOE solo docentes, Universidades para el Bienestar): con [[adr-0017]] un «No» vale 0; ¿se mantiene para el 1.14 o esa IES queda fuera del promedio? Argumento a favor del 0: excluirlo mejora a esas IES frente a las que investigan poco. Único candidato a «no aplica» que dejó el análisis de los 41 observables.
2. **Unidad de análisis en IES no autónomas** (campus del TecNM, Normales, unidades de la UPN): ¿responde el campus por sí mismo, contestando «No» donde no tiene la palanca (presupuesto etiquetado, promoción docente, licencias laborales, perfiles de puesto), o reporta la normatividad de su sistema?
3. Heredado de task-135: si el alcance sectorial es obligatorio (lo tienen 35 de 41; sin ella 1.1, 1.12, 1.14, 1.15, 4.1, 4.7); el 1.12 sin pregunta B; simular calificaciones antes de fijar la ponderación (pesos propios siguen nulos, [[task-15]]).
4. Para cuando exista cálculo: las reglas 0/0 (especial del 1.14 con cero proyectos; parte administrativa de B con cero instancias) y la herencia gen → cp de los denominadores (`is_present`, `no_apply`).
5. **Ritmo de aprobación de generales, condición de la apertura del 25.** En la copia de producción del 22 de septiembre, 0 de 66 paquetes de generales están en `gen_finished` (51 `gen_draft`, 14 `gen_sent`, 1 `gen_need_changes`). Con [[adr-0018]], ninguna IES captura cp hasta que la revisión finalice su información base, aunque la fecha haya pasado; sin un ritmo de revisión acordado, la apertura del 25 no abre nada ([[task-163]]).

## Criterios de aceptación

- [x] Respuesta de Rubén sobre el 1.14 registrada
- [ ] Unidad de análisis en IES no autónomas decidida y registrada
- [ ] Alcance obligatorio, 1.12 y simulación de calificaciones acordados o agendados
- [ ] Ritmo de aprobación de generales acordado de cara a la apertura del 25

## Reunión con Rubén, 2026-09-23

Fuente: [[2026-09-23-reunion-ruben]].

**Punto 1, respondido: el 1.14 se queda sin «no aplica».** Rubén, `[28:06]`–`[28:16]`: «¿si nos dicen que no tienen la información…? […] hay algún número de indicadores que luego no tienen la información». Ricardo, `[28:14]`: «¿Cómo?»; `[28:24]`: «es solo la 1.14 […] ¿funciona el no aplica? Yo digo que la respuesta no, pues es ausencia: todas las IES deberían tener investigación». Rubén, `[29:02]`: «Es un debate […] Lo que hemos hecho hasta ahora es que le pongan, y pues les baja la puntuación; por lo general eso le afecta a instituciones que no tienen área 3 de conocimiento, o área social». Ricardo, `[29:46]`–`[29:58]`: «Yo digo que lo dejamos en sí, ¿no?» (duda T5 de la limpia). Rubén, `[30:02]`, su criterio para el no aplica: «cuando la metodología se hizo de una forma que afecta a alguien que no tiene algo, pero se entiende, es razonable que no lo tenga» (su ejemplo: una política para menores de 18 años en una instancia de posgrado). Ricardo, `[30:51]`: «Aquí yo creo que a nivel de observable no». Rubén, `[31:22]`: «siempre que hay un no aplica también tenemos que tomar una decisión metodológica: por ejemplo, se descuenta del promedio […] Bueno, dejémoslo así por ahora, dejémoslo así». Ricardo, `[32:00]`: «si contestan no aplica tendríamos que promediar con un componente menos, y eso complica muchas cosas». Rubén, `[32:49]`: la pregunta «está bastante amplio para quienes no se dedican a estudios sociales» (grupos académicos para igualdad y no discriminación, aun en un área de física). Ricardo, `[33:28]`: «Sí, yo creo que sí aplica». Confirma [[adr-0017]] para el 1.14: el «No» vale cero.

**Punto 3, conversado sin cerrar.** El 1.12 sin transversalidad orgánica y los planes de estudio como transversalidad curricular, `[44:47]`–`[48:56]`: detalle en [[task-173]] punto (b). La simulación: Rubén, `[1:16:52]`, propone «hacer algunos casos para ver cómo se comportaría el índice», y `[1:17:33]`, «lo resolvemos la próxima» ([[task-173]] punto c). Del alcance sectorial obligatorio solo quedó que no todos lo tienen: Ricardo, `[41:23]`, «no todas tienen transversalidad sectorial»; Rubén, `[41:37]`, «eso no va a tener, porque es una pregunta enfocada en un solo sector, como formación docente».

**Punto 5, un dato de Rubén.** `[37:59]`: «funcionó un montón que dimos fecha límite para el viernes para subir la información base: yo creo que como el 60 % de las IES ya subieron la información»; Ricardo, `[38:25]`: «Perfecto, genial»; Rubén, `[38:30]`: «Nos está funcionando mucho esa estrategia». Es el envío de las IES, no el ritmo de revisión: el ritmo de aprobación de generales no se acordó.

Los puntos 2 y 4 no se tocaron.
