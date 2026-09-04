<script setup>
/**
 * Renglón del observable: el número es la etiqueta con la que el
 * equipo del observatorio se refiere a cada uno («1.10»), así que va
 * antes del nombre y no como dato secundario.
 */
import HeaderCommon from "~/components/dashboard/common/generic/HeaderCommon.vue";

const props = defineProps({
  main: Object,
  collection_data: Object,
  show_details: {
    type: Boolean,
    default: false,
  },
})

</script>

<template>
  <HeaderCommon
    :main="main"
    :show_details="show_details"
    :collection_data="collection_data"
    :width="420"
  >
    <template #title>
      <b class="mr-2">{{ main.number }}</b>
      {{ main.name }}
    </template>
  </HeaderCommon>
</template>

<style scoped>

</style>
