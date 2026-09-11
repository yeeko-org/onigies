<script setup>
// Dos booleanos y no un selector de tres valores: así es el modelo y así
// extiende si aparece un tercer universo de instancias.

const INSTANCES = [
  {key: 'includes_academic', label: 'Instancias académicas'},
  {key: 'includes_admin', label: 'Instancias administrativas'},
]

const HINT = 'Marca al menos una: define a qué universo se le pregunta.'
const EMPTY_WARNING =
  'Sin ninguna marcada, la pregunta no tiene a quién preguntarle'

const props = defineProps({
  readonly: Boolean,
})

const full_main = defineModel({type: Object, required: true})

const is_empty = computed(() => !INSTANCES.some(
  entry => full_main.value[entry.key]))

</script>

<template>
  <div class="mb-2">
    <div class="text-body-2 text-medium-emphasis">
      Se pregunta a:
    </div>
    <div class="d-flex flex-wrap ga-6">
      <v-checkbox
        v-for="entry in INSTANCES"
        :key="entry.key"
        v-model="full_main[entry.key]"
        :label="entry.label"
        :readonly="props.readonly"
        density="comfortable"
        hide-details
      />
    </div>
    <div class="text-caption text-medium-emphasis">
      {{ HINT }}
    </div>
    <div v-if="is_empty" class="text-caption text-warning">
      {{ EMPTY_WARNING }}
    </div>
  </div>
</template>
