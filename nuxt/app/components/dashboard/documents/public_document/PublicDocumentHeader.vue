<script setup>

import HeaderCommon from "~/components/dashboard/common/generic/HeaderCommon.vue";

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
      <v-chip
        v-if="main.generator"
        prepend-icon="auto_awesome"
        class="mr-2"
      >
        Se genera desde la base
      </v-chip>
      <v-chip
        :color="main.is_published ? 'accent' : undefined"
        :prepend-icon="main.is_published ? 'public' : 'draft'"
      >
        {{ main.is_published ? 'Publicado' : 'Borrador' }}
      </v-chip>
    </template>
  </HeaderCommon>
</template>
