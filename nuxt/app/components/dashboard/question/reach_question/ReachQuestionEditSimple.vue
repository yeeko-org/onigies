<script setup>
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
    :chips="chips"
    @item-saved="emits('item-saved', $event)"
  />
</template>

<style scoped>

</style>
