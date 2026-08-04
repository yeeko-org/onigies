<script setup>

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
  >
    <template #title>
      <strong> {{ main.acronym }}</strong>
    </template>
    <template #details>
      <!-- Las instituciones de prueba conviven en el mismo listado que las
           reales; el chip evita confundirlas al revisar o al reportar. -->
      <v-chip
        v-if="main.is_test"
        color="orange-darken-2"
        size="small"
        variant="flat"
        prepend-icon="science"
      >
        Test
      </v-chip>
    </template>
  </HeaderCommon>
</template>

<style scoped>

</style>