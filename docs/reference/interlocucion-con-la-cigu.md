---
type: reference
id: interlocucion-con-la-cigu
title: "Interlocución con la CIGU: quién es quién del lado del cliente"
state: current
date: 2026-09-11
related: ["[[task-102]]", "[[task-103]]", "[[task-100]]"]
---

# Interlocución con la CIGU: quién es quién del lado del cliente

Quién es quién del lado del cliente para el ONIGIES y qué se puede pedir a través de quién. Se corrige aquí cuando algo cambie; no se escribe otro documento.

## El cliente

| Persona | Dónde está | Qué hace para el ONIGIES |
|---|---|---|
| **Rubén** (también «Rubí» en documentos viejos) | CIGU | Responsable del ONIGIES y el interlocutor de Ricardo en el proyecto: el instrumento, las definiciones metodológicas, el presupuesto y los pagos pasan por él |
| **Carlos Gutiérrez** | Titular del área TIC de la entidad, CIGU; su correo firma «Departamento de Sistemas, Dirección de Planeación, Vinculación y Proyectos Especiales» | Recién nombrado. Es quien levanta los tickets en la plataforma de la DGTIC, porque **cada entidad tiene una sola cuenta**. Lo hace para toda la CIGU, no para un proyecto en particular |
| **Ricardo Sanginés** | Yeeko, desarrollador externo | No puede levantar tickets: no tiene cuenta en la plataforma de la DGTIC ni la tendrá. Aporta los datos técnicos de cada solicitud, y **no tiene canal directo con Carlos** |
| **Sandra Barranco García**, «Sandy» | Líder de proyecto en la CIGU | **No es del ONIGIES, es del STIG.** Se la nombra aquí solo porque los documentos de agosto de 2026 le atribuyeron un trámite de servidor que pertenece a ese otro proyecto |

Nazul Valencia aparecía en los documentos de agosto como responsable TIC de la entidad y como vía para abrir el trámite. **Ya no trabaja en la CIGU**: quien ocupa ese lugar es Carlos.

## Lo que el ONIGIES no tiene todavía

**No hay solicitud de servidor, no ha habido reunión con Cómputo UNAM y no hay interlocutor en la DGTIC.** La reunión sigue pendiente en [[task-102]], con sus tres preguntas sin responder —procedimiento, qué pasa con el dominio durante la transición y capacidad de disco—, y la decisión que depende de ella, en [[task-103]]. El cuello de botella no es de procedimiento: es que el vínculo con Carlos no está hecho, y hacerlo le toca a Rubén, que lo reconoció en la reunión del 4 de septiembre de 2026 (`[45:21]`: «Todavía me falta crear ese vínculo»).

Mientras tanto la plataforma vive en un servidor de Yeeko. Ricardo sostiene que formalizar es lo correcto aunque no haya riesgo técnico; la confianza personal de Rubén existe, la cobertura institucional no.

## Lo que es del STIG y no aplica aquí

El STIG es otro proyecto de la misma CIGU, con repo propio en `~/dev/unam/stig` y completamente independiente de este: otro sistema, otros servidores, otros tickets, otro roadmap. Su máquina virtual, la reunión del 4 de septiembre de 2026 con la DGTIC y el trámite que gestionó Sandy son suyos, y no son precedente ni antecedente de nada del ONIGIES.

El procedimiento de la DGTIC —cómo se levanta un ticket, qué pide el análisis web, cómo se entrega y se da de baja una máquina virtual— está documentado allá, en `system_docs/reference/interlocucion-con-dgtic.md`. **Misma institución, caso distinto:** sirve para saber qué esperar cuando llegue el turno del ONIGIES, nunca como estado de este proyecto.

## La DGTIC

Dirección General de Cómputo y de Tecnologías de Información y Comunicación; «Cómputo UNAM» es el nombre informal con el que estos documentos la llaman. Dos áreas suyas importarán cuando el ONIGIES llegue ahí: la que entrega máquinas virtuales y configura el distribuidor de cargas, y la **Coordinación de Seguridad de la Información**, que hace la revisión de seguridad —el «análisis web»— antes de que un sistema entre en operación. Ninguna de las dos ha visto todavía nada del ONIGIES.
