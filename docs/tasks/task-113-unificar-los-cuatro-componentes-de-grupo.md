---
type: task
id: task-113
title: Unificar los cuatro componentes de grupo de la información base
state: closed
date: 2026-08-11
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
related: ["[[task-96]]", "[[task-101]]", "[[task-107]]"]
---

# Unificar los cuatro componentes de grupo de la información base

Los cuatro componentes de grupo de la sección crecieron por separado y hoy no comparten ni contrato ni presentación. Se homologan.

**El encabezado se pinta una sola vez, en el Panel.** Título, subtítulo e instrucción salen del catálogo ([[task-107]]), y **se extirpan los textos introductorios hardcodeados** de los cuatro hijos — los mismos que [[task-57]] marcaba como redactados por IA y sin validar, y que ahora pasan a ser editables desde el dashboard.

**Contrato homologado:** los cuatro reciben lo mismo — el survey, el catálogo de su grupo y si es editable. Hoy dos reciben los campos del catálogo y dos no, porque arman sus filas desde el catálogo de sectores.

**Montaje:** un mapa estático a nivel de módulo más `<component :is>`. Muere la cadena de condicionales que decide hoy qué hijo pintar. Sin `shallowRef`: el mapa es constante y no necesita reactividad.

**Convención de solo lectura y deshabilitado**, que hoy las dos tablas aplican distinto y hay que homologar. Ricardo la confirmó explícitamente al revisarla —su formulación original invertía los dos términos por un lapsus de escritura, y la versión buena es esta:

- **`readonly`** — la audiencia o el estado del flujo no permiten editar: la revisora mirando, o la IES con el envío ya entregado.
- **`disabled`** — la fila queda excluida **por una respuesta previa**: un «No» en «Está presente» ([[task-112]]), un «No aplica» en autoridades ([[task-56]]).

**Va en el mismo lote que [[task-107]].** El modelo nuevo mata el JSON de campos y con él el contrato que estos componentes consumen: entre una task y la otra el frontend de la sección queda roto. Se ejecutan juntas y se commitean juntas.

La tipografía del módulo vive en [[task-96]]; aquí no se duplica.

## Cierre (2026-08-12, sesión orquestada)

Entregada en `943c7ac`, en el mismo lote y commit que [[task-107]] como estaba mandado. Contrato final de los cuatro hijos: `v-model` del Survey + `:catalog` (el grupo con sus `questions`) + `:editable`, más la prop `invalid` (Set de keys) que [[task-106]] agregó después sin romper la homogeneidad. El nombre de prop quedó `editable` por convención dominante del repo; la distinción de Ricardo vive en los bindings internos (`:readonly="!editable"` vs `:disabled` por respuesta previa). Ajuste posterior de Ricardo: en autoridades la instrucción del grupo la pinta el hijo justo arriba de su tabla (mapa `OWN_INSTRUCTION_GROUPS`), con el bloque de la titular primero. Un rótulo quedó a sabiendas en código: «La persona titular de la institución es:» no es texto de grupo sino de pregunta — sembrarlo como GeneralQuestion es [[task-120]].

## Criterios de aceptación

- [x] El encabezado de cada grupo se pinta una sola vez, desde el catálogo
- [x] Ningún componente de grupo tiene texto introductorio escrito en el código
- [x] Los cuatro componentes reciben el mismo contrato
- [x] El montaje es por mapa estático y `<component :is>`, sin cadena de condicionales
- [x] `readonly` y `disabled` significan lo mismo en las dos tablas
