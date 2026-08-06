<script setup>
import FlowAttachments from "~/components/dashboard/flow/FlowAttachments.vue";
import Comments from "~/components/dashboard/common/utils/Comments.vue";

const props = defineProps({
  feature: { type: Object, required: true },
  value: { type: Object, default: null },
  isStaff: { type: Boolean, default: false },
  // Solo el turno del usuario habilita la edición; en false, todo es read-only.
  editable: { type: Boolean, default: true }
})

const emit = defineEmits(['update'])

// Los adjuntos NO viven aquí: se escriben en sitio sobre `value`
// (`flow_attachments`) contra su propio endpoint, fuera del ciclo
// emit → PATCH de la característica.
const localValue = ref({
  has_attribute: false,
  justification: '',
  final_option: null,
  comments: '',
})

const saving = ref(false)

const hasAttribute = computed({
  get: () => localValue.value.has_attribute,
  set: (val) => {
    localValue.value.has_attribute = val
    if (!val) {
      localValue.value.justification = ''
      localValue.value.final_option = null
    }
    saveChanges()
  }
})

const feature_options = computed(() => {
  return props.feature.children?.map(feature => feature.data) || []
})

// Una característica tiene escala evaluable solo si define opciones; "Otra"
// (is_other) no las tiene y queda fuera de la calificación de la revisora.
const hasScale = computed(() => feature_options.value.length > 0)
const isRated = computed(() => localValue.value.final_option != null)

const panelColor = computed(() => {
  if (!localValue.value.has_attribute) return ''
  if (props.isStaff) {
    return localValue.value.final_option ? 'green-lighten-5' : 'orange-lighten-5'
  }
  return 'blue-lighten-5'
})

const initValue = () => {
  if (props.value) {
    // Array garantizado para el v-model de FlowAttachments.
    if (!Array.isArray(props.value.flow_attachments))
      props.value.flow_attachments = []
    localValue.value = {
      id: props.value.id,
      has_attribute: props.value.has_attribute || false,
      justification: props.value.justification || '',
      final_option: props.value.final_option?.id || props.value.final_option,
      comments: props.value.comments || '',
    }
  }
}

const saveChanges = async () => {
  saving.value = true
  try {
    emit('update', {
      ...localValue.value,
      good_practice: props.value?.good_practice,
      feature: props.feature.data.id
    })
  } finally {
    saving.value = false
  }
}

const saveJustification = () => {
  saveChanges()
}

const saveFinalOption = (optionId) => {
  localValue.value.final_option = optionId
  saveChanges()
}

watch(() => props.value, initValue, { immediate: true, deep: true })
</script>

<template>
  <v-card
    class="my-2"
    variant="tonal"
    color="indigo"
  >
    <v-card-title style="min-height: 76px">
      <div class="d-flex align-center w-100">
        <v-checkbox
          v-if="!isStaff"
          v-model="hasAttribute"
          :disabled="!editable"
          hide-details
          density="compact"
          class="flex-grow-0 mr-2"
          @click.stop
        />
        <v-icon
          v-else
          :color="localValue.has_attribute ? 'success' : 'grey'"
          class="mr-2"
        >
          {{ localValue.has_attribute ? 'check_circle' : 'circle_outline' }}
        </v-icon>

        <div class="flex-grow-1">
          <span class="font-weight-bold">
            {{ feature.data.name }}
          </span>
          <span
            v-if="feature.data.description && !isStaff"
            class="text-medium-emphasis ml-1 text-subtitle-1"
          >
            ({{ feature.data.description }})
          </span>
        </div>
        <template v-if="isStaff">
          <v-chip
            v-if="isRated"
            size="small"
            color="success"
            class="ml-2"
          >
            Evaluado
          </v-chip>
          <v-chip
            v-else-if="hasScale && localValue.has_attribute"
            size="small"
            color="warning"
            variant="tonal"
            class="ml-2"
          >
            Sin calificar
          </v-chip>
          <Comments
            :main="localValue"
            collection_name="feature_good_practice"
          />
        </template>
      </div>
    </v-card-title>

    <v-card-text v-if="localValue.has_attribute">
<!--      <v-alert-->
<!--        v-if="feature.description"-->
<!--        density="compact"-->
<!--        type="info"-->
<!--        variant="tonal"-->
<!--        class="mb-4"-->
<!--      >-->
<!--        {{ feature.description }}-->
<!--      </v-alert>-->

      <!-- Para IES: Justificación -->
      <template v-if="localValue.has_attribute && !isStaff">
        <p
          v-if="feature.data.reason_text && false"
          class="text-subtitle-1 mb-2"
        >
          {{ feature.data.reason_text }}
        </p>
        <v-textarea
          v-model="localValue.justification"
          :label="`${feature.data.reason_text} (Opcional)`"
          :readonly="!editable"
          variant="outlined"
          density="compact"
          rows="2"
          auto-grow
          max-rows="20"
          hide-details
          @blur="saveJustification"
        />

        <div class="mt-4 d-flex flex-wrap">
          <p
            class="text-subtitle-2 mt-2"
          >
            Evidencias (Opcional):
          </p>
          <FlowAttachments
            v-if="value?.id"
            v-model="value.flow_attachments"
            app-label="example"
            model-name="featuregoodpractice"
            :id="value.id"
            :editable="editable"
            class="ml-3"
          />
        </div>
      </template>

      <!-- Para Staff: Evaluación -->
      <template v-if="isStaff && localValue.has_attribute">
        <div v-if="localValue.justification" class="mb-4">
          <div class="text-caption text-medium-emphasis mb-1">
            Justificación de la IES
          </div>
          <div class="text-body-1" style="white-space: pre-wrap;">
            {{ localValue.justification }}
          </div>
        </div>

        <span class="text-subtitle-2 mb-2">Evalúa la característica</span>
        <span class="text-caption text-grey-darken-1">
          ({{ feature.data.description }})
        </span>
        <v-slider
          v-model="localValue.final_option"
          :disabled="!editable"
          :ticks="feature_options.reduce((acc, opt) => ({ ...acc, [opt.id]: opt.name }), {})"
          :min="feature_options[0]?.id"
          :max="feature_options[feature_options.length - 1]?.id"
          :step="1"
          show-ticks="always"
          tick-size="4"
          :color="isRated ? 'primary' : 'grey-lighten-1'"
          track-color="grey-lighten-2"
          :class="{ 'slider-unrated': !isRated }"
          @update:model-value="saveFinalOption"
        >
          <template #tick-label="{ tick }">
            <span>{{ tick.label }}</span>
          </template>
        </v-slider>
        <div
          v-if="!isRated && hasScale"
          class="text-caption text-warning mb-2"
        >
          Mueve el control para asignar una calificación.
        </div>
        <!-- La revisión solo consulta la evidencia de la IES. -->
        <div
          v-if="value?.flow_attachments?.length"
          class="mt-4"
        >
          <p class="text-subtitle-2 mb-2">Evidencias adjuntas:</p>
          <FlowAttachments
            v-model="value.flow_attachments"
            app-label="example"
            model-name="featuregoodpractice"
            :id="value.id"
          />
        </div>

        <v-divider class="my-4" />
<!--        <Comments-->
<!--          v-if="value?.id"-->
<!--          model="featuregoodpractice"-->
<!--          :parent-id="value.id"-->
<!--          class="mt-4"-->
<!--        />-->
      </template>

    </v-card-text>
  </v-card>
</template>

<style scoped>
.v-btn-toggle {
  gap: 4px;
}

/* Sin calificar: thumb hueco (relleno transparente, solo borde) para que no
   parezca que ya hay un valor seleccionado a la izquierda. */
.slider-unrated :deep(.v-slider-thumb__surface) {
  background-color: rgb(var(--v-theme-surface));
  border: 2px solid rgb(var(--v-theme-grey-lighten-1));
}
</style>