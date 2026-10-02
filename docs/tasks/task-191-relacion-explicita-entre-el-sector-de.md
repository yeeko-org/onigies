---
type: task
id: task-191
title: Relación explícita entre el sector de alumnado y su pregunta de planes de estudio
state: open
date: 2026-10-02
owner: ricardo
parent: "[[task-5]]"
source: ["[[2026-10-02-alta-del-nivel-tecnico-superior]]"]
related: ["[[adr-0024]]", "[[adr-0012]]"]
---

# Relación explícita entre el sector de alumnado y su pregunta de planes de estudio

Hoy los cuatro niveles de alumnado existen dos veces sin ligarse: como `Sector` en la tabla de poblaciones y como `GeneralQuestion` del grupo `planes_estudio`. Ningún código cruza la presencia declarada de un sector con la pregunta de planes de ese nivel: una IES puede decir «no atiendo medio superior» y aun así debe marcar «No aplica» en sus planes de medio superior, y nada avisa si reporta planes de un nivel que dijo no tener.

Ricardo preguntó si conviene un campo `sector` en la pregunta de planes para prohibir la contradicción desde el frontend. Lo dejó pendiente para platicarlo con Rubén con calma. La propuesta del modelo en la sesión del 2026-10-02:

- **Señal, no prohibición.** Un plan vigente sin matrícula (primera generación aún no entra) o alumnado remanente de un plan en extinción son casos reales; prohibir forzaría un dato falso donde el instrumento distingue con cuidado «cero», «sin dato» y «no existe» ([[adr-0012]]). Avisar lo convierte en algo que la IES o la revisora resuelven.
- **FK nullable `sector` en `GeneralQuestion`**, con selector en el catálogo, preferible a una llave en `addl_config`: es una relación consultable desde el ETL y `addl_config` guarda comportamiento, no referencias. Es migración de esquema.
- **Primer uso:** bajo la pregunta de planes, una línea cuando el sector ligado tiene `is_present=False` («Declaraste que no tienes alumnado de este nivel»), y el caso cruzado como aviso visible en la compuerta de completitud del grupo de planes, no como error.
- **Segundo uso, si Rubén lo quiere:** al marcar la presencia en «No», prellenar «No aplica» en los planes del mismo nivel, editable. Es decisión de medición suya.
- **Duda honesta:** si la señal nunca se vuelve regla, el FK sirve para una línea y un aviso, y una convención de nombres (`media_plans` ↔ «medio superior») lo lograría más barato pero frágil, porque el nombre del sector lo edita Rubén.

## Criterios de aceptación

- [ ] Rubén y Ricardo deciden si la relación existe y si es señal o regla
- [ ] Si existe: migración con el FK, los cuatro pares ligados por migración de datos, selector en el catálogo
- [ ] Si existe: el aviso cruzado en la UI y en la compuerta de planes, con su test
