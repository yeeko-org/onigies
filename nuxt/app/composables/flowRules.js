import {
  getMissingFields, getUnratedFeatures,
} from '~/composables/good_practice_validation.js'
import { useMainStore } from '~/store/index.js'
import { devWarn } from '~/utils/log.js'

/**
 * Registry de reglas de UX del flujo: nombre → función(obj) → string[] de
 * faltantes ([] = cumple). El catálogo de status (Status.entry_rules) nombra
 * las reglas que deben cumplirse para mover un objeto a ese status; aquí viven
 * sus implementaciones. La regla de hijos (valid_child_statuses) NO vive aquí:
 * es un built-in del motor (useFlowStore.getChildrenNotReady).
 */
const RULES = {
  practice_complete: getMissingFields,
  // Toda característica marcada debe estar calificada por la revisora
  // (final_option). Lee cats.feature del store para resolver nombre e is_other.
  features_rated: obj =>
    getUnratedFeatures(obj, useMainStore().cats.feature)
      .map(name => `Falta calificar la característica: ${name}`),
}

/**
 * Rol de una persona usuaria en el motor de flujo. Replica `User.is_reviewer`
 * del backend (is_superuser OR is_staff OR reviewer).
 */
export function flowRoleOf(user) {
  if (!user) return null
  return (user.is_superuser || user.is_staff || user.reviewer)
    ? 'reviewer' : 'ies'
}

/**
 * Evalúa las entry_rules de un status sobre un objeto. Devuelve
 * { ok, missing }, combinando los faltantes de todas las reglas que fallan
 * (para alimentar FlowBlockedDialog).
 */
export function runEntryRules(entryRules, obj) {
  const missing = []
  for (const name of entryRules || []) {
    const fn = RULES[name]
    if (!fn) {
      devWarn(`flowRules: regla desconocida "${name}"`)
      continue
    }
    missing.push(...fn(obj))
  }
  return { ok: missing.length === 0, missing }
}