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
  <!-- El name_field es `name` (la clave interna); quien edita reconoce la
       pregunta por su texto, así que ese va en el renglón. -->
  <HeaderCommon
    :main="main"
    :show_details="show_details"
    :collection_data="collection_data"
    :width="420"
  >
    <template #title>
      {{ main.text }}
    </template>
    <template #details>
      <v-chip size="small" variant="tonal" color="grey-darken-2">
        {{ main.name }}
      </v-chip>
    </template>
  </HeaderCommon>
</template>

<style scoped>

</style>
