<script setup >

const props = defineProps({
  is_massive_edit: Boolean,
  is_edit: Boolean,
  full_main: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <v-col cols="12" class="d-flex pa-0">

    <v-text-field
      v-model="full_main.acronym"
      label="Acrónimo"
      class="mr-2"
      variant="outlined"
      style="max-width: 300px;"
    ></v-text-field>
    <v-checkbox
      v-model="full_main.is_public"
      label="¿Es una institución pública?"
      class="mr-2"
      variant="outlined"
    ></v-checkbox>

  </v-col>
</template>

<style scoped>

</style>