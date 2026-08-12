---
type: task
id: task-115
title: "Endurecimiento del servidor actual: DEBUG y CORS"
state: open
date: 2026-08-11
owner: ai
parent: "[[task-4]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
related: ["[[task-100]]"]
---

# Endurecimiento del servidor actual: DEBUG y CORS

Rescate de dos puntos que hasta hoy solo vivían en el roadmap del skill `deployment`, en su fase de endurecimiento, sin task que los reclamara. **Aplican al servidor de hoy**, antes y con independencia de la migración a la UNAM ([[task-100]]): no hay razón para esperar a mudarse para cerrarlos, y sí para no esperar — la sección de información base se abre a las IES esta semana.

- **CORS:** la configuración de producción acepta cualquier origen. Hay que sustituirlo por una lista explícita de orígenes permitidos, ahora que la topología está estable: el frontend en Netlify puenteado sobre el dominio de la UNAM, y el API en el servidor de Yeeko.
- **DEBUG:** producción corre hoy con el modo de depuración encendido. Apagarlo, y revisar de paso la lista de hosts permitidos.

**Ejecutar después del jueves 13.** Aunque sea independiente de la migración, apagar el modo de depuración en producción es de los cambios que rompen cosas en silencio, y el jueves se abre la sección de información base a todas las IES. No se arriesga la ventana de apertura por un endurecimiento que puede esperar unos días.

Al apagar el modo de depuración conviene verificar que los archivos subidos se siguen sirviendo. La ruta de los archivos se declaró explícita justamente para sobrevivir a este cambio, pero es lo primero que hay que comprobar después de tocarlo.

## Criterios de aceptación

- [ ] Producción corre con el modo de depuración apagado
- [ ] CORS usa una lista explícita de orígenes permitidos, no el comodín
- [ ] La lista de hosts permitidos está revisada para el host de producción
- [ ] Los archivos subidos se siguen sirviendo tras el cambio
