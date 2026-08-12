<script setup>
/**
 * Grupo `forma_gobierno`: una sola pregunta booleana (`is_centralized`)
 * con sus dos opciones excluyentes en `addl_config.options`, cada una
 * partida en nombre del tipo y descripción. El `value` de la opción ES
 * el booleano que se guarda en la fila de respuesta, sin traducción.
 */
import {
  questionByName, useGeneralSurvey,
} from '~/composables/useGeneralSurvey.js'

const props = defineProps({
  catalog: { type: Object, default: () => ({}) },
  editable: { type: Boolean, default: false },
  // Claves de los campos que la compuerta de completado marcó como
  // faltantes (useGeneralValidation).
  invalid: { type: Set, default: () => new Set() },
})

const survey = defineModel({ type: Object, required: true })

const { questionValue, setQuestionValue } = useGeneralSurvey(survey)

const question = computed(
  () => questionByName(props.catalog, 'is_centralized'))
const options = computed(() => question.value?.addl_config?.options || [])

const answer = computed({
  get: () => questionValue(question.value),
  set: (value) => setQuestionValue(question.value, value),
})
</script>

<template>
  <div>
    <p v-if="question" class="text-body-1 mb-3">
      {{ question.text }}
    </p>
    <p
      v-if="question?.hint"
      class="text-caption text-grey-darken-1 mb-3"
    >
      {{ question.hint }}
    </p>
    <v-radio-group
      v-model="answer"
      :readonly="!editable"
      :error="invalid.has('question:is_centralized')"
      hide-details="auto"
    >
      <v-radio
        v-for="option in options"
        :key="String(option.value)"
        :value="option.value"
        color="accent"
        class="mt-2"
      >
        <template #label>
          <span class="text-body-1">
            <strong>{{ option.name }}</strong>
            <template v-if="option.description">
              — {{ option.description }}
            </template>
          </span>
        </template>
      </v-radio>
    </v-radio-group>
    <!-- Separa la pregunta de la evidencia probatoria que pinta el panel. -->
    <v-divider class="mt-4" />
  </div>
</template>
