---
type: decision
id: adr-0025
title: El alcance no ofrece los sectores que la IES declaró ausentes en Generales
state: accepted
date: 2026-10-02
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-10-02-alta-del-nivel-tecnico-superior]]"]
affects: ["api/api/views/answer/__init__.py", "api/api/views/answer/serializers.py"]
related: ["[[adr-0012]]", "[[adr-0002]]", "[[adr-0024]]"]
---

# El alcance no ofrece los sectores que la IES declaró ausentes en Generales

## Contexto y planteamiento del problema

Las preguntas de transversalidad sectorial (alcance) del cuestionario principal ofrecen una lista de sectores que se arma en vivo: los principales más los propios de la pregunta. Hasta hoy esa lista ignoraba lo que la IES declaró en Generales: una IES que dijo «no tengo posgrado» seguía viendo «Alumnado de nivel posgrado» como opción en las 32 preguntas estándar. Los planes de estudio, en cambio, ya ocultaban el nivel marcado «No aplica». Con el TSU precargado en «No» para todas las encuestas 2025 ([[adr-0024]]), el desajuste se volvía visible en 33 preguntas para casi todas las IES. Ricardo: «Por supuesto que no deben mostrarse los sectores que ya se declararon en "no" en las preguntas de transversalidad sectorial».

## Criterios de decisión

- La IES no ve opciones que ella misma descartó.
- Nada contestado se pierde ni se reescribe en silencio.
- Un mismo criterio para la IES y para la revisora.

## Opciones consideradas

- **Filtrar en el backend**, en los dos endpoints que sirven la lista (detalle del eje y detalle del observable), con el tri-estado de [[adr-0012]].
- **Filtrar en el componente del Nuxt** — descartada: la revisora y la IES podrían ver listas distintas, y el export dependería del cliente.

## Resultado

Se filtra en el backend: `get_sectors` excluye los sectores cuya `PopulationQuantity.is_present` de esa encuesta es `False`, y también las autoridades marcadas «No aplica» (`no_apply=True`), que no declaran presencia (ampliación del mismo día, a petición de Ricardo). El nulo (nadie lo contestó) y el `True` siguen visibles. `ReachResponse.sectors` ya guardados no se tocan. El cuestionario en blanco que exporta a Word no pasa por este serializer y sigue completo. La validación de completitud sigue leyendo lo guardado.

### Consecuencias

- **Bueno:** las IES sin TSU no ven el sector nuevo; las que declararon «No» en cualquier población dejan de verla en el alcance.
- **Malo:** una consulta más por detalle.
- **Caso límite descartado:** un sector marcado en alcance y después declarado «No» en Generales no puede ocurrir, porque el cuestionario principal solo se captura con Generales aprobadas y Generales no se reabre ([[adr-0002]]); la única salida es la válvula de admin, un acto explícito.

### Cómo se comprueba

`CaptureApiTests.test_reach_hides_sectors_declared_absent` (`api/answer/tests.py`): con un sector en `False`, uno en `True` y uno nulo, la pregunta de alcance llega sin el primero, por los dos endpoints y para IES y revisora.

## Más información

[[2026-10-02-alta-del-nivel-tecnico-superior]].
