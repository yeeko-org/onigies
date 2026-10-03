---
type: task
id: task-193
title: Bloqueo del periodo cerrado en bp también en el servidor
state: open
date: 2026-10-02
owner: ai
parent: "[[task-6]]"
source: ["[[2026-10-02-comentarios-editables-y-valvula-de-admin]]"]
related: ["[[task-190]]"]
---

# Bloqueo del periodo cerrado en bp también en el servidor

Hoy el periodo cerrado solo lo bloquea el cliente en bp: `GoodPracticeList.vue` lo admite en un comentario («el backend no lo bloquea en /good_practice/»). Desde el 2026-10-02 los dos viewsets de bp pasan por `PracticeContentWriteMixin`, que surge los mensajes de `content_lock_errors` de la raíz; bastaría un `GoodPracticePackage.content_lock_errors(user)` que devuelva el mensaje de periodo cerrado a la IES no de prueba, como hace `AxisValue` en cp, para que el servidor lo aplique sin más cambios.

## Criterios de aceptación

- [ ] Con el periodo cerrado, una IES real recibe 403 al escribir contenido de bp por API; una institución «De prueba» sigue pudiendo
- [ ] El mensaje del 403 es el mismo que muestra la UI
