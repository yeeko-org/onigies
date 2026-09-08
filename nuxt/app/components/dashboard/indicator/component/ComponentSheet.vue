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

const { schemas } = storeToRefs(useMainStore())

const observable_collection = computed(() =>
  schemas.value?.collections_dict?.observable)

// Un componente recién creado todavía no trae la clave anidada.
const observables = computed(() => props.full_main.observables || [])

function applyItemSaved({res}) {
  const pk = observable_collection.value.pk
  const rows = props.full_main.observables || []
  const idx = rows.findIndex(row => row[pk] === res[pk])
  if (idx !== -1)
    rows[idx] = {...rows[idx], ...res}
}

</script>

<template>
  <v-card v-if="observable_collection" class="mb-4">
    <v-card-text>
      <PanelsResult
        v-if="observables.length"
        :results="observables"
        :collection_data="observable_collection"
        :total_count="observables.length"
        :show_details="show_details"
        in_sheet
        @item-saved="applyItemSaved"
      >
        <template #title>
          Observables ({{ observables.length }})
        </template>
      </PanelsResult>
      <div v-else class="text-medium-emphasis font-italic">
        Este componente todavía no tiene observables.
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>

</style>
