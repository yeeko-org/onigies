<script setup>
import ObservableQuestionHeader from
  "~/components/dashboard/question/common/ObservableQuestionHeader.vue";

const props = defineProps({
  main: Object,
  collection_data: Object,
  show_details: {
    type: Boolean,
    default: false,
  },
})

const chips = computed(() => [`Orden ${props.main.order}`])

</script>

<template>
  <ObservableQuestionHeader
    :main="main"
    :collection_data="collection_data"
    :show_details="show_details"
    :chips="chips"
  />
</template>

<style scoped>

</style>
