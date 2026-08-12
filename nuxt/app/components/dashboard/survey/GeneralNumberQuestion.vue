<script setup>
/**
 * Un renglón-pregunta de la sección «Información base»: el texto del
 * instrumento a la izquierda y la cantidad a la derecha.
 */
defineProps({
  question: { type: String, required: true },
  // Texto de ayuda del catálogo, si la pregunta lo trae.
  hint: { type: String, default: '' },
  // Rótulo corto de la cantidad («planes», «instancias»), que el
  // catálogo resuelve como `effective_label`. Se pinta como etiqueta
  // flotante del campo.
  label: { type: String, default: '' },
  readonly: Boolean,
  disabled: Boolean,
  error: Boolean,
  // Ofrece el escape «No aplica» (planes de un nivel que la IES no
  // imparte). Sin él, un cero y un nivel inexistente se confunden.
  noApplyOption: Boolean,
})

const value = defineModel({ type: Number, default: null })
const noApply = defineModel('noApply', { type: Boolean, default: false })

const questionId = useId()
</script>

<template>
  <div class="d-flex flex-column ga-4">
    <div>
      <span :id="questionId" class="text-body-1 general-question__text">
        {{ question }}
      </span>
      <div v-if="hint" class="text-caption text-grey-darken-1 mt-1">
        {{ hint }}
      </div>
    </div>
    <div class="d-flex align-center ga-6">
      <v-count-input
        v-model="value"
        :readonly="readonly"
        :disabled="disabled || noApply"
        :error="error"
        :label="label || undefined"
        :aria-describedby="questionId"
        inputmode="numeric"
        min-width="160"
        max-width="160"
      />
      <v-checkbox
        v-if="noApplyOption"
        v-model="noApply"
        label="No aplica"
        :readonly="readonly"
        :disabled="disabled"
        color="accent"
        density="compact"
        hide-details
        class="d-inline-flex flex-grow-0"
      />
    </div>
  </div>
</template>

<style scoped>
.general-question__text {
  /* min-width: 0 deja que el texto se rompa en vez de empujar al input. */
  flex: 1 1 auto;
  min-width: 0;
}
</style>
