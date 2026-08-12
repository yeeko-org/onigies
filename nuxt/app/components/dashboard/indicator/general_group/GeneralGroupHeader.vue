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
  <!-- El name_field del modelo es `name`, la clave interna del grupo; en el
       renglón manda el nombre público y la clave queda como referencia. -->
  <HeaderCommon
    :main="main"
    :show_details="show_details"
    :collection_data="collection_data"
  >
    <template #title>
      {{ main.public_name || main.title }}
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
