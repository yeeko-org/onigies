---
type: task
id: task-157
title: Barrido crítico del cuestionario cuando Rubén avise que terminó sus correcciones
state: open
date: 2026-09-11
owner: ai
parent: "[[task-2]]"
related: ["[[2026-09-04-reunion-con-ruben]]", "[[task-116]]", "[[fb-2]]"]
---

# Barrido crítico del cuestionario cuando Rubén avise que terminó sus correcciones

**Bloqueada hasta que Rubén avise que terminó de corregir el cuestionario desde el dashboard.** Antes de eso el barrido leería un texto que todavía se mueve, y habría que repetirlo.

El barrido lee **el contenido de producción**, no el seed: el seed quedó retirado tras la última siembra del 2026-09-10 ([[task-139]]) y desde entonces el dashboard es la única fuente del instrumento, así que cualquier corrección de Rubén solo existe en la base.

Qué busca: cualquier otro error importante que la revisión humana no atrapa —preguntas copiadas de otro observable y nunca ajustadas, títulos duplicados o distintos entre la lista de verificación y el cuestionario, grafías inconsistentes del mismo término, signos de apertura «¿» faltantes—.

Por qué hace falta, y por qué lo hace el asistente y no Rubén: `[18:08]` «yo no reviso esas preguntas porque, como son idénticas en estructura —no en contenido—, siempre que reviso nada más reviso lo que es diferente. Pero por eso se fue, justamente». Es una estrategia de revisión racional frente a 41 observables casi iguales, y es exactamente por donde se cuelan los copy-paste; los dos hallazgos de este tipo que ya se conocen salieron de un barrido programático, no de leer.

[[task-116]] es la lista de lo ya conocido —las correcciones que Rubén se llevó de la reunión del 2026-09-04—: este barrido busca lo que **no** está ahí, y sirve además para verificar que lo que sí está quedó aplicado.

Pendientes ya conocidos que no van en esa lista y que este barrido debe comprobar:

- El punto C.3 del documento de correcciones ([[2026-09-04-correcciones-de-redaccion-del-instrumento]], tú/usted) proponía «usted», y la reunión resolvió «tú» para los mensajes de la plataforma (`[56:52]`); si Rubén aplicó el documento al pie de la letra, lo aplicó al revés. Ver [[task-156]].

## Criterios de aceptación

- [ ] Rubén avisó que terminó sus correcciones
- [ ] El barrido corrió sobre el contenido de producción, no sobre el seed
- [ ] Los hallazgos nuevos quedaron en un documento que Rubén pueda recorrer, o se cerró declarando que no hubo ninguno
