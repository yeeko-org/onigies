---
type: task
id: task-120
title: Sembrar el rótulo de la persona titular como GeneralQuestion
state: open
date: 2026-08-12
owner: ai
parent: "[[task-101]]"
source: ["[[2026-08-12-sesion-orquestada-a-b-captura-correcta]]"]
related: ["[[task-113]]", "[[task-107]]"]
---

# Sembrar el rótulo de la persona titular como GeneralQuestion

Al extirpar los textos hardcodeados ([[task-113]]) quedó uno a sabiendas: «La persona titular de la institución es:» en `GeneralAuthorities.vue`. No es texto introductorio de grupo sino rótulo de pregunta, y el grupo `autoridades` se sembró sin preguntas. Si el equipo de Rubén debe poder editarlo — que es el espíritu de [[task-107]]/[[task-108]] —, hay que sembrarlo como `GeneralQuestion` del grupo (probablemente sin mapeo a columna: la titular persiste como fila de `PopulationQuantity` de total 1) y que el componente lo lea del catálogo.

Decidir al tomarla si el radio de la titular amerita su propio `q_type` o si basta un name sin columna con render custom — misma familia de excepción que `is_centralized`.

## Criterios de aceptación

- [ ] El rótulo de la titular vive en el catálogo y es editable desde el dashboard
- [ ] `GeneralAuthorities.vue` no tiene textos de pregunta en código
