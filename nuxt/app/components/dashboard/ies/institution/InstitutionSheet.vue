<script setup>

import PanelsResult from "~/components/dashboard/common/main/PanelsResult.vue";
import InvitationList from "~/components/dashboard/ies/institution/InvitationList.vue";

import {useMainStore} from "~/store/index.js";
import {storeToRefs} from "pinia";
import CollectionDisplay from "~/components/dashboard/CollectionDisplay.vue";
const mainStore = useMainStore()
const { schemas } = storeToRefs(mainStore)

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

const package_collection_data = computed(() => {
  return schemas.value.collections_dict['good_practice_package']
})

const good_practices_collection_data = computed(() => {
  return schemas.value.collections_dict['good_practice']
})

const init_filters = computed(() => {
  return {
    institution: props.full_main.id,
  }
})

</script>

<template>

  <v-card class="mb-4">
    <v-card-text>
      <InvitationList
        :invitations="full_main.invitation_tokens || []"
        :institution-id="full_main.id"
      />
    </v-card-text>
  </v-card>
  <v-card class="mb-4">
    <v-card-text>
      <CollectionDisplay
        :parent_collection="package_collection_data"
        :init_filters="init_filters"
        :init_total_count="full_main.good_practice_packages_count"
        direct_sheet
      >
        <template #title>
          Envíos de buenas prácticas
          ({{ full_main.good_practice_packages_count }})
        </template>
      </CollectionDisplay>
    </v-card-text>
  </v-card>
  <v-card class="mb-4">
    <v-card-text>
      <CollectionDisplay
        :parent_collection="good_practices_collection_data"
        :init_filters="init_filters"
        :init_total_count="full_main.good_practices_count"
        direct_sheet
      >
        <template #title>
          Buenas prácticas
          ({{ full_main.good_practices_count }})
        </template>
      </CollectionDisplay>
    </v-card-text>
  </v-card>


</template>

<style scoped>

</style>