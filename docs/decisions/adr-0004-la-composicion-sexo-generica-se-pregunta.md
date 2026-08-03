---
type: decision
id: adr-0004
title: La composición sexo-genérica se pregunta en Generales, no en el observable 1.7
state: accepted
date: 2026-07-04
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-07-04-seed-del-cuestionario]]"]
affects: ["api/question/seed_data/axis_1.py", "api/survey/models.py", "api/indicator/models.py"]
---

# La composición sexo-genérica se pregunta en Generales, no en el observable 1.7

## Contexto

El observable 1.7 (integración paritaria) trae un bloque adicional en el instrumento: «¿Cuál es la integración por sexo-género de las siguientes poblaciones de la IES?», con los diez sectores principales y, aparte, cuatro autoridades. Al modelar el seed había que decidir dónde se captura esa tabla.

## Opciones consideradas

- **Dentro del observable 1.7**, como su alcance poblacional, igual que en los demás observables. Uniforme con el resto del instrumento, pero convierte un dato de la institución en respuesta de un observable.
- **En «Información de base» (Generales)**, una sola vez por periodo, y que el observable la consuma para calcular su indicador.

## Resultado

Se captura en Generales: **la composición sexo-genérica es un dato institucional del periodo**, no una respuesta al observable. Aterriza en `PopulationQuantity`, que ya tenía `number_men`/`number_women`. Las cuatro autoridades se modelan como `Sector` con el flag nuevo `is_authority=True` — dos ya existían (Titular de la IES, Máximo cuerpo colegiado) y se agregaron «Titulares de instancias académicas» y «Titulares de instancias administrativas» — bajo un `GeneralGroup` nuevo, «autoridades». El indicador del 1.7 se calcula desde `PopulationQuantity` vía `pop_weight`, y el observable conserva únicamente su parte A.

### Consecuencias

- **Bueno:** el dato se pregunta una vez y no una vez por observable; queda disponible para cualquier otro indicador que necesite composición poblacional.
- **Malo:** el 1.7 deja de ser autocontenido — su indicador depende de que Generales esté respondido, lo que refuerza que el grupo `gen` sea prerrequisito del cuestionario principal (ver [[adr-0002]]).
- La captura de esa tabla en el frontend no existe todavía: es [[task-18]].

## Cómo se comprueba

El seed del observable 1.7 no genera `ReachQuestion` de composición, y `GeneralGroup` incluye «autoridades» con `is_population=True`.
