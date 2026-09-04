<script setup>
/**
 * Edición del texto de pregunta de transversalización, dentro del Sheet
 * de su observable.
 *
 * Las banderas de entidades académicas y dependencias administrativas
 * deciden qué tablas de captura se pintan: se muestran, no se editan.
 *
 * Todo el marco vive en ObservableQuestionEdit; este archivo existe
 * porque la convención de nombre del dashboard resuelve
 * `BQuestionEditSimple.vue`, no un componente compartido.
 */
import ObservableQuestionEdit from
  "~/components/dashboard/question/common/ObservableQuestionEdit.vue";

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

const chips = computed(() => [
  `Orden ${full_main.value.order}`,
  ...(full_main.value.includes_academic
    ? ['Entidades académicas'] : []),
  ...(full_main.value.includes_admin
    ? ['Dependencias administrativas'] : []),
])

</script>

<template>
  <ObservableQuestionEdit
    v-model="full_main"
    collection_snake="b_question"
    text_label="Pregunta de transversalización"
    :chips="chips"
    @item-saved="emits('item-saved', $event)"
  />
</template>

<style scoped>

</style>
