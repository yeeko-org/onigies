<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";
import PanelsResult from "~/components/dashboard/common/main/PanelsResult.vue";

const props = defineProps({
  full_main: {
    type: Object,
    required: true,
  },
  show_details: {
    type: Boolean,
    default: false,
  },
  collection_data: Object,
})

const { all_nodes, schemas } = storeToRefs(useMainStore())

// Reemplaza la iteración genérica de colecciones hijas para dejar fuera
// las buenas prácticas, que cuelgan del eje pero no son cuestionario. El
// eje no tiene payload de detalle: la lista sale del árbol en memoria.
const component_collection = computed(() =>
  schemas.value?.collections_dict?.component)

const axis_node = computed(() => {
  const root = all_nodes.value?.axes
  if (!root)
    return null
  return root.find(node => node.id === `group_${props.full_main.id}`) || null
})

const components = computed(() =>
  (axis_node.value?.children || []).map(node => ({...node.data})))

</script>

<template>
  <v-card v-if="component_collection" class="mb-4">
    <v-card-text>
      <PanelsResult
        :results="components"
        :collection_data="component_collection"
        :total_count="components.length"
        :show_details="show_details"
        in_sheet
      >
        <template #title>
          Componentes ({{ components.length }})
        </template>
      </PanelsResult>
    </v-card-text>
  </v-card>
</template>

<style scoped>

</style>
