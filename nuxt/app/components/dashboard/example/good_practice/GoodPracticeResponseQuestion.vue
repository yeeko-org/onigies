<script setup>
import { computed } from 'vue'

// Bloque presentacional de la pregunta IES has_good_practices (ortogonal
// al flow): muestra la respuesta registrada o el radio Sí/No. No muta el
// paquete ni toca el motor; solo emite la intención y el padre decide.
const props = defineProps({
  hasGoodPractices: { type: Boolean, default: null },
  canEditResponse: { type: Boolean, default: false },
})

const emit = defineEmits(['respond', 'reopen'])

const responseOptions = [
  { value: true, label: 'Sí tengo buenas prácticas',
    color: 'success', icon: 'check_circle' },
  { value: false, label: 'No / No deseo responder',
    color: 'grey-darken-1', icon: 'cancel' },
]

const selectedResponse = computed(() =>
  responseOptions.find(o => o.value === props.hasGoodPractices) || {})

const responseModel = computed({
  get: () => props.hasGoodPractices,
  set: (newValue) => {
    if (newValue === true) emit('respond', true)
    else if (newValue === false) emit('respond', false)
  },
})
</script>

<template>
  <v-card-text class="text-subtitle-1 mt-3 mb-1 d-flex">
    <div class="text-indigo">
      ¿Durante los últimos cinco años, su institución ha implementado
      alguna política, programa o acción en materia de igualdad de género,
      no discriminación, cuidados corresponsables y/o
      una vida libre de violencias que, por su trascendencia o innovación,
      considere que constituya una práctica exitosa
      que pudiera ser compartida a nivel nacional?
    </div>
    <v-spacer></v-spacer>
    <div
      v-if="hasGoodPractices != null"
      class="ml-3 d-flex flex-column align-center"
      style="width: 680px;"
    >
      <v-chip
        :color="selectedResponse.color"
        :prepend-icon="selectedResponse.icon"
        variant="tonal"
        size="large"
      >
        {{ selectedResponse.label }}
      </v-chip>
      <v-btn
        v-if="canEditResponse"
        color="accent"
        variant="outlined"
        prepend-icon="undo"
        class="mt-3"
        size="small"
        @click="emit('reopen')"
      >
        Cambiar respuesta
      </v-btn>
    </div>
    <v-radio-group
      v-else-if="canEditResponse"
      v-model="responseModel"
      style="width: 680px;"
      class="ml-3"
    >
      <v-radio
        v-for="(opt, i) in responseOptions"
        :key="opt.value"
        :class="{ 'mr-3': i === 0 }"
        :label="opt.label"
        :value="opt.value"
      />
    </v-radio-group>
  </v-card-text>
</template>