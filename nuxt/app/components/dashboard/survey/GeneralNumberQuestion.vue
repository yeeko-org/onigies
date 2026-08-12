<script setup>
/**
 * Un renglón-pregunta de la sección «Información base»: el texto del
 * instrumento a la izquierda y la cantidad a la derecha.
 */
defineProps({
  question: { type: String, required: true },
  // Unidad corta de la cantidad («personas», «planes»), cuando el
  // instrumento la deja implícita en la redacción de la pregunta.
  unit: { type: String, default: '' },
  readonly: Boolean,
  disabled: Boolean,
})

const value = defineModel({ type: Number, default: null })

const questionId = useId()
</script>

<template>
  <div class="d-flex  flex-column ga-4">
    <span :id="questionId" class="text-body-1 general-question__text">
      {{ question }}
    </span>
    <v-count-input
      v-model="value"
      :readonly="readonly"
      :disabled="disabled"
      :suffix="unit || undefined"
      :aria-describedby="questionId"
      inputmode="numeric"
      width="160"
      max-width="160"
    />
  </div>
</template>

<style scoped>
.general-question__text {
  /* min-width: 0 deja que el texto se rompa en vez de empujar al input. */
  flex: 1 1 auto;
  min-width: 0;
}
</style>