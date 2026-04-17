const RULES = [
  {
    label: 'Eje y componente',
    check: p => !!(p.axis && p.component),
  },
  {
    label: 'Periodo de vigencia',
    check: p => !!(p.start_year && p.end_year),
  },
  {
    label: 'Descripción o Resultados Obtenidos',
    check: p => !!p.description?.trim() || !!p.results?.trim(),
  },
  {
    label: 'Al menos una característica marcada',
    check: p => (p.feature_values || []).some(f => f.has_attribute),
  },
]

export function getMissingFields(practice) {
  if (!practice) return []
  return RULES.filter(r => !r.check(practice)).map(r => r.label)
}

export function isPracticeComplete(practice) {
  return !!practice && getMissingFields(practice).length === 0
}