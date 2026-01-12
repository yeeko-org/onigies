<script setup>
import { ref, computed, watch } from 'vue'
import StatusDetail from "~/components/dashboard/status/StatusDetail.vue";

const props = defineProps({
  feature: { type: Object, required: true },
  value: { type: Object, default: null },
  isStaff: { type: Boolean, default: false }
})

const emit = defineEmits(['update'])

const localValue = ref({
  has_attribute: false,
  justification: '',
  final_option: null
})

const expanded = ref(false)
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

const featureOptions = computed(() => props.feature.options || [])

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
      final_option: props.value.final_option?.id || props.value.final_option
    }
  }
}

const saveChanges = async () => {
  saving.value = true
  try {
    emit('update', {
      ...localValue.value,
      good_practice: props.value?.good_practice,
      feature: props.feature.id
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
  <v-expansion-panel :bg-color="panelColor">
    <v-expansion-panel-title>
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
          {{ localValue.has_attribute ? 'mdi-check-circle' : 'mdi-circle-outline' }}
        </v-icon>

        <div class="flex-grow-1">
          <span class="font-weight-medium">{{ feature.name }}</span>
          <span
            v-if="feature.complement"
            class="text-medium-emphasis ml-1"
          >
            - {{ feature.complement }}
          </span>
        </div>

        <v-chip
          v-if="isStaff && localValue.final_option"
          size="small"
          color="success"
          class="ml-2"
        >
          Evaluado
        </v-chip>
      </div>
    </v-expansion-panel-title>

    <v-expansion-panel-text>
      <v-alert
        v-if="feature.description"
        density="compact"
        type="info"
        variant="tonal"
        class="mb-4"
      >
        {{ feature.description }}
      </v-alert>

      <!-- Para IES: Justificación -->
      <template v-if="localValue.has_attribute && !isStaff">
        <p
          v-if="feature.reason_text"
          class="text-caption text-medium-emphasis mb-2"
        >
          {{ feature.reason_text }}
        </p>
        <v-textarea
          v-model="localValue.justification"
          label="Justificación (opcional)"
          variant="outlined"
          density="compact"
          rows="2"
          hide-details
          @blur="saveJustification"
        />

        <div class="mt-4">
          <p class="text-subtitle-2 mb-2">
            Evidencias de esta característica
          </p>
<!--          <Evidences-->
<!--            v-if="value?.id"-->
<!--            model="featuregoodpractice"-->
<!--            :parent-id="value.id"-->
<!--          />-->
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

        <p class="text-subtitle-2 mb-2">Seleccione su evaluación:</p>
        <v-btn-toggle
          :model-value="localValue.final_option"
          mandatory
          divided
          variant="outlined"
          color="primary"
          class="flex-wrap"
          @update:model-value="saveFinalOption"
        >
          <v-btn
            v-for="opt in featureOptions"
            :key="opt.id"
            :value="opt.id"
            size="small"
          >
            {{ opt.name }} ({{ opt.value }})
          </v-btn>
        </v-btn-toggle>

        <div class="mt-4">
          <p class="text-subtitle-2 mb-2">Evidencias adjuntas:</p>
<!--          <Evidences-->
<!--            v-if="value?.id"-->
<!--            model="featuregoodpractice"-->
<!--            :parent-id="value.id"-->
<!--            readonly-->
<!--          />-->
        </div>

        <v-divider class="my-4" />

<!--        <StatusDetail-->
<!--          v-if="value?.id"-->
<!--          model="featuregoodpractice"-->
<!--          field="status_validation"-->
<!--          :item-id="value.id"-->
<!--        />-->

<!--        <Comments-->
<!--          v-if="value?.id"-->
<!--          model="featuregoodpractice"-->
<!--          :parent-id="value.id"-->
<!--          class="mt-4"-->
<!--        />-->
      </template>

      <!-- Mensaje cuando no está activo -->
      <v-alert
        v-if="!localValue.has_attribute && !isStaff"
        type="info"
        variant="tonal"
        density="compact"
      >
        Marca la casilla si tu buena práctica cumple con esta característica.
      </v-alert>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

<style scoped>
.v-btn-toggle {
  gap: 4px;
}
</style>