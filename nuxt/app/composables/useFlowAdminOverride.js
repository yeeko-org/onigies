import { useAuthStore } from '~/store/auth'
import { useDashboardStore } from '~/store/dash.js'
import { useFlowStore } from '~/store/flow.js'
import { useFlow } from '~/composables/useFlow.js'

/**
 * Kernel de la válvula de admin (adr-0023, task-190): lleva un hijo o nieto
 * a cualquier status que la revisión establece, saltando el rol propio y
 * `next_statuses`, mientras la raíz esté del lado de la revisión. Hermano de
 * useFlowActions y no parte de él: no comparte entry_rules, regla de hijos
 * ni diálogo de bloqueo, y así el kernel normal no carga lógica de admin.
 *
 * `record` es un ref al registro (se muta en sitio al aplicar);
 * `appLabel`/`modelName` valores o getters. `options.root` (valor, ref o
 * getter) es la raíz del flujo, sin la cual no hay válvula;
 * `options.onTransitioned(ev)` se espera tras la mutación y el snackbar.
 */
export function useFlowAdminOverride(record, appLabel, modelName,
  options = {}) {
  const authStore = useAuthStore()
  const dashStore = useDashboardStore()
  const flowStore = useFlowStore()
  const { sending, adminTransition } = useFlow(
    () => toValue(appLabel), () => toValue(modelName),
    () => record.value?.id)

  const root = computed(() => toValue(options.root) || null)
  const available = computed(() => authStore.is_admin && !!root.value)
  const rootBlocked = computed(
    () => root.value ? flowStore.getAdminRootBlock(root.value) : [])
  const targets = computed(() => flowStore.getAdminTargets(
    record.value?.status, toValue(appLabel), toValue(modelName)))

  const dialog = ref(false)
  const target = ref(null)
  const comment = ref('')
  const canSubmit = computed(() => !!target.value
    && target.value !== record.value?.status && !!comment.value.trim())

  function open() {
    if (!available.value || rootBlocked.value.length) return
    target.value = null
    comment.value = ''
    dialog.value = true
  }

  function close() {
    dialog.value = false
  }

  // En error el diálogo queda abierto con lo escrito (useFlow ya notificó).
  async function submit() {
    if (sending.value || !canSubmit.value) return null
    if (rootBlocked.value.length) {
      dashStore.showError(rootBlocked.value[0])
      return null
    }
    const ev = await adminTransition(target.value, comment.value)
    if (!ev) return null
    close()
    record.value.status = ev.to_status
    if (!record.value.flow_events)
      record.value.flow_events = []
    record.value.flow_events.push(ev)
    const name = flowStore.getStatus(ev.to_status)?.public_name
      || ev.to_status
    dashStore.showSnackbar(
      `Estatus cambiado a "${name}" por cambio administrativo.`)
    await options.onTransitioned?.(ev)
    return ev
  }

  return {
    root, available, rootBlocked, targets,
    dialog, target, comment, sending, canSubmit,
    open, close, submit,
  }
}
