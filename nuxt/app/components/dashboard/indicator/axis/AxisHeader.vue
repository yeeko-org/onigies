<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";
import HeaderCommon from "~/components/dashboard/common/generic/HeaderCommon.vue";
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

// PanelCommon corta en `category_group`: el eje nunca pide detalle al
// backend, así que los conteos salen del árbol ya en memoria.
const axis_node = computed(() => {
  const root = all_nodes.value?.axes
  if (!root)
    return null
  return root.find(node => node.id === `group_${props.main.id}`) || null
})

const component_nodes = computed(() => axis_node.value?.children || [])

const components_count = computed(() => component_nodes.value.length)

const observables_count = computed(() => component_nodes.value.reduce(
  (acc, node) => acc + (node.children ? node.children.length : 0), 0))

</script>

<template>
  <HeaderCommon
    :main="main"
    :show_details="show_details"
    :collection_data="collection_data"
  >
    <template #details>
      <div class="d-flex ga-2">
        <HeaderChip
          :count="components_count"
          collection_name="component"
        />
        <HeaderChip
          :count="observables_count"
          collection_name="observable"
        />
      </div>
    </template>
  </HeaderCommon>
</template>

<style scoped>

</style>
