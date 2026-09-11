---
type: record
id: 2025-09-11-cotizacion-plataforma-v3
title: Cotización de la plataforma v3 del ONIGIES, versión de septiembre de 2025
date: 2025-09-11
file: docs/records/assets/2025-09-11-Plataforma-v3-Calculo-2025.odt
related: ["[[estado-administrativo-y-de-pagos]]", "[[2026-01-07-cotizacion-plataforma-v3]]"]
---

Primera versión de la cotización del desarrollo de la versión 3 de la plataforma ONIGIES, fechada por el nombre del archivo el 11 de septiembre de 2025. Es la base contra la que se compara todo lo administrativo del proyecto; el mapa vivo está en [[estado-administrativo-y-de-pagos]].

El original `.odt` vive en `docs/records/assets/2025-09-11-Plataforma-v3-Calculo-2025.odt`; lo de abajo es su conversión íntegra con `pandoc -f odt -t markdown`, tabla incluida.

**Lo que distingue a esta versión:** los conceptos que se pagaron en 2025 están **subrayados** en el documento original. `pandoc` no conserva el subrayado y los rinde en *cursiva*, así que en la tabla de abajo **cursiva = subrayado = concepto pagado en 2025**. Son ocho: «Soporte para subir y mostrar buenas prácticas» (5,000), «Diseño de nueva base de datos» (8,000) y el bloque completo «Dashboard para registro y validación de información» (75,000) con sus seis renglones.

**Artefacto de conversión, no del original:** el renglón `TOTAL` salió como `,400` porque `pandoc` perdió los primeros dígitos. La aritmética del propio documento lo fija: subtotal 240,000 + IVA 38,400 = **278,400**. Ese valor es cálculo del asistente, no lectura del archivo; el `.odt` es la fuente si hace falta comprobarlo.

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

Instalación y Soporte a mediano plazo

Se solicitará a la coordinación de cómputo una nueva máquina virtual con el sistema operativo actualizado para que soporte la tecnología con la que se desarrollará la plataforma.

La versión anterior se modificará para que pueda tener un subdominio o una ruta URL específica para distinguir la versión previa y la nueva.

Durante un periodo de 18 meses, se dará soporte técnico para resolver dudas, capacitar al personal operativo, así como para resolver bugs o errores de elementos que no funcionen correctamente.

Costos:

  ------------------------------------------------------------- --------------
  Módulos                                                       Costo
  **Plataforma pública**                                        **48,000**
  Diseño de nueva identidad gráfica del sitio web               16,000
  Configuración base de vistas web de sitio público             17,000
  Interactividad web y fichas intermedias                       7,000
  *Soporte para subir y mostrar buenas prácticas\**             *5,000*
  Modificación de versión 1 para compatibilidad                 3,000
  **Base de datos**                                             **25,000**
  *Diseño de nueva base de datos*                               *8,000*
  Exportaciones a Excel                                         12,000
  Cálculo de indicadores y ponderaciones                        5,000
  ***Dashboard para registro y validación de información\****   ***75,000***
  *Poblaciones\**                                               *16,000*
  *Preguntas básicas de institucionalización\**                 *5,000*
  *Preguntas transversalización\**                              *14,000*
  *Preguntas complementarias (complementos y ampliaciones)\**   *8,000*
  *Flujo de validación de datos con estatus y comentarios\**    *25,000*
  *Soporte para subir y aprobar buenas prácticas\**             *7,000*
  **Diseño e implementación de visualizaciones**                **92,000**
  Visualizaciones de población                                  17,000
  Visualizaciones de índices agregados                          40,000
  Despliegue y visualización de preguntas                       9,000
  Despliegue histórico de información                           4,000
  Histograma IES                                                4,000
  Visualizaciones de población                                  18,000
  **Subtotal**                                                  **240,000**
  **IVA**                                                       **38,400**
  **TOTAL**                                                     **,400**
  ------------------------------------------------------------- --------------
