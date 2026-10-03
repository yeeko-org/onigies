import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from '~/store/auth'
import { useMainStore } from '~/store/index.js'
import { flowRoleOf } from '~/composables/flowRules.js'
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
  axisvalue: { field: 'observable_responses', label: 'observables' },
  observableresponse: {
    field: 'group_responses', label: 'grupos de preguntas' },
  generalpackage: { field: 'general_group_responses', label: 'grupos' },
}

// Solo si el serializer de la raíz aún no trae su `not_sent_message`; el
// mismo texto que `ROOT_NOT_SENT_MESSAGE` del backend.
const ROOT_NOT_SENT_FALLBACK = 'La institución aún no ha enviado esto a '
  + 'revisión; la revisión podrá actuar sobre esta respuesta cuando lo envíe.'

const ADMIN_ROOT_CLOSED = 'El envío ya está cerrado; no admite cambios '
  + 'administrativos.'

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

  /**
   * Compuerta de la raíz: espejo de `flow.permissions.root_turn_errors`.
   * La revisión no transiciona un descendiente mientras la raíz siga en
   * turno de la IES —un grupo «completado» antes de enviar el eje ya tiene
   * rol reviewer, pero el eje no se ha cedido—. Devuelve string[] de
   * motivos para pre-bloquear el menú; el motor lo rechaza en el POST de
   * todos modos. El texto lo da cada raíz (`not_sent_message`), porque solo
   * ella sabe si es un eje, un envío de generales o uno de buenas prácticas.
   */
  function getRootNotInTurn(root) {
    const authStore = useAuthStore()
    if (authStore.flow_role !== 'reviewer') return []
    const rootStatus = byName.value[root?.status]
    if (rootStatus?.role !== 'ies') return []
    return [root?.not_sent_message || ROOT_NOT_SENT_FALLBACK]
  }

  function appliesTo(st, appLabel, modelName) {
    return (st?.applicable_models || []).some(
      ([a, m]) => a === appLabel && m === modelName)
  }

  // Rol de la raíz del flujo; para un objeto raíz, el suyo.
  function rootRole(root) {
    return byName.value[root?.status]?.role || null
  }

  /**
   * Lado de un evento: el rol de quien lo escribió. El catálogo de personas
   * usuarias de la IES solo trae a las suyas y a las revisoras, y el de la
   * revisión a todas las de institución: una persona ausente del catálogo
   * es staff sin institución, o sea del lado de la revisión.
   */
  function eventSide(ev) {
    const user = useMainStore().users_by_id[ev?.user]
    return flowRoleOf(user) || 'reviewer'
  }

  /**
   * Un evento es un cambio administrativo (adr-0023) si su destino no está
   * entre los siguientes legales del origen y trae comentario. El
   * comentario descarta los cambios de dominio que el motor escribe fuera
   * del grafo sin texto (respuesta inicial de un observable, cascada del
   * descarte de bp). Es una derivación: no hay bandera en el evento.
   */
  function isAdminEvent(ev) {
    if (!ev?.to_status || !ev.from_status || !ev.comment) return false
    const from = byName.value[ev.from_status]
    if (!from) return false
    return !(from.next_statuses || []).includes(ev.to_status)
  }

  /**
   * Inicio de la ronda en curso del lado `role`: el evento más reciente de
   * la raíz que la metió a ese lado desde el otro (espejo de
   * `round_started_at`). Los movimientos dentro del mismo lado no abren
   * ronda. `null` = la raíz nunca cambió de lado; `undefined` = la raíz
   * no trae `flow_events` y no se puede saber.
   */
  function roundStartedAt(root, role) {
    const events = root?.flow_events
    if (!Array.isArray(events)) return undefined
    let start = null
    for (const ev of events) {
      if (byName.value[ev.to_status]?.role !== role) continue
      if (ev.from_status && byName.value[ev.from_status]?.role === role)
        continue
      const at = Date.parse(ev.created_at)
      if (start === null || at > start) start = at
    }
    return start
  }

  /**
   * ¿La persona usuaria puede editar o borrar este comentario? Espejo de la
   * guarda del backend: la raíz en su turno, el comentario de su lado (sin
   * importar quién lo escribió) y de la ronda en curso. El motivo de un
   * cambio administrativo solo lo corrige una cuenta de administración, y
   * nadie lo borra (FlowTimeline esconde el bote).
   */
  function canEditComment(ev, root) {
    if (!ev?.comment) return false
    const auth = useAuthStore()
    const role = auth.flow_role
    if (rootRole(root) !== role || eventSide(ev) !== role) return false
    if (isAdminEvent(ev) && !auth.is_admin) return false
    const start = roundStartedAt(root, role)
    // Una raíz sin `flow_events` no deja ver la ronda: se queda la regla de
    // turno y lado, y el backend responde 403 si el comentario es viejo.
    if (start == null) return true
    return Date.parse(ev.created_at) > start
  }

  /**
   * Destinos de la válvula de admin para un registro: lo que la revisión
   * establece (destinos de las transiciones que salen de status de rol
   * reviewer) más los status de rol reviewer, para devolverle el turno;
   * aplicables al modelo y ordenados por prioridad. Se restan el actual y
   * sus `next_statuses`: un destino legal hecho por la válvula quedaría en
   * el timeline como transición normal (isAdminEvent no lo marcaría), así
   * que esos van por el menú de estatus. Cada status del catálogo trae los
   * de su grupo (`admin_targets`); el cálculo del grafo es solo respaldo
   * para un catálogo anterior a ese campo.
   */
  function getAdminTargets(currentName, appLabel, modelName) {
    const current = byName.value[currentName]
    const group = current?.group
    if (!group) return []
    const all = Object.values(byName.value).filter((st) => st.group === group)
    let names = Array.isArray(current.admin_targets)
      ? current.admin_targets : null
    if (!names) {
      const set = new Set()
      for (const st of all) {
        if (st.role !== 'reviewer') continue
        set.add(st.name)
        for (const next of st.next_statuses || []) set.add(next)
      }
      names = [...set]
    }
    const legal = new Set([currentName, ...(current.next_statuses || [])])
    return names
      .map((name) => byName.value[name])
      .filter((st) => st && st.group === group && !legal.has(st.name)
        && appliesTo(st, appLabel, modelName))
      .sort((a, b) => (b.priority || 0) - (a.priority || 0))
  }

  /**
   * Compuerta de la válvula de admin: solo con la raíz del lado de la
   * revisión. Devuelve el motivo para el tooltip del botón bloqueado.
   */
  function getAdminRootBlock(root) {
    const role = rootRole(root)
    if (role === 'reviewer') return []
    if (role === 'ies')
      return [root?.not_sent_message || ROOT_NOT_SENT_FALLBACK]
    return [ADMIN_ROOT_CLOSED]
  }

  return { byName, loaded, ensureStatuses, getStatus,
    canEditContent, getAvailableTransitions, getChildrenNotReady,
    getRootNotInTurn, rootRole, eventSide, isAdminEvent, canEditComment,
    getAdminTargets, getAdminRootBlock }
})
