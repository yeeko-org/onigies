---
type: decision
id: adr-0022
title: Lo pedido que se excede se cobra; lo no planeado —reuniones incluidas— se registra y se factura prorrateado
state: accepted
date: 2026-09-25
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-09-25-estimacion-costos-onigies]]"]
affects: ["docs/records/2026-09-25-estimacion-costos-onigies.md", "docs/reference/estado-administrativo-y-de-pagos.md"]
related: ["[[task-154]]", "[[task-179]]", "[[task-180]]", "[[estado-administrativo-y-de-pagos]]"]
---

# Lo pedido que se excede se cobra; lo no planeado —reuniones incluidas— se registra y se factura prorrateado

## Contexto y planteamiento del problema

La estimación de costos del 25 de septiembre de 2026 ([[2026-09-25-estimacion-costos-onigies]]) midió que el trabajo hecho en ONIGIES cuesta, a las tarifas de Ricardo (850 MXN/h antes del 2 de marzo de 2026, 1,300 después), unos 163,000 contra los 88,000 de los renglones pagados en 2025: un desborde neto de unos 75,000. Partido por causa, unos 29,800 son cosas que el cliente pidió y que excedieron lo cotizado, y unos 62,200 son trabajo que la cotización no previó: la base común del dashboard, la infraestructura y los deploys, las reuniones y su procesamiento.

Ricardo parte de que todo lo cotizado se le va a pagar; la pregunta no era cuánto falta cobrar por la regla contractual, sino qué se cobra aparte y cómo se trata lo que él no planeó.

## Criterios de decisión

- Cobrar lo que el cliente pidió y que ningún renglón pagaba.
- No ocultar el costo real de lo no planeado, pero tampoco presentarlo como «deuda» del cliente cuando el error fue de estimación.
- Que la próxima cotización aprenda de esto.

## Opciones consideradas

- **Cobrar solo la regla contractual** (cotizado × % entregado − cobrado): deja fuera todo lo pedido y todo lo no planeado.
- **Cobrar todo el desborde como extra**: presenta los errores de estimación propios como pedidos del cliente.
- **Separar por causa**: lo pedido se cobra; lo no planeado se registra y se factura repartido.

## Resultado

Se eligió **separar por causa**, en tres reglas que Ricardo fijó en el diálogo:

1. **Lo que pidieron y se excedió se cobra como extra.** Hoy: el excedente de buenas prácticas, el editor del cuestionario, las invitaciones de las IES («que me lo pidieron así»), la institución de prueba y la exportación a Word. Unos 29,800 a hoy, unos 35,300 con buenas prácticas terminada.
2. **Lo no planeado se registra para aprender y también se factura, prorrateado entre los demás renglones cuando sea posible.** En sus palabras sobre las transcripciones: «más que "por cobrar" serán costos adicionales que yo no planee bien, igual que lo de los deploys»; y después: «Se registra para aprender, pero también para facturar, pero prorrateado (cuando sea posible) entre los otros costos». Incluye la base del dashboard, la infraestructura y los deploys, las transcripciones y la planeación, y el exceso del diseño de la base de datos.
3. **Las reuniones se cuentan, como costo no planeado prorrateado (regla 2).** «Las reuniones normalmente no las cobro como concepto, pero sí debería»: las grabadas por su duración y las no grabadas por lo que Ricardo declare. Hacia adelante, Ricardo quiere que aparezcan listadas en la cotización.

### Consecuencias

- **Bueno:** la conversación con Rubén separa lo que él pidió de lo que Ricardo calculó mal, y lo segundo se recupera sin presentarlo como deuda. Los deploys de la construcción quedan como costo no planeado. Si la cláusula de soporte de 18 meses los cubre o no frente a Rubén no lo decidió Ricardo: sigue abierto en [[task-179]].
- **Malo:** prorratear exige un margen donde repartir. Hoy ese margen existe en lo pendiente de 2026 (visualizaciones e identidad; el margen del cuestionario es de 2025 y ya está descontado en el neto), pero si lo pendiente se desborda, lo no planeado se queda sin dónde caer.

### Cómo se comprueba

La estimación de costos clasifica cada concepto como «por cobrar» o «no planeado», y el documento de negociación ([[task-180]]) presenta los extras pedidos con su causa y su evidencia.

## Más información

Diálogo de la estimación de costos del 25 de septiembre de 2026; la cotización nueva debe llevar un renglón o una reserva para coordinación e infraestructura. Pendientes abiertos en [[task-179]].
