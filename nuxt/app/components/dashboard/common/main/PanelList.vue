<script setup>

import PanelCommon from "~/components/dashboard/common/main/PanelCommon.vue";
import { useDynamicComponent } from "~/composables/useDynamicComponent.js";

import {nextTick} from 'vue'

const props = defineProps({
  results: Array,
  collection_data: Object,
  sel: Object,
  show_details: {
    type: Boolean,
    default: false,
  },
  parent: String,
  is_simple: Boolean,
  main_action: String,
})

const open_panels = ref([])
const main_show_details = ref(false)

const emits = defineEmits(['select-item', 'item-saved', 'item-deleted'])

const header_component = useDynamicComponent(props.collection_data, 'Header')
const sheet_component = useDynamicComponent(props.collection_data, 'Sheet')

function deleteItem(elem_id) {
  open_panels.value = open_panels.value.filter(id => id !== elem_id)
  emits('item-deleted', elem_id)
}

function changeShowDetails() {
  nextTick(() => {
    setTimeout(() => {
      main_show_details.value = true
    }, 10)
  })
}

const elem_id = computed(() => props.collection_data.pk)

// function saveItem() {
//   emits('save-item')
// }

</script>

<template>
  <v-expansion-panels
    multiple
    v-model="open_panels"
  >
    <PanelCommon
      v-for="elem in results"
      :key="elem[elem_id]"
      :collection_data="collection_data"
      :main="elem"
      :sel="sel"
      :main_action="main_action"
      @finish-open="changeShowDetails"
      @item-saved="emits('item-saved', $event)"
      @item-deleted="deleteItem"
      @select-item="emits('select-item', $event)"
    >
      <template
        #header="{openMain}"
        v-if="header_component"
      >
        <component
          :is="header_component"
          :main="elem"
          :collection_data="collection_data"
          :show_details="show_details"
          @open-panel="openMain"
          :parent="parent"
          :is_simple="is_simple"
        />
      </template>
      <template
        v-if="sheet_component"
        #sheet="{ full_main }"
      >
        <component
          :is="sheet_component"
          :full_main="full_main"
          :show_details="main_show_details"
          :collection_data="collection_data"
        />
      </template>
    </PanelCommon>
  </v-expansion-panels>
</template>

<style scoped>

</style>