---
type: task
id: task-179
title: "Completar la estimación de costos de ONIGIES: declarar el trabajo sin huella"
state: open
date: 2026-09-25
owner: ricardo
parent: "[[task-154|cuadre de pagos con la CIGU]]"
related: ["[[estado-administrativo-y-de-pagos]]", "[[2026-09-25-conceptualizacion-en-miro]]", "[[2026-09-25-estimacion-costos-onigies]]", "[[task-180]]", "[[adr-0022]]"]
---

# Completar la estimación de costos de ONIGIES: declarar el trabajo sin huella

Pendientes del lado de Ricardo para cerrar la estimación de costos propia de ONIGIES ([[2026-09-25-estimacion-costos-onigies]]), que alimenta el cuadre de pagos de [[task-154]] y la negociación de [[task-180]]. Hoy: unos 163,000 MXN de costo real por lo hecho contra los 88,000 de los renglones pagados en 2025, más 2,600 de adelanto de identidad gráfica.

## Resuelto la noche del 25 de septiembre

Ricardo, en diálogo con el coordinador:

- **Declarado:** 8 h de reuniones sin grabación y 8 h de análisis y construcción de la base de datos, las dos antes de marzo, a 850 ([[2026-09-25-reuniones-sin-grabacion]], [[2026-09-25-analisis-y-construccion-de-la-base]]); 2 h de identidad gráfica en Claude Design, a 1,300 ([[2026-09-25-identidad-grafica-en-claude-design]]). La conceptualización en Miró (6 h) va al flujo de validación.
- **% entregado:** cuestionario por observable 85 %, flujo de validación 95 %; los demás como estaban (poblaciones ~95 %, buenas prácticas ~80 %, base de datos 100 %).
- **Extras:** se cobra lo pedido que se excedió —excedente de buenas prácticas, editor del cuestionario, invitaciones de las IES, institución de prueba, exportación a Word—; lo no planeado se registra y se factura prorrateado; las reuniones se cuentan como costo no planeado, prorrateado ([[adr-0022]]). Con eso queda resuelta la tabla de extras. De la cláusula de soporte Ricardo no dijo nada: dijo que los deploys son costo no planeado («igual que lo de los deploys»); que la cláusula de 18 meses no los absorba frente a Rubén es lectura de la estimación, pendiente abajo.

## Criterios de aceptación

- [x] Declarar con offline_minutes las reuniones sin grabación anteriores a marzo de 2026 y el análisis de la base de datos
- [x] Confirmar el «% entregado» de los renglones pagados
- [x] Confirmar qué extras se cobran
- [ ] Declarar la preparación de las dos cotizaciones y del informe de actividades de diciembre de 2025, si Ricardo quiere sumarla
- [ ] Confirmar la fecha de Miró (hoy tarificada a 850, suponiendo que fue antes de marzo; después, sube 2,700)
- [ ] Decidir si el 2026-06-30 y el 07-02 (~1 h, un puente SSH a la UNAM con la llave de soporte de STIG) fueron de ONIGIES
- [ ] Confirmar si los 80,000 comprometidos para 2026 incluyen IVA
- [ ] Confirmar la lectura de la cláusula de soporte de 18 meses: ¿«igual que lo de los deploys» significa que la cláusula no cubre los deploys ni los puentes de la construcción? Opciones del record: (a) extra por «necesario para operar», (b) dentro de lo cotizado, (c) el puente nginx a «Modificación de versión 1»
- [ ] Decidir si el trabajo de pesos de `QuestionType` pertenece a «Cálculo de indicadores y ponderaciones» (5,000) en vez de al editor del cuestionario
- [ ] Decidir si el puente nginx hacia Netlify se asigna al renglón «Modificación de versión 1 para compatibilidad» (3,000) en vez de a infraestructura
- [ ] Decidir si los días de principios de marzo con commits (03-02, 03-03, 03-09) se estiman por git (6.7 h) en vez de por historial (1.3 h), como desviación declarada del método
- [ ] Declarar los costos de terceros: quién paga y cuánto cuestan el servidor de Yeeko, el bucket S3 `onigies-v3-temporal` y Netlify
- [ ] Decidir si los puertos de OCSA (colecciones, `ps_schema`, catálogos) y la preparación de Fedora, 5.3 h y unos 5,800 MXN, son inversión propia y salen del costo
- [ ] Revisar las fracciones facturables de las sesiones mixtas, que son estimaciones de lectura: `803fabce` 40 %, `b6c8a4f0` 80 %, `6635e96d` 50 %, `b055612f` 90 %
- [ ] Revisar las cuatro tarjetas de memoria de Windows (email-smtp-microsoft365, feedback_docstrings_es, feedback_minimal_queryset, email.md): fase 3 de migrate-session-logs
