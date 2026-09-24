<script setup>
/**
 * Pregunta especial: una proporción capturada como total y cuántos
 * cumplen. Que cumplan más que el total se marca en el campo; no impide
 * guardar, igual que el resto de la compuerta de completado.
 *
 * Las etiquetas hablan de proyectos porque la única pregunta especial del
 * instrumento (1.14) cuenta proyectos de investigación dirigidos por
 * mujeres; una especial de otro tema pediría etiquetas desde el catálogo.
 */
const props = defineProps({
  observable: { type: Object, required: true },
  readonly: Boolean,
  disabled: Boolean,
})

const draft = defineModel({ type: Object, required: true })

const questions = computed(() => props.observable.special_questions || [])

function complyingError(row) {
  if (row?.total == null || row?.complying == null) return []
  return row.complying > row.total
    ? ['No puede rebasar el total.'] : []
}
</script>

<template>
  <div>
    <div v-for="question in questions" :key="question.id" class="mb-2">
      <p class="text-body-1 font-weight-medium mb-3">
        {{ question.text }}
      </p>
      <div v-if="draft[question.id]" class="d-flex flex-wrap ga-6">
        <v-count-input
          v-model="draft[question.id].total"
          label="Total proyectos"
          :readonly="readonly"
          :disabled="disabled"
          inputmode="numeric"
          min-width="200"
          max-width="200"
        />
        <v-count-input
          v-model="draft[question.id].complying"
          label="Dirigidos por mujeres"
          :error-messages="complyingError(draft[question.id])"
          :readonly="readonly"
          :disabled="disabled"
          inputmode="numeric"
          min-width="200"
          max-width="200"
        />
      </div>
    </div>
  </div>
</template>
