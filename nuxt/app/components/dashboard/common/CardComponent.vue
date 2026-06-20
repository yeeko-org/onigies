<script setup>

import { useDynamicComponent } from "~/composables/useDynamicComponent.js";
const props = defineProps({
  collection_data: {
    type: Object,
    required: true,
  },
  full_main: {
    type: Object,
    required: true,
  },
  title: String,
})

const card_component = useDynamicComponent(props.collection_data, 'Card')
</script>

<template>
  <component
    v-if="card_component && full_main"
    :is="card_component"
    :full_main="full_main"
    :title="title"
  />
  <span v-else class="text-h6 mr-2 text-warning">
    Sin {{title || collection_data.name}}
  </span>
</template>

<style scoped>

</style>