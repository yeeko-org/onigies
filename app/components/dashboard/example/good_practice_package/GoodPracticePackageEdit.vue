<script setup >
import dayjs from "dayjs";

const props = defineProps({
  is_massive_edit: Boolean,
  is_edit: Boolean,
})
const full_main = defineModel({type: Object, required: true})

const sent_at = computed(() => {
  return full_main.value.sent_at
    ? dayjs(full_main.value.sent_at).format('DD/MM/YYYY')
    : null
})

const institution_full = computed(() => {
  return full_main.value.survey_full?.institution_full || {}
})

</script>

<template>
  <v-col cols="12" class="d-flex pa-0 text-h6 ga-2">
    <v-card
      v-if="full_main.survey_full"
      class="px-3 py-2" color="blue" variant="tonal"
    >
      {{institution_full.name}}
      ({{institution_full.acronym}})
    </v-card>
    <v-card class="px-3 py-2" color="indigo" variant="tonal">
      {{full_main.survey_full?.period}}
    </v-card>
    <v-card
      v-if="sent_at"
      class="px-3 py-2"
      color="green"
      variant="tonal"
    >
      Enviado el {{sent_at}}
    </v-card>

  </v-col>
</template>

<style scoped>

</style>