<script setup>
/**
 * El cuestionario principal de un eje (flujo `cp`). El eje es la unidad de
 * envío y la raíz del flujo; cada observable, la unidad de trabajo
 * (CpObservablePanel).
 *
 * Dos audiencias sobre el mismo árbol, separadas por la prop `review`:
 * - IES (/respuestas, sin `review`): captura, y la compuerta de respuesta
 *   (`cp_capture`) del backend manda sobre todo lo capturable: cerrada, ve
 *   el cuestionario completo pero no responde ni transiciona.
 * - Revisión (dashboard, `review`): contenido de solo lectura; transiciona,
 *   comenta y ve adjuntos. La compuerta solo detiene a la IES (el motor no
 *   la aplica a la revisión), así que aquí no apaga nada: solo se informa.
 */
import { useAuthStore } from '~/store/auth.js'
import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import { useFlowStore } from '~/store/flow.js'
import { useIesStore } from '~/store/ies.js'
import { useFlowActions } from '~/composables/useFlowActions.js'
import { useDates } from '~/composables/useDates.js'
import {
  applyObservableState, countByStatus, countInTurn, resolvedCount,
} from '~/utils/cp_capture.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import FlowStatusActions from
  '~/components/dashboard/flow/FlowStatusActions.vue'
import FlowTransitionDialogs from
  '~/components/dashboard/flow/FlowTransitionDialogs.vue'
import FlowComments from '~/components/dashboard/flow/FlowComments.vue'
import CpObservablePanel from './CpObservablePanel.vue'
import CpStatusCounts from './CpStatusCounts.vue'

const props = defineProps({
  // Id del AxisValue (se pide al backend) u objeto ya completo: el
  // EditSimple del dashboard solo recibe v-model y ya trae el detalle.
  axisValueId: { type: Number, default: null },
  axisValue: { type: Object, default: null },
  review: Boolean,
})

// Resumen del eje con la forma del renglón de lista (status y conteo de
// observables): el dashboard lo fusiona en la fila colapsada.
const emit = defineEmits(['flow-changed'])

const authStore = useAuthStore()
const mainStore = useMainStore()
const dashStore = useDashboardStore()
const flowStore = useFlowStore()
const iesStore = useIesStore()
const route = useRoute()
const { formatLongDate } = useDates()
const { $api } = useNuxtApp()

const axis = ref(null)
const loading = ref(false)
// Paneles abiertos por componente: un v-expansion-panels por componente.
const openPanels = ref({})

async function load() {
  if (props.axisValue) {
    axis.value = props.axisValue
    return
  }
  if (!props.axisValueId) return
  loading.value = true
  try {
    const res = await mainStore.getSimple(
      ['axis_value', props.axisValueId],
      'No se pudo cargar el cuestionario del eje')
    if (res.data) axis.value = res.data
  } finally {
    loading.value = false
  }
}

watch(() => props.axisValue || props.axisValueId, load, { immediate: true })

const capture = computed(() => axis.value?.cp_capture || {})
const captureOpen = computed(() => capture.value.open === true)
// Quién ve el módulo de estatus: la IES solo con la compuerta abierta.
const showFlow = computed(() => props.review || captureOpen.value)

const gateMessage = computed(() => {
  if (props.review || captureOpen.value || !capture.value.reason) return ''
  if (capture.value.reason === 'gen_not_approved')
    return 'Tu información base todavía no está validada; hasta entonces '
      + 'puedes consultar el cuestionario pero no responderlo.'
  if (capture.value.open_at)
    return 'El cuestionario se abrirá a respuestas el '
      + `${formatLongDate(capture.value.open_at)}. Mientras tanto puedes `
      + 'consultar sus preguntas.'
  return 'El cuestionario aún no está abierto a respuestas. Mientras '
    + 'tanto puedes consultar sus preguntas.'
})

// La misma compuerta, contada a la revisión: explica por qué la IES no
// avanza, sin detener a quien revisa.
const reviewGateMessage = computed(() => {
  if (!props.review || captureOpen.value || !capture.value.reason)
    return ''
  const prefix = 'La institución aún no puede responder este eje: '
  if (capture.value.reason === 'gen_not_approved')
    return `${prefix}su información base no está validada.`
  if (capture.value.open_at)
    return `${prefix}el cuestionario se abre el `
      + `${formatLongDate(capture.value.open_at)}.`
  return `${prefix}el cuestionario no está abierto a respuestas.`
})

const baseLink = computed(() => ({
  path: route.path, query: { ...route.query, tab: 'base' } }))

// Observables en el orden del instrumento, en tramos por componente: el
// componente solo agrupa a la vista, no participa del flujo.
const sections = computed(() => {
  const result = []
  for (const obs of axis.value?.observable_responses || []) {
    const full = obs.observable_full || {}
    const last = result[result.length - 1]
    if (last && last.id === full.component) last.items.push(obs)
    else result.push({
      id: full.component, name: full.component_name, items: [obs] })
  }
  return result
})

const byStatus = computed(
  () => countByStatus(axis.value?.observable_responses))
const progress = computed(
  () => resolvedCount(byStatus.value, flowStore.getStatus))
// La cola de la revisión: lo que espera su transición en este eje.
const reviewQueue = computed(() => countInTurn(
  axis.value, authStore.flow_role, flowStore.getStatus))
// Mientras el eje no se envía, lo completado aún no es turno de nadie en
// la revisión (review_turn_errors lo detiene): se cuenta como avance de la
// institución, no como cola.
const axisWithIes = computed(
  () => flowStore.getStatus(axis.value?.status)?.role === 'ies')

const brief = computed(() => axis.value && ({
  id: axis.value.id,
  status: axis.value.status,
  observables_by_status: byStatus.value,
}))
watch(brief, (value, old) => {
  if (value && old && JSON.stringify(value) !== JSON.stringify(old))
    emit('flow-changed', value)
})

// --- Sincronía con el servidor ---------------------------------------

/**
 * El motor propaga status hacia arriba (grupo → observable → eje) y los
 * PATCH/POST solo devuelven el objeto tocado: aquí se relee lo demás y se
 * copia sobre los mismos objetos, sin reemplazarlos, para no perder
 * borradores abiertos en otros grupos.
 */
async function sync(observable, { skipObservable = false } = {}) {
  if (observable && !skipObservable) {
    try {
      const { data } = await $api.get(
        `/observable_response/${observable.id}/`)
      applyObservableState(observable, data)
    } catch (e) {
      devWarn('No se pudo releer el observable', e)
    }
  }
  await refreshAxis()
}

async function refreshAxis() {
  if (!axis.value) return
  try {
    const { data } = await $api.get('/axis_value/', {
      params: { institution: axis.value.institution,
        period: axis.value.period },
    })
    const rows = data.results || data
    const fresh = rows.find((row) => row.id === axis.value.id)
    if (fresh) axis.value.status = fresh.status
    // Las fichas de /respuestas leen los ejes del perfil: se mantienen al
    // día sin volver a pedirlo.
    for (const survey of iesStore.surveys || [])
      for (const av of survey.axis_values || []) {
        const row = rows.find((r) => r.id === av.id)
        if (!row) continue
        av.status = row.status
        av.observables_by_status = row.observables_by_status
      }
  } catch (e) {
    devWarn('No se pudo releer el status del eje', e)
  }
}

// --- Paso del eje -----------------------------------------------------

const highlight = ref(false)
watch(() => axis.value?.status, () => { highlight.value = false })

const axisActions = useFlowActions(axis, 'survey', 'axisvalue', {
  onTransitioned: () => refreshAxis(),
})

// Tras cambiar un observable: si el eje ya puede cederse al otro rol
// (regla de hijos cumplida), se ofrece el paso; nunca se da solo. Con
// más de un destino posible (la revisión: aprobar o pedir ajustes) no se
// elige por nadie: se resalta el status del eje y se avisa.
function offerAxisStep() {
  const ready = axisActions.transitions.value.filter(
    (tr) => tr.role !== authStore.flow_role && !tr.blocked)
  if (!ready.length) return
  highlight.value = true
  const name = axis.value.axis_full?.short_name || 'el eje'
  const msg = `Todos los observables de ${name} están listos.`
  if (ready.length > 1) {
    dashStore.showSnackbar(`${msg} Elige el siguiente paso en el status `
      + 'del eje.')
    return
  }
  const t = ready[0]
  dashStore.showSnackbar(msg, {
    label: t.action_name || t.public_name,
    handler: () => axisActions.onSelect(t) })
}
</script>

<template>
  <div>
    <v-progress-linear v-if="loading" indeterminate color="primary" />
    <v-card v-else-if="axis" elevation="6" class="pa-3">
      <v-card-title class="d-flex align-start flex-wrap ga-3 text-wrap">
        <v-icon start :color="axis.axis_full?.color" class="mt-1">
          {{ axis.axis_full?.icon }}
        </v-icon>
        <span class="mt-1">
          Eje {{ axis.axis_full?.order }}. {{ axis.axis_full?.name }}
        </span>
        <v-spacer />
        <div
          class="cp-axis-status"
          :class="{ 'cp-axis-status--offer': highlight }"
        >
          <FlowStatusActions
            v-if="showFlow"
            v-model="axis"
            app-label="survey"
            model-name="axisvalue"
            :actions="axisActions"
            size="large"
          />
          <FlowStatusChip v-else :status="axis.status" size="large" />
        </div>
        <FlowComments
          v-model="axis"
          app-label="survey"
          model-name="axisvalue"
          :width="200"
          :readonly="!showFlow"
          class="mt-1"
        />
      </v-card-title>

      <v-card-text
        v-if="axis.axis_full?.description"
        class="py-1 text-body-2 text-grey-darken-1 font-italic"
      >
        {{ axis.axis_full.description }}
      </v-card-text>

      <v-card-text class="d-flex align-center flex-wrap ga-2 py-2">
        <span
          v-if="review && axisWithIes"
          class="text-body-2 text-grey-darken-1 mr-2"
          data-testid="cp-review-queue"
        >
          <v-icon size="18" start>schedule</v-icon>
          {{ reviewQueue.observables }} completados por la institución, eje
          sin enviar
        </span>
        <span
          v-else-if="review"
          class="text-body-2 mr-2"
          :class="reviewQueue.observables || reviewQueue.groups
            ? 'text-high-emphasis font-weight-medium'
            : 'text-grey-darken-1'"
          data-testid="cp-review-queue"
        >
          <v-icon size="18" start>flag</v-icon>
          En turno de la revisión: {{ reviewQueue.observables }}
          {{ reviewQueue.observables === 1 ? 'observable' : 'observables' }}
          y {{ reviewQueue.groups }}
          {{ reviewQueue.groups === 1 ? 'grupo' : 'grupos' }}
        </span>
        <span v-else class="text-body-2 text-grey-darken-1 mr-2">
          {{ progress.resolved }}/{{ progress.total }} observables sin
          captura pendiente
        </span>
        <CpStatusCounts :counts="byStatus" />
      </v-card-text>

      <v-alert
        v-if="gateMessage"
        type="info"
        variant="tonal"
        icon="lock_clock"
        class="mx-3 my-2"
      >
        {{ gateMessage }}
        <div v-if="capture.reason === 'gen_not_approved'" class="mt-2">
          <NuxtLink :to="baseLink">Ir a Información base</NuxtLink>
        </div>
      </v-alert>
      <v-alert
        v-if="reviewGateMessage"
        type="info"
        variant="tonal"
        density="compact"
        icon="lock_clock"
        class="mx-3 my-2"
      >
        {{ reviewGateMessage }}
      </v-alert>

      <v-card-text>
        <div v-for="section in sections" :key="section.id" class="mb-6">
          <div class="text-overline text-grey-darken-1 mb-1">
            {{ section.name }}
          </div>
          <v-expansion-panels
            v-model="openPanels[section.id]"
            multiple
            variant="accordion"
          >
            <CpObservablePanel
              v-for="obs in section.items"
              :key="obs.id"
              :model-value="obs"
              :axis="axis"
              :a-options="axis.a_options"
              :gen-denominators="axis.gen_denominators"
              :capture-open="captureOpen"
              :review="review"
              :sync="sync"
              @observable-changed="offerAxisStep"
            />
          </v-expansion-panels>
        </div>
      </v-card-text>

      <FlowTransitionDialogs :actions="axisActions" />
    </v-card>
  </div>
</template>

<style scoped>
.cp-axis-status {
  border-radius: 8px;
  padding: 4px;
  transition: box-shadow 0.3s;
}
.cp-axis-status--offer {
  box-shadow: 0 0 0 2px rgb(var(--v-theme-accent));
}
</style>
