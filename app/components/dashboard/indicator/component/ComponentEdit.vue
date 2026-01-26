<script setup >

import SelectGroup from "~/components/dashboard/common/select/SelectGroup.vue";

const props = defineProps({
  is_massive_edit: Boolean,
  is_edit: Boolean,
  full_main: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <v-col cols="12" class="d-flex pa-0">

    <SelectGroup
      filter_group_name="axes"
      :main_object="full_main"
      forced_level="type"
      :width="400"
    />


  </v-col>
</template>

<style scoped>

</style>