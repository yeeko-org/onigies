<script setup>
/**
 * Grupo `forma_gobierno`: el catálogo lo declara como dos campos booleanos
 * (`decentralized` / `centralized`) porque así se lee en el instrumento, pero
 * el Survey guarda un solo booleano `is_centralized`. Las dos opciones son
 * excluyentes, así que aquí se presentan como un radio y se traducen al
 * booleano; nunca se envían dos campos.
 */
const props = defineProps({
  fields: { type: Array, default: () => [] },
  editable: { type: Boolean, default: false },
})

const survey = defineModel({ type: Object, required: true })

const labelOf = (name) => props.fields.find((f) => f.name === name)?.label || ''

const government = computed({
  get() {
    if (survey.value.is_centralized == null) return null
    return survey.value.is_centralized ? 'centralized' : 'decentralized'
  },
  set(value) {
    survey.value.is_centralized = value === 'centralized'
  },
})
</script>

<template>
  <div>
    <p class="text-body-2 mb-3">
      Señale cuál de las siguientes descripciones corresponde a la forma de
      gobierno de su institución.
    </p>
    <v-radio-group
      v-model="government"
      :readonly="!editable"
      hide-details="auto"
    >
      <v-radio value="decentralized" color="accent">
        <template #label>
          <span class="text-body-2">{{ labelOf('decentralized') }}</span>
        </template>
      </v-radio>
      <v-radio value="centralized" color="accent" class="mt-2">
        <template #label>
          <span class="text-body-2">{{ labelOf('centralized') }}</span>
        </template>
      </v-radio>
    </v-radio-group>
  </div>
</template>
