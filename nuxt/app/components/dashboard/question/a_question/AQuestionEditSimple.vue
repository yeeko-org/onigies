<script setup>
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
    :chips="chips"
    @item-saved="emits('item-saved', $event)"
  />
</template>

<style scoped>

</style>
