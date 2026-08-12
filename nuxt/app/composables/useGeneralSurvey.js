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
 * Pregunta del catálogo del grupo por su clave estable (`name`). Los
 * grupos con comportamiento propio (forma de gobierno, la previa de
 * poblaciones) la buscan por nombre porque su render no es genérico.
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
 * Quién ofrece «No aplica» lo declara el seed, no el código: hoy son las
 * tres preguntas de planes de estudio (una IES puede no impartir un nivel,
 * y sin la casilla su cero sería indistinguible de «no lo ofrecemos»).
 */
export const allowsNoApply = (question) =>
  question?.addl_config?.allow_no_apply === true

/**
 * Columna de la fila de respuesta donde aterriza el valor: el `q_type` de
 * la pregunta decide cuál de las dos tipadas aplica.
 */
const valueField = (question) =>
  (question?.q_type === 'boolean' ? 'value_boolean' : 'value_integer')

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

  // Respuesta y metadatos de cada pregunta escalar (task-117): valor y
  // «No aplica» viven en la misma fila, para que agregar una pregunta no
  // exija una columna nueva en Survey.
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
      row = {
        general_question: questionId, no_apply: false,
        value_integer: null, value_boolean: null,
      }
      survey.value.question_responses.push(row)
    }
    return row
  }

  const isQuestionNoApply = (questionId) =>
    responseFor(questionId)?.no_apply === true

  const questionValue = (question) => {
    const row = responseFor(question?.id)
    return row ? row[valueField(question)] ?? null : null
  }

  // La fila se materializa al responder, no al pintar: solo las preguntas
  // que alguien tocó necesitan viajar al servidor.
  const setQuestionValue = (question, value) => {
    const row = ensureQuestionRow(question?.id)
    if (row) row[valueField(question)] = value ?? null
  }

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
    // El vacío de un v-count-input borrado llega como '' o NaN y el
    // backend solo entiende `None`: se normaliza aquí, no allá.
    const scalar = (value) => (isEmptyValue(value) ? null : value)
    const responses = questionRows.value
      .filter((r) => r.general_question)
      .map((r) => {
        const noApply = r.no_apply === true
        return {
          general_question: r.general_question,
          no_apply: noApply,
          value_integer: noApply ? null : scalar(r.value_integer),
          value_boolean: noApply ? null : scalar(r.value_boolean),
        }
      })
    return {
      id: data.id,
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
    questionValue, setQuestionValue, buildPayload,
  }
}
