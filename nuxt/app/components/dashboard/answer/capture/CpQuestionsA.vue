<script setup>
/**
 * Bloque A (armonización e institucionalización): el enunciado del
 * observable como encabezado y cada característica con la escala global
 * de opciones (Sí/No).
 */
const props = defineProps({
  observable: { type: Object, required: true },
  options: { type: Array, default: () => [] },
  readonly: Boolean,
  disabled: Boolean,
})

const draft = defineModel({ type: Object, required: true })

const questions = computed(() => props.observable.a_questions || [])
</script>

<template>
  <div>
    <p v-if="observable.a_main_question" class="text-body-1 font-weight-medium">
      {{ observable.a_main_question }}
    </p>
    <p
      v-if="observable.a_main_subtitle"
      class="text-body-2 text-grey-darken-1 mb-2"
    >
      {{ observable.a_main_subtitle }}
    </p>
    <div
      v-for="question in questions"
      :key="question.id"
      class="cp-a-row d-flex align-center ga-4 py-1"
    >
      <span class="text-body-2 flex-grow-1">{{ question.text }}</span>
      <v-radio-group
        v-if="draft[question.id]"
        v-model="draft[question.id].selected_option"
        :readonly="readonly"
        :disabled="disabled"
        :aria-label="question.text"
        color="accent"
        density="compact"
        inline
        hide-details
        class="flex-grow-0"
      >
        <v-radio
          v-for="option in options"
          :key="option.id"
          :label="option.text"
          :value="option.id"
        />
      </v-radio-group>
    </div>
  </div>
</template>

<style scoped>
.cp-a-row + .cp-a-row {
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}
</style>
