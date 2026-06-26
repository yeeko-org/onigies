import { useDashboardStore } from '~/store/dash.js'
import { useFlowStore } from '~/store/flow.js'
import { useFlow } from '~/composables/useFlow.js'
import { runEntryRules } from '~/composables/flowRules.js'

/**
 * Kernel headless del control de estado: toda la lógica que antes vivía dentro
 * de FlowStatusActions (transiciones disponibles, compuerta de entry_rules,
 * diálogo de comentario y ejecución con mutación en sitio del registro), sin
 * presentación.
 *
 * `record` es un ref al registro completo (status + flow_events + id); se muta
 * en sitio al transicionar para que chip, hint y timeline se refresquen sin
 * recargar. `appLabel`/`modelName` pueden ser valores o getters.
 */
export function useFlowActions(record, appLabel, modelName, options = {}) {
  const dashStore = useDashboardStore()
  const flowStore = useFlowStore()
  const { sending, transition } = useFlow(
    () => toValue(appLabel), () => toValue(modelName),
    () => record.value?.id)

  const transitions = computed(() => flowStore.getAvailableTransitions(
    record.value?.status, toValue(appLabel), toValue(modelName)))
  const hasActions = computed(() => transitions.value.length > 0)
  const currentStatus = computed(
    () => flowStore.getStatus(record.value?.status))
  const events = computed(() => record.value?.flow_events || [])

  const actionDialog = ref(false)
  const pendingTransition = ref(null)
  const comment = ref('')

  const blockedDialog = ref(false)
  const blockedTitle = ref('')
  const blockedReasons = ref([])

  function block(title, reasons) {
    blockedTitle.value = title
    blockedReasons.value = reasons
    blockedDialog.value = true
  }

  // Devuelve el FlowEvent si transicionó; null si abrió un diálogo (bloqueo o
  // comentario) o falló. El consumidor usa el retorno para decidir, p.ej.,
  // cerrar su diálogo solo cuando el cambio realmente ocurrió.
  async function onSelect(t) {
    const { ok, missing } = runEntryRules(t.entry_rules, record.value)
    if (!ok) {
      block(`Aún no puedes pasar a "${t.public_name}"`, missing)
      return null
    }
    const childMissing = flowStore.getChildrenNotReady(
      record.value, t, toValue(modelName))
    if (childMissing.length) {
      block(`Aún no puedes pasar a "${t.public_name}"`, childMissing)
      return null
    }
    // Un solo diálogo cubre confirmación y/o comentario (opcional u
    // obligatorio); solo la transición sin nada se ejecuta directo.
    if (t.requires_confirmation || t.comment_type !== 'none') {
      pendingTransition.value = t
      comment.value = ''
      actionDialog.value = true
      return null
    }
    return runTransition(t, '')
  }

  async function runTransition(t, commentText) {
    const ev = await transition(t.name, commentText)
    if (!ev) return null
    closeDialog()
    record.value.status = ev.to_status
    if (!record.value.flow_events)
      record.value.flow_events = []
    record.value.flow_events.push(ev)
    dashStore.showSnackbar(`Estado cambiado a "${t.public_name}"`)
    await options.onTransitioned?.(ev)
    return ev
  }

  // El comentario va siempre en el evento: vacío si comment_type es 'none' u
  // 'optional' sin texto; el motor valida el obligatorio.
  function confirmAction() {
    const t = pendingTransition.value
    if (!t) return
    return runTransition(t, comment.value)
  }

  function closeDialog() {
    actionDialog.value = false
    pendingTransition.value = null
    comment.value = ''
  }

  return {
    sending, transitions, hasActions, currentStatus, events,
    actionDialog, pendingTransition, comment,
    blockedDialog, blockedTitle, blockedReasons, block,
    onSelect, runTransition, confirmAction, closeDialog,
  }
}