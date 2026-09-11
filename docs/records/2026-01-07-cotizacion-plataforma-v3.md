---
type: record
id: 2026-01-07-cotizacion-plataforma-v3
title: Cotización de la plataforma v3 del ONIGIES, versión de enero de 2026
date: 2026-01-07
file: docs/records/assets/2026-01-07-Plataforma-v3-Calculo-2026.odt
related: ["[[estado-administrativo-y-de-pagos]]", "[[2025-09-11-cotizacion-plataforma-v3]]"]
---

Segunda versión de la cotización del desarrollo de la versión 3 de la plataforma ONIGIES, fechada por el nombre del archivo el 7 de enero de 2026. El mapa vivo que compara ambas está en [[estado-administrativo-y-de-pagos]].

El original `.odt` vive en `docs/records/assets/2026-01-07-Plataforma-v3-Calculo-2026.odt`; lo de abajo es su conversión íntegra con `pandoc -f odt -t markdown`, tabla incluida.

**Qué cambia respecto de [[2025-09-11-cotizacion-plataforma-v3]].** El texto anterior a la tabla es casi idéntico; la diferencia está en la tabla y en una sección nueva.

- **Los conceptos pagados en 2025 pierden su monto** y quedan como `-----`: «Soporte para subir y mostrar buenas prácticas», «Diseño de nueva base de datos» y el bloque «Dashboard para registro y validación de información» completo. Suman **88,000** de la cotización de 2025.
- **Entra un módulo nuevo, «Automatización de Informes de Resultados», por 81,000**, con su sección de texto propia: informes en PDF por institución, esquema híbrido de automatización + IA + revisión humana, y la razón de escala —41 observables frente a los 14 indicadores de la primera metodología—.
- **Los bloques que no se tocaron:** «Diseño e implementación de visualizaciones» sigue en 92,000, y dentro de «Plataforma pública» y «Base de datos» los renglones no pagados conservan su monto.

El subtotal pasa de 240,000 a **233,000**: 240,000 − 88,000 pagados + 81,000 del módulo nuevo. Total con IVA, **270,280**.

---

**NUEVA METODOLOGÍA PARA EL ONIGIES**

**Desarrollo de la versión 3 de la plataforma**

Introducción

La plataforma del Observatorio Nacional para la Igualdad de Género en las Instituciones de Educación Superior (ONIGIES) cuenta actualmente con el soporte para registrar y dar a conocer los resultados de varios años con la metodología original.

Sin embargo, se plantea la creación de una plataforma completamente nueva. Las razones para comenzar de nuevo son las siguientes:

- Existe una actualización metodológica y tiene poca compatibilidad con la metodología original.
- La plataforma original se desarrolló hace más de 5 años, con tecnología que actualmente tiene poco soporte, la nueva tecnología ha avanzado en muchos sentidos, por lo que vale la pena arrancar desde cero para incorporar esas mejoras de seguridad y rendimiento.
- Las visualizaciones deberán obedecer una lógica distinta a 7 ejes y entre 1 y 4 componentes, en su lugar, serán 4 materias o derechos.
- Existe un nuevo nivel más profundo de información que son características o elementos aplicables
- Nuevos datos de población sexo-diversa que requerirá su espacio de visualización
- La necesidad de agregar buenas prácticas de las IES tanto a las visualizaciones como al detalle de las IES.

Nuevo diseño

El sitio web tendrá un nuevo diseño para presentar la información y para contar de mejor manera la narrativa del objetivo, la metodología y los resultados.

Las visualizaciones también cambiarán, las burbujas podrían ser reemplazadas por barras por gráficos radiales o por algún otro recurso que facilite la comparación entre IES y entre indicadores.

Adicionalmente, se desarrollará una visualización que resumirá en un solo vistazo todas las respuestas (ya que la mayoría son binarias) de todos los derechos, componentes y observables, con la posibilidad de hacer zoom y clics en secciones específicas para tener el detalle completo.

Se intentará agregarle mayor interactividad y animaciones a las visualizaciones, para hacerlas visualmente atractivas y llamativas.

Módulos y vistas

Los siguientes módulos que ya se desarrollaron, se volverán a implementar desde cero siguiendo una lógica similar:

Vista inicio

Resumen de los ejes (ahora derechos), explicación metodológica, vista histórica, descarga de datos concentrados, histograma de avance de las IES.

Vista por IES

Cada una de las IES con datos aprobados tendrá una página donde se mostrarán los resultados del último año, así como un resumen del avance histórico. Además, se podrán descargar los datos origen.

Registro histórico

Posibilidad de registrar varios años de información, pudiendo distinguir en todo momento el año que se está visualizando o registrando.

Exportaciones de Excel

Las IES podrán descargar su información en cualquier momento del registro, mientras que el público general podrá descargarla ya que ha sido aprobada.

Dashboard con validación por revisoras

Además de la vista por IES, se podrá contar con una visión general con la lista de todas las IES y sus estatus de avance.

Vista preliminar

La interactividad (ya sea por medio del mouse o con clics) deberá incluir fichas o tarjetas preliminares resumen que permitan a las personas usuarias permanecer en la misma vista.

Visualizaciones para población

Se desarrollarán visualizaciones específicas para mostrar las diferencias de género de las poblaciones de los sectores y subsectores.

Otras mejoras.

Los indicadores y las preguntas (en el nivel que se acuerde) podrán tener documentación asociada, por ejemplo, la normativa relacionada.

Se podrán agregar filtros para las IES como distinguir entre públicas y privadas, las que tienen posgrados, ordenar según tamaño, elegir las IES de una entidad federativa, etc.

Otra mejora será la posibilidad de visualizar hasta el nivel más desagregado las preguntas y las respuestas de las instituciones, ya que esta información que actualmente sólo se encuentra disponible en la descarga de los datos en formato excel.

La gestión de las credenciales contará con una nueva capa de seguridad, así como con la posibilidad de enviar un link con un token para que sean las IES las que gestionen por su cuenta sus contraseñas. También se contempla una

Por último, la nueva plataforma deberá ser fácilmente editable, tanto en las definiciones de los indicadores, como en todos los contenidos visibles y explicaciones. Los procesos para agregar IES, establecer las fechas (cierre de registro, cierre de validación, publicación, etc.) se facilitar la gestión al equipo operativo del ONIGIES.

Automatización de Informes de Resultados.

Los informes de Resultados en el pasado han sido creados individualmente para cada una de las IES que terminaban la validación de su información, sin embargo, dicha actividad contemplaba una gran cantidad de trabajo tanto en la redacción, en el análisis de la información y en el diseño editorial.\
\
Para esta nueva versión del ONIGIES, se espera una cantidad más grande de Instituciones. También se ampliará el número de indicadores a desplegar, ya que existirán 41 Observables, versus 14 indicadores de la primera versión metodológica. Por ello, automatizar la creación de informes en formato PDF es algo necesario, sin dejar de pasar por la revisión humana.

Para construir el módulo de automatización, se deberá agregar al Dashboard una sección para visualizar el informe (editable) y para cada una de las secciones, tener a la mano para las personas revisoras los indicadores y resultados desagregados.

Además, se agregarán a los componentes y a los observables la posibilidad de agregar descripciones de lo que implica cada nivel de avance. También se plantearán algunos escenarios y redacciones posibles.

Se plantea un esquema híbrido que combine la automatización de redacciones para los niveles de avance, la Inteligencia Artificial (basada en los lineamientos previamente escritos) y la revisión humana para hallazgos extras y para la verificación de las redacciones.

Los informes deberán contener un diseño editorial, las visualizaciones y las redacciones de todos los ejes, componentes y observables, así como las poblaciones y las distinciones entre las preguntas de institucionalización y transversalización.

Se plantean los reportes anuales, así como los reportes

Instalación y Soporte a mediano plazo

Se solicitará a la coordinación de cómputo una nueva máquina virtual con el sistema operativo actualizado para que soporte la tecnología con la que se desarrollará la plataforma.

La versión anterior se modificará para que pueda tener un subdominio o una ruta URL específica para distinguir la versión previa y la nueva.

Durante un periodo de 18 meses, se dará soporte técnico para resolver dudas, capacitar al personal operativo, así como para resolver bugs o errores de elementos que no funcionen correctamente.

Costos:

  ------------------------------------------------------------- -----------------
  Módulos                                                       Costo
  **Plataforma pública**                                        **43,000**
  Diseño de nueva identidad gráfica del sitio web               16,000
  Configuración base de vistas web de sitio público             17,000
  Interactividad web y fichas intermedias                       7,000
  *Soporte para subir y mostrar buenas prácticas\**             *\-\-\-\--*
  Modificación de versión 1 para compatibilidad                 3,000
  **Base de datos**                                             **17,000**
  *Diseño de nueva base de datos*                               *\-\-\-\--*
  Exportaciones a Excel                                         12,000
  Cálculo de indicadores y ponderaciones                        5,000
  ***Dashboard para registro y validación de información\****   ***\-\-\-\--***
  *Poblaciones\**                                               *\-\-\-\--*
  *Preguntas básicas de institucionalización\**                 *\-\-\-\--*
  *Preguntas transversalización\**                              *\-\-\-\--*
  *Preguntas complementarias (complementos y ampliaciones)\**   *\-\-\-\--*
  *Flujo de validación de datos con estatus y comentarios\**    *\-\-\-\--*
  *Soporte para subir y aprobar buenas prácticas*               ***\-\-\-\--***
  **Diseño e implementación de visualizaciones**                **92,000**
  Visualizaciones de población                                  17,000
  Visualizaciones de índices agregados                          40,000
  Despliegue y visualización de preguntas                       9,000
  Despliegue histórico de información                           4,000
  Histograma IES                                                4,000
  Visualizaciones de población                                  18,000
  **Automatización de Informes de Resultados**                  **81,000**
  Diseño editorial y de visualizaciones                         8,000
  Base para informes en PDF con visualizaciones                 17,000
  Informes anuales por institución                              26,000
  Informes multianuales                                         30,000
  **Subtotal**                                                  **233,000**
  **IVA**                                                       **37,280**
  **TOTAL**                                                     **270,280**
  ------------------------------------------------------------- -----------------
