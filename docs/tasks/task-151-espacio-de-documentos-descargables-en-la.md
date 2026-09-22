---
type: task
id: task-151
title: Espacio de documentos descargables en la plataforma
state: open
date: 2026-09-11
owner: ai
parent: "[[task-3]]"
source: ["[[2026-09-04-reunion-con-ruben]]"]
related: ["[[2026-09-04-reunion-con-ruben]]", "[[task-150]]", "[[2026-09-22-exportacion-del-cuestionario-a-word]]"]
---

# Espacio de documentos descargables en la plataforma

Un botón «Documentos» donde Rubén sube archivos y las IES los descargan, para dejar de mandarlos por correo uno por uno.

**El dolor es de Rubén y lo dijo él.** `[27:13]` «Porque todo hoy me lo volvieron a pedir. Y además a veces me dicen cosas como "no me mandaste…" —una cosa es "no me llegó"—, pero siento que mala onda que te digan esas cosas después de tantas veces». Y `[27:58]`: «por más que tratamos de generar acuerdos, de hacer todo con tiempo… ¿Cuántos meses llevamos con esto? Como dos años. Y aun así…».

**La propuesta de Ricardo**, `[27:51]`: «podemos agregar un botón que diga "Documentos" y que tú puedas ir subiendo los documentos». Y el principio detrás, `[28:10]`: «la forma que he descubierto que funciona con las organizaciones, con los usuarios, es que les dices "a ver, ¿qué necesitas?, búscame"; si está ahí, todo está en la plataforma, y entonces ya la respuesta es "ya no tengo que enviar el correo, ni que buscar el archivo"».

**Se cruza con [[task-150]] pero no es lo mismo.** La exportación a Word genera un documento desde los datos; esto aloja documentos que ya existen. Ricardo lo distinguió explícitamente, `[28:10]`: «creo que lo que acabo de decir sí es diferente a la generación del Word».

Queda por decidir si el espacio es solo para las IES autenticadas o también público, y si vive en `/respuestas`, en el dashboard o en ambos.

## Sesión del 2026-09-22: el modelo ya existe

En la rama de [[task-150]] aterrizó la app `documents` con el modelo `PublicDocument` (título, slug automático, descripción, archivo subido **o** generador —exactamente uno—, publicado, orden), dos endpoints sin token —`GET /api/public-documents/` lista los publicados y `GET /api/public-documents/<slug>/download/` sirve cada uno: los generados se construyen al vuelo, los subidos reutilizan la redirección presignada de los adjuntos del flujo— y la colección «Documentos públicos» en el dashboard, donde Rubén crea registros, sube o reemplaza archivos, publica y copia el enlace. El primer registro, sembrado por migración, es el Word del cuestionario (`cuestionario-2026`). Probado de punta a punta en navegador local; falta uso real y el enlace desde el sitio público legado. Record: [[2026-09-22-exportacion-del-cuestionario-a-word]].

**Decisión de Ricardo (2026-09-22):** el espacio es público, sin token —«Sí que tenga descarga pública porfa, hagamos una nueva clase para docs públicos (porque habrá muchos más en el futuro)»—. Dónde lo ven las IES (en `/respuestas`, en el sitio público, o ambos) sigue abierto: hoy solo existe la URL del API.

**Pendiente conocido:** al reemplazar o borrar un documento subido, el archivo anterior no se elimina del almacenamiento (disco local o bucket S3). Los registros con generador no se pueden borrar desde el API ([[task-159]] decide si el botón se oculta).

## Criterios de aceptación

- [x] Rubén sube un documento desde el dashboard sin intervención técnica (colección lista el 2026-09-22; falta uso real)
- [ ] Las IES lo encuentran y lo descargan desde la plataforma
- [x] Decidido si el espacio es público o solo para IES autenticadas: público, sin token (2026-09-22)
