<script setup>
/**
 * Un observable del eje como panel expandible: la unidad de trabajo de la
 * captura. Arriba la pregunta inicial (se guarda sola al cambiar) y el
 * status del observable; debajo los grupos de preguntas, editables solo
 * con la respuesta «Sí» y consultables antes de decidir.
 *
 * Los saltos de status que siguen a un grupo o a la respuesta inicial se
 * OFRECEN (snackbar con acción), nunca se dan solos.
 *
 * Con `review` (dashboard) la respuesta inicial y los grupos son de solo
 * lectura y el módulo de estatus se muestra aunque la compuerta de
 * respuesta esté cerrada: esa compuerta solo detiene a la IES.
 */
import { useAuthStore } from '~/store/auth.js'
import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import { useFlowStore } from '~/store/flow.js'
import { useFlowActions } from '~/composables/useFlowActions.js'
import { useQuestionTypes } from '~/composables/useQuestionTypes.js'
import {
  applyObservableState, attentionGroup as findAttentionGroup,
} from '~/utils/cp_capture.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import FlowStatusActions from
  '~/components/dashboard/flow/FlowStatusActions.vue'
import FlowTransitionDialogs from
  '~/components/dashboard/flow/FlowTransitionDialogs.vue'
import TitleCommon from '~/components/dashboard/common/utils/TitleCommon.vue'
import YesNoRadio from '~/components/dashboard/common/select/YesNoRadio.vue'
import CpGroupIcons from './CpGroupIcons.vue'
import CpGroupCard from './CpGroupCard.vue'

const props = defineProps({
  axis: { type: Object, required: true },
  aOptions: { type: Array, default: () => [] },
  genDenominators: { type: Object, default: () => ({}) },
  captureOpen: Boolean,
  review: Boolean,
  // Refresca desde el servidor los status del observable, de sus grupos
  // y del eje: el motor propaga hacia arriba y el PATCH no lo devuelve.
  sync: { type: Function, required: true },
})

const observable = defineModel({ type: Object, required: true })

const emit = defineEmits(['observable-changed'])

const authStore = useAuthStore()
const mainStore = useMainStore()
const dashStore = useDashboardStore()
const flowStore = useFlowStore()
const { types_by_name } = useQuestionTypes()

const instrument = computed(() => observable.value.observable_full || {})
const groups = computed(() => observable.value.group_responses || [])
const answered = computed(() => observable.value.value !== null
  && observable.value.value !== undefined)
const answeredYes = computed(() => observable.value.value === true)

// Mismo ancho que el título del observable en el dashboard
// (ObservableHeader): dos renglones y el resto en el tooltip.
const TITLE_WIDTH = 520

// El color de «No» y de «sin responder» es el de los status que esas
// respuestas implican (Sin la medida / Por iniciar): el catálogo manda, así
// el ícono y los chips cambian juntos si cambia la paleta.
const INIT_ICONS = {
  true: { icon: 'toggle_on', label: 'Sí' },
  false: { icon: 'toggle_off', status: 'cp_not_present', label: 'No' },
  null: { icon: 'pending', status: 'cp_pre_start', label: 'Sin responder' },
}
const initIcon = computed(() => {
  const item = INIT_ICONS[
    answered.value ? String(observable.value.value) : 'null']
  const color = item.status
    ? flowStore.getStatus(item.status)?.color || 'grey'
    : 'accent'
  return { ...item, color }
})
const title = computed(
  () => `${instrument.value.number} ${instrument.value.name}`)
// El renglón del observable lleva el tinte de su eje, como los paneles del
// dashboard (PanelCommon); el cuerpo abierto queda blanco.
const titleColor = computed(
  () => `${props.axis.axis_full?.color || 'blue-grey'}-lighten-5`)

// La respuesta inicial la da la IES en el turno del eje; el backend
// decide lo demás (revisión activa) y responde 400 con el motivo.
const canAnswer = computed(() => props.captureOpen && !authStore.is_staff
  && flowStore.getStatus(props.axis.status)?.role === authStore.flow_role)

// Atención por regla, no por nombre: el grupo en turno de quien mira con
// prioridad mayor que la del observable (a la IES, uno devuelto con
// ajustes; a la revisión, uno completado en un observable aún en llenado).
const attentionGroup = computed(() => findAttentionGroup(
  observable.value, authStore.flow_role, flowStore.getStatus))
const showFlow = computed(() => props.review || props.captureOpen)

// --- Pregunta inicial -------------------------------------------------

const savingInit = ref(false)

// Apagada mientras la IES aún no puede responder (compuerta cerrada); de
// solo lectura para quien ya no tiene el turno o revisa.
const initDisabled = computed(
  () => (!props.review && !props.captureOpen) || savingInit.value)

async function onInitChange(value) {
  // Volver a «sin responder» no se ofrece.
  if (value === null || value === undefined) return
  if (value === observable.value.value) return
  savingInit.value = true
  try {
    const res = await mainStore.patchSimple(
      ['observable_response', observable.value.id, { value }],
      'No se pudo guardar la respuesta')
    if (res.errors) return
    applyObservableState(observable.value, res.data)
    dashStore.showSnackbar('Respuesta guardada')
    await props.sync(observable.value, { skipObservable: true })
    emit('observable-changed')
  } finally {
    savingInit.value = false
  }
}

// --- Status del observable y ofertas ----------------------------------

const highlight = ref(false)
watch(() => observable.value.status, () => { highlight.value = false })

const obsActions = useFlowActions(
  observable, 'answer', 'observableresponse', {
    root: () => props.axis,
    onTransitioned: async () => {
      await props.sync(observable.value)
      emit('observable-changed')
    },
  })

// Tras mover un grupo: si el observable puede seguirlo al mismo status
// (la regla de hijos ya se cumple), se ofrece el paso.
function offerObservableStep(toStatus) {
  const t = obsActions.transitions.value.find(
    (tr) => tr.name === toStatus && !tr.blocked)
  if (!t) return
  highlight.value = true
  const number = instrument.value.number
  dashStore.showSnackbar(
    `Todos los grupos del observable ${number} están listos.`,
    { label: t.action_name || t.public_name,
      handler: () => obsActions.onSelect(t) })
}

async function onGroupTransitioned(ev) {
  await props.sync(observable.value)
  offerObservableStep(ev?.to_status)
}

async function onGroupSaved({ statusChanged }) {
  if (statusChanged) await props.sync(observable.value)
}

// --- Consulta previa --------------------------------------------------

const showPreview = ref(false)
const previewTypes = computed(() => groups.value.map((g) => ({
  id: g.id,
  icon: types_by_name.value[g.question_type]?.icon || 'help',
  name: types_by_name.value[g.question_type]?.public_name
    || g.question_type,
})))
</script>

<template>
  <v-expansion-panel :value="observable.id" class="cp-observable">
    <v-expansion-panel-title :color="titleColor">
      <div class="d-flex align-center flex-wrap ga-3 pr-2">
        <TitleCommon
          :title_text="title"
          :title_width="TITLE_WIDTH"
          card_class="text-subtitle-1 font-weight-medium"
        />
        <v-icon :color="initIcon.color" size="28">
          {{ initIcon.icon }}
          <v-tooltip activator="parent" location="top">
            Respuesta inicial: {{ initIcon.label }}
          </v-tooltip>
        </v-icon>
        <FlowStatusChip :status="observable.status" x-small />
        <CpGroupIcons
          :groups="groups"
          :highlight-id="attentionGroup?.id ?? null"
          :dimmed="observable.value === false"
        />
      </div>
    </v-expansion-panel-title>

    <v-expansion-panel-text>
      <div class="cp-column">
        <div class="d-flex align-start flex-wrap ga-6 mb-4">
          <div class="cp-init">
            <YesNoRadio
              :model-value="answered ? observable.value : null"
              :label="instrument.init_question"
              label-class="text-body-1 font-weight-medium"
              :readonly="!canAnswer"
              :disabled="initDisabled"
              @update:model-value="onInitChange"
            >
              <template #append>
                <v-progress-circular
                  v-if="savingInit"
                  indeterminate
                  size="20"
                  width="2"
                />
              </template>
            </YesNoRadio>
            <div
              v-if="instrument.note"
              class="cp-note d-flex align-start ga-1 mt-2 text-caption
                text-medium-emphasis"
            >
              <v-icon size="14" class="cp-note__icon">info</v-icon>
              <span>{{ instrument.note }}</span>
            </div>
          </div>
          <div
            v-if="answeredYes"
            class="cp-status-slot"
            :class="{ 'cp-status-slot--offer': highlight }"
          >
            <FlowStatusActions
              v-if="showFlow"
              v-model="observable"
              app-label="answer"
              model-name="observableresponse"
              :actions="obsActions"
              hint="tooltip"
            />
            <FlowStatusChip v-else :status="observable.status" />
          </div>
        </div>

        <v-card
          v-if="!answeredYes"
          variant="flat"
          border
          class="d-flex align-center flex-wrap ga-4 px-4 py-2 mb-4"
        >
          <span class="text-body-2 text-grey-darken-1">
            Preguntas de este observable:
          </span>
          <span
            v-for="item in previewTypes"
            :key="item.id"
            class="d-inline-flex align-center ga-1 text-body-2"
          >
            <v-icon size="18">{{ item.icon }}</v-icon>
            {{ item.name }}
          </span>
          <v-spacer />
          <v-btn
            variant="text"
            :append-icon="showPreview ? 'expand_less' : 'expand_more'"
            @click="showPreview = !showPreview"
          >
            {{ showPreview ? 'Ocultar preguntas' : 'Ver preguntas' }}
          </v-btn>
        </v-card>

        <template v-if="answeredYes || showPreview">
          <CpGroupCard
            v-for="(group, index) in groups"
            :key="group.id"
            v-model="observable.group_responses[index]"
            :observable="instrument"
            :axis="axis"
            :a-options="aOptions"
            :gen-denominators="genDenominators"
            :capture-open="captureOpen"
            :review="review"
            :preview="!answeredYes"
            @saved="onGroupSaved"
            @transitioned="onGroupTransitioned"
          />
        </template>
      </div>

      <FlowTransitionDialogs :actions="obsActions" />
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

<style scoped>
/* La captura se lee en una columna: a lo ancho de un monitor el texto de
   la pregunta y sus radios quedarían a media pantalla de distancia. */
.cp-column {
  max-width: 900px;
}
.cp-init {
  flex: 1 1 0;
  min-width: 320px;
}
.cp-note {
  white-space: pre-line;
}
.cp-note__icon {
  margin-top: 1px;
}
.cp-status-slot {
  border-radius: 8px;
  padding: 4px;
  transition: box-shadow 0.3s;
}
.cp-status-slot--offer {
  box-shadow: 0 0 0 2px rgb(var(--v-theme-accent));
}
</style>
