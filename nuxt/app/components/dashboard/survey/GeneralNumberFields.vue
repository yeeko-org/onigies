<script setup>
/**
 * Grupos de la sección «Información base» cuyas respuestas son enteros
 * (`estructuras`, `planes_estudio`). Las preguntas y sus rótulos salen de
 * `GeneralGroup.questions` del catálogo, no del código: la redacción del
 * instrumento la manda el seed.
 */
import GeneralNumberQuestion from
  '~/components/dashboard/survey/GeneralNumberQuestion.vue'
import { useGeneralSurvey, allowsNoApply } from
  '~/composables/useGeneralSurvey.js'

const props = defineProps({
  // Catálogo del grupo (GeneralGroup con sus `questions`).
  catalog: { type: Object, default: () => ({}) },
  editable: { type: Boolean, default: false },
  // Claves de los campos que la compuerta de completado marcó como
  // faltantes (useGeneralValidation).
  invalid: { type: Set, default: () => new Set() },
})

const survey = defineModel({ type: Object, required: true })

const { ensureQuestionRow, isQuestionNoApply, questionValue,
  setQuestionValue } = useGeneralSurvey(survey)

const numberQuestions = computed(
  () => (props.catalog.questions || []).filter((q) => q.q_type === 'integer'))

const isNoApply = (question) => isQuestionNoApply(question.id)

// La fila de la pregunta se materializa al marcar, no al pintar: solo
// las preguntas que alguien tocó necesitan metadatos guardados.
const setNoApply = (question, value) => {
  const row = ensureQuestionRow(question.id)
  if (!row) return
  row.no_apply = value === true
  // «No aplica» y un conteo no pueden convivir: el servidor anula el
  // valor al guardar y aquí se espeja al instante.
  if (row.no_apply) setQuestionValue(question, null)
}
</script>

<template>
  <div class="d-flex flex-column ga-4">
    <!-- El divider también cierra la última pregunta: separa el bloque de
         preguntas de la evidencia probatoria que el panel pinta después. -->
    <template v-for="question in numberQuestions" :key="question.name">
      <GeneralNumberQuestion
        :model-value="questionValue(question)"
        :question="question.text"
        :hint="question.hint"
        :label="question.effective_label"
        :readonly="!editable"
        :error="invalid.has(`question:${question.name}`)"
        :no-apply-option="allowsNoApply(question)"
        :no-apply="isNoApply(question)"
        @update:model-value="setQuestionValue(question, $event)"
        @update:no-apply="setNoApply(question, $event)"
      />
      <v-divider />
    </template>
  </div>
</template>
