<script setup>
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
    :chips="chips"
    @item-saved="emits('item-saved', $event)"
  />
</template>

<style scoped>

</style>
