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
export function useFlowActions(record, appLabel, modelName) {
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

  const commentDialog = ref(false)
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
    if (t.requires_comment) {
      pendingTransition.value = t
      comment.value = ''
      commentDialog.value = true
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
    return ev
  }

  function confirmComment() {
    if (pendingTransition.value)
      return runTransition(pendingTransition.value, comment.value)
  }

  function closeDialog() {
    commentDialog.value = false
    pendingTransition.value = null
  }

  return {
    sending, transitions, hasActions, currentStatus, events,
    commentDialog, pendingTransition, comment,
    blockedDialog, blockedTitle, blockedReasons, block,
    onSelect, runTransition, confirmComment, closeDialog,
  }
}