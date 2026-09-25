<script setup>
/**
 * Un grupo de respuesta (un tipo de pregunta de un observable) como
 * tarjeta: título, status, las preguntas del tipo, evidencia y
 * comentarios.
 *
 * El borrador vive aquí y se guarda por grupo con el split-button de gen
 * y bp («Guardar ▾»: guardar y mantener, o guardar y transicionar): la IES
 * captura en varias sesiones y no hay autoguardado por pregunta. Al
 * guardar, el backend devuelve la compuerta de completado (`completion`),
 * que se muestra sin bloquear el guardado: dice lo que impediría marcar el
 * grupo como completado.
 *
 * Con `review` (dashboard) nada se edita: las respuestas se leen (sin
 * atenuar, a diferencia de la consulta previa de la IES), los adjuntos se
 * ven y quedan el status y los comentarios.
 *
 * El grupo sin captura (`population`, sin `model_response`) solo muestra su
 * status: no se transiciona, no se comenta ni lleva evidencia; su dato vive
 * en información base.
 */
import { useAuthStore } from '~/store/auth.js'
import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import { useFlowStore } from '~/store/flow.js'
import { useFlowActions } from '~/composables/useFlowActions.js'
import { useQuestionTypes } from '~/composables/useQuestionTypes.js'
import {
  CP_TYPES, buildDraft, buildGroupPayload, saveThenTransition,
  transitionDoneBySave,
} from '~/utils/cp_capture.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import FlowStatusActions from
  '~/components/dashboard/flow/FlowStatusActions.vue'
import FlowTransitionDialogs from
  '~/components/dashboard/flow/FlowTransitionDialogs.vue'
import FlowComments from '~/components/dashboard/flow/FlowComments.vue'
import FlowAttachments from '~/components/dashboard/flow/FlowAttachments.vue'
import FlowSaveMenu from '~/components/dashboard/flow/FlowSaveMenu.vue'
import CpQuestionsA from './CpQuestionsA.vue'
import CpQuestionsB from './CpQuestionsB.vue'
import CpQuestionsReach from './CpQuestionsReach.vue'
import CpQuestionsPlan from './CpQuestionsPlan.vue'
import CpQuestionsSpecial from './CpQuestionsSpecial.vue'

const BODIES = {
  a_questions: CpQuestionsA,
  b_questions: CpQuestionsB,
  reach: CpQuestionsReach,
  plans: CpQuestionsPlan,
  special: CpQuestionsSpecial,
}

const props = defineProps({
  // `observable_full` del ObservableResponse: el instrumento.
  observable: { type: Object, required: true },
  // Raíz del flujo (el eje): gobierna quién edita el contenido.
  axis: { type: Object, required: true },
  aOptions: { type: Array, default: () => [] },
  genDenominators: { type: Object, default: () => ({}) },
  captureOpen: Boolean,
  // Consulta previa a responder «Sí»: todo visible, nada editable.
  preview: Boolean,
  review: Boolean,
})

const group = defineModel({ type: Object, required: true })

const emit = defineEmits(['saved', 'transitioned'])

const authStore = useAuthStore()
const mainStore = useMainStore()
const dashStore = useDashboardStore()
const flowStore = useFlowStore()
const route = useRoute()
const { types_by_name } = useQuestionTypes()

const type = computed(() => types_by_name.value[group.value.question_type]
  || { public_name: group.value.question_type })
const spec = computed(() => CP_TYPES[group.value.question_type] || null)
const body = computed(() => BODIES[group.value.question_type] || null)

// Controles apagados cuando la IES no puede responder por ahora
// (compuerta o consulta previa); solo lectura cuando el flujo no le da el
// turno. La revisión siempre lee, y transiciona salvo en la consulta
// previa (observable sin «Sí»: sus grupos no se revisan).
const disabled = computed(
  () => !props.review && (props.preview || !props.captureOpen))
const editable = computed(() => !props.review && !disabled.value
  && !authStore.is_staff
  && flowStore.canEditContent(group.value, props.axis))
const showActions = computed(
  () => (props.review ? !props.preview : !disabled.value))
// Sin captura: el dato vive en información base (criterio del backend,
// `model_response` nulo en el tipo, no el nombre del tipo).
const noCapture = computed(() => !!types_by_name.value[
  group.value.question_type] && !type.value.model_response)
// La IES comenta donde trabaja el contenido; la revisión, donde revisa.
const commentReadonly = computed(
  () => (props.review ? props.preview : !editable.value))

const draft = ref({})
const baseline = ref({})

function resetDraft() {
  const fresh = buildDraft(group.value, props.observable)
  draft.value = fresh
  baseline.value = JSON.parse(JSON.stringify(fresh))
}

// La línea base se rehace cuando cambian las respuestas guardadas (al
// cargar y tras cada guardado), no con cada cambio de status.
watch(() => spec.value && group.value[spec.value.responses],
  resetDraft, { immediate: true })

const payload = computed(() => buildGroupPayload(
  group.value.question_type, draft.value, baseline.value))
const dirty = computed(() => !!payload.value)

// Valores que el backend rechazaría (negativos): se detienen aquí.
const hasInvalid = computed(() => Object.values(draft.value).some((row) =>
  Object.values(row || {}).some((v) => typeof v === 'number' && v < 0)))

const saving = ref(false)
const completion = ref(null)

async function save() {
  if (!payload.value) return true
  saving.value = true
  try {
    const before = group.value.status
    const res = await mainStore.patchSimple(
      ['group_response', group.value.id, payload.value],
      'No se pudo guardar el bloque')
    if (res.errors) return false
    const { completion: result, ...data } = res.data
    Object.assign(group.value, data)
    completion.value = result || null
    dashStore.showSnackbar('Cambios guardados')
    emit('saved', { statusChanged: before !== data.status })
    return true
  } finally {
    saving.value = false
  }
}

// El kernel del grupo; toda transición con cambios pendientes guarda
// antes, para que la compuerta del backend evalúe lo que la IES ve.
const kernel = useFlowActions(group, 'answer', 'groupresponse', {
  root: () => props.axis,
  onTransitioned: (ev) => emit('transitioned', ev),
})
// Guardar y luego transicionar, como los split-buttons de gen y bp; si el
// guardado falla, el status no se mueve.
async function saveAndTransition(t) {
  const res = await saveThenTransition(t, {
    dirty: dirty.value,
    save,
    status: () => group.value.status,
    select: kernel.onSelect,
  })
  if (res.skipped) {
    const msg = `Cambios guardados. Estatus cambiado a "${t.public_name}"`
    dashStore.showSnackbar(msg)
  }
  return res.event ?? null
}
const actions = { ...kernel, onSelect: saveAndTransition }
const { transitions, hasActions, currentStatus, sending } = kernel

// En «Por iniciar» el guardado ya pasa el grupo a «En llenado»: esa
// transición sale del menú y el guardado principal lo dice.
const doneBySave = computed(
  () => transitionDoneBySave(currentStatus.value, transitions.value))
const saveTransitions = computed(() => transitions.value
  .filter((t) => t.name !== doneBySave.value?.name))
const saveLabel = computed(() => doneBySave.value
  ? `Guardar y pasar a ${doneBySave.value.public_name}` : '')

// La IES transiciona desde el split-button mientras edita; fuera de la
// edición (pospuesto, aprobado) le quedan transiciones sin nada que
// guardar, y esas siguen en el chip-menú.
const iesChipMenu = computed(() => !props.review && showActions.value
  && !editable.value && hasActions.value)

// Sin nada que ver ni que subir, la sección de evidencia no se pinta.
const showEvidence = computed(() => editable.value
  || (group.value.flow_attachments || []).length > 0)

watchEffect(() => {
  if (group.value && !Array.isArray(group.value.flow_attachments))
    group.value.flow_attachments = []
})

const baseLink = computed(() => ({
  path: route.path, query: { ...route.query, tab: 'base' } }))
</script>

<template>
  <v-card elevation="2" class="cp-group-card mb-4">
    <div class="d-flex align-start flex-wrap ga-3 px-4 pt-3 pb-2">
      <v-icon class="mt-1 text-medium-emphasis">
        {{ type.icon || 'help' }}
      </v-icon>
      <div class="d-flex align-center">
        <span class="text-subtitle-1 font-weight-medium text-high-emphasis">
          {{ type.public_name }}
        </span>
        <v-btn
          v-if="type.description"
          icon
          variant="text"
          size="small"
          :aria-label="`Descripción: ${type.public_name}`"
        >
          <v-icon color="grey-darken-1">info</v-icon>
          <v-tooltip activator="parent" location="end" max-width="400">
            {{ type.description }}
          </v-tooltip>
        </v-btn>
      </div>
      <v-spacer />
      <FlowStatusActions
        v-if="!noCapture && ((review && showActions) || iesChipMenu)"
        v-model="group"
        app-label="answer"
        model-name="groupresponse"
        :actions="actions"
        size="small"
        variant="tonal"
        hint="tooltip"
      />
      <FlowStatusChip
        v-else
        :status="group.status"
        size="small"
        variant="tonal"
        class="mt-1"
      />
      <FlowComments
        v-if="!noCapture"
        v-model="group"
        app-label="answer"
        model-name="groupresponse"
        :width="220"
        :readonly="commentReadonly"
      />
    </div>
    <v-divider />

    <v-card-text class="text-high-emphasis">
      <v-alert
        v-if="noCapture"
        type="info"
        variant="tonal"
        density="compact"
      >
        La distribución por sexo-género de este observable se captura en
        <span v-if="review">la información base del cuestionario</span>
        <NuxtLink v-else :to="baseLink">Información base</NuxtLink>; aquí
        no hay preguntas que responder.
      </v-alert>
      <component
        :is="body"
        v-else-if="body"
        v-model="draft"
        :observable="observable"
        :options="aOptions"
        :gen-denominators="genDenominators"
        :readonly="!editable"
        :disabled="disabled"
      />

      <template v-if="!noCapture && showEvidence">
        <v-divider class="mt-5 mb-3" />
        <p class="text-subtitle-2 mb-1">Evidencia probatoria</p>
        <FlowAttachments
          v-model="group.flow_attachments"
          app-label="answer"
          model-name="groupresponse"
          :id="group.id"
          :editable="editable"
        />
      </template>

      <v-alert
        v-if="completion?.errors?.length"
        type="error"
        variant="tonal"
        density="compact"
        class="mt-4"
      >
        <div class="text-body-2 mb-1">
          Para marcar este bloque como completado falta:
        </div>
        <ul class="pl-4 text-body-2">
          <li v-for="(msg, i) in completion.errors" :key="i">{{ msg }}</li>
        </ul>
      </v-alert>
      <v-alert
        v-if="completion?.warnings?.length"
        type="warning"
        variant="tonal"
        density="compact"
        class="mt-3"
      >
        <ul class="pl-4 text-body-2">
          <li v-for="(msg, i) in completion.warnings" :key="i">{{ msg }}</li>
        </ul>
      </v-alert>

      <div
        v-if="editable && !noCapture"
        class="d-flex justify-end mt-4"
      >
        <FlowSaveMenu
          :transitions="saveTransitions"
          :current-status="currentStatus"
          :save-label="saveLabel"
          :loading="saving || sending"
          :disabled="hasInvalid"
          :save-disabled="!dirty"
          @save="save"
          @select="saveAndTransition"
        />
      </div>
    </v-card-text>

    <FlowTransitionDialogs :actions="kernel" />
  </v-card>
</template>
