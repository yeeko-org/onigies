<script setup>
/**
 * Grupos de la sección «Información base» cuyas respuestas son columnas
 * enteras del Survey (`estructuras`, `planes_estudio`). Los campos y sus
 * etiquetas salen del esquema `GeneralGroup.fields` del catálogo, no del
 * código: la redacción de la pregunta la manda el instrumento.
 */
import GeneralNumberInput from
  '~/components/dashboard/survey/GeneralNumberInput.vue'

const props = defineProps({
  fields: { type: Array, default: () => [] },
  editable: { type: Boolean, default: false },
})

const survey = defineModel({ type: Object, required: true })

const numberFields = computed(
  () => props.fields.filter((f) => f.type === 'integer'))
</script>

<template>
  <v-row>
    <v-col
      v-for="field in numberFields"
      :key="field.name"
      cols="12"
      md="6"
    >
      <GeneralNumberInput
        v-model="survey[field.name]"
        :label="field.label"
        :readonly="!editable"
      />
    </v-col>
  </v-row>
</template>
