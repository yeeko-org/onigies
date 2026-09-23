<script setup>
/**
 * Un grupo de respuesta (un tipo de pregunta de un observable) como
 * tarjeta: título, status, las preguntas del tipo, evidencia y
 * comentarios.
 *
 * El borrador vive aquí y se guarda por grupo con un botón que solo
 * aparece con cambios: la IES captura en varias sesiones y no hay
 * autoguardado por pregunta. Al guardar, el backend devuelve la compuerta
 * de completado (`completion`), que se muestra sin bloquear el guardado:
 * dice lo que impediría marcar el grupo como completado.
 *
 * Con `review` (dashboard) nada se edita: las respuestas se leen (sin
 * atenuar, a diferencia de la consulta previa de la IES), los adjuntos se
 * ven y quedan el status y los comentarios.
 */
import { useAuthStore } from '~/store/auth.js'
import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import { useFlowStore } from '~/store/flow.js'
import { useFlowActions } from '~/composables/useFlowActions.js'
import { useQuestionTypes } from '~/composables/useQuestionTypes.js'
import {
  CP_TYPES, buildDraft, buildGroupPayload,
} from '~/utils/cp_capture.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import FlowStatusActions from
  '~/components/dashboard/flow/FlowStatusActions.vue'
import FlowTransitionDialogs from
  '~/components/dashboard/flow/FlowTransitionDialogs.vue'
import FlowComments from '~/components/dashboard/flow/FlowComments.vue'
import FlowAttachments from '~/components/dashboard/flow/FlowAttachments.vue'
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
  onTransitioned: (ev) => emit('transitioned', ev),
})
const actions = {
  ...kernel,
  onSelect: async (t) => {
    if (dirty.value && !(await save())) return null
    return kernel.onSelect(t)
  },
}

watchEffect(() => {
  if (group.value && !Array.isArray(group.value.flow_attachments))
    group.value.flow_attachments = []
})

const baseLink = computed(() => ({
  path: route.path, query: { ...route.query, tab: 'base' } }))
</script>

<template>
  <v-card variant="tonal" color="blue-grey" class="cp-group-card mb-4">
    <div class="d-flex align-start flex-wrap ga-3 px-4 pt-3 pb-1">
      <v-icon class="mt-1">{{ type.icon || 'help' }}</v-icon>
      <span class="text-subtitle-1 font-weight-medium text-high-emphasis mt-1">
        {{ type.public_name }}
      </span>
      <v-spacer />
      <FlowStatusActions
        v-if="showActions"
        v-model="group"
        app-label="answer"
        model-name="groupresponse"
        :actions="actions"
      />
      <FlowStatusChip v-else :status="group.status" x-small />
    </div>

    <v-card-text class="text-high-emphasis">
      <v-alert
        v-if="group.question_type === 'population'"
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

      <div class="d-flex align-start flex-wrap ga-4 mt-5">
        <div class="flex-grow-1">
          <p class="text-subtitle-2 mb-1">Evidencia probatoria</p>
          <FlowAttachments
            v-model="group.flow_attachments"
            app-label="answer"
            model-name="groupresponse"
            :id="group.id"
            :editable="editable"
          />
        </div>
        <FlowComments
          v-model="group"
          app-label="answer"
          model-name="groupresponse"
          :width="220"
        />
      </div>

      <div v-if="editable && dirty" class="d-flex justify-end mt-4">
        <v-btn
          variant="flat"
          prepend-icon="save"
          :loading="saving"
          :disabled="hasInvalid"
          @click="save"
        >
          Guardar
        </v-btn>
      </div>

      <div
        v-if="completion?.errors?.length"
        class="cp-completion cp-completion--error mt-3"
      >
        <div class="font-weight-medium mb-1">
          Para marcar este bloque como completado falta:
        </div>
        <ul class="pl-4">
          <li v-for="(msg, i) in completion.errors" :key="i">{{ msg }}</li>
        </ul>
      </div>
      <div
        v-if="completion?.warnings?.length"
        class="cp-completion cp-completion--warning mt-3"
      >
        <ul class="pl-4">
          <li v-for="(msg, i) in completion.warnings" :key="i">{{ msg }}</li>
        </ul>
      </div>
    </v-card-text>

    <FlowTransitionDialogs :actions="kernel" />
  </v-card>
</template>

<style scoped>
.cp-completion {
  font-size: 0.8rem;
  line-height: 1.4;
  border-radius: 6px;
  padding: 6px 10px;
}
.cp-completion--error {
  background: #fdecea;
  color: #b3261e;
}
.cp-completion--warning {
  background: #fff4e0;
  color: #8a5300;
}
</style>
