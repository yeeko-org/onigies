---
type: record
id: 2026-08-20-revision-de-piloto-automatico-y-retiro
date: 2026-08-20
---

# Revisión de los commits de piloto automático y retiro de la superficie de status

Sesión del 20 de agosto de 2026, coordinada en modo duo. Nace de la revisión que Ricardo hizo de los tres commits de la sesión en piloto automático del 19 de agosto (673dd34, 1b968fa, dc72a96) y termina con una decisión de producto ejecutada y el borrado de StatusControl listo para su propia sesión.

## La dinámica de marcadores, estrenada

Ricardo dejó sus dudas en el código con el prefijo `TO-AI:` (6 comentarios) y sus mini-encargos con `AI-TASK:` (3). Todos se aclararon en diálogo y se resolvieron; la convención quedó establecida —detonado el diálogo de aclaración, los `TO-AI` se borran— y capturada con propuesta de estandarización en [[learning-8]], junto al `TO-RICK:` propuesto en [[learning-1]] y al skill de piloto automático de [[learning-2]].

## Resoluciones de código

- **Identidad de paneles por pk**: los `PanelCommon` declaran `value` con la pk de la fila y `open_panels` guarda pks, no índices (decisión de Ricardo sobre las dos alternativas; el fix por índices se descartó a media sesión). Cobertura e2e pendiente en [[task-130]].
- **`statusGroupLabel`**: se unificó el rótulo de status de `StatusDetail` y el snackbar de `EditCommon`… y quedó anulado horas después por el retiro de esa misma superficie. Muere del todo en [[task-7]].
- **Ctrl+click roto hacia `patchCatalog`**: diagnóstico de índice viciado del IDE, sin cambio de código; quedó como [[task-129]] con la prueba de falsación pendiente.
- Tasks abiertas de la revisión: [[task-126]] (extender JSDoc), [[task-128]] (generar la capa de tipos desde `ps_schema`).

## StatusControl: inventario y retiro adelantado

La pregunta de Ricardo —¿algo usa StatusControl de verdad?— produjo el inventario completo en [[2026-08-20-inventario-de-usos-vivos-de-statuscontrol]]: cero funcionalidad de flujo depende de él; el §8 del diseño está desbloqueado desde el 12 de agosto y nadie lo había ejecutado.

Decisiones de Ricardo de hoy: **(1)** la superficie visible de «Status de Envío» del dashboard se retiró en esta misma sesión —select del detalle de edición, filtro de barra, select de edición masiva—; el hallazgo que la remató es que el select de edición masiva apuntaba a un handler inexistente y jamás pudo montarse, porque ninguna colección enciende `can_massive_edit` (insumo anotado en la task global de inventario del motor). **(2)** [[task-7]] (el borrado completo) se ejecuta en una sesión propia, no en esta. **(3)** El deploy de lo hecho hoy va en la siguiente sesión, antes de task-7.

## El episodio de alcances y la colisión de tasks

Tres nodos nacieron en el grafo del proyecto cuando su alcance era global; se reubicaron (las dos ideas como learnings `scope: global`, la task cross-proyecto al grafo global). De la mudanza se quemó el id `task-127` ([[learning-4]]) y el barrido que no miró el grafo global dejó la task ciega a la `task-43` global que ya cubría lo mismo ([[learning-6]]); la resolución fue subordinarla como su fase de inventario. El learning de la regla de alcance se descartó y se borró del disco a petición expresa de Ricardo («es un learning para mí que ya incorporé»). Los bugs de tooling encontrados de paso quedaron como tasks globales (los `\n` literales de `learn --body`).

## Deuda de verificación

Nada automatizado ejercita los cambios de hoy (la suite e2e no toca el dashboard administrativo — hallazgo registrado en [[task-130]]). La aceptación es la pasada manual de Ricardo antes del commit: borrar filas con paneles abiertos y confirmar que la superficie de status ya no se ofrece.
