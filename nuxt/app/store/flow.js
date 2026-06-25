import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from '~/store/auth'
import { devWarn } from '~/utils/log.js'

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

  return { byName, loaded, ensureStatuses, getStatus, canEditContent,
    getAvailableTransitions }
})
