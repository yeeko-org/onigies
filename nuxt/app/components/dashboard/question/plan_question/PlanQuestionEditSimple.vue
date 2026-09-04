<script setup>
/**
 * Edición del texto de pregunta de planes de estudio, dentro del Sheet
 * de su observable.
 *
 * El orden es, junto con el observable, la clave natural del seed: se
 * muestra, no se edita.
 *
 * Todo el marco vive en ObservableQuestionEdit; este archivo existe
 * porque la convención de nombre del dashboard resuelve
 * `PlanQuestionEditSimple.vue`, no un componente compartido.
 */
import ObservableQuestionEdit from
  "~/components/dashboard/question/common/ObservableQuestionEdit.vue";

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

const chips = computed(() => [`Orden ${full_main.value.order}`])

</script>

<template>
  <ObservableQuestionEdit
    v-model="full_main"
    collection_snake="plan_question"
    text_label="Pregunta de planes de estudio"
    :chips="chips"
    @item-saved="emits('item-saved', $event)"
  />
</template>

<style scoped>

</style>
