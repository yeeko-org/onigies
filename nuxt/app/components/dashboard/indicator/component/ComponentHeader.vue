<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";
import HeaderCommon from "~/components/dashboard/common/generic/HeaderCommon.vue";
import DisplayGroup from "~/components/dashboard/common/select/DisplayGroup.vue";
import HeaderChip from "~/components/dashboard/common/utils/HeaderChip.vue";

const props = defineProps({
  main: Object,
  collection_data: Object,
  show_details: {
    type: Boolean,
    default: false,
  },
})

const { all_nodes } = storeToRefs(useMainStore())

const observables_count = computed(() => {
  const root = all_nodes.value?.axes
  if (!root)
    return 0
  const node = root.find(n => n.id === `type_${props.main.id}`)
  return node?.children ? node.children.length : 0
})

</script>

<template>
  <HeaderCommon
    :main="main"
    :show_details="show_details"
    :collection_data="collection_data"
  >
    <template #icon>
      <v-card
        color="grey"
        rounded="lg"
        variant="outlined"
        class="mx-2 d-flex _flex-column align-center"
      >
        <DisplayGroup
          :main_object="main"
          filter_group_name="axes"
          main_collection_name="component"
          field="axis"
          forced_level="type"
        />
      </v-card>
    </template>
    <template #details>
      <HeaderChip
        :count="observables_count"
        collection_name="observable"
      />
    </template>
  </HeaderCommon>
</template>

<style scoped>

</style>
