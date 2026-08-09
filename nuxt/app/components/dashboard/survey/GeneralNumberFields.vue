<script setup>
/**
 * Grupos de la sección «Información base» cuyas respuestas son columnas
 * enteras del Survey (`estructuras`, `planes_estudio`). Los campos y sus
 * etiquetas salen del esquema `GeneralGroup.fields` del catálogo, no del
 * código: la redacción de la pregunta la manda el instrumento.
 */
import GeneralNumberQuestion from
  '~/components/dashboard/survey/GeneralNumberQuestion.vue'

const props = defineProps({
  fields: { type: Array, default: () => [] },
  editable: { type: Boolean, default: false },
})

const survey = defineModel({ type: Object, required: true })

const numberFields = computed(
  () => props.fields.filter((f) => f.type === 'integer'))
</script>

<template>
  <div class="d-flex flex-column ga-4">
    <GeneralNumberQuestion
      v-for="field in numberFields"
      :key="field.name"
      v-model="survey[field.name]"
      :question="field.label"
      :unit="field.unit || ''"
      :readonly="!editable"
    />
  </div>
</template>
