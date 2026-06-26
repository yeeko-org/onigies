export const YEAR_MIN = 2000
export const currentYear = () => new Date().getFullYear()

const yearInRange = v => {
  const n = Number(v)
  return Number.isInteger(n) && n >= YEAR_MIN && n <= currentYear()
}

// Predicados por campo: única fuente de verdad de la completitud. Los reusan
// tanto la compuerta (RULES → getMissingFields/entry_rules) como las reglas
// inline del formulario en GoodPracticeEditSimple, para que nunca diverjan.
export const hasAxis = p => !!p.axis
export const hasDescription = p => !!p.description?.trim()
export const hasResults = p => !!p.results?.trim()
export const hasFeature = p =>
  (p.feature_values || []).some(f => f.has_attribute)

// Vigencia válida = ambos años presentes, en rango y coherentes (inicio ≤ fin).
export const vigenciaOk = p => {
  if (!p.start_year || !p.end_year) return false
  if (!yearInRange(p.start_year) || !yearInRange(p.end_year)) return false
  return Number(p.start_year) <= Number(p.end_year)
}

const RULES = [
  { label: 'Eje y componente', check: hasAxis },
  { label: 'Descripción', check: hasDescription },
  { label: 'Resultados obtenidos', check: hasResults },
  { label: 'Periodo de vigencia', check: vigenciaOk },
  { label: 'Al menos una característica marcada', check: hasFeature },
]

export function getChecklist(practice) {
  if (!practice) return []
  return RULES.map(r => ({ label: r.label, ok: r.check(practice) }))
}

export function getMissingFields(practice) {
  return getChecklist(practice).filter(i => !i.ok).map(i => i.label)
}

export function isPracticeComplete(practice) {
  return !!practice && getMissingFields(practice).length === 0
}

// Calificación de la revisora: una característica marcada por la IES
// (has_attribute) está calificada cuando tiene final_option. La opción
// abierta "Otra" (is_other) no tiene escala 1–5, así que queda exenta.
const featureIdOf = fv => fv.feature?.id ?? fv.feature

// Devuelve los nombres de las características marcadas que aún no tienen
// calificación de la revisora. `features` es el catálogo (cats.feature):
// aporta el nombre legible y el flag is_other para exentar "Otra".
export function getUnratedFeatures(practice, features) {
  const byId = new Map((features || []).map(f => [f.id, f]))
  return (practice?.feature_values || [])
    .filter(fv => fv.has_attribute && fv.final_option == null)
    .map(fv => byId.get(featureIdOf(fv)))
    .filter(f => f && !f.is_other)
    .map(f => f.name)
}

// Reglas Vuetify para un campo de año. Vacío permitido (borrador); con valor,
// debe estar en rango; en 'end' además no puede ser menor que 'start'.
export function yearRules(practice, which) {
  const rangeMsg = `Debe ser un año entre ${YEAR_MIN} y ${currentYear()}`
  const rules = [v => !v || yearInRange(v) || rangeMsg]
  if (which === 'end') {
    const msg = 'El año de fin no puede ser menor al de inicio'
    rules.push(
      v => !v || !practice.start_year ||
        Number(v) >= Number(practice.start_year) || msg)
  }
  return rules
}