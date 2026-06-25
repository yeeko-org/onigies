import { getMissingFields } from '~/composables/good_practice_validation.js'
import { useFlowStore } from '~/store/flow.js'
import { devWarn } from '~/utils/log.js'

/**
 * Compuerta de UX para enviar un paquete: lista los motivos por los que aún no
 * se puede (prácticas que siguen en turno de la IES, es decir, sin marcar como
 * completadas). Mira el catálogo (role del status de cada hijo); la regla dura
 * (todas en bp_completed) la enforced el motor vía valid_child_statuses.
 */
function getPackageNotReady(pkg) {
  const practices = pkg?.good_practices || []
  if (!practices.length)
    return ['Aún no has agregado ninguna buena práctica.']
  const flowStore = useFlowStore()
  return practices
    .filter(p => {
      const st = flowStore.getStatus(p.status)
      return !st || st.role === 'ies'
    })
    .map(p => `${p.name || 'Sin nombre'}: márcala como completada.`)
}

/**
 * Registry de reglas de UX del flujo: nombre → función(obj) → string[] de
 * faltantes ([] = cumple). El catálogo de status (Status.entry_rules) nombra
 * las reglas que deben cumplirse para mover un objeto a ese status; aquí viven
 * sus implementaciones. Reusa la validación de buenas prácticas.
 */
const RULES = {
  practice_complete: getMissingFields,
  package_ready: getPackageNotReady,
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