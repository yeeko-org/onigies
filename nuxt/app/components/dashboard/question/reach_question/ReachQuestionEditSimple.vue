<script setup>
import ObservableQuestionEdit from
  "~/components/dashboard/question/common/ObservableQuestionEdit.vue";
import ReachSectorFields from
  "~/components/dashboard/question/reach_question/ReachSectorFields.vue";

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

</script>

<template>
  <ObservableQuestionEdit
    v-model="full_main"
    collection_snake="reach_question"
    actions_below
    @item-saved="emits('item-saved', $event)"
  >
    <template #after>
      <ReachSectorFields v-model="full_main" readonly />
    </template>
  </ObservableQuestionEdit>
</template>

<style scoped>

</style>
