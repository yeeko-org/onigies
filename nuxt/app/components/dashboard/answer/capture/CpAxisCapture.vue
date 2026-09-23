<script setup>
/**
 * La pestaña de un eje en /respuestas: el cuestionario principal del eje
 * (flujo `cp`) para la IES. El eje es la unidad de envío y la raíz del
 * flujo; cada observable, la unidad de trabajo (CpObservablePanel).
 *
 * La compuerta de respuesta (`cp_capture`) viene del backend y manda
 * sobre todo lo capturable: cerrada, la IES ve el cuestionario completo
 * pero no responde ni transiciona.
 */
import { useAuthStore } from '~/store/auth.js'
import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import { useFlowStore } from '~/store/flow.js'
import { useIesStore } from '~/store/ies.js'
import { useFlowActions } from '~/composables/useFlowActions.js'
import { useDates } from '~/composables/useDates.js'
import {
  applyObservableState, countByStatus, resolvedCount,
} from '~/utils/cp_capture.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import FlowStatusActions from
  '~/components/dashboard/flow/FlowStatusActions.vue'
import FlowTransitionDialogs from
  '~/components/dashboard/flow/FlowTransitionDialogs.vue'
import FlowComments from '~/components/dashboard/flow/FlowComments.vue'
import CpObservablePanel from './CpObservablePanel.vue'

const props = defineProps({
  axisValueId: { type: Number, required: true },
})

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

watch(() => props.axisValueId, load, { immediate: true })

const capture = computed(() => axis.value?.cp_capture || {})
const captureOpen = computed(() => capture.value.open === true)

const gateMessage = computed(() => {
  if (captureOpen.value || !capture.value.reason) return ''
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

// Resumen del eje: conteo de observables por status, el más urgente
// primero (priority del catálogo).
const summary = computed(() => {
  const counts = countByStatus(axis.value?.observable_responses)
  return Object.entries(counts)
    .map(([name, count]) => ({ name, count, st: flowStore.getStatus(name) }))
    .filter((row) => row.st)
    .sort((a, b) => (b.st.priority || 0) - (a.st.priority || 0))
})
const progress = computed(() => resolvedCount(
  countByStatus(axis.value?.observable_responses), flowStore.getStatus))

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

// --- Envío del eje ----------------------------------------------------

const highlight = ref(false)
watch(() => axis.value?.status, () => { highlight.value = false })

const axisActions = useFlowActions(axis, 'survey', 'axisvalue', {
  onTransitioned: () => refreshAxis(),
})

// Tras cambiar un observable: si el eje ya puede cederse a la revisión
// (regla de hijos cumplida), se ofrece el envío; nunca se da solo.
function offerAxisStep() {
  const t = axisActions.transitions.value.find(
    (tr) => tr.role !== authStore.flow_role && !tr.blocked)
  if (!t) return
  highlight.value = true
  const name = axis.value.axis_full?.short_name || 'el eje'
  dashStore.showSnackbar(
    `Todos los observables de ${name} están listos.`,
    { label: t.action_name || t.public_name,
      handler: () => axisActions.onSelect(t) })
}
</script>

<template>
  <div>
    <v-progress-linear v-if="loading" indeterminate color="primary" />
    <template v-else-if="axis">
      <v-card variant="flat" class="mb-4">
        <div class="d-flex align-start flex-wrap ga-3 px-4 pt-3">
          <v-icon :color="axis.axis_full?.color" class="mt-1">
            {{ axis.axis_full?.icon }}
          </v-icon>
          <span class="mt-1 text-h6">{{ axis.axis_full?.name }}</span>
          <v-spacer />
          <div
            class="cp-axis-status"
            :class="{ 'cp-axis-status--offer': highlight }"
          >
            <FlowStatusActions
              v-if="captureOpen"
              v-model="axis"
              app-label="survey"
              model-name="axisvalue"
              :actions="axisActions"
            />
            <FlowStatusChip v-else :status="axis.status" />
          </div>
          <FlowComments
            v-model="axis"
            app-label="survey"
            model-name="axisvalue"
            :width="200"
          />
        </div>
        <v-card-text class="d-flex align-center flex-wrap ga-2 pb-0">
          <span class="text-body-2 text-grey-darken-1 mr-2">
            {{ progress.resolved }}/{{ progress.total }} observables sin
            captura pendiente
          </span>
          <v-chip
            v-for="row in summary"
            :key="row.name"
            :color="row.st.color"
            size="small"
            variant="tonal"
          >
            <v-icon start>{{ row.st.icon }}</v-icon>
            {{ row.count }}
            <v-tooltip activator="parent" location="top">
              {{ row.st.public_name }}
            </v-tooltip>
          </v-chip>
        </v-card-text>
      </v-card>

      <v-alert
        v-if="gateMessage"
        type="info"
        variant="tonal"
        icon="lock_clock"
        class="mb-4"
      >
        {{ gateMessage }}
        <div v-if="capture.reason === 'gen_not_approved'" class="mt-2">
          <NuxtLink :to="baseLink">Ir a Información base</NuxtLink>
        </div>
      </v-alert>

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
            :sync="sync"
            @observable-changed="offerAxisStep"
          />
        </v-expansion-panels>
      </div>

      <FlowTransitionDialogs :actions="axisActions" />
    </template>
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
