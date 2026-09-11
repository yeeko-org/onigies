<script setup>
// Los tres campos estructurales son columnas de ReachQuestion y viajan
// en el mismo PATCH que el texto, por eso viven dentro de la tarjeta de
// la pregunta y no en la cabecera del bloque.

import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";

const MAIN_LABEL = 'Incluye el bloque de sectores principales'
const MAIN_READONLY_LABEL = 'Sectores principales incluidos'
const MAIN_READONLY_HINT = 'Vienen del catálogo de sectores; aquí no se editan'
const OTHERS_LABEL = 'Otras poblaciones'
const MAIN_GROUP_INCLUDED = 'Sectores principales — ya incluidos por el bloque'
const PLANNING_LABEL = 'Ofrece la salida «cubierto por la planeación general»'
const PLANNING_HINT =
  'No es una población: la respuesta cae en «no focalizado».'

const props = defineProps({
  readonly: Boolean,
})

const full_main = defineModel({type: Object, required: true})

const { cats } = storeToRefs(useMainStore())

const sorted_sectors = computed(
  () => [...(cats.value?.sector || [])].sort((a, b) => a.order - b.order))

const main_sectors = computed(
  () => sorted_sectors.value.filter(row => row.is_main))

const other_sectors = computed(
  () => sorted_sectors.value.filter(row => !row.is_main))

const main_names = computed(
  () => main_sectors.value.map(row => row.name).join(', '))

const main_hint = computed(() => `Suma de golpe las ${
  main_sectors.value.length} poblaciones marcadas como principales en el `
  + 'catálogo de sectores.')

// El desplegable lleva su rótulo en `name` porque `item-title` apunta
// ahí: un subheader con `title` saldría en blanco.
const sector_items = computed(() => [
  {
    type: 'subheader',
    name: full_main.value.has_main_sectors
      ? MAIN_GROUP_INCLUDED : 'Sectores principales',
  },
  ...main_sectors.value.map(row => ({
    ...row,
    // Marcarlo aquí con el bloque encendido duplicaría la población.
    props: {disabled: !!full_main.value.has_main_sectors},
  })),
  {type: 'subheader', name: OTHERS_LABEL},
  ...other_sectors.value,
])

const others_count = computed(
  () => (full_main.value.others_sectors || []).length)

const total_count = computed(() => others_count.value
  + (full_main.value.has_main_sectors ? main_sectors.value.length : 0))

// Es el número que espeja el chip de la fila colapsada y el que se
// razona del instrumento (el POB-ESTÁNDAR de 12).
const total_hint = computed(() => {
  if (!full_main.value.has_main_sectors)
    return `${total_count.value} ${
      total_count.value === 1 ? 'población' : 'poblaciones'}`
  return `${total_count.value} poblaciones en total: ${
    main_sectors.value.length} principales + ${others_count.value} extra`
})

</script>

<template>
  <div>
    <v-checkbox
      v-model="full_main.has_main_sectors"
      :label="MAIN_LABEL"
      :readonly="props.readonly"
      :hint="main_hint"
      persistent-hint
      density="comfortable"
    />
    <!-- Los diez principales se consultan, no se eligen: como texto no
         simulan un control editable ni compiten con el select de abajo. -->
    <div
      v-if="full_main.has_main_sectors"
      class="reading-width mb-4 ml-2"
    >
      <div class="text-body-2 font-weight-medium">
        {{ MAIN_READONLY_LABEL }}
      </div>
      <div class="text-caption">{{ main_names }}</div>
      <div class="text-caption text-medium-emphasis">
        {{ MAIN_READONLY_HINT }}
      </div>
    </div>
    <v-select
      v-model="full_main.others_sectors"
      :items="sector_items"
      item-title="name"
      item-value="id"
      multiple
      :readonly="props.readonly"
      :label="OTHERS_LABEL"
      :hint="total_hint"
      persistent-hint
      variant="outlined"
      density="comfortable"
      class="reading-width mt-3"
    />
    <v-checkbox
      v-model="full_main.has_general_planning"
      :label="PLANNING_LABEL"
      :readonly="props.readonly"
      :hint="PLANNING_HINT"
      persistent-hint
      density="comfortable"
      class="mt-2"
    />
  </div>
</template>

<style scoped>
.reading-width {
  max-width: 90ch;
}
</style>
