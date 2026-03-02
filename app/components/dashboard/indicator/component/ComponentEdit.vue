<script setup >

import SelectGroup from "~/components/dashboard/common/select/SelectGroup.vue";

const props = defineProps({
  is_massive_edit: Boolean,
  is_edit: Boolean,
})
const full_main = defineModel({type: Object, required: true})
</script>

<template>
  <v-col cols="12" class="d-flex pa-0">

    <SelectGroup
      v-model="full_main"
      filter_group_name="axes"
      main_collection_name="component"
      forced_level="type"
      :width="400"
    />


  </v-col>
</template>

<style scoped>

</style>