/**
 * Secciones del registro de una IES y su publicación.
 *
 * Una sección es lo que la IES ve como pestaña en /respuestas: la
 * granularidad es gruesa —el cuestionario principal cuenta como una sola
 * sección aunque se despliegue en un tab por eje—, porque lo que se abre o
 * se cierra es el instrumento completo, no cada eje por separado.
 *
 * `PUBLISHED_SECTIONS` es una constante y no un dato en la base: mientras el
 * desarrollo va sección por sección, publicar una es un cambio de código que
 * se despliega junto con la sección misma. Las instituciones marcadas
 * `is_test` ven todo, para poder probar y demostrar lo que aún no se abre.
 *
 * Fuente única de los dos lugares que enumeran secciones: las pestañas de
 * `pages/respuestas/[period].vue` y los chips de `pages/respuestas/index.vue`.
 * La revisora no pasa por /respuestas, así que esto no la afecta.
 */

export const SECTION_BASE = 'base'
export const SECTION_CP = 'cp'
export const SECTION_BP = 'bp'

// En el orden en que se presentan a la IES.
export const ALL_SECTIONS = [SECTION_BASE, SECTION_CP, SECTION_BP]

export const PUBLISHED_SECTIONS = [SECTION_BP]

/**
 * Sección a la que pertenece un valor de pestaña. Los ejes usan pestañas
 * `axis-{id}` y todos caen en la misma sección `cp`.
 */
export function sectionOfTab(tab) {
  if (!tab) return null
  if (String(tab).startsWith('axis-')) return SECTION_CP
  return ALL_SECTIONS.includes(tab) ? tab : null
}

export function visibleSections(is_test = false) {
  return is_test ? ALL_SECTIONS : PUBLISHED_SECTIONS
}

export function isSectionVisible(section, is_test = false) {
  return visibleSections(is_test).includes(section)
}
