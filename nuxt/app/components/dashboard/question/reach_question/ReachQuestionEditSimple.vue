<script setup>
/**
 * Edición del texto de pregunta de alcance de población, dentro del Sheet
 * de su observable.
 *
 * La lista de poblaciones (`has_main_sectors`, `others_sectors`) y la opción
 * de planeación general son estructura del checklist: se muestran, no se
 * editan.
 *
 * Todo el marco vive en ObservableQuestionEdit; este archivo existe
 * porque la convención de nombre del dashboard resuelve
 * `ReachQuestionEditSimple.vue`, no un componente compartido.
 */
import ObservableQuestionEdit from
  "~/components/dashboard/question/common/ObservableQuestionEdit.vue";

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

const chips = computed(() => [
  ...(full_main.value.has_main_sectors
    ? ['Sectores principales'] : []),
  ...(full_main.value.has_general_planning
    ? ['Con planeación general'] : []),
  `Sectores extra: ${(full_main.value.others_sectors || []).length}`,
])

</script>

<template>
  <ObservableQuestionEdit
    v-model="full_main"
    collection_snake="reach_question"
    text_label="Pregunta de alcance de población"
    :chips="chips"
    @item-saved="emits('item-saved', $event)"
  />
</template>

<style scoped>

</style>
