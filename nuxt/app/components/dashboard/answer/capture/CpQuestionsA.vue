<script setup>
/**
 * Bloque A (armonización e institucionalización): el enunciado del
 * observable como encabezado y cada característica con la escala global
 * de opciones (Sí/No).
 */
import YesNoRadio from '~/components/dashboard/common/select/YesNoRadio.vue'

const props = defineProps({
  observable: { type: Object, required: true },
  options: { type: Array, default: () => [] },
  readonly: Boolean,
  disabled: Boolean,
})

const draft = defineModel({ type: Object, required: true })

const questions = computed(() => props.observable.a_questions || [])

// La escala global llega ordenada por valor descendente (Sí antes que No).
const scale = computed(() => props.options.map(
  (option) => ({ value: option.id, text: option.text })))
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
      class="cp-a-row py-2"
    >
      <YesNoRadio
        v-if="draft[question.id]"
        v-model="draft[question.id].selected_option"
        :label="question.text"
        :options="scale"
        :readonly="readonly"
        :disabled="disabled"
      />
    </div>
  </div>
</template>

<style scoped>
.cp-a-row + .cp-a-row {
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}
</style>
