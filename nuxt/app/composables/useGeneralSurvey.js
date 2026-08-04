import { computed } from 'vue'
import { useMainStore } from '~/store/index.js'

/**
 * Datos de la sección «Información base» (grupo de flujo `gen`) sobre el
 * recurso Survey: listas de sectores del catálogo y lectura/escritura de las
 * filas de PopulationQuantity.
 *
 * Las cuatro banderas del catálogo Sector bastan para armar la sección:
 * `is_main` (las 10 poblaciones núcleo), `is_standard_extra` (las 2 extra de
 * POB-ESTÁNDAR), `is_authority` (las 4 autoridades) e `is_ies_head` (la
 * titular unipersonal). Los sectores sin ninguna —p. ej. «Autoridades y alto
 * funcionariado», de la lista custom del observable 1.13— no se capturan aquí.
 */
export function useGeneralSurvey(survey) {
  const mainStore = useMainStore()

  const allSectors = computed(() => mainStore.cats?.sector || [])
  const mainSectors = computed(
    () => allSectors.value.filter((s) => s.is_main))
  const extraSectors = computed(
    () => allSectors.value.filter((s) => s.is_standard_extra))
  // Las ~12 filas de la tabla de poblaciones, en el orden del catálogo.
  const populationSectors = computed(
    () => [...mainSectors.value, ...extraSectors.value])
  const authoritySectors = computed(
    () => allSectors.value.filter((s) => s.is_authority))
  const iesHead = computed(
    () => authoritySectors.value.find((s) => s.is_ies_head) || null)
  // Los cuerpos colegiados y titulares de instancias: siempre existen, así que
  // la tabla de autoridades no lleva columna «Existe».
  const authorityBodies = computed(
    () => authoritySectors.value.filter((s) => s.id !== iesHead.value?.id))

  const rows = computed(() => survey.value?.population_quantities || [])

  const rowFor = (sectorId) => rows.value.find((r) => r.sector === sectorId)

  /**
   * Materializa una fila editable por cada sector que la sección captura, para
   * que los v-model escriban directo sobre el array que después se persiste.
   * Idempotente: se puede llamar en cada carga del survey.
   */
  function ensureRows() {
    if (!survey.value) return
    if (!Array.isArray(survey.value.population_quantities))
      survey.value.population_quantities = []
    if (!Array.isArray(survey.value.sectors))
      survey.value.sectors = []
    const current = survey.value.population_quantities
    for (const sector of [...populationSectors.value,
      ...authoritySectors.value]) {
      if (!current.some((r) => r.sector === sector.id))
        current.push({
          sector: sector.id, number_men: null, number_women: null, name: '',
        })
    }
  }

  const isSelected = (sectorId) => (survey.value?.sectors || [])
    .includes(sectorId)

  const rowTotal = (sectorId) => {
    const row = rowFor(sectorId)
    if (!row) return null
    if (row.number_men == null && row.number_women == null) return null
    return (row.number_men || 0) + (row.number_women || 0)
  }

  const hasCount = (row) => !!row
    && (row.number_men != null || row.number_women != null)

  /**
   * Payload del PATCH a /survey/{id}/. Se manda el recurso completo (la
   * sección entera vive en un solo Survey), incluidas SIEMPRE las dos claves
   * de sincronización total: `sectors` y `population_quantities`.
   *
   * Qué filas viajan: solo las que llevan algún conteo. La existencia de una
   * población ya vive en `sectors`, así que una fila sin hombres ni mujeres no
   * aporta nada y la sincronización por omisión la borra. Las autoridades no
   * se agregan a `sectors` (no son poblaciones objetivo) y los 2 sectores
   * extra nunca llevan conteo (son estructurales).
   */
  function buildPayload() {
    const data = survey.value
    const clean = (row) => ({
      sector: row.sector,
      number_men: row.number_men,
      number_women: row.number_women,
      name: row.name || '',
    })
    const quantities = []
    for (const sector of mainSectors.value) {
      const row = rowFor(sector.id)
      if (isSelected(sector.id) && hasCount(row)) quantities.push(clean(row))
    }
    for (const sector of authoritySectors.value) {
      const row = rowFor(sector.id)
      if (hasCount(row)) quantities.push(clean(row))
    }
    return {
      id: data.id,
      academic_instances: data.academic_instances,
      admin_instances: data.admin_instances,
      media_plans: data.media_plans,
      superior_plans: data.superior_plans,
      postgraduate_plans: data.postgraduate_plans,
      is_centralized: data.is_centralized,
      sectors: data.sectors || [],
      population_quantities: quantities,
    }
  }

  return {
    allSectors, mainSectors, extraSectors, populationSectors,
    authoritySectors, iesHead, authorityBodies,
    rowFor, ensureRows, isSelected, rowTotal, hasCount, buildPayload,
  }
}
