<script setup>

import HeaderCommon from "~/components/dashboard/common/generic/HeaderCommon.vue";
import SelectGroup from "~/components/dashboard/common/select/SelectGroup.vue";
import HeaderChip from "~/components/dashboard/common/utils/HeaderChip.vue";
import DisplayGroup from "~/components/dashboard/common/select/DisplayGroup.vue";

const props = defineProps({
  main: Object,
  collection_data: Object,
  show_details: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <HeaderCommon
    :main="main"
    :show_details="show_details"
    :collection_data="collection_data"
  >
    <template #details>
      <v-card
        color="grey"
        rounded="lg"
        variant="outlined"
        class="mx-2 d-flex _flex-column align-center"
      >
        <DisplayGroup
          :main_object="main"
          filter_group_name="axes"
          main_collection_name="good_practice"
          forced_level="subtype"
        />
      </v-card>
    </template>
  </HeaderCommon>
</template>

<style scoped>

</style>
