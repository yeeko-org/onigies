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
/**
 * Pregunta del catálogo del grupo por su clave estable (`name`), que es
 * también la columna del Survey donde aterriza la respuesta. Los grupos
 * con comportamiento propio (forma de gobierno, la previa de poblaciones)
 * la buscan por nombre porque su render no es genérico.
 */
export const questionByName = (catalog, name) =>
  (catalog?.questions || []).find((q) => q.name === name) || null

/**
 * Vacío para la validación y para los conteos: el cero es un dato
 * capturado, nunca una casilla sin responder. `NaN` entra porque un
 * v-number-input borrado puede emitirlo antes de asentar en nulo.
 */
export const isEmptyValue = (value) => value == null || value === ''
  || (typeof value === 'number' && Number.isNaN(value))

/**
 * Preguntas que ofrecen «No aplica». Son las tres de planes de estudio:
 * una IES puede no impartir un nivel educativo, y sin la casilla su cero
 * sería indistinguible de «no ofrecemos ese nivel». Las instancias no la
 * llevan: toda institución tiene estructura.
 */
export const NO_APPLY_QUESTIONS = [
  'media_plans', 'superior_plans', 'postgraduate_plans']

export const allowsNoApply = (question) =>
  NO_APPLY_QUESTIONS.includes(question?.name)

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
  // Los cuerpos colegiados y titulares de instancias: la tabla de autoridades
  // no declara presencia, su escape es el «No aplica» por renglón.
  const authorityBodies = computed(
    () => authoritySectors.value.filter((s) => s.id !== iesHead.value?.id))

  const rows = computed(() => survey.value?.population_quantities || [])

  const rowFor = (sectorId) => rows.value.find((r) => r.sector === sectorId)

  const EMPTY_COUNTS = {
    number_women: null, number_men: null, number_non_binary: null,
  }

  /**
   * Materializa una fila editable por cada sector que la sección captura, para
   * que los v-model escriban directo sobre el array que después se persiste.
   * Idempotente: se puede llamar en cada carga del survey.
   */
  function ensureRows() {
    if (!survey.value) return
    if (!Array.isArray(survey.value.population_quantities))
      survey.value.population_quantities = []
    const current = survey.value.population_quantities
    for (const sector of [...populationSectors.value,
      ...authoritySectors.value]) {
      if (!current.some((r) => r.sector === sector.id))
        current.push({
          sector: sector.id, is_present: null, no_apply: false,
          ...EMPTY_COUNTS, name: '',
        })
    }
  }

  // Metadatos por pregunta (hoy solo el «No aplica»): viven en filas
  // aparte porque el valor sigue siendo una columna del Survey, y una
  // columna en nulo no distingue «no aplica» de «sin capturar».
  const questionRows = computed(
    () => survey.value?.question_responses || [])

  const responseFor = (questionId) =>
    questionRows.value.find((r) => r.general_question === questionId)

  /** Materializa la fila de una pregunta para que el v-model escriba
   * directo sobre el array que se persiste. Idempotente. */
  function ensureQuestionRow(questionId) {
    if (!survey.value || !questionId) return null
    if (!Array.isArray(survey.value.question_responses))
      survey.value.question_responses = []
    let row = responseFor(questionId)
    if (!row) {
      row = { general_question: questionId, no_apply: false }
      survey.value.question_responses.push(row)
    }
    return row
  }

  const isQuestionNoApply = (questionId) =>
    responseFor(questionId)?.no_apply === true

  // La existencia vive en la propia fila desde adr-0012; `Survey.sectors`
  // ya no se escribe (es derivado y de solo lectura en el serializer).
  const isPresent = (sectorId) => rowFor(sectorId)?.is_present === true

  // El «no» explícito y el «no aplica» no pueden dejar conteos viejos a la
  // vista: el backend los anula al guardar y aquí se espeja al instante.
  const clearCounts = (sectorId) => {
    const row = rowFor(sectorId)
    if (row) Object.assign(row, EMPTY_COUNTS)
  }

  // Apagar la pregunta previa deja a la vista conteos de una columna que
  // ya no se pinta; el backend los anula al guardar y aquí se espeja al
  // instante, para todas las filas (poblaciones y autoridades).
  const clearNonBinary = () => {
    for (const row of rows.value) row.number_non_binary = null
  }

  const hasCount = (row) => !!row
    && (row.number_men != null || row.number_women != null
      || row.number_non_binary != null)

  const rowTotal = (sectorId) => {
    const row = rowFor(sectorId)
    if (!hasCount(row)) return null
    return (row.number_men || 0) + (row.number_women || 0)
      + (row.number_non_binary || 0)
  }

  /**
   * Payload del PATCH a /survey/{id}/. Se manda el recurso completo (la
   * sección entera vive en un solo Survey). `sectors` ya no viaja: es
   * derivado de las filas y el serializer lo ignora.
   *
   * Qué filas viajan: las que llevan alguna respuesta, aunque no lleven
   * conteo — un «no» explícito o un «no aplica» son respuesta (adr-0012), y
   * el serializer hace upsert sin borrar las omitidas.
   */
  function buildPayload() {
    const data = survey.value
    const hasAnswer = (row) => !!row && (row.is_present != null
      || row.no_apply === true || hasCount(row))
    const clean = (row) => ({
      sector: row.sector,
      is_present: row.is_present ?? null,
      no_apply: row.no_apply === true,
      number_men: row.number_men,
      number_women: row.number_women,
      number_non_binary: row.number_non_binary ?? null,
      name: row.name || '',
    })
    const quantities = []
    for (const sector of [...populationSectors.value,
      ...authoritySectors.value]) {
      const row = rowFor(sector.id)
      if (hasAnswer(row)) quantities.push(clean(row))
    }
    // Las filas de pregunta viajan todas las materializadas: el upsert no
    // borra por omisión, así que desmarcar debe llegar como `false`.
    const responses = questionRows.value
      .filter((r) => r.general_question)
      .map((r) => ({
        general_question: r.general_question,
        no_apply: r.no_apply === true,
      }))
    return {
      id: data.id,
      academic_instances: data.academic_instances,
      admin_instances: data.admin_instances,
      media_plans: data.media_plans,
      superior_plans: data.superior_plans,
      postgraduate_plans: data.postgraduate_plans,
      is_centralized: data.is_centralized,
      measures_non_binary: data.measures_non_binary,
      population_quantities: quantities,
      question_responses: responses,
    }
  }

  return {
    allSectors, mainSectors, extraSectors, populationSectors,
    authoritySectors, iesHead, authorityBodies,
    rowFor, ensureRows, isPresent, clearCounts, clearNonBinary, rowTotal,
    hasCount, responseFor, ensureQuestionRow, isQuestionNoApply,
    buildPayload,
  }
}
