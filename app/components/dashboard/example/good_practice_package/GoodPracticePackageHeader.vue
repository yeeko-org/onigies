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
    <template #title>
      {{main.survey_full?.institution_full?.acronym}} - {{main.survey_full?.period}}
    </template>
    <template #details>
      <v-chip
        append-icon="lightbulb"
        color="pink"
      >
        <b class="mr-1">{{main.good_practices_count}}</b>
        Buenas Prácticas
      </v-chip>
    </template>
  </HeaderCommon>
</template>

<style scoped>

</style>
