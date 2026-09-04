<script setup>
/**
 * Edición del texto de pregunta especial, dentro del Sheet
 * de su observable.
 *
 * Una sola por observable, y solo en los casos ad-hoc (hoy 1.14).
 *
 * Todo el marco vive en ObservableQuestionEdit; este archivo existe
 * porque la convención de nombre del dashboard resuelve
 * `SpecialQuestionEditSimple.vue`, no un componente compartido.
 */
import ObservableQuestionEdit from
  "~/components/dashboard/question/common/ObservableQuestionEdit.vue";

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

const chips = computed(() => [])

</script>

<template>
  <ObservableQuestionEdit
    v-model="full_main"
    collection_snake="special_question"
    text_label="Pregunta especial"
    :chips="chips"
    @item-saved="emits('item-saved', $event)"
  />
</template>

<style scoped>

</style>
