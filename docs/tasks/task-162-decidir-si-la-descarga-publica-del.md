---
type: task
id: task-162
title: Decidir si la descarga pública del Word se cachea
state: open
date: 2026-09-22
owner: ricardo
parent: "[[task-2]]"
related: ["[[task-150]]", "[[task-151]]"]
---

# Decidir si la descarga pública del Word se cachea

Prioridad baja. Propuesta del cierre del 2026-09-22.

La descarga pública `GET /api/public-documents/cuestionario-2026/download/` regenera el Word de 1.9 MB en cada petición (unos 0.3 s y 13 consultas en local), sin caché, en el servidor de Yeeko que comparten unos veinte clientes. Es anónima: cualquiera puede pedirla en bucle.

Opciones:

- **Cachear** el archivo generado con llave en la fecha de última modificación del cuestionario (se regenera solo cuando cambian los textos). Cuesta decidir qué cuenta como «modificación» —observables, preguntas, grupos de información de base, notas— y guardar el archivo (disco o S3).
- **Aceptar** el costo actual: el tráfico esperado es bajo (las IES y el equipo de la CIGU) y la generación es barata.

## Criterios de aceptación

- [ ] Ricardo eligió entre cachear y aceptar
