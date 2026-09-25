---
type: decision
id: adr-0021
title: Lo histórico del ONIGIES original se conecta por liga, no se integra al sistema nuevo
state: accepted
date: 2026-09-25
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-09-25-estimacion-costos-onigies]]", "[[2026-01-07-cotizacion-plataforma-v3]]"]
affects: ["docs/records/2026-09-25-estimacion-costos-onigies.md"]
related: ["[[task-100]]", "[[task-180]]"]
---

# Lo histórico del ONIGIES original se conecta por liga, no se integra al sistema nuevo

## Contexto y planteamiento del problema

La cotización de 2026 ([[2026-01-07-cotizacion-plataforma-v3]]) trae tres piezas que tocan la información de años anteriores: «Registro histórico» (varios años de información, distinguiendo el año que se ve o se registra), el renglón «Despliegue histórico de información» (4,000) dentro de visualizaciones, y «Modificación de versión 1 para compatibilidad» (3,000), que pide que la versión anterior tenga «un subdominio o una ruta URL específica para distinguir la versión previa y la nueva». Los datos de 2017–2018 viven en el ONIGIES original (Python 2 + Vue 2), que sigue sirviendo el sitio público y no está en este repo.

Al estimar lo que falta, el 25 de septiembre de 2026, el coordinador señaló que migrar esos datos al modelo nuevo sería un trabajo propio que hoy no tiene renglón y que probablemente cuesta más que la gráfica misma. Ricardo confirmó que lo histórico está incluido en lo cotizado y que el costo sería real, pero se opuso a la integración total:

> Sí lo incluye y tienes razón, pero tengo que oponerme a que sea una integración total, lo pensé como una liga a lo histórico, no a ponerlo junto.

## Criterios de decisión

- No abrir un proyecto de migración de datos de una metodología anterior (14 indicadores) a la nueva (41 observables), según la propia cotización de 2026, que ninguna cotización pagó.
- Mantener el costo de «Despliegue histórico» y de «Modificación de versión 1» dentro de su precio.
- Que la información vieja siga consultable.

## Opciones consideradas

- **Integración total**: migrar los datos de 2017–2018 al modelo nuevo y mostrarlos junto a los actuales.
- **Liga a lo histórico**: el sistema nuevo enlaza al sitio viejo (o a su ruta o subdominio propio) para los años anteriores, sin mezclar los datos.

## Resultado

Se eligió **la liga a lo histórico**, porque así es como Ricardo lo pensó al cotizar y porque la integración total sería un proyecto aparte sin precio.

### Consecuencias

- **Bueno:** «Despliegue histórico» y «Modificación de versión 1» quedan en horas chicas (2–3 h la segunda, en la estimación del 25 de septiembre); la versión vieja sigue viva en su propia ruta.
- **Malo:** los años viejos no se comparan en las mismas gráficas que los nuevos; quien quiera ver la evolución completa salta entre dos sitios. Lo histórico que sí se integra es el que nazca en el sistema nuevo, año con año.

### Cómo se comprueba

El sitio público nuevo tiene una liga visible a la versión anterior, y los datos de 2017–2018 no se muestran junto a los nuevos en las mismas vistas.

## Más información

Surgió en el diálogo de la estimación de costos del 25 de septiembre de 2026 ([[2026-09-25-estimacion-costos-onigies]], sección «Lo que falta»). El traslado de la infraestructura a la UNAM vive en [[task-100]]. Si Rubén pidiera la integración total, se cotiza aparte ([[task-180]]).
