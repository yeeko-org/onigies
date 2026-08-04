import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from '~/store/auth'
import { devWarn } from '~/utils/log.js'

/**
 * Espejo en cliente de la FK registry del backend (flow_parent): para cada
 * modelo participante, el campo donde su serializer Full anida a los hijos y
 * la etiqueta con que nombrarlos en los mensajes. Una raíz con regla de hijos
 * (valid_child_statuses) debe anidarlos en ese campo. Es convención de
 * serialización, no dato de catálogo: por eso vive como const, no como estado.
 */
const CHILD_REGISTRY = {
  goodpracticepackage: { field: 'good_practices', label: 'buenas prácticas' },
  // axisvalue: { field: 'observable_responses', label: 'respuestas' },
  // observableresponse: { field: 'group_responses', label: 'grupos' },
  generalpackage: { field: 'general_group_responses', label: 'grupos' },
}

function childrenOf(record, modelName) {
  const field = CHILD_REGISTRY[modelName]?.field
  return field ? (record?.[field] || []) : []
}

/**
 * Catálogo de status del motor de flujo, cargado una sola vez desde
 * `/flow/statuses/` y cacheado por nombre. Es la única fuente de verdad de
 * display (public_name, color, icon) y de reglas estáticas (role,
 * next_statuses, applicable_models). Los objetos del backend traen `status`
 * como string (el nombre); aquí se resuelve.
 */
export const useFlowStore = defineStore('flow', () => {
  const byName = ref({})
  const loaded = ref(false)

  // Idempotente: solo pega al backend la primera vez.
  async function ensureStatuses() {
    if (loaded.value) return
    const { $api } = useNuxtApp()
    try {
      const { data } = await $api.get('/flow/statuses/')
      const map = {}
      for (const st of data) map[st.name] = st
      byName.value = map
      loaded.value = true
    } catch (e) {
      devWarn('No se pudo cargar el catálogo de status de flujo', e)
    }
  }

  function getStatus(name) {
    return name ? byName.value[name] || null : null
  }

  /**
   * ¿La persona usuaria puede editar el CONTENIDO de un objeto? Son dos
   * permisos, no uno: el RAÍZ gobierna (su rol debe ser el turno del usuario) y
   * el status propio debe ser editable (content_editable). Por defecto la raíz
   * es el propio objeto, para los nodos raíz (p.ej. el GoodPracticePackage en
   * bp); para hijos/nietos se pasa la raíz explícita.
   */
  function canEditContent(obj, root = obj) {
    const authStore = useAuthStore()
    const rootStatus = byName.value[root?.status]
    const ownStatus = byName.value[obj?.status]
    return !!ownStatus?.content_editable
      && rootStatus?.role === authStore.flow_role
  }

  /**
   * Transiciones disponibles para mover un objeto desde su status actual.
   * Replica `get_available_transitions` del backend con datos del catálogo:
   * el turno es del rol del usuario, y el destino aplica al modelo. La regla
   * de hijos NO se evalúa aquí (la valida el POST); igual que el GET viejo.
   */
  function getAvailableTransitions(currentName, appLabel, modelName) {
    const current = byName.value[currentName]
    if (!current || !current.role) return []
    const authStore = useAuthStore()
    if (authStore.flow_role !== current.role) return []
    return (current.next_statuses || [])
      .map((name) => byName.value[name])
      .filter((t) => t && (t.applicable_models || []).some(
        ([a, m]) => a === appLabel && m === modelName))
  }

  /**
   * Compuerta de hijos: replica `_check_children_rule` del motor como pre-check
   * de UX. Si el status destino declara `valid_child_statuses`, TODOS los hijos
   * deben estar en uno de esos status. Devuelve string[] de motivos ([] =
   * cumple) para FlowBlockedDialog; el mensaje lista los status permitidos por
   * su public_name, no nombra al hijo ofensor. La regla dura la enforced el
   * motor en el POST (400); esto solo evita el round-trip fallido.
   */
  function getChildrenNotReady(record, target, modelName) {
    const allowed = target?.valid_child_statuses || []
    if (!allowed.length) return []
    const children = childrenOf(record, modelName)
    if (children.every((c) => allowed.includes(c.status))) return []
    const names = allowed
      .map((name) => getStatus(name)?.public_name || name)
      .join(', ')
    const label = CHILD_REGISTRY[modelName]?.label || 'elementos'
    // Sin artículo ni cuantificador delante del label: este concuerda en
    // género con cada colección («buenas prácticas», «grupos») y una cadena
    // fija se equivocaría en la mitad de los casos.
    return [`Faltan ${label} por alcanzar un status válido: ${names}.`]
  }

  return { byName, loaded, ensureStatuses, getStatus, canEditContent,
    getAvailableTransitions, getChildrenNotReady }
})
