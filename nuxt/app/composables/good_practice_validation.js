export const YEAR_MIN = 2000
export const currentYear = () => new Date().getFullYear()

const yearInRange = v => {
  const n = Number(v)
  return Number.isInteger(n) && n >= YEAR_MIN && n <= currentYear()
}

// Vigencia válida = ambos años presentes, en rango y coherentes (inicio ≤ fin).
const vigenciaOk = p => {
  if (!p.start_year || !p.end_year) return false
  if (!yearInRange(p.start_year) || !yearInRange(p.end_year)) return false
  return Number(p.start_year) <= Number(p.end_year)
}

const RULES = [
  {
    label: 'Eje y componente',
    check: p => !!(p.axis),
  },
  {
    label: 'Descripción',
    check: p => !!p.description?.trim(),
  },
  {
    label: 'Resultados obtenidos',
    check: p => !!p.results?.trim(),
  },
  {
    label: 'Periodo de vigencia',
    check: vigenciaOk,
  },
  {
    label: 'Al menos una característica marcada',
    check: p => (p.feature_values || []).some(f => f.has_attribute),
  },
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