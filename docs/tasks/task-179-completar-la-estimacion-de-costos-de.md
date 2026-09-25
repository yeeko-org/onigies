---
type: task
id: task-179
title: "Completar la estimación de costos de ONIGIES: declarar el trabajo sin huella"
state: open
date: 2026-09-25
owner: ricardo
parent: "[[task-154|cuadre de pagos con la CIGU]]"
related: ["[[estado-administrativo-y-de-pagos]]", "[[2026-09-25-conceptualizacion-en-miro]]", "[[2026-09-25-estimacion-costos-onigies]]"]
---

# Completar la estimación de costos de ONIGIES: declarar el trabajo sin huella

Pendientes del lado de Ricardo para cerrar la estimación de costos propia de ONIGIES, que alimenta el cuadre de pagos de [[task-154]]. La estimación ya está en [[2026-09-25-estimacion-costos-onigies]]: unos 156,800 MXN de costo real contra 86,206.90 cobrados, sin contar el trabajo que no dejó huella. Lo que falta es lo que solo Ricardo sabe.

- Las seis reuniones grabadas ya llevan `offline_minutes` (362 min) y la conceptualización en Miró está en [[2026-09-25-conceptualizacion-en-miro]] (360 min, estimado, sin fecha; se tarificó a 850 suponiendo que fue antes de marzo).
- ⚠️ Dos días del periodo ciego se dejaron fuera por ambiguos: el 2026-06-30 y el 07-02 (un puente SSH a la UNAM con la llave de soporte de STIG, ~1 h). Si fueron de ONIGIES, se suman.
- ⚠️ La tabla de extras es hipótesis sacada de títulos y prompts: confirmar qué fue pedido por Rubén fuera de la cotización.
- ⚠️ Cuatro decisiones de método que el record deja abiertas, cada una marcada ahí como suya: el «% entregado» por renglón (hoy supuesto: ~100 % lo pagado, ~0 % lo pendiente; él mismo dijo el 4 de septiembre que «todavía falta una parte potente de las BP y falta la página pública»), la lectura de la cláusula de soporte (deploys, incidentes y puentes: ¿proyecto, dentro de lo cotizado o el puente nginx como «Modificación de versión 1»?), los primeros días de marzo (1.4 h por historial contra 7.1 h por git; usar git contradice el método) y los costos de terceros.

## Criterios de aceptación

- [ ] Declarar con offline_minutes el trabajo sin huella: reuniones de metodología de octubre a diciembre de 2025, análisis de la base de datos, preparación de las cotizaciones
- [ ] Confirmar la fecha de Miró, los días 06-30 y 07-02 y la tabla de extras
- [ ] Confirmar si los 80,000 comprometidos para 2026 incluyen IVA
- [ ] Confirmar el «% entregado» de cada renglón de la cotización, en particular buenas prácticas, plataforma pública y «Cálculo de indicadores y ponderaciones»
- [ ] Decidir cómo se leen los 18 meses de soporte: (a) deploys e incidentes de la construcción son proyecto y los puentes S3/nginx un extra; (b) todo dentro de lo cotizado; (c) el puente nginx al renglón «Modificación de versión 1 para compatibilidad»
- [ ] Decidir si los días de principios de marzo con commits (03-02, 03-03, 03-09) se estiman por git en vez de por historial, como desviación declarada del método
- [ ] Declarar los costos de terceros: quién paga y cuánto cuestan el servidor de Yeeko, el bucket S3 `onigies-v3-temporal` y Netlify
- [ ] Revisar las cuatro tarjetas de memoria de Windows (email-smtp-microsoft365, feedback_docstrings_es, feedback_minimal_queryset, email.md): fase 3 de migrate-session-logs
