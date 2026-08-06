---
type: task
id: task-93
title: Decidir los pendientes de la sesión de adjuntos y campos numéricos
state: open
date: 2026-08-06
owner: ricardo
source: ["[[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]]"]
related: ["[[task-67]]", "[[task-68]]", "[[task-55]]"]
---

# Decidir los pendientes de la sesión de adjuntos y campos numéricos

Batch de decisiones que quedaron abiertas al cierre de la sesión duo del 6 de agosto — Ricardo tuvo que salir. El contexto completo de cada una está en la bitácora [[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]] y el análisis UX de la señal numérica vive resumido en [[task-67]]. Ninguna bloquea lo ya construido: son afinaciones sobre el stack de adjuntos ([[adr-0010]]) y la decisión de UX de [[task-67]].

## Criterios de aceptación

- [ ] task-67: elegida la señal del campo numérico — recomendación: ícono `123` en prepend-inner + `inputmode="numeric"` + texto sr-only con aria-describedby; alternativa: placeholder «p. ej. 1250» con persistent-placeholder (ver con etiquetas largas)
- [ ] task-67 anexas: ¿migrar los dos años de BP (`GoodPracticeEditSimple`) a `GeneralNumberInput` para unificar el idioma numérico? ¿agregar retroalimentación al rechazo mudo al teclear letras, o queda fuera?
- [ ] Candado de periodo en adjuntos: hoy, con periodo cerrado pero paquete sin enviar, la IES aún puede adjuntar (consistente con el PATCH del Survey, que tampoco valida periodo — [[task-55]]). ¿Se cierra junto con task-55 o antes?
- [ ] Validación de archivo en la subida: hoy sin límite de tamaño ni de tipo (paridad con el viejo). ¿Se define uno?
- [ ] Borrado físico: el DELETE borra el registro, no el archivo del storage (paridad con el viejo). ¿Se queda así?
- [ ] Menores con default por paridad (revertibles con avisar): la tarjeta de BP cuenta solo adjuntos de la práctica, sin sumar los de características; `mainStore.saveFile` muerto se borra en [[task-7]]
