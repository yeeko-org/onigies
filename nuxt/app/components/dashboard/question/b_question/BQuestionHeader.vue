<script setup>
/**
 * Renglón de pregunta de transversalización.
 *
 * El título es el texto de la pregunta: el modelo no tiene
 * `name_field` y el genérico pintaría «SIN NOMBRE/TÍTULO».
 */
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

const chips = computed(() => [
  ...(props.main.includes_academic ? ['Académicas'] : []),
  ...(props.main.includes_admin ? ['Administrativas'] : []),
])

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
