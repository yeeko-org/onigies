<script setup>
/**
 * Bloque de planes de estudio: un conteo por nivel. El nivel que la IES
 * declaró como «No aplica» en información base no se pregunta, y lo
 * declarado acompaña al campo como referencia.
 */
import { PLAN_LEVELS } from '~/utils/cp_capture.js'

const props = defineProps({
  observable: { type: Object, required: true },
  genDenominators: { type: Object, default: () => ({}) },
  readonly: Boolean,
  disabled: Boolean,
})

const draft = defineModel({ type: Object, required: true })

const questions = computed(() => props.observable.plan_questions || [])

const levels = computed(() => PLAN_LEVELS
  .filter((level) => !props.genDenominators?.[level.field]?.no_apply)
  .map((level) => {
    const total = props.genDenominators?.[level.field]?.value ?? null
    return {
      ...level,
      hint: total === null ? '' : `de ${total} planes declarados`,
    }
  }))
</script>

<template>
  <div>
    <div v-for="question in questions" :key="question.id" class="mb-3">
      <p class="text-body-1 mb-3">{{ question.text }}</p>
      <div v-if="draft[question.id]" class="d-flex flex-wrap ga-6">
        <v-count-input
          v-for="level in levels"
          :key="level.field"
          v-model="draft[question.id][level.field]"
          :label="level.label"
          :hint="level.hint"
          :readonly="readonly"
          :disabled="disabled"
          persistent-hint
          hide-details="auto"
          inputmode="numeric"
          min-width="200"
          max-width="200"
        />
      </div>
    </div>
    <p v-if="!levels.length" class="text-body-2 text-grey-darken-1">
      En información base se declaró que ningún nivel aplica.
    </p>
  </div>
</template>
