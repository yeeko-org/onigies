<script setup>
import Evidences from "~/components/dashboard/utils/Evidences.vue";
import Comments from "~/components/dashboard/utils/Comments.vue";

const props = defineProps({
  feature: { type: Object, required: true },
  value: { type: Object, default: null },
  isStaff: { type: Boolean, default: false }
})

const emit = defineEmits(['update'])

const localValue = ref({
  has_attribute: false,
  justification: '',
  final_option: null,
  evidences: [],
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
      localValue.value.evidences = []
    }
    saveChanges()
  }
})

const feature_options = computed(() => {
  return props.feature.children.map(feature => feature.data) || []
})

const panelColor = computed(() => {
  if (!localValue.value.has_attribute) return ''
  if (props.isStaff) {
    return localValue.value.final_option ? 'green-lighten-5' : 'orange-lighten-5'
  }
  return 'blue-lighten-5'
})

const initValue = () => {
  if (props.value) {
    localValue.value = {
      id: props.value.id,
      has_attribute: props.value.has_attribute || false,
      justification: props.value.justification || '',
      final_option: props.value.final_option?.id || props.value.final_option,
      evidences: props.value.evidences || [],
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
            v-if="localValue.final_option"
            size="small"
            color="success"
            class="ml-2"
          >
            Evaluado
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
          variant="outlined"
          density="compact"
          rows="2"
          hide-details
          @blur="saveJustification"
        />

        <div class="mt-4 d-flex flex-wrap">
          <p
            class="text-subtitle-2 mt-2"
          >
            Evidencias (Opcional):
          </p>
          <Evidences
            :full_main="localValue"
            main_collection_name="feature_good_practice"
          />
        </div>
      </template>

      <!-- Para Staff: Evaluación -->
      <template v-if="isStaff && localValue.has_attribute">
        <v-alert
          v-if="localValue.justification"
          type="info"
          variant="tonal"
          density="compact"
          class="mb-4"
        >
          <strong>Justificación de la IES:</strong><br>
          {{ localValue.justification }}
        </v-alert>

        <span class="text-subtitle-2 mb-2">Evalúa la característica</span>
        <span class="text-caption text-grey-darken-1">
          ({{ feature.data.description }})
        </span>
        <v-slider
          v-model="localValue.final_option"
          :ticks="feature_options.reduce((acc, opt) => ({ ...acc, [opt.id]: opt.name }), {})"
          :min="feature_options[0]?.id"
          :max="feature_options[feature_options.length - 1]?.id"
          :step="1"
          show-ticks="always"
          tick-size="4"
          color="primary"
          track-color="grey-lighten-2"
          @update:model-value="saveFinalOption"
        >
          <template #tick-label="{ tick }">
            <span>{{ tick.label }}</span>
          </template>
        </v-slider>
        <div
          v-if="localValue.evidences.length > 0"
          class="mt-4"
        >
          <p class="text-subtitle-2 mb-2">Evidencias adjuntas:</p>
          <Evidences
            :full_main="localValue"
            main_collection_name="feature_good_practice"
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
</style>