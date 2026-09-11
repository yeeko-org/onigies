<script setup>
import ObservableQuestionEdit from
  "~/components/dashboard/question/common/ObservableQuestionEdit.vue";
import OrgInstancesFields from
  "~/components/dashboard/question/b_question/OrgInstancesFields.vue";

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

</script>

<template>
  <ObservableQuestionEdit
    v-model="full_main"
    collection_snake="b_question"
    actions_below
    @item-saved="emits('item-saved', $event)"
  >
    <template #before>
      <OrgInstancesFields v-model="full_main" readonly />
    </template>
  </ObservableQuestionEdit>
</template>

<style scoped>

</style>
