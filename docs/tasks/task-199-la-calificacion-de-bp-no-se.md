---
type: task
id: task-199
title: "La calificación de bp no se bloquea por turno: una revisora puede recalificar un envío finalizado"
state: open
date: 2026-10-02
owner: ricardo
parent: "[[task-6]]"
related: ["[[adr-0026]]", "[[task-70]]"]
---

# La calificación de bp no se bloquea por turno: una revisora puede recalificar un envío finalizado

La nota privada por criterio (`FeatureGoodPractice.comments`) quedó bajo turno de la raíz ([[task-70]]), pero `final_option` del criterio y `final_value` de la práctica no: `PracticeContentWriteMixin` exime a la revisión del candado de contenido y solo le limita los campos. Una revisora puede recalificar con el envío en `bp_finished` o de vuelta en la IES. Lo señaló el crítico del 2026-10-02 y nunca se le planteó a Ricardo. Decidir si la calificación sigue la misma regla de turno que la nota (lo natural) o se deja libre como válvula de corrección.

## Criterios de aceptación

- [ ] Ricardo decidió si la calificación se bloquea por turno
- [ ] Si se bloquea: candado en `FeatureGoodPracticeSerializer.validate` y en el de práctica, con tests
