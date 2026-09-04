<script setup>
/**
 * Edición del texto de opción de institucionalización, dentro del Sheet
 * de su observable.
 *
 * Cada AQuestion es una opción del checklist de institucionalización; el
 * enunciado del bloque vive en el observable, en `a_main_question`.
 *
 * Todo el marco vive en ObservableQuestionEdit; este archivo existe
 * porque la convención de nombre del dashboard resuelve
 * `AQuestionEditSimple.vue`, no un componente compartido.
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
    collection_snake="a_question"
    text_label="Opción de institucionalización"
    :chips="chips"
    @item-saved="emits('item-saved', $event)"
  />
</template>

<style scoped>

</style>
