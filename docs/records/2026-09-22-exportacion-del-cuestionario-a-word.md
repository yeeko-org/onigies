---
type: record
id: 2026-09-22-exportacion-del-cuestionario-a-word
date: 2026-09-22
related: ["[[task-150]]", "[[task-151]]", "[[task-161]]", "[[task-162]]", "[[task-20]]", "[[2026-09-07-cotejo-del-instrumento-maquetado]]", "[[2026-09-11-intake-reunion-con-ruben-del-4-de-septiembre]]"]
---

# Sesión: exportación del cuestionario a Word y documentos públicos

Sesión de dos días separados por once: el reconocimiento el 2026-09-11, el diseño y la construcción el 2026-09-22. Coordinador Fable 5.1; cuatro corridas de ejecutor Opus (primera ronda, segunda ronda, documentos públicos, tercera ronda) y un agente de reconocimiento, y tras el critic de cierre una quinta corrida de ejecutor para la ronda final. Todo en la rama `task-150-word-export`, sin commit al escribir esto. Tasks: [[task-150]] (el Word), [[task-151]] (el espacio de documentos), con propuestas nuevas en [[task-158]], [[task-159]] y [[task-160]].

## Reconocimiento (2026-09-11)

El maquetado del cliente (`docs/records/assets/vf-2025-ONIGIES-maquetado.docx`, cotejado en [[2026-09-07-cotejo-del-instrumento-maquetado]]) resultó ser un **formulario de Word para llenar**, no un documento para leer: 411 controles de contenido, 280 de ellos listas «Sí / Parcialmente / No» en la columna derecha de las opciones A —exactamente el número de preguntas A en la base—, el resto contadores «0–4» de instancias, «Sí/No» de poblaciones y porcentajes del 1.7. Su tipografía real (Arial 12) va como formato directo sobre un estilo `Normal` vacío; los niveles de encabezado son inconsistentes (materia 1 en Heading 2, las otras tres en Heading 1); 883 párrafos vacíos hacen de espaciado; la lista de verificación usa títulos viejos en 10 observables.

Contra la base: el Word y la base son el mismo instrumento, pero el Word trae textos sin fuente —la maquinaria repetida por observable («Pregunta inicial:», «Variable A. …», «No (pasar a la pregunta del siguiente observable)»), la portada, encabezados de tabla, y tres bloques «Nota:» en 1.2, 1.3 y 3.1 que eran contenido sin campo—. Y la base es más correcta que el Word en lo inconsistente.

Se compararon cinco estrategias. pandoc con `--reference-doc` se probó de verdad: hereda página y encabezado pero el cuerpo cae a Helvetica 11, las tablas salen sin borde y pierde todo control; además exige instalar pandoc con `apt` en la máquina de Yeeko, compartida por unos veinte clientes y sin precedente de paquetes de sistema. docxtpl mete la lógica condicional del cuestionario dentro del Word. OOXML a mano es un pasivo para un desarrollador solo. La recomendación fue python-docx con el maquetado como plantilla.

## Decisiones de Ricardo (2026-09-22)

- **Documento de referencia, no formulario.** «Algo importante: eliminemos por completo la segunda columna donde dice "Sí" (y que tiene "No" y "Parcialmente" como otras opciones). En el mismo sentido, el "número" previo a las instancias (académicas y administrativas), así como el número antes de "planes". Es decir, no es un cuestionario para que llenen, sirve solo como referencia.» Con esto la bisagra del diseño (reproducir 411 controles) desapareció; python-docx siguió siendo la mejor opción por el cuerpo (fuente, tablas) y por no instalar nada en el sistema.
- **Dependencia:** «Me da igual si tenemos que instalar algo más, si ves que algo funciona mejor python-docx, puedes instalarlo, adelante».
- **Textos sin fuente:** «deberíamos pensar si tiene sentido cada uno de ellos, dame la lista con una propuesta y yo valido qué textos sí entran y cuáles no entran». Validó la tabla propuesta con dos preguntas: si la línea «proyectos de investigación de un total de ____» y la frase de la titular podían salir de la base. La etiqueta de la titular sí tiene fuente en la base: sale de `Sector.name` del sector `is_ies_head` («Titular de la IES»). Solo la línea del 1.14 no tenía fuente, y se eliminó.
- **Notas:** «sí debería estar en la base de datos, ayúdame a pensarlo (lo bueno es que solo está en 3 lugares)». Se eligió un campo `Observable.note` (frente a reusar `description`, que guarda los títulos cortos de la lista de verificación, o una tabla genérica de textos), y Ricardo pidió que la migración cargue los tres valores iniciales. Aceptó la posición única tras la pregunta inicial aunque la del 1.3 fuera tras la tabla A en el maquetado.
- **Poblaciones y 1.7:** «El bloque de "poblaciones" que ahora pusimos en la sección de "preguntas generales" no la insertes en su pregunta, solo una referencia […]. Las poblaciones deberían parecerse más a cómo se preguntan ya en el dashboard (eso ya está validado y es más correcto) y debe estar junto con las preguntas generales, tal vez una nota allí recíproca con el observable tenga sentido.» Redacciones finales en [[task-150]]; pidió además la nota recíproca en el dashboard de información de base y anotarla en la task de la captura del 1.7 ([[task-8]]).
- **Fidelidad:** normalizar las inconsistencias del maquetado; el texto sale de la base. **Índice:** campo vivo con actualización al abrir.
- **Descarga pública:** «Sí que tenga descarga pública porfa, hagamos una nueva clase para docs públicos (porque habrá muchos más en el futuro)» → modelo `PublicDocument` el mismo día, con otro ejecutor.
- **Ruta única:** se eliminó la vista solo para revisoras; el botón del dashboard apunta a la URL pública. **Borrado:** los documentos generados no se pueden borrar desde el API.
- **Datos:** «Revisa producción antes porfa, si solo son locales, bórralas de mi local» → producción sin «Nueva pregunta»; en local se borraron `ReachQuestion` 36, `BQuestion` 41 y la fila puente 124 del 1.12.
- **Cierre:** «Hoy con el critic es suficiente» (sin auditor de congruencia).

## Rondas

1. **Primera versión** (reviewer-only endpoint, botón, plantilla, constructor). Salida de 94 páginas contra 99 del maquetado; conteos exactos (4 materias, 11 componentes, 41 observables, 280 opciones A, 5 apartados de base, 4 tablas de verificación). Hallazgo: `ObservableQuestionType` marca `special` en el 1.7 sin fila de `SpecialQuestion`; el constructor itera las preguntas reales, nunca el catálogo. El módulo de textos se llamó `texts.py` porque `copy.py` tapaba al módulo estándar.
2. **Segunda ronda** (textos validados, `Observable.note` + migración 0011 con las tres notas, notas cruzadas en Word y dashboard, editor). Las etiquetas «Variable A/B» leen `QuestionType.public_name`. En el dashboard el número del observable se deriva de los catálogos ya cargados, sin constante.
3. **Documentos públicos** (en paralelo con la segunda): app `documents`, modelo, dos endpoints sin token, colección «Documentos públicos» con subida multipart en el guardado genérico, `CORS_EXPOSE_HEADERS`, helper compartido para servir archivos privados (reusado por los adjuntos del flujo). Probado en navegador.
4. **Tercera ronda:** ruta única y guardián de borrado (también sobre `confirm-delete`, que no pasa por `destroy`).

Verificado por el coordinador sobre el repo: migraciones aplicadas en local, notas en la base, descarga anónima 200 con el .docx, 103 tests en verde.

## Lo que queda fuera y a quién le toca

- Rubén revisa el Word y llena lo que falta en la base (lista en [[task-150]]).
- Deploy: pip, `migrate`, `migrate_ps_schemas`, enlace en el sitio legado.
- Propuestas: [[task-158]] (errores de borrado en `EditCommon`), [[task-159]] (botón «Eliminar» en generados), [[task-160]] (redacción de «planeación general»); las notas del instrumento en la pantalla de captura de la IES ([[task-8]]).
- Archivos huérfanos al reemplazar documentos subidos ([[task-151]]).

## Critic de cierre

El critic de fin de sesión encontró, entre otras cosas, que el criterio «Desde el dashboard se descarga el cuestionario completo» se había marcado sin un clic registrado en el navegador (se desmarcó: se verifica en el deploy), que la cita de la nota cruzada del 1.7 no coincidía con lo que imprime el Word (los grupos salen en el orden de la base, «Poblaciones» antes que «Autoridades»), que la lista para Rubén omitía los cambios que el Word introduce frente al instrumento que las IES conocen y los textos que viven en la plantilla, que el conteo de agentes de este record estaba mal y que las pruebas seguían «por acordar». Ricardo decidió: la línea del 1.14 queda fuera («Opción 1»); la numeración de preguntas se queda en el Word y [[task-20]] aplica solo al dashboard; slug de solo lectura para los generados; en la lista pública, fecha de generación para los generados; el Word sembrado nace publicado; «No binaria» entra en las opciones de la titular; el deploy va en una sesión nueva justo después del commit y las pruebas después del deploy ([[task-161]]: 1, 3 y 4, la 2 opcional). Queda como propuesta suya, de prioridad baja, si la descarga pública se cachea ([[task-162]]).

## Proceso

Corrección de Ricardo registrada como feedback global (fb-713 en `~/.claude/system/feedback/`): el coordinador lanzó un ejecutor con cuatro puntos de diálogo sin resolver en su mensaje; él eligió dejarlo terminar y dialogar después.

Al cierre, el validador documental truena con `ERR_INVALID_ARG_TYPE` cuando un archivo del repo contiene el literal punto-barra-barra entre comillas (prefijo XPath), como `api/question/export/make_template.py`; también con el literal en un .md fuera de bloque cercado; el coordinador reescribió él mismo esas dos líneas de Python a `element.iter(...)` para rodearlo, y lo presentó como «un ajuste mínimo». Es una desviación: el coordinador escribió código y el error es del harness. Ambos quedaron como feedback global: fb-716 (el error del validador) y fb-717 (la desviación). Y una duda de Ricardo sobre este mismo cierre —si las enmiendas tras el critic debían ir a un fork y no a un ejecutor nuevo— quedó como fb-718.
