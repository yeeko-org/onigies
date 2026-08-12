import { computed, toValue } from 'vue'
import {
  useGeneralSurvey, allowsNoApply, isEmptyValue,
} from '~/composables/useGeneralSurvey.js'

/**
 * Compuerta de contenido de un grupo de «Información base» (task-106):
 * qué le falta responder al grupo para poder marcarse como completado.
 *
 * Guardar nunca valida —la IES captura en varias sesiones—; la compuerta
 * es solo del paso a completado, que es el que compromete el grupo ante
 * la revisión.
 *
 * Reglas madre, iguales en los cuatro grupos: el nulo es «sin responder»
 * y bloquea; el «no» explícito y el «No aplica» eximen lo que cuelga de
 * ellos; y el cero es un dato capturado, nunca un vacío.
 *
 * Cada faltante viaja con una `key` estable que los componentes usan
 * para pintar el error en el campo exacto, y con el texto que lo nombra
 * en el resumen: el criterio es señalar QUÉ falta, no solo que falta.
 */

// Los tres conteos de una fila, en el orden de captura (Mujeres antes
// que Hombres, convención de toda la sección).
const COUNT_FIELDS = [
  { field: 'number_women', label: 'mujeres' },
  { field: 'number_men', label: 'hombres' },
  { field: 'number_non_binary', label: 'personas no binarias' },
]

export function useGeneralValidation(survey, catalog) {
  const { populationSectors, authorityBodies, iesHead,
    rowFor, isQuestionNoApply } = useGeneralSurvey(survey)

  const group = computed(() => toValue(catalog) || {})
  const groupName = computed(() => group.value.name || '')
  const questions = computed(() => group.value.questions || [])

  // La columna no binaria solo se exige si la institución declaró que
  // mide esa población: sin esa capacidad ni siquiera se pinta.
  const measuresNonBinary = computed(
    () => survey.value?.measures_non_binary === true)

  const countIssues = (sector, issues) => {
    const row = rowFor(sector.id)
    for (const { field, label } of COUNT_FIELDS) {
      if (field === 'number_non_binary' && !measuresNonBinary.value) continue
      if (isEmptyValue(row?.[field]))
        issues.push({
          key: `count:${sector.id}:${field}`,
          label: `${sector.name}: falta el conteo de ${label}.`,
        })
    }
  }

  const populationIssues = () => {
    const issues = []
    if (survey.value?.measures_non_binary == null)
      issues.push({
        key: 'question:measures_non_binary',
        label: 'Falta indicar si su institución contempla la categoría '
          + 'no binaria.',
      })
    for (const sector of populationSectors.value) {
      const row = rowFor(sector.id)
      if (row?.is_present == null) {
        issues.push({
          key: `presence:${sector.id}`,
          label: `${sector.name}: falta indicar si está presente.`,
        })
        continue
      }
      // Las 2 poblaciones extra son estructurales: declaran presencia y
      // nunca se cuentan. El «no» exime al resto del renglón.
      if (row.is_present === true && sector.is_main)
        countIssues(sector, issues)
    }
    return issues
  }

  const authorityIssues = () => {
    const issues = []
    // La titular es unipersonal y no tiene escape: su sexo y género se
    // guarda como un 1 en el conteo que corresponde.
    if (iesHead.value) {
      const row = rowFor(iesHead.value.id)
      const answered = row && (row.number_women === 1 || row.number_men === 1
        || row.number_non_binary === 1)
      if (!answered)
        issues.push({
          key: 'head',
          label: 'Falta indicar el sexo y género de la persona titular '
            + 'de la institución.',
        })
    }
    for (const sector of authorityBodies.value) {
      if (rowFor(sector.id)?.no_apply === true) continue
      countIssues(sector, issues)
    }
    return issues
  }

  // Grupos que responden sobre columnas del Survey, una por pregunta del
  // catálogo (estructuras, planes de estudio y forma de gobierno).
  const questionIssues = () => {
    const issues = []
    for (const question of questions.value) {
      if (allowsNoApply(question) && isQuestionNoApply(question.id)) continue
      if (isEmptyValue(survey.value?.[question.name]))
        issues.push({
          key: `question:${question.name}`,
          label: `Falta la respuesta: ${question.text}`,
        })
    }
    return issues
  }

  const issues = computed(() => {
    if (!survey.value) return []
    if (groupName.value === 'poblaciones') return populationIssues()
    if (groupName.value === 'autoridades') return authorityIssues()
    return questionIssues()
  })

  return { issues }
}
