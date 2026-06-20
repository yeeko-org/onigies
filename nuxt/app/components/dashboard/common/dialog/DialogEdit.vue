<script setup>

import EditCommon from "~/components/dashboard/common/generic/EditCommon.vue";
import { useDynamicComponent } from "~/composables/useDynamicComponent.js";

const props = defineProps({
  collection_data: Object,
})
const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['close-dialog'])

const edit_component = useDynamicComponent(props.collection_data, 'Edit')
const sheet_component = useDynamicComponent(props.collection_data, 'Sheet')

function saveItem({res, is_new}) {
  // console.log('saveItem', res, is_new)
  emits('close-dialog', res)
}

</script>

<template>
  <v-card>
    <v-card-title class="text-h5 d-flex">
      <span v-if="!full_main.id">
        Crear {{collection_data.name}}
      </span>
      <span v-else>
        Editar {{collection_data.name}}
      </span>
      <v-spacer></v-spacer>
      <v-btn
        icon="close"
        variant="text"
        @click="emits('close-dialog')"
      >
      </v-btn>
    </v-card-title>
    <v-card-text class="py-0 px-2">
      <EditCommon
        v-model="full_main"
        :collection_name="collection_data.snake_name"
        @item-saved="saveItem"
        in_dialog
      >
        <template #edit v-if="edit_component">
          <component
            :is="edit_component"
            v-model="full_main"
            is_edit
          />
        </template>
        <template
          #sheet="{full_main}"
          v-if="sheet_component"
        >
          <component
            :is="sheet_component"
            :full_main="full_main"
            :show_details="true"
            :collection_data="collection_data"
          />
        </template>
      </EditCommon>

      <component
        v-if="sheet_component"
        :is="sheet_component"
        :full_main="full_main"
        :show_details="true"
        :collection_data="collection_data"
      />
    </v-card-text>
  </v-card>
</template>

<style scoped>

</style>