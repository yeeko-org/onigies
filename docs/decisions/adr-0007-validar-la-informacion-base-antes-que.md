---
type: decision
id: adr-0007
title: Validar la información base antes que los avances del cuestionario
state: accepted
date: 2026-08-03
origin: meeting
deliberation: dialogued
rationale: recorded
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
affects: ["api/survey/models.py", "api/api/views/survey/__init__.py", "api/ies/models.py"]
---

# Validar la información base antes que los avances del cuestionario

## Contexto y planteamiento del problema

En la reunión del 28 de julio ([[2026-07-28-reunion-flujo-bp-e-informacion-base]]) Rubí planteó una preocupación de calendario que terminó cambiando el orden de trabajo. Faltaban menos de dos semanas para el 10 de agosto y la sección estadística —el registro de datos cuantitativos, «la que en realidad mueve más a las universidades»— no iba a estar completa.

Su propuesta no fue recortar el cuestionario sino **invertir la secuencia**: abrir primero únicamente la sección de información base, validarla con las revisoras y las IES, y solo después abrir los observables.

> `[25:11]` «Es que quería ver si es viable habilitar en primer lugar la sección de información base, como que te concentraras en esa, porque así podríamos llegar a la... Creo que tengo una reunión informativa, no sé si el 10 o el 17 de agosto, podríamos llegar a esa reunión y decirles como esta vez no vamos a avanzar con las instituciones antes de que tengan lista la información base.»

## Criterios de decisión

Lo que se estaba optimizando no era la velocidad de entrega sino **la integridad de los indicadores**. La razón es aritmética y Rubí la nombró desde la experiencia de ediciones anteriores:

> `[25:53]` «¿Por qué? Porque en otras ocasiones nos ha pasado que mueven los datos y eso genera problemas.»
>
> `[25:57]` «Claro, el denominador, si cambias el denominador...»
>
> `[25:59]` «Sí, o sea, como esta vez antes de validar los avances, primero vamos a validar la estructura porque se vuelve fundamental.»

La información base —matrícula, personal, composición poblacional por sector— es el **denominador** de buena parte de los indicadores del observatorio. Si una IES la modifica después de que las revisoras validaron sus avances, todos los indicadores calculados sobre esos avances quedan mal, sin que nadie se entere. El costo de recalcular y revalidar es mucho mayor que el de retrasar la apertura de las demás secciones.

Un criterio secundario: la propuesta convierte una restricción de calendario en un mensaje defendible ante las IES en la sesión informativa, en vez de en una disculpa. `[32:21]` «Sí, es una cuestión de seriedad al final, o sea, de todos modos lo íbamos a hacer, pero ahorita está ayudando a tener suficiente tiempo para que esté listo el cuestionario completo».

## Opciones consideradas

- **Abrir todo el cuestionario a la vez**, como en ediciones anteriores. Es lo que se venía haciendo, y es lo que produjo el problema de los denominadores movidos.
- **Abrir por etapas, información base primero**, y no dejar avanzar a las instituciones hasta tenerla validada.

Rubí planteó también la posibilidad genérica de «dosificar el trabajo» (`[25:11]`), reconociendo que sus propuestas de dosificación no siempre calzan con la lógica de desarrollo. La conversación la aterrizó en la secuencia concreta de arriba.

## Resultado

Se adopta la **apertura por etapas con la información base como prerrequisito**. Las IES no avanzan con los observables hasta que su información base esté capturada y validada.

Calendario acordado en la misma reunión:

- **2026-08-03:** la sección de información base lista para captura.
- Semana del 3: Rubí y las revisoras la validan.
- **2026-08-10:** se abre la sección a las IES.
- **2026-08-14:** sesión informativa donde se comunica la regla a las instituciones.
- **Principios de septiembre:** se abren los demás apartados, para que las IES respondan durante septiembre y octubre.

Rubí ofreció además el colchón que hace viable la secuencia: `[32:21]` «yo te podría ofrecer como otras dos semanas más en las que con las revisoras validamos esa información con las IES y eso nos va a mantener entretenidas».

### Consecuencias

- **Bueno:** los denominadores quedan congelados y validados antes de que se calcule ningún indicador sobre ellos. El equipo de revisión tiene trabajo útil durante las semanas en que el resto del cuestionario todavía se construye.
- **Bueno:** desplaza la presión del 10 de agosto de «todo el cuestionario» a «una sección», que sí es alcanzable.
- **Malo:** la ventana para responder el cuestionario completo se comprime a septiembre y octubre.
- **Malo:** obliga a un mecanismo que hoy no existe — poder abrir una sección y no las demás. Es [[task-53]].
- La decisión solo se sostiene si la información base queda efectivamente cerrada tras validarse; si las IES la pueden seguir editando, el problema del denominador regresa intacto. Ese candado es [[task-55]], y hoy no existe en el API.

### Cómo se comprueba

El día que se abran los observables, las IES con la información base sin validar no pueden capturar en ellos; y una IES con la información base cerrada recibe un rechazo del API al intentar modificarla.

## Más información

El compromiso de construcción que se desprende de esta decisión es [[task-41]]. El acta completa es [[2026-07-28-reunion-flujo-bp-e-informacion-base]].
