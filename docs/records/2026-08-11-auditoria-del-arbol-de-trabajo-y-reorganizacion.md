---
type: record
id: 2026-08-11-auditoria-del-arbol-de-trabajo-y-reorganizacion
title: "Auditoría del árbol de trabajo sin commitear y reorganización jerárquica de las tareas"
date: 2026-08-11
related: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
validate-paths: false
---

# Auditoría del árbol de trabajo sin commitear y reorganización jerárquica de las tareas

Dos trabajos de la misma jornada del 11 de agosto de 2026, que se registran juntos porque el segundo se apoya en el primero: una auditoría de lo que el trabajo manual sin commitear de Ricardo ya cubría de las tareas abiertas, y la reorganización del grafo de tareas que hasta hoy tenía treinta y tres huérfanas.

## Parte 1 · Qué cubría el árbol de trabajo

Contexto que ordena lo demás: el commit `4987fa7` («Gen: alias VCountInput, fila-pregunta numérica y panels en gris», 9 de agosto) dejó escrito en su propio mensaje «veredicto visual en contra: se rehace en [[task-96]]; se commitea como base». El árbol de trabajo auditado es ese rehacer, en curso, más un bloque aparte que no tiene nada que ver con Generales.

Diez archivos modificados, ninguno en el índice, más un archivo sin seguimiento.

### Tareas cubiertas por completo

**[[task-62]]** — la casilla de institución de prueba existe ahora en la edición del dashboard, y el campo es escribible sin pasar por el admin porque el serializer de institución expone todos los campos sin marcarlo de solo lectura. Sus dos criterios originales quedan satisfechos. **No se cierra**: Ricardo le agregó dos criterios nuevos el mismo día.

### Tareas cubiertas parcialmente

**[[task-96]]** — cubre uno de sus cuatro criterios, no toca el segundo, **retrocede en el tercero** y deja el cuarto pendiente. El detalle está reescrito en el cuerpo de la propia task.

**[[task-67]]**, su madre — con el ícono retirado y sin sustituto, el campo numérico vuelve a no tener ninguna señal visual, que es exactamente el estado que la abrió. Su segundo criterio, la aplicación consistente en toda la captura, ni se ha empezado: los años de buenas prácticas siguen en otro idioma de componente.

**[[task-68]]** — el árbol cumple la parte visible de lo que Rubén pidió: el rótulo perdió el «(opcional)». La obligatoriedad real quedó resuelta por [[adr-0011]], que decide que no la habrá; con eso la task queda cerrada.

**[[task-97]]** — el archivo sin seguimiento `api/.claude/test_migrate_orphan.py` **no es avance suyo: es el objeto de su segundo criterio**, que pide el veredicto de Ricardo sobre promoverlo a la suite o borrarlo. Sigue sin decidir desde el 9 de agosto.

### Cambios sin task que los cubriera

Dos estaban en el radar antes de auditar; el resto no:

- La columna «No binarie» en la tabla de poblaciones, cuyo dato **se pierde al guardar**: el campo no existe en el modelo de cantidades de población, no viaja en el payload y no entra en el total.
- El encabezado «Existe» convertido en «Se atiende» en generales. [[task-88]] cubría el seed del cuestionario por observable, no esto — y la reunión del mismo día objetó justamente esa palabra para poblaciones.
- **Nuevo:** el reordenamiento de columnas a mujeres antes que hombres en poblaciones, que deja la tabla de autoridades incoherente con ella. Desde hoy es convención del repositorio, anotada en el `CLAUDE.md` raíz, así que lo que falta es aplicarla también a autoridades.
- **Nuevo:** los encabezados de las columnas de conteo pasaron de alineación derecha a centrada, mientras el contenido sigue alineado a la derecha.
- **Nuevo:** el renombre del filtro de institución de prueba en el esquema de catálogo del API. Va en dirección contraria a la convención de lenguaje que Ricardo fijó después: «De prueba», nunca «test».
- **Nuevo:** la pregunta del componente numérico pasó de estar a la izquierda del campo a estar encima, y subió de tamaño tipográfico.
- Higiene sin task: una entrada nueva en el gitignore, un permiso local del arnés y un salto de línea final en la hoja de estilos.
- Siete líneas de importación por encima de las ochenta columnas en el panel de grupo.

### Reversiones deliberadas, no errores

Dos tareas ya cerradas quedaron contradichas por el árbol de trabajo. **Ricardo las revirtió con criterio visual propio, a la manera antigua y sin IA de por medio, y esos veredictos valen como definitivos.** Se registran aquí para que no se lean como regresión:

1. **[[task-66]]**, cerrada el 6 de agosto, había fijado el ancho de las celdas de conteo y el margen automático que pegaba el campo al borde derecho de la celda, «donde está el encabezado». El árbol de trabajo borró esa regla. La consecuencia práctica —el número de conteo pegado al margen derecho— es una de las autocríticas que Ricardo anotó en la demo, y se absorbe en [[task-96]].
2. **La primera decisión de [[task-93]]**, cerrada el 9 de agosto, pedía un componente-fila con la pregunta a la izquierda y el campo numérico fijo a la derecha, con ícono y unidad. El árbol la deshace en dos de sus tres elementos: la pregunta pasa arriba y el ícono desaparece. Sobrevive solo la unidad como sufijo, que es justamente la que no se ve.

## Parte 2 · La reorganización jerárquica

Antes de hoy el grafo tenía siete raíces de facto —[[task-1]] a [[task-6]], más [[task-41]]— y treinta y tres tareas abiertas sin `parent`, casi todas posteriores a las reuniones de agosto. La propuesta se le presentó a Ricardo y la aprobó tal cual.

### Cuatro raíces nuevas

- **[[task-98]] · Flujo — UX de estatus y transiciones para las dos audiencias.** Ocho hijas. Se separa de [[task-1]] porque aquélla es deuda de migración y ésta es diseño de experiencia sobre un motor que ya corre.
- **[[task-99]] · Comentarios: unificación, edición y borrado.** Tres hijas, todas de la revisión con Fernanda.
- **[[task-100]] · Migración a la infraestructura de la UNAM.** Absorbe [[task-95]] y [[task-25]], y estrena [[task-102]] y [[task-103]]. Recoge lo que hasta hoy solo vivía en un roadmap declarado esqueleto.
- **[[task-101]] · Catálogos editables del instrumento desde el dashboard.** Nace sin hijas: las suyas se están diseñando en diálogo con Ricardo.

### Reparto a raíces existentes

- A [[task-1]]: [[task-97]].
- A [[task-3]]: [[task-63]], [[task-64]], [[task-65]], [[task-84]], [[task-85]] y la nueva [[task-104]]. Y dentro de esa rama, [[task-84]] pasa a ser madre de [[task-82]] y [[task-83]], porque es la decisión de diseño de la que ambas dependen.
- A [[task-6]]: [[task-49]], [[task-52]] y [[task-87]].
- A [[task-41]]: [[task-55]], [[task-68]] y las nuevas [[task-105]] y [[task-106]].
- A [[task-2]]: [[task-92]], que espera la superficie de captura del cuestionario por observable.

### Lo que se queda suelto a propósito

[[task-61]] (montar Vitest) y [[task-91]] (migrar a Vuetify 3.13) son infraestructura transversal del monorepo, no cuelgan de ninguna funcionalidad. [[task-62]] y [[task-78]] quedan emparejadas por su enlace a [[adr-0009]] y no necesitan raíz. [[task-89]] y [[task-90]] quedan sueltas porque ya no son propuestas por hacer sino candidatas de la lista de extras, pendientes de cotización.

### Dos consecuencias del reparto, sin resolver

**[[task-4]] se quedó sin hijas abiertas.** Su única hija viva, [[task-25]], se mudó a [[task-100]] porque es limpieza del servidor de Yeeko, y la otra ya estaba cerrada. El endurecimiento que aún debe —el modo de depuración y la lista de orígenes permitidos en producción— vive hoy en el roadmap del skill `deployment`, no en tareas. Queda por decidir si se cierra, si absorbe ese endurecimiento como hijas propias, o si se muda entera bajo [[task-100]].

**[[task-94]] se quedó suelta.** La propuesta contemplaba abrir un bloque de testing que la agrupara con [[task-61]], pero esa opción no se decidió. Sigue como raíz sin hijas.

### El lote de diseño, cerrado el mismo día

Seis frentes quedaron sin abrir en el primer reparto porque se estaban cerrando en diálogo con Ricardo. El diálogo terminó esa misma jornada y todos aterrizaron:

- [[task-107]] y [[task-108]] — el modelo `GeneralQuestion`, los campos de texto del catálogo de grupos y su alta como catálogos editables, bajo [[task-101]], que deja de ser una raíz sin hijas. [[task-109]] queda como evaluación futura de un abstracto común.
- [[task-110]] — el respaldo de backend de la columna no binaria y su pregunta previa, que se decidió **única** para las dos tablas.
- [[task-112]] — el tri-estado, con su encabezado «Está presente», que además cierra el hilo de redacción que [[task-88]] dejaba abierto para generales. Su decisión vive en [[adr-0012]], que enmienda el punto 3 de [[adr-0008]].
- [[task-113]] — la unificación de los cuatro componentes de grupo, que absorbe la extirpación de los textos hardcodeados.
- [[task-111]] — la fórmula de paridad, bajo [[task-5]], junto a [[task-27]], [[task-28]] y [[task-29]].

Y dos que salieron del mismo diálogo sin estar en la lista original: [[task-114]], el diseño visual de la evidencia probatoria, registrado explícitamente como propuestas a dialogar; y [[task-115]], que rescata bajo [[task-4]] el endurecimiento de DEBUG y CORS del servidor actual — con lo que [[task-4]] deja de estar vacía. [[task-94]] también encontró madre: [[task-61]] pasa a encabezar un mini-bloque de testing.
