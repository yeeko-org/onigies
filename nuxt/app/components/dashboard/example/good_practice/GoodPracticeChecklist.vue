<script setup>
/**
 * Checklist en vivo de completitud de una buena práctica (turno IES). Lee la
 * misma fuente de verdad que el gate de "marcar como completada"
 * (good_practice_validation.js), así el checklist, el FlowBlockedDialog y las
 * entry_rules nunca se contradicen. Cuando todo está en ✓ apunta al menú de
 * estado para marcarla como completada (intención del viejo showReadyPrompt,
 * sin reintroducir el diálogo).
 */
import { computed } from 'vue'
import {
  getChecklist,
  isPracticeComplete,
} from '~/composables/good_practice_validation.js'

const { practice } = defineProps({
  practice: { type: Object, required: true },
})

const items = computed(() => getChecklist(practice))
const complete = computed(() => isPracticeComplete(practice))
</script>

<template>
  <v-sheet border rounded="lg" class="pa-4">
    <div class="text-subtitle-2 mb-2 d-flex align-center ga-2">
      <v-icon size="small">checklist</v-icon>
      Elementos para completar la buena práctica
    </div>
    <v-list density="compact" bg-color="transparent" class="py-0">
      <v-list-item
        v-for="item in items"
        :key="item.label"
        class="px-0"
        min-height="32"
      >
        <template #prepend>
          <v-icon
            :color="item.ok ? 'success' : 'error'"
            size="small"
            class="mr-2"
          >
            {{ item.ok ? 'check_circle' : 'radio_button_unchecked' }}
          </v-icon>
        </template>
        <v-list-item-title
          :class="item.ok
            ? 'text-medium-emphasis'
            : 'text-error font-weight-medium'"
        >
          {{ item.label }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
    <v-alert
      v-if="complete"
      type="success"
      variant="tonal"
      density="compact"
      icon="done_all"
      class="mt-3"
    >
      Esta buena práctica ya está completa. Usa el menú de estado
      (arriba) para marcarla como completada.
    </v-alert>
  </v-sheet>
</template>