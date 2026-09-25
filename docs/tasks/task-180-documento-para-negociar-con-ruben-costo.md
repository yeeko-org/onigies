---
type: task
id: task-180
title: "Documento para negociar con Rubén: costo real, extras pedidos y compensación con lo pendiente"
state: open
date: 2026-09-25
owner: ricardo
parent: "[[task-154|cuadre de pagos con la CIGU]]"
related: ["[[2026-09-25-estimacion-costos-onigies]]", "[[adr-0022]]", "[[adr-0021]]", "[[task-179]]", "[[estado-administrativo-y-de-pagos]]"]
---

# Documento para negociar con Rubén: costo real, extras pedidos y compensación con lo pendiente

Ricardo lo pidió la noche del 25 de septiembre de 2026, al cerrar la estimación de costos ([[2026-09-25-estimacion-costos-onigies]]): «Hay que construir un documento o una tarea para mí que ayude a plantear las condiciones y exponer los costos reales, los estimados, etc.». El record es primero para él; este documento es lo que se adapta para Rubén.

## Lo que ya está resuelto y el documento solo tiene que exponer

- **Punto de partida de Ricardo:** todo lo cotizado se le va a pagar. La pregunta no es cuánto falta cobrar por contrato, sino cuánto más ha trabajado y cómo se compensa.
- **Criterios de cobro** ([[adr-0022]]): lo pedido que se excedió se cobra (~29,800 a hoy, ~35,300 con buenas prácticas terminada); lo no planeado (~62,200) se factura prorrateado; las reuniones se cuentan como costo no planeado, prorrateado. Pendiente de Ricardo ([[task-179]]): si la cláusula de soporte de 18 meses cubre o no los deploys de la construcción — Rubén podría leerla así.
- **El desborde a hoy:** unos 75,000 netos contra los 88,000 de 2025.
- **Lo pendiente cabe con margen:** 233,000 cotizados contra 138,000–208,000 estimados con IA y el harness, incluidas la máquina virtual y la reserva de coordinación. Margen de 22,400 a 92,400, ya descontados los 2,600 de identidad gráfica gastados a cuenta.
- **Lo histórico se conecta por liga** ([[adr-0021]]); si Rubén quisiera la integración total, se cotiza aparte.
- **La identidad gráfica ya existe**, hecha con Claude Design, y gustó mucho al mostrarla ([[2026-09-25-identidad-grafica-en-claude-design]]). Es un buen gancho para abrir la conversación: el renglón de 16,000 está casi resuelto.
- **La ponderación del índice** se cierra con ≈3 h de reunión con Rubén más ≈3 h de Ricardo ([[task-28]], [[task-29]]); después el cálculo lo hace el asistente en 2–3 h.

## La propuesta de informes, como moneda de cambio

El renglón de informes (81,000) promete PDFs terminados por institución, con diseño editorial, vista editable en el dashboard y redacciones por nivel de avance. Ricardo lo ve así:

> A estas alturas, Opus 5.5 (o algo más avanzado cuando se haga) pueden resolver los informes uno a uno con muchísima precisión. Acá puedo ponerme perro en exigir un par de templates completos hechos por ellos y acá los adaptamos en corto. La otra solución es un skill tipo lo que hice para Paola en el proyecto OCSA. Veo que puede ser muy eficiente de esa manera. Dejarles la herramienta y que ellos la ajusten. Puede ser un acuerdo a buscar con Rubén para compensar los mega costos que hemos tenido hasta ahora.

El precedente de OCSA: el kit de Paola fue una carpeta con un `CLAUDE.md` que hace preguntas aclaratorias antes de consultar, referencias del esquema y ejemplos; con él ella exploró los datos y escribió su propio informe. Ricardo: «Funcionó todo integrado, pero sobre todo las aclaraciones y las referencias». En OCSA ese renglón pasó de 12,000 cotizados a 32,000 cobrados. Para ONIGIES habría que decidir con Rubén qué herramienta usaría el equipo de la CIGU y si tendría acceso de solo lectura a la base. Las «descripciones de cada nivel de avance» que la cotización promete todavía no existen en ningún lado. Los informes multianuales necesitan varios años de datos: calendarizarlos para 2027 o después. Rubén ya los ubicó en 2027 ([[2026-09-23-reunion-ruben]], `[03:06]`), y Ricardo no quiere task del módulo hasta que se la pidan: esta task prepara la conversación, no la construcción.

## Criterios de aceptación

- [ ] Exponer el costo real contra lo cotizado de los renglones pagados en 2025 (unos 163,000 contra 88,000) con la tabla de la brecha por concepto
- [ ] Presentar los extras pedidos con su causa y su evidencia: excedente de buenas prácticas, editor del cuestionario, invitaciones (con el argumento contra el texto del link con token), institución de prueba y exportación a Word
- [ ] Presentar los costos no planeados y cómo se prorratean, sin presentarlos como deuda del cliente
- [ ] Exponer la estimación honesta de lo pendiente de 2026 (138,000–208,000 contra 233,000) y el margen que deja (22,400–92,400)
- [ ] Proponer los informes con plantillas completas del cliente o con un kit como el de OCSA, como moneda de cambio para compensar el desborde
- [ ] Poner precio a la instalación y los trámites de la máquina virtual de la UNAM y a una reserva de coordinación
- [ ] Decidir qué parte llega a Rubén y en qué forma, y adaptar el documento
